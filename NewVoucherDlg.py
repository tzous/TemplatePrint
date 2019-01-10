# -*- coding: utf-8 -*-
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtWidgets
import sqlite3
from Ui_NewVoucherDlg import Ui_NewVoucherDlg  # 新建模板对话框
from DesignCanvas import DesignCanvas  # 画板
from Voucher import Voucher, Element  # 模板类
from SysData import SysData  # 系统数据


# 新建模板对话框
# noinspection SpellCheckingInspection
class NewVoucherDlg(QtWidgets.QDialog, Ui_NewVoucherDlg):

    def __init__(self):
        super(NewVoucherDlg, self).__init__()
        self.setupUi(self)
        self.sysData = SysData()
        self.typeIds = []
        self.initTypes()
        # 确认
        self.btnOK.clicked.connect(self.accept)
        # 取消
        self.btnCancel.clicked.connect(self.reject)

    # 初始化下拉框
    def initTypes(self):
        for t in self.sysData.types:
            self.cmbType.addItem(t[1])
            self.typeIds.append(t[0])

    # 得到所选的类别ID
    def getCurrType(self):
        return self.typeIds[self.cmbType.currentIndex()]

    # 设置类别下拉框中当前项
    def setCurrType(self, curtype):
        i = 0
        for t in self.typeIds:
            if t == curtype:
                self.cmbType.setCurrentIndex(i)
                break
            i = i + 1
