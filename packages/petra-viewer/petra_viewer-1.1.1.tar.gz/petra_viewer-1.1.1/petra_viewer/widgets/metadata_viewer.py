# This module is based on json-viewer written by Ashwin Nanjappa.
# origin  https://github.com/ashwin/json-viewer.git
import logging
from PyQt5 import QtWidgets

from petra_viewer.main_window import APP_NAME

logger = logging.getLogger(APP_NAME)


class TextToTreeItem:

    # ----------------------------------------------------------------------
    def __init__(self):
        self.text_list = []
        self.titem_list = []

    # ----------------------------------------------------------------------
    def append(self, text_list, titem):
        for text in text_list:
            self.text_list.append(text)
            self.titem_list.append(titem)

    # ----------------------------------------------------------------------
    def clear(self):
        self.text_list = []
        self.titem_list = []

    # ----------------------------------------------------------------------
    # Return model indices that match string
    def find(self, find_str):

        titem_list = []
        for i, s in enumerate(self.text_list):
            if find_str in s:
                titem_list.append(self.titem_list[i])

        return titem_list


# ----------------------------------------------------------------------
class JsonView(QtWidgets.QWidget):

    def __init__(self, parent, data_pool):
        super(JsonView, self).__init__()

        self.find_box = None
        self.tree_widget = None
        self.text_to_titem = TextToTreeItem()
        self.find_str = ""
        self.found_titem_list = []
        self.found_idx = 0
        self.data_pool = data_pool
        self.main_window = parent

        jdata = {}
        # Find UI
        find_layout = self.make_find_ui()

        self.tree_widget = QtWidgets.QTreeWidget()
        self.tree_widget.setHeaderLabels(["Key", "Value"])
        self.tree_widget.header().setSectionResizeMode(QtWidgets.QHeaderView.Stretch)

        root_item = self.tree_widget.invisibleRootItem()
        self.recurse_jdata(jdata, root_item)
        self.tree_widget.addTopLevelItem(root_item)

        # Add table to layout
        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.tree_widget)

        # Group box
        gbox = QtWidgets.QGroupBox("")
        gbox.setLayout(layout)

        layout2 = QtWidgets.QVBoxLayout()
        layout2.addLayout(find_layout)
        layout2.addWidget(gbox)

        self.setLayout(layout2)

    # ----------------------------------------------------------------------
    def update_view(self, data):
        root_item = self.tree_widget.invisibleRootItem()
        self.recurse_jdata(data, root_item)
        self.tree_widget.addTopLevelItem(root_item)
        self.tree_widget.expandAll()

    # ----------------------------------------------------------------------
    def make_find_ui(self):

        # Text box
        self.find_box = QtWidgets.QLineEdit()
        self.find_box.returnPressed.connect(self.find_button_clicked)

        # Find Button
        find_button = QtWidgets.QPushButton("Find")
        find_button.clicked.connect(self.find_button_clicked)

        layout = QtWidgets.QHBoxLayout()
        layout.addWidget(self.find_box)
        layout.addWidget(find_button)
        return layout

    # ----------------------------------------------------------------------
    def find_button_clicked(self):

        find_str = self.find_box.text()

        # Very common for use to click Find on empty string
        if find_str == "":
            return

        # New search string
        if find_str != self.find_str:
            self.find_str = find_str
            self.found_titem_list = self.text_to_titem.find(self.find_str)
            self.found_idx = 0
        else:
            item_num = len(self.found_titem_list)
            self.found_idx = (self.found_idx + 1) % item_num
        self.tree_widget.setCurrentItem(self.found_titem_list[self.found_idx])

    # ----------------------------------------------------------------------
    def recurse_jdata(self, jdata, tree_widget):
        if isinstance(jdata, dict):
            for key, val in jdata.items():
                self.tree_add_row(key, val, tree_widget)
        elif isinstance(jdata, list):
            for i, val in enumerate(jdata):
                key = str(i)
                self.tree_add_row(key, val, tree_widget)
        else:
            print("This should never be reached!")

    # ----------------------------------------------------------------------
    def tree_add_row(self, key, val, tree_widget):
        text_list = []
        if isinstance(val, dict) or isinstance(val, list):
            text_list.append(key)
            row_item = QtWidgets.QTreeWidgetItem([key])
            self.recurse_jdata(val, row_item)
        else:
            text_list.append(key)
            text_list.append(str(val))
            row_item = QtWidgets.QTreeWidgetItem([key, str(val)])

        tree_widget.addChild(row_item)
        self.text_to_titem.append(text_list, row_item)

    # ----------------------------------------------------------------------
    def update_meta(self):
        try:
            self.clear_view()
            file_key = self.main_window.get_current_file()
            # Can happen if stream is closed
            if file_key is None or file_key == '':
                return

            data_to_display = self.data_pool.get_metadata(file_key)
            if data_to_display is not None:
                self.update_view(data_to_display)
        except Exception as err:
            logger.error(f'Cannot update meta: {err}', exc_info=True)

    # ----------------------------------------------------------------------
    def clear_view(self):
        self.tree_widget.clear()
        self.text_to_titem.clear()
