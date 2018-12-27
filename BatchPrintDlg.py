# -*- coding: utf-8 -*-
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtWidgets
from PyQt5.QtPrintSupport import QPrinter,QPrintDialog

from Ui_BatchPrintDlg import Ui_BatchPrintDlg
from SysData import SysData  #系统数据
import xlrd
import os

class BatchPrintDlg(QtWidgets.QDialog,Ui_BatchPrintDlg):
    
    def __init__(self):
        super(BatchPrintDlg, self).__init__()
        self.setupUi(self)
        self.SysData = SysData() #系统数据
        self.voucher = None   #当前模板
        self.num = 0       #模板字段数
        self.edtTotalPages.setText('0')
        #选择文件按钮
        self.btnOpenFile.clicked.connect(self.clickedbtnOpenFile)
        #打印按钮
        self.btnPrint.clicked.connect(self.clickedbtnPrint)
    
    #表格初始化
    def initUi(self):
        if self.voucher ==  None:
            return
        self.num = self.voucher.getElementNumbers()
        self.HeaderList = []
        for i in range(1, self.num + 1):
            self.HeaderList.append("字段"+str(i))
        '表格初始化'
        self.DataModel = QStandardItemModel()
        self.DataModel.setHorizontalHeaderLabels(self.HeaderList) #
        self.tvContent.setModel(self.DataModel)

    #打开文件，读入批量数据，设置页数
    def clickedbtnOpenFile(self):
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, '请选择打印文件','',  'Excel表格(*.xls);;Excel2010表格(*.xlsx);;wps表格(*.et)')
        if filename:
            self.edtFileName.setText(filename)
            if os.access(filename, os.F_OK):
                self.initUi()
                workbook = xlrd.open_workbook(filename)   #打开数据文件
                sheet = workbook.sheet_by_index(0)   #第一个sheet
                if sheet.ncols < self.num:    #检查字段数
                    QtWidgets.QMessageBox.information(self,"error","数据文件列数少于模板字段，请检查！", QtWidgets.QMessageBox.Yes)
                    return
                beginrow = 0    #设置数据起始行
                if self.SysData.batchprint:    #有标题行，数据从第二行开始
                    beginrow = 1
                if int(sheet.nrows - beginrow) == 0:
                    QtWidgets.QMessageBox.information(self,"error","数据为空，请检查！", QtWidgets.QMessageBox.Yes)
                    return
                    
                self.edtTotalPages.setText(str(sheet.nrows))   #更新页数控件
                self.edtBeginPage.setText('1')
                self.edtEndPage.setText(str(sheet.nrows - beginrow))
                for i in range(beginrow,sheet.nrows):    #写入tableview控件
                    for j in range(0, sheet.ncols-1):
                        val = sheet.row(i)[j].value
                        self.DataModel.setItem(i, j, QStandardItem(str(val)))
    
    #开始打印    
    def clickedbtnPrint(self):
        if self.voucher ==  None:
            return
        if int(self.edtTotalPages.text()) == 0:
            QtWidgets.QMessageBox.information(self,"提示","数据为空！", QtWidgets.QMessageBox.Yes)
            return
        self.printer = QPrinter()
        self.printer.setPageSize(QPrinter.A4)    #默认A4打印纸
        dialog = QPrintDialog(self.printer, self)
        if not dialog.exec_():
            return        

        painter = QPainter(self.printer)
        for i in range(int(self.edtBeginPage.text())-1,int(self.edtEndPage.text())):
            for j in range(0, self.num):    #读入凭证每个元素，将当前纪录数据更新到元素中
                em = self.voucher.getElement(j)  
                index = self.DataModel.index(i,j);
                val = self.DataModel.data(index)
                em.setVal(val)
                self.voucher.updateElement(j, em)
        
            painter.save()    #打印每一页
            self.voucher.paintElements(painter)
            self.printer.newPage()
            painter.restore()
