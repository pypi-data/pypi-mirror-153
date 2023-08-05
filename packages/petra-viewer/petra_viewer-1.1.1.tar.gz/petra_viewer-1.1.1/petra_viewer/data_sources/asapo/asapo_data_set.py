# Created by matveyev at 18.02.2021

"""
Class for ASAPO stream
inherit from AbstractDataFile and DetectorImage

after creation loads all frames from stream and merges data from them to one 3D cube [frameID, X, Y]
and apply current parameters (maks, flat field etc)

if user change parameters - reloads data from stream, makes new cube and applies new parameters
"""

import numpy as np
from distutils.util import strtobool
import logging

try:
    import asapo_consumer
except:
    pass

from petra_viewer.main_window import APP_NAME
from petra_viewer.data_sources.base_classes.base_2d_detector import Base2DDetectorDataSet, apply_base_settings

try:
    from AsapoWorker.asapo_receiver import SerialDatasetAsapoReceiver, SerialAsapoReceiver
    from AsapoWorker.data_handler import get_image
except:
    pass

SETTINGS = {'host': '',
            'path': '',
            'has_filesystem': False,
            'beamtime': '',
            'token': '',
            'detectors': '',
            'max_messages': 1000,
            'max_streams': 100,
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
            }

logger = logging.getLogger(APP_NAME)


# ----------------------------------------------------------------------
def apply_settings_asapo(settings):

    for param in ['host', 'path', 'beamtime', 'token', 'detectors']:
        if param in settings:
            SETTINGS[param] = settings[param]
        else:
            SETTINGS[param] = ''

    SETTINGS['has_filesystem'] = False
    if 'has_filesystem' in settings:
        try:
            SETTINGS['has_filesystem'] = strtobool(settings['has_filesystem'])
        except:
            pass

    if 'max_messages' in settings:
        SETTINGS['max_messages'] = 100
        if param in settings:
            try:
                SETTINGS[param] = int(settings[param])
            except:
                pass

    apply_base_settings(settings, SETTINGS)


