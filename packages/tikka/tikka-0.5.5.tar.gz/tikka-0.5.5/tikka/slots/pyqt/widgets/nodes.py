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
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget

from tikka.domains.application import Application
from tikka.domains.entities.constants import DATA_PATH
from tikka.domains.entities.events import CurrencyEvent, NodesEvent
from tikka.slots.pyqt.models.nodes import NodesTableModel
from tikka.slots.pyqt.resources.gui.widgets.nodes_rc import Ui_NodesWidget
from tikka.slots.pyqt.widgets.node_menu import NodePopupMenu
from tikka.slots.pyqt.windows.node_add import NodeAddWindow


class NodesWidget(QWidget, Ui_NodesWidget):
    """
    NodesWidget class
    """

    def __init__(
        self,
        application: Application,
        mutex: QMutex,
        parent: Optional[QWidget] = None,
    ) -> None:
        """
        Init NodesWidget instance

        :param application: Application instance
        :param mutex: QMutex instance
        :param parent: MainWindow instance
        """
        super().__init__(parent=parent)
        self.setupUi(self)

        self.application = application
        self.mutex = mutex
        self._ = self.application.translator.gettext

        self.nodes_table_model = NodesTableModel(self.application)
        self.nodesTableView.setModel(self.nodes_table_model)
        self.nodesTableView.resizeColumnsToContents()
        self.nodesTableView.resizeRowsToContents()

        self.nodesTableView.customContextMenuRequested.connect(self.on_context_menu)

        # events
        self.addServerButton.clicked.connect(self._on_add_server_button_clicked)

        # subscribe to application events
        self.application.event_dispatcher.add_event_listener(
            CurrencyEvent.EVENT_TYPE_CHANGED, self._on_currency_event
        )
        self.application.event_dispatcher.add_event_listener(
            NodesEvent.EVENT_TYPE_LIST_CHANGED, self._on_node_list_changed_event
        )

    def _on_add_server_button_clicked(self):
        """
        Trigger when user click on add server button

        :return:
        """
        NodeAddWindow(self.application, self).exec_()

    def _on_currency_event(self, _):
        """
        When a currency event is triggered

        :param _: CurrencyEvent instance
        :return:
        """
        # update model
        self.nodesTableView.model().init_data()
        # resize view
        self.nodesTableView.resizeColumnsToContents()
        self.nodesTableView.resizeRowsToContents()

    def _on_node_list_changed_event(self, _):
        """
        When the node list has changed

        :param _: NodesEvent instance
        :return:
        """
        # update model
        self.nodesTableView.model().init_data()
        # resize view
        self.nodesTableView.resizeColumnsToContents()
        self.nodesTableView.resizeRowsToContents()

    def on_context_menu(self, position: QPoint):
        """
        When right button on table view

        :param position: QPoint instance
        :return:
        """
        index = self.nodesTableView.indexAt(position)
        if index.isValid():
            # get selected node
            row = index.row()
            node = self.nodes_table_model.nodes[row]
            # display popup menu at click position
            NodePopupMenu(self.application, node).exec_(
                self.nodesTableView.mapToGlobal(position)
            )


if __name__ == "__main__":
    qapp = QApplication(sys.argv)

    application_ = Application(DATA_PATH)

    main_window = QMainWindow()
    main_window.show()

    main_window.setCentralWidget(NodesWidget(application_, QMutex(), main_window))

    sys.exit(qapp.exec_())
