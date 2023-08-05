# Created by matveyev at 19.02.2021

WIDGET_NAME = 'CubeView'

import pyqtgraph.opengl as gl
import numpy as np

from distutils.util import strtobool

from PyQt5 import QtWidgets, QtCore

from petra_viewer.utils.axes_3d import Custom3DAxis
from petra_viewer.utils.fake_image_item import FakeImageItem
from petra_viewer.utils.utils import refresh_combo_box
from petra_viewer.widgets.abstract_widget import AbstractWidget
from petra_viewer.gui.cube_view_ui import Ui_CubeView


# ----------------------------------------------------------------------
class CubeView(AbstractWidget):
    """
    """

    # ----------------------------------------------------------------------
    def __init__(self, parent, data_pool):
        """
        """
        super(CubeView, self).__init__(parent)
        self._ui = Ui_CubeView()
        self._ui.setupUi(self)

        self._data_pool = data_pool

        self._visible = True
        self._view_is_actual = True
        self._hist_is_actual = True

        self._fake_image_item = FakeImageItem(data_pool)
        self._ui.hist.item.setImageItem(self._fake_image_item)
        self._ui.hist.setBackground('w')

        self.view_widget = gl.GLViewWidget()
        # self.view_widget.orbit(256, 256)
        # self.view_widget.setCameraPosition(0, 0, 0)
        # self.view_widget.opts['distance'] = 200

        self.axes = Custom3DAxis(self.view_widget, color=(0.2,0.2,0.2,.6))
        self.view_widget.addItem(self.axes)

        self.volume_item = None
        self._default_scale = np.array([1, 1, 1])
        self._current_scale = np.array([1, 1, 1])
        self._view_distance = 1

        self._ui.h_layout.insertWidget(1, self.view_widget, 1)

        self._ui.cmb_area.currentIndexChanged.connect(self.display_file)

        self._ui.sp_slices.valueChanged.connect(self.display_file)
        self._ui.chk_smooth.clicked.connect(self.display_file)
        self._ui.sp_borders.valueChanged.connect(self.display_file)
        self._ui.chk_white_bck.stateChanged.connect(self._set_background)

        self._ui.sp_cam_distance.valueChanged.connect(self._move_camera)
        self._ui.sp_cam_elevation.valueChanged.connect(self._move_camera)
        self._ui.sp_cam_azimuth.valueChanged.connect(self._move_camera)

        self._ui.cmd_reset_camera.clicked.connect(self._reset_view)

        self._ui.sp_x_scale.valueChanged.connect(self._scale)
        self._ui.sp_y_scale.valueChanged.connect(self._scale)
        self._ui.sp_z_scale.valueChanged.connect(self._scale)

        self._ui.cmd_reset_scale.clicked.connect(self._reset_scale)

        self._ui.hist.item.sigLevelChangeFinished.connect(lambda: self._auto_levels(False))
        self._ui.hist.item.sigLookupTableChanged.connect(self.display_file)

        self._ui.hist.scene().sigMouseClicked.connect(self._hist_mouse_clicked)

        self._ui.chk_auto_levels.clicked.connect(self._auto_levels)

        self._ui.bg_lev_mode.buttonClicked.connect(self._change_level_mode)

        self._status_timer = QtCore.QTimer(self)
        self._status_timer.timeout.connect(self._refresh_camera_position)
        self._status_timer.start(100)

    # ----------------------------------------------------------------------
    def _get_area(self):
        current_choose = self._ui.cmb_area.currentText()
        if current_choose == 'Whole cube':
            return -1
        else:
            return self._data_pool.get_roi_key(int(current_choose.split('_')[1]))

    # ----------------------------------------------------------------------
    def _auto_levels(self, state):
        if state:
            self._block_hist_signals(True)

            self._fake_image_item.setAutoLevels()
            l_min, l_max = self._fake_image_item.levels
            self._ui.hist.item.setLevels(l_min, l_max)

            self._block_hist_signals(False)
        else:
            self._change_chk_auto_levels_state(False)

        self.display_file()

    # ----------------------------------------------------------------------
    def _hist_mouse_clicked(self, event):

        if event.double():
            self._auto_levels(True)
            self._change_chk_auto_levels_state(True)

    # ----------------------------------------------------------------------
    def _change_level_mode(self, button):

        self._block_hist_signals(True)

        if button == self._ui.rb_lin_levels:
            self._fake_image_item.setMode('lin')
        elif button == self._ui.rb_sqrt_levels:
            self._fake_image_item.setMode('sqrt')
        else:
            self._fake_image_item.setMode('log')

        self._block_hist_signals(False)

        self._auto_levels(True)
        self._change_chk_auto_levels_state(True)

    # ----------------------------------------------------------------------
    def _change_chk_auto_levels_state(self, state):
        self._ui.chk_auto_levels.blockSignals(True)
        self._ui.chk_auto_levels.setChecked(state)
        self._ui.chk_auto_levels.blockSignals(False)

    # ----------------------------------------------------------------------
    def _refresh_camera_position(self):
        for param in ['distance', 'elevation', 'azimuth']:
            if not getattr(self._ui, f'sp_cam_{param}').hasFocus():
                getattr(self._ui, f'sp_cam_{param}').blockSignals(True)
                getattr(self._ui, f'sp_cam_{param}').setValue(int(self.view_widget.opts[param]))
                getattr(self._ui, f'sp_cam_{param}').blockSignals(False)

    # ----------------------------------------------------------------------
    def set_settings(self, settings):

        self._block_signals(True)

        if 'slices' in settings:
            self._ui.sp_slices.setValue(int(settings['slices']))

        if 'smooth' in settings:
            self._ui.chk_smooth.setChecked(strtobool(settings['smooth']))

        if 'borders' in settings:
            self._ui.sp_borders.setValue(int(settings['borders']))

        if 'white_background' in settings:
            self._ui.chk_white_bck.setChecked(strtobool(settings['white_background']))

        self.display_file()

        self._block_signals(False)

    # ----------------------------------------------------------------------
    def fill_roi(self):
        current_selection = self._ui.cmb_area.currentText()
        self._ui.cmb_area.blockSignals(True)
        self._ui.cmb_area.clear()
        self._ui.cmb_area.addItem('Whole cube')
        for ind in range(self._data_pool.roi_counts()):
            roi_key = self._data_pool.get_roi_key(ind)
            if self._data_pool.get_file_dimension(self._parent.get_current_file()) == self._data_pool.get_roi_param(roi_key, 'dimensions'):
                self._ui.cmb_area.addItem(f'ROI_{ind}')

        if not refresh_combo_box(self._ui.cmb_area, current_selection):
            self.display_file()

        self._ui.cmb_area.blockSignals(False)

    # ----------------------------------------------------------------------
    def _block_hist_signals(self, state):
        if state:
            self._ui.hist.item.sigLevelChangeFinished.disconnect()
            self._ui.hist.item.sigLookupTableChanged.disconnect()
        else:
            self._ui.hist.item.sigLevelChangeFinished.connect(lambda: self._auto_levels(False))
            self._ui.hist.item.sigLookupTableChanged.connect(self.display_file)

    # ----------------------------------------------------------------------
    def roi_changed(self, roi_ind):

        if roi_ind == self._get_area():
            self.display_file()

    # ----------------------------------------------------------------------
    def main_file_changed(self):

        self._block_hist_signals(True)
        self.fill_roi()
        self._hist_is_actual = False
        self._block_hist_signals(False)

        self.display_file()

    # ----------------------------------------------------------------------
    def data_updated(self):

        file_name = self._parent.get_current_file()
        if file_name is None:
            return

        self._auto_levels(True)
        self._change_chk_auto_levels_state(True)
        self._fake_image_item.sigImageChanged.emit()

    # ----------------------------------------------------------------------
    def clear_view(self):

        self._block_signals(True)

        if self.volume_item is not None:
            self.view_widget.removeItem(self.volume_item)
            self.volume_item = None

        self._ui.x_label.setText('')
        self._ui.y_label.setText('')
        self._ui.z_label.setText('')

        self._ui.sp_x_scale.setValue(1)
        self._ui.sp_y_scale.setValue(1)
        self._ui.sp_z_scale.setValue(1)

        self.axes.setSize(1, 1, 1)
        self.axes.set_x_label('')
        self.axes.set_y_label('')
        self.axes.set_z_label('')

        self._block_signals(False)

    # ----------------------------------------------------------------------
    def visibility_changed(self, state):
        self._visible = state
        if state and not self._view_is_actual:
            self.display_file()

    # ----------------------------------------------------------------------
    def display_file(self):

        if not self._visible:
            self._view_is_actual = False
            return

        if not self._hist_is_actual:
            self._fake_image_item.setNewFile(self._parent.get_current_file())
            self._hist_is_actual = True

        self.clear_view()

        file_name = self._parent.get_current_file()
        if file_name is None:
            return

        data, axes_names = self._data_pool.get_3d_cube(file_name, self._get_area())

        if data is None:
            return

        self._block_signals(True)

        levels = self._ui.hist.item.getLevels()

        if self._ui.rb_log_levels.isChecked():
            data = np.log(data + 1)
        elif self._ui.rb_sqrt_levels.isChecked():
            data = np.sqrt(data + 1)

        data = np.maximum(np.minimum((data - levels[0]) / float(levels[1] - levels[0]) * 255, 255), 0)

        data_to_display = np.zeros(data.shape + (4,), dtype=np.ubyte)
        data_to_display[..., 0] = 0 if self._ui.chk_white_bck.isChecked() else 255
        data_to_display[..., 1] = 0 if self._ui.chk_white_bck.isChecked() else 255
        data_to_display[..., 2] = 0 if self._ui.chk_white_bck.isChecked() else 255
        data_to_display[..., 3] = data

        borders = int(self._ui.sp_borders.value())
        if borders > 0:
            data_to_display = self._color_border(data_to_display, borders)

        self._default_scale = np.array([1, 1, 1])

        axes_sizes = data_to_display.shape[:3]
        max_size = np.max(data_to_display.shape[:3])
        for axis in range(3):
            if axes_sizes[axis] < max_size/3:
                self._default_scale[axis] = int(np.ceil(max_size/(3*axes_sizes[axis])))

        self._ui.sp_x_scale.setValue(self._default_scale[0])
        self._ui.sp_y_scale.setValue(self._default_scale[1])
        self._ui.sp_z_scale.setValue(self._default_scale[2])

        self._current_scale = self._default_scale

        self.volume_item = gl.GLVolumeItem(data_to_display,  sliceDensity=int(self._ui.sp_slices.value()),
                                           smooth=self._ui.chk_smooth.isChecked(), glOptions='translucent')

        self.volume_item.scale(self._default_scale[0], self._default_scale[1], self._default_scale[2])

        self.view_widget.addItem(self.volume_item)
        self.volume_item.translate(-data_to_display.shape[0] * self._default_scale[0] / 2,
                                   -data_to_display.shape[1] * self._default_scale[1] / 2,
                                   -data_to_display.shape[2] * self._default_scale[2] / 2)

        self._view_distance = max(data_to_display.shape)*5
        self.view_widget.setCameraPosition(distance=self._view_distance)

        self.axes.setSize(data_to_display.shape[0] * self._default_scale[0],
                          data_to_display.shape[1] * self._default_scale[1],
                          data_to_display.shape[2] * self._default_scale[2])

        self._ui.x_label.setText(axes_names[0])
        self.axes.set_x_label(axes_names[0])
        if len(axes_names) > 1:
            self._ui.y_label.setText(axes_names[1])
            self.axes.set_y_label(axes_names[1])
        if len(axes_names) > 2:
            self._ui.z_label.setText(axes_names[2])
            self.axes.set_z_label(axes_names[2])

        self._block_signals(False)

        self._view_is_actual = True

    @staticmethod
    # ----------------------------------------------------------------------
    def _color_border(data_to_display, borders):

        data_to_display[:, :borders, :borders] = [255, 0, 0, 255]
        data_to_display[:, :borders, -borders:] = [255, 0, 0, 255]
        data_to_display[:, -borders:, :borders] = [255, 0, 0, 255]
        data_to_display[:, -borders:, -borders:] = [255, 0, 0, 255]

        data_to_display[:borders, :, :borders] = [255, 0, 0, 255]
        data_to_display[:borders, :, -borders:] = [255, 0, 0, 255]
        data_to_display[-borders:, :, :borders] = [255, 0, 0, 255]
        data_to_display[-borders:, :, -borders:] = [255, 0, 0, 255]

        data_to_display[:borders, -borders:, :] = [255, 0, 0, 255]
        data_to_display[:borders, :borders, :] = [255, 0, 0, 255]
        data_to_display[-borders:, :borders, :] = [255, 0, 0, 255]
        data_to_display[-borders:, -borders:, :] = [255, 0, 0, 255]

        return data_to_display

    # ----------------------------------------------------------------------
    def _set_background(self, status):

        self.view_widget.setBackgroundColor('w' if status else 'b')
        self.display_file()

    # ----------------------------------------------------------------------
    def _reset_view(self):
        self.view_widget.reset()
        self.view_widget.setCameraPosition(distance=self._view_distance)
        self.view_widget.setBackgroundColor('w' if self._ui.chk_white_bck.isChecked() else 'b')

    # ----------------------------------------------------------------------
    def _move_camera(self):

        self.view_widget.setCameraPosition(distance=self._ui.sp_cam_distance.value(),
                                           elevation=self._ui.sp_cam_elevation.value(),
                                           azimuth=self._ui.sp_cam_azimuth.value())

    # ----------------------------------------------------------------------
    def _scale(self):

        new_scale = np.array([int(self._ui.sp_x_scale.value()),
                              int(self._ui.sp_y_scale.value()),
                              int(self._ui.sp_z_scale.value())])
        d_scale = new_scale/self._current_scale

        self.volume_item.scale(d_scale[0], d_scale[1], d_scale[2])

        self._current_scale = new_scale

    # ----------------------------------------------------------------------
    def _reset_scale(self):
        self._block_signals(True)

        self._ui.sp_x_scale.setValue(self._default_scale[0])
        self._ui.sp_y_scale.setValue(self._default_scale[1])
        self._ui.sp_z_scale.setValue(self._default_scale[2])

        self._scale()

        self._block_signals(False)

    # ----------------------------------------------------------------------
    def _block_signals(self, flag):

        self._ui.sp_slices.blockSignals(flag)
        self._ui.chk_smooth.blockSignals(flag)
        self._ui.sp_x_scale.blockSignals(flag)
        self._ui.sp_y_scale.blockSignals(flag)
        self._ui.sp_z_scale.blockSignals(flag)
