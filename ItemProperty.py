# -*- coding: utf-8 -*-
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtWidgets

from Ui_ItemProperty import Ui_ItemProperty

#模板设计时的字段属性对话框
class ItemPropertyDialog(QtWidgets.QDialog,Ui_ItemProperty):    
    def __init__(self):    
        super(ItemPropertyDialog,self).__init__()    
        self.setupUi(self)
        self.element = None
        self.icode = -1 #字段编号
        self.tcode = -1 #字段类型序号

    #初始化界面
    def InitUi(self):
        if self.element == None:
            return
        self.labelItemType.setText('字段'+str(self.icode)+'类型：')
        self.listEditType.addItems(self.element.getAllChineseTypes())  #字段类别列表
        self.tcode = self.element.allTypes.index(self.element.type)
        self.listEditType.setCurrentRow(self.tcode)
        if self.element.getHAlign() == Qt.AlignLeft:   #水平对齐
            self.rbHLeft.setChecked(True)
        elif self.element.getHAlign() == Qt.AlignHCenter:
            self.rbHCenter.setChecked(True)
        else:
            self.rbHRight.setChecked(True)
        if self.element.getVAlign() == Qt.AlignTop:   #垂直对齐
            self.rbVTop.setChecked(True)
        elif self.element.getVAlign() == Qt.AlignVCenter:
            self.rbVCenter.setChecked(True)
        else:
            self.rbVBottom.setChecked(True)
        if self.element.getTrim():               #删空格
            self.cbTrim.setChecked(True)
        if self.element.getPrefix():             #前缀
            self.cbPrefix.setChecked(True)
        self.cPrefixText.setText(self.element.getPrefixText())
        if self.element.getPostfix():           #后缀
            self.cbPostfix.setChecked(True)
        self.cPostfixText.setText(self.element.getPostfixText())
        if self.element.getMeanCol():           #均列打印
            self.cbMeanCol.setChecked(True)
        self.iMeanColVal.setText(str(self.element.getMeanColVal()))
        if self.element.getLineWrap():          #自动折行
            self.cbLineWrap.setChecked(True)
        if self.element.getPrintBorder():       #打印边框
            self.cbPrintBorder.setChecked(True)
        self.cCheckType.setText(self.element.getCheckVal())   #打勾项字符
        
        self.textFont.setText(self.element.font.toString())    #字体
        self.btnFont.clicked.connect(self.clickedbtnFont)

        self.listEditType.clicked.connect(self.onListIndexChanged)
        self.btnOK.clicked.connect(self.clickedbtnOK)

    #设置字体对话框
    def clickedbtnFont(self):
        cf, ok = QtWidgets.QFontDialog.getFont()
        if ok:
            self.element.setFont(cf)
            self.textFont.setText(cf.toString())

    #字段类别变更处理
    def onListIndexChanged(self, index):
        self.element.type = self.element.allTypes[index.row()]
        if self.element.type == 'text':
            self.element.setVal('文本')
        elif self.element.type == 'num':
            self.element.setVal('0')
        elif self.element.type == 'numcap':
            self.element.setVal('零')
        elif self.element.type == 'money':
            self.element.setVal('0.00')
        elif self.element.type == 'moneycap':
            self.element.setVal('0.00')
        elif self.element.type == 'check':
            self.element.setVal(self.element.checkVal)
        else:
            self.element.setVal('文本')

    #确认
    def clickedbtnOK(self):
        if self.rbHLeft.isChecked():
            self.element.hAlign =Qt.AlignLeft
        if self.rbHCenter.isChecked():
            self.element.hAlign =Qt.AlignHCenter
        if self.rbHRight.isChecked():
            self.element.hAlign =Qt.AlignRight
        if self.rbVTop.isChecked():
            self.element.vAlign =Qt.AlignTop
        if self.rbVCenter.isChecked():
            self.element.vAlign =Qt.AlignVCenter
        if self.rbVBottom.isChecked():
            self.element.vAlign =Qt.AlignBottom
        if self.cbTrim.isChecked():
            self.element.trim = True
        else:
            self.element.trim = False
        if self.cbPrefix.isChecked():
            self.element.prefix = True
        else:
            self.element.prefix = False
        if self.cbPostfix.isChecked():
            self.element.postfix = True
        else:
            self.element.postfix = False
        if self.cbMeanCol.isChecked():
            self.element.meanCol = True
        else:
            self.element.meanCol = False
        if self.cbPrintBorder.isChecked():
            self.element.printBorder = True
        else:
            self.element.printBorder = False
        if self.cbLineWrap.isChecked():
            self.element.lineWrap = True
        else:
            self.element.lineWrap = False
            
        self.element.prefixText = self.cPrefixText.text()     #前缀文本，如人民币符号¥等
        self.element.postfixText = self.cPostfixText.text()   #后缀文本
        self.element.meanColVal = int(self.iMeanColVal.text())     #均列打印间隔
        self.element.checkVal = self.cCheckType.text()      #check类型，取值预置为√×*等
        self.element.setVal(self.element.getVal())    #根据属性重算显示文本
        self.accept()
