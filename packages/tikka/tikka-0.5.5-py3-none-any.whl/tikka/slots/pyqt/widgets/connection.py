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
import sys
from typing import Optional

from PyQt5.QtCore import QMutex, QPoint
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget

from tikka.domains.application import Application
from tikka.domains.entities.constants import DATA_PATH
from tikka.domains.entities.events import ConnectionsEvent, CurrencyEvent, NodesEvent
from tikka.slots.pyqt.entities.constants import (
    ICON_NETWORK_CONNECTED,
    ICON_NETWORK_DISCONNECTED,
)
from tikka.slots.pyqt.entities.worker import AsyncQWorker
from tikka.slots.pyqt.resources.gui.widgets.connection_rc import Ui_ConnectionWidget
from tikka.slots.pyqt.widgets.node_menu import NodePopupMenu


class ConnectionWidget(QWidget, Ui_ConnectionWidget):
    """
    ConnectionWidget class
    """

    def __init__(
        self,
        application: Application,
        mutex: QMutex,
        parent: Optional[QWidget] = None,
    ) -> None:
        """
        Init ConnectionWidget instance

        :param application: Application instance
        :param mutex: QMutex instance
        :param parent: MainWindow instance
        """
        super().__init__(parent=parent)
        self.setupUi(self)

        self.application = application
        self.mutex = mutex
        self._ = self.application.translator.gettext

        self.connected_button_text = self._("Reconnect")
        self.disconnected_button_text = self._("Connect")

        self.init_urls()

        if self.application.connections.is_connected():
            self._on_node_connected()
        else:
            self._on_node_disconnected()

        # events
        self.urlsComboBox.activated.connect(self.on_urls_combobox_index_changed)
        self.connectButton.clicked.connect(self._on_connect_button_clicked_event)
        self.refreshNodeButton.clicked.connect(
            self._on_refresh_node_button_clicked_event
        )

        # subscribe to application events
        self.application.event_dispatcher.add_event_listener(
            CurrencyEvent.EVENT_TYPE_CHANGED, self._on_currency_event
        )
        self.application.event_dispatcher.add_event_listener(
            NodesEvent.EVENT_TYPE_LIST_CHANGED,
            lambda event: self.init_urls(),
        )
        self.application.event_dispatcher.add_event_listener(
            ConnectionsEvent.EVENT_TYPE_CONNECTED, self._on_node_connected
        )
        self.application.event_dispatcher.add_event_listener(
            ConnectionsEvent.EVENT_TYPE_DISCONNECTED, self._on_node_disconnected
        )

        ##############################
        # ASYNC METHODS
        ##############################
        # Create a QWorker object
        self.network_fetch_current_node_async_qworker = AsyncQWorker(
            self.application.nodes.network_fetch_current_node,
            self.mutex,
        )
        self.network_fetch_current_node_async_qworker.finished.connect(
            self._on_finished_fetch_node_from_network
        )

        self.fetch_node_from_network()

    def init_urls(self) -> None:
        """
        Init combobox with node urls

        :return:
        """
        self.urlsComboBox.clear()

        urls = [node.url for node in self.application.nodes.list()]
        self.urlsComboBox.addItems(urls)
        # get current node url from domain
        current_node_url = self.application.nodes.get_current_url()
        self.urlsComboBox.setCurrentIndex(urls.index(current_node_url))

    def on_urls_combobox_index_changed(self):
        """
        Triggered when url selection is changed

        :return:
        """
        url = self.urlsComboBox.currentText()
        if url:
            node = self.application.nodes.get(url)
            if node is None:
                # get the first one
                url = self.urlsComboBox.itemText(0)
            self.application.nodes.set_current_url(url)
            self.fetch_node_from_network()

    def _on_connect_button_clicked_event(self):
        """
        Triggered when user click on connect button

        :return:
        """
        if self.application.connections.is_connected():
            self.application.connections.disconnect()

        url = self.urlsComboBox.currentText()
        if url:
            node = self.application.nodes.get(url)
            if node is not None:
                self.application.connections.connect(node)

    def _on_refresh_node_button_clicked_event(self):
        """
        Triggered when user click on refresh node button

        :return:
        """
        self.fetch_node_from_network()

    def fetch_node_from_network(self):
        """
        Update node infos from current url connection

        :return:
        """
        # Disable button
        self.refreshNodeButton.setEnabled(False)
        # Start the thread
        self.network_fetch_current_node_async_qworker.start()

    def _on_finished_fetch_node_from_network(self):
        """
        Triggered when async request fetch_node_from_network is finished

        :return:
        """
        self.refreshNodeButton.setEnabled(True)
        self._update_ui()

    def _update_ui(self):
        """
        Update node infos in UI

        :return:
        """
        url = self.urlsComboBox.currentText()
        if url:
            node = self.application.nodes.get(url)
            if node is None:
                self.softwareValueLabel.setText("")
                self.versionValueLabel.setText("")
                self.peerIDValueLabel.setText("")
                self.blockValueLabel.setText("")
            else:
                self.softwareValueLabel.setText(node.software)
                self.versionValueLabel.setText(node.software_version)
                self.peerIDValueLabel.setText(node.peer_id)
                self.blockValueLabel.setText(str(node.block))

    def _on_currency_event(self, _):
        """
        When a currency event is triggered

        :param _: CurrencyEvent instance
        :return:
        """
        self.init_urls()

    def on_context_menu(self, position: QPoint):
        """
        When right button on table view

        :param position: QPoint instance
        :return:
        """
        url = self.urlsComboBox.currentText()
        if url:
            node = self.application.nodes.get(url)
            if node is not None:
                NodePopupMenu(self.application, node).exec_(self.mapToGlobal(position))

    def _on_node_connected(self, _=None):
        """
        Triggered when node is connected

        :return:
        """
        self.connectButton.setText(self.connected_button_text)
        self.connectionStatusLabel.setPixmap(QPixmap(ICON_NETWORK_CONNECTED))

    def _on_node_disconnected(self, _=None):
        """
        Triggered when node is disconnected

        :return:
        """
        self.connectButton.setText(self.disconnected_button_text)
        self.connectionStatusLabel.setPixmap(QPixmap(ICON_NETWORK_DISCONNECTED))


if __name__ == "__main__":
    qapp = QApplication(sys.argv)

    application_ = Application(DATA_PATH)

    main_window = QMainWindow()
    main_window.show()

    main_window.setCentralWidget(ConnectionWidget(application_, QMutex(), main_window))

    sys.exit(qapp.exec_())
