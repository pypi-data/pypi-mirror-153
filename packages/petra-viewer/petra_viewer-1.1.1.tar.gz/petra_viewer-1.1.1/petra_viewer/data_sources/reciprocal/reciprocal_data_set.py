# Created by matveyev

import h5py

import numpy as np

from petra_viewer.data_sources.base_classes.base_data_set import BaseDataSet

SETTINGS = {
            }


class ReciprocalScan(BaseDataSet):

    # ----------------------------------------------------------------------
    def __init__(self, data_pool, file_name=None, opened_file=None, gridder=None):
        super(ReciprocalScan, self).__init__(data_pool)

        self._original_file = file_name

        if gridder is not None:
            self._nD_data_array = np.copy(gridder.data)
            self._data_shape = self._nD_data_array.shape
            self._possible_axes_units = [{'Qx': np.copy(gridder.xaxis)},
                                         {'Qy': np.copy(gridder.yaxis)},
                                         {'Qz': np.copy(gridder.zaxis)}]

        elif opened_file is not None:
            if self._data_pool.memory_mode == 'ram':
                self._nD_data_array = self._get_data()
                self._data_shape = self._nD_data_array.shape
            else:
                self._data_shape = self._get_data_shape()

        self._axes_units = ['Qx', 'Qy', 'Qz']
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
        source_file = h5py.File(self._original_file, 'r')
        self._possible_axes_units = [{'Qx': np.copy(source_file['reciprocal_scan']['x_axis'])},
                                     {'Qy': np.copy(source_file['reciprocal_scan']['y_axis'])},
                                     {'Qz': np.copy(source_file['reciprocal_scan']['z_axis'])}]
        return np.array(source_file['reciprocal_scan']['3d_cube'], dtype=np.float32)

    # ----------------------------------------------------------------------
    def _get_data_shape(self):
        source_file = h5py.File(self._original_file, 'r')
        self._possible_axes_units = [{'Qx': np.copy(source_file['reciprocal_scan']['x_axis'])},
                                     {'Qy': np.copy(source_file['reciprocal_scan']['y_axis'])},
                                     {'Qz': np.copy(source_file['reciprocal_scan']['z_axis'])}]
        return len(source_file['reciprocal_scan']['x_axis']), len(source_file['reciprocal_scan']['y_axis']), \
               len(source_file['reciprocal_scan']['z_axis'])
    
    # ----------------------------------------------------------------------
    def save_file(self, file_name):

        with h5py.File(file_name, 'w') as hf:
            group = hf.create_group('reciprocal_scan')
            group.create_dataset('x_axis', data=self._possible_axes_units[0]['Qx'])
            group.create_dataset('y_axis', data=self._possible_axes_units[1]['Qy'])
            group.create_dataset('z_axis', data=self._possible_axes_units[2]['Qz'])
            group.create_dataset('3d_cube', data=self._nD_data_array)
