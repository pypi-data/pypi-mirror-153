from __future__ import absolute_import
from __future__ import division
from __future__ import print_function
from __future__ import unicode_literals
#  Copyright (c) 2021 DataRobot, Inc. and its affiliates. All rights reserved.
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
import six
from builtins import super
from builtins import dict
import datarobot.mlops.install_aliases  # noqa: F401
from contextlib import contextmanager
import logging
import time

import certifi
from confluent_kafka import Producer, Consumer, KafkaException, KafkaError
from enum import Enum
from future.moves.urllib.parse import urlparse

from datarobot.mlops.channel.record import Record
from datarobot.mlops.common import config
from datarobot.mlops.common.config import ConfigConstants
from datarobot.mlops.common.enums import SpoolerType, MLOpsSpoolAction
from datarobot.mlops.common.exception import DRCommonException
from datarobot.mlops.common.exception import DRConfigKeyNotFound
from datarobot.mlops.common.exception import DRSpoolerException
from datarobot.mlops.constants import Constants
from datarobot.mlops.spooler.filesystem_spooler import SpoolerOffsetManager
from datarobot.mlops.spooler.record_spooler import RecordSpooler

logger = logging.getLogger(__name__)


@contextmanager
def suppress(exception_type):
    try:
        yield
    except exception_type:
        pass


class KafkaConf(Enum):
    BOOTSTRAP_SERVERS = "bootstrap.servers"
    REQUEST_TIMEOUT = "request.timeout.ms"
    SESSION_TIMEOUT = "session.timeout.ms"
    DELIVERY_TIMEOUT = "delivery.timeout.ms"
    LINGER = "linger.ms"
    SECURITY_PROTOCOL = "security.protocol"
    SSL_CA_LOCATION = "ssl.ca.location"
    SSL_KEY_LOCATION = "ssl.key.location"
    SSL_KEY_PASSWORD = "ssl.key.password"
    SASL_MECHANISM = "sasl.mechanism"
    SASL_USERNAME = "sasl.username"
    SASL_PASSWORD = "sasl.password"
    SASL_OAUTHBEARER_CONFIG = "sasl.oauthbearer.config"
    OAUTH_CALLBACK = "oauth_cb"
    GROUP_ID = "group.id"
    AUTO_OFFSET_RESET = "auto.offset.reset"
    ENABLE_AUTO_COMMIT = "enable.auto.commit"
    QUEUE_BUFFERING_MAX = "queue.buffering.max.kbytes"
    SOCKET_TIMEOUT = "socket.timeout.ms"
    METADATA_MAX_AGE = "metadata.max.age.ms"
    SOCKET_KEEPALIVE = "socket.keepalive.enable"


