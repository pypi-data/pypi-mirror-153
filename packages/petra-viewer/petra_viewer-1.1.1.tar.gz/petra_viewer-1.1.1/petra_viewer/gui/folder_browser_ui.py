# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uis/folder_browser.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_FolderBrowser(object):
    def setupUi(self, FolderBrowser):
        FolderBrowser.setObjectName("FolderBrowser")
        FolderBrowser.resize(269, 483)
        self.verticalLayout = QtWidgets.QVBoxLayout(FolderBrowser)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(FolderBrowser)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.le_filter = QtWidgets.QLineEdit(FolderBrowser)
        self.le_filter.setObjectName("le_filter")
        self.horizontalLayout.addWidget(self.le_filter)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.tr_file_browser = QtWidgets.QTreeView(FolderBrowser)
        self.tr_file_browser.setMinimumSize(QtCore.QSize(0, 0))
        self.tr_file_browser.setObjectName("tr_file_browser")
        self.verticalLayout.addWidget(self.tr_file_browser)

        self.retranslateUi(FolderBrowser)
        QtCore.QMetaObject.connectSlotsByName(FolderBrowser)

    def retranslateUi(self, FolderBrowser):
        _translate = QtCore.QCoreApplication.translate
        FolderBrowser.setWindowTitle(_translate("FolderBrowser", "Form"))
        self.label.setText(_translate("FolderBrowser", "Filter:"))

