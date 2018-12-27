# -*- coding: utf-8 -*-
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from Ui_PrintLogDlg import Ui_PrintLogDlg
from SysData import SysData
from PrintLog import PrintLog
from Voucher import Voucher

class PrintLogDlg(QDialog,Ui_PrintLogDlg):    
    def __init__(self):    
        super(PrintLogDlg,self).__init__()    
        self.setupUi(self)
        self.sysData = SysData()
        self.voucher = None
        self.printlog = PrintLog()
        self.logdatas = []  #保存选中的prlogs记录
        self.emdatas = []   #保存选中的明细数据记录
        self.rows = 20    #每次查询行数
        self.nbegin = 0
        self.nend = self.rows
        self.totalrows = 0 #总行数
        self.initUi()
        self.btnQuery.clicked.connect(self.onClickedbtnQuery)
        self.btnClean.clicked.connect(self.onClickedbtnClean)
        self.btnFirst.clicked.connect(self.onClickedbtnFirst)
        self.btnPrev.clicked.connect(self.onClickedbtnPrev)
        self.btnNext.clicked.connect(self.onClickedbtnNext)
        self.btnLast.clicked.connect(self.onClickedbtnLast)
        self.tvLogDetails.clicked.connect(self.onClickedtvLogDetails)
        self.btnOK.clicked.connect(self.clickedbtnOK)        
        self.tvLogDetails.setContextMenuPolicy(Qt.CustomContextMenu)  
        self.tvLogDetails.customContextMenuRequested.connect(self.showContextMenu) 
        self.contextMenu = QMenu(self)  #模板右键菜单
        self.actionDelete = self.contextMenu.addAction('删除当前记录') 
        self.actionDelete.triggered.connect(self.onactionDelete)

        
    def initUi(self):
        self.HeaderList = ['日期', '模板名']
        for i in range(1, 11):
            self.HeaderList.append("字段"+str(i))
        '表格初始化'
        self.DataModel = QStandardItemModel()
        self.DataModel.setHorizontalHeaderLabels(self.HeaderList)#
        self.tvLogDetails.setModel(self.DataModel)

        
    def onClickedbtnQuery(self):
        self.voucher = None
        self.logdatas = [] 
        self.initUi()
        
        prdate = self.edtDate.text() #查询日期条件
        if prdate == '--':
            prdate = ''
        vtext = self.edtVoucherName.text() #查询模板条件
        self.totalrows = self.printlog.getTotalRows(prdate, vtext) #得到总行数
        self.printlog.loadPrintLog(prdate, vtext, self.nbegin, self.nend) #得到查询结果
        if self.totalrows < self.rows:
            self.nend = self.totalrows
        i = 0
        for t in self.printlog.prlogs:   #查询结果加入tableview
            self.DataModel.setItem(i, 0, QStandardItem(t[1]))
            self.DataModel.setItem(i, 1, QStandardItem(t[3]))
            self.DataModel.setItem(i, 2, QStandardItem(t[4]))
            self.DataModel.setItem(i, 3, QStandardItem(t[5]))
            self.DataModel.setItem(i, 4, QStandardItem(t[6]))
            self.DataModel.setItem(i, 5, QStandardItem(t[7]))
            self.DataModel.setItem(i, 6, QStandardItem(t[8]))
            self.DataModel.setItem(i, 7, QStandardItem(t[9]))
            self.DataModel.setItem(i, 8, QStandardItem(t[10]))
            self.DataModel.setItem(i, 9, QStandardItem(t[11]))
            self.DataModel.setItem(i, 10, QStandardItem(t[12]))
            self.DataModel.setItem(i, 11, QStandardItem(t[13]))
            i = i + 1
        
    def onClickedtvLogDetails(self):
        row = self.tvLogDetails.currentIndex().row()#返回表格被选中行 数值
        #col = self.tvLogDetails.currentIndex().column()#返回表格被选中列 数值
        i = 0
        for t in self.printlog.prlogs:
            if i == row:
                self.logdatas = t #保存凭证信息
                self.printlog.loadEmDataByLid(self.logdatas[0]) # 读入明细数据
                self.emdatas = self.printlog.emdatas
                break
            i = i + 1

    def clickedbtnOK(self):
        if  self.logdatas == []:
            QMessageBox.information(self,"Information","没有选择打印数据！", QMessageBox.Ok )
        else:
            self.accept()

    def onClickedbtnFirst(self):
        if self.totalrows == 0:
            return
        if self.nbegin <= 0: #已在首页
            return
        self.nbegin = 0
        self.nend = self.rows
        self.onClickedbtnQuery()
        
    def onClickedbtnPrev(self):
        if self.totalrows == 0:
            return
        if self.nbegin <= 0:  #已在首页
            return
        self.nend = self.nbegin   
        self.nbegin = self.nbegin - self.rows
        if self.nbegin < 0:
            self.nbegin = 0
        self.onClickedbtnQuery()
        
    def onClickedbtnNext(self):
        if self.totalrows == 0:
            return
        if self.nend >= self.totalrows:  #已在末页
            return

        self.nbegin = self.nend
        self.nend = self.nend + self.rows
        if self.nend > self.totalrows:
            self.nend = self.totalrows

        self.onClickedbtnQuery()

    def onClickedbtnLast(self):
        if self.totalrows == 0:
            return
        if self.nend >= self.totalrows:   #已在末页
            return
        row = self.totalrows % self.rows
        self.nbegin = self.totalrows - row
        self.nend = self.totalrows
        if self.nbegin < 0:
            self.nbegin = 0
        self.onClickedbtnQuery()
        
    def onClickedbtnClean(self):
        prdate = self.edtDate.text() #查询日期条件
        if prdate == '--':
            prdate = ''
        vtext = self.edtVoucherName.text() #查询模板条件

        if prdate != '' and vtext == '':
            msg = "是否删除日期为“%s”的数据?" %(prdate)
        elif prdate == '' and vtext != '':
            msg = "是否删除所有模板名为“%s”开头的数据?" %(vtext)
        elif prdate != '' and vtext != '':
            msg = "是否删除日期为“%s”且模板名为“%s”开头的数据?" %(prdate, vtext)
        else:
            msg = "是否删除所有数据?" 
        ret = QMessageBox.information(self,"Question",msg, QMessageBox.Yes|QMessageBox.No )
        if ret != QMessageBox.Yes:
                return
        self.printlog.DeletePrintLog(prdate, vtext)
        self.voucher = None
        self.logdatas = [] 
        self.initUi()

    def onactionDelete(self):
        msg = "是否删除当前记录?"
        ret = QMessageBox.information(self,"Question",msg, QMessageBox.Yes|QMessageBox.No )
        if ret != QMessageBox.Yes:
                return
        self.printlog.DeletePrintLogByID(int(self.logdatas[0]))
        self.onClickedbtnQuery()

        
    #tableview控件右键事件
    def showContextMenu(self, ev):
        if self.totalrows == 0:
            return
        self.onClickedtvLogDetails()
        self.contextMenu.exec_(QCursor.pos()) #在鼠标位置显示
        
