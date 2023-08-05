# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uis/rois_view.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_RoisView(object):
    def setupUi(self, RoisView):
        RoisView.setObjectName("RoisView")
        RoisView.resize(800, 600)
        self.centralwidget = QtWidgets.QWidget(RoisView)
        self.centralwidget.setObjectName("centralwidget")
        RoisView.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(RoisView)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 28))
        self.menubar.setObjectName("menubar")
        RoisView.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(RoisView)
        self.statusbar.setObjectName("statusbar")
        RoisView.setStatusBar(self.statusbar)

        self.retranslateUi(RoisView)
        QtCore.QMetaObject.connectSlotsByName(RoisView)

    def retranslateUi(self, RoisView):
        _translate = QtCore.QCoreApplication.translate
        RoisView.setWindowTitle(_translate("RoisView", "ROIs view"))

