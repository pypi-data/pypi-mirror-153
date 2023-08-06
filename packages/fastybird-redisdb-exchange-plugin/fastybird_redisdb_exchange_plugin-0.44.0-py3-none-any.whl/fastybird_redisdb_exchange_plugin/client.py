#!/usr/bin/python3

#     Copyright 2021. FastyBird s.r.o.
#
#     Licensed under the Apache License, Version 2.0 (the "License");
#     you may not use this file except in compliance with the License.
#     You may obtain a copy of the License at
#
#         http://www.apache.org/licenses/LICENSE-2.0
#
#     Unless required by applicable law or agreed to in writing, software
#     distributed under the License is distributed on an "AS IS" BASIS,
#     WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
#     See the License for the specific language governing permissions and
#     limitations under the License.

"""
Redis DB exchange plugin exchange service
"""

# Python base dependencies
import json
import time
from typing import Dict, Optional, Union

# Library dependencies
import fastybird_metadata.exceptions as metadata_exceptions
from fastybird_exchange.client import IClient
from fastybird_exchange.consumer import Consumer
from fastybird_metadata.loader import load_schema_by_routing_key
from fastybird_metadata.routing import RoutingKey
from fastybird_metadata.types import ConnectorSource, ModuleSource, PluginSource
from fastybird_metadata.validator import validate
from kink import inject
from redis import Redis
from redis.client import PubSub
from whistle import EventDispatcher

# Library libs
from fastybird_redisdb_exchange_plugin.events import (
    AfterMessageHandledEvent,
    BeforeMessageHandledEvent,
    ClientClosedEventEvent,
)
from fastybird_redisdb_exchange_plugin.exceptions import (
    HandleDataException,
    HandleRequestException,
)
from fastybird_redisdb_exchange_plugin.logger import Logger


