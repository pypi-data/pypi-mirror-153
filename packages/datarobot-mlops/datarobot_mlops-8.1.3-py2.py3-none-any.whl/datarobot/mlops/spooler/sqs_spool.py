from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
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
import datarobot.mlops.install_aliases  # noqa: F401
import boto3
import sys

from datarobot.mlops.channel.record import Record
from datarobot.mlops.common import config
from datarobot.mlops.common.config import ConfigConstants, ConfigKeys
from datarobot.mlops.common.enums import SpoolerType, SQSQueueType, MLOpsSpoolAction
from datarobot.mlops.common.exception import DRSpoolerException, DRApiException
from datarobot.mlops.spooler.record_spooler import RecordSpooler


class SQSRecordSpooler(RecordSpooler):
    DEFAULT_MESSAGE_GROUP_ID = "MLOpsAgentGroup"
    FIFO_SUFFIX = ".fifo"

    # Each SQS message cannot be greater than 256KB.
    # The prediction data will be limited in 256000 bytes to leave some room for metadata
    SQS_MAX_MESSAGE_SIZE = 256000
    SQS_DEFAULT_MESSAGE_GROUP = "AAAAAAAA"
    SQS_DEFAULT_MAX_NUMBER_OF_MESSAGES = 10  # max allowed by SQS batch

    def __init__(self, sqs_client=None):
        super(SQSRecordSpooler, self).__init__()
        self.initialized = False

        self._queue_name = None
        self._queue_url = None
        self._message_group_id = None

        self._max_number_of_messages = 0
        self._queue_type = SQSQueueType.STANDARD
        self._message_byte_size_limit = self.SQS_MAX_MESSAGE_SIZE
        self._sqs_client = sqs_client

    @staticmethod
    def get_type():
        return SpoolerType.SQS

    def get_required_config(self):
        return []

    def get_optional_config(self):
        return [ConfigConstants.SQS_QUEUE_NAME, ConfigConstants.SQS_QUEUE_URL]

    def set_config(self):
        # If we move to only allowing the queue name for configuration, we can re-enable this check.
        # missing = super(SQSRecordSpooler, self).get_missing_config()
        # if len(missing) > 0:
        #     raise DRSpoolerException("Configuration values missing: {}".format(missing))
        self._queue_name = config.get_config_default(ConfigConstants.SQS_QUEUE_NAME, None)

        if self._queue_name is None:
            self._logger.info("{} is not set. Using {}."
                              .format(ConfigConstants.SQS_QUEUE_NAME.name,
                                      ConfigConstants.SQS_QUEUE_URL.name))
            self._queue_url = config.get_config_default(ConfigConstants.SQS_QUEUE_URL, None)
            if self._queue_url is None:
                raise DRSpoolerException("Configuration values missing: {}"
                                         .format(ConfigConstants.SQS_QUEUE_NAME.name))

        data_format_str = config.get_config_default(
            ConfigConstants.SPOOLER_DATA_FORMAT, self.JSON_DATA_FORMAT_STR
        )
        if data_format_str != self.JSON_DATA_FORMAT_STR:
            raise DRSpoolerException("Data Format: '{}' is not supported for the SQS Spooler"
                                     .format(data_format_str))

        self._max_number_of_messages = config.get_config_default(
            config.ConfigConstants.SPOOLER_DEQUEUE_MAX_RECORDS_PER_CALL,
            self.SQS_DEFAULT_MAX_NUMBER_OF_MESSAGES
        )
        # Use deployment id for FIFO queue message group id
        self._message_group_id = config.get_config_default(ConfigConstants.DEPLOYMENT_ID,
                                                           self.SQS_DEFAULT_MESSAGE_GROUP)

    def open(self, action=MLOpsSpoolAction.ENQUEUE):
        self.set_config()
        if self._sqs_client is None:
            try:
                self._sqs_client = boto3.client("sqs")
            except Exception as e:
                raise DRApiException("Failed to initialize AWS SQS Client with error: {}"
                                     .format(str(e)))

        if self._queue_name is not None:
            response = self._sqs_client.get_queue_url(QueueName=self._queue_name)
            self._queue_url = response["QueueUrl"]

        self._validate_url(self._queue_url)

        if self._queue_url.endswith(self.FIFO_SUFFIX):
            self._queue_type = SQSQueueType.FIFO

        self.initialized = True

    @staticmethod
    def _validate_url(url):
        if not url:
            raise DRSpoolerException("Invalid AWS SQS URL - " + url)

    def _send_sqs_batch(self, entries, status_list):
        num_messages = len(entries)
        try:
            response = self._sqs_client.send_message_batch(
                QueueUrl=self._queue_url,
                Entries=entries
            )
            if response["ResponseMetadata"]["HTTPStatusCode"] != 200:
                raise DRSpoolerException("Failed to send message to AWS SQS queue - {}"
                                         .format(self._queue_url))
            status_list += [True] * num_messages
            return num_messages
        except Exception as e:
            status_list += [False] * num_messages
            raise DRSpoolerException("Failed to send message to AWS SQS queue - "
                                     "{} with error: {}".format(self._queue_url, str(e)))

    def get_message_byte_size_limit(self):
        return self.SQS_MAX_MESSAGE_SIZE

    def enqueue(self, record_list):
        if not self.initialized:
            raise DRSpoolerException("Spooler must be opened before using.")

        records_send = 0
        entries = []
        record_list_size = 0
        status_list = []

        self._logger.debug("About to publish {} messages".format(len(record_list)))

        for idx, record in enumerate(record_list, start=1):
            record_json = record.to_json()
            entry = {
                "Id": str(idx),
                "MessageBody": record_json,
            }
            if self._queue_type == SQSQueueType.FIFO:
                entry["MessageGroupId"] = self._message_group_id

            record_size = sys.getsizeof(record_json)

            if record_size > self.get_message_byte_size_limit():
                self._logger.error("Message size {} larger than max {}"
                                   .format(record_size,
                                           self.get_message_byte_size_limit()))
                key = ConfigKeys.MLOPS_FEATURE_DATA_ROWS_IN_ONE_MESSAGE_STR
                value = super().get_feature_data_rows_in_a_message()
                self._logger.error("Try reducing the value of {}. Current setting is {}."
                                   .format(key, value))
                status_list += [False]

            else:
                # Send messages once reach max message size or exceed limit
                if len(entries) == self._max_number_of_messages \
                        or record_list_size + record_size >= self._message_byte_size_limit:
                    self._logger.debug("SQS Overflow at {} messages".format(len(entries)))
                    records_send += self._send_sqs_batch(entries, status_list)
                    self._logger.debug("Sent {} messages".format(len(entries)))
                    del entries[:]
                    record_list_size = 0

                # Add entry to list
                entries.append(entry)
                record_list_size += record_size

        if len(entries) > 0:
            records_send += self._send_sqs_batch(entries, status_list)
            self._logger.debug("Sent {} messages".format(len(entries)))

        return status_list

    def ack_records(self, record_id_list):
        if not self.enable_dequeue_ack_record or record_id_list is None:
            return

        entries = []
        for record_id in record_id_list:
            entry = self._records_pending_ack.pop(record_id)
            entries.append(entry)

        self._delete_message(entries)

    def dequeue(self):
        if not self.initialized:
            raise DRSpoolerException("Spooler must be opened before using.")

        try:
            response = self._sqs_client.receive_message(
                QueueUrl=self._queue_url,
                MaxNumberOfMessages=self._max_number_of_messages,
                VisibilityTimeout=120
            )
        except Exception as e:
            raise DRSpoolerException("Failed to receive message from AWS SQS queue - {} "
                                     "with error: {}".format(self._queue_url, str(e)))

        if response["ResponseMetadata"]["HTTPStatusCode"] != 200:
            raise DRSpoolerException("Fail to receive message from AWS SQS queue - {}"
                                     .format(self._queue_url))

        record_list = list()
        # If there is no message, the http status code is still 200. Need to check the response
        if "Messages" not in response:
            return record_list

        entries = list()
        # Send delete request for messages received
        for msg in response["Messages"]:
            entry = {"Id": msg["MessageId"], "ReceiptHandle": msg["ReceiptHandle"]}
            record = Record.from_json(msg["Body"])
            self._add_pending_record(record.get_id(), entry)
            entries.append(entry)
            record_list.append(record)

        if not self.enable_dequeue_ack_record:
            self._delete_message(entries)

        return record_list

    def _delete_message(self, entries):
        if len(entries) == 0:
            return

        self._sqs_client.delete_message_batch(
            QueueUrl=self._queue_url,
            Entries=entries
        )

    # Used by mlops-cli for dequeue
    def empty(self):
        response = self._sqs_client.get_queue_attributes(
            QueueUrl=self._queue_url,
            AttributeNames=[
                "ApproximateNumberOfMessages",
                "ApproximateNumberOfMessagesDelayed",
                "ApproximateNumberOfMessagesNotVisible",
            ]
        )
        return all([int(count) == 0 for count in response["Attributes"].values()])

    # used only for testing
    def delete_queue(self):
        self._sqs_client.delete_queue(QueueUrl=self._queue_url)

    def close(self):
        pass

    def __dict__(self):
        return {
            ConfigConstants.SPOOLER_TYPE.name: SpoolerType.SQS.name,
            ConfigConstants.SQS_QUEUE_URL.name: self._queue_url,
            ConfigConstants.SQS_QUEUE_NAME.name: self._queue_name,
        }
