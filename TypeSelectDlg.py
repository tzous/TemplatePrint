# -*- coding: utf-8 -*-
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtWidgets

from Ui_TypeSelectDlg import Ui_TypeSelectDlg
from SysData import SysData


# noinspection PyAttributeOutsideInit
class TypeSelectDlg(QtWidgets.QDialog, Ui_TypeSelectDlg):
    def __init__(self):
        super(TypeSelectDlg, self).__init__()
        self.setupUi(self)
        self.initUi()
        self.lstTypes.clicked.connect(self.onClickedlstTypes)

    def initUi(self):
        self.sysData = SysData()
        self.typeIds = []
        self.typeNames = []
        self.curTypeid = -1
        self.lstTypes.clear()
        for t in self.sysData.types:
            self.typeIds.append(t[0])
            self.typeNames.append(QtWidgets.QListWidgetItem(t[1]))
        for i in range(len(self.typeNames)):
            self.lstTypes.insertItem(i + 1, self.typeNames[i])

    def onClickedlstTypes(self):
        # item = self.lstTypes.currentItem()
        self.curTypeid = self.typeIds[self.lstTypes.currentRow()]
