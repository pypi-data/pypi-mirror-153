# Created by matveyev at 18.02.2021

import h5py
import os

import numpy as np

from petra_viewer.utils.fio_reader import fioReader
from petra_viewer.data_sources.base_classes.base_2d_detector import Base2DDetectorDataSet, apply_base_settings

SETTINGS = {'door_address': None,
            'enable_mask': False,
            'mask': None,
            'mask_file': '',
            'enable_ff': False,
            'ff': None,
            'ff_file': '',
            'ff_min': 0,
            'ff_max': 100,
            'enable_fill': False,
            'fill_radius': 7,
            'atten_correction': True,
            'atten_param': 'atten',
            'inten_correction': True,
            'inten_param': 'eh_c01',
            'all_params': []
            }


# ----------------------------------------------------------------------
def apply_settings_sardana(settings):
    if 'door_address' in settings:
        SETTINGS['door_address'] = settings['door_address']
    else:
        SETTINGS['door_address'] = None

    for param, param2, default in zip(['atten_param', 'inten_param'],
                                      ['atten_correction', 'inten_correction'],
                                      ['atten', 'eh_c01']):
        if param in settings:
            SETTINGS[param] = settings[param]
            SETTINGS[param2] = True
        else:
            SETTINGS[param] = default
            SETTINGS[param2] = False

    apply_base_settings(settings, SETTINGS)


