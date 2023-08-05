# Created by matveyev at 10.11.2021

from PyQt5 import QtCore


class FakeImageItem(QtCore.QObject):

    sigImageChanged = QtCore.pyqtSignal()

    _levels = None, None

    # ----------------------------------------------------------------------
    def __init__(self, data_pool, image_item=None):
        super(FakeImageItem, self).__init__()

        self._current_file = None
        self._mode = 'lin'
        self._data_pool = data_pool
        self._image_item = image_item

    # ----------------------------------------------------------------------
    @property
    def levels(self):
        if self._current_file is None:
            return None, None

        if self._levels[0] is None:
            self._levels = self._data_pool.get_levels(self._current_file, self._mode)

        return self._levels

    # ----------------------------------------------------------------------
    def setAutoLevels(self):
        self._levels = self._data_pool.get_levels(self._current_file, self._mode)

    # ----------------------------------------------------------------------
    def setMode(self, mode):
        self._mode = mode
        self._levels = self._data_pool.get_levels(self._current_file, self._mode)
        self.sigImageChanged.emit()

    # ----------------------------------------------------------------------
    def setNewFile(self, file):
        self._current_file = file
        self._levels = None, None
        self.sigImageChanged.emit()

    # ----------------------------------------------------------------------
    def setEmptyFile(self):
        self._current_file = None
        self._levels = (0, 1)
        self.sigImageChanged.emit()

    # ----------------------------------------------------------------------
    def setLookupTable(self, lut):
        if self._image_item is not None:
            self._image_item.setLookupTable(lut)

    # ----------------------------------------------------------------------
    def setLevels(self, levels):
        self._levels = levels
        if self._image_item is not None:
            self._image_item.setLevels(levels)

    # ----------------------------------------------------------------------
    def getHistogram(self, perChannel=False):
        if self._current_file is None:
            return None, None
        else:
            return self._data_pool.get_histogram(self._current_file, self._mode)

    # ----------------------------------------------------------------------
    def channels(self):
        if self._image_item is not None:
            return self._image_item.channels()
        else:
            return 1