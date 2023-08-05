# Created by matveyev

import h5py
import os
import re
import numpy as np

from petra_viewer.data_sources.base_classes.base_data_set import BaseDataSet

SETTINGS = {
            }


class BeamLineView(BaseDataSet):

    # ----------------------------------------------------------------------
    def __init__(self, data_pool, file_name=None):
        super(BeamLineView, self).__init__(data_pool)

        self._file_name = file_name

        if self._data_pool.memory_mode == 'ram':
            self._nD_data_array = self._get_data()
            self._data_shape = self._nD_data_array.shape
        else:
            self._data_shape = self._get_data_shape()

        self._possible_axes_units = [{name: np.arange(axis_len)}
                                     for name, axis_len in zip(['X', 'Y', 'Z'], self._data_shape)]

        self._axes_units = ['X', 'Y', 'Z']
        self._axis_units_is_valid = [True, True, True]

    # ----------------------------------------------------------------------
    def _set_default_section(self):
        self._section = ({'axis': 'X', 'integration': False, 'min': 0, 'max': self._data_shape[0] - 1, 'step': 1,
                          'range_limit': self._data_shape[0] - 1},
                         {'axis': 'Y', 'integration': False, 'min': 0, 'max': self._data_shape[1] - 1, 'step': 1,
                          'range_limit': self._data_shape[1] - 1},
                         {'axis': 'Z', 'integration': False, 'min': 0, 'max': self._data_shape[2] - 1, 'step': 1,
                          'range_limit': self._data_shape[2] - 1})

    # ----------------------------------------------------------------------
    def _get_data(self):

        with h5py.File(self._file_name, 'r') as in_file:
            data = in_file['data_cube'][...]

            self._possible_axes_units[0] = {'X': in_file['x_axis'][...]}
            self._possible_axes_units[1] = {'Y': in_file['y_axis'][...]}
            self._possible_axes_units[2] = {'Z': in_file['z_axis'][...]}

        return data

    # ----------------------------------------------------------------------
    def _get_data_shape(self):
        with h5py.File(self._file_name, 'r') as in_file:
            return in_file['data_cube'].shape

