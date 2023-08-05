# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uis/array_selector.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ArraySelector(object):
    def setupUi(self, ArraySelector):
        ArraySelector.setObjectName("ArraySelector")
        ArraySelector.resize(812, 45)
        self.horizontalLayout = QtWidgets.QHBoxLayout(ArraySelector)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.sp_value_from = QtWidgets.QDoubleSpinBox(ArraySelector)
        self.sp_value_from.setDecimals(0)
        self.sp_value_from.setObjectName("sp_value_from")
        self.horizontalLayout.addWidget(self.sp_value_from)
        self.lb_to = QtWidgets.QLabel(ArraySelector)
        self.lb_to.setObjectName("lb_to")
        self.horizontalLayout.addWidget(self.lb_to)
        self.sp_value_to = QtWidgets.QDoubleSpinBox(ArraySelector)
        self.sp_value_to.setDecimals(0)
        self.sp_value_to.setObjectName("sp_value_to")
        self.horizontalLayout.addWidget(self.sp_value_to)
        self.sl_range = RangeSlider(ArraySelector)
        self.sl_range.setOrientation(QtCore.Qt.Horizontal)
        self.sl_range.setObjectName("sl_range")
        self.horizontalLayout.addWidget(self.sl_range)
        self.sl_frame = QtWidgets.QSlider(ArraySelector)
        self.sl_frame.setMaximum(5)
        self.sl_frame.setOrientation(QtCore.Qt.Horizontal)
        self.sl_frame.setObjectName("sl_frame")
        self.horizontalLayout.addWidget(self.sl_frame)
        self.but_first = QtWidgets.QPushButton(ArraySelector)
        self.but_first.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icon/first.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.but_first.setIcon(icon)
        self.but_first.setIconSize(QtCore.QSize(15, 15))
        self.but_first.setObjectName("but_first")
        self.horizontalLayout.addWidget(self.but_first)
        self.but_previous = QtWidgets.QPushButton(ArraySelector)
        self.but_previous.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icon/previous.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.but_previous.setIcon(icon1)
        self.but_previous.setIconSize(QtCore.QSize(15, 15))
        self.but_previous.setObjectName("but_previous")
        self.horizontalLayout.addWidget(self.but_previous)
        self.sp_step = QtWidgets.QDoubleSpinBox(ArraySelector)
        self.sp_step.setDecimals(0)
        self.sp_step.setObjectName("sp_step")
        self.horizontalLayout.addWidget(self.sp_step)
        self.but_next = QtWidgets.QPushButton(ArraySelector)
        self.but_next.setText("")
        icon2 = QtGui.QIcon()
        icon2.addPixmap(QtGui.QPixmap(":/icon/next.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.but_next.setIcon(icon2)
        self.but_next.setIconSize(QtCore.QSize(15, 15))
        self.but_next.setObjectName("but_next")
        self.horizontalLayout.addWidget(self.but_next)
        self.but_last = QtWidgets.QPushButton(ArraySelector)
        self.but_last.setText("")
        icon3 = QtGui.QIcon()
        icon3.addPixmap(QtGui.QPixmap(":/icon/last.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.but_last.setIcon(icon3)
        self.but_last.setIconSize(QtCore.QSize(15, 15))
        self.but_last.setObjectName("but_last")
        self.horizontalLayout.addWidget(self.but_last)
        self.cmd_show_all = QtWidgets.QPushButton(ArraySelector)
        self.cmd_show_all.setObjectName("cmd_show_all")
        self.horizontalLayout.addWidget(self.cmd_show_all)
        self.horizontalLayout.setStretch(3, 1)
        self.horizontalLayout.setStretch(4, 1)

        self.retranslateUi(ArraySelector)
        QtCore.QMetaObject.connectSlotsByName(ArraySelector)

    def retranslateUi(self, ArraySelector):
        _translate = QtCore.QCoreApplication.translate
        ArraySelector.setWindowTitle(_translate("ArraySelector", "Form"))
        self.lb_to.setText(_translate("ArraySelector", "-"))
        self.cmd_show_all.setText(_translate("ArraySelector", "Show all"))

from petra_viewer.utils.range_slider import RangeSlider
import petra_viewer.gui.icons_rc
