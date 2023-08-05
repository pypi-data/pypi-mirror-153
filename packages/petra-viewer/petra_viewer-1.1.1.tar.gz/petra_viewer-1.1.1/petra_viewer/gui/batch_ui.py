# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'uis/batch.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_batch(object):
    def setupUi(self, batch):
        batch.setObjectName("batch")
        batch.resize(400, 145)
        self.verticalLayout = QtWidgets.QVBoxLayout(batch)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tx_status = QtWidgets.QTextEdit(batch)
        self.tx_status.setTextInteractionFlags(QtCore.Qt.NoTextInteraction)
        self.tx_status.setObjectName("tx_status")
        self.verticalLayout.addWidget(self.tx_status)
        self.pb_progress = QtWidgets.QProgressBar(batch)
        self.pb_progress.setProperty("value", 0)
        self.pb_progress.setObjectName("pb_progress")
        self.verticalLayout.addWidget(self.pb_progress)
        self.but_box = QtWidgets.QDialogButtonBox(batch)
        self.but_box.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.but_box.setStandardButtons(QtWidgets.QDialogButtonBox.Abort|QtWidgets.QDialogButtonBox.Close)
        self.but_box.setObjectName("but_box")
        self.verticalLayout.addWidget(self.but_box)

        self.retranslateUi(batch)
        QtCore.QMetaObject.connectSlotsByName(batch)

    def retranslateUi(self, batch):
        _translate = QtCore.QCoreApplication.translate
        batch.setWindowTitle(_translate("batch", "Batch processing"))

