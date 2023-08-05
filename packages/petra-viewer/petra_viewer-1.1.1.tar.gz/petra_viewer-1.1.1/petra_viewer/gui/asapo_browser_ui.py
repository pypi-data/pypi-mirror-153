# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uis/asapo_browser.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ASAPOBrowser(object):
    def setupUi(self, ASAPOBrowser):
        ASAPOBrowser.setObjectName("ASAPOBrowser")
        ASAPOBrowser.resize(613, 487)
        self.verticalLayout = QtWidgets.QVBoxLayout(ASAPOBrowser)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.chk_refresh = QtWidgets.QCheckBox(ASAPOBrowser)
        self.chk_refresh.setObjectName("chk_refresh")
        self.horizontalLayout_3.addWidget(self.chk_refresh)
        self.sb_sec = QtWidgets.QSpinBox(ASAPOBrowser)
        self.sb_sec.setEnabled(False)
        self.sb_sec.setMinimum(1)
        self.sb_sec.setObjectName("sb_sec")
        self.horizontalLayout_3.addWidget(self.sb_sec)
        self.label_4 = QtWidgets.QLabel(ASAPOBrowser)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_3.addWidget(self.label_4)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem)
        self.chk_auto_add = QtWidgets.QCheckBox(ASAPOBrowser)
        self.chk_auto_add.setObjectName("chk_auto_add")
        self.horizontalLayout_3.addWidget(self.chk_auto_add)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(ASAPOBrowser)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.le_filter = QtWidgets.QLineEdit(ASAPOBrowser)
        self.le_filter.setObjectName("le_filter")
        self.horizontalLayout.addWidget(self.le_filter)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.chk_time_filter = QtWidgets.QCheckBox(ASAPOBrowser)
        self.chk_time_filter.setObjectName("chk_time_filter")
        self.horizontalLayout_2.addWidget(self.chk_time_filter)
        self.dte_from = QtWidgets.QDateTimeEdit(ASAPOBrowser)
        self.dte_from.setEnabled(False)
        self.dte_from.setCalendarPopup(True)
        self.dte_from.setObjectName("dte_from")
        self.horizontalLayout_2.addWidget(self.dte_from)
        self.label_3 = QtWidgets.QLabel(ASAPOBrowser)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        self.dte_to = QtWidgets.QDateTimeEdit(ASAPOBrowser)
        self.dte_to.setEnabled(False)
        self.dte_to.setCalendarPopup(True)
        self.dte_to.setObjectName("dte_to")
        self.horizontalLayout_2.addWidget(self.dte_to)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.tr_asapo_browser = QtWidgets.QTreeView(ASAPOBrowser)
        self.tr_asapo_browser.setMinimumSize(QtCore.QSize(0, 0))
        self.tr_asapo_browser.setObjectName("tr_asapo_browser")
        self.verticalLayout.addWidget(self.tr_asapo_browser)

        self.retranslateUi(ASAPOBrowser)
        QtCore.QMetaObject.connectSlotsByName(ASAPOBrowser)

    def retranslateUi(self, ASAPOBrowser):
        _translate = QtCore.QCoreApplication.translate
        ASAPOBrowser.setWindowTitle(_translate("ASAPOBrowser", "Form"))
        self.chk_refresh.setText(_translate("ASAPOBrowser", "Refresh every"))
        self.label_4.setText(_translate("ASAPOBrowser", "sec"))
        self.chk_auto_add.setText(_translate("ASAPOBrowser", "Automatically open new"))
        self.label.setText(_translate("ASAPOBrowser", "Filter:"))
        self.chk_time_filter.setText(_translate("ASAPOBrowser", "Filter time from:"))
        self.label_3.setText(_translate("ASAPOBrowser", "To:"))

