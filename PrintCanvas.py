# -*- coding: utf-8 -*-
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

import base64


# noinspection SpellCheckingInspection,PyAttributeOutsideInit
class PrintCanvas(QWidget):
    def __init__(self, *args, **kwargs):
        super(PrintCanvas, self).__init__(*args, **kwargs)  # 继承父类

        # self.setMouseTracking(True)#保证得到鼠标信息
        self.drawingRectColor = QColor(200, 200, 200)  # 默认填充色
        self.voucher = None  # 当前凭证模板
        self.painter = QPainter(self)
        self.startPoint = QPoint()  # 当前画板矩形左上角点
        self.elementList = []  # 凭证元素控件列表

    # 设置当前凭证模板
    def setVoucher(self, v):
        self.voucher = v

    def getVoucher(self):
        return self.voucher

    def initUi(self):
        # 先释放原凭证元素控件
        for e in self.elementList:
            e.close()
            e.deleteLater()
        # 再重新生成元素控件
        self.elementList = []
        if self.voucher is None:
            return
        i = 0
        while i < self.voucher.getElementNumbers():
            em = self.voucher.getElement(i)
            if em.type == 'check':
                self.emwidget = QCheckBox(self)
            else:
                self.emwidget = QLineEdit(self)
            self.emwidget.move(em.startPoint.x(), em.startPoint.y())
            self.emwidget.resize(em.width, em.height)
            self.emwidget.show()
            self.elementList.append(self.emwidget)
            i = i + 1

    def initUiData(self):
        if self.voucher is None:
            return
        i = 0
        while i < self.voucher.getElementNumbers():
            em = self.voucher.getElement(i)
            if em.type == 'check':
                if em.getVal() == em.checkVal:
                    self.elementList[i].toggle()
            else:
                self.elementList[i].setText(str(em.getVal()))
            i = i + 1

    def paintEvent(self, ev):
        if self.voucher is None:
            return

        # 画背景，如无背景则画一矩形
        p = self.painter
        p.begin(self)
        if self.voucher.getBackground() is None:
            p.setBrush(self.drawingRectColor)  # 实心
            p.drawRect(self.startPoint.x(), self.startPoint.y(), self.voucher.getPixelWidth(),
                       self.voucher.getPixelHeight())
        else:
            imgdata = base64.b64decode(self.voucher.getBackground())
            pixImg = QPixmap()
            pixImg.loadFromData(imgdata)
            p.drawPixmap(self.startPoint.x(), self.startPoint.y(), self.voucher.getPixelWidth(),
                         self.voucher.getPixelHeight(), pixImg)
        p.end()
