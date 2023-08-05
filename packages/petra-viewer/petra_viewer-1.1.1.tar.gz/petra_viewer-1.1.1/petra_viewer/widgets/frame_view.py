# Created by matveyev at 15.02.2021

WIDGET_NAME = 'FrameView'

import logging
import configparser
from distutils.util import strtobool

from PyQt5 import QtWidgets, QtCore, QtGui, QtPrintSupport

from petra_viewer.main_window import APP_NAME
from petra_viewer.utils.fake_image_item import FakeImageItem
from petra_viewer.widgets.abstract_widget import AbstractWidget
from petra_viewer.widgets.view_2d import ViewPyQt, ViewSilx
from petra_viewer.gui.frame_view_ui import Ui_FrameView

logger = logging.getLogger(APP_NAME)


# ----------------------------------------------------------------------
class FrameView(AbstractWidget):
    """
    """
    section_updated = QtCore.pyqtSignal()
    main_file_changed = QtCore.pyqtSignal()

    clear_view = QtCore.pyqtSignal()
    roi_moved = QtCore.pyqtSignal(int)
    new_axes = QtCore.pyqtSignal()

    new_units = QtCore.pyqtSignal()

    # ----------------------------------------------------------------------
    def __init__(self, parent, data_pool, settings):
        """
        """
        super(FrameView, self).__init__(parent)
        self._ui = Ui_FrameView()
        self._ui.setupUi(self)

        self._ui.cut_selectors.set_data_pool(data_pool)

        self.hist = self._ui.hist
        self.hist.setBackground('w')

        self._signals_blocked = False

        try:
            self.backend = settings['FRAME_VIEW']['backend']
        except:
            self.backend = 'pyqt'

        self.hist_mode = 'selected'
        self.auto_levels = True

        try:
            if settings['FRAME_VIEW']['levels'] == 'selection':
                self._ui.rb_hist_selected.setChecked(True)
                self.hist_mode = 'selected'
            else:
                self._ui.rb_hist_all.setChecked(True)
                self.hist_mode = 'all'
        except:
            self._ui.rb_hist_selected.setChecked(True)

        if self.backend == 'pyqt':
            self._main_view = ViewPyQt(self, 'main', data_pool)
            self._second_view = ViewPyQt(self, 'second', data_pool)

            self._fake_image_item = FakeImageItem(data_pool, self._main_view.plot_2d)

            if self.hist_mode == 'all':
                self.hist.item.setImageItem(self._fake_image_item)
            else:
                self.hist.item.setImageItem(self._main_view.plot_2d)

            self.level_mode = 'lin'

            self._ui.chk_auto_levels.clicked.connect(self._toggle_auto_levels)
            self._ui.bg_lev_mode.buttonClicked.connect(self._change_level_mode)
            self._ui.bg_hist_selection.buttonClicked.connect(self._change_hist_mode)
            self.hist.scene().sigMouseClicked.connect(self._hist_mouse_clicked)
            self.hist.item.sigLevelChangeFinished.connect(lambda: self._toggle_auto_levels(False))
            self.hist.item.sigLookupTableChanged.connect(self._new_lookup_table)

            self._main_view.roi_moved.connect(lambda roi_id: self.roi_moved.emit(roi_id))
            self._main_view.roi_moved.connect(lambda roi_id: self._second_view.roi_changed(roi_id))

            self._second_view.roi_moved.connect(lambda roi_id: self.roi_moved.emit(roi_id))
            self._second_view.roi_moved.connect(lambda roi_id: self.second_view.roi_changed(roi_id))

            self._setup_actions()

        else:
            self._main_view = ViewSilx(self, 'main', data_pool)
            self._second_view = ViewSilx(self, 'second', data_pool)

            self._ui.fr_hist.setVisible(False)

        self._second_view.hide()

        self._ui.view_layout.addWidget(self._main_view, 0)
        self._ui.view_layout.addWidget(self._second_view, 0)

        self._status_bar = QtWidgets.QStatusBar(self)
        self._ui.v_layout.addWidget(self._status_bar, 0)

        self._shape_label = QtWidgets.QLabel("")
        self._status_bar.addPermanentWidget(self._shape_label)

        self._coordinate_label = QtWidgets.QLabel("")
        self._status_bar.addPermanentWidget(self._coordinate_label)

        self.current_frames = [0, 0]
        self.level_mode = 'lin'
        self.max_frame = 0

        self._ui.cut_selectors.layout().setSpacing(0)
        self._ui.cut_selectors.layout().setContentsMargins(0, 0, 0, 0)

        self.data_pool = data_pool

    # ----------------------------------------------------------------------
    def _block_hist_signal(self, state):
        if state:
            for signal in [self.hist.scene().sigMouseClicked,
                           self.hist.item.sigLevelChangeFinished,
                           self.hist.item.sigLookupTableChanged]:
                try:
                    signal.disconnect()
                except:
                    pass

        else:
            self.hist.scene().sigMouseClicked.connect(self._hist_mouse_clicked)
            self.hist.item.sigLevelChangeFinished.connect(lambda: self._toggle_auto_levels(False))
            self.hist.item.sigLookupTableChanged.connect(self._new_lookup_table)

    # ----------------------------------------------------------------------
    def set_settings(self, settings):

        if self.backend == 'pyqt':
            for action in ['axes', 'axes_titles', 'grid', 'cross', 'aspect']:
                try:
                    getattr(self, f'action_{action}').setChecked(strtobool(settings[f'display_{action}']))
                except Exception as err:
                    logger.error("{} : cannot apply settings: {}".format(WIDGET_NAME, err), exc_info=True)

    # ----------------------------------------------------------------------
    def add_file(self, file_name, move_from='second', move_action=False):

        logger.debug(f"Add file {file_name}, view: {move_from}")
        if move_from == 'second':
            self._main_view.add_file(file_name)
            self.data_pool.protect_file(file_name, False)
        else:
            self._second_view.add_file(file_name)
            self.data_pool.protect_file(file_name, True)

        if not move_action:
            self.new_main_file()

    # ----------------------------------------------------------------------
    def get_current_rect(self):
        return self._main_view.get_current_rect()

    # ----------------------------------------------------------------------
    def roi_changed(self, roi_ind):

        self._main_view.roi_changed(roi_ind)
        self._second_view.roi_changed(roi_ind)

    # ----------------------------------------------------------------------
    def add_roi(self, idx):

        self._main_view.add_roi(idx)
        self._second_view.add_roi(idx)

    # ----------------------------------------------------------------------
    def file_closed_by_pool(self, file_name):

        self._main_view.file_closed_by_pool(file_name)
        self._second_view.file_closed_by_pool(file_name)

    # ----------------------------------------------------------------------
    def new_coordinate(self, source, x_value, y_value, pos):

        self._coordinate_label.setText(f'Current coordinates: X: {x_value}, Y: {y_value}')

        if source == 'main':
            self._second_view.move_marker(pos)
        else:
            self._main_view.move_marker(pos)

    # ----------------------------------------------------------------------
    def new_view_box(self, source, view_rect):

        if source == 'main':
            self._second_view.new_view_box(view_rect)
        else:
            self._main_view.new_view_box(view_rect)

    # ----------------------------------------------------------------------
    def delete_roi(self, idx):

        self._main_view.delete_roi(idx)
        self._second_view.delete_roi(idx)

    # ----------------------------------------------------------------------
    def update_axes(self, axes_labels):

        self._main_view.new_axes(axes_labels)
        self._second_view.new_axes(axes_labels)

        self.update_images()

        if not self._signals_blocked:
            self.new_axes.emit()

    # ----------------------------------------------------------------------
    def _new_lookup_table(self):

        self._second_view.new_lookup_table()

    # ----------------------------------------------------------------------
    def get_levels(self):
        if self.hist_mode == 'selected':
            return self._main_view.plot_2d.levels
        else:
            return self._fake_image_item.levels

    # ----------------------------------------------------------------------
    def _change_chk_auto_levels_state(self, state):
        self._ui.chk_auto_levels.blockSignals(True)
        self._ui.chk_auto_levels.setChecked(state)
        self._ui.chk_auto_levels.blockSignals(False)

    # ----------------------------------------------------------------------
    def _toggle_auto_levels(self, state):

        self.auto_levels = state

        if state:
            self._block_hist_signal(True)
            if self.hist_mode == 'all':
                self._fake_image_item.setAutoLevels()
                l_min, l_max = self._fake_image_item.levels
                self.hist.item.setLevels(l_min, l_max)
            else:
                self.hist.item.autoHistogramRange()
            self._block_hist_signal(False)

            self.update_images()
        else:
            self._change_chk_auto_levels_state(False)

        self._second_view.new_levels()

    # ----------------------------------------------------------------------
    def _change_hist_mode(self, button):

        if button == self._ui.rb_hist_selected:
            self.hist_mode = 'selected'
            self.hist.item.setImageItem(self._main_view.plot_2d)
        else:
            self.hist_mode = 'all'
            self.hist.item.setImageItem(self._fake_image_item)

        self._change_chk_auto_levels_state(True)

    # ----------------------------------------------------------------------
    def _change_level_mode(self, button):

        if button == self._ui.rb_lin_levels:
            self.level_mode = 'lin'
        elif button == self._ui.rb_sqrt_levels:
            self._level_mode = 'sqrt'
        else:
            self.level_mode = 'log'

        if self.hist_mode == 'all':
            self._fake_image_item.setMode(self.level_mode)

        self._toggle_auto_levels(True)
        self._change_chk_auto_levels_state(True)

    # ----------------------------------------------------------------------
    def _hist_mouse_clicked(self, event):

        if event.double():
            if self._main_view.current_file is not None:
                self._toggle_auto_levels(True)
                self._change_chk_auto_levels_state(True)

    # ----------------------------------------------------------------------
    def get_current_axes(self):

        selection = self._ui.cut_selectors.get_current_selection()

        return {'x': [ind for ind, sect in enumerate(selection) if sect['axis'] == 'X'][0],
                'y': [ind for ind, sect in enumerate(selection) if sect['axis'] == 'Y'][0]}

    # ----------------------------------------------------------------------
    def data_updated(self):
        if self._main_view.current_file is not None:
            self._toggle_auto_levels(True)
            self._change_chk_auto_levels_state(True)
            if self.hist_mode == 'all':
                self._fake_image_item.sigImageChanged.emit()

    # ----------------------------------------------------------------------
    def new_cut(self, invisible_axis):
        self.update_images()
        if invisible_axis:
            self.new_axes.emit()

    # ----------------------------------------------------------------------
    def set_new_units(self, axis, units, axes_labels):
        self.data_pool.recalculate_rois(axis, units)

        for file in self._main_view.get_files_list() + self._second_view.get_files_list():
            self.data_pool.set_axis_units(file, axis, units)

        self._main_view.new_axes(axes_labels)
        self._second_view.new_axes(axes_labels)

        self.update_images()

        self.new_units.emit()

    # ----------------------------------------------------------------------
    def _set_section_for_second_view(self, file, section):
        if self.data_pool.get_file_dimension(self._second_view.current_file) != \
                self.data_pool.get_file_dimension(self._main_view.current_file):
            return False

        if not self.data_pool.are_axes_valid(self._second_view.current_file):
            return False

        new_section = []

        for ind, axis_param in enumerate(section):

            v_min = self.data_pool.get_value_for_frame(self._main_view.current_file, ind, axis_param['min'])
            v_min = self.data_pool.get_frame_for_value(self._second_view.current_file, ind, v_min,
                                                       axis_param['axis'] not in ['X', 'Y'])

            v_max = self.data_pool.get_value_for_frame(self._main_view.current_file, ind, axis_param['max'])
            v_max = self.data_pool.get_frame_for_value(self._second_view.current_file, ind, v_max,
                                                       axis_param['axis'] not in ['X', 'Y'] and axis_param['integration'])

            if v_min is None or v_max is None:
                return False

            new_params = dict(axis_param)
            new_params.update({'min': v_min, 'max': v_max})
            new_section.append(new_params)

        self.data_pool.save_section(file, new_section)

        return True

    # ----------------------------------------------------------------------
    def update_second_view_image(self):
        selection = self.data_pool.get_section(self._main_view.current_file)

        second_view_is_valid = True
        for file in self._second_view.get_files_list():
            second_view_is_valid = self._set_section_for_second_view(file, selection)

        if second_view_is_valid:
            self._second_view.update_image()
        else:
            self._second_view.clear_view()

    # ----------------------------------------------------------------------
    def update_images(self):

        selection = self._ui.cut_selectors.get_current_selection()
        logger.debug(f"Saving selection {selection} for file {self._main_view.current_file}")
        self.data_pool.save_section(self._main_view.current_file, selection)

        logger.debug(f"Update image with sel {selection}")

        if self.backend == 'pyqt':
            self._block_hist_signal(True)

        self._main_view.update_image()
        self.update_second_view_image()

        if self.backend == 'pyqt':
            self._block_hist_signal(False)

        self.section_updated.emit()

    # ----------------------------------------------------------------------
    def _setup_limits(self):
        """
        Set ranges for all selectors
        """
        if self._main_view.current_file is None:
            return

        limits = self.data_pool.get_file_axis_limits(self._main_view.current_file)
        self._ui.cut_selectors.set_limits(limits)

        self._shape_label.setText(f"Data shape: {limits}")

    # ----------------------------------------------------------------------
    def current_file(self):
        return self._main_view.current_file

    # ----------------------------------------------------------------------
    def update_file(self, file_key):
        """
        Update widget parameters to reflect changes in the data shape _refresh_selectors of given stream.
        """
        if self._main_view.current_file == file_key and file_key is not None:
            self._setup_limits()

            sections = self.data_pool.get_section(self._main_view.current_file)
            axes_names = self.data_pool.get_file_axes(self._main_view.current_file)
            logger.debug(f"Setup frame_view selectors with section: {sections}")
            self._ui.cut_selectors.set_section(sections)

            axes_labels = [name for s, name in zip(sections, axes_names) if s['axis'] == 'X']
            axes_labels += [name for s, name in zip(sections, axes_names) if s['axis'] == 'Y']
            self.update_axes(axes_labels)

    # ----------------------------------------------------------------------
    def new_main_file(self):
        """
        Update widget in case if main file was changed
        """
        if self._main_view.current_file is None:
            self._fake_image_item.setEmptyFile()
            self._change_chk_auto_levels_state(True)
            self._ui.cut_selectors.refresh_selectors()
            self.clear_view.emit()
            return

        self._ui.cut_selectors.refresh_selectors()
        if self.backend == 'pyqt':
            self._fake_image_item.setNewFile(self._main_view.current_file)
            self._change_chk_auto_levels_state(True)

        self._signals_blocked = True
        self.update_file(self._main_view.current_file)
        if self._main_view.previous_file is not None:
            old_axes = self.data_pool.get_file_axes(self._main_view.previous_file)
            if not self._ui.cut_selectors.set_axes(old_axes):
                self._parent.report_error(f'File cannot be displayed in {old_axes} \nsetting {self.data_pool.get_file_axes(self._main_view.current_file)}')
        self._signals_blocked = False
        self.main_file_changed.emit()

    # ----------------------------------------------------------------------
    def _setup_actions(self):

        toolbar = QtWidgets.QToolBar("Main toolbar", self)

        label = QtWidgets.QLabel("Level and colors: ", self)
        toolbar.addWidget(label)

        action_levels = toolbar.addAction(QtGui.QIcon(QtGui.QPixmap(":/icon/colormap.png")), "Grid")
        action_levels.setCheckable(True)
        action_levels.setChecked(True)
        action_levels.toggled.connect(lambda flag: self._ui.fr_hist.setVisible(flag))

        toolbar.addSeparator()

        label = QtWidgets.QLabel("Lock aspect: ", self)
        toolbar.addWidget(label)

        self.action_aspect = toolbar.addAction(QtGui.QIcon(QtGui.QPixmap(":/icon/aspect.png")), "Aspect ratio")
        self.action_aspect.setCheckable(True)
        self.action_aspect.toggled.connect(lambda flag, setting='aspect': self._apply_setting(setting, flag))

        toolbar.addSeparator()

        label = QtWidgets.QLabel("Axes and grid: ", self)
        toolbar.addWidget(label)

        self.action_axes = toolbar.addAction(QtGui.QIcon(QtGui.QPixmap(":/icon/axes.png")), "Axes")
        self.action_axes.setCheckable(True)
        self.action_axes.toggled.connect(lambda flag, setting='axes': self._apply_setting(setting, flag))

        self.action_axes_titles = toolbar.addAction(QtGui.QIcon(QtGui.QPixmap(":/icon/titles.png")), "Titles")
        self.action_axes_titles.setCheckable(True)
        self.action_axes_titles.toggled.connect(lambda flag, setting='titles': self._apply_setting(setting, flag))

        self.action_grid = toolbar.addAction(QtGui.QIcon(QtGui.QPixmap(":/icon/grid.png")), "Grid")
        self.action_grid.setCheckable(True)
        self.action_grid.toggled.connect(lambda flag, setting='grid': self._apply_setting(setting, flag))

        self.action_cross = toolbar.addAction(QtGui.QIcon(QtGui.QPixmap(":/icon/crosshair.png")), "Crosshair")
        self.action_cross.setCheckable(True)
        self.action_cross.toggled.connect(lambda flag, setting='cross': self._apply_setting(setting, flag))

        toolbar.addSeparator()

        label = QtWidgets.QLabel("Export image: ", self)
        toolbar.addWidget(label)

        print_action = toolbar.addAction(QtGui.QIcon(QtGui.QPixmap(":/icon/print.png")), "Print")
        print_action.triggered.connect(self._print)

        action = toolbar.addAction(QtGui.QIcon(QtGui.QPixmap(":/icon/copy.png")), "Copy to Clipboard")
        action.triggered.connect(self._copy_to_clipboard)

        action = toolbar.addAction(QtGui.QIcon(QtGui.QPixmap(":/icon/save.png")), "Save")
        action.triggered.connect(self._save)

        toolbar.addSeparator()

        self._ui.v_layout.insertWidget(0, toolbar, 0)

    # ----------------------------------------------------------------------
    def _apply_setting(self, setting, state):
        self._main_view.apply_setting(setting, state)
        self._second_view.apply_setting(setting, state)

    # ----------------------------------------------------------------------
    def _save(self):
        default_name = self._parent.get_current_folder()
        file_name, format = QtWidgets.QFileDialog.getSaveFileName(self, 'Save as', default_name,
                                                             'Windows Bitmap (*.bmp);; Joint Photographic Experts Group (*jpg);; Portable Network Graphics (*.png);; Portable Pixmap (*.ppm); X11 Bitmap (*.xbm);; X11 Pixmap (*.xpm)')
        if file_name:
            file_name += format.split('*')[1].strip('()')
            pix = QtGui.QPixmap(self._ui.view_widget.size())
            self._ui.view_widget.render(pix)
            pix.save(file_name)

    # ----------------------------------------------------------------------
    def _copy_to_clipboard(self):
        QtWidgets.qApp.clipboard().setPixmap(self._ui.view_widget.grab())

    # ----------------------------------------------------------------------
    def _print(self):
        dialog = QtPrintSupport.QPrintPreviewDialog()
        dialog.paintRequested.connect(self.handlePaintRequest)
        dialog.exec_()

    # ----------------------------------------------------------------------
    def handlePaintRequest(self, printer):
        self._ui.view_widget.render(QtGui.QPainter(printer))

