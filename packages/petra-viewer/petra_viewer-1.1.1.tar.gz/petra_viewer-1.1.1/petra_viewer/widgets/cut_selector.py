# Created by matveyev at 04.08.2021

from PyQt5 import QtWidgets, QtCore
import logging

from petra_viewer.utils.utils import refresh_combo_box
from petra_viewer.widgets.array_selector import ArraySelector
from petra_viewer.main_window import APP_NAME
from petra_viewer.gui.cut_selector_ui import Ui_CutSelector


logger = logging.getLogger(APP_NAME)


class CutSelector(QtWidgets.QWidget):

    new_units = QtCore.pyqtSignal(list)

    def __init__(self, parent):
        """
        """
        super(CutSelector, self).__init__()
        self._ui = Ui_CutSelector()
        self._ui.setupUi(self)

        self._my_dims = None
        self._data_pool = None

        self._frame_viewer = parent

        self._x_buttons_group = QtWidgets.QButtonGroup()
        self._x_buttons_group.setExclusive(True)

        self._y_buttons_group = QtWidgets.QButtonGroup()
        self._y_buttons_group.setExclusive(True)

        self._z_buttons_group = QtWidgets.QButtonGroup()
        self._z_buttons_group.setExclusive(True)

        self._array_selectors = []
        self._integration_boxes = []

        self._units_selectors = {}

        self._x_buttons = []
        self._y_buttons = []
        self._z_buttons = []

        self._axes_labels = []

        self._ui.cut_selectors.setLayout(QtWidgets.QGridLayout(self._ui.cut_selectors))
        self._ui.cut_selectors.layout().setContentsMargins(0, 0, 0, 0)

        self._last_axes = {'X': -1, 'Y': -1, 'Z': -1}

    # ----------------------------------------------------------------------
    def set_axes(self, axes):
        main_file = self._frame_viewer.current_file()

        if self._data_pool.get_file_dimension(main_file) != len(axes):
            return

        compatible = True
        for ind, axis in enumerate(axes):
            compatible *= axis in self._data_pool.get_possible_axis_units(self._frame_viewer.current_file(), ind)

        if not compatible:
            return False

        for ind, axis in enumerate(axes):
            if self._axes_labels[ind] != axis:
                if ind in self._units_selectors:
                    if not refresh_combo_box(self._units_selectors[ind], axis):
                        return False
                else:
                    return False

        return True

    # ----------------------------------------------------------------------
    def set_data_pool(self, data_pool):
        self._data_pool = data_pool

    # ----------------------------------------------------------------------
    def _new_layout(self):

        for axis in ['x', 'y', 'z']:
            for button in getattr(self, f'_{axis}_buttons_group').buttons():
                getattr(self, f'_{axis}_buttons_group').removeButton(button)

        layout = self._ui.cut_selectors.layout()
        for i in reversed(range(layout.count())):
            item = layout.itemAt(i)
            if item:
                w = layout.itemAt(i).widget()
                if w:
                    layout.removeWidget(w)
                    w.setVisible(False)

        label = QtWidgets.QLabel('Axis', self)
        label.setAlignment(QtCore.Qt.AlignHCenter)
        layout.addWidget(label, 0, 0)

        label = QtWidgets.QLabel('X', self)
        label.setAlignment(QtCore.Qt.AlignHCenter)
        layout.addWidget(label, 0, 1)

        label = QtWidgets.QLabel('Y', self)
        label.setAlignment(QtCore.Qt.AlignHCenter)
        layout.addWidget(label, 0, 2)

        label = QtWidgets.QLabel('Z', self)
        label.setAlignment(QtCore.Qt.AlignHCenter)
        layout.addWidget(label, 0, 3)

        label = QtWidgets.QLabel('', self)
        label.setAlignment(QtCore.Qt.AlignHCenter)
        layout.addWidget(label, 0, 4)
        layout.setColumnStretch(4, 1)

        label = QtWidgets.QLabel('Integration', self)
        label.setAlignment(QtCore.Qt.AlignHCenter)
        layout.addWidget(label, 0, 5)

    # ----------------------------------------------------------------------
    def refresh_selectors(self):
        self._new_layout()

        layout = self._ui.cut_selectors.layout()

        self._array_selectors = []
        self._integration_boxes = []
        self._units_selectors = {}
        self._x_buttons = []
        self._y_buttons = []

        self._axes_labels = []

        main_file = self._frame_viewer.current_file()

        if main_file is None:
            return

        for ind in range(self._data_pool.get_file_dimension(main_file)):
            possible_units = self._data_pool.get_possible_axis_units(self._frame_viewer.current_file(), ind)
            if len(possible_units) > 1:
                widget = QtWidgets.QComboBox(self)
                widget.addItems(list(possible_units.keys()))
                refresh_combo_box(widget, self._data_pool.get_axis_units(self._frame_viewer.current_file(), ind))
                self._axes_labels.append(widget.currentText())
                widget.currentTextChanged.connect(lambda text, id=ind: self._new_units(id, text))
                self._units_selectors[ind] = widget
            else:
                name = list(possible_units.keys())[0]
                widget = QtWidgets.QLabel(name, self)
                self._axes_labels.append(name)
                widget.setAlignment(QtCore.Qt.AlignHCenter | QtCore.Qt.AlignVCenter)
            layout.addWidget(widget, ind + 1, 0)

            rb = QtWidgets.QRadioButton(self)
            rb.clicked.connect(lambda state, ax='X', id=ind: self._new_axes(ax, id))
            layout.addWidget(rb, ind + 1, 1)
            self._x_buttons_group.addButton(rb)
            self._x_buttons.append(rb)

            rb = QtWidgets.QRadioButton(self)
            rb.clicked.connect(lambda state, ax='Y', id=ind: self._new_axes(ax, id))
            layout.addWidget(rb, ind + 1, 2)
            self._y_buttons_group.addButton(rb)
            self._y_buttons.append(rb)

            rb = QtWidgets.QRadioButton(self)
            rb.clicked.connect(lambda state, ax='Z', id=ind: self._new_axes(ax, id))
            layout.addWidget(rb, ind + 1, 3)
            self._z_buttons_group.addButton(rb)
            self._z_buttons.append(rb)

            selector = ArraySelector(ind, self, self._data_pool, self._frame_viewer)
            layout.addWidget(selector, ind + 1, 4)
            self._array_selectors.append(selector)

            chk_box = QtWidgets.QCheckBox(self)
            chk_box.clicked.connect(lambda state, id=ind: self._integration_changed(state, id))
            layout.addWidget(chk_box, ind + 1, 5)
            self._integration_boxes.append(chk_box)

    # ----------------------------------------------------------------------
    def _new_units(self, axis, units):
        self._axes_labels[axis] = units
        self._frame_viewer.set_new_units(axis, units,
                                         [self._axes_labels[self._last_axes[ind]] for ind in ['X', 'Y']])
        self._array_selectors[axis].units_changed()

    # ----------------------------------------------------------------------
    def new_range(self, ind):
        self._frame_viewer.new_cut(ind not in [self._last_axes['X'], self._last_axes['Y'], self._last_axes['Z']])

    # ----------------------------------------------------------------------
    def set_integration(self, ind):
        self._integration_boxes[ind].setChecked(True)
        self._integration_changed(True, ind)

    # ----------------------------------------------------------------------
    def _integration_changed(self, state, ind):
        self._array_selectors[ind].switch_integration_mode(state)
        self.new_range(ind)

    # ----------------------------------------------------------------------
    def _new_axes(self, axis, ind):

        self.block_signals(True)

        if axis == 'X' and ind in [self._last_axes['Y'], self._last_axes['Z']]:
            if ind == self._last_axes['Y']:
                self._y_buttons[self._last_axes['X']].setChecked(True)
            else:
                self._z_buttons[self._last_axes['X']].setChecked(True)

        elif axis == 'Y' and ind in [self._last_axes['X'], self._last_axes['Z']]:
            if ind == self._last_axes['X']:
                self._x_buttons[self._last_axes['Y']].setChecked(True)
            else:
                self._z_buttons[self._last_axes['Y']].setChecked(True)

        elif axis == 'Z' and ind in [self._last_axes['X'], self._last_axes['Y']]:
            if ind == self._last_axes['X']:
                self._x_buttons[self._last_axes['Z']].setChecked(True)
            else:
                self._y_buttons[self._last_axes['Z']].setChecked(True)


        labels = ['', '']
        for ind, (name, x_but, y_but, z_but, array_selector, integration_box) in \
                                                                        enumerate(zip(self._axes_labels,
                                                                                      self._x_buttons_group.buttons(),
                                                                                      self._y_buttons_group.buttons(),
                                                                                      self._z_buttons_group.buttons(),
                                                                                      self._array_selectors,
                                                                                      self._integration_boxes)):

            if x_but.isChecked() or y_but.isChecked():
                array_selector.switch_integration_mode(True)
                integration_box.setVisible(False)
                if x_but.isChecked():
                    self._last_axes['X'] = ind
                    labels[0] = name
                else:
                    self._last_axes['Y'] = ind
                    labels[1] = name
            else:
                if z_but.isChecked():
                    self._last_axes['Z'] = ind

                array_selector.switch_integration_mode(integration_box.isChecked())
                integration_box.setVisible(True)

        self.block_signals(False)

        self._frame_viewer.update_axes(labels)

    # ----------------------------------------------------------------------
    def set_limits(self, limits):
        for limit, selector in zip(limits, self._array_selectors):
            selector.setup_limits(limit)

    # ----------------------------------------------------------------------
    def get_current_selection(self):
        section = []
        for x_but, y_but, z_but, array_selector, integration_box in zip(self._x_buttons_group.buttons(),
                                                                        self._y_buttons_group.buttons(),
                                                                        self._z_buttons_group.buttons(),
                                                                        self._array_selectors,
                                                                        self._integration_boxes):

            if x_but.isChecked():
                axis = 'X'
            elif y_but.isChecked():
                axis = 'Y'
            elif z_but.isChecked():
                axis = 'Z'
            else:
                axis = ''

            f_min, f_max = array_selector.get_values()
            section.append({'axis': axis,
                            'integration': integration_box.isChecked(),
                            'min': f_min,
                            'max': f_max})

        return section

    # ----------------------------------------------------------------------
    def set_section(self, selections):
        """
        Set selection.
        """
        self.block_signals(True)

        self._last_axes = {}

        self._last_axes = {'X': -1, 'Y': -1, 'Z': -1}

        n_dims = len(selections)

        for ind, (x_but, y_but, z_but, array_selector, integration_box, section) in \
                                                                        enumerate(zip(self._x_buttons_group.buttons(),
                                                                                      self._y_buttons_group.buttons(),
                                                                                      self._z_buttons_group.buttons(),
                                                                                      self._array_selectors,
                                                                                      self._integration_boxes,
                                                                                      selections)):

            x_but.setChecked(section['axis'] == 'X')
            if n_dims > 1:
                y_but.setChecked(section['axis'] == 'Y')
                y_but.setEnabled(True)
            else:
                y_but.setEnabled(False)
            if n_dims > 2:
                z_but.setChecked(section['axis'] == 'Z')
                z_but.setEnabled(True)
            else:
                z_but.setEnabled(False)
            self._last_axes[section['axis']] = ind

            integration_box.setChecked(section['integration'])
            integration_box.setVisible(section['axis'] not in ['X', 'Y'])
            array_selector.set_section(section)

        self.block_signals(False)

    # ----------------------------------------------------------------------
    def block_signals(self, flag):

        for widget in self._x_buttons + self._y_buttons + self._z_buttons + \
                      self._array_selectors + self._integration_boxes + list(self._units_selectors.values()):
            widget.blockSignals(flag)

