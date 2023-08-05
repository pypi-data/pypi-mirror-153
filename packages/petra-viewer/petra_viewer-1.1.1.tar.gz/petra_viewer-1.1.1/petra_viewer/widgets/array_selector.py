# Created by matveyev at 04.08.2021
import numpy as np
from PyQt5 import QtWidgets, QtCore
import logging

from petra_viewer.main_window import APP_NAME
from petra_viewer.gui.array_selector_ui import Ui_ArraySelector

logger = logging.getLogger(APP_NAME)


class ArraySelector(QtWidgets.QWidget):

    def __init__(self, my_id, cut_selector, data_pool, frame_viewer):
        """
        """
        super(ArraySelector, self).__init__()
        self._ui = Ui_ArraySelector()
        self._ui.setupUi(self)

        self._my_id = my_id
        self.limit_range = 0
        self._max_frame = 0

        self._old_z_min = None
        self._old_z_max = None

        self._data_pool = data_pool
        self._frame_viewer = frame_viewer
        self._cut_selector = cut_selector

        self._ui.sl_frame.valueChanged.connect(self._update_from_frame_slider)
        self._ui.sl_range.sliderMoved.connect(self._update_from_range_slider)

        self._ui.but_first.clicked.connect(lambda: self._update_from_navigation_buttons('first'))
        self._ui.but_previous.clicked.connect(lambda: self._update_from_navigation_buttons('previous'))
        self._ui.but_next.clicked.connect(lambda: self._update_from_navigation_buttons('next'))
        self._ui.but_last.clicked.connect(lambda: self._update_from_navigation_buttons('last'))

        self._ui.sp_value_from.editingFinished.connect(self._update_from_sp)
        self._ui.sp_value_to.editingFinished.connect(self._update_from_sp)

        self._ui.cmd_show_all.clicked.connect(self._show_all)

    # ----------------------------------------------------------------------
    def _new_cut(self):
        self._old_z_min = self._ui.sl_range.low()
        self._old_z_max = self._ui.sl_range.high()
        self._cut_selector.new_range(self._my_id)

    # ----------------------------------------------------------------------
    def switch_integration_mode(self, state):

        self._ui.sl_frame.setVisible(not state)
        self._ui.sl_range.setVisible(state)
        self._ui.sp_value_to.setVisible(state)
        self._ui.lb_to.setVisible(state)

    # ----------------------------------------------------------------------
    def _show_all(self):
        self._set_spin_boxes(0, self._max_frame)
        self._set_slider_value(0, self._max_frame)

        self._old_z_min = self._ui.sl_range.low()
        self._old_z_max = self._ui.sl_range.high()

        self._cut_selector.set_integration(self._my_id)

    # ----------------------------------------------------------------------
    def _update_from_frame_slider(self, value):
        """
        Set value of range slider and spin_boxes
        """
        self._set_spin_boxes(value, value)
        self._set_slider_value(value, value)
        self._new_cut()

    # ----------------------------------------------------------------------
    def _update_from_range_slider(self, z_min, z_max):
        """
        Set value of range slider and spin_boxes
        """
        z_min, z_max = self._apply_range_limit(z_min, z_max)
        self._set_spin_boxes(z_min, z_max)
        self._set_slider_value(z_min, z_max)
        self._new_cut()

    # ----------------------------------------------------------------------
    def _update_from_navigation_buttons(self, mode):
        """
        Process button_clink on navigation buttons
        """
        z_min = self._ui.sl_range.low()
        z_max = self._ui.sl_range.high()

        new_min = z_min
        new_max = z_max

        if mode == 'first':
            new_min = 0
        elif mode == 'previous':
            new_min -= 1
            new_max -= 1
        elif mode == 'next':
            new_min += 1
            new_max += 1
        elif mode == 'last':
            new_max = self._max_frame
            if z_min == z_max:
                new_min = self._max_frame

        new_max = min(max(0, new_max), self._max_frame)
        new_min = min(max(0, new_min), self._max_frame)
        new_min, new_max = self._apply_range_limit(new_min, new_max)

        self._set_spin_boxes(new_min, new_max)
        self._set_slider_value(new_min, new_max)
        self._new_cut()

    # ----------------------------------------------------------------------
    def _update_from_sp(self):
        """
        Set values to slider given in the SpinBox.
        """
        z_min = self._value_to_frame(self._ui.sp_value_from.value())
        z_max = self._value_to_frame(self._ui.sp_value_to.value())
        z_min, z_max = self._apply_range_limit(z_min, z_max)

        if z_min != self._old_z_min or z_max != self._old_z_max:
            self._set_slider_value(z_min, z_max)
            self._set_spin_boxes(z_min, z_max)
            self._new_cut()

    # ----------------------------------------------------------------------
    def _set_slider_value(self, z_min, z_max):
        """
        Set values to slider.
        """
        self.blockSignals(True)
        self._ui.sl_frame.setValue(z_min)
        self._ui.sl_range.setLow(z_min)
        self._ui.sl_range.setHigh(z_max)
        self.blockSignals(False)

    # ----------------------------------------------------------------------
    def units_changed(self):
        self.blockSignals(True)

        decimals = self._data_pool.get_axis_resolution(self._frame_viewer.current_file(), self._my_id)

        self._ui.sp_value_from.setDecimals(decimals)
        self._ui.sp_value_from.setSingleStep(np.power(10., -decimals))
        self._ui.sp_value_to.setDecimals(decimals)
        self._ui.sp_value_to.setSingleStep(np.power(10., -decimals))

        self._ui.sp_step.setDecimals(decimals)
        self._ui.sp_step.setSingleStep(np.power(10., -decimals))
        self._ui.sp_step.setValue(np.power(10., -decimals))

        self._ui.sl_range.setSingleStep(np.power(10., -decimals))
        self._ui.sl_frame.setSingleStep(np.power(10., -decimals))

        self._ui.sp_value_to.setMinimum(self._frame_to_value(0))
        self._ui.sp_value_to.setMaximum(self._frame_to_value(self._ui.sl_range.maximum()))

        self._ui.sp_value_from.setMinimum(self._frame_to_value(0))
        self._ui.sp_value_from.setMaximum(self._frame_to_value(self._ui.sl_range.maximum()))

        self._ui.sp_value_from.setValue(self._frame_to_value(self._ui.sl_range.low()))
        self._ui.sp_value_to.setValue(self._frame_to_value(self._ui.sl_range.high()))

        self.blockSignals(False)

    # ----------------------------------------------------------------------
    def _frame_to_value(self, frame):
        return self._data_pool.get_value_for_frame(self._frame_viewer.current_file(), self._my_id, frame)

    # ----------------------------------------------------------------------
    def _value_to_frame(self, frame):
        return self._data_pool.get_frame_for_value(self._frame_viewer.current_file(), self._my_id, frame)

    # ----------------------------------------------------------------------
    def _set_spin_boxes(self, z_min, z_max):
        """
        Set value of spin_boxes sp_value_from, sp_value_to and sp_step
        """
        self.blockSignals(True)

        z_min = self._frame_to_value(z_min)
        z_max = self._frame_to_value(z_max)

        self._ui.sp_value_from.setValue(z_min)
        self._ui.sp_value_to.setValue(z_max)

        self.blockSignals(False)

    # ----------------------------------------------------------------------
    def _apply_range_limit(self, z_min, z_max):
        z_min = max(0, min(z_min, z_max))
        if 0 < self.limit_range - 1 < (z_max - z_min):
            z_max = self.limit_range + z_min - 1
        return z_min, z_max

    # ----------------------------------------------------------------------
    def setup_limits(self, max_frame):
        """
        Set limits to sliders and spin_boxes
        """
        self.blockSignals(True)
        logger.debug(f"Setup_limits of {max_frame} for {self._my_id}")

        self._ui.sl_frame.setMaximum(max_frame)
        self._ui.sl_range.setMaximum(max_frame)
        self._ui.sl_range.setMinimum(0)

        self._ui.sp_value_to.setMinimum(self._frame_to_value(0))
        self._ui.sp_value_to.setMaximum(self._frame_to_value(max_frame))

        self._ui.sp_value_from.setMinimum(self._frame_to_value(0))
        self._ui.sp_value_from.setMaximum(self._frame_to_value(max_frame))

        self._max_frame = max_frame

        self.blockSignals(False)

    # ----------------------------------------------------------------------
    def set_section(self, section):

        decimals = self._data_pool.get_axis_resolution(self._frame_viewer.current_file(), self._my_id)

        self._ui.sp_value_from.setDecimals(decimals)
        self._ui.sp_value_to.setDecimals(decimals)
        self._ui.sp_step.setDecimals(decimals)

        self._ui.sp_step.setMinimum(np.power(10., -decimals))

        if section['axis'] in ['X', 'Y']:
            self.switch_integration_mode(True)
        else:
            self.switch_integration_mode(section['integration'])

        self.limit_range = section['range_limit']
        self._ui.sp_step.setValue(section['step'])
        self._set_slider_value(section['min'], section['max'])
        self._set_spin_boxes(section['min'], section['max'])
        self._old_z_min = section['min']
        self._old_z_max = section['max']

    # ----------------------------------------------------------------------
    def get_values(self):
        return int(self._ui.sl_range.low()), int(self._ui.sl_range.high())

    # ----------------------------------------------------------------------
    def blockSignals(self, flag):
        self._ui.sl_frame.blockSignals(flag)
        self._ui.sl_range.blockSignals(flag)
        self._ui.sp_step.blockSignals(flag)
        self._ui.sp_value_from.blockSignals(flag)
        self._ui.sp_value_to.blockSignals(flag)