@inject(
    alias=IClient,
    bind={
        "event_dispatcher": EventDispatcher,
        "consumer": Consumer,
    },
)
class Client(IClient):  # pylint: disable=too-many-instance-attributes
    """
    Redis exchange client

    @package        FastyBird:RedisDbExchangePlugin!
    @module         client

    @author         Adam Kadlec <adam.kadlec@fastybird.com>
    """

    __connection: Redis

    __pub_sub: Optional[PubSub] = None

    __identifier: str
    __channel_name: str

    __event_dispatcher: Optional[EventDispatcher]
    __consumer: Optional[Consumer]

    __stopped: bool = True

    __logger: Logger

    # -----------------------------------------------------------------------------

    def __init__(  # pylint: disable=too-many-arguments
        self,
        identifier: str,
        channel_name: str,
        connection: Redis,
        logger: Logger,
        event_dispatcher: Optional[EventDispatcher] = None,
        consumer: Optional[Consumer] = None,
    ) -> None:
        self.__identifier = identifier
        self.__channel_name = channel_name

        self.__event_dispatcher = event_dispatcher
        self.__connection = connection
        self.__logger = logger

        self.__consumer = consumer

    # -----------------------------------------------------------------------------

    @property
    def identifier(self) -> str:
        """Client message identifier"""
        return self.__identifier

    # -----------------------------------------------------------------------------

    def start(self) -> None:
        """Start exchange services"""
        self.__stopped = False

        self.__logger.info(
            "Starting Redis DB exchange client",
            extra={
                "source": "redisdb-exchange-plugin-client",
                "type": "start",
            },
        )

        # Connect to pub sub exchange
        self.__pub_sub = self.__connection.pubsub()
        # Subscribe to channel
        self.__pub_sub.subscribe(self.__channel_name)

        self.__logger.debug(
            "Successfully subscribed to RedisDB exchange channel: %s",
            self.__channel_name,
            extra={
                "source": "redisdb-exchange-plugin-connection",
                "type": "subscribe",
            },
        )

    # -----------------------------------------------------------------------------

    def stop(self) -> None:
        """Close all opened connections & stop exchange thread"""
        self.__stopped = True

        time.sleep(0.01)

        if self.__pub_sub is not None:
            # Unsubscribe from channel
            self.__pub_sub.unsubscribe(self.__channel_name)
            # Disconnect from pub sub exchange
            self.__pub_sub.close()

            self.__logger.debug(
                "Successfully unsubscribed from RedisDB exchange channel: %s",
                self.__channel_name,
                extra={
                    "source": "redisdb-exchange-plugin-connection",
                    "type": "unsubscribe",
                },
            )

            self.__pub_sub = None

        self.__connection.close()

        self.__logger.info(
            "Closing Redis DB exchange client",
            extra={
                "source": "redisdb-exchange-plugin-client",
                "type": "stop",
            },
        )

        if self.__event_dispatcher is not None:
            self.__event_dispatcher.dispatch(
                event_id=ClientClosedEventEvent.EVENT_NAME,
                event=ClientClosedEventEvent(),
            )

    # -----------------------------------------------------------------------------

    def handle(self) -> None:
        """Process Redis exchange messages"""
        try:
            if self.__pub_sub is None:
                return

            if self.__stopped:
                return

            message = self.__pub_sub.get_message()

            if message is None or not isinstance(message, dict):
                return

            if message.get("type") != "message":
                return

            try:
                data: Dict[str, Union[str, int, float, bool, None]] = json.loads(str(message.get("data")))

                # Ignore own messages
                if data.get("sender_id", None) is not None and data.get("sender_id", None) == self.__identifier:
                    return

                self.__receive(data)

            except json.JSONDecodeError as ex:
                self.__logger.exception(ex)

        except OSError as ex:
            self.__logger.error("Error reading from redis database")

            raise HandleRequestException("Error reading from redis database") from ex

    # -----------------------------------------------------------------------------

    def register_consumer(self, consumer: Consumer) -> None:
        """Register client consumer"""
        self.__consumer = consumer

    # -----------------------------------------------------------------------------

    def __receive(self, data: Dict) -> None:
        self.__logger.debug("Received message from exchange")

        if self.__event_dispatcher is not None:
            self.__event_dispatcher.dispatch(
                event_id=BeforeMessageHandledEvent.EVENT_NAME, event=BeforeMessageHandledEvent(payload=json.dumps(data))
            )

        if self.__consumer is not None:
            try:
                source = self.__validate_source(source=data.get("source", None))
                routing_key = self.__validate_routing_key(
                    routing_key=data.get("routing_key", None),
                )

                if (
                    routing_key is not None
                    and source is not None
                    and data.get("data", None) is not None
                    and isinstance(data.get("data", None), dict) is True
                ):
                    data = self.__validate_data(
                        source=source,
                        routing_key=routing_key,
                        data=data.get("data", None),
                    )

                    self.__consumer.consume(
                        source=source,
                        routing_key=routing_key,
                        data=data,
                    )

                else:
                    self.__logger.warning(
                        "Received exchange message is not valid",
                        extra={
                            "source": "redisdb-exchange-plugin-client",
                            "type": "receive",
                        },
                    )

            except HandleDataException as ex:
                self.__logger.exception(ex)

        else:
            self.__logger.warning("No consumer is registered")

        if self.__event_dispatcher is not None:
            self.__event_dispatcher.dispatch(
                event_id=AfterMessageHandledEvent.EVENT_NAME, event=AfterMessageHandledEvent(payload=json.dumps(data))
            )

    # -----------------------------------------------------------------------------

    @staticmethod
    def __validate_source(source: Optional[str]) -> Union[ModuleSource, PluginSource, ConnectorSource, None]:
        if source is not None and isinstance(source, str) is True and ModuleSource.has_value(source):
            return ModuleSource(source)

        if source is not None and isinstance(source, str) is True and PluginSource.has_value(source):
            return PluginSource(source)

        if source is not None and isinstance(source, str) is True and ConnectorSource.has_value(source):
            return ConnectorSource(source)

        return None

    # -----------------------------------------------------------------------------

    @staticmethod
    def __validate_routing_key(routing_key: Optional[str]) -> Optional[RoutingKey]:
        if routing_key is not None and isinstance(routing_key, str) is True and RoutingKey.has_value(routing_key):
            return RoutingKey(routing_key)

        return None

    # -----------------------------------------------------------------------------

    def __validate_data(
        self,
        source: Union[ModuleSource, PluginSource, ConnectorSource],
        routing_key: RoutingKey,
        data: Dict,
    ) -> Dict:
        """Validate received exchange message against defined schema"""
        try:
            schema: str = load_schema_by_routing_key(routing_key)

        except metadata_exceptions.FileNotFoundException as ex:
            self.__logger.error(
                "Schema file for source: %s and routing key: %s could not be loaded",
                source.value,
                routing_key.value,
                extra={
                    "source": "redisdb-exchange-plugin-client",
                    "type": "validate-data",
                },
            )

            raise HandleDataException("Provided data could not be validated") from ex

        except metadata_exceptions.InvalidArgumentException as ex:
            self.__logger.error(
                "Schema file for source: %s and routing key: %s is not configured in mapping",
                source.value,
                routing_key.value,
                extra={
                    "source": "redisdb-exchange-plugin-client",
                    "type": "validate-data",
                },
            )

            raise HandleDataException("Provided data could not be validated") from ex

        try:
            return validate(json.dumps(data), schema)

        except metadata_exceptions.MalformedInputException as ex:
            raise HandleDataException("Provided data are not in valid json format") from ex

        except metadata_exceptions.LogicException as ex:
            self.__logger.error(
                "Schema file for source: %s and routing key: %s could not be parsed & compiled",
                source.value,
                routing_key.value,
                extra={
                    "source": "redisdb-exchange-plugin-client",
                    "type": "validate-data",
                },
            )

            raise HandleDataException("Provided data could not be validated") from ex

        except metadata_exceptions.InvalidDataException as ex:
            raise HandleDataException("Provided data are not valid") from ex
