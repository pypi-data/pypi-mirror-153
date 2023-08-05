# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uis/section_range.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_SectionRange(object):
    def setupUi(self, SectionRange):
        SectionRange.setObjectName("SectionRange")
        SectionRange.resize(176, 101)
        self.v_layout = QtWidgets.QVBoxLayout(SectionRange)
        self.v_layout.setObjectName("v_layout")
        self.lb_axis = QtWidgets.QLabel(SectionRange)
        font = QtGui.QFont()
        font.setPointSize(12)
        self.lb_axis.setFont(font)
        self.lb_axis.setObjectName("lb_axis")
        self.v_layout.addWidget(self.lb_axis)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_3 = QtWidgets.QLabel(SectionRange)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_3.addWidget(self.label_3)
        self.sb_pos = QtWidgets.QDoubleSpinBox(SectionRange)
        self.sb_pos.setObjectName("sb_pos")
        self.horizontalLayout_3.addWidget(self.sb_pos)
        self.v_layout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_2 = QtWidgets.QLabel(SectionRange)
        font = QtGui.QFont()
        font.setPointSize(10)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_4.addWidget(self.label_2)
        self.sb_width = QtWidgets.QDoubleSpinBox(SectionRange)
        self.sb_width.setMinimum(0.0)
        self.sb_width.setObjectName("sb_width")
        self.horizontalLayout_4.addWidget(self.sb_width)
        self.v_layout.addLayout(self.horizontalLayout_4)

        self.retranslateUi(SectionRange)
        QtCore.QMetaObject.connectSlotsByName(SectionRange)

    def retranslateUi(self, SectionRange):
        _translate = QtCore.QCoreApplication.translate
        SectionRange.setWindowTitle(_translate("SectionRange", "Form"))
        self.lb_axis.setText(_translate("SectionRange", "Vertical axis:"))
        self.label_3.setText(_translate("SectionRange", "ROI position:"))
        self.label_2.setText(_translate("SectionRange", "ROI width:"))

