from __future__ import print_function
from __future__ import absolute_import
from __future__ import division
from __future__ import unicode_literals
#  Copyright (c) 2020 DataRobot, Inc. and its affiliates. All rights reserved.
#  Last updated 2022.
#
#  DataRobot, Inc. Confidential.
#  This is unpublished proprietary source code of DataRobot, Inc. and its affiliates.
#  The copyright notice above does not evidence any actual or intended publication of
#  such source code.
#
#  This file and its contents are subject to DataRobot Tool and Utility Agreement.
#  For details, see
#  https://www.datarobot.com/wp-content/uploads/2021/07/DataRobot-Tool-and-Utility-Agreement.pdf.

from builtins import super
from builtins import int
from builtins import str
from builtins import bytes
from builtins import map
import datarobot.mlops.install_aliases  # noqa: F401
from builtins import object
import errno
import glob
import io
import json
import logging
import os
import time
import six
import struct
import sys
import zlib

from datarobot.mlops.channel.record import Record
from datarobot.mlops.common import config
from datarobot.mlops.common.config import ConfigConstants
from datarobot.mlops.common.enums import SpoolerType, DataFormat, MLOpsSpoolAction
from datarobot.mlops.common.exception import DRSpoolerException, DRApiException
from datarobot.mlops.spooler.record_spooler import RecordSpooler
from datarobot.mlops.spooler.spooler_offset_manager import SpoolerOffsetManager, FSRecord

logger = logging.getLogger(__name__)


