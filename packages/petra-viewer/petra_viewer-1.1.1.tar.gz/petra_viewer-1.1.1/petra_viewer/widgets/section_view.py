# Created by matveyev at 15.02.2021
import numpy as np

WIDGET_NAME = 'SectionView'

import pyqtgraph as pg
import re
import os

from PyQt5 import QtWidgets, QtCore, QtGui, QtPrintSupport
from petra_viewer.gui.section_viewer_ui import Ui_SectionView

from petra_viewer.utils.section_plot import SectionPlot
from petra_viewer.widgets.section_range import SectionRange
from petra_viewer.utils.cursors import CrosshairCursor, Ruler
from petra_viewer.utils.legend_item import addLegend


# ----------------------------------------------------------------------
class SectionView(QtWidgets.QWidget):
    """
    """

    update_roi = QtCore.pyqtSignal(int)

    delete_me = QtCore.pyqtSignal(int)

    # ----------------------------------------------------------------------
    def __init__(self, parent, data_pool, my_id, my_dims):
        """
        """
        super(SectionView, self).__init__()
        self._ui = Ui_SectionView()
        self._ui.setupUi(self)
        self._init_tool_bar()

        self._parent = parent
        self.data_pool = data_pool
        self.my_id = my_id
        self.my_dims = my_dims

        self._enabled = True

        self._enabled_fits = []

        self._main_plot = pg.PlotItem()
        self._main_plot.showGrid(True, True)
        # self._main_plot.setMenuEnabled(False)
        self._main_plot.getViewBox().setMouseMode(pg.ViewBox.RectMode)

        self._ui.gv_main.setStyleSheet("")
        self._ui.gv_main.setBackground('w')
        self._ui.gv_main.setObjectName("gvMain")

        self._ui.gv_main.setCentralItem(self._main_plot)
        self._ui.gv_main.setRenderHints(self._ui.gv_main.renderHints())

        self._section_plots = {}
        self._normalized = False

        self._cross = CrosshairCursor(self._main_plot)
        self._cross.setVisible(False)
        self._ruler = Ruler(self._main_plot)
        self._ruler.setEnabled(False)

        range_pen = pg.mkPen(color='r', width=2, style=QtCore.Qt.DashLine)
        self.range_line_from = pg.InfiniteLine(angle=90, movable=False, pen=range_pen)
        self.range_line_from.sigPositionChanged.connect(
            lambda: self._ui.dsp_cut_from.setValue(self.range_line_from.value()))
        self.range_line_to = pg.InfiniteLine(angle=90, movable=False, pen=range_pen)
        self.range_line_to.sigPositionChanged.connect(
            lambda: self._ui.dsp_cut_to.setValue(self.range_line_to.value()))

        self._main_plot.addItem(self.range_line_from, ignoreBounds=True)
        self._main_plot.addItem(self.range_line_to, ignoreBounds=True)

        self._legend = addLegend(self._main_plot)
        self._legend.hide()

        self._current_axes_num = 0
        self._section_ranger = []
        self._selector_layout = QtWidgets.QVBoxLayout(self._ui.range_selectors)
        self._selector_layout.setSpacing(0)
        self._selector_layout.setContentsMargins(0, 0, 0, 0)

        self._ui.cb_section_axis.clear()
        self._ui.cb_section_axis.addItems(self.data_pool.get_file_axes(self._parent.get_current_file()))
        self._ui.cb_section_axis.setCurrentIndex(self.data_pool.get_roi_param(self.my_id, 'axis_0'))

        self._section_ranger = []

        for ind in range(1, self.my_dims):
            widget = SectionRange(self, self.data_pool, self.my_id, ind)
            widget.setup_view()
            widget.update_roi.connect(lambda roi_id: self.update_roi.emit(roi_id))
            self._section_ranger.append(widget)
            self._selector_layout.layout().addWidget(widget)

        self._selector_layout.layout().addSpacerItem(QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding))

        self._ui.cb_section_axis.currentIndexChanged.connect(self._set_new_section_axis)

        self._main_plot.scene().sigMouseMoved.connect(self._mouse_moved)
        self._main_plot.scene().sigMouseClicked.connect(self._mouse_clicked)
        # self._main_plot.scene().sigMouseHover.connect(self._mouse_hover)

        self._ui.dsp_cut_from.valueChanged.connect(lambda value, x='from': self._check_cut(x, value))
        self._ui.dsp_cut_to.valueChanged.connect(lambda value, x='to': self._check_cut(x, value))
        self._ui.bg_cut_range.buttonClicked.connect(lambda selection: self._cut_range(selection))
        self._main_plot.sigXRangeChanged.connect(self._new_range)

        self._ui.cmd_delete_me.clicked.connect(lambda state, idx=my_id: self.delete_me.emit(idx))

    # ----------------------------------------------------------------------
    def main_file_changed(self):
        if self.get_current_file() is not None:
            self._enabled = self.data_pool.get_file_dimension(self.get_current_file()) == self.my_dims
        else:
            self._enabled = False

        self._ui.cb_section_axis.setEnabled(self._enabled)

        for widget in self._section_ranger:
            widget.enable_me(self._enabled)

    # ----------------------------------------------------------------------
    def get_current_file(self):
        return self._parent.get_current_file()

    # ----------------------------------------------------------------------
    def refresh_name(self):
        return self.data_pool.get_roi_index(self.my_id)

    # ----------------------------------------------------------------------
    def roi_changed(self):
        if not self._enabled:
            return

        self._block_signals(True)

        for widget in self._section_ranger:
            widget.refresh_view()

        self._block_signals(False)

        self.update_plots()

    # ----------------------------------------------------------------------
    def add_file(self, file_name, color):
        if self.data_pool.get_file_dimension(file_name) != self.my_dims:
            return

        self._section_plots[file_name] = SectionPlot(self._main_plot, file_name, self._normalized, color)
        x, y = self.data_pool.get_roi_plot(file_name, self.my_id)
        x_min, x_max = self._get_fit_range()
        self._section_plots[file_name].update_plot(x, y, x_min, x_max)
        for function in self._enabled_fits:
            self._section_plots[file_name].make_fit(function, x_min, x_max)

    # ----------------------------------------------------------------------
    def delete_file(self, file_name):
        if file_name in self._section_plots:
            self._section_plots[file_name].release()
            del self._section_plots[file_name]
            if self._enabled:
                self.update_limits()

    # ----------------------------------------------------------------------
    def update_plots(self):
        x_min, x_max = self._get_fit_range()

        for file_name, plot_item in self._section_plots.items():
            x, y = self.data_pool.get_roi_plot(file_name, self.my_id)
            plot_item.update_plot(x, y, x_min, x_max)

    # ----------------------------------------------------------------------
    def update_limits(self):
        if self._enabled:
            for widget in self._section_ranger:
                widget.refresh_view()

    # ----------------------------------------------------------------------
    def _normalize_plots(self, state):
        self._normalized = state
        x_min, x_max = self._get_fit_range()
        for plot in self._section_plots.values():
            plot.normalize_plot(state, x_min, x_max)

    # ----------------------------------------------------------------------
    def _set_new_section_axis(self, axis):
        self.data_pool.set_section_axis(self.my_id, axis)
        self.update_roi.emit(self.my_id)
        for widget in self._section_ranger:
            widget.setup_view()

        self.update_plots()

    # ----------------------------------------------------------------------
    def units_changed(self):

        if not self._enabled:
            return

        self._block_signals(True)

        self._ui.cb_section_axis.clear()
        self._ui.cb_section_axis.addItems(self.data_pool.get_file_axes(self._parent.get_current_file()))
        self._ui.cb_section_axis.setCurrentIndex(self.data_pool.get_roi_param(self.my_id, 'axis_0'))

        for widget in self._section_ranger:
            widget.setup_view()

        self._block_signals(False)

        self.update_plots()

    # ----------------------------------------------------------------------
    def _block_signals(self, flag):
        self._ui.cb_section_axis.blockSignals(flag)
        self.data_pool.blockSignals(flag)

    # ----------------------------------------------------------------------
    def _mouse_moved(self, pos):
        if self._main_plot.sceneBoundingRect().contains(pos):
            pos = self._main_plot.vb.mapSceneToView(pos)

            current_file = self.get_current_file()
            if current_file is not None:
                axis_name = self.data_pool.get_file_axes(current_file)[self.data_pool.get_roi_param(self.my_id, 'axis_0')]

                self._cross.setPos(axis_name, pos.x(), pos.y())
                self._ruler.mouseMoved(pos.x(), pos.y())

                self._ui.lb_status.setText('{}: {:3f}, Value: {:.3f}'.format(axis_name, pos.x(), pos.y()))

    # ----------------------------------------------------------------------
    def _mouse_clicked(self, event):
        """
        """
        if event.double():
            try:
                self._main_plot.autoRange()
            except:
                pass

        pos = event.scenePos()
        if self._main_plot.sceneBoundingRect().contains(pos):
            pos = self._main_plot.vb.mapSceneToView(pos)
            self._ruler.mouseClicked(pos.x(), pos.y())

            for _, scan_plot in self._section_plots.items():
                scan_plot.show_tool_tip(False)

            closest_plot = self.closest_plot(pos)
            if closest_plot:
                closest_plot.show_tool_tip(True, pos)

    # ----------------------------------------------------------------------
    def _new_range(self):
        if self._ui.rb_range_all.isChecked():
            x_min, x_max = self._main_plot.getAxis('bottom').range
            self._ui.dsp_cut_from.setValue(x_min)
            self._ui.dsp_cut_to.setValue(x_max)
        else:
            x_min, x_max = self._ui.dsp_cut_from.value(), self._ui.dsp_cut_to.value()

        for _, scan_plot in self._section_plots.items():
            scan_plot.update_fits(x_min, x_max)

    # ----------------------------------------------------------------------
    def _cut_range(self, selection):
        fit_all = selection.objectName() == 'rb_range_all'
        self._fit_all = fit_all
        self._ui.dsp_cut_from.setEnabled(not fit_all)
        self._ui.dsp_cut_to.setEnabled(not fit_all)
        self.range_line_from.setMovable(not fit_all)
        self.range_line_to.setMovable(not fit_all)
        self._new_range()

    # ----------------------------------------------------------------------
    def _check_cut(self, type, value):
        if type == 'from':
            self.range_line_from.setValue(value)

            to = self._ui.dsp_cut_to.value()
            if to < value:
                self._ui.dsp_cut_to.setValue(value)
                self.range_line_to.setValue(value)

        elif type == 'to':
            self.range_line_to.setValue(value)

            start = self._ui.dsp_cut_from.value()
            if start > value:
                self._ui.dsp_cut_from.setValue(value)
                self.range_line_from.setValue(value)

        self._new_range()

    # ----------------------------------------------------------------------
    def closest_plot(self, pos, threshold=0.05):
        closest_plot = None
        min_distance = self._main_plot.viewRange()[1][1] - self._main_plot.viewRange()[1][0]

        for _, plot in self._section_plots.items():
            y_distance = plot.distance_y(pos)
            y_range = plot.range_y()
            if y_distance < min_distance and (y_distance / y_range < threshold):
                closest_plot = plot
                min_distance = y_distance

        return closest_plot

    # ----------------------------------------------------------------------
    def _get_fit_range(self):
        if self._ui.rb_range_all.isChecked():
            [[x_min, x_max], [_, _]] = self._main_plot.viewRange()
        else:
            x_max = self._ui.dsp_cut_to.value()
            x_min = self._ui.dsp_cut_from.value()

        return x_min, x_max

    # ----------------------------------------------------------------------
    def _make_fit(self, function):
        if function not in self._enabled_fits:
            self._enabled_fits.append(function)
            x_min, x_max = self._get_fit_range()
            for plot in self._section_plots.values():
                plot.make_fit(function, x_min, x_max)
        else:
            self._enabled_fits.remove(function)
            for plot in self._section_plots.values():
                plot.remove_fit(function)

    # ----------------------------------------------------------------------
    def _delete_fits(self):
        for plot in self._section_plots.values():
            plot.delete_fits()

    # ----------------------------------------------------------------------
    def _axis_scale(self):
        self._main_plot.setLogMode(self._log_x.isChecked(), self._log_y.isChecked())

    # ----------------------------------------------------------------------
    def _show_all(self):
        minimum_x, maximum_x = +np.Inf, -np.Inf
        minimum_y, maximum_y = +np.Inf, -np.Inf

        for plot in self._section_plots.values():
            x_min, x_max, y_min, y_max = plot.get_range()
            minimum_x = min(minimum_x, x_min)
            maximum_x = max(maximum_x, x_max)
            minimum_y = min(minimum_y, y_min)
            maximum_y = max(maximum_y, y_max)

        try:
            self._main_plot.getViewBox().setRange(QtCore.QRectF(minimum_x, minimum_y,
                                                                maximum_x - minimum_x, maximum_y - minimum_y))
        except:
            pass

    # ----------------------------------------------------------------------
    def _save(self, type):
        default_name = self._parent.current_folder() + '/roi_{}'.format(self.data_pool.get_roi_index(self.my_id))
        if type == 'image':
            file_name, format = QtWidgets.QFileDialog.getSaveFileName(self, 'Save as', default_name,
                 'Windows Bitmap (*.bmp);; Joint Photographic Experts Group (*.jpg);; Portable Network Graphics (*.png);; Portable Pixmap (*.ppm); X11 Bitmap (*.xbm);; X11 Pixmap (*.xpm)')
            if file_name:
                file_name += format.split('*')[1].strip('()')
                pix = QtGui.QPixmap(self._ui.gv_main.size())
                self._ui.gv_main.render(pix)
                pix.save(file_name)
        else:
            save_name, file_type = QtWidgets.QFileDialog.getSaveFileName(self, 'Save as', default_name,
                                                                         'Text file (*.txt)')

            file_type = re.compile("\((.+)\)").search(file_type).group(1).strip('*')
            if save_name:
                dir_name = os.path.dirname(save_name)
                base_name = os.path.basename(save_name)

                for file_name, plot in self._section_plots.items():
                    header, data = plot.get_data_to_save()
                    header[0] = self.data_pool.get_roi_axis_name(self.data_pool.get_roi_index(self.my_id), file_name)
                    self.data_pool.save_roi_to_file(file_type,
                                                    os.path.join(dir_name, file_name + "_" + base_name + file_type),
                                                    header, data)

    # ----------------------------------------------------------------------
    def _copy_to_clipboard(self, type):
        if type == 'image':
            QtWidgets.qApp.clipboard().setPixmap(self._ui.gv_main.grab())
        else:
            pass

    # ----------------------------------------------------------------------
    def _print_plot(self):
        dialog = QtPrintSupport.QPrintPreviewDialog()
        dialog.paintRequested.connect(self.handlePaintRequest)
        dialog.exec_()

    # ----------------------------------------------------------------------
    def handlePaintRequest(self, printer):
        self._ui.gv_main.render(QtGui.QPainter(printer))

    # ----------------------------------------------------------------------
    def _init_tool_bar(self):
        toolbar = QtWidgets.QToolBar("Main toolbar", self)
        # toolbar.setObjectName('main_tool_bar')

        label = QtWidgets.QLabel("Export image: ", self)
        toolbar.addWidget(label)

        print_action = toolbar.addAction(QtGui.QIcon(QtGui.QPixmap(":/icon/print.png")), "Print")
        print_action.triggered.connect(self._print_plot)

        action = toolbar.addAction(QtGui.QIcon(QtGui.QPixmap(":/icon/copy.png")), "Copy to Clipboard")
        action.triggered.connect(lambda: self._copy_to_clipboard('image'))

        action = toolbar.addAction(QtGui.QIcon(QtGui.QPixmap(":/icon/save.png")), "Save")
        action.triggered.connect(lambda: self._save('image'))

        toolbar.addSeparator()

        label = QtWidgets.QLabel("Export data: ", self)
        toolbar.addWidget(label)

        action = toolbar.addAction(QtGui.QIcon(QtGui.QPixmap(":/icon/copy.png")), "Copy to Clipboard")
        action.triggered.connect(lambda: self._copy_to_clipboard('data'))

        action = toolbar.addAction(QtGui.QIcon(QtGui.QPixmap(":/icon/save.png")), "Save")
        action.triggered.connect(lambda: self._save('data'))

        toolbar.addSeparator()

        action_grid = toolbar.addAction(QtGui.QIcon(QtGui.QPixmap(":/icon/grid.png")), "Grid")
        action_grid.setCheckable(True)
        action_grid.setChecked(True)
        action_grid.triggered.connect(lambda flag: self._main_plot.showGrid(flag, flag, alpha=0.25))

        action_cross = toolbar.addAction(QtGui.QIcon(QtGui.QPixmap(":/icon/crosshair.png")), "Crosshair Cursor")
        action_cross.setCheckable(True)
        action_cross.setChecked(False)
        action_cross.triggered.connect(lambda state: self._cross.setVisible(state))

        action_ruler = toolbar.addAction(QtGui.QIcon(QtGui.QPixmap(":/icon/ruler.png")), "Distance Measurement")
        action_ruler.setCheckable(True)
        action_ruler.setChecked(False)
        action_ruler.triggered.connect(lambda state: self._ruler.setEnabled(state))

        toolbar.addSeparator()

        label = QtWidgets.QLabel("Axes: ", self)
        toolbar.addWidget(label)

        button = QtWidgets.QToolButton(self)
        button.setText("Y")

        menu = QtWidgets.QMenu(button)

        normalize = QtWidgets.QAction("Normalize", self)
        normalize.setCheckable(True)
        normalize.setChecked(False)
        normalize.triggered.connect(lambda state: self._normalize_plots(state))
        menu.addAction(normalize)

        group = QtWidgets.QActionGroup(self)
        group.setExclusive(True)

        self._lin_y = QtWidgets.QAction("Linear", self)
        self._lin_y.setCheckable(True)
        self._lin_y.setChecked(True)
        self._lin_y.triggered.connect(self._axis_scale)
        group.addAction(self._lin_y)
        menu.addAction(self._lin_y)

        self._log_y = QtWidgets.QAction("Log", self)
        self._log_y.setCheckable(True)
        self._log_y.triggered.connect(self._axis_scale)
        group.addAction(self._log_y)
        menu.addAction(self._log_y)

        button.setMenu(menu)
        button.setPopupMode(QtWidgets.QToolButton.InstantPopup)
        toolbar.addWidget(button)

        button = QtWidgets.QToolButton(self)
        button.setText("X")

        menu = QtWidgets.QMenu(button)

        group = QtWidgets.QActionGroup(self)
        group.setExclusive(True)

        self._lin_x = QtWidgets.QAction("Linear", self)
        self._lin_x.setCheckable(True)
        self._lin_x.setChecked(True)
        self._lin_x.triggered.connect(self._axis_scale)
        group.addAction(self._lin_x)
        menu.addAction(self._lin_x)

        self._log_x = QtWidgets.QAction("Log", self)
        self._log_x.setCheckable(True)
        self._log_x.triggered.connect(self._axis_scale)
        group.addAction(self._log_x)
        menu.addAction(self._log_x)

        button.setMenu(menu)
        button.setPopupMode(QtWidgets.QToolButton.InstantPopup)
        toolbar.addWidget(button)

        auto_zoom = toolbar.addAction("Auto zoom")
        auto_zoom.triggered.connect(self._show_all)

        toolbar.addSeparator()

        button = QtWidgets.QToolButton(self)
        button.setText("Fit")
        self._make_fit_menu(button)
        toolbar.addWidget(button)

        toolbar.addSeparator()

        action_legend = toolbar.addAction("Legend")
        action_legend.setCheckable(True)
        action_legend.setChecked(False)
        action_legend.toggled.connect(lambda state: self._legend.setVisible(state))
        action_legend.setToolTip("Show Legend")

        self._ui.v_layout_2.insertWidget(0, toolbar, 0)

    # ----------------------------------------------------------------------
    def _make_save_menu(self, button):
        menu = QtWidgets.QMenu(parent=button)
        action = menu.addAction("As Image")
        action.triggered.connect(self.saveAsImage)
        action = menu.addAction("As Text")
        action.triggered.connect(self.saveAsText)
        button.setMenu(menu)
        button.setPopupMode(QtWidgets.QToolButton.InstantPopup)

    # ----------------------------------------------------------------------
    def _make_fit_menu(self, button):
        menu = QtWidgets.QMenu(parent=button)
        action = menu.addAction("Linear")
        action.setCheckable(True)
        action.triggered.connect(lambda: self._make_fit("linear"))
        action = menu.addAction("Gaussian")
        action.setCheckable(True)
        action.triggered.connect(lambda: self._make_fit("gaussian"))
        action = menu.addAction("Lorentzian")
        action.setCheckable(True)
        action.triggered.connect(lambda: self._make_fit("lorentzian"))
        action = menu.addAction("FWHM")
        action.setCheckable(True)
        action.triggered.connect(lambda: self._make_fit("fwhm"))
        menu.addSeparator()
        action = menu.addAction("Delete All")
        action.triggered.connect(self._delete_fits)
        button.setMenu(menu)
        button.setPopupMode(QtWidgets.QToolButton.InstantPopup)