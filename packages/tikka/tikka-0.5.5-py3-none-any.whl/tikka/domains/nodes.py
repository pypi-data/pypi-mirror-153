# Copyright 2021 Vincent Texier <vit@free.fr>
#
# This software is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This software is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
from typing import List, Optional

from tikka.adapters.network.nodes import NetworkNodes
from tikka.adapters.network.rpc.connection import RPCConnection
from tikka.domains.config import Config
from tikka.domains.connections import Connections
from tikka.domains.currencies import Currencies
from tikka.domains.entities.events import ConnectionsEvent, NodesEvent
from tikka.domains.entities.node import Node
from tikka.domains.events import EventDispatcher
from tikka.interfaces.adapters.network.nodes import NetworkNodesInterface
from tikka.interfaces.adapters.repository.nodes import NodesRepositoryInterface
from tikka.interfaces.adapters.repository.preferences import (
    CURRENT_ENTRY_POINT_URL,
    PreferencesRepositoryInterface,
)


class Nodes:
    """
    Nodes domain class
    """

    DEFAULT_LIST_OFFSET = 0
    DEFAULT_LIST_LIMIT = 1000

    PROPERTY_URL = NodesRepositoryInterface.COLUMN_URL
    PROPERTY_PEER_ID = NodesRepositoryInterface.COLUMN_PEER_ID
    PROPERTY_BLOCK = NodesRepositoryInterface.COLUMN_BLOCK
    PROPERTY_SOFTWARE = NodesRepositoryInterface.COLUMN_SOFTWARE
    PROPERTY_SOFTWARE_VERSION = NodesRepositoryInterface.COLUMN_SOFTWARE_VERSION

    def __init__(
        self,
        repository: NodesRepositoryInterface,
        preferences_repository: PreferencesRepositoryInterface,
        connections: Connections,
        network: NetworkNodesInterface,
        config: Config,
        currencies: Currencies,
        event_dispatcher: EventDispatcher,
    ):
        """
        Init Nodes domain instance

        :param repository: EntryPointsRepositoryInterface instance
        :param preferences_repository: PreferencesRepositoryInterface instance
        :param connections: Connections instance
        :param network: Network adapter instance for handling nodes
        :param config: Config instance
        :param currencies: Currencies instance
        :param event_dispatcher: EventDispatcher instance
        """
        self.repository = repository
        self.preferences_repository = preferences_repository
        self.connections = connections
        self.network = network
        self.config = config
        self.currencies = currencies
        self.event_dispatcher = event_dispatcher
        self.current_url = self.currencies.get_entry_point_urls()[0]

        self.init_repository()

        # events
        self.event_dispatcher.add_event_listener(
            ConnectionsEvent.EVENT_TYPE_CONNECTED, self._on_connections_connected
        )

    def init_repository(self):
        """
        Init repository with default entry points from config

        :return:
        """
        # init repository with current currency entry point urls
        if len(self.repository.list()) == 0:
            for url in self.currencies.get_entry_point_urls():
                self.repository.add(Node(url))

        self.current_url = self.repository.list(0, 1)[0].url

        current_url_in_preferences = self.preferences_repository.get(
            CURRENT_ENTRY_POINT_URL
        )
        if current_url_in_preferences is None:
            self.preferences_repository.set(CURRENT_ENTRY_POINT_URL, self.current_url)
        else:
            self.current_url = current_url_in_preferences

    def network_fetch_current_node(self) -> None:
        """
        Update node from network

        :return:
        """
        node = self.network.get()
        if node is None:
            return None

        self.repository.update(node)

        return None

    @staticmethod
    def network_test_and_get_node(url: str) -> Optional[Node]:
        """
        Try to open connection on url and return node if successful

        Then close connection

        :param url: Entry point url
        :return:
        """
        node = None

        connections = Connections(RPCConnection(), EventDispatcher())
        connections.connect(Node(url))
        if connections.is_connected():
            network_nodes = NetworkNodes(connections)
            node = network_nodes.get()
        connections.disconnect()

        return node

    def add(self, node: Node) -> None:
        """
        Add node in repository

        :param node: Node instance
        :return:
        """
        self.repository.add(node)

        self.event_dispatcher.dispatch_event(
            NodesEvent(NodesEvent.EVENT_TYPE_LIST_CHANGED)
        )

    def get(self, url: str) -> Optional[Node]:
        """
        Get Node instance by url

        :param url: Url
        :return:
        """
        return self.repository.get(url)

    def update(self, node: Node) -> None:
        """
        Update Node in repository

        :param node: Node instance
        :return:
        """
        self.repository.update(node)

        self.event_dispatcher.dispatch_event(
            NodesEvent(NodesEvent.EVENT_TYPE_LIST_CHANGED)
        )

    def list(self) -> List[Node]:
        """
        Return all Nodes from repository

        :return:
        """
        return self.repository.list()

    def count(self) -> int:
        """
        Return total node count

        :return:
        """
        return self.repository.count()

    def delete(self, url: str):
        """
        Delete Node by url

        :param url: Node url
        :return:
        """
        # do not delete default entry points from config
        if url in self.currencies.get_entry_point_urls():
            return

        self.repository.delete(url)
        # switch current entry point to first in list
        self.set_current_url(self.repository.list(0, 1)[0].url)
        # set new entry point in preferences
        self.preferences_repository.set(CURRENT_ENTRY_POINT_URL, self.get_current_url())

        self.event_dispatcher.dispatch_event(
            NodesEvent(NodesEvent.EVENT_TYPE_LIST_CHANGED)
        )

    def get_current_url(self) -> str:
        """
        Return current entry point url

        :return:
        """
        return self.current_url

    def set_current_url(self, url: str) -> None:
        """
        Set current entry point url

        :return:
        """
        self.current_url = url
        # update preference
        self.preferences_repository.set(
            CURRENT_ENTRY_POINT_URL,
            self.current_url,
        )
        # switch current connection
        self.connections.disconnect()
        node = self.get(self.current_url)
        if node is not None:
            self.connections.connect(node)

    def _on_connections_connected(self, _: ConnectionsEvent):
        """
        Triggered when the connection is established

        :param _:
        :return:
        """
        self.network_fetch_current_node()
