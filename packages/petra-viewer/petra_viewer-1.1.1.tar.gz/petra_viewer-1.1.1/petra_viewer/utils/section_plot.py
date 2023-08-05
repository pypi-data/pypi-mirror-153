# Created by matveyev at 17.02.2021

from PyQt5 import QtCore, QtGui

import weakref
import numpy as np
import pyqtgraph as pg

import petra_viewer.lookandfeel as lookandfeel
from petra_viewer.utils.fitter import make_fit

# ----------------------------------------------------------------------
class SectionPlot(QtCore.QObject):
    PENCOUNTER = 0

    # Base class for the x_data and beamline parameter plots

    # ----------------------------------------------------------------------
    def __init__(self, plot_item, name, normalized, color):
        super(SectionPlot, self).__init__()

        self.plot_item = weakref.ref(plot_item)

        self.plot = plot_item.plot([], name=name,
                                   pen=pg.mkPen(color=lookandfeel.PLOT_COLORS[color % len(lookandfeel.PLOT_COLORS)]))

        self._fit_style = pg.mkPen(color=lookandfeel.PLOT_COLORS[color % len(lookandfeel.PLOT_COLORS)],
                                   style=QtCore.Qt.DashLine)

        SectionPlot.PENCOUNTER += 1

        self.x_data = np.array([])
        self.y_data = np.array([])

        self._fits = {}

        self._is_visible = True

        self.tooltip = pg.TextItem(text=name, color=(0, 0, 0))
        self.tooltip.setFont(QtGui.QFont("Arial", 9))
        self.tooltip.hide()
        self.plot_item().addItem(self.tooltip)

        self.scan_data = None

        self.plot_is_normalized = normalized

        self._name = name

    # ----------------------------------------------------------------------
    def get_data(self):
        return self.plot.getData()

    # ----------------------------------------------------------------------
    def get_range(self):
        x_data, y_data = self.plot.getData()

        return np.min(x_data), np.max(x_data), np.min(y_data), np.max(y_data)

    # ----------------------------------------------------------------------
    def get_data_to_save(self):
        data = np.transpose(self.plot.getData())
        header = ['x', 'ROI value']
        for function, plot in self._fits.items():
            _, y = plot.getData()
            data = np.hstack((data, np.transpose(y)[:, np.newaxis]))
            header.append(function)

        return header, data

    # ----------------------------------------------------------------------
    def empty(self):
        return len(self.plot.getData()[0]) < 1

    # ----------------------------------------------------------------------
    def set_visible(self, flag):
        self.plot.setVisible(flag)
        if not flag:
            self.tooltip.setVisible(flag)

    # ----------------------------------------------------------------------
    def release(self):
        self.plot_item().removeItem(self.plot)
        self.plot_item().removeItem(self.tooltip)
        self.plot_item().legend.removeItemByAddress(self.plot)
        self.delete_fits()

    # ----------------------------------------------------------------------
    def show_tool_tip(self, flag, pos=None):
        if flag:
            self.tooltip.setColor(self.plot.opts["pen"].color())
            self.tooltip.setPos(pos.x(), pos.y())
            self.tooltip.show()
        else:
            self.tooltip.hide()

    # ----------------------------------------------------------------------
    def distance_y(self, pos):
        x, y = self.plot.getData()
        if np.min(x) <= pos.x() and pos.x() <= np.max(x):
            x_idx = np.argmin(np.abs(x - pos.x()))
            return np.abs(pos.y() - y[x_idx])

        return 1e+8

    # ----------------------------------------------------------------------
    def range_y(self):
        _, y = self.plot.getData()
        return np.abs(np.max(y) - np.min(y))

    # ----------------------------------------------------------------------
    def normalize_plot(self, status, x_min, x_max):
        self.plot_is_normalized = status
        if status:
            if len(self.y_data):
                dy = np.max(self.y_data) - np.min(self.y_data)
                if dy > 0:
                    y = (self.y_data - np.min(self.y_data)) / dy
                    self.plot.setData(self.x_data, y)

        else:
            try:
                if len(self.y_data):
                    self.plot.setData(self.x_data, self.y_data)
            except:
                pass

        self.update_fits(x_min, x_max)

    # ----------------------------------------------------------------------
    def update_plot(self, x, y, x_min, x_max):

        self.x_data = x
        self.y_data = y

        if x is None or y is None:
            self.plot.hide()
            self.delete_fits()
            return

        self.plot.show()

        if self.plot_is_normalized:
            dy = np.max(y) - np.min(y)
            if dy > 0:
                y = (y - np.min(y)) / dy
            else:
                y = y/np.max(y)

        self.plot.setData(self.x_data, y)

        self.update_fits(x_min, x_max)

    # ----------------------------------------------------------------------
    def update_fits(self, x_min, x_max):
        for function in self._fits.keys():
            self.make_fit(function, x_min, x_max)

    # ----------------------------------------------------------------------
    def make_fit(self, function, x_min, x_max):
            x, y = self.plot.getData()

            selected = np.where(np.logical_and(x_min <= x, x <= x_max))
            x = np.copy(x[selected])
            y = np.copy(y[selected])

            if len(x) < 100:
                new_x = np.linspace(np.min(x), np.max(x), 100)
                y = np.interp(new_x, x, y, x[0], x[-1])
                x = new_x

            y_fit, label, fit_res = make_fit(x, y, function)

            plot_name = self._name + ': ' + function + ': ' + label
            if function not in self._fits:
                self._fits[function] = self.plot_item().plot(x, y_fit, name=plot_name, pen=self._fit_style)
            else:
                self._fits[function].setData(x, y_fit, name=plot_name)

    # ----------------------------------------------------------------------
    def remove_fit(self, function):
        if function in self._fits:
            self.plot_item().removeItem(self._fits[function])
            self.plot_item().legend.removeItemByAddress(self._fits[function])
            del self._fits[function]

    # ----------------------------------------------------------------------
    def delete_fits(self):
        for _, plot in self._fits.items():
            self.plot_item().removeItem(plot)
            self.plot_item().legend.removeItemByAddress(plot)