class KafkaRecordSpooler(RecordSpooler):
    # The largest record batch size allowed by Kafka.
    # See `message.max.bytes` https://kafka.apache.org/documentation/
    DEFAULT_KAFKA_MESSAGE_BYTE_SIZE_LIMIT = 1000000
    DEFAULT_KAFKA_CONSUMER_POLL_TIMEOUT_MS = 3000
    DEFAULT_KAFKA_CONSUMER_MAX_NUM_MESSAGES = 100

    KAFKA_DEFAULT_ACK_RETRY = 3
    KAFKA_DEFAULT_ACK_DEADLINE = 600

    def __init__(self):
        super(KafkaRecordSpooler, self).__init__()
        self._initialized = False
        self._kafka_producer_config = None
        self._kafka_consumer_config = None
        self._topic_name = None
        self._bootstrap_servers = None
        self._kafka_properties_location = None
        self._consumer = None
        self._producer = None
        self._poll_timeout_seconds = None
        self._buffer_max_wait = None
        self._max_messages_to_consume = None
        self._dequeue_enabled = False
        self._max_flush_time = None
        self._desired_message_size = None
        self._ack_deadline = config.get_config_default(
            config.ConfigConstants.KAFKA_ACK_DEADLINE_STR,
            self.KAFKA_DEFAULT_ACK_DEADLINE
        )
        self._last_rebalancing = time.time()
        self._spooler_offset_manager = SpoolerOffsetManager(
            self._ack_deadline, self.KAFKA_DEFAULT_ACK_RETRY
        )

    def get_type(self):
        return SpoolerType.KAFKA

    def get_required_config(self):
        return [
            ConfigConstants.KAFKA_BOOTSTRAP_SERVERS,
            ConfigConstants.KAFKA_TOPIC_NAME,
        ]

    def get_optional_config(self):
        return [
            ConfigConstants.KAFKA_CONSUMER_GROUP_ID,
            ConfigConstants.KAFKA_CONSUMER_MAX_NUM_MESSAGES,
            ConfigConstants.KAFKA_CONSUMER_POLL_TIMEOUT_MS,
            ConfigConstants.KAFKA_BUFFER_MAX_KB,
            ConfigConstants.KAFKA_MAX_FLUSH_MS,
            ConfigConstants.KAFKA_MESSAGE_BYTE_SIZE_LIMIT,
            ConfigConstants.KAFKA_REQUEST_TIMEOUT_MS,
            ConfigConstants.KAFKA_SESSION_TIMEOUT_MS,
            ConfigConstants.KAFKA_DELIVERY_TIMEOUT_MS,
            ConfigConstants.KAFKA_SOCKET_TIMEOUT_MS,
            ConfigConstants.KAFKA_METADATA_MAX_AGE_MS,
            ConfigConstants.KAFKA_LINGER_MS,
            ConfigConstants.KAFKA_SECURITY_PROTOCOL,
            ConfigConstants.KAFKA_SSL_CA_LOCATION,
            ConfigConstants.KAFKA_SSL_KEY_LOCATION,
            ConfigConstants.KAFKA_SSL_KEY_PASSWORD,
            ConfigConstants.KAFKA_SASL_MECHANISM,
            ConfigConstants.KAFKA_SASL_USERNAME,
            ConfigConstants.KAFKA_SASL_PASSWORD,
            ConfigConstants.KAFKA_SASL_OAUTHBEARER_CONFIG,
            ConfigConstants.KAFKA_SOCKET_KEEPALIVE,
        ]

    def get_message_byte_size_limit(self):
        return config.get_config_default(ConfigConstants.KAFKA_MESSAGE_BYTE_SIZE_LIMIT,
                                         self.DEFAULT_KAFKA_MESSAGE_BYTE_SIZE_LIMIT)

    def set_config(self):
        self._topic_name = config.get_config(ConfigConstants.KAFKA_TOPIC_NAME)
        self._max_flush_time = \
            config.get_config_default(ConfigConstants.KAFKA_MAX_FLUSH_MS, -1000) / 1000

        # The max amount of time we should need to wait for the local send buffer to free up a slot
        # should basically be the delivery timeout plus a little bit of wiggle room.
        self._buffer_max_wait = config.get_config_default(
            ConfigConstants.KAFKA_DELIVERY_TIMEOUT_MS, 300000
        ) + 1000
        self._desired_message_size = self.get_message_byte_size_limit()
        self._kafka_producer_config = self._gen_kafka_client_config()

        # NOTE: following consumer configuration is only used for testing
        if self._dequeue_enabled:
            with suppress(DRConfigKeyNotFound):
                consumer_group_id = config.get_config(ConfigConstants.KAFKA_CONSUMER_GROUP_ID)
                self._kafka_consumer_config = self._kafka_producer_config.copy()
                self._kafka_consumer_config[KafkaConf.GROUP_ID] = consumer_group_id
                self._kafka_consumer_config[KafkaConf.AUTO_OFFSET_RESET] = "earliest"
                self._kafka_consumer_config[KafkaConf.ENABLE_AUTO_COMMIT] = \
                    not self.enable_dequeue_ack_record

    def _gen_kafka_client_config(self):
        _config = {}
        self._bootstrap_servers = config.get_config(ConfigConstants.KAFKA_BOOTSTRAP_SERVERS)
        _config[KafkaConf.BOOTSTRAP_SERVERS] = self._bootstrap_servers

        # It is recommended to use certifi to provide a consistent experience across *all* OSes
        # if the user didn't provide a CA location.
        _config[KafkaConf.SSL_CA_LOCATION] = config.get_config_default(
            ConfigConstants.KAFKA_SSL_CA_LOCATION, certifi.where())

        with suppress(DRConfigKeyNotFound):
            sasl_mechanism = config.get_config(ConfigConstants.KAFKA_SASL_MECHANISM).upper()
            _config[KafkaConf.SASL_MECHANISM] = sasl_mechanism
            if sasl_mechanism == "OAUTHBEARER":
                oauth_conf_str = config.get_config_default(
                    ConfigConstants.KAFKA_SASL_OAUTHBEARER_CONFIG, ""
                )
                _config[KafkaConf.SASL_OAUTHBEARER_CONFIG] = oauth_conf_str
                oauth_handler = AzureActiveDirectoryOauthBearer.from_config_str(
                    oauth_conf_str, self._bootstrap_servers
                )
                _config[KafkaConf.OAUTH_CALLBACK] = oauth_handler

        with suppress(DRConfigKeyNotFound):
            _config[KafkaConf.REQUEST_TIMEOUT] = config.get_config(
                ConfigConstants.KAFKA_REQUEST_TIMEOUT_MS)

        with suppress(DRConfigKeyNotFound):
            _config[KafkaConf.SESSION_TIMEOUT] = config.get_config(
                ConfigConstants.KAFKA_SESSION_TIMEOUT_MS)

        with suppress(DRConfigKeyNotFound):
            _config[KafkaConf.DELIVERY_TIMEOUT] = config.get_config(
                ConfigConstants.KAFKA_DELIVERY_TIMEOUT_MS)

        with suppress(DRConfigKeyNotFound):
            _config[KafkaConf.SOCKET_KEEPALIVE] = config.get_config(
                ConfigConstants.KAFKA_SOCKET_KEEPALIVE)

        with suppress(DRConfigKeyNotFound):
            _config[KafkaConf.SOCKET_TIMEOUT] = config.get_config(
                ConfigConstants.KAFKA_SOCKET_TIMEOUT_MS)

        with suppress(DRConfigKeyNotFound):
            _config[KafkaConf.QUEUE_BUFFERING_MAX] = config.get_config(
                ConfigConstants.KAFKA_BUFFER_MAX_KB)

        with suppress(DRConfigKeyNotFound):
            _config[KafkaConf.METADATA_MAX_AGE] = config.get_config(
                ConfigConstants.KAFKA_METADATA_MAX_AGE_MS)

        with suppress(DRConfigKeyNotFound):
            _config[KafkaConf.LINGER] = config.get_config(
                ConfigConstants.KAFKA_LINGER_MS)

        with suppress(DRConfigKeyNotFound):
            _config[KafkaConf.SECURITY_PROTOCOL] = config.get_config(
                ConfigConstants.KAFKA_SECURITY_PROTOCOL)

        with suppress(DRConfigKeyNotFound):
            _config[KafkaConf.SSL_KEY_LOCATION] = config.get_config(
                ConfigConstants.KAFKA_SSL_KEY_LOCATION)

        with suppress(DRConfigKeyNotFound):
            _config[KafkaConf.SSL_KEY_PASSWORD] = config.get_config(
                ConfigConstants.KAFKA_SSL_KEY_PASSWORD)

        with suppress(DRConfigKeyNotFound):
            _config[KafkaConf.SASL_USERNAME] = config.get_config(
                ConfigConstants.KAFKA_SASL_USERNAME)

        with suppress(DRConfigKeyNotFound):
            _config[KafkaConf.SASL_PASSWORD] = config.get_config(
                ConfigConstants.KAFKA_SASL_PASSWORD)

        return _config

    def open(self, action=MLOpsSpoolAction.ENQUEUE):
        self._dequeue_enabled = (action is MLOpsSpoolAction.DEQUEUE or
                                 action is MLOpsSpoolAction.ENQUEUE_DEQUEUE)
        self.set_config()

        self._poll_timeout_seconds = config.get_config_default(
            ConfigConstants.KAFKA_CONSUMER_POLL_TIMEOUT_MS,
            self.DEFAULT_KAFKA_CONSUMER_POLL_TIMEOUT_MS,
        ) / 1000
        self._max_messages_to_consume = config.get_config_default(
            ConfigConstants.KAFKA_CONSUMER_MAX_NUM_MESSAGES,
            self.DEFAULT_KAFKA_CONSUMER_MAX_NUM_MESSAGES,
        )

        try:
            producer_settings = {k.value: v for k, v in self._kafka_producer_config.items()}
            self._producer = Producer(producer_settings,
                                      on_delivery=self._delivery_status_callback,
                                      logger=logging.getLogger("kafka.producer"))
            self._producer.poll(0)  # Make sure oauth callback triggered

            if self._dequeue_enabled:
                consumer_settings = {k.value: v for k, v in self._kafka_consumer_config.items()}
                self._consumer = Consumer(
                    consumer_settings, logger=logging.getLogger("kafka.consumer")
                )
                self._consumer.poll(0)  # Make sure oauth callback triggered
                self._consumer.subscribe([self._topic_name])

            self._initialized = True

        except Exception:
            self._logger.error("Failed to initialize Kafka client.", exc_info=True)
            raise DRCommonException

    # Used by mlops-cli for dequeue
    def empty(self):
        return self._empty_count >= self.DEFAULT_CONSUMER_MAX_FETCH_BEFORE_SET_EMPTY

    def close(self):
        if self._producer:
            self._logger.info("Waiting for %s buffered messages to flush (%ss)...",
                              len(self._producer), self._max_flush_time)
            self._producer.flush(self._max_flush_time)
            if len(self._producer) > 0:
                self._logger.warning("Failed to flush all buffered messages: %s",
                                     len(self._producer))
            self._producer = None
            self._logger.debug("Kafka producer closed.")

        if self._consumer:
            self._consumer.close()
            self._consumer = None
            self._logger.debug("Kafka consumer closed.")

    def enqueue(self, record_list):
        if not self._initialized:
            raise DRSpoolerException("Spooler must be opened before using.")

        self._logger.debug("Publishing %s records", len(record_list))
        status_list = []

        if len(record_list) < 1:
            return status_list

        for record in record_list:
            try:
                self._publish_single_record(record)

                # The 'status_list' here is used only to obey the RecordSpooler interface.
                # Send status may be obtained only via the blocking operation future.get(),
                # which we can't call on a consumer's thread.
                status_list.append(True)
            except (KafkaException, DRSpoolerException):
                self._logger.error("Failed to publish a message to Kafka", exc_info=True)
                status_list.append(False)

        self._logger.debug("Published %s messages", len(status_list))
        return status_list

    def _publish_single_record(self, record):
        record_json = record.to_json()
        record_bytearray = record_json.encode("utf-8")
        record_size = len(record_bytearray)

        if record_size > self._desired_message_size:
            self._logger.warning("Attempting to enqueue large record: %s bytes", record_size)

        tries = 5  # only retry a handful of times before giving up
        # TODO: convert to generic channel back-pressure interface when available
        while tries > 0:
            try:
                self._producer.produce(
                    self._topic_name,
                    value=record_bytearray,
                )
                break  # no need to loop if no error
            except BufferError:
                tries -= 1
                self._logger.warning("Local Kafka send buffer is full; backing off...")
                # TODO: could more intelligently set poll timeout based on request.timeout.ms,
                # socket.timeout.ms and delivery.timeout.ms values.
                if tries != 0:
                    self._producer.poll(self._buffer_max_wait)
        else:
            raise DRSpoolerException("Unable to publish record due to full local buffer.")
        # used to trigger delivery report callbacks for previously delivered records
        self._producer.poll(0)

    def commit_next_valid_offset(self):
        offset_meta_map = self._spooler_offset_manager.find_next_offsets()
        for partition, offset_meta_list in six.iteritems(offset_meta_map):
            if len(offset_meta_list) == 0:
                continue

            offset_meta_max = max(offset_meta_list, key=lambda item: item.get_offset())
            consumer_message = self._records_pending_ack.get(offset_meta_max.get_record_id())
            if consumer_message is not None:
                self._consumer.commit(consumer_message)
                self._spooler_offset_manager.set_last_committed_offset(offset_meta_max)

            for offset_meta in offset_meta_list:
                self._records_pending_ack.pop(offset_meta.get_record_id(), None)
            self._spooler_offset_manager.clear_records_processed()

    def ack_records(self, records_id_list):
        if not self.enable_dequeue_ack_record:
            return
        for record_id in records_id_list:
            record = self._records_pending_ack.get(record_id, None)
            if record:
                self._spooler_offset_manager.ack_record(record.offset(), record.partition())

    def dequeue(self):
        if not self._initialized:
            raise DRSpoolerException("Spooler must be opened before using.")

        if self.enable_dequeue_ack_record:
            self.commit_next_valid_offset()

            if self._last_rebalancing + self._ack_deadline < time.time():
                self._last_rebalancing = time.time()
                self._consumer.unsubscribe()
                self._consumer.subscribe([self._topic_name])
            self._spooler_offset_manager.clear_records_processed()

        record_list = []
        try:
            messages = self._consumer.consume(
                num_messages=self._max_messages_to_consume, timeout=self._poll_timeout_seconds)

        except KafkaError:
            self._logger.error("Unable to dequeue messages.", exc_info=True)
            return record_list

        for msg in messages:
            record = self._read_single_message(msg)
            if record is not None and (
                    not self.enable_dequeue_ack_record
                    or
                    not self._spooler_offset_manager.is_record_processed(record.get_id())
            ):
                record_list.append(record)
                if self.enable_dequeue_ack_record:
                    self._add_pending_record(record.get_id(), msg)
                    self._spooler_offset_manager.track_offset_record(
                        msg.offset(), record.get_id(), msg.partition()
                    )

        if len(record_list) == 0:
            self._empty_count += 1
        else:
            self._empty_count = 0

        return record_list

    def _read_single_message(self, msg):

        if msg is None:
            self._logger.debug("Consumer assigned to topics: %s", self._consumer.assignment())
            return None

        self._logger.debug(
            "Received message from topic %s partition [%s] @ offset %s",
            msg.topic(), msg.partition(), msg.offset()
        )

        if msg.error():
            # skip broker messages about an empty queue
            if msg.error().code() != KafkaError._PARTITION_EOF:
                self._logger.error(msg.error())
            return None

        try:
            msg_bytes = msg.value()
            message_json = msg_bytes.decode("utf-8")
            record = Record.from_json(message_json)
        except UnicodeDecodeError:
            self._logger.error("Unable to deserialize message", exc_info=True)
            return None

        return record

    def _delivery_status_callback(self, err, msg):
        if err is not None:
            # TODO: other than this log message, this is more or less a silent error in that we
            #       don't bubble it up to the upstream code to try and deal with (i.e. retry)
            self._logger.error("Failed to deliver message: %s", err)
        else:
            self._logger.debug(
                "Produced record to topic %s partition [%s] @ offset %s (%ss)",
                msg.topic(), msg.partition(), msg.offset(), msg.latency(),
            )

    def __dict__(self):
        return {
            ConfigConstants.SPOOLER_TYPE.name: SpoolerType.KAFKA.name,
            ConfigConstants.KAFKA_TOPIC_NAME.name: self._topic_name,
            ConfigConstants.KAFKA_BOOTSTRAP_SERVERS.name: self._bootstrap_servers,
            ConfigConstants.KAFKA_MAX_FLUSH_MS.name: int(self._max_flush_time * 1000),
        }


