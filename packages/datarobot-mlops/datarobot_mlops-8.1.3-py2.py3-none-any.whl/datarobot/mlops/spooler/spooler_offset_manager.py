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


import datarobot.mlops.install_aliases  # noqa: F401
from builtins import object
import logging
import time
import six


logger = logging.getLogger(__name__)


class FSRecord(object):
    def __init__(self, offset, record):
        self.offset = offset
        self.record = record


class OffsetMeta(object):
    def __init__(self, partition, offset, record_id):
        self.acknowledge_received = False
        self.retry_counter = 0
        self.timestamp = time.time()
        self.offset = offset
        self.partition = partition
        self.record_id = record_id

    def inc_retry_counter(self):
        self.retry_counter += 1

    def set_timestamp(self, timestamp):
        self.timestamp = timestamp

    def get_offset(self):
        return self.offset

    def get_partition(self):
        return self.partition

    def get_record_id(self):
        return self.record_id

    def ack(self):
        self.acknowledge_received = True

    def is_ack_or_retry_exceed_limit(self, max_retry):
        return self.acknowledge_received or self.retry_counter > max_retry

    def is_expired(self, ack_deadline_ms):
        return (
                not self.acknowledge_received and
                (self.timestamp + ack_deadline_ms) < time.time()
        )


class SpoolerOffsetManager(object):
    DEFAULT_PARTITION = 0

    def __init__(self, clear_record_timeout_sec, max_retry):
        self.last_clear_records_processed = time.time()
        self.clear_record_timeout_sec = clear_record_timeout_sec
        self.max_retry = max_retry
        self.ack_records = dict()
        self.partition_map = dict()
        self.records_processed = set()

    def set_last_committed_offset(self, offset_meta):
        partition = offset_meta.get_partition()
        last_committed_offset = offset_meta.get_offset()

        if partition not in self.partition_map:
            return

        to_remove = [
            offset for offset, _ in six.iteritems(self.partition_map[partition])
            if offset <= last_committed_offset
        ]
        for key in to_remove:
            del self.partition_map[partition][key]

    def clear_records_processed(self):
        if self.last_clear_records_processed + self.clear_record_timeout_sec < time.time():
            self.records_processed.clear()
            self.last_clear_records_processed = time.time()

    def find_next_offsets(self):
        offset_map = dict()
        for partition, ack_record_map in six.iteritems(self.partition_map):
            offset_list = [
                offset_meta for _, offset_meta in six.iteritems(ack_record_map)
                if offset_meta.is_ack_or_retry_exceed_limit(self.max_retry)
            ]
            offset_map[partition] = offset_list
        return offset_map

    def find_next_offset_single_partition(self):
        return self.find_next_offsets()[self.DEFAULT_PARTITION]

    def find_next_expired_offset(self, ack_deadline_ms, partition=DEFAULT_PARTITION):
        if partition not in self.partition_map:
            return

        for _, offset_meta in six.iteritems(self.partition_map[partition]):
            if offset_meta.is_expired(ack_deadline_ms):
                return offset_meta
        return None

    def ack_record(self, offset, partition=DEFAULT_PARTITION):
        if partition not in self.partition_map:
            return

        offset_meta = self.partition_map[partition].get(offset, None)
        if offset_meta:
            offset_meta.ack()
            self.records_processed.add(offset_meta.get_record_id())

    def track_offset_record(self, offset, record_id, partition=DEFAULT_PARTITION):
        ack_record_map = self.partition_map.get(partition, dict())

        offset_meta = ack_record_map.get(offset, OffsetMeta(partition, offset, record_id))
        offset_meta.inc_retry_counter()
        offset_meta.set_timestamp(time.time())
        ack_record_map[offset] = offset_meta
        self.partition_map[partition] = ack_record_map

    def is_record_processed(self, record_id):
        return record_id in self.records_processed
