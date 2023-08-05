# Created by matveyev at 04.08.2021

from PyQt5 import QtWidgets, QtCore

from petra_viewer.gui.axis_selector_ui import Ui_AxisSelector

from petra_viewer.utils.utils import refresh_combo_box


# ----------------------------------------------------------------------
class AxisSelector(QtWidgets.QWidget):

    new_selection = QtCore.pyqtSignal(int, int, int)

    # ----------------------------------------------------------------------
    def __init__(self, parent, my_id, my_name):
        """
        """
        super(AxisSelector, self).__init__(parent)
        self._parent = parent

        self._ui = Ui_AxisSelector()
        self._ui.setupUi(self)

        self._my_id = my_id
        self._value = None

        self.set_new_name(my_name)
        self._ui.cmb_selector.currentIndexChanged.connect(self._new_index_selected)

    # ----------------------------------------------------------------------
    def _new_index_selected(self, new_index):
        self.new_selection.emit(self._my_id, self._value, new_index)
        self._value = new_index

    # ----------------------------------------------------------------------
    def set_new_name(self, my_name):
        self._ui.lb_name.setText(my_name)

    # ----------------------------------------------------------------------
    def set_new_axes(self, axes_list, new_index):

        self.block_signals(True)
        self._ui.cmb_selector.clear()
        self._ui.cmb_selector.addItems(axes_list)
        self._ui.cmb_selector.setCurrentIndex(new_index)
        self._value = new_index
        self.block_signals(False)

    # ----------------------------------------------------------------------
    def set_new_axis(self, new_index):

        self.block_signals(True)

        self._ui.cmb_selector.setCurrentIndex(new_index)
        self._value = new_index

        self.block_signals(False)

    # ----------------------------------------------------------------------
    def get_current_value(self):

        return self._ui.cmb_selector.currentIndex()

    # ----------------------------------------------------------------------
    def get_current_name(self):
        return self._ui.cmb_selector.currentText()

    # ----------------------------------------------------------------------
    def block_signals(self, flag):
        self._ui.cmb_selector.blockSignals(flag)
