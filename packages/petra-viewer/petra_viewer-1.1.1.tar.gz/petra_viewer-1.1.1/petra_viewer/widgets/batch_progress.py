# Created by matveyev at 06.05.2021

from PyQt5 import QtCore, QtWidgets

from petra_viewer.gui.batch_ui import Ui_batch


# ----------------------------------------------------------------------
class BatchProgress(QtWidgets.QWidget):

    stop_batch = QtCore.pyqtSignal()

    # ----------------------------------------------------------------------
    def __init__(self):
        super(BatchProgress, self).__init__()

        self._ui = Ui_batch()
        self._ui.setupUi(self)

        self._ui.but_box.clicked.connect(self._button_clicked)

    # --------------------------------------------------------------------
    def clear(self):
        self._ui.tx_status.clear()
        self._ui.pb_progress.setValue(0)

    # ----------------------------------------------------------------------
    def add_values(self, text, progress):
        self._ui.tx_status.append(text)
        self._ui.pb_progress.setValue(progress*100)

    # ----------------------------------------------------------------------
    def _button_clicked(self, button):
        pass
        self.stop_batch.emit()
        self.close()