# Created by matveyev at 09.11.2021

from PyQt5 import QtWidgets, QtCore

from petra_viewer.widgets.abstract_widget import AbstractWidget

from petra_viewer.data_sources.test_datasets.test_datasets import SardanaPeak1, SardanaPeak2, HeavySardana, \
    ASAPO2DPeak, ASAPO3DPeak, ASAPO4DPeak, BeamView

from petra_viewer.gui.tests_browser_ui import Ui_TestsBrowser

WIDGET_NAME = 'TestsBrowser'


# ----------------------------------------------------------------------
class TestsBrowser(AbstractWidget):

    test_selected = QtCore.pyqtSignal(str)

    def __init__(self, parent):
        """
        """
        super(TestsBrowser, self).__init__(parent)
        self._ui = Ui_TestsBrowser()
        self._ui.setupUi(self)

        self._ui.tb_sets.setHorizontalHeaderLabels(['Name', 'Dim', 'Size'])
        self._ui.tb_sets.setSelectionBehavior(QtWidgets.QAbstractItemView.SelectRows)
        self._ui.tb_sets.setColumnWidth(1, 50)

        self.test_classes = [SardanaPeak1, SardanaPeak2, HeavySardana, ASAPO2DPeak, ASAPO3DPeak, ASAPO4DPeak, BeamView]
        self._ui.tb_sets.setRowCount(len(self.test_classes))

        for ind, test_class in enumerate(self.test_classes):
            name, dims, size = test_class.get_info(test_class)
            self._ui.tb_sets.setItem(ind, 0, QtWidgets.QTableWidgetItem(f'{name}'))
            self._ui.tb_sets.setItem(ind, 1, QtWidgets.QTableWidgetItem(f'{dims}'))
            self._ui.tb_sets.setItem(ind, 2, QtWidgets.QTableWidgetItem(f'{size}'))

        self._ui.tb_sets.itemDoubleClicked.connect(self._add_test)

    # ----------------------------------------------------------------------
    def _add_test(self, item):
        self.test_selected.emit(self.test_classes[item.row()].my_name)