# ----------------------------------------------------------------------
class SardanaDataSet(Base2DDetectorDataSet):

    # ----------------------------------------------------------------------
    def __init__(self, data_pool, file_name):
        super(SardanaDataSet, self).__init__(data_pool)

        self.my_name = os.path.splitext(os.path.basename(file_name))[0]

        self._original_file = file_name

        self._possible_axes_units = [{}, {}, {}]

        # first we load scan data from .fio
        if os.path.isfile(os.path.splitext(file_name)[0] + '.fio'):
            fio_file = fioReader(os.path.splitext(file_name)[0] + '.fio')
            for key, value in fio_file.parameters.items():
                try:
                    self._additional_data[key] = float(value)
                except:
                    self._additional_data[key] = value

        self._scan_length = None

        opened_file = h5py.File(self._original_file, 'r')
        scan_data = opened_file['scan']['data']

        # if user did ct after scan, Lambda could save them as scan frames, we ignore them
        for key in scan_data.keys():

            # if this is 1D array - we add it to possible scan axes
            if key != 'lmbd' and len(scan_data[key].shape) == 1:
                if self._scan_length is None:
                    self._scan_length = len(scan_data[key][...])
                if len(scan_data[key][...]) == self._scan_length:
                    self._possible_axes_units[0][key] = np.array(scan_data[key][...])
                    if key not in SETTINGS['all_params']:
                        SETTINGS['all_params'].append(key)

        for key in scan_data.keys():
            # up to now only one type of scans - Lambda scans
            if key == 'lmbd':
                self._detector = 'lmbd'
                self._detector_folder = os.path.join(os.path.dirname(opened_file.filename),
                                                     os.path.splitext(os.path.basename(opened_file.filename))[0], 'lmbd')

                if self._data_pool.memory_mode == 'ram':
                    self._nD_data_array = self._get_data()
                    self._data_shape = self._nD_data_array.shape
                else:
                    self._data_shape = self._get_data_shape()

        self._possible_axes_units[0]['point_nb'] = np.arange(self._data_shape[0])
        self._possible_axes_units[1] = {'detector Y': np.arange(self._data_shape[1])}
        self._possible_axes_units[2] = {'detector X': np.arange(self._data_shape[2])}

        self._axes_units = ['point_nb', 'detector Y', 'detector X']
        self._axis_units_is_valid = [True, True, True]

    # ----------------------------------------------------------------------
    def _set_default_section(self):
        self._section = ({'axis': 'Z', 'integration': False, 'min': 0, 'max': self._data_shape[0] - 1, 'step': 1,
                          'range_limit': self._data_shape[0]},
                         {'axis': 'Y', 'integration': False, 'min': 0, 'max': self._data_shape[1] - 1, 'step': 1,
                          'range_limit': self._data_shape[1]},
                         {'axis': 'X', 'integration': False, 'min': 0, 'max': self._data_shape[2] - 1, 'step': 1,
                          'range_limit': self._data_shape[2]})

    # ----------------------------------------------------------------------
    def _get_settings(self):
        return SETTINGS

    # ----------------------------------------------------------------------
    def get_metadata(self):

        return self._additional_data

    # ----------------------------------------------------------------------
    def _reload_data(self, frame_ids=None):
        """
        reloads sardana data
        :param frame_ids: if not None: frames to be loaded
        :return: np.array, 3D data cube
        """

        file_lists = [f for f in os.listdir(self._detector_folder) if f.endswith('.nxs')]
        file_lists.sort()

        if len(file_lists) > 0:
            if frame_ids is not None:
                _need_cut = False
                if len(file_lists) > 1:
                    _select_frames = False
                    files_to_load = [file_lists[frame_ids[0]]]
                    for frame in frame_ids[1:]:
                        files_to_load.append(file_lists[frame_ids[frame]])
                else:
                    _select_frames = True
                    files_to_load = file_lists
            else:
                files_to_load = file_lists
                _select_frames = False
                _need_cut = True

            source_file = h5py.File(os.path.join(self._detector_folder, files_to_load[0]), 'r')
            cube = np.array(source_file['entry']['instrument']['detector']['data'], dtype=np.float32)

            for name in files_to_load[1:]:
                source_file = h5py.File(os.path.join(self._detector_folder, name), 'r')
                cube = np.vstack((cube, np.array(source_file['entry']['instrument']['detector']['data'],
                                                 dtype=np.float32)))

            if _need_cut:
                cube = cube[:self._scan_length, :, :]

            if _select_frames:
                cube = cube[frame_ids, :, :]

            return np.array(cube, dtype=np.float32)
        else:
            raise RuntimeError('No lmbd file found')

    # ----------------------------------------------------------------------
    def _get_data_shape(self):
        """
        in case user select 'disk' mode (data is not kept in memory) - we calculate data shape without loading all data
        :return: tuple with data shape
        """

        file_lists = [f for f in os.listdir(self._detector_folder) if f.endswith('.nxs')]
        file_lists.sort()

        if len(file_lists) > 1:
            frame = self._reload_data([0])
            return len(file_lists), frame[0], frame[1]
        else:
            source_file = h5py.File(os.path.join(self._detector_folder, file_lists[0]), 'r')
            return source_file['entry']['instrument']['detector']['data'].shape

    # ----------------------------------------------------------------------
    def _calculate_correction(self, data_shape, frame_ids):

        self._correction = np.ones(data_shape[0], dtype=np.float32)

        try:
            if SETTINGS['atten_correction']:
                if SETTINGS['atten_param'] in self._possible_axes_units[0]:
                    if frame_ids is not None:
                        self._correction *= np.maximum(self._possible_axes_units[0][SETTINGS['atten_param']][frame_ids], 1)
                    else:
                        self._correction *= np.maximum(self._possible_axes_units[0][SETTINGS['atten_param']], 1)
        except Exception as err:
            raise RuntimeError("{}: cannot calculate atten correction: {}".format(self.my_name, err))

        try:
            if SETTINGS['inten_correction']:
                if SETTINGS['inten_param'] in self._possible_axes_units[0]:
                    if frame_ids is not None:
                        self._correction *= np.max((1, self._possible_axes_units[0][SETTINGS['inten_param']][0])) / \
                                            np.maximum(self._possible_axes_units[0][SETTINGS['inten_param']][frame_ids], 1)
                    else:
                        self._correction *= np.max((1, self._possible_axes_units[0][SETTINGS['inten_param']][0])) / \
                                            np.maximum(self._possible_axes_units[0][SETTINGS['inten_param']], 1)

        except Exception as err:
            raise RuntimeError("{}: cannot calculate inten correction: {}".format(self.my_name, err))

    # ----------------------------------------------------------------------
    def _corrections_required(self):
        if super(SardanaDataSet, self)._corrections_required():
            return True

        if SETTINGS['atten_correction']:
            return True

        if SETTINGS['inten_correction']:
            return True

        return False

