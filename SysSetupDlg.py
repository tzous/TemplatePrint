# -*- coding: utf-8 -*-
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtWidgets

from Ui_SysSetupDlg import Ui_SysSetupDlg
from SysData import SysData


# 打印设置对话框
# noinspection SpellCheckingInspection
class SysSetupDlg(QtWidgets.QDialog, Ui_SysSetupDlg):
    def __init__(self):
        super(SysSetupDlg, self).__init__()
        self.setupUi(self)
        self.sysData = SysData()
        self.initUi()
        self.btnOK.clicked.connect(self.onClickedbtnOK)

    def initUi(self):
        self.edtLeftMargin.setText(str(self.sysData.leftmargin))
        self.edtTopMargin.setText(str(self.sysData.topmargin))
        if self.sysData.batchprint:
            self.cbBatchPrint.toggle()

    def onClickedbtnOK(self):
        self.sysData.leftmargin = int(self.edtLeftMargin.text())
        self.sysData.topmargin = int(self.edtTopMargin.text())
        if self.cbBatchPrint.isChecked():
            self.sysData.batchprint = True
        else:
            self.sysData.batchprint = False

        self.sysData.saveSysData()
        self.accept()
