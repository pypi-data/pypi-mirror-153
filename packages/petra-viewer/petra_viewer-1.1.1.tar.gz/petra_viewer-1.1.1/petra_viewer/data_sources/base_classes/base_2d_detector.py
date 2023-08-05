# Created by matveyev at 20.05.2021

"""
Base class for images, obtained by 2D detectors
provide general functionality:

1) applying pixel mask to individual frame
2) excluding pixels based on flat filed detector map
3) filling detector gaps with interpolation of neighbor pixels
4) correction of intensity individual frame

"""

import numpy as np
import logging
from scipy import ndimage

from petra_viewer.main_window import APP_NAME
from petra_viewer.utils.utils import read_mask_file, read_ff_file
from petra_viewer.data_sources.base_classes.base_data_set import BaseDataSet

logger = logging.getLogger(APP_NAME)


# ----------------------------------------------------------------------
def apply_base_settings(settings, SETTINGS):

    SETTINGS['enable_fill'] = False
    SETTINGS['fill_radius'] = False
    if 'fill_radius' in settings:
        try:
            SETTINGS['fill_radius'] = float(settings['fill_radius'])
            SETTINGS['enable_fill'] = True
        except:
            pass

    for param, default in zip(['min_ff', 'max_ff'], [0, 100]):
        SETTINGS[param] = default
        if param in settings:
            try:
                SETTINGS[param] = float(settings[param])
            except:
                pass

    for mode, funct in zip(['mask', 'ff'], [read_mask_file, read_ff_file]):
        SETTINGS[f'enable_{mode}'] = False
        SETTINGS[f'{mode}'] = None
        SETTINGS[f'{mode}_file'] = ''

        if f'{mode}' in settings:
            data = funct(settings[f'{mode}'])
            if data is not None:
                SETTINGS[f'enable_{mode}'] = True
                SETTINGS[f'{mode}'] = data
                SETTINGS[f'{mode}_file'] = settings[f'{mode}']


# ----------------------------------------------------------------------
class Base2DDetectorDataSet(BaseDataSet):
    
    def __init__(self, data_pool):
        super(Base2DDetectorDataSet, self).__init__(data_pool)
        
        self._need_apply_mask = True

    # ----------------------------------------------------------------------
    def _get_settings(self):
        raise RuntimeError('Non implemented')

    # ----------------------------------------------------------------------
    def _reload_data(self, frame_ids=None):
        raise RuntimeError('Non implemented')

    # ----------------------------------------------------------------------
    def _get_data_shape(self):
        raise RuntimeError('Non implemented')

    # ----------------------------------------------------------------------
    def _calculate_correction(self, data_shape, frame_ids):
        """
        some files can require correction for individual frames (e.g. for incoming beam intensity)

        :param data_shape: 3D data cube shape
        :param frame_ids: if not None: frame ids for which correction has to be calculated
        :return: np.array if correction factors
        """
        self._correction = np.ones(data_shape[0], dtype=np.float32)

    # ----------------------------------------------------------------------
    def _get_data(self, frame_id=None):
        """
        Get nD array of data with applied activated parameters
        :param frame_id: tuple, select requested frames_id
        :return: np.array
        """

        logger.debug(f"Request data with frame_id={frame_id}, mode={self._data_pool.memory_mode}")
        frame_id = np.arange(*frame_id) if frame_id is not None else None

        if self._data_pool.memory_mode != 'ram':
            self._nD_data_array = None
            _data = self._reload_data(frame_id)
            self.apply_corrections(_data, frame_id)

            if frame_id is not None:
                return _data[frame_id]
            return _data

        if self._need_apply_mask:
            self._nD_data_array = self._reload_data()
            self.apply_corrections(self._nD_data_array)
            self._need_apply_mask = False

        if frame_id is not None:
            return self._nD_data_array[frame_id]

        return self._nD_data_array

    # ----------------------------------------------------------------------
    def apply_corrections(self, data, frame_id=None):
        """
        Apply several corrections to the data value.
        """
        logger.debug(f"Applying correction for {self.my_name}")

        _settings = self._get_settings()

        _pixel_mask = None
        _fill_weights = None

        # here we calculate pixel mask for selected set of options
        if _settings['enable_mask'] and _settings['mask'] is not None:
            _pixel_mask = _settings['mask'] > 0

        if _settings['enable_ff'] and _settings['ff'] is not None:
            _ff = np.copy(_settings['ff'])
            if _pixel_mask is None:
                _pixel_mask = (_ff < _settings['ff_min']) + (_ff > _settings['ff_max'])
            else:
                _pixel_mask += (_ff < _settings['ff_min']) + (_ff > _settings['ff_max'])

        # here we calculate pixel mask gap filling
        if _settings['enable_fill']:
            _fill_weights = ndimage.uniform_filter(1.-_pixel_mask, size=_settings['fill_radius'])

        self._calculate_correction(data.shape, frame_id)

        try:
            if _pixel_mask is not None:
                for frame in data:
                    frame[_pixel_mask] = 0

            if _settings['enable_ff'] and _settings['ff'] is not None:
                for ind in range(data.shape[0]):
                    data[ind] = data[ind]/_settings['ff']

            if _settings['enable_fill']:
                for ind in range(data.shape[0]):
                    frame_f = ndimage.uniform_filter(data[ind], size=_settings['fill_radius'])
                    if _pixel_mask is not None:
                        data[ind][_pixel_mask] = (frame_f/_fill_weights)[_pixel_mask]
                    else:
                        data[ind] = (frame_f/_fill_weights)

            for frame, corr in zip(data, self._correction):
                    frame *= corr

        except Exception as err:
            raise RuntimeError("{}: cannot apply mask: {}".format(self.my_name, err))

    # ----------------------------------------------------------------------
    def _cut_data(self, section, output_dim):
        """
        return cut from data
        :param data: nD np.array
        :param section: array of tuples to define section: (axis, from, to)
        :return:
        """
        section_sorted = sorted(section)

        if self._data_pool.memory_mode != 'ram':
            data = self._get_data((section_sorted[0][1], section_sorted[0][2]))
        else:
            data = self._get_data()

        logger.debug(f"Data before cut {data.shape}, selection={section}, output_dim: {output_dim}")

        for axis_slice in section[output_dim:]:
            axis, start, stop = axis_slice
            start = max(start, 0)
            stop = min(stop, data.shape[axis])
            if axis > 0 or self._data_pool.memory_mode == 'ram':
                data = np.mean(data.take(indices=range(start, stop), axis=axis), axis=axis, keepdims=True)
            else:
                data = np.mean(axis=axis, keepdims=True)

        for axis_slice in section[:output_dim]:
            axis, start, stop = axis_slice
            if axis > 0 or self._data_pool.memory_mode == 'ram':
                start = max(start, 0)
                stop = min(stop, data.shape[axis])
                if axis > 0 or self._data_pool.memory_mode == 'ram':
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
    def _corrections_required(self):
        """
        Check if any correction foreseen for the data
        """
        settings = self._get_settings()
        if settings['enable_mask'] and settings['mask'] is not None:
            return True

        if settings['enable_ff'] and settings['ff'] is not None:
            return True

        # here we calculate pixel mask gap filling
        if settings['enable_fill']:
            return True

        return False

    # ----------------------------------------------------------------------
    def apply_settings(self):
        self._need_apply_mask = self._corrections_required()

        self._hist_lin = None
        self._hist_log = None
        self._hist_sqrt = None

        self._levels = None