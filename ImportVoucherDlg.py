# -*- coding: utf-8 -*-
from PyQt5 import QtWidgets
from Ui_ImportVoucherDlg import Ui_ImportVoucherDlg 
from SysData import SysData  #系统数据
from Voucher import Voucher

#模板导入对话框
class ImportVoucherDlg(QtWidgets.QDialog,Ui_ImportVoucherDlg):
    
    def __init__(self):
        super(ImportVoucherDlg, self).__init__()
        self.setupUi(self)
        self.sysData = SysData()
        self.typeIds = []   #类别ID列表
        self.initTypes()
        #确认
        self.btnopenfile.clicked.connect(self.onclickedbtnopenfile)

    #类别加载到comboBox中
    def initTypes(self):
        for t in self.sysData.types:
            self.cmbType.addItem(t[1])
            self.typeIds.append(t[0])

    #得到当前comboBox的类别
    def getCurrType(self):
        return self.typeIds[self.cmbType.currentIndex()]
            
    #打开模板文件，得到相关信息，并显示到对话框中
    def onclickedbtnopenfile(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, '请选择模板文件', '*.tdb')
        if filename:
            self.edtfilename.setText(filename)
            voucher = Voucher()
            voucher.loadfromdb(filename)
            self.edtName.setText(voucher.name)
            self.edtDisplayText.setText(voucher.text)
