# Created by matveyev at 22.02.2021

WIDGET_NAME = 'ROIsView'

import logging
import pickle
import os

try:
    import PyTango
    has_pytango = True
except:
    has_pytango = False

from PyQt5 import QtWidgets, QtCore

from petra_viewer.gui.rois_view_ui import Ui_RoisView
from petra_viewer.widgets.section_view import SectionView

from petra_viewer.main_window import APP_NAME

logger = logging.getLogger(APP_NAME)


# ----------------------------------------------------------------------
class RoisView(QtWidgets.QMainWindow):
    """
    """
    PEN_COUNTER = 0

    update_roi = QtCore.pyqtSignal(int)

    # ----------------------------------------------------------------------
    def __init__(self, parent, data_pool):
        """
        """
        super(RoisView, self).__init__()
        self._ui = Ui_RoisView()
        self._ui.setupUi(self)

        self.menuBar().setNativeMenuBar(False)

        self.setCentralWidget(None)

        self.setDockOptions(QtWidgets.QMainWindow.AnimatedDocks |
                            QtWidgets.QMainWindow.AllowNestedDocks |
                            QtWidgets.QMainWindow.AllowTabbedDocks)

        self.setTabPosition(QtCore.Qt.LeftDockWidgetArea, QtWidgets.QTabWidget.North)

        self._parent = parent

        self._data_pool = data_pool
        self._parent = parent

        menu_add_roi = QtWidgets.QAction('Add ROI', self)
        menu_add_roi.triggered.connect(self.add_roi)
        self.menuBar().addAction(menu_add_roi)

        menu_fetch_roi = QtWidgets.QAction('Fetch ROIs', self)
        menu_fetch_roi.triggered.connect(self.fetch_rois)
        self.menuBar().addAction(menu_fetch_roi)

        self._menu_rois = QtWidgets.QMenu('Show ROI', self)
        self.menuBar().addMenu(self._menu_rois)

        batch_menu = QtWidgets.QMenu('Batch process', self)

        action = batch_menu.addAction("Process files...")
        action.triggered.connect(lambda checked, x='files': self._batch_process(x))

        action = batch_menu.addAction("Process folder...")
        action.triggered.connect(lambda checked, x='folder': self._batch_process(x))

        self.menuBar().addMenu(batch_menu)

        self._roi_widgets = {}
        self._docks = {}

        self._opened_files = {}
        self._last_color = -1
        self.settings = {}

    # ----------------------------------------------------------------------
    def get_current_file(self):
        return self._parent.get_current_file()

    # ----------------------------------------------------------------------
    def set_settings(self, settings):

        self.settings.update(settings)

    # ----------------------------------------------------------------------
    def fetch_rois(self):
        if 'macro_server' in self.settings and has_pytango:
            data = pickle.loads(PyTango.DeviceProxy(self.settings['macro_server']).environment[1])['new']['DetectorROIs']
            for roi in data.values():
                last_id = self.add_roi()
                self._data_pool.set_section_axis(last_id, 0)
                self._data_pool.roi_parameter_changed(last_id, 1, 'pos',
                                                      self._data_pool.get_value_for_frame(self.get_current_file(),
                                                                                          1, roi[0][1]))
                self._data_pool.roi_parameter_changed(last_id, 1, 'width',
                                                      self._data_pool.get_value_for_frame(self.get_current_file(),
                                                                                          1, roi[0][3] - roi[0][1] + 1))
                self._data_pool.roi_parameter_changed(last_id, 2, 'pos',
                                                      self._data_pool.get_value_for_frame(self.get_current_file(),
                                                                                          2, roi[0][0]))
                self._data_pool.roi_parameter_changed(last_id, 2, 'width',
                                                      self._data_pool.get_value_for_frame(self.get_current_file(),
                                                                                          2,  roi[0][2] - roi[0][0] + 1))
                self._roi_widgets[last_id].roi_changed()
                self.update_roi.emit(last_id)

    # ----------------------------------------------------------------------
    def add_roi(self):
        idx, name, roi_dims = self._data_pool.add_new_roi()
        if idx is None:
            return

        self._parent.add_roi(idx)
        widget, dock = self._add_dock(SectionView, f'ROI {name}', QtCore.Qt.LeftDockWidgetArea,
                                      self, self._data_pool, idx, roi_dims)

        current_rect = self._parent.get_current_rect()
        width = (current_rect[2] - current_rect[0])/10
        x = (current_rect[0] + current_rect[2])/2 - width/2

        height = (current_rect[3] - current_rect[1])/10
        y = (current_rect[1] + current_rect[3])/2 - height/2

        current_axes = self._parent.get_current_axes()

        for axis in range(1, 100):
            if self._data_pool.get_roi_param(idx, f'axis_{axis}') == current_axes['x']:
                self._data_pool.roi_parameter_changed(idx, axis, 'pos', x)
                self._data_pool.roi_parameter_changed(idx, axis, 'width', width)
            elif self._data_pool.get_roi_param(idx, f'axis_{axis}') == current_axes['y']:
                self._data_pool.roi_parameter_changed(idx, axis, 'pos', y)
                self._data_pool.roi_parameter_changed(idx, axis, 'width', height)

        dock.setStyleSheet("""QDockWidget {font-size: 12pt; font-weight: bold;}""")

        widget.update_roi.connect(lambda roi_id: self.update_roi.emit(roi_id))
        widget.delete_me.connect(self._close_tab)
        self._roi_widgets[idx] = widget
        self._docks[idx] = dock

        for file_name, color in self._opened_files.items():
            self._roi_widgets[idx].add_file(file_name, color)

        widget.roi_changed()

        self.update_roi.emit(idx)

        return idx

    # ----------------------------------------------------------------------
    def _batch_process(self, mode):
        if mode == 'files':
            file_names, _ = QtWidgets.QFileDialog.getOpenFileNames(self, 'Select files',
                                                                   self.file_browser.current_folder(),
                                                                   'NEXUS files (*.nxs)')
        else:
            dir_name = QtWidgets.QFileDialog.getExistingDirectory(self, 'Select directory',
                                                                  self.file_browser.current_folder())

            file_names = [name for name in os.listdir(dir_name) if name.endswith('.nxs')]

        save_dir = QtWidgets.QFileDialog.getExistingDirectory(self, 'Save to', self.file_browser.current_folder())
        if save_dir:
            self._data_pool.batch_process_rois(file_names, save_dir, '.txt')

    # ----------------------------------------------------------------------
    def _add_dock(self, WidgetClass, label, location, *args, **kwargs):
        """
        """
        widget = WidgetClass(*args, **kwargs)

        dock = QtWidgets.QDockWidget(label)
        dock.setFocusPolicy(QtCore.Qt.StrongFocus)
        dock.setObjectName(f"{label}Dock")
        dock.setWidget(widget)

        children = [child for child in self.findChildren(QtWidgets.QDockWidget)
                    if isinstance(child.widget(), SectionView)]
        if children:
            self.tabifyDockWidget(children[-1], dock)
        else:
            self.addDockWidget(QtCore.Qt.LeftDockWidgetArea, dock)

        self._menu_rois.addAction(dock.toggleViewAction())

        return widget, dock

    # ----------------------------------------------------------------------
    def _close_tab(self, roi_id):
        self._data_pool.delete_roi(roi_id)
        self._parent.delete_roi(roi_id)

        self.removeDockWidget(self._docks[roi_id])

        del self._docks[roi_id]
        del self._roi_widgets[roi_id]

        for idx, dock in enumerate(list(self._docks.values())):
            dock.setWindowTitle(f'ROI {idx}')

    # ----------------------------------------------------------------------
    def current_folder(self):
        return self._parent.get_current_folder()

    # ----------------------------------------------------------------------
    def add_file(self, file_name):
        self._opened_files[file_name] = self._last_color + 1
        self._last_color += 1
        for widget in self._roi_widgets.values():
            widget.add_file(file_name, self._last_color)

    # ----------------------------------------------------------------------
    def delete_file(self, file_name):
        del self._opened_files[file_name]

        for widget in self._roi_widgets.values():
            widget.main_file_changed()
            widget.delete_file(file_name)

    # ----------------------------------------------------------------------
    def update_plots(self):
        for widget in self._roi_widgets.values():
            widget.update_limits()
            widget.update_plots()

    # ----------------------------------------------------------------------
    def units_changed(self):

        for widget in self._roi_widgets.values():
            widget.units_changed()

    # ----------------------------------------------------------------------
    def roi_changed(self, roi_id):

        self._roi_widgets[roi_id].roi_changed()

    # ----------------------------------------------------------------------
    def main_file_changed(self):
        for widget in self._roi_widgets.values():
            widget.main_file_changed()

    # ----------------------------------------------------------------------
    def load_ui_settings(self, settings):
        try:
            self.restoreGeometry(settings.value("{}/geometry".format(WIDGET_NAME)))
        except Exception as err:
            logger.error("{} : cannot restore geometry: {}".format(WIDGET_NAME, err))

    # ----------------------------------------------------------------------
    def save_ui_settings(self, settings):
        settings.setValue("{}/geometry".format(WIDGET_NAME), self.saveGeometry())
