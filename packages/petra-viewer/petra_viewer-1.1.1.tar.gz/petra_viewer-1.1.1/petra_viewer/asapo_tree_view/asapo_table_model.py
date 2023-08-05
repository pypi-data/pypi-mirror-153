# Created by matveyev at 19.01.2021,
import numpy as np
from PyQt5 import QtCore

from petra_viewer.asapo_tree_view.asapo_entries_class import Node, StreamNode
from petra_viewer.asapo_tree_view.asapo_table_headers import headers

# ----------------------------------------------------------------------
class ASAPOModel(QtCore.QAbstractItemModel):

    root_index = QtCore.QModelIndex()

    # ----------------------------------------------------------------------
    def __init__(self, root=None):
        if root is None:
            root = Node(None, None, None)
        self.root = root
        self._last_num_column = 0
        self._drag_drop_storage = {}
        super(ASAPOModel, self).__init__()

    # ----------------------------------------------------------------------
    def clear(self):
        if len(self.root.children):
            self.beginRemoveRows(self.root_index, 0, len(self.root.children)-1)
            for row in range(len(self.root.children))[::-1]:
                self.root.remove_child(row)
            self.endRemoveRows()

    # ----------------------------------------------------------------------
    def rowCount(self, parent=None, *args, **kwargs):
        node = self.get_node(parent)
        return node.child_count

    # ----------------------------------------------------------------------
    def columnCount(self, parent=None, *args, **kwargs):
        return len(headers)

    # ----------------------------------------------------------------------
    def index(self, row, column, parent=None, *args, **kwargs):
        node = self.get_node(parent)
        return self.createIndex(row, column, node.child(row))

    # ----------------------------------------------------------------------
    def parent(self, index=None):
        node = self.get_node(index)
        if node.parent is None:
            return QtCore.QModelIndex()
        if node.parent == self.root:
            return QtCore.QModelIndex()
        return self.createIndex(node.parent.row, 0, node.parent)

    # ----------------------------------------------------------------------
    def data(self, index, role=QtCore.Qt.DisplayRole):
        node = self.get_node(index)
        return node.data(index.column(), role)

    # ----------------------------------------------------------------------
    def flags(self, index):
        node = self.get_node(index)
        return node.flags(index.column())

    # ----------------------------------------------------------------------
    def headerData(self, section, orientation, role):
        if orientation == QtCore.Qt.Horizontal and role == QtCore.Qt.DisplayRole:
            if headers and 0 <= section < len(headers):
                return list(headers.keys())[section]
            return None
        return super(ASAPOModel, self).headerData(section, orientation, role)

    # ----------------------------------------------------------------------
    def get_node(self, index):
        if index and index.isValid():
            node = index.internalPointer()
            if node:
                return node
        return self.root

    # ----------------------------------------------------------------------
    def remove(self, index):
        node = self.get_node(index)
        self.beginRemoveRows(index.parent(), node.row, node.row)
        if not index.parent().isValid():
            parent_node = self.root
        else:
            parent_node = index.parent().internalPointer()

        parent_node.remove_child(node.row)
        self.endRemoveRows()

    # ----------------------------------------------------------------------
    def add_stream(self, detector_ind, stream_ind, stream_info):
        """Add new stream (child) to given data_source (node)

        Parameters:
            detector_ind (int): Index of the node
            stream_ind (int): Index of stream in stream list
            stream_info (dict): Information about stream
        """

        detector_index = self.index(detector_ind, 0)
        detector_node = self.get_node(detector_index)
        self.start_insert_row(detector_index, stream_ind)
        stream = StreamNode(detector_node, stream_ind, stream_info)
        self.finish_row_changes()

        return stream

    # ----------------------------------------------------------------------
    def update_stream(self, detector_ind, stream_ind, stream_info):
        """Update stream information

        Parameters:
            detector_ind (int): Index of the node
            stream_ind (int): Index of stream in stream list
            stream_info (dict): Information about stream
        """

        detector_index = self.index(detector_ind, 0)
        detector_node = self.get_node(detector_index)
        stream = detector_node.child(stream_ind)
        if stream is not None:
            stream.update_info(stream_info)

    # ----------------------------------------------------------------------
    def start_insert_row(self, insert_index, row=0):
        self.beginInsertRows(insert_index, row, row)

    # ----------------------------------------------------------------------
    def start_adding_detector(self, insert_index=0, num_elements=1):
        self.beginInsertRows(self.root_index, insert_index, insert_index + num_elements-1)

    # ----------------------------------------------------------------------
    def finish_row_changes(self):
        self.endInsertRows()

    # # ----------------------------------------------------------------------
    # def filter_row(self, index, value_to_look):
    #     print('filter_row')
    #     node = self.get_node(index)
    #     if self.filter_time and isinstance(node, StreamNode):
    #         return node.filter_row(value_to_look) & self.filter_from < node.time_stamp < self.filter_to
    #     else:
    #         return node.filter_row(value_to_look)

    # ----------------------------------------------------------------------
    def save_columns_count(self):
        self._last_num_column = self.columnCount()

    # ----------------------------------------------------------------------
    def add_columns(self):
        num_columns = self.columnCount()

        if num_columns > self._last_num_column:
            self.beginInsertColumns(self.root_index, self._last_num_column, num_columns - 1)
            self.endInsertColumns()
        elif num_columns < self._last_num_column:
            self.beginRemoveRows(self.root_index, num_columns, self._last_num_column - 1)
            self.endRemoveColumns()

        self._last_num_column = num_columns


# ----------------------------------------------------------------------
class ProxyModel(QtCore.QSortFilterProxyModel):

    new_version = True

    filter_from = -np.Inf
    filter_to = np.Inf
    filter_time = False

    # ----------------------------------------------------------------------
    def filterAcceptsRow(self, source_row, source_parent):

        if self.filter_time:
            node = self.sourceModel().get_node(source_parent).child(source_row)
            if isinstance(node, StreamNode):
                time_accepted = self.filter_from < node.time_stamp < self.filter_to
            else:
                time_accepted = True
        else:
            time_accepted = True

        if self.new_version:
            return super(ProxyModel, self).filterAcceptsRow(source_row, source_parent) & time_accepted
        else:
            match = False
            my_index = self.sourceModel().index(source_row, 0, source_parent)
            for row in range(self.sourceModel().rowCount(my_index)):
                match |= self.filterAcceptsRow(row, my_index)

            match |= super(ProxyModel, self).filterAcceptsRow(source_row, source_parent)

            return match & time_accepted