# ----------------------------------------------------------------------
class ASAPODataSet(Base2DDetectorDataSet):

    # ----------------------------------------------------------------------
    def __init__(self, detector_name, stream_name, data_pool):
        super(ASAPODataSet, self).__init__(data_pool)

        self.my_name = stream_name

        consumer = asapo_consumer.create_consumer(SETTINGS['host'], SETTINGS['path'],
                                                  SETTINGS['has_filesystem'], SETTINGS['beamtime'],
                                                  detector_name, SETTINGS['token'], 1000)
        logger.debug(
            "Create new consumer (host=%s, path=%s, has_filesystem=%s, "
            "beamtime=%s, data_source=%s, token=%s, timeout=%i).",
            SETTINGS['host'], SETTINGS['path'], SETTINGS['has_filesystem'], SETTINGS['beamtime'],
            detector_name, SETTINGS['token'], 1000)

        self._setup_receiver(consumer, stream_name, detector_name)
        self._additional_data['metadata'] = []
        self._additional_data['raw_img'] = []
        self._additional_data['already_loaded_ids'] = []
        if self._data_pool.memory_mode == 'ram':
            self._nD_data_array = self._get_data()
            self._data_shape = list(self._nD_data_array.shape)
        else:
            self._data_shape = self._get_data_shape()
        axes_names = ['message_ID'] + [f'dim_{i}' for i in range(1, len(self._data_shape))]

        self._possible_axes_units = [{name: np.arange(axis_len)} for name, axis_len in zip(axes_names, self._data_shape)]

        self._axes_units = axes_names
        self._axis_units_is_valid = [True for _ in axes_names]

        self._additional_data['frame_ID'] = np.arange(self._data_shape[0])

        self._need_apply_mask = True

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
                range_limit = SETTINGS['max_messages']
            else:
                range_limit = 0
            self._section.append({'axis': axis, 'integration': False, 'min': 0, 'max': self._data_shape[i] - 1,
                                  'step': 1, 'range_limit': range_limit})

    # ----------------------------------------------------------------------
    def update_info(self, info):
        """
        Update data shape using new stream information.

        If data sections uses the last already_loaded_ids it will be update to
        current last already_loaded_ids
        """
        old_max = self._data_shape[0]
        self._data_shape[0] = info['lastId']
        sel = self._section[0]
        if sel['max'] == old_max-1:
            sel['max'] = info['lastId'] - 1
            if not sel['integration'] and sel['axis'] == '':
                sel['min'] = info['lastId'] - 1
            if sel['max'] - sel['min'] >= sel['range_limit']:
                sel['min'] = sel['max'] - sel['range_limit'] - 1

    # ----------------------------------------------------------------------
    def _setup_receiver(self, consumer, stream_name, data_source):
        """
        Create and set parameters for receiver, which will be used to retrieve data from ASAPO.
        Currently there is no information in the ASAPO data_source about it content.
        Several try/except blocks stays to guess, how to retrieve data from given data_source.

        Parameters:
            consumer (asapo_consumer): ASAPO consumer
            stream_name (str): Stream name
            data_source (str): ASAPO data_source
        """
        opt = [['file', SerialAsapoReceiver, False],
               ['file', SerialAsapoReceiver, True],
               ['dataset', SerialDatasetAsapoReceiver, False],
               ['dataset', SerialDatasetAsapoReceiver, True]]

        for setting in opt:
            try:
                self._mode = setting[0]
                self.receiver = setting[1](consumer)
                self.receiver.stream = stream_name
                self.receiver.data_source = data_source
                self.receiver.set_start_id(1)
                self.meta_only = setting[2]
                self.receiver.get_next(self.meta_only)
                break
            except Exception as e:
                logger.debug(f"Setting mode={self._mode} meta_only={self.meta_only} fails: {e}")
        logger.info(f"Set mode '{self._mode}' and receiver: {self.receiver}")

    # ----------------------------------------------------------------------
    def _get_settings(self):
        return SETTINGS

    # -------------------------------------------------------------------
    def get_metadata(self):

        if 'metadata' not in self._additional_data:
            return None

        if self._section[0]['integration']:
            frame_sel = range(self._section[0]['min'], self._section[0]['max'])
        else:
            frame_sel = range(self._section[0]['min'], self._section[0]['min'] + 1)

        item_ids = [self._additional_data['already_loaded_ids'].index(frame) for frame in frame_sel]
        data_to_display = {}
        for item_id in item_ids:
            data_to_display[str(item_id)] = self._additional_data['metadata'][item_id]

        return data_to_display

    # -------------------------------------------------------------------
    def _reload_data(self, frame_ids=None):
        """
        reloads stream
        :param frame_ids: if not None: frames to be loaded
        :return: np.array, 3D data cube
        """

        # ToDO Limit number of retrieved messages
        img_list = []
        logger.debug(f"Retrieve messages from ASAPO. IDs: {frame_ids}")
        if frame_ids is None:
            frame_ids = np.arange(self.receiver.get_current_size())
        for frame in frame_ids:
            if frame not in self._additional_data['already_loaded_ids']:
                if len(self._additional_data['already_loaded_ids']) == SETTINGS['max_messages']:
                    self._additional_data['already_loaded_ids'].pop(0)
                    self._additional_data['metadata'].pop(0)
                self.receiver.set_start_id(frame + 1)
                data, meta_data = self.receiver.get_next(self.meta_only)
                img = self._convert_image(data, meta_data)
                img_list.append(img)
                self._additional_data['metadata'].append(meta_data)
                self._additional_data['already_loaded_ids'].append(frame)
                self._additional_data['raw_img'].append(img.copy())
            else:
                idx = self._additional_data['already_loaded_ids'].index(frame)
                img_list.append(self._additional_data['raw_img'][idx])

        img_array = np.stack(img_list)
        logger.debug(f"Retrieved image array {img_array.shape}, "
                     f"metadata len {len(self._additional_data['metadata'])}")
        return np.stack(img_list)

    # ----------------------------------------------------------------------
    def _convert_image(self, data, meta_data):
        """
        de-Serialize numpy array (image) from ASAPO data based on ASAPO metadata.
        Default empty image of 2x2 is used to be compatible with the rest code of the package.
        Parameters:
            data (byte): data from ASAPO message
            meta_data (dict): metadata from ASAPO message
        Returns:
            image (np.ndarray): n-Dimensional np.array
        """
        def_img = np.zeros((2, 2), dtype=np.float32)
        if data is None:
            return def_img
        try:
            if self._mode == 'file':
                return get_image(data, meta_data).astype(np.float32)
            else:
                return get_image(data[0], meta_data[0]).astype(np.float32)
        except Exception as e:
            logger.info(f"Fail to get image from ASAPO data: {e}")
            return def_img

    # ----------------------------------------------------------------------
    def _get_data_shape(self):
        """
        Get data shape of complete ASAPO stream.
        Assume all messages have the same data shape

        """
        frame = self._reload_data([0])
        return [self.receiver.get_current_size()] + list(frame.shape[1:])
