# Created by matveyev at 24.03.2021

import pyqtgraph as pg
import numpy as np

from PyQt5 import QtWidgets, QtCore, QtGui
from silx.gui.plot.PlotWindow import Plot2D

from petra_viewer.utils.image_marker import ImageMarker
from petra_viewer.gui.view_2d_ui import Ui_View2D


class View2d(QtWidgets.QWidget):

    # ----------------------------------------------------------------------
    def __init__(self, frame_viewer, type, data_pool):
        """
        """
        super(View2d, self).__init__()
        self._ui = Ui_View2D()
        self._ui.setupUi(self)

        self._frame_viewer = frame_viewer
        self._type = type
        self.data_pool = data_pool

        self._my_files = []
        self.current_file = None
        self.previous_file = None

        self._tb_files = QtWidgets.QTabBar(self)
        self._tb_files.setObjectName("tb_main")
        self._tb_files.setTabsClosable(True)
        self._tb_files.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self._tb_files.customContextMenuRequested.connect(self._move_tab_menu)
        self._ui.v_layout.insertWidget(0, self._tb_files, 0)

        self._rois = {}

        self._tb_files.tabCloseRequested.connect(self._close_file)
        self._tb_files.currentChanged.connect(self._switch_file)

    # ----------------------------------------------------------------------
    def block_signals(self, flag):
        self._tb_files.blockSignals(flag)

    # ----------------------------------------------------------------------
    def _move_tab_menu(self, pos):

        if self._type == 'main' and len(self._my_files) == 1:
            return

        menu = QtWidgets.QMenu()
        if self._type == 'main':
            action = QtWidgets.QAction('Move to compare')
        else:
            action = QtWidgets.QAction('Move to main')

        menu.addAction(action)

        action = menu.exec_(self.mapToGlobal(pos))

        if action:
            index = self._tb_files.currentIndex()
            self._frame_viewer.add_file(self._my_files[index], self._type, self._type == 'main')
            del self._my_files[index]
            self.current_file = None
            self._tb_files.removeTab(index)

            if len(self._my_files) == 0:
                self.hide()

    # ----------------------------------------------------------------------
    def new_view_box(self, view_box):
        pass

    # ----------------------------------------------------------------------
    def add_file(self, file_name):

        self.block_signals(True)

        self.previous_file = self.current_file

        if self._type != 'main' and len(self._my_files) > 0:
            while len(self._my_files) > 0:
                self._frame_viewer.add_file(self._my_files[0], self._type)
                del self._my_files[0]
                self.current_file = None
                self._tb_files.removeTab(0)

        new_index = self._tb_files.count()
        self._my_files.insert(new_index, file_name)
        self._tb_files.insertTab(new_index, '{}'.format(file_name))
        self._tb_files.setCurrentIndex(new_index)
        self.current_file = file_name

        self.show()

        self.block_signals(False)

    # ----------------------------------------------------------------------
    def new_lookup_table(self):
        pass

    # ----------------------------------------------------------------------
    def new_levels(self):
        pass

    # ----------------------------------------------------------------------
    def _close_file(self, index):
        self.plot_2d.clear()
        file_to_remove = self._my_files[index]
        del self._my_files[index]
        self.current_file = None
        self._tb_files.removeTab(index)
        self.data_pool.remove_file(file_to_remove)

        if len(self._my_files) == 0 and self._type != 'main':
            self.hide()

    # ----------------------------------------------------------------------
    def file_closed_by_pool(self, file_name):
        if file_name in self._my_files:
            self.plot_2d.clear()
            index = self._my_files.index(file_name)
            del self._my_files[index]
            if self.current_file == file_name:
                self.current_file = None
            self._tb_files.removeTab(index)

            if len(self._my_files) == 0 and self._type != 'main':
                self.hide()

    # ----------------------------------------------------------------------
    def add_roi(self,idx):
        pass

    # ----------------------------------------------------------------------
    def delete_roi(self, idx):
        pass

    # ----------------------------------------------------------------------
    def roi_changed(self, roi_ind):
        pass

    # ----------------------------------------------------------------------
    def new_axes(self, labels):
        pass

    # ----------------------------------------------------------------------
    def get_current_rect(self):
        return [0, 0, 10, 10]

    # ----------------------------------------------------------------------
    def get_files_list(self):
        return self._my_files

    # ----------------------------------------------------------------------
    def _switch_file(self, index):

        self.previous_file = self.current_file

        if index > -1:
            self.current_file = self._my_files[index]
        else:
            self.current_file = None

        if self._type == 'main':
            self._frame_viewer.new_main_file()

    # ----------------------------------------------------------------------
    def clear_view(self):
        self.plot_2d.clear()

    # ----------------------------------------------------------------------
    def update_image(self):
        if self.current_file is None:
            self.plot_2d.clear()
            return None, None

        data_to_display, pos = self.data_pool.get_2d_picture(self.current_file)

        if data_to_display is None:
            self.plot_2d.clear()
            return None, None

        if self._frame_viewer.level_mode == 'log':
            data_to_display = np.log(data_to_display + 1)
        elif self._frame_viewer.level_mode == 'sqrt':
            data_to_display = np.sqrt(data_to_display + 1)

        return data_to_display, pos


