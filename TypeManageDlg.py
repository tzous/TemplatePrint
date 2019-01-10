# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets
from PyQt5.QtCore import *
from PyQt5.QtGui import *

from Ui_TypeManageDlg import Ui_TypeManageDlg
from SysData import SysData  # 系统数据
from MyTools import MyTools


# noinspection PyAttributeOutsideInit,SpellCheckingInspection
class TypeManageDlg(QtWidgets.QDialog, Ui_TypeManageDlg):

    def __init__(self):
        super(TypeManageDlg, self).__init__()
        self.setupUi(self)
        self.initUi()
        self.btnAdd.clicked.connect(self.onClickedbtnAdd)
        self.btnSave.clicked.connect(self.onClickedbtnSave)
        self.btnDelete.clicked.connect(self.onClickedbtnDelete)
        self.lstTypes.clicked.connect(self.onClickedlstTypes)

    def initUi(self):
        self.sysData = SysData()
        self.typeIds = []
        self.typeNames = []
        self.currentRow = -1
        self.lstTypes.clear()
        for t in self.sysData.types:
            self.typeIds.append(t[0])
            self.typeNames.append(QtWidgets.QListWidgetItem(t[1]))
        for i in range(len(self.typeNames)):
            self.lstTypes.insertItem(i + 1, self.typeNames[i])

    def onClickedlstTypes(self):
        item = self.lstTypes.currentItem()
        self.currentRow = self.lstTypes.currentRow()
        self.edtTypeName.setText(item.text())

    def onClickedbtnAdd(self):
        mytools = MyTools()
        s = mytools.trim(self.edtTypeName.text())
        if s == '':
            return
        self.sysData.SaveNewType(s)
        self.initUi()
        self.edtTypeName.setText('')

    def onClickedbtnSave(self):
        mytools = MyTools()
        s = mytools.trim(self.edtTypeName.text())
        if s == '' or self.currentRow < 0:
            return
        self.sysData.UpdateTypeByID(self.typeIds[self.currentRow], s)
        self.initUi()
        self.edtTypeName.setText('')

    def onClickedbtnDelete(self):
        if self.currentRow < 0:
            return
        ret = self.sysData.DeleteTypeByID(self.typeIds[self.currentRow])
        if ret != 0:
            QtWidgets.QMessageBox.information(self, "Information", "删除失败，类别中有打印模板！", QtWidgets.QMessageBox.Yes)
        else:
            self.initUi()
            self.edtTypeName.setText('')
