# Created by matveyev at 13.08.2021
import logging
import pyqtgraph as pg
from PyQt5 import QtWidgets, QtCore
from pyqtgraph.graphicsItems.GradientEditorItem import Gradients

from petra_viewer.main_window import APP_NAME
from petra_viewer.utils.utils import read_mask_file, read_ff_file

WIDGET_NAME = ''
logger = logging.getLogger(APP_NAME)


# ----------------------------------------------------------------------
class Base2DDetectorSetup(QtWidgets.QWidget):
    """
    General class, which provides GUI interface to setup parameters

    These are common parameters:

    SETTINGS = {'enable_mask': False,
                'mask': None,
                'mask_file': '',
                'enable_ff': False,
                'ff': None,
                'ff_file': '',
                'ff_min': 0,
                'ff_max': 100,
                'enable_fill': False,
                'fill_radius': 7,
                }
    """

    # ----------------------------------------------------------------------
    def __init__(self, main_window):
        """
        """
        super(Base2DDetectorSetup, self).__init__()

        self._ui = self._my_ui()
        self._ui.setupUi(self)

        self._main_window = main_window

        # pyqtgraph instance to display pixel mask
        self._main_plot = pg.PlotItem()
        self._main_plot.showAxis('left', False)
        self._main_plot.showAxis('bottom', False)
        self._main_plot.setMenuEnabled(False)

        self._ui.gv_main.setStyleSheet("")
        self._ui.gv_main.setBackground('w')
        self._ui.gv_main.setObjectName("gvMain")

        self._ui.gv_main.setCentralItem(self._main_plot)
        self._ui.gv_main.setRenderHints(self._ui.gv_main.renderHints())

        self._main_plot.getViewBox().setAspectLocked()

        self._plot_2d = pg.ImageItem()
        self._plot_2d.setLookupTable(pg.ColorMap(*zip(*Gradients['grey']["ticks"])).getLookupTable())
        self._main_plot.addItem(self._plot_2d)

        # display current setting
        self._settings = self._my_settings()

        for param in ['mask', 'ff']:
            if self._settings[f'enable_{param}']:
                getattr(self._ui, f'rb_{param}_on').setChecked(True)
                getattr(self._ui, f'but_load_{param}').setChecked(True)
                getattr(self._ui, f'lb_{param}_file').setText(self._settings[f'{param}_file'])
            else:
                getattr(self._ui, f'rb_{param}_off').setChecked(True)

        self._ui.dsb_ff_from.setValue(self._settings['ff_min'])
        self._ui.dsb_ff_to.setValue(self._settings['ff_max'])

        if self._settings['enable_fill']:
            self._ui.rb_fill_on.setChecked(True)
            self._ui.sb_fill.setEnabled(True)
            self._ui.sb_fill.setValue(self._settings['fill_radius'])
        else:
            self._ui.rb_fill_off.setChecked(True)

        self._display_mask()

        # signals from interface
        self._ui.bg_mask_option.buttonClicked.connect(lambda button: self.change_mode(button, 'mask'))
        self._ui.bg_ff_option.buttonClicked.connect(lambda button: self.change_mode(button, 'ff'))
        self._ui.bg_fill_option.buttonClicked.connect(self.change_fill)

        self._ui.but_load_mask.clicked.connect(lambda: self.load_from_file('mask'))
        self._ui.but_load_ff.clicked.connect(lambda: self.load_from_file('ff'))

        self._ui.dsb_ff_from.valueChanged.connect(self._new_ff_limit)
        self._ui.dsb_ff_to.valueChanged.connect(self._new_ff_limit)

        self._main_plot.scene().sigMouseClicked.connect(self._mouse_clicked)

        try:
            self.restoreGeometry(QtCore.QSettings(APP_NAME).value("{}/geometry".format(WIDGET_NAME)))
        except Exception as err:
            logger.error("{} : cannot restore geometry: {}".format(WIDGET_NAME, err))

    # ----------------------------------------------------------------------
    def _my_ui(self):
        raise RuntimeError('Non implemented')

    # ----------------------------------------------------------------------
    def _my_settings(self):
        raise RuntimeError('Non implemented')

    # ----------------------------------------------------------------------
    def change_fill(self, button):
        if button == self._ui.rb_fill_off:
            self._ui.sb_fill.setEnabled(False)
        else:
            self._ui.sb_fill.setEnabled(True)

    # ----------------------------------------------------------------------
    def change_mode(self, button, mode):

        if button == getattr(self._ui, f'rb_{mode}_off'):
            getattr(self._ui, f'but_load_{mode}').setEnabled(False)
        else:
            getattr(self._ui, f'but_load_{mode}').setEnabled(True)
            getattr(self._ui, f'lb_{mode}_file').setText(self._settings[f'{mode}_file'])

        self._display_mask()

    # ----------------------------------------------------------------------
    def load_from_file(self, mode):
        """
        load mask of flat filed mask form file

        :param mode: 'mask' or 'ff' (flat filed)
        :return:
        """
        file_name, _ = QtWidgets.QFileDialog.getOpenFileName(self, f'Open file with {mode}',
                                                             self._main_window.get_current_folder())

        if file_name:
            if mode =='mask':
                data = read_mask_file(file_name)
            else:
                data = read_ff_file(file_name)

            if data is not None:
                getattr(self._ui, f'lb_{mode}_file').setText(file_name)

        self._display_mask()

    # ----------------------------------------------------------------------
    def _new_ff_limit(self):
        self._display_mask()

    # ----------------------------------------------------------------------
    def _display_mask(self):
        """
        calculated mask for current setting and displays it
        :return:
        """

        _mask = self._calculate_mask()

        if _mask is not None:
            try:
                self._plot_2d.setImage(_mask, autoLevels=True)
            except Exception as err:
                logger.error("{} : cannot display mask geometry: {}".format(WIDGET_NAME, err))
                self._plot_2d.clear()
        else:
            self._plot_2d.clear()

    # ----------------------------------------------------------------------
    def _calculate_mask(self):

        _mask = None

        if self._ui.rb_mask_on.isChecked():
            _mask = read_mask_file(self._ui.lb_mask_file.text())
            if _mask is not None:
                _mask = _mask > 0

        if self._ui.rb_ff_on.isChecked():
            _ff = read_ff_file(self._ui.lb_ff_file.text())
            if _ff is not None:
                _ff = (_ff < self._ui.dsb_ff_from.value()) + (_ff > self._ui.dsb_ff_to.value())
                if _mask is None:
                    _mask = _ff
                else:
                    _mask += _ff

        return _mask

    # ----------------------------------------------------------------------
    def get_settings(self):

        settings = {}
        if self._ui.rb_mask_on.isChecked():
            settings['mask'] = self._ui.lb_mask_file.text()
        else:
            settings['mask'] = ''

        if self._ui.rb_ff_on.isChecked():
            settings['ff'] = self._ui.lb_ff_file.text()
        else:
            settings['ff'] = ''

        settings['min_ff'] = str(self._ui.dsb_ff_from.value())
        settings['max_ff'] = str(self._ui.dsb_ff_to.value())

        if self._ui.rb_fill_on.isChecked():
            settings['fill_radius'] = str(self._ui.sb_fill.value())

        return settings

    # ----------------------------------------------------------------------
    def accept(self):

        QtCore.QSettings(APP_NAME).setValue("{}/geometry".format(WIDGET_NAME), self.saveGeometry())

        super(Base2DDetectorSetup, self).accept()

    # ----------------------------------------------------------------------
    def reject(self):

        QtCore.QSettings(APP_NAME).setValue("{}/geometry".format(WIDGET_NAME), self.saveGeometry())

        super(Base2DDetectorSetup, self).reject()

    # ----------------------------------------------------------------------
    def _mouse_clicked(self, event):
        """
        """
        if event.double():
            try:
                self._main_plot.autoRange()
            except:
                pass
