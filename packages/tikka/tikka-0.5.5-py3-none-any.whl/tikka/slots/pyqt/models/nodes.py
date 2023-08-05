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

from typing import TYPE_CHECKING, List, Optional

from PyQt5.QtCore import QAbstractTableModel, QModelIndex, Qt, QVariant

from tikka.domains.application import Application
from tikka.domains.entities.node import Node

if TYPE_CHECKING:
    import _


class NodesTableModel(QAbstractTableModel):
    """
    NodesTableModel class that drives the population of tabular display
    """

    def __init__(self, application: Application):
        super().__init__()

        self.application = application
        self._ = self.application.translator.gettext

        self.headers = [
            self._("Url"),
            self._("Software"),
            self._("Version"),
            self._("Peer ID"),
        ]

        self.column_types = [
            self.application.nodes.repository.COLUMN_URL,
            self.application.nodes.repository.COLUMN_SOFTWARE,
            self.application.nodes.repository.COLUMN_SOFTWARE_VERSION,
            self.application.nodes.repository.COLUMN_PEER_ID,
        ]
        self.sort_order_types = [
            None,
            None,
        ]

        self.sort_column = self.application.nodes.repository.COLUMN_URL
        self.sort_order = None
        self.nodes: List[Node] = []
        self.init_data()

    def init_data(self):
        """
        Fill data from repository

        :return:
        """
        self.beginResetModel()
        self.nodes = self.application.nodes.repository.list()
        self.endResetModel()

    def sort(self, sort_column: int, sort_order: Optional[int] = None):
        """
        Triggered by Qt Signal Sort by column

        :param sort_column: Index of sort column
        :param sort_order: Qt.SortOrder flag
        :return:
        """
        self.sort_column = self.column_types[sort_column]
        self.sort_order = (
            self.sort_order_types[0]
            if sort_order is None
            else self.sort_order_types[sort_order]
        )
        self.init_data()

    def rowCount(self, _: QModelIndex = QModelIndex()) -> int:
        """
        Return row count

        :param _: QModelIndex instance
        :return:
        """
        count = self.application.nodes.repository.count()
        if count == 0:
            return 0
        if count <= len(self.nodes):
            return count

        return len(self.nodes)

    def columnCount(self, _: QModelIndex = QModelIndex()) -> int:
        """
        Return column count (length of headers list)

        :param _: QModelIndex instance
        :return:
        """
        return len(self.headers)

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole) -> QVariant:
        """
        Return data of cell for column index.column

        :param index: QModelIndex instance
        :param role: Item data role
        :return:
        """
        col = index.column()
        row = index.row()
        node = self.nodes[row]
        data = QVariant()
        if role == Qt.DisplayRole:
            if col == 0:
                data = QVariant(node.url)
            if col == 1:
                data = QVariant(node.software)
            if col == 2:
                data = QVariant(node.software_version)
            if col == 3:
                data = QVariant(node.peer_id)

        return data

    def headerData(
        self, section: int, orientation: int, role: int = Qt.DisplayRole
    ) -> QVariant:
        """
        Return

        :param section: Headers column index
        :param orientation: Headers orientation
        :param role: Item role
        :return:
        """
        if role != Qt.DisplayRole:
            return QVariant()

        if orientation == Qt.Horizontal:
            return QVariant(self.headers[section])

        # return row number as vertical header
        return QVariant(int(section + 1))