# ----------------------------------------------------------------------
class ViewPyQt(View2d):

    roi_moved = QtCore.pyqtSignal(int)

    def __init__(self, frame_viewer, type, data_pool):
        super(ViewPyQt, self).__init__(frame_viewer, type, data_pool)

        self.gv_main = pg.GraphicsView(self)
        self.gv_main.setStyleSheet("")
        self.gv_main.setBackground('w')
        self.gv_main.setObjectName("gvMain")
        self._ui.v_layout.addWidget(self.gv_main)

        self._main_plot = pg.PlotItem()
        self._main_plot.showAxis('left', False)
        self._main_plot.showAxis('bottom', False)
        self._main_plot.setMenuEnabled(False)
        self._main_plot.getViewBox().setMouseMode(pg.ViewBox.RectMode)

        self.gv_main.setCentralItem(self._main_plot)
        self.gv_main.setRenderHints(self.gv_main.renderHints())

        self.plot_2d = pg.ImageItem()
        self._main_plot.addItem(self.plot_2d)

        self._center_cross = ImageMarker(0, 0, self._main_plot)

        self._main_plot.scene().sigMouseMoved.connect(self._mouse_moved)
        self._main_plot.scene().sigMouseClicked.connect(self._mouse_clicked)
        self._main_plot.getViewBox().sigRangeChangedManually.connect(self._range_changed)
        self._main_plot_signals_connected = True

    # ----------------------------------------------------------------------
    def apply_setting(self, setting, state):

        if setting == 'axes':
            self._main_plot.showAxis('left', state)
            self._main_plot.showAxis('bottom', state)

        elif setting == 'titles':
            self._main_plot.showLabel('left', state)
            self._main_plot.showLabel('bottom', state)

        elif setting == 'grid':
            self._main_plot.showGrid(state, state, alpha=0.25)

        elif setting == 'cross':
            self._center_cross.setVisible(state)

        elif setting == 'aspect':
            self._main_plot.getViewBox().setAspectLocked(state)

    # ----------------------------------------------------------------------
    def _range_changed(self):
        self._frame_viewer.new_view_box(self._type, self._main_plot.getViewBox().viewRect())

    # ----------------------------------------------------------------------
    def get_current_rect(self):
        rect = self._main_plot.getViewBox().viewRect()

        return [rect.x(), rect.y(), rect.x() + rect.width(), rect.y() + rect.height()]

    # ----------------------------------------------------------------------
    def new_view_box(self, view_rect):
        self._main_plot.getViewBox().setRange(view_rect)

    # ----------------------------------------------------------------------
    def new_lookup_table(self):
        if self.plot_2d.image is not None:
           self.plot_2d.setLookupTable(self._frame_viewer.hist.item.getLookupTable(self.plot_2d.image))

    # ----------------------------------------------------------------------
    def new_levels(self):
        self.plot_2d.setLevels(self._frame_viewer.hist.item.getLevels())

    # ----------------------------------------------------------------------
    def add_roi(self,idx):
        roi_id = self.data_pool.get_roi_index(idx)
        self._rois[idx] = (pg.RectROI([0, 0], [1, 1], pen=(0, 9)),
                           pg.TextItem(text='ROI {}'.format(roi_id), color=(255, 0, 0)),
                           idx)

        self._rois[idx][1].setFont(QtGui.QFont("Arial", 10))
        self._rois[idx][0].sigRegionChangeFinished.connect(lambda rect, id=idx: self._roi_changed(id, rect))
        self._main_plot.addItem(self._rois[idx][0])
        self._main_plot.addItem(self._rois[idx][1])

    # ----------------------------------------------------------------------
    def delete_roi(self, idx):

        self._main_plot.removeItem(self._rois[idx][0])
        self._main_plot.removeItem(self._rois[idx][1])
        del self._rois[idx]

        for _, label, my_id in self._rois.values():
            label.setText('ROI {}'.format(self.data_pool.get_roi_index(my_id)))

    # ----------------------------------------------------------------------
    def roi_changed(self, roi_ind):

        if self.current_file is None:
            self._rois[roi_ind][0].setVisible(False)
            self._rois[roi_ind][1].setVisible(False)
            return

        if self.data_pool.get_roi_param(self._rois[roi_ind][2], 'dimensions') != \
                self.data_pool.get_file_dimension(self.current_file):
            self._rois[roi_ind][0].setVisible(False)
            self._rois[roi_ind][1].setVisible(False)
            return

        self._rois[roi_ind][0].setVisible(True)
        self._rois[roi_ind][1].setVisible(True)

        self._rois[roi_ind][0].sigRegionChangeFinished.disconnect()

        current_axes = self._frame_viewer.get_current_axes()

        x_pos, y_pos = 0, 0
        x_width, y_width = 1, 1

        axes_limits = self.data_pool.get_all_axes_limits()

        if current_axes['x'] == self.data_pool.get_roi_param(self._rois[roi_ind][2], 'axis_0'):
            x_pos = axes_limits[current_axes['x']][0]
            x_width = axes_limits[current_axes['x']][1] - axes_limits[current_axes['x']][0]
        else:
            axis = 1
            while axis < 100:
                if current_axes['x'] == self.data_pool.get_roi_param(self._rois[roi_ind][2], f'axis_{axis}'):
                    x_pos = self.data_pool.get_roi_param(self._rois[roi_ind][2], f'axis_{axis}_pos')
                    x_width = self.data_pool.get_roi_param(self._rois[roi_ind][2], f'axis_{axis}_width')
                    break
                axis += 1

        if current_axes['y'] == self.data_pool.get_roi_param(self._rois[roi_ind][2], 'axis_0'):
            y_pos = axes_limits[current_axes['y']][0]
            y_width = axes_limits[current_axes['y']][1] - axes_limits[current_axes['y']][0]
        else:
            axis = 1
            while axis < 100:
                if current_axes['y'] == self.data_pool.get_roi_param(self._rois[roi_ind][2], f'axis_{axis}'):
                    y_pos = self.data_pool.get_roi_param(self._rois[roi_ind][2], f'axis_{axis}_pos')
                    y_width = self.data_pool.get_roi_param(self._rois[roi_ind][2], f'axis_{axis}_width')
                    break
                axis += 1

        self._rois[roi_ind][0].setPos([x_pos, y_pos])
        self._rois[roi_ind][0].setSize([x_width, y_width])
        self._rois[roi_ind][1].setPos(x_pos + x_width, y_pos + y_width)
        self._rois[roi_ind][0].sigRegionChangeFinished.connect(lambda rect, idx=roi_ind: self._roi_changed(idx, rect))

    # ----------------------------------------------------------------------
    def _roi_changed(self, roi_ind, rect):

        current_axes = self._frame_viewer.get_current_axes()

        pos, size = rect.pos(), rect.size()

        x_axis = self.data_pool.get_roi_axis(self._rois[roi_ind][2], current_axes['x'])
        accepted_x_pos = self.data_pool.roi_parameter_changed(self._rois[roi_ind][2], x_axis, 'pos', pos.x())
        accepted_x_width = self.data_pool.roi_parameter_changed(self._rois[roi_ind][2], x_axis, 'width', size.x())

        y_axis = self.data_pool.get_roi_axis(self._rois[roi_ind][2], current_axes['y'])
        accepted_y_pos = self.data_pool.roi_parameter_changed(self._rois[roi_ind][2], y_axis, 'pos', pos.y())
        accepted_y_width = self.data_pool.roi_parameter_changed(self._rois[roi_ind][2], y_axis, 'width', size.y())

        self.roi_moved.emit(self._rois[roi_ind][2])

        self._rois[roi_ind][0].sigRegionChangeFinished.disconnect()
        self._rois[roi_ind][0].setPos([accepted_x_pos, accepted_y_pos])
        self._rois[roi_ind][0].setSize([accepted_x_width, accepted_y_width])

        self._rois[roi_ind][1].setPos(accepted_x_pos + accepted_x_width, accepted_y_pos + accepted_y_width)
        self._rois[roi_ind][0].sigRegionChangeFinished.connect(lambda rect, id=roi_ind: self._roi_changed(roi_ind, rect))

    # ----------------------------------------------------------------------
    def new_axes(self, labels):

        self._main_plot.setLabel('bottom', labels[0])
        self._main_plot.setLabel('left', labels[1])

        for idx in range(len(self._rois)):
            self.roi_changed(idx)

    # ----------------------------------------------------------------------
    def _mouse_moved(self, pos):

        if self._main_plot.sceneBoundingRect().contains(pos):
            pos = self._main_plot.vb.mapSceneToView(pos)

            self._center_cross.setPos(pos)

            if self.current_file is None:
                return

            try:
                current_axes = self._frame_viewer.get_current_axes()

                x_value = self.data_pool.get_value_for_frame(self.current_file, current_axes['x'], int(pos.x()))
                y_value = self.data_pool.get_value_for_frame(self.current_file, current_axes['y'], int(pos.y()))

            except:
                x_value = ''
                y_value = ''

            self._frame_viewer.new_coordinate(self._type, x_value, y_value, pos)

    # ----------------------------------------------------------------------
    def move_marker(self, pos):
        self._center_cross.setPos(pos)

    # ----------------------------------------------------------------------
    def _mouse_clicked(self, event):
        """
        """
        if event.double():
            try:
                self._main_plot.autoRange()
                self._frame_viewer.new_view_box(self._type, self._main_plot.getViewBox().viewRect())
            except:
                pass

    # ----------------------------------------------------------------------
    def clear_view(self):

        super(ViewPyQt, self).clear_view()

        for roi in self._rois:
            roi[0].setVisible(False)
            roi[1].setVisible(False)

    # ----------------------------------------------------------------------
    def update_image(self):

        data_to_display, pos = super(ViewPyQt, self).update_image()
        if data_to_display is not None:
            if self._frame_viewer.hist_mode == 'selected' and self._frame_viewer.auto_levels:
                self.plot_2d.setImage(data_to_display, autoLevels=True)
            else:
                self.plot_2d.setImage(data_to_display, levels=self._frame_viewer.get_levels())

            self.plot_2d.setRect(pos)
            for ind in range(len(self._rois)):
                self.roi_changed(ind)


# ----------------------------------------------------------------------
class ViewSilx(View2d):

    def __init__(self, frame_viewer, type, data_pool):

        super(ViewSilx, self).__init__(frame_viewer, type, data_pool)

        self.plot_2d = Plot2D(self)
        self.plot_2d.setObjectName("plot_2d")
        self._ui.v_layout.addWidget(self.plot_2d)

    # ----------------------------------------------------------------------
    def new_axes(self, labels):
        self.plot_2d.getXAxis().setLabel(labels[0])
        self.plot_2d.getYAxis().setLabel(labels[1])

    # ----------------------------------------------------------------------
    def update_image(self):
        data_to_display, x, y = super(ViewSilx, self).update_image()
        if data_to_display is not None:
            sections = self.data_pool.get_section(self.current_file)
            origen = [s['min'] for s in sections if s['axis'] == 'X']
            origen += [s['min'] for s in sections if s['axis'] == 'Y']
            self.plot_2d.addImage(np.transpose(data_to_display), replace=True, origin=origen)
