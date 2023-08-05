# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uis/view_2d.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_View2D(object):
    def setupUi(self, View2D):
        View2D.setObjectName("View2D")
        View2D.resize(631, 697)
        self.v_layout = QtWidgets.QVBoxLayout(View2D)
        self.v_layout.setObjectName("v_layout")

        self.retranslateUi(View2D)
        QtCore.QMetaObject.connectSlotsByName(View2D)

    def retranslateUi(self, View2D):
        _translate = QtCore.QCoreApplication.translate
        View2D.setWindowTitle(_translate("View2D", "Form"))

