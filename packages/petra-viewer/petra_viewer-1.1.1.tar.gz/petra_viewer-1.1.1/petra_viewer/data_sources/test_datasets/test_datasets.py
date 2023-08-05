# Created by matveyev at 09.11.2021

import numpy as np
import configparser

from petra_viewer.data_sources.sardana.sardana_data_set import SardanaDataSet
from petra_viewer.data_sources.asapo.asapo_data_set import ASAPODataSet
from petra_viewer.data_sources.beamview.beamview_data_set import BeamLineView

__all__ = ['SardanaPeak1', 'SardanaPeak2', 'HeavySardana', 'ASAPO2DPeak', 'ASAPO3DPeak', 'ASAPO4DPeak', 'BeamView']


class BaseTestDataSet(object):

    dims = []

    my_name = ''

    max_int = None

    # ----------------------------------------------------------------------
    def get_info(self):
        return self.my_name, f'{len(self.dims)}D', 'x'.join([str(dim) for dim in self.dims])


# --------------------------------------------------------------------
class __Fake3DSardana(SardanaDataSet, BaseTestDataSet):

    # ----------------------------------------------------------------------
    def __init__(self, data_pool):

        super(SardanaDataSet, self).__init__(data_pool)

        self._possible_axes_units = [{'point_nb': np.arange(self.dims[0])},
                                     {'detector X': np.arange(self.dims[1])},
                                     {'detector Y': np.arange(self.dims[2])}]

        self._axes_units = ['point_nb', 'detector X', 'detector Y']
        self._axis_units_is_valid = [True, True, True]

        if self._data_pool.memory_mode == 'ram':
            self._nD_data_array = self._get_data()
            self._data_shape = self._nD_data_array.shape
        else:
            self._data_shape = self._get_data_shape()

    # ----------------------------------------------------------------------
    def _set_default_section(self):
        self._section = ({'axis': 'Z', 'integration': False, 'min': 0, 'max': self._data_shape[0] - 1, 'step': 1,
                          'range_limit': self._data_shape[0]},
                         {'axis': 'X', 'integration': False, 'min': 0, 'max': self._data_shape[1] - 1, 'step': 1,
                          'range_limit': self._data_shape[1]},
                         {'axis': 'Y', 'integration': False, 'min': 0, 'max': self._data_shape[2] - 1, 'step': 1,
                          'range_limit': self._data_shape[2]})

    # ----------------------------------------------------------------------
    def _generate_fake_data(self):

        y, x = np.meshgrid(np.linspace(-self.dims[2]/2, self.dims[2]/2, self.dims[2]),
                           np.linspace(-self.dims[1]/2, self.dims[1]/2, self.dims[1]))

        mean, sigma = 1, 4
        frame = np.exp(-((np.sqrt(x * x + y * y * 4) - mean) ** 2 / (2.0 * sigma ** 2))) * self.max_int

        data_cube = np.zeros(self.dims)
        for ind, scale in enumerate(np.power(np.sin(np.linspace(0, np.pi, self.dims[0])), 4)):
            data_cube[ind] = frame * scale

        data_cube -= np.min(data_cube) - 1

        return data_cube

    # ----------------------------------------------------------------------
    def _reload_data(self, frame_ids=None):
        if frame_ids is None:
            return self._generate_fake_data()
        else:
            return self._generate_fake_data()[frame_ids]

    # ----------------------------------------------------------------------
    def _get_data_shape(self):

        return self.dims


# ----------------------------------------------------------------------
class SardanaPeak1(__Fake3DSardana):

    dims = [11, 101, 201]

    my_name = 'SardanaPeak1'

    max_int = 50

    # ----------------------------------------------------------------------
    def __init__(self, data_pool):

        super(SardanaPeak1, self).__init__(data_pool)

        self._possible_axes_units[0]['omega'] = np.linspace(1, 2, self.dims[0])
        self._possible_axes_units[0]['delta'] = np.linspace(2, 4, self.dims[0])


# ----------------------------------------------------------------------
class SardanaPeak2(__Fake3DSardana):

    dims = [21, 151, 101]

    my_name = 'SardanaPeak2'

    max_int = 150

    # ----------------------------------------------------------------------
    def __init__(self, data_pool):
        super(SardanaPeak2, self).__init__(data_pool)

        self._possible_axes_units[0]['omega'] = np.linspace(1.5, 2.5, self.dims[0])


# ----------------------------------------------------------------------
class HeavySardana(__Fake3DSardana):

    dims = [501, 1556, 516]

    my_name = 'HeavySardana'

    max_int = 1e6

    # ----------------------------------------------------------------------
    def __init__(self, data_pool):
        super(HeavySardana, self).__init__(data_pool)

        self._possible_axes_units[0]['omega'] = np.linspace(1.5, 2.5, self.dims[0])


