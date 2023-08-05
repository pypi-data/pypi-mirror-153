# Created by matveyev at 15.02.2021

import h5py
import os
from contextlib import contextmanager
import numpy as np

from PyQt5 import QtCore, QtWidgets


# ----------------------------------------------------------------------
@contextmanager
def wait_cursor():
    try:
        QtWidgets.QApplication.setOverrideCursor(QtCore.Qt.WaitCursor)
        yield
    finally:
        QtWidgets.QApplication.restoreOverrideCursor()

# ----------------------------------------------------------------------
class FileFilter(QtCore.QSortFilterProxyModel):

    new_version = True

    # ----------------------------------------------------------------------
    def filterAcceptsRow(self, source_row, source_parent):
        if self.new_version:
            return super(FileFilter, self).filterAcceptsRow(source_row, source_parent)
        else:
            match = False
            my_index = self.sourceModel().index(source_row, 0, source_parent)
            for row in range(self.sourceModel().rowCount(my_index)):
                match |= self.filterAcceptsRow(row, my_index)

            match |= super(FileFilter, self).filterAcceptsRow(source_row, source_parent)

            return match

    # ----------------------------------------------------------------------
    def lessThan(self, left, right):
        left_name = self.sourceModel().data(left)
        right_name = self.sourceModel().data(right)

        left_is_dir = self.sourceModel().isDir(left)
        right_is_dir = self.sourceModel().isDir(right)

        return (not left_is_dir, left_name) < (not right_is_dir, right_name)


# ----------------------------------------------------------------------
def refresh_combo_box(combo, text):
    idx = combo.findText(text)
    if idx != -1:
        combo.setCurrentIndex(idx)
        return True
    else:
        combo.setCurrentIndex(0)
        return False


# ----------------------------------------------------------------------
def get_text_coordinates(plot_item, size, position='tl'):

    [[x_min, x_max], [y_min, y_max]] = plot_item.viewRange()

    dx = abs(x_max - x_min) * 0.05
    dy = abs(y_max - y_min) * 0.05

    if position == 'tl':
      textx = x_min + dx
      texty = y_max - dy
    elif position == 'tr':
      textx = x_max - dx - size.width() * plot_item.getViewBox().viewPixelSize()[0]
      texty = y_max - dy
    elif position == 'bl':
      textx = x_max + dx
      texty = y_min + dy + size.height() * plot_item.getViewBox().viewPixelSize()[1]
    elif position == 'br':
      textx = x_max - dx - size.width() * plot_item.getViewBox().viewPixelSize()[0]
      texty = y_min + dy + size.height() * plot_item.getViewBox().viewPixelSize()[1]

    return QtCore.QPointF(textx, texty)


# ----------------------------------------------------------------------
def read_mask_file(file_name):
    mask = None
    try:
        with h5py.File(file_name, 'r') as f:
            for name in ['mask', 'pixel_mask']:
                if name in f.keys():
                    mask = np.array(f[name])
                    break
    except:
        pass

    return mask

# ----------------------------------------------------------------------
def read_ff_file(file_name):
    ff = None
    try:
        with h5py.File(file_name, 'r') as f:
            for name in ['ff']:
                if name in f.keys():
                    ff = np.array(f[name])
                    break
    except:
        pass

    return ff


# ----------------------------------------------------------------------
def info_dialog(text):
    msg = QtWidgets.QMessageBox()
    msg.setModal(False)
    msg.setIcon(QtWidgets.QMessageBox.Information)
    msg.setText(text)
    msg.setWindowTitle("Info")
    msg.show()
    return msg


# ----------------------------------------------------------------------
def check_settings(new_settings):
    for entry, sub_entries in zip(['WIDGETS'], [['file_types', 'visualization']]):
        if entry not in new_settings:
            return False
        for sub_entry in sub_entries:
            if sub_entry not in new_settings[entry]:
                return False
    return True