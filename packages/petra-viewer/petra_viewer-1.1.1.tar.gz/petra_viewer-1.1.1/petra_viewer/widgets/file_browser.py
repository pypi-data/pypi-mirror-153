# Created by matveyev at 15.02.2021

import platform
import os
import logging

try:
    from watchdog.observers import Observer
    from watchdog.events import PatternMatchingEventHandler
except:
    pass

try:
    import PyTango
except:
    pass

from petra_viewer.widgets.breadcrumbsaddressbar.platform.common import if_platform

if platform.system() == "Windows":
    from petra_viewer.widgets.breadcrumbsaddressbar.platform.windows import (
        event_device_connection, parse_message)

from PyQt5 import QtWidgets, QtCore

from petra_viewer.widgets.abstract_widget import AbstractWidget
from petra_viewer.gui.file_browser_ui import Ui_FileBrowser

from petra_viewer.utils.utils import FileFilter
from petra_viewer.data_sources.sardana.sardana_data_set import SETTINGS
from petra_viewer.main_window import APP_NAME

WIDGET_NAME = 'DataBrowser'

file_formats = ["*.nxs", "*.h5"]

FILE_REFRESH_PERIOD = 1

logger = logging.getLogger(APP_NAME)


# ----------------------------------------------------------------------
class FileBrowser(AbstractWidget):
    """
    """

    file_selected = QtCore.pyqtSignal(str, str)

    # ----------------------------------------------------------------------
    def __init__(self, parent, mode):
        """
        """
        super(FileBrowser, self).__init__(parent)
        self._ui = Ui_FileBrowser()
        self._ui.setupUi(self)
        self._mode = mode

        self._file_model = QtWidgets.QFileSystemModel()
        self._file_model.setFilter(QtCore.QDir.AllDirs | QtCore.QDir.NoDot | QtCore.QDir.NoDotDot | QtCore.QDir.Files)
        self._file_model.setNameFilters(file_formats)
        self._file_model.setNameFilterDisables(False)

        self._eid = None
        self._door_server = None

        self.file_filter = FileFilter()
        try:
            self.file_filter.setRecursiveFilteringEnabled(True)
        except AttributeError:
            self.file_filter.new_version = False
        self.file_filter.setSourceModel(self._file_model)

        self._ui.tr_file_browser.setModel(self.file_filter)
        self._ui.tr_file_browser.hideColumn(2)
        self._ui.tr_file_browser.hideColumn(1)

        self._ui.tr_file_browser.header().setSortIndicatorShown(True)
        self._ui.tr_file_browser.setSortingEnabled(True)
        self._ui.tr_file_browser.sortByColumn(0, QtCore.Qt.SortOrder.AscendingOrder)

        path = os.getcwd()
        self.address = self._ui.breadcrumbsaddressbar
        self.address.set_path(path)
        self.address.path_selected.connect(self._set_tree_to_path)
        self._set_tree_to_path(path)

        try:
            self._my_event_handler = PatternMatchingEventHandler(file_formats, "", False, True)
            self._my_event_handler.on_any_event = self._on_created

            self._my_observer = None
        except:
            self._ui.chk_monitor.setEnabled(False)

        self._ui.tr_file_browser.doubleClicked.connect(self._open_folder)
        self._ui.le_filter.textEdited.connect(self._apply_filter)
        self._ui.chk_monitor.clicked.connect(self._toggle_watch_dog)

        if self._mode == 'sardana':
            self._ui.chk_door.clicked.connect(self._toggle_watch_door)
        else:
            self._ui.chk_door.setVisible(False)

        self._ui.cmd_reload.clicked.connect(self._reload)

    # ----------------------------------------------------------------------
    @if_platform('Windows')
    def nativeEvent(self, eventType, message):
        msg = parse_message(message)
        devices = event_device_connection(msg)
        if devices:
            print("insert/remove device")
            self.address.update_rootmenu_devices()
        return False, 0

    # ----------------------------------------------------------------------
    def load_ui_settings(self, settings):
        super(FileBrowser, self).load_ui_settings(settings)
        try:
            path = settings.value(f"{WIDGET_NAME}/last_path")
            self.address.set_path(path)
            self._set_tree_to_path(path)
        except:
            pass

    # ----------------------------------------------------------------------
    def save_ui_settings(self, settings):
        super(FileBrowser, self).save_ui_settings(settings)
        settings.setValue(f"{WIDGET_NAME}/last_path", self.address.path())

    # ----------------------------------------------------------------------
    def _reload(self):
        current_folder = self.file_filter.mapToSource(self._ui.tr_file_browser.rootIndex())
        parent = self.file_filter.mapToSource(self.file_filter.parent(self._ui.tr_file_browser.rootIndex()))
        self._file_model.setRootPath(self._file_model.filePath(parent))
        self._file_model.setRootPath(self._file_model.filePath(current_folder))

    # ----------------------------------------------------------------------
    def apply_settings(self):
        try:
            if self._mode == 'sardana':
                if 'door_address' in SETTINGS:
                    if self._eid is not None:
                        self._toggle_watch_door(False)
                        _need_to_reset = True
                    else:
                        _need_to_reset = False
                    if SETTINGS['door_address'] is not None:
                        try:
                            self._door_server = PyTango.DeviceProxy(SETTINGS['door_address'])
                            if _need_to_reset:
                                self._toggle_watch_door(True)
                        except:
                            self._parent.report_error('Cannot connect to {}'.format(SETTINGS['door_address']))

        except Exception as err:
            logger.error("{} : cannot apply settings: {}".format(WIDGET_NAME, err), exc_info=True)

    # ----------------------------------------------------------------------
    def safe_close(self):
        if self._eid is not None:
            self._door_server.unsubscribe_event(self._eid)

    # ----------------------------------------------------------------------
    def _toggle_watch_door(self, state):
        if state:
            if self._door_server is not None:
                try:
                    self._eid = self._door_server.subscribe_event('Info', PyTango.EventType.CHANGE_EVENT, self.new_info)
                except Exception as err:
                    self._parent.report_error("Cannot plug to the door", repr(err))
        else:
            if self._eid is not None:
                self._door_server.unsubscribe_event(self._eid)
                self._eid = None

    # ----------------------------------------------------------------------
    def new_info(self, event):
        if not event.err:
            if event.attr_value.value is not None:
                info = str(event.attr_value.value[0])
                if info.startswith("Operation saved in") and info.endswith('(nxs)'):
                    self.file_selected.emit(info.strip("Operation saved in").strip('(nxs)').strip(), self._mode)

    # ----------------------------------------------------------------------
    def _set_tree_to_path(self, path):

        path = str(path)
        self._file_model.setRootPath(path)
        self._ui.tr_file_browser.setRootIndex(self.file_filter.mapFromSource(self._file_model.index(path)))

    # ----------------------------------------------------------------------
    def _open_folder(self):

        selected_index = self._ui.tr_file_browser.selectionModel().currentIndex()
        file_index = self.file_filter.mapToSource(selected_index)
        if self._file_model.isDir(file_index):
            self.address.set_path(str(self._file_model.filePath(file_index)))
        else:
            file_name = str(self._file_model.filePath(file_index))
            self.file_selected.emit(file_name, self._mode)

    # ----------------------------------------------------------------------
    def _apply_filter(self, text):

        self.file_filter.setFilterRegExp(text)
        self.file_filter.setFilterCaseSensitivity(QtCore.Qt.CaseInsensitive)
        self.file_filter.setDynamicSortFilter(True)

        if text != '':
            self._ui.tr_file_browser.expandAll()
        else:
            self._ui.tr_file_browser.collapseAll()

    # ----------------------------------------------------------------------
    def current_folder(self):
        return self._file_model.filePath(self.file_filter.mapToSource(self._ui.tr_file_browser.rootIndex()))

    # ----------------------------------------------------------------------
    def _change_observer_folder(self):
        if self._ui.chk_monitor.isChecked():
            if self._my_observer is not None:
                self._my_observer.stop()
                self._my_observer.join()

            folder = self._file_model.filePath(self.file_filter.mapToSource(self._ui.tr_file_browser.rootIndex()))

            if folder != '':
                self._my_observer = Observer()
                self._my_observer.schedule(self._my_event_handler, folder, recursive=True)
                self._my_observer.start()

    # ----------------------------------------------------------------------
    def _toggle_watch_dog(self, state):
        if state:
            self._change_observer_folder()
        else:
            if self._my_observer is not None:
                self._my_observer.stop()
                self._my_observer.join()
                self._my_observer = None

    # ----------------------------------------------------------------------
    def _on_created(self, event):
        for type in file_formats:
            if type in event.src_path:
                self.file_selected.emit(event.src_path, self._mode)
