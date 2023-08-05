# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uis/cut_selector.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_CutSelector(object):
    def setupUi(self, CutSelector):
        CutSelector.setObjectName("CutSelector")
        CutSelector.resize(863, 300)
        self.verticalLayout = QtWidgets.QVBoxLayout(CutSelector)
        self.verticalLayout.setObjectName("verticalLayout")
        self.cut_selectors = QtWidgets.QWidget(CutSelector)
        self.cut_selectors.setMinimumSize(QtCore.QSize(0, 0))
        self.cut_selectors.setObjectName("cut_selectors")
        self.verticalLayout.addWidget(self.cut_selectors)

        self.retranslateUi(CutSelector)
        QtCore.QMetaObject.connectSlotsByName(CutSelector)

    def retranslateUi(self, CutSelector):
        _translate = QtCore.QCoreApplication.translate
        CutSelector.setWindowTitle(_translate("CutSelector", "Form"))

