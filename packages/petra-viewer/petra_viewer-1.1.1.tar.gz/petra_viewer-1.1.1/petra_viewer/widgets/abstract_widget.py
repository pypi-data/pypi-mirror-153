# Created by matveyev at 14.04.2021

import logging
from PyQt5 import QtWidgets

WIDGET_NAME = None
from petra_viewer.main_window import APP_NAME

logger = logging.getLogger(APP_NAME)


# ----------------------------------------------------------------------
class AbstractWidget(QtWidgets.QWidget):

    def __init__(self, parent):
        super(AbstractWidget, self).__init__()
        self._parent = parent

    # ----------------------------------------------------------------------
    def set_settings(self, settings):
        pass

    # ----------------------------------------------------------------------
    def load_ui_settings(self, settings):
        try:
            self.restoreGeometry(settings.value("{}/geometry".format(WIDGET_NAME)))
        except Exception as err:
            logger.error("{} : cannot restore geometry: {}".format(WIDGET_NAME, err))

    # ----------------------------------------------------------------------
    def save_ui_settings(self, settings):
        settings.setValue("{}/geometry".format(WIDGET_NAME), self.saveGeometry())