class AzureActiveDirectoryOauthBearer(object):
    AUTHORITY_TEMPLATE = "https://login.microsoftonline.com/{}/"
    AAD_TENANT_ID = "aad.tenant.id"
    AAD_CLIENT_ID = "aad.client.id"
    AAD_CLIENT_SECRET = "aad.client.secret"

    def __init__(self, tenant_id, client_id, client_secret, scopes):
        # Delay import since the dep is optional as only Azure Event Hubs users will want to use
        # this auth method.
        try:
            import msal
        except ImportError:
            message = ("Azure Active Directory Authentication failed; missing package; "
                       "need to `pip install {}[azure]`".format(Constants.OFFICIAL_NAME))
            raise RuntimeError(message)

        authority = self.AUTHORITY_TEMPLATE.format(tenant_id)
        self.app = msal.ConfidentialClientApplication(
            client_id,
            authority=authority,
            client_credential=client_secret,
        )
        self.scopes = scopes

    @classmethod
    def from_config_str(cls, config_string, bootstrap_servers):
        oauthbearer_config = dict(x.strip().split("=") for x in config_string.split(","))
        logger.debug("Parsed config str: %s", oauthbearer_config)

        _bootstrap_server = bootstrap_servers.split(",")[0].strip()
        logger.debug("Parsed bootstrap server: %s", _bootstrap_server)
        _uri = urlparse("https://" + _bootstrap_server)
        scope = "{}://{}/.default".format(_uri.scheme, _uri.hostname)
        logger.debug("Generated scope: %s", scope)
        return cls(tenant_id=oauthbearer_config[cls.AAD_TENANT_ID],
                   client_id=oauthbearer_config[cls.AAD_CLIENT_ID],
                   client_secret=oauthbearer_config[cls.AAD_CLIENT_SECRET],
                   scopes=[scope])

    def __call__(self, _config):
        """
        Note here value of _config comes from sasl.oauthbearer.config below.
        It is not used in this this case.
        """
        # Firstly, looks up a token from cache
        # Since we are looking for token for the current app, NOT for an end user,
        # notice we give account parameter as None.
        result = self.app.acquire_token_silent(self.scopes, account=None)
        if not result:
            logging.info("No suitable token exists in cache. Let's get a new one from AAD.")
            result = self.app.acquire_token_for_client(self.scopes)

        if "access_token" in result:
            logger.debug("Access token %s... (expires %s)",
                         result["access_token"][:10], result["expires_in"])
            return result["access_token"], time.time() + float(result["expires_in"])
        else:
            logging.debug(result)
            msg = "Failed to get Auth from Active Directory:\n{}".format(
                result["error_description"]
            )
            raise RuntimeError(msg)
