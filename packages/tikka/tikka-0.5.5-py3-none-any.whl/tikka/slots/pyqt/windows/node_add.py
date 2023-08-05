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
from typing import TYPE_CHECKING, Optional

from PyQt5 import QtCore, QtWidgets
from PyQt5.QtGui import QKeyEvent
from PyQt5.QtWidgets import QApplication, QDialog, QWidget

from tikka.domains.application import Application
from tikka.domains.entities.constants import DATA_PATH
from tikka.domains.entities.events import NodesEvent
from tikka.domains.entities.node import Node
from tikka.slots.pyqt.resources.gui.windows.node_add_rc import Ui_nodeAddDialog

if TYPE_CHECKING:
    import _


class NodeAddWindow(QDialog, Ui_nodeAddDialog):
    """
    NodeAddWindow class
    """

    def __init__(self, application: Application, parent: Optional[QWidget] = None):
        """
        Init add node window

        :param application: Application instance
        :param parent: QWidget instance
        """
        super().__init__(parent=parent)
        self.setupUi(self)

        self.application = application
        self._ = self.application.translator.gettext

        # buttons
        self.buttonBox.button(self.buttonBox.Ok).setEnabled(False)

        # events
        self.urlLineEdit.keyPressEvent = self.on_url_line_edit_key_press_event
        self.testButton.clicked.connect(self._on_test_button_clicked)
        self.buttonBox.accepted.connect(self.on_accepted_button)
        self.buttonBox.rejected.connect(self.close)

    def on_url_line_edit_key_press_event(self, event: QKeyEvent):
        """
        Triggered when enter is pressed to validate url in url t line edit

        :param event: QKeyEvent instance
        :return:
        """
        if event.key() == QtCore.Qt.Key_Return:
            self._on_test_button_clicked()
        else:
            QtWidgets.QLineEdit.keyPressEvent(self.urlLineEdit, event)
            # if the key is not return, handle normally

    def _on_test_button_clicked(self):
        """
        Run when use click test button

        :return:
        """
        url = self.urlLineEdit.text()
        node = self.application.nodes.network_test_and_get_node(url)
        if node is not None:
            self.softwareValueLabel.setText(node.software)
            self.versionValueLabel.setText(node.software_version)
            self.peerIDValueLabel.setText(node.peer_id)
            self.blockValueLabel.setText(str(node.block))
            self.errorLabel.setText("")
            self.buttonBox.button(self.buttonBox.Ok).setEnabled(True)
        else:
            self.softwareValueLabel.setText("")
            self.versionValueLabel.setText("")
            self.peerIDValueLabel.setText("")
            self.blockValueLabel.setText("")
            self.errorLabel.setText(self._("Impossible to connect"))
            self.buttonBox.button(self.buttonBox.Ok).setEnabled(False)

    def on_accepted_button(self) -> None:
        """
        Triggered when user click on ok button

        :return:
        """
        url = self.urlLineEdit.text()
        if self.application.nodes.get(url) is not None:
            return

        self.application.nodes.add(
            Node(
                url=self.urlLineEdit.text(),
                peer_id=self.peerIDValueLabel.text(),
                block=int(self.blockValueLabel.text()),
                software=self.softwareValueLabel.text(),
                software_version=self.versionValueLabel.text(),
            )
        )

        self.application.event_dispatcher.dispatch_event(
            NodesEvent(NodesEvent.EVENT_TYPE_LIST_CHANGED)
        )


if __name__ == "__main__":
    qapp = QApplication(sys.argv)
    application_ = Application(DATA_PATH)
    NodeAddWindow(application_).exec_()