class FSRecordSpooler(RecordSpooler):
    DEFAULT_MAX_FILE_SIZE = 1 * 1024 * 1024 * 1024
    DEFAULT_MAX_NUM_FILES = 10
    DEFAULT_FS_SPOOLER_MESSAGE_SIZE_LIMIT_IN_BYTES = 10 * 1024 * 1024
    LAST_RECORD_DELIMITER = 0xFEEDCAFE
    MAGIC_NUMBER_RECORD = 0xDEADBEEF
    FS_SPOOLER_FILENAME = "fs_spool."
    FS_SPOOLER_VERSION = 1

    PACK_FORMAT_INTEGER = "!I"
    LAST_RECORD_DELIMITER_SIZE_BYTES = struct.calcsize(PACK_FORMAT_INTEGER)
    MAGIC_RECORD_DELIMITER_SIZE_BYTES = struct.calcsize(PACK_FORMAT_INTEGER)

    PACK_FORMAT_CHECKSUM_RECORD = "!Q"
    CHECKSUM_RECORD_SIZE_BYTES = struct.calcsize(
        PACK_FORMAT_CHECKSUM_RECORD
    )

    PACK_FORMAT_VERSION_AND_RECORD_LEN = "!3IQ"
    VERSION_AND_RECORD_LEN_SIZE_BYTES = struct.calcsize(
        PACK_FORMAT_VERSION_AND_RECORD_LEN
    )

    DEFAULT_DEQUEUE_SPOOL_META_FILENAME = "spool_meta.consumer"

    DEFAULT_FILESYSTEM_ACK_RETRY = 3
    DEFAULT_FILESYSTEM_ACK_DEADLINE_SEC = 600  # 10 minutes

    def __init__(self):
        super(FSRecordSpooler, self).__init__()

        self._spool_directory_path = None
        self._spool_file_max_size = None
        self._spool_max_files = None

        # enqueue variables
        self._enqueue_initialized = False
        self._add_checksum = None
        self._spool_capacity = None
        self._enqueue_file = None
        self._spool_data_format = DataFormat.JSON

        # file index will be incremented and start with 1
        self._enqueue_file_index = 0
        self._enqueue_current_size = 0

        # dequeue variables
        self._dequeue_initialized = False
        self._dequeue_files = []
        self._current_dequeue_file = None
        self._dequeue_fd = None
        self._dequeue_bytes_read = 0
        self._dequeue_counters = {}
        self._dequeue_lock_file = None
        self._dequeue_spool_data_format = DataFormat.JSON
        self._dequeue_metafile = None

        # fields for ack records
        self._ack_deadline = config.get_config_default(
            ConfigConstants.FILESYSTEM_ACK_DEADLINE_STR, self.DEFAULT_FILESYSTEM_ACK_DEADLINE_SEC
        )
        self._last_expired_timestamp = time.time()
        self._last_offset_acknowledge = 0
        self._spooler_offset_manager = SpoolerOffsetManager(
            self._ack_deadline, self.DEFAULT_FILESYSTEM_ACK_RETRY
        )

    @staticmethod
    def get_type():
        return SpoolerType.FILESYSTEM

    def get_required_config(self):
        return [ConfigConstants.FILESYSTEM_DIRECTORY]

    def get_optional_config(self):
        return [ConfigConstants.FILESYSTEM_MAX_NUM_FILES, ConfigConstants.FILESYSTEM_MAX_FILE_SIZE,
                ConfigConstants.SPOOLER_CHECKSUM]

    def set_config(self):
        missing = super(FSRecordSpooler, self).get_missing_config()
        if len(missing) > 0:
            raise DRSpoolerException("Configuration values missing: {}".format(missing))

        self._spool_directory_path = os.path.abspath(
            config.get_config(ConfigConstants.FILESYSTEM_DIRECTORY))
        self._spool_file_max_size = \
            config.get_config_default(ConfigConstants.FILESYSTEM_MAX_FILE_SIZE,
                                      self.DEFAULT_MAX_FILE_SIZE)
        self._spool_max_files = config.get_config_default(ConfigConstants.FILESYSTEM_MAX_NUM_FILES,
                                                          self.DEFAULT_MAX_NUM_FILES)
        self._add_checksum = config.get_config_default(ConfigConstants.SPOOLER_CHECKSUM, True)

        self._spool_capacity = self._spool_file_max_size * self._spool_max_files
        data_format_str = config.get_config_default(
            ConfigConstants.SPOOLER_DATA_FORMAT, self.JSON_DATA_FORMAT_STR
        )
        if data_format_str == self.JSON_DATA_FORMAT_STR:
            self._spool_data_format = DataFormat.JSON
            self._dequeue_spool_data_format = DataFormat.JSON
        elif data_format_str == self.BINARY_DATA_FORMAT_STR:
            self._spool_data_format = DataFormat.BYTE_ARRAY
            self._dequeue_spool_data_format = DataFormat.BYTE_ARRAY
        else:
            raise DRSpoolerException(
                "Data Format: '{}' is not supported for the Filesystem Spooler".format(
                    data_format_str
                )
            )

    def open(self, action=MLOpsSpoolAction.ENQUEUE):
        self.set_config()
        try:
            spooler_action_name = config.get_config(ConfigConstants.SPOOLER_ACTION)
            spooler_action = MLOpsSpoolAction[spooler_action_name]
        except Exception:
            spooler_action = action

        if not os.path.exists(self._spool_directory_path):
            raise DRSpoolerException(
                "Path provided {} for {} does not exist; "
                "you must create this directory yourself".format(
                    self._spool_directory_path, FSRecordSpooler.__name__
                )
            )

        if not os.path.isdir(self._spool_directory_path):
            raise DRSpoolerException(
                "Path provided {} for {} is not a directory".format(
                    self._spool_directory_path, FSRecordSpooler.__name__
                )
            )

        if not os.access(self._spool_directory_path, os.R_OK):
            raise DRSpoolerException(
                "Path provided {} for {} does not have read permission".format(
                    self._spool_directory_path, FSRecordSpooler.__name__
                )
            )

        if spooler_action == MLOpsSpoolAction.ENQUEUE or \
                spooler_action == MLOpsSpoolAction.ENQUEUE_DEQUEUE:

            if not os.access(self._spool_directory_path, os.W_OK):
                raise DRSpoolerException(
                    "Path provided {} for {} does not have write permission".format(
                        self._spool_directory_path, FSRecordSpooler.__name__
                    )
                )

            if self._spool_file_max_size <= 0:
                raise DRSpoolerException(
                    "Invalid value for spool_file_max_size {} for {}".format(
                        self._spool_file_max_size, FSRecordSpooler.__name__
                    )
                )

            if self._spool_max_files <= 0:
                raise DRSpoolerException(
                    "Invalid value for spool_max_files {} for {}".format(
                        self._spool_max_files, FSRecordSpooler.__name__
                    )
                )

            self._init_enqueue()
        if spooler_action == MLOpsSpoolAction.DEQUEUE or \
                spooler_action == MLOpsSpoolAction.ENQUEUE_DEQUEUE:
            self._init_dequeue()

    @staticmethod
    def _validate_dequeue_format(data_format):
        if data_format != DataFormat.JSON:
            raise NotImplementedError(
                """Dequeue operation is not yet implemented for the File system spooler with
                byte array data format"""
            )

    # We are interested in the latest modification file,
    # so if file was deleted, return 0.
    # In some cases, when processing is very fast (e.g. small file size in tests),
    # files can have the same modification time.
    # So sorting is performed by modification time and index.
    @staticmethod
    def key_modification_time(x):
        try:
            return os.stat(x).st_mtime, FSRecordSpooler._spool_file_index_get(x)
        except Exception:
            pass
        return 0, 0

    @staticmethod
    def _spool_file_index_get(spool_filepath):
        spool_file_name = os.path.basename(spool_filepath)
        return int(spool_file_name.split(".")[1])

    def _load_meta_file_for_dequeue(self):
        meta_filename = os.path.join(
            self._spool_directory_path, FSRecordSpooler.DEFAULT_DEQUEUE_SPOOL_META_FILENAME
        )
        self._dequeue_metafile = MetaFile(meta_filename)

    def _dequeue_end_of_file_reached(self, last_spool_file):
        return os.stat(last_spool_file).st_size <= self._dequeue_metafile.get_offset()

    def _dequeue_delete_spool_file(self, spool_file):
        self._print_dequeue_counters()
        os.remove(spool_file)

    def _load_dequeue_spool_file_list(self):
        spool_files_paths = self._read_spool_dir()
        self._dequeue_files = sorted(spool_files_paths, key=self.key_modification_time)
        if self._current_dequeue_file is not None:
            try:
                self._dequeue_files.remove(self._current_dequeue_file)
            except ValueError:
                return

    def _print_dequeue_counters(self):
        if self._current_dequeue_file is not None:
            self._logger.info("Dequeue counters for the spool file: {}".format(
                self._current_dequeue_file))
            for data_type, count in self._dequeue_counters.items():
                self._logger.info("Data Type: {} Number of records: {}".format(data_type, count))

    def _get_next_spool_file_to_dequeue(self):
        self._load_dequeue_spool_file_list()

        # No new dequeue file is present
        if len(self._dequeue_files) == 0:
            self._current_dequeue_file = None
            return False

        self._current_dequeue_file = self._dequeue_files[0]
        self._dequeue_files.remove(self._current_dequeue_file)
        self._dequeue_spool_data_format = \
            self._get_data_format_of_spool_file(self._current_dequeue_file,
                                                self._dequeue_spool_data_format)
        self._validate_dequeue_format(self._dequeue_spool_data_format)

        self._logger.info("Starting dequeue with new file: {}".format(self._current_dequeue_file))
        self._dequeue_fd = io.open(self._current_dequeue_file, "r")
        self._dequeue_bytes_read = 0
        for data_type in self._dequeue_counters:
            self._dequeue_counters[data_type] = 0
        return True

    def _check_and_create_lock_for_dequeue(self):
        prefix = "agent"
        suffix = ".lock"
        lock_files = glob.glob(os.path.join(self._spool_directory_path, prefix + "*" + suffix))
        if len(lock_files) > 0:
            # Some agent process seems to be already working on this spooler
            lock_file = os.path.basename(lock_files[0])
            agent_pid = os.path.splitext(lock_file)[0].split("_")[1]
            raise Exception("""The spool directory [{}] is currently in use by an Agent with process id
                 [pid={}].  If no agent process is running, remove the file: '{}' and then rerun the
                 command""".format(self._spool_directory_path, agent_pid, lock_files[0]))
        pid = os.getpid()
        self._dequeue_lock_file = os.path.join(
            self._spool_directory_path, "{}_{}{}".format(prefix, pid, suffix)
        )
        # Touch the lock file
        with open(self._dequeue_lock_file, "a"):
            os.utime(self._dequeue_lock_file, None)

    def _init_dequeue(self):
        self._check_and_create_lock_for_dequeue()

        self._load_meta_file_for_dequeue()
        if self._dequeue_metafile.exists():
            last_spool_file = os.path.join(
                self._spool_directory_path, self._dequeue_metafile.get_last_spool_file_name()
            )
            if not os.path.exists(last_spool_file):
                self._get_next_spool_file_to_dequeue()
                return
            dequeue_spool_data_format = \
                self._get_data_format_of_spool_file(last_spool_file,
                                                    self._dequeue_spool_data_format)
            self._validate_dequeue_format(dequeue_spool_data_format)
            if self._dequeue_end_of_file_reached(last_spool_file):
                self._dequeue_delete_spool_file(last_spool_file)
                self._get_next_spool_file_to_dequeue()
            else:
                self._current_dequeue_file = last_spool_file
                self._dequeue_bytes_read = self._dequeue_metafile.get_offset()
                self._logger.info("Starting dequeue from file '{}' @ offset: {}".format(
                    self._current_dequeue_file, self._dequeue_bytes_read)
                )
                self._dequeue_fd = io.open(self._current_dequeue_file, "r")
                self._dequeue_fd.seek(self._dequeue_bytes_read)
                self._dequeue_spool_data_format = dequeue_spool_data_format
        else:
            self._get_next_spool_file_to_dequeue()
        self._dequeue_initialized = True

    def _init_enqueue(self):
        spool_files_paths = self._read_spool_dir()
        spool_files_paths = sorted(spool_files_paths, key=self.key_modification_time)

        if len(spool_files_paths):
            self._enqueue_current_size = self._get_files_total_size(spool_files_paths)
            enqueue_filepath = spool_files_paths[-1]
            # take the largest index of all spool files
            self._enqueue_file_index = max(
                list(map(lambda x: FSRecordSpooler._spool_file_index_get(x), spool_files_paths))
            )

            current_data_format = self._get_data_format_of_spool_file(enqueue_filepath,
                                                                      self._spool_data_format)
            if current_data_format != self._spool_data_format:
                self._close_current_enqueue(enqueue_filepath, current_data_format)
                self._request_new_enqueue_file()
            else:
                if self._spool_data_format == DataFormat.BYTE_ARRAY:
                    self._init_enqueue_binary(enqueue_filepath)
                else:
                    self._init_enqueue_json(enqueue_filepath)
        else:
            self._close_current_and_request_new_enqueue_file()
        self._enqueue_initialized = True

    def _get_data_format_of_spool_file(self, spool_filepath, default):
        if os.stat(spool_filepath).st_size == 0:
            return default
        with io.open(spool_filepath, "rb") as f:
            magic = struct.unpack_from(
                "!1I", f.read(FSRecordSpooler.MAGIC_RECORD_DELIMITER_SIZE_BYTES), 0)[0]
            if magic == FSRecordSpooler.MAGIC_NUMBER_RECORD:
                return DataFormat.BYTE_ARRAY
            else:
                return DataFormat.JSON

    def _init_enqueue_json(self, enqueue_filepath):
        # if last file still has some space, then use it
        try:
            stat = os.stat(enqueue_filepath)
            if stat.st_size < self._spool_file_max_size:
                self._enqueue_file = io.open(enqueue_filepath, "a")
            else:
                self._close_current_and_request_new_enqueue_file()
        except IOError:
            pass

    def _init_enqueue_binary(self, enqueue_filepath):
        # if last file does not have LAST_RECORD_DELIMITER, continue writing into it
        try:
            if not self._file_has_last_record_delimiter(enqueue_filepath):
                self._enqueue_file = io.open(enqueue_filepath, "ab")
            else:
                self._close_current_and_request_new_enqueue_file()
        except IOError:
            pass

    # used for enqueue
    @staticmethod
    def _file_has_last_record_delimiter(filename):
        with io.open(filename, "rb") as f:
            """
            seek(offset, [whence]) params are:
            1st - offset calculated from the 2nd param;
            2nd - whence: 0-absolute position; 1-current position, 2-end.
            """
            f.seek(0, 2)
            # empty file case
            if f.tell() < FSRecordSpooler.LAST_RECORD_DELIMITER_SIZE_BYTES:
                return False
            else:
                f.seek(-FSRecordSpooler.LAST_RECORD_DELIMITER_SIZE_BYTES, 2)
                buf = f.read(FSRecordSpooler.LAST_RECORD_DELIMITER_SIZE_BYTES)

                import struct

                (last_record_delimeter,) = struct.unpack_from(
                    FSRecordSpooler.PACK_FORMAT_INTEGER, buf, 0
                )
                return last_record_delimeter == FSRecordSpooler.LAST_RECORD_DELIMITER

    # used for enqueue
    @staticmethod
    def _get_files_total_size(list_of_files):
        total_size = 0
        for filename in list_of_files:
            try:
                stat = os.stat(filename)
                total_size += stat.st_size
            except Exception:
                pass
        return total_size

    def _read_spool_dir(self):
        return glob.glob(
            os.path.join(
                self._spool_directory_path, FSRecordSpooler.FS_SPOOLER_FILENAME + "*"
            )
        )

    def _close_current_enqueue(self, filename, format):
        if format == DataFormat.BYTE_ARRAY:
            with io.open(filename, "ab") as f:
                f.write(
                    struct.pack(
                        FSRecordSpooler.PACK_FORMAT_INTEGER,
                        FSRecordSpooler.LAST_RECORD_DELIMITER,
                    )
                )

    def close(self):
        self._close_enqueue_file()
        if self._dequeue_fd is not None:
            self._dequeue_fd.close()
        if self._dequeue_lock_file is not None:
            try:
                os.remove(self._dequeue_lock_file)
            except OSError as e:
                if e.errno != errno.ENOENT:
                    raise
        self._print_dequeue_counters()

    def _close_enqueue_file(self):
        if self._enqueue_file is not None:
            self._enqueue_file.close()
            self._enqueue_file = None

    def _close_current_and_request_new_enqueue_file(self):
        if self._enqueue_file is not None:
            if self._spool_data_format == DataFormat.BYTE_ARRAY:
                self._enqueue_write_end_of_file_delimiter()
            self._close_enqueue_file()
        return self._request_new_enqueue_file()

    def _request_new_enqueue_file(self):
        if len(self._read_spool_dir()) >= self._spool_max_files:
            self._logger.warning(
                "WARNING: Filesystem spooler reached max capacity: \
                    max files: {}; max file size {}".format(
                    self._spool_max_files, self._spool_file_max_size
                )
            )
            return False

        self._enqueue_file_index += 1
        new_enqueue_filepath = os.path.join(
            self._spool_directory_path,
            self.FS_SPOOLER_FILENAME + str(self._enqueue_file_index),
        )
        if self._spool_data_format == DataFormat.BYTE_ARRAY:
            self._enqueue_file = io.open(new_enqueue_filepath, "ab")
        else:
            self._enqueue_file = io.open(new_enqueue_filepath, "a")

        return True

    def _enqueue_check_spooler_has_enough_space(self, bytes_to_write_size):
        if (
                self._enqueue_current_size
                + bytes_to_write_size
                + FSRecordSpooler.LAST_RECORD_DELIMITER_SIZE_BYTES
                > self._spool_capacity
        ):
            # recalculate how much space is taken and recheck:
            self._enqueue_current_size = self._get_files_total_size(
                self._read_spool_dir()
            )
            if (
                    self._enqueue_current_size
                    + bytes_to_write_size
                    + FSRecordSpooler.LAST_RECORD_DELIMITER_SIZE_BYTES
                    > self._spool_capacity
            ):
                self._logger.warning(
                    "WARNING: Filesystem spooler reached max capacity: \
                        max files: {}; max file size {}".format(
                        self._spool_max_files, self._spool_file_max_size
                    )
                )
                return False
        return True

    def _check_enqueue_file_has_enough_space(self, bytes_to_write_size):
        if not self._enqueue_file:
            return False
        if self._spool_data_format == DataFormat.BYTE_ARRAY:
            if (
                    self._enqueue_file.tell()
                    + bytes_to_write_size
                    + FSRecordSpooler.LAST_RECORD_DELIMITER_SIZE_BYTES
                    > self._spool_file_max_size
            ):
                return False
        else:
            if self._enqueue_file.tell() + bytes_to_write_size > self._spool_file_max_size:
                return False
        return True

    def _enqueue_write_end_of_file_delimiter(self):
        self._enqueue_file.write(
            struct.pack(
                FSRecordSpooler.PACK_FORMAT_INTEGER,
                FSRecordSpooler.LAST_RECORD_DELIMITER,
            )
        )

    def _enqueue_write_data(self, buf):
        buf_len = len(buf)
        bytes_written = self._enqueue_file.write(buf)
        if buf_len != bytes_written:
            raise DRSpoolerException(
                "Fewer bytes has been written than expected: written: {}; expected: {}.".format(
                    bytes_written, buf_len
                )
            )
        self._enqueue_current_size += buf_len
        if self._spool_data_format == DataFormat.JSON:
            self._enqueue_file.write(six.text_type("\n"))
            self._enqueue_current_size += 1

    def enqueue_single_record(self, record):
        """
        Enqueue Record object into spooler

        :param record: Record object to enqueue
        :return: True if operation succeeded, otherwise False
        """
        if not self._enqueue_initialized:
            raise DRSpoolerException("Spooler must be opened before using.")

        if not isinstance(record, Record):
            raise DRApiException("argument of type {} is expected", type(Record))

        if self._spool_data_format == DataFormat.BYTE_ARRAY:
            serialized_record = record.serialize()
            record_len = len(serialized_record)
            record_dump_size = (
                    FSRecordSpooler.VERSION_AND_RECORD_LEN_SIZE_BYTES + record_len
            )
        else:
            serialized_record = record.to_json()
            record_len = sys.getsizeof(serialized_record)
            record_dump_size = record_len + 1  # New line character

        if not self._enqueue_check_spooler_has_enough_space(record_dump_size):
            return False
        if not self._check_enqueue_file_has_enough_space(record_dump_size):
            if not self._close_current_and_request_new_enqueue_file():
                return False

        if self._spool_data_format == DataFormat.BYTE_ARRAY:
            checksum = zlib.crc32(
                bytes(serialized_record)
            ) & 0xffffffff if self._add_checksum else 0
            buf = bytearray()
            buf.extend(
                struct.pack(
                    FSRecordSpooler.PACK_FORMAT_VERSION_AND_RECORD_LEN,
                    FSRecordSpooler.MAGIC_NUMBER_RECORD,
                    FSRecordSpooler.FS_SPOOLER_VERSION,
                    record_len,
                    checksum
                )
            )
            buf.extend(serialized_record)
            self._enqueue_write_data(buf)
        else:
            self._enqueue_write_data(six.text_type(serialized_record))

        return True

    def enqueue(self, record_list):
        if not self._enqueue_initialized:
            raise DRSpoolerException("Filesystem spooler must be opened for enqueue before using.")

        status_list = []
        for record in record_list:
            status_list.append(self.enqueue_single_record(record))

        # We need to explicitly issue a flush, otherwise the last Record stays
        # in buffer until file is closed. This is especially a problem with
        # the embedded agent case, where the agent keeps waiting for the record
        # in the spool file, which is not flushed until the program exits.
        if self._enqueue_file:
            self._enqueue_file.flush()
        return status_list

    def ack_records(self, records_id_list):
        if not self.enable_dequeue_ack_record:
            return

        for record_id in records_id_list:
            fs_record = self._records_pending_ack.get(record_id, None)
            if fs_record is not None:
                self._spooler_offset_manager.ack_record(fs_record.offset)
                self._records_pending_ack.pop(record_id)
        self.commit_next_valid_offset()

    def commit_next_valid_offset(self):
        offset_meta_list = self._spooler_offset_manager.find_next_offset_single_partition()
        if len(offset_meta_list) == 0:
            return

        offset_meta_max = max(offset_meta_list, key=lambda item: item.get_offset())
        self._last_offset_acknowledge = offset_meta_max.get_offset()
        self._spooler_offset_manager.set_last_committed_offset(offset_meta_max)
        self._dequeue_metafile_update()

        for offset_meta in offset_meta_list:
            self._records_pending_ack.pop(offset_meta.get_record_id(), None)
        self._spooler_offset_manager.clear_records_processed()

    def _dequeue_metafile_update(self):
        if self.enable_dequeue_ack_record:
            offset = self._last_offset_acknowledge
        else:
            offset = self._dequeue_bytes_read
        self._dequeue_metafile.update(self._current_dequeue_file, offset)

    def get_message_byte_size_limit(self):
        if self._spool_file_max_size is None:
            self._spool_file_max_size = \
                config.get_config_default(ConfigConstants.FILESYSTEM_MAX_FILE_SIZE,
                                          self.DEFAULT_MAX_FILE_SIZE)
        return min(self._spool_file_max_size, self.DEFAULT_FS_SPOOLER_MESSAGE_SIZE_LIMIT_IN_BYTES)

    def __dict__(self):
        return {
            ConfigConstants.SPOOLER_TYPE.name: SpoolerType.FILESYSTEM.name,
            ConfigConstants.FILESYSTEM_DIRECTORY.name: self._spool_directory_path,
            ConfigConstants.FILESYSTEM_MAX_FILE_SIZE.name: self._spool_file_max_size,
            ConfigConstants.FILESYSTEM_MAX_NUM_FILES.name: self._spool_max_files,
            ConfigConstants.SPOOLER_DATA_FORMAT.name: self._spool_data_format.name,
        }

    # Used by mlops-cli for dequeue
    def empty(self):
        if len(self._dequeue_files) == 0:
            self._load_dequeue_spool_file_list()
        if self._current_dequeue_file is None:
            success = self._get_next_spool_file_to_dequeue()
            if not success:
                return True
        if self.enable_dequeue_ack_record:
            offset = self._last_offset_acknowledge
        else:
            offset = self._dequeue_bytes_read
        return (
                os.stat(self._current_dequeue_file).st_size == offset and
                len(self._dequeue_files) == 0
        )

    def dequeue(self):
        record_list = []

        if not self._dequeue_initialized:
            raise DRSpoolerException("Filesystem spooler must be opened for dequeue before using.")

        if self._current_dequeue_file is None or self._dequeue_fd is None:
            if not self._get_next_spool_file_to_dequeue():
                return record_list

        if (
                self.enable_dequeue_ack_record and
                self._last_expired_timestamp + self._ack_deadline < time.time()
        ):
            offset_meta = self._spooler_offset_manager.find_next_expired_offset(self._ack_deadline)
            if offset_meta is not None:
                record_fs = self._records_pending_ack.get(offset_meta.get_record_id())
                if not self._spooler_offset_manager.is_record_processed(
                        offset_meta.get_record_id()):
                    self._spooler_offset_manager.track_offset_record(record_fs.get_offset())
                    return record_fs.get_record()
            else:
                self._last_expired_timestamp = time.time()

        move_to_next_dequeue_file = False
        if os.stat(self._current_dequeue_file).st_size == self._dequeue_bytes_read:
            if len(self._dequeue_files) == 0:
                self._load_dequeue_spool_file_list()
                # Strictly greater because spool reload could also get the current
                # dequeue file
                if len(self._dequeue_files) > 0:
                    move_to_next_dequeue_file = True
            else:
                move_to_next_dequeue_file = True

        if move_to_next_dequeue_file:
            self._dequeue_fd.close()
            if len(self._dequeue_files) > 0:
                # We don't want to delete the last one, because some enqueue might
                # happen to it later and metafile has references to it
                self._dequeue_delete_spool_file(self._current_dequeue_file)
            if not self._get_next_spool_file_to_dequeue():
                return record_list

        try:
            record_line_str = self._dequeue_fd.readline()
            self._dequeue_bytes_read = self._dequeue_fd.tell()
            if not record_line_str:
                return record_list
        finally:
            self._dequeue_metafile_update()

        try:
            record = Record.from_json(record_line_str)
            data_type = record.get_data_type().name
            if data_type not in self._dequeue_counters:
                self._dequeue_counters[data_type] = 0
            self._dequeue_counters[data_type] += 1

            if self.enable_dequeue_ack_record:
                if self._spooler_offset_manager.is_record_processed(record.get_id()):
                    return record_list

                self._add_pending_record(
                    record.get_id(), FSRecord(self._dequeue_bytes_read, record)
                )
                self._spooler_offset_manager.track_offset_record(
                    self._dequeue_bytes_read, record.get_id()
                )
            record_list.append(record)
            return record_list
        except Exception as e:
            self._logger.error("Exception during dequeue: {}".format(e))
            return record_list