# --------------------------------------------------------------------
class __FakeNDASAPO(ASAPODataSet, BaseTestDataSet):

    # ----------------------------------------------------------------------
    def __init__(self, data_pool):

        super(ASAPODataSet, self).__init__(data_pool)

        if self._data_pool.memory_mode == 'ram':
            self._nD_data_array = self._get_data()
            self._data_shape = list(self._nD_data_array.shape)
        else:
            self._data_shape = self._get_data_shape()

        axes_names = ['message_ID'] + [f'dim_{i}' for i in range(1, len(self._data_shape))]

        self._possible_axes_units = [{name: np.arange(axis_len)} for name, axis_len in zip(axes_names, self._data_shape)]
        self._axes_units = axes_names
        self._axis_units_is_valid = [True for _ in axes_names]


        self._additional_data['metadata'] = [{'_id': ind, 'data_source': self.my_name}
                                             for ind in range(self._data_shape[0])]

        self._additional_data['already_loaded_ids'] = list(range(self._data_shape[0]))

        self._additional_data['frame_ID'] = np.arange(self._data_shape[0])

    # ----------------------------------------------------------------------
    def _set_default_section(self):
        self._section = []
        axis = ['' for _ in range(len(self._data_shape))]
        axis[-1] = 'X'
        if len(axis) > 1:
            axis[-2] = 'Y'
        if len(axis) > 2:
            axis[-3] = 'Z'

        for i, axis in enumerate(axis):
            if i == 0:
                range_limit = 0
            self._section.append({'axis': axis, 'integration': False, 'min': 0, 'max': self._data_shape[i] - 1,
                                  'step': 1, 'range_limit': range_limit})

    # ----------------------------------------------------------------------
    def _generate_fake_data(self):

        def _get_frame():
            y, x = np.meshgrid(np.linspace(-self.dims[-1] / 2, self.dims[-1] / 2, self.dims[-1]),
                               np.linspace(-self.dims[-2] / 2, self.dims[-2] / 2, self.dims[-2]))

            mean, sigma = 1, 4
            return np.exp(-((np.sqrt(x * x + y * y * 4) - mean) ** 2 / (2.0 * sigma ** 2))) * 100

        def _fill_axis(data, rest_axes):
            if len(rest_axes):
                for ind, scale in enumerate(np.power(np.sin(np.linspace(0, np.pi, self.dims[rest_axes[0]])), 4)):
                    data[ind] = _fill_axis(data[ind], rest_axes[1:]) * scale
            else:
                data = _get_frame()

            return data

        data_cube = _fill_axis(np.zeros(self.dims), list(range(len(self.dims[:-2]))))

        data_cube -= np.min(data_cube) - 1

        return data_cube

    # ----------------------------------------------------------------------
    def _reload_data(self, frame_ids=None):
        if frame_ids is None:
            return self._generate_fake_data()
        else:
            return self._generate_fake_data()[frame_ids]

    # ----------------------------------------------------------------------
    def _get_data_shape(self):

        return self.dims


# ----------------------------------------------------------------------
class ASAPO2DPeak(__FakeNDASAPO):

    dims = [101, 151]

    my_name = 'ASAPO2DPeak'


# ----------------------------------------------------------------------
class ASAPO3DPeak(__FakeNDASAPO):

    dims = [21, 101, 151]

    my_name = 'ASAPO3DPeak'


# ----------------------------------------------------------------------
class ASAPO4DPeak(__FakeNDASAPO):

    dims = [5, 21, 101, 151]

    my_name = 'ASAPO4DPeak'


# --------------------------------------------------------------------
class BeamView(BeamLineView, BaseTestDataSet):

    my_name = 'BeamView'

    dims = [101, 101, 15]

    # ----------------------------------------------------------------------
    def _get_data(self):

        x, y = np.meshgrid(np.linspace(-self.dims[0]/2, self.dims[0]/2, self.dims[0]),
                           np.linspace(-self.dims[1]/2, self.dims[1]/2, self.dims[1]))

        mean, sigma = 2, 6
        frame = np.exp(-((np.sqrt(x * x + y * y * 4) - mean) ** 2 / (2.0 * sigma ** 2)))*100

        data_cube = np.zeros(self.dims)
        for ind, scale in enumerate(np.power(np.sin(np.linspace(0, np.pi, self.dims[2])), 4)):
            data_cube[..., ind] = frame * scale

        data_cube -= np.min(data_cube)

        self._additional_data['X'] = np.linspace(-self.dims[0]/2, self.dims[0]/2, self.dims[0])
        self._additional_data['Y'] = np.linspace(-self.dims[1]/2, self.dims[1]/2, self.dims[0])
        self._additional_data['Z'] = np.arange(0, self.dims[2]) * 3

        return data_cube

    # ----------------------------------------------------------------------
    def _get_data_shape(self):

        return self.dims

