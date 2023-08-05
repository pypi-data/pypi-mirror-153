# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uis/file_browser.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_FileBrowser(object):
    def setupUi(self, FileBrowser):
        FileBrowser.setObjectName("FileBrowser")
        FileBrowser.resize(269, 483)
        self.verticalLayout = QtWidgets.QVBoxLayout(FileBrowser)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(FileBrowser)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.le_filter = QtWidgets.QLineEdit(FileBrowser)
        self.le_filter.setObjectName("le_filter")
        self.horizontalLayout.addWidget(self.le_filter)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.chk_door = QtWidgets.QCheckBox(FileBrowser)
        self.chk_door.setObjectName("chk_door")
        self.horizontalLayout_3.addWidget(self.chk_door)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.chk_monitor = QtWidgets.QCheckBox(FileBrowser)
        self.chk_monitor.setObjectName("chk_monitor")
        self.horizontalLayout_2.addWidget(self.chk_monitor)
        self.cmd_reload = QtWidgets.QPushButton(FileBrowser)
        self.cmd_reload.setObjectName("cmd_reload")
        self.horizontalLayout_2.addWidget(self.cmd_reload)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.breadcrumbsaddressbar = BreadcrumbsAddressBar(FileBrowser)
        self.breadcrumbsaddressbar.setObjectName("breadcrumbsaddressbar")
        self.verticalLayout.addWidget(self.breadcrumbsaddressbar)
        self.tr_file_browser = QtWidgets.QTreeView(FileBrowser)
        self.tr_file_browser.setMinimumSize(QtCore.QSize(0, 0))
        self.tr_file_browser.setObjectName("tr_file_browser")
        self.verticalLayout.addWidget(self.tr_file_browser)

        self.retranslateUi(FileBrowser)
        QtCore.QMetaObject.connectSlotsByName(FileBrowser)

    def retranslateUi(self, FileBrowser):
        _translate = QtCore.QCoreApplication.translate
        FileBrowser.setWindowTitle(_translate("FileBrowser", "Form"))
        self.label.setText(_translate("FileBrowser", "Filter:"))
        self.chk_door.setText(_translate("FileBrowser", "Monitor door"))
        self.chk_monitor.setText(_translate("FileBrowser", "Monitor folder"))
        self.cmd_reload.setText(_translate("FileBrowser", "Refresh"))

from petra_viewer.widgets.breadcrumbsaddressbar.breadcrumbsaddressbar import BreadcrumbsAddressBar
import petra_viewer.gui.icons_rc
