# Created by matveyev at 23.02.2021

from datetime import datetime

from PyQt5 import QtCore, QtGui
from petra_viewer.asapo_tree_view.asapo_table_headers import headers

# ----------------------------------------------------------------------
class Node(object):

    def __init__(self, parent, row=-1, info=None):

        self.parent = parent

        self.children = []
        self.headers = []

        if info is not None:
            self.info = info
        else:
            self.info = {}

        if self.parent is not None:
            self.parent.add_child(self, row)

    # ----------------------------------------------------------------------
    def add_child(self, child, row=-1):
        if row == -1:
            self.children.append(child)
        else:
            self.children.insert(row, child)
        child._parent = self

    # ----------------------------------------------------------------------
    def remove_child(self, row):
        del self.children[row]

    # ----------------------------------------------------------------------
    @property
    def row(self):
        if self.parent is None:
            return 0
        return self.parent.children.index(self)

    # ----------------------------------------------------------------------
    @property
    def child_count(self):
        return len(self.children)

    # ----------------------------------------------------------------------
    def child(self, row):
        try:
            return self.children[row]
        except IndexError:
            return None

    # ----------------------------------------------------------------------
    def all_child(self):
        return self.children

    # ----------------------------------------------------------------------
    def data(self, column, role):

        if role in [QtCore.Qt.DisplayRole, QtCore.Qt.EditRole]:
            for key in headers[list(headers.keys())[column]]:
                if key in self.info:
                    return self.info[key]
            return ''

        elif role == QtCore.Qt.FontRole:
            return self.my_font(QtGui.QFont())

        elif role == QtCore.Qt.ForegroundRole:
            return self.my_color()

    # ----------------------------------------------------------------------
    def flags(self, column):

        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable

    # ----------------------------------------------------------------------
    def my_font(self, base_font):
        raise RuntimeError('Not implemented!')

    # ----------------------------------------------------------------------
    def my_color(self):
        return QtCore.QVariant()

    # ----------------------------------------------------------------------
    def my_name(self):
        return self.data(list(headers.keys()).index('Name'), QtCore.Qt.DisplayRole)


# ----------------------------------------------------------------------
class StreamNode(Node):

    def __init__(self, parent, row=-1, info=None):
        super(StreamNode, self).__init__(parent, row, info)
        self._reformat_time()

    # ----------------------------------------------------------------------
    def update_info(self, info):
        self.info = info
        self._reformat_time()

    # ----------------------------------------------------------------------
    def my_font(self, base_font):
        return base_font

    # ----------------------------------------------------------------------
    def _reformat_time(self):
        for key in self.info:
            if 'timestampCreated' in key:
                self.time_stamp = self.info[key] / 1e9
                self.info[key] = str(datetime.fromtimestamp(self.info[key]/1e9))

# ----------------------------------------------------------------------
class DetectorNode(Node):

    # ----------------------------------------------------------------------
    def my_font(self, base_font):
        base_font.setBold(True)
        return base_font

