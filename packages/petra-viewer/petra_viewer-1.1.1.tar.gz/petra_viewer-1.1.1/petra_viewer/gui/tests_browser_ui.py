# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uis/tests_browser.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_TestsBrowser(object):
    def setupUi(self, TestsBrowser):
        TestsBrowser.setObjectName("TestsBrowser")
        TestsBrowser.resize(322, 489)
        self.verticalLayout = QtWidgets.QVBoxLayout(TestsBrowser)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tb_sets = QtWidgets.QTableWidget(TestsBrowser)
        self.tb_sets.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAsNeeded)
        self.tb_sets.setHorizontalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOff)
        self.tb_sets.setColumnCount(3)
        self.tb_sets.setObjectName("tb_sets")
        self.tb_sets.setRowCount(0)
        self.tb_sets.horizontalHeader().setDefaultSectionSize(100)
        self.tb_sets.horizontalHeader().setMinimumSectionSize(50)
        self.tb_sets.verticalHeader().setDefaultSectionSize(20)
        self.tb_sets.verticalHeader().setMinimumSectionSize(20)
        self.verticalLayout.addWidget(self.tb_sets)

        self.retranslateUi(TestsBrowser)
        QtCore.QMetaObject.connectSlotsByName(TestsBrowser)

    def retranslateUi(self, TestsBrowser):
        _translate = QtCore.QCoreApplication.translate
        TestsBrowser.setWindowTitle(_translate("TestsBrowser", "Tests Browser"))

