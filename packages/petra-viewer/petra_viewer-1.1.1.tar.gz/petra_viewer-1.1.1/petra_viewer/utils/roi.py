# Created by matveyev at 22.02.2021
import numpy as np


class ROI(object):

    # ------------------------------------------------------------------
    def __init__(self, data_pool, my_id, dims, axis):

        self.my_id = my_id
        self._data_pool = data_pool

        self._section_params = {'dimensions': dims}

        self._fill_section(axis)

        self._saved_sections = {}

    # ------------------------------------------------------------------
    def set_section_axis(self, axis):

        self._saved_sections[self._section_params['axis_0']] = dict(self._section_params)
        if axis in self._saved_sections:
            self._section_params = dict(self._saved_sections[axis])
        else:
            self._fill_section(axis)

    # ------------------------------------------------------------------
    def roi_parameter_changed(self, axis, param, value, axes_limits):

        if axis == 0:
            if param == 'pos':
                return axes_limits[0]
            else:
                return axes_limits[1] - axes_limits[0]

        if param == 'pos':
            value = max(value, axes_limits[0])
            value = min(value, axes_limits[1] - self._section_params['axis_{}_width'.format(axis)])
        else:
            value = min(value, axes_limits[1] - self._section_params['axis_{}_pos'.format(axis)])

        self._section_params['axis_{}_{}'.format(axis, param)] = value
        return value

    # ------------------------------------------------------------------
    def get_section_params(self):
        return self._section_params

    # ------------------------------------------------------------------
    def get_param(self, param):
        if param in self._section_params:
            return self._section_params[param]
        else:
            return None

    # ------------------------------------------------------------------
    def _fill_section(self, section_axis):

        axes = list(np.arange(self._section_params['dimensions']))
        axes.remove(section_axis)

        self._section_params['axis_0'] = section_axis

        for ind, axis in enumerate(axes):
            self._section_params[f'axis_{ind+1}'] = axis
            self._section_params[f'axis_{ind+1}_pos'] = 0
            self._section_params[f'axis_{ind+1}_width'] = 1
