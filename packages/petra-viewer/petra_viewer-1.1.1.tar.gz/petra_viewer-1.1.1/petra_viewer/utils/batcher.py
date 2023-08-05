import os

import h5py
import numpy as np
from PyQt5 import QtCore

from petra_viewer.data_sources.sardana.sardana_data_set import SardanaDataSet


#----------------------------------------------------------------------
class Batcher(QtCore.QThread):

    """
    separate QThread, that calculates ROIs for list of files
    """

    exception = QtCore.pyqtSignal(str, str, str)
    new_file = QtCore.pyqtSignal(str, float)
    done = QtCore.pyqtSignal()

    #----------------------------------------------------------------------
    def __init__(self, data_pool, file_list, dir_name, file_type):
        super(Batcher, self).__init__()
        self.file_list = file_list
        self.dir_name = dir_name
        self.file_type = file_type

        self.data_pool = data_pool

        self._stop_batch = False

    # ----------------------------------------------------------------------
    def interrupt_batch(self):
        self._stop_batch = True

    # ----------------------------------------------------------------------
    def run(self):
        total_files = len(self.file_list )
        for ind, file_name in enumerate(self.file_list):
            if not self._stop_batch:
                try:
                    with h5py.File(file_name, 'r') as f:
                        if 'scan' in f.keys():
                            self.new_file.emit(file_name, ind/total_files)
                            new_file = SardanaDataSet(self.data_pool, file_name)
                            for ind, roi in self.data_pool._rois.items():
                                x_axis, y_axis = new_file.get_roi_plot(roi.get_section_params())
                                header = [new_file.get_file_axes()[roi.get_param('axis_0')], 'ROI_value']
                                save_name = ''.join(os.path.splitext(os.path.basename(file_name))[:-1]) + \
                                            "_ROI_{}".format(ind) + self.file_type
                                self.data_pool.save_roi_to_file(self.file_type,
                                                                os.path.join(self.dir_name, save_name),
                                                                header,
                                                                np.transpose(np.vstack((x_axis, y_axis))))

                except Exception as err:
                    error_msg = f'{err.__class__.__module__}.{err.__class__.__name__}: {err}'
                    error_cause = err.__cause__
                    while error_cause is not None:
                        error_msg += f'\n\nCaused by {error_cause.__class__.__module__}.{error_cause.__class__.__name__}: {error_cause}'
                        error_cause = error_cause.__cause__

                    self.exception.emit('Cannot calculate ROI',
                                        'Cannot calculate ROI for {}'.format(file_name),
                                        error_msg)
            else:
                break

        self.done.emit()