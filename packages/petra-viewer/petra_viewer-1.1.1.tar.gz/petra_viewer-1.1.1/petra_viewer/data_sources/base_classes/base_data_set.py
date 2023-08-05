# Created by matveyev at 18.02.2021

"""
General class for opened file/stream
"""

import numpy as np
import logging

from PyQt5 import QtCore

from petra_viewer.main_window import APP_NAME

logger = logging.getLogger(APP_NAME)


class BaseDataSet(object):

    # ----------------------------------------------------------------------
    def __init__(self, data_pool):

        self.my_name = ''
        self._data_pool = data_pool
        self._additional_data = {}

        self._axes_units = []
        self._axis_units_is_valid = []

        self._possible_axes_units = []  # [{unit_name: [unit values]} or None]
        # this is main array, which stores data
        self._nD_data_array = np.array([])
        # user can select mode, where data are not kept in memory. We need to have at least information about data shape
        self._data_shape = []

        # here we keep some auxiliary data: scanned motors, etc
        self._additional_data = {}

        self._hist_lin = None
        self._hist_log = None
        self._hist_sqrt = None

        self._levels = None

        self._section = None

    # ----------------------------------------------------------------------
    def _set_default_section(self):
        self._section = None

    # ----------------------------------------------------------------------
    def save_section(self, section):
        if self._section is None:
            self._set_default_section()

        for old, new in zip(self._section, section):
            old.update(new)

    # ----------------------------------------------------------------------
    def get_section(self):
        if self._section is None:
            self._set_default_section()

        return self._section

    # ----------------------------------------------------------------------
    def _get_data(self):
        return self._nD_data_array

    # ----------------------------------------------------------------------
    def apply_settings(self):
        pass

    # ----------------------------------------------------------------------
    def get_file_axes(self):
        """
        some files can have own axes captions
        :param file:
        :return: dict {axis_index: axis_name}
        """
        return self._axes_units

    # ----------------------------------------------------------------------
    def get_file_dimension(self):
        """
        return nD cube dimensions
        :param file:
        :return: int
        """
        return len(self._data_shape)

    # ----------------------------------------------------------------------
    def get_additional_data(self, entry):
        """
        for some file types we can store additional information
        :param file:
        :param entry:
        :return: if file has requested entry - returns it, else None
        """
        if entry in self._additional_data:
            return self._additional_data[entry]
        else:
            return None

    # ----------------------------------------------------------------------
    def get_axis_limits(self):
        """

        :return: list [max, ], limits for each axis
        """

        return [lim-1 for lim in self._data_shape]

    # ----------------------------------------------------------------------
    def get_axis_resolution(self, axis):
        """

        :return: int, decimals for particular axis
        """
        axis_values = self._get_axis(axis)
        min_shift = np.min(np.diff(axis_values))
        power = 0
        while np.power(10., -power) > min_shift:
            power += 1
        return power

    # ----------------------------------------------------------------------
    def get_possible_axis_units(self, axis):
        """

        :return: list, possible units for particular axis
        """
        return self._possible_axes_units[axis]

    # ----------------------------------------------------------------------
    def set_axis_units(self, axis, units):
        """

        :param: axis, particular axis
        :param: units, user selected units
        """
        if units in self._possible_axes_units[axis]:
            self._axes_units[axis] = units
            self._axis_units_is_valid[axis] = True
        else:
            self._axis_units_is_valid[axis] = False

    # ----------------------------------------------------------------------
    def get_axis_units(self, axis):
        """

        :return: str, selected units for particular axis
        """
        return self._axes_units[axis]

    # ----------------------------------------------------------------------
    def are_axes_valid(self):
        """

        :return: bool, are file compatible with current selection of axes
        """
        return np.all(self._axis_units_is_valid)

    # ----------------------------------------------------------------------
    def get_frame_for_value(self, axis, pos, check_range):
        """
        for some file types user can select the displayed unit for some axis
        e.g. for Sardana scan we can display point_nb, or motor position etc...

        here we return the frame number along this axis for particular unit value

        :param axis: axis index
        :param pos: unit value
        :param check_range: bool, if True - returns value only if pos within axis range, else None
        :return: frame index
        """

        axis_value = self._get_axis(axis)

        if check_range:
            if not np.min(axis_value) - np.diff(axis_value)[0] < pos < np.max(axis_value) + np.diff(axis_value)[-1]:
                return None

        return np.argmin(np.abs(axis_value-pos))

    # ----------------------------------------------------------------------
    def get_value_for_frame(self, axis, pos):
        """
        for some file types user can select the displayed unit for some axis
        e.g. for Sardana scan we can display point_nb, or motor position etc...

        here we return the unit value along this axis for particular frame number

        :param axis: axis index
        :param pos: frame index
        :return: unit value
        """

        return self._possible_axes_units[axis][self._axes_units[axis]][pos]

    # ----------------------------------------------------------------------
    def get_max_frame_along_axis(self, axis):
        """

        :param axis:
        :return: maximum index along axis
        """
        return self._data_shape[axis] - 1

    # ----------------------------------------------------------------------
    def get_metadata(self):

        return None

    # ----------------------------------------------------------------------
    def get_roi_plot(self, sect):
        """

        :param sect: ROI parameters
        :return: X and Y of ROI plot
        """
        logger.debug(f"{self.my_name}: Request roi plot with section {sect}")
        return self._get_axis(sect['axis_0']), self.get_roi_cut(sect, True)

    # ----------------------------------------------------------------------
    def recalculate_value(self, axis, value, new_units):
        if new_units in self._possible_axes_units[axis]:
            frame = self.get_frame_for_value(axis, value, False)
            return self._possible_axes_units[axis][new_units][frame]
        else:
            return value

    # ----------------------------------------------------------------------
    def get_roi_cut(self, sect, do_sum=False):
        """
        returns ROI cut from data cube
        :param sect: ROI parameters
        :param do_sum: if True - return 1D plot, in False - return 3D cut
        :return: np.arrays: X and
        """

        if len(self._data_shape) != sect['dimensions']:
            return 0, 0

        slices = [(sect['axis_0'], 0, self._data_shape[sect['axis_0']])] # [(axis, from, to), etc]
        for axis in range(1, len(self._data_shape)):
            a_min = self.get_frame_for_value(sect[f'axis_{axis}'], sect[f'axis_{axis}_pos'], False)
            a_max = self.get_frame_for_value(sect[f'axis_{axis}'], sect[f'axis_{axis}_pos'] + sect[f'axis_{axis}_width'], False)
            slices.append((sect[f'axis_{axis}'], a_min, a_max))

        return self._cut_data(slices, 1 if do_sum else 3)

    # ----------------------------------------------------------------------
    def get_2d_picture(self):
        """

        returns 2D frame to be displayed in Frame viewer
        :return: 2D np.array

        """

        logger.debug(f"{self.my_name}: Request 2D picture")
        rest_axes = list(range(len(self._data_shape)))

        section = self.get_section()

        x_axis_ind = [ind for ind, sect in enumerate(section) if sect['axis'] == 'X'][0]
        x_min = section[x_axis_ind]['min']
        x_max = section[x_axis_ind]['max']
        cut_params = [(x_axis_ind, x_min, x_max + 1)]
        rest_axes.remove(x_axis_ind)

        y_axis_ind = [ind for ind, sect in enumerate(section) if sect['axis'] == 'Y'][0]
        y_min = section[y_axis_ind]['min']
        y_max = section[y_axis_ind]['max']
        cut_params.append((y_axis_ind, y_min, y_max + 1))
        rest_axes.remove(y_axis_ind)

        for axis in rest_axes:
            if section[axis]['min'] > self.get_max_frame_along_axis(axis):
                return None

            if section[axis]['integration']:
                if section[axis]['max'] > self.get_max_frame_along_axis(axis):
                    return None

                cut_params.append((axis, section[axis]['min'], section[axis]['max'] + 1))
            else:
                cut_params.append((axis, section[axis]['min'], section[axis]['min'] + 1))

        x_min = self.get_value_for_frame(x_axis_ind, x_min)
        x_max = self.get_value_for_frame(x_axis_ind, x_max)
        y_min = self.get_value_for_frame(y_axis_ind, y_min)
        y_max = self.get_value_for_frame(y_axis_ind, y_max)

        return self._cut_data(cut_params, 2), QtCore.QRectF(x_min, y_min, x_max - x_min, y_max-y_min)

    # ----------------------------------------------------------------------
    def _cut_data(self, section, output_dim):
        """
        return cut from data
        :param data: nD np.array
        :param section: array of tuples to define section: (axis, from, to)
        :return:
        """

        data = self._get_data()

        logger.debug(f"Data before cut {data.shape}, selection={section}, output_dim: {output_dim}")

        for axis_slice in section[output_dim:]:
            axis, start, stop = axis_slice
            start = max(start, 0)
            stop = min(stop, data.shape[axis])
            data = np.mean(data.take(indices=range(start, stop), axis=axis), axis=axis, keepdims=True)

        for axis_slice in section[:output_dim]:
            axis, start, stop = axis_slice
            if axis > 0 or self._data_pool.memory_mode == 'ram':
                start = max(start, 0)
                stop = min(stop, data.shape[axis])
                data = data.take(indices=range(start, stop), axis=axis)

        if np.ndim(data) == 0:
            data = np.zeros(5)[:, None]
        if np.ndim(data) == 1 and output_dim == 2:
            data = data[:, None]

        axes_order = list(range(len(data.shape)))
        for ind, (axis, _, _) in enumerate(section):
            move_from = axes_order.index(axis)
            if move_from != ind:
                data = np.moveaxis(data, move_from, ind)
                del axes_order[move_from]
                axes_order.insert(ind, axis)

        data = np.squeeze(data)

        logger.debug(f"Data after cut {data.shape} ")
        return data
    # ----------------------------------------------------------------------
    def _get_axis(self, plot_axis):
        """

        :param plot_axis: axis index
        :return: np.array of X coordinate for ROI plot
        """
        return self._possible_axes_units[plot_axis][self._axes_units[plot_axis]]

    # ----------------------------------------------------------------------
    def get_3d_cube(self, roi_params):

        logger.debug(f"{self.my_name}: Request 3D picture")

        n_dims = len(self._data_shape)
        rest_axes = list(range(n_dims))

        if roi_params is None:
            lims = [[0, size] for size in self._data_shape]
        else:
            lims = [[0, size] for size in self._data_shape]
            for axis in rest_axes[1:]:
                lims[roi_params[f'axis_{axis}']] = [roi_params[f'axis_{axis}_pos'],
                                                    roi_params[f'axis_{axis}_pos'] + roi_params[f'axis_{axis}_width']]

        section = self.get_section()

        x_axis_ind = [ind for ind, sect in enumerate(section) if sect['axis'] == 'X'][0]
        cut_params = [(x_axis_ind, lims[x_axis_ind][0], lims[x_axis_ind][1])]
        rest_axes.remove(x_axis_ind)
        axes_names = [self._axes_units[x_axis_ind]]

        if n_dims > 1:
            y_axis_ind = [ind for ind, sect in enumerate(section) if sect['axis'] == 'Y'][0]
            cut_params.append((y_axis_ind, lims[y_axis_ind][0], lims[y_axis_ind][1]))
            rest_axes.remove(y_axis_ind)
            axes_names.append(self._axes_units[y_axis_ind])

        if n_dims > 2:
            z_axis_ind = [ind for ind, sect in enumerate(section) if sect['axis'] == 'Z'][0]
            cut_params.append((z_axis_ind, lims[z_axis_ind][0], lims[z_axis_ind][1]))
            rest_axes.remove(z_axis_ind)
            axes_names.append(self._axes_units[z_axis_ind])

        for axis in rest_axes:
            if section[axis]['min'] > self.get_max_frame_along_axis(axis):
                return None

            if section[axis]['integration']:
                if section[axis]['max'] > self.get_max_frame_along_axis(axis):
                    return None

                cut_params.append((axis, section[axis]['min'], section[axis]['max'] + 1))
            else:
                cut_params.append((axis, section[axis]['min'], section[axis]['min'] + 1))

        return self._cut_data(cut_params, 3), axes_names

    # ----------------------------------------------------------------------
    def get_histogram(self, mode):

        logger.debug(f"{self.my_name}: Histogram request {self.my_name}")

        if self._hist_lin is None:
            self._hist_lin, self._hist_log, self._hist_sqrt, self._levels = self._calculate_hist()

        if mode == 'lin':
            return self._hist_lin
        elif mode == 'log':
            return self._hist_log
        elif mode == 'sqrt':
            return self._hist_sqrt
        else:
            raise RuntimeError('Unknown hist mode')

    # ----------------------------------------------------------------------
    def get_levels(self, mode):

        logger.debug(f"{self.my_name}: Level request {self.my_name}")

        if self._levels is None:
            self._hist_lin, self._hist_log, self._hist_sqrt, self._levels = self._calculate_hist()

        if mode == 'lin':
            return self._levels
        elif mode == 'log':
            return np.log(self._levels + 1)
        elif mode == 'sqrt':
            return np.sqrt(self._levels + 1)
        else:
            raise RuntimeError('Unknown hist mode')

    # ----------------------------------------------------------------------
    def _calculate_hist(self, selection=None):

        logger.debug(f"{self.my_name}: Calculating histogram for {self.my_name}, selection: {selection}")

        original_data = self._get_data()

        hists = []

        for data in [original_data, np.log(original_data+1), np.sqrt(original_data+1)]:
            mn = np.nanmin(data).item()
            mx = np.nanmax(data).item()
            if mx == mn:
                # degenerate image, arange will fail
                mx += 1
            if np.isnan(mn) or np.isnan(mx):
                # the data are all-nan
                return None, None
            if data.dtype.kind in "ui":
                # For integer data, we select the bins carefully to avoid aliasing
                step = int(np.ceil((mx - mn) / 500.))
                bins = []
                if step > 0.0:
                    bins = np.arange(mn, mx + 1.01 * step, step, dtype=int)
            else:
                # for float data, let numpy select the bins.
                bins = np.linspace(mn, mx, 500)

            if len(bins) == 0:
                bins = np.asarray((mn, mx))

            data = data[np.isfinite(data)]
            hist = np.histogram(data, bins)

            hists.append((hist[1][:-1], hist[0]))

        return hists[0], hists[1], hists[2], np.array([np.min(original_data), np.max(original_data)])