# Created by matveyev at 15.02.2021

import os
import psutil
import numpy as np
import logging

from collections import OrderedDict

from PyQt5 import QtCore, QtWidgets

from petra_viewer.utils.batcher import Batcher
from petra_viewer.utils.opener import Opener
from petra_viewer.utils.utils import wait_cursor

from petra_viewer.data_sources.reciprocal.reciprocal_data_set import ReciprocalScan

from petra_viewer.utils.roi import ROI
from petra_viewer.widgets.batch_progress import BatchProgress
from petra_viewer.main_window import APP_NAME

logger = logging.getLogger(APP_NAME)


# ----------------------------------------------------------------------
class DataPool(QtCore.QObject):

    new_file_added = QtCore.pyqtSignal(str)
    file_deleted = QtCore.pyqtSignal(str)
    close_file = QtCore.pyqtSignal(str)
    file_updated = QtCore.pyqtSignal(str)

    data_updated = QtCore.pyqtSignal()

    # ----------------------------------------------------------------------
    def __init__(self, parent):

        super(DataPool, self).__init__()

        self.main_window = parent

        self._lim_mode = 'no'
        self._max_num_files = None
        self._max_memory = None
        self.memory_mode = 'ram'

        self._files_data = {}
        self._files_history = []
        self._protected_files = []

        self._rois = OrderedDict()
        self._last_roi_key = -1

        self.settings = {'export_file_delimiter': ';',
                         'export_file_format': '%.6e'}

        self._batcher = None
        self._opener = None
        self._open_mgs = _open_file_dialog()

        self._progress = BatchProgress()
        self._progress.stop_batch.connect(self._interrupt_batch)

        # needed for tests
        self.open_file_in_progress = False

    # ----------------------------------------------------------------------
    def get_settings(self):
        return self.main_window.setting()

    # ----------------------------------------------------------------------
    def set_settings(self, settings):
        """
            this function is called during startup and everytime user changes settings
        """

        if 'max_open_files' in settings:
            self._max_num_files = int(settings['max_open_files'])

        if 'memory_mode' in settings:
            self.memory_mode = settings['memory_mode']

        if 'max_memory_usage' in settings:
            self._max_memory = int(settings['max_memory_usage'])

        if 'export_file_delimiter' in settings:
            if settings['export_file_delimiter'] == 'semicolumn':
                self.settings['export_file_delimiter'] = ';'

        if 'export_file_format' in settings:
            self.settings['export_file_format'] = '%' + settings['export_file_format']

    # ----------------------------------------------------------------------
    def report_error(self, title, informative_text, detailed_text):
        """
            this function reports error to the main window
        """

        self.main_window.report_error(title,
                                      informative_text=informative_text,
                                      detailed_text=detailed_text)

    # ----------------------------------------------------------------------
    #       Files/streams open/save section
    # ----------------------------------------------------------------------
    def open_stream(self, detector_name, stream_name, info):
        """
            called by signal from ASAPO browser
            since we don't want the GUI to freeze during stream load - we make an QThread, which in really reads data

            Parameters:
                detector_name (str): Name of ASAPO data source
                stream_name (str): Name of ASAPO stream
                info (dict): Properties of stream
        """

        # all opened files are entry to self._files_data dict
        # first we check, that this stream in not yet opened
        entry_name = '/'.join([detector_name, stream_name])
        if entry_name in self._files_data:
            self._files_data[entry_name].update_info(info)
            self.file_updated.emit(entry_name)
            logger.error("File with this name already opened")
            return

        self._start_opener('stream', f'Opening stream {stream_name}',
                           {'detector_name': detector_name, 'stream_name': stream_name, 'entry_name': entry_name})

    # ----------------------------------------------------------------------
    def update_stream(self, detector_name, stream_name, info):
        """
            called by signal from ASAPO browser
            since we don't want the GUI to freeze during stream load - we make an QThread, which in really reads data

            Parameters:
                detector_name (str): Name of ASAPO data source
                stream_name (str): Name of ASAPO stream
                info (dict): Properties of stream
        """
        entry_name = '/'.join([detector_name, stream_name])
        if entry_name in self._files_data:
            logger.debug(f"Update stream {entry_name}")
            self._files_data[entry_name].update_info(info)
            self.file_updated.emit(entry_name)

    # ----------------------------------------------------------------------
    def open_file(self, file_name, mode):
        """
            called by signal from file browser

            since we don't want the GUI to freeze during stream load - we make an QThread, which in really reads data

        """

        # all opened files are entry to self._files_data dict
        # first we check, that this stream in not yet opened
        entry_name = os.path.splitext(os.path.basename(file_name))[0]
        if entry_name in self._files_data:
            logger.error("File with this name already opened")
            return

        if ".nxs" in file_name:
            self._start_opener('sardana', f'Opening file {file_name}',
                               {'file_name': file_name, 'entry_name': entry_name})
        elif ".h5" in file_name:
            if mode == 'beam':
                self._start_opener('beamline', f'Opening file {file_name}',
                                   {'file_name': file_name, 'entry_name': entry_name})
            else:
                self._start_opener('reciprocal', f'Opening file {file_name}',
                                   {'file_name': file_name, 'entry_name': entry_name})

    # ----------------------------------------------------------------------
    def open_test(self, test_name):
        """
            called by signal from tests browser

            since we don't want the GUI to freeze during stream load - we make an QThread, which in really reads data

        """

        # all opened files are entry to self._files_data dict
        # first we check, that this stream in not yet opened
        entry_name = test_name
        counter = 0
        while entry_name in self._files_data:
            counter += 1
            entry_name = f'{test_name}_{counter}'

        self._start_opener('test', f'Opening test {entry_name}',
                           {'test_name': test_name, 'entry_name': entry_name})

    # ----------------------------------------------------------------------
    def _start_opener(self, mode, user_msg, kwargs):
        """
        create popup message for user

        :param mode:
        :param user_msg: message in popup dialog
        :param kwargs:
        :return:
        """
        #
        logger.debug(f"Start opener with mode: {mode}, {user_msg}, {kwargs}")
        self._open_mgs.setText(user_msg)
        self._open_mgs.show()

        self.open_file_in_progress = True
        self._opener = Opener(self, mode, kwargs)
        self._opener.exception.connect(self.report_error)
        self._opener.done.connect(self._open_done)
        self._opener.start()

    # ----------------------------------------------------------------------
    def _open_done(self):
        """
            called by Opener, closes popup message
        """

        self._open_mgs.hide()

    # ----------------------------------------------------------------------
    def add_new_entry(self, entry_name, entry):
        """
            called from Opener, after the data are read, and add entry to the self._files_data

        """

        # first we check, that we do not overcome user limit to max opened files
        if self._max_num_files is not None and self._max_num_files > 0:
            while len(self._files_data) >= self._max_num_files:
                if not self._get_first_to_close():
                    break

        # or that we do not overcome user limit to memory use
        elif self._max_memory is not None and self._max_memory > 0:
            while float(psutil.Process(os.getpid()).memory_info().rss) / (1024. * 1024.) >= self._max_memory:
                if not self._get_first_to_close():
                    break

        self._files_data[entry_name] = entry

        # since the dict is not order according to the adding time and there are "protected" files,
        # we just track history of opened files in separate list. TODO: use OrderedDict
        self._files_history.append(entry_name)

        # than we need to update all axes rages and re-update all settings for all opened files
        self.get_all_axes_limits()

        # now we read to notify the GUI about new added file
        self.new_file_added.emit(entry_name)

        # workaround to enable test debug
        self.open_file_in_progress = False

    # ----------------------------------------------------------------------
    def _get_first_to_close(self):
        """
            all files, moved to comparison are protected to be closed, so we return first non-protected from history
            :returns True is file was close, False if there is no file to be closed
        """

        for name in self._files_history:
            if name not in self._protected_files:
                self.close_file.emit(name)
                self.remove_file(name)
                return True

        return False

    # ----------------------------------------------------------------------
    def remove_file(self, name):

        del self._files_data[name]
        self._files_history.remove(name)
        self.file_deleted.emit(name)

    # ----------------------------------------------------------------------
    def protect_file(self, name, status):
        """
            when user moves file to comparison, we don not close it in automatic mode (max files opened, max memory)
        """

        if status:
            if name not in self._protected_files:
                self._protected_files.append(name)
        else:
            if name in self._protected_files:
                self._protected_files.remove(name)

    # ----------------------------------------------------------------------
    def save_converted(self, entry_name, gridder):
        """
            saves files after conversion to reciprocal space
        """

        file_name, ok = QtWidgets.QFileDialog.getSaveFileName(self.main_window, 'Select file name',
                                                              self.main_window.get_current_folder() + "/" + entry_name,
                                                              'HDF5 format (*.h5)')
        if ok:
            # since we automatically open saved file, file name has to be unique
            while file_name in self._files_data:
                file_name, ok = QtWidgets.QFileDialog.getSaveFileName(self.main_window, 'Select file name',
                                                                      self.main_window.get_current_folder() + "/" + entry_name,
                                                                      'HDF5 format (*.h5)')
            if not ok:
                return

        if not file_name.endswith('.h5'):
            file_name += '.h5'

        ReciprocalScan(self, gridder=gridder).save_file(file_name)
        self.open_file(file_name, 'reciprocal')

    # ----------------------------------------------------------------------
    #       General section
    # ----------------------------------------------------------------------
    def get_histogram(self, file, mode):
        return self._files_data[file].get_histogram(mode)

    # ----------------------------------------------------------------------
    def get_levels(self, file, mode):
        return self._files_data[file].get_levels(mode)

    # ----------------------------------------------------------------------
    def get_possible_axis_units(self, file_name, axis):
        """

        :return: list, possible units for particular axis
        """

        return self._files_data[file_name].get_possible_axis_units(axis)

    # ----------------------------------------------------------------------
    def set_axis_units(self, file_name, axis, units):
        """

        :param: axis, particular axis
        :param: units, user selected units
        """
        self._files_data[file_name].set_axis_units(axis, units)

    # ----------------------------------------------------------------------
    def get_axis_units(self, file_name, axis):
        """

        :return: str, selected units for particular axis
        """
        return self._files_data[file_name].get_axis_units(axis)

    # ----------------------------------------------------------------------
    def are_axes_valid(self, file_name):
        """

        :return: str, selected units for particular axis
        """
        return self._files_data[file_name].are_axes_valid()

    # ----------------------------------------------------------------------
    def get_file_dimension(self, file_name):
        """
            :param: file_name
            :return: dimension of the file
        """

        return self._files_data[file_name].get_file_dimension()

    # ----------------------------------------------------------------------
    def get_metadata(self, file_name):
        """
            :param: file_name
            :return: metadata to be displayed
        """
        logger.debug(f"Metadata requested for file {file_name}")

        return self._files_data[file_name].get_metadata()

    # ----------------------------------------------------------------------
    #       ROIs plots section
    # ----------------------------------------------------------------------
    def roi_counts(self):
        return len(self._rois)

    # ----------------------------------------------------------------------
    def get_roi_key(self, roi_num):
        """
            :returns the key for Ns roi in dict
        """
        return list(self._rois.keys())[roi_num]

    # ----------------------------------------------------------------------
    def recalculate_rois(self, axis, new_units):

        main_file = self.main_window.get_current_file()
        if main_file is None:
            return

        for roi in self._rois.values():
            roi_params = roi.get_section_params()
            roi_axis = None
            for roi_axis in range(roi_params['dimensions']):
                if roi_params['axis_{}'.format(roi_axis)] == axis:
                    break

            if roi_axis is None or roi_axis == 0:
                continue

            new_min = self._files_data[main_file].recalculate_value(axis, roi_params['axis_{}_pos'.format(roi_axis)],
                                                                    new_units)
            new_max = self._files_data[main_file].recalculate_value(axis, roi_params['axis_{}_pos'.format(roi_axis)]
                                                                    + roi_params['axis_{}_width'.format(roi_axis)],
                                                                    new_units)
            if new_min is None or new_max is None:
                continue

            roi_params['axis_{}_pos'.format(roi_axis)] = new_min
            roi_params['axis_{}_width'.format(roi_axis)] = new_max - new_min

    # ----------------------------------------------------------------------
    def add_new_roi(self):
        """
            all ROI are kept in OrderedDict with unique key
        """

        main_file = self.main_window.get_current_file()
        if main_file is None:
            return None, None, None

        file_dim = self._files_data[main_file].get_file_dimension()

        axis = None
        section = self.get_section(main_file)
        for ind, sect in enumerate(section):
            if sect['axis'] == 'Z':
                axis = ind
                break
        if axis is None:
            for ind, sect in enumerate(section):
                if sect['axis'] == '':
                    axis = ind
                    break
        if axis is None:
            for ind, sect in enumerate(section):
                if sect['axis'] == 'X':
                    axis = ind
                    break

        self._last_roi_key += 1
        self._rois[self._last_roi_key] = ROI(self, self._last_roi_key, file_dim, axis)

        return self._last_roi_key, self.get_roi_index(self._last_roi_key), file_dim

    # ----------------------------------------------------------------------
    def get_roi_index(self, roi_key):
        for idx, key in enumerate(self._rois.keys()):
            if key == roi_key:
                return idx

        return None

    # ----------------------------------------------------------------------
    def delete_roi(self, roi_key):
        del self._rois[roi_key]

    # ----------------------------------------------------------------------
    def get_roi_cut(self, file, roi_key):
        """
            calculate 3D cut from the data cube, defined by the ROI[roi_key]
            :returns 3d np.array
        """
        return self._files_data[file].get_roi_cut(self._rois[roi_key].get_section_params())

    # ----------------------------------------------------------------------
    def get_roi_plot(self, file, roi_key):
        """
            calculate 1D plot from the data cube, defined by the ROI[roi_key]
            :returns two 1D np.arrays (X, Y)
        """
        with wait_cursor():
            return self._files_data[file].get_roi_plot(self._rois[roi_key].get_section_params())

    # ----------------------------------------------------------------------
    def set_section_axis(self, roi_key, axis):
        """
            set new section axis for ROI
            :param roi_key - key for ROIs dict,
            :param axis - new ROI axis
        """
        logger.debug(f"data_pool.set_section_axis: roi_key {roi_key}, axis: {axis}")
        self._rois[roi_key].set_section_axis(axis)

    # ----------------------------------------------------------------------
    def get_roi_axis(self, roi_key, real_axis):
        """
            return internal ROI axis for given real axis
            :param roi_key - key for ROIs dict,
            :param real_axis - data cube axis
            :return int, ROI internal axis
        """
        section_params = self._rois[roi_key].get_section_params()
        for ind in range(section_params['dimensions']):
            if section_params['axis_{}'.format(ind)] == real_axis:
                return ind

        return None

    # ----------------------------------------------------------------------
    def roi_parameter_changed(self, roi_key, roi_axis, param, value):
        """
            function checks if the requested ROI`s value is valid. If value is valid - returns it,
            if not, returns the most close valid one
            :param roi_key - key for ROIs dict,
            :param roi_axis - which real_axis is modified,
            :param param - 'width', 'pos'
            :param value - requested by user value
            :returns accepted value
        """
        logger.debug(f"data_pool.set_section_axis: roi_key {roi_key}, axis: {roi_axis}, param: {param}, value: {value}")

        section_params = self._rois[roi_key].get_section_params()
        real_axis = section_params['axis_{}'.format(roi_axis)]

        axis_lim = self.get_all_axes_limits()
        if axis_lim is not None:
            return self._rois[roi_key].roi_parameter_changed(roi_axis, param, value, axis_lim[real_axis])
        else:
            return value

    # ----------------------------------------------------------------------
    def get_roi_axis_name(self, roi_key, file):
        """
            :returns axis name, along which ROI is calculated, for particular file
        """
        return self._files_data[file].get_file_axes()[self._rois[roi_key].get_param('axis_0')]

    # ----------------------------------------------------------------------
    def get_roi_param(self, roi_key, param):
        """
            :param roi_key
            :param param: 'axis_0' - axis along which roi has to be plotted;
            'axis_1', 'axis_1_pos', 'axis_1_width' - cut parameters
            ...
            'axis_N', 'axis_N_pos', 'axis_N_width' - cut parameters

            :returns requested value
        """
        return self._rois[roi_key].get_param(param)

    # ----------------------------------------------------------------------
    def get_roi_limits(self, roi_key, section_axis):
        """
            :returns max and min values for particular axis and ROI for all files have the same dims
        """
        section_params = self._rois[roi_key].get_section_params()
        real_axis = section_params['axis_{}'.format(section_axis)]

        axis_lim = self.get_all_axes_limits()
        if axis_lim is not None:
            axis_min = axis_lim[real_axis][0]
            axis_max = axis_lim[real_axis][1]

            return axis_min, axis_max, \
                   axis_max - axis_min - section_params['axis_{}_width'.format(section_axis)], \
                   axis_max - axis_min - section_params['axis_{}_pos'.format(section_axis)]

        else:
            return None, None, None, None

    # ----------------------------------------------------------------------
    #       ROIs batch processing section
    # ----------------------------------------------------------------------
    def _interrupt_batch(self):
        self._batcher.interrupt_batch()

    # ----------------------------------------------------------------------
    def _new_batch_file(self, fname, progress):
        self._progress.add_values(fname, progress)

    # ----------------------------------------------------------------------
    def _new_batch_done(self):
        self._progress.hide()

    # ----------------------------------------------------------------------
    def batch_process_rois(self, file_list, dir_name, file_type):
        """

        :param file_list: list of files to be processed
        :param dir_name: output directory
        :param file_type: output file type
        :return:

        """
        # first we reset progress bar
        self._progress.clear()
        self._progress.show()

        self._batcher = Batcher(self, file_list, dir_name, file_type)
        self._batcher.exception.connect(self.report_error)
        self._batcher.new_file.connect(self._new_batch_file)
        self._batcher.done.connect(self._new_batch_done)
        self._batcher.start()

    # ----------------------------------------------------------------------
    def save_roi_to_file(self, file_type, save_name, header, data):
        """
        called from Batcher to save processed data
        :param file_type:
        :param save_name:
        :param header:
        :param data:
        :return:
        """
        if file_type == '.txt':
            np.savetxt(save_name, data, fmt=self.settings['export_file_format'],
                       delimiter=self.settings['export_file_delimiter'],
                       newline='\n', header=';'.join(header))

    # ----------------------------------------------------------------------
    #       2D frames section
    # ----------------------------------------------------------------------
    def get_2d_picture(self, file):
        """
        returns 2D frame to be displayed in Frame viewer
        :param file: key for self._files_data
        :return: 2D np.array
        """
        logger.debug(f"Return 2D image: for file {file}")
        with wait_cursor():
            return self._files_data[file].get_2d_picture()

        # ----------------------------------------------------------------------
    def get_section(self, file):
        """
        Return previous sections of files
        """
        return self._files_data[file].get_section()

    # ----------------------------------------------------------------------
    def save_section(self, file, section):
        """
        Saves sections of files
        :param section: dict with section
        """
        return self._files_data[file].save_section(section)

    # ----------------------------------------------------------------------
    def get_max_frame_along_axis(self, file, axis):
        """

        :param file: key for self._files_data
        :param axis:
        :return: maximum value along requested axis
        """
        return self._files_data[file].get_max_frame_along_axis(axis)

    # ----------------------------------------------------------------------
    def get_additional_data(self, file, entry):
        """
        for some file types we can store additional information
        :param file:
        :param entry:
        :return: if file has requested entry - returns it, else None
        """
        return self._files_data[file].get_additional_data(entry)

    # ----------------------------------------------------------------------
    def get_frame_for_value(self, file, axis, pos, check_range=False):
        """
        for some file types user can select the displayed unit for some axis
        e.g. for Sardana scan we can display point_nb, or motor position etc...

        here we return the frame number along this axis for particular unit value

        :param file:
        :param axis:
        :param pos:
        :return:
        """
        return self._files_data[file].get_frame_for_value(axis, pos, check_range)

    # ----------------------------------------------------------------------
    def get_value_for_frame(self, file, axis, pos):
        """
        for some file types user can select the displayed unit for some axis
        e.g. for Sardana scan we can display point_nb, or motor position etc...

        here we return the unit value along this axis for particular frame number
        :param file:
        :param axis:
        :param pos:
        :return:
        """
        return self._files_data[file].get_value_for_frame(axis, pos)

    # ----------------------------------------------------------------------
    def get_axis_resolution(self, file, axis):
        """
        for some file types user can select the displayed unit for some axis
        e.g. for Sardana scan we can display point_nb, or motor position etc...

        here we return the expected resolution of axis to set the resolution of spin boxes
        :param file:
        :param axis:
        :return: int
        """

        return self._files_data[file].get_axis_resolution(axis)

    # ----------------------------------------------------------------------
    def get_file_axes(self, file):
        """
        some files can have own axes captions
        :param file:
        :return: dict {axis_index: axis_name}
        """
        return self._files_data[file].get_file_axes()

    # ----------------------------------------------------------------------
    def get_file_axis_limits(self, file):
        """
        Return axis limits of given file
        :param file:
        :return: dict {axis_index: axis_limits}
        """
        return self._files_data[file].get_axis_limits()

    # ----------------------------------------------------------------------
    def get_all_axes_limits(self, file_dim=None):
        """
        recalculates the limits for all files
        :file_dim: dim of files to be included in calculations
        :return:
        """

        if file_dim is None:
            main_file = self.main_window.get_current_file()
            if main_file is None:
                return None

            file_dim = self._files_data[main_file].get_file_dimension()

        new_limits = [[0, 0] for _ in range(file_dim)]

        for data_set in self._files_data.values():
            if data_set.get_file_dimension() != file_dim:
                continue

            for axis, max_frame in enumerate(data_set.get_axis_limits()):
                min_v = data_set.get_value_for_frame(axis, 0)
                new_limits[axis][0] = min(new_limits[axis][0], min_v)

                max_v = data_set.get_value_for_frame(axis, max_frame)
                new_limits[axis][1] = max(new_limits[axis][1], max_v)

        return new_limits

    # ----------------------------------------------------------------------
    #       3D data section
    # ----------------------------------------------------------------------
    def get_3d_cube(self, file, roi_ind):
        """
        Return full 3D data cube
        :param file:
        :param roi_ind: index of ROI to be displayed
        :return: 3D np array
        """

        if roi_ind == -1:
            section = None
        else:
            section = self._rois[roi_ind].get_section_params()

        with wait_cursor():
            return self._files_data[file].get_3d_cube(section)

    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    # ----------------------------------------------------------------------
    def apply_settings(self):
        for data in self._files_data.values():
            data.apply_settings()

        self.data_updated.emit()


# ----------------------------------------------------------------------
def _open_file_dialog():
    """
        displays popup message during file open
    :return:
    """
    open_mgs = QtWidgets.QMessageBox()
    open_mgs.setModal(False)
    open_mgs.setIcon(QtWidgets.QMessageBox.Information)
    open_mgs.setWindowTitle("Opening ...")
    open_mgs.setStandardButtons(QtWidgets.QMessageBox.NoButton)
    return open_mgs
