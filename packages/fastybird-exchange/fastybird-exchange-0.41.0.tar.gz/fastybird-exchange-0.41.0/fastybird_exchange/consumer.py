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
Exchange library messages consumer
"""

# Python base dependencies
from abc import ABC, abstractmethod
from typing import Dict, List, Optional, Set, Union

# Library dependencies
from fastybird_metadata.routing import RoutingKey
from fastybird_metadata.types import ConnectorSource, ModuleSource, PluginSource
from kink import inject


class IConsumer(ABC):  # pylint: disable=too-few-public-methods
    """
    Data exchange consumer interface

    @package        FastyBird:Exchange!
    @module         consumer

    @author         Adam Kadlec <adam.kadlec@fastybird.com>
    """

    @abstractmethod
    def consume(
        self,
        source: Union[ModuleSource, PluginSource, ConnectorSource],
        routing_key: RoutingKey,
        data: Optional[Dict[str, Union[str, int, float, bool, None]]],
    ) -> None:
        """Consume data received from exchange bus"""


class IQueue(ABC):  # pylint: disable=too-few-public-methods
    """
    Data exchange consumer queue interface

    @package        FastyBird:Exchange!
    @module         consumer

    @author         Adam Kadlec <adam.kadlec@fastybird.com>
    """

    @abstractmethod
    def set_consumers(self, consumers: List[IConsumer]) -> None:
        """Set consumers to queue"""

    # -----------------------------------------------------------------------------

    @abstractmethod
    def append(
        self,
        source: Union[ModuleSource, PluginSource, ConnectorSource],
        routing_key: RoutingKey,
        data: Optional[Dict],
    ) -> None:
        """Append new item to queue"""

    # -----------------------------------------------------------------------------

    @abstractmethod
    def handle(self) -> None:
        """Proces one item from queue"""

    # -----------------------------------------------------------------------------

    @abstractmethod
    def has_unfinished_items(self) -> bool:
        """Check if queue has some unfinished items"""


@inject(
    bind={
        "consumers": List[IConsumer],
        "queue": IQueue,
    }
)
class Consumer:
    """
    Data exchange consumer proxy

    @package        FastyBird:Exchange!
    @module         consumer

    @author         Adam Kadlec <adam.kadlec@fastybird.com>
    """

    __consumers: Set[IConsumer]
    __queue: Optional[IQueue] = None

    # -----------------------------------------------------------------------------

    def __init__(
        self,
        consumers: Optional[List[IConsumer]] = None,
        queue: Optional[IQueue] = None,
    ) -> None:
        if consumers is None:
            self.__consumers = set()

        else:
            self.__consumers = set(consumers)

        self.__queue = queue

    # -----------------------------------------------------------------------------

    def consume(
        self,
        source: Union[ModuleSource, PluginSource, ConnectorSource],
        routing_key: RoutingKey,
        data: Optional[Dict],
    ) -> None:
        """Call all registered consumers and consume data"""
        if self.__queue is not None:
            self.__queue.append(source=source, routing_key=routing_key, data=data)

        else:
            for consumer in self.__consumers:
                consumer.consume(source=source, routing_key=routing_key, data=data)

    # -----------------------------------------------------------------------------

    def register_consumer(
        self,
        consumer: IConsumer,
    ) -> None:
        """Register new consumer to proxy"""
        self.__consumers.add(consumer)

        if self.__queue is not None:
            self.__queue.set_consumers(consumers=list(self.__consumers))

    # -----------------------------------------------------------------------------

    def register_queue(
        self,
        queue: IQueue,
    ) -> None:
        """Register consumer queue"""
        if self.__queue is not None:
            raise AttributeError("Queue is already configured in consumer service")

        self.__queue = queue