# MetaFile used for dequeue
class MetaFile(object):

    def __init__(self, meta_filename):
        self._dequeue_meta_filename = meta_filename
        if not os.path.exists(meta_filename):
            self._exists = False
            self._dequeue_offset = 0
            self._last_dequeue_spool_filename = None
            return

        self._exists = True

        with open(meta_filename, "r") as f:
            metadata = json.loads(f.read())

        if metadata is None:
            raise Exception("Invalid metadata in metafile: {}".format(meta_filename))

        if "file_name" not in metadata:
            raise Exception("Invalid metafile format: 'file_name' key is missing")

        if "offset" not in metadata:
            raise Exception("Invalid metafile format: 'offset' key is missing")

        self._last_dequeue_spool_filename = metadata["file_name"]
        self._dequeue_offset = metadata["offset"]
        logger.info("Found existing metafile with last spool file: {} Offset: {}".format(
            self._last_dequeue_spool_filename, self._dequeue_offset)
        )

    def get_last_spool_file_name(self):
        return self._last_dequeue_spool_filename

    def get_offset(self):
        return self._dequeue_offset

    def _serialize(self):
        return json.dumps(
            {
                "file_name": self._last_dequeue_spool_filename,
                "offset": self._dequeue_offset
            }
        )

    def exists(self):
        return self._exists

    def update(self, filename, offset):
        self._last_dequeue_spool_filename = os.path.basename(filename)
        self._dequeue_offset = offset
        with open(self._dequeue_meta_filename, "w") as f:
            f.write(self._serialize())
