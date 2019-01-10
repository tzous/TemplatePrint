# -*- coding: utf-8 -*-
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *

from ItemProperty import ItemPropertyDialog  # 项目属性对话框
import base64


# noinspection PyAttributeOutsideInit,SpellCheckingInspection
class DesignCanvas(QWidget):
    def __init__(self, *args, **kwargs):
        super(DesignCanvas, self).__init__(*args, **kwargs)  # 继承父类

        self.initUI()
        self.initEventPlot()

        self.setMouseTracking(True)  # 保证得到鼠标信息
        self.drawingRectColor = QColor(200, 200, 200)  # 默认填充色
        self.voucher = None  # 当前凭证模板
        self.edited = False  # 是否已编辑过

        self.startPoint = QPoint()  # 当前画板矩形左上角点
        self.curElement = -1  # 当前元素编号，鼠标左键单击时使用
        self.currElement = -1  # 当前元素编号，鼠标左键双击及右键时使用，因为释放时是同一个事件，所以要分开
        self.multiSelect = False  # 是否多选
        self.multiSelectList = []  # 多选列表

        self.painter = QPainter(self)
        self.permit = False  # 描述是否允许
        self.drag = False  # 当前是否可拖动
        self.xExpand = False  # 在X方向扩展
        self.yExpand = False  # 在Y方向扩展

    # 初始化UI
    def initUI(self):
        # 右键菜单
        self.setContextMenuPolicy(Qt.CustomContextMenu)
        # self.customContextMenuRequested.connect(self.showContextMenu)
        self.contextMenu = QMenu(self)  # 单选右键菜单
        self.actionModify = self.contextMenu.addAction('修改属性')
        self.contextMenu.addSeparator()
        self.actionDelete = self.contextMenu.addAction('删除')
        self.actionModify.triggered.connect(self.actionHandlerModify)
        self.actionDelete.triggered.connect(self.actionHandlerDelete)

        self.contextMultiMenu = QMenu(self)  # 多选右键菜单
        self.actionAlignLeft = self.contextMultiMenu.addAction('左对齐')
        self.actionAlignRight = self.contextMultiMenu.addAction('右对齐')
        self.actionAlignTop = self.contextMultiMenu.addAction('上对齐')
        self.actionAlignBottom = self.contextMultiMenu.addAction('下对齐')
        self.actionSameWidth = self.contextMultiMenu.addAction('相同宽度')
        self.actionSameHeight = self.contextMultiMenu.addAction('相同高度')
        self.contextMultiMenu.addSeparator()
        self.actionMultiCancel = self.contextMultiMenu.addAction('取消')
        self.actionAlignLeft.triggered.connect(self.actionHandlerAlignLeft)
        self.actionAlignRight.triggered.connect(self.actionHandlerAlignRight)
        self.actionAlignTop.triggered.connect(self.actionHandlerAlignTop)
        self.actionAlignBottom.triggered.connect(self.actionHandlerAlignBottom)
        self.actionSameWidth.triggered.connect(self.actionHandlerSameWidth)
        self.actionSameHeight.triggered.connect(self.actionHandlerSameHeight)
        self.actionMultiCancel.triggered.connect(self.actionHandlerMultiCancel)

    # 事件初始化
    def initEventPlot(self):
        pass

    # 设置当前凭证模板
    def setVoucher(self, v):
        self.voucher = v

    def getVoucher(self):
        return self.voucher

    # 描述是否允许
    def setPermit(self, t):
        if t:
            self.permit = True
        else:
            self.permit = False

    def getPermit(self):
        return self.permit

    # 设置画板矩形左上角点
    def setStartPoint(self, e):
        self.startPoint = e

    def getStartPoint(self):
        return self.startPoint

    def setMultiSelect(self, tf):
        if tf:
            self.multiSelect = True
        else:
            self.multiSelect = False
            self.multiSelectList = []

    def getMultiSelect(self):
        return self.multiSelect

    def getMultiSelectList(self):
        return self.multiSelectList

    # 鼠标点在画板矩形中
    def mouseInCanvas(self, pos):
        if self.voucher is None:
            return False
        x = pos.x() - self.startPoint.x()
        y = pos.y() - self.startPoint.y()
        if 0 <= x <= self.voucher.getPixelWidth() and 0 <= y <= self.voucher.getPixelHeight():
            return True
        else:
            return False

    # 移动鼠标事件
    def mouseMoveEvent(self, ev):
        if self.voucher is None:
            return
        evpos = ev.pos()  # 得到鼠标位置
        virtualpos = QPoint(evpos.x() - self.startPoint.x(), evpos.y() - self.startPoint.y())
        window = self.parent().window()  # 得到窗口对象
        if window is not None:
            self.parent().window().labelCoordinates.setText('X: %d; Y: %d' % (evpos.x(), evpos.y()))  # 设置窗口状态栏信息
        # 处于非扩展或拖动状态，鼠标形状设定
        if not (self.xExpand or self.yExpand or self.drag):
            self.inShape = False
            # 设置鼠标移动时的光标类型
            i = 0
            while i < self.voucher.getElementNumbers():
                em = self.voucher.getElement(i)
                # 是否在右边上
                if em.xcontains(virtualpos):
                    self.setCursor(QCursor(Qt.SizeHorCursor))
                    self.inShape = True
                # 是否在下边上
                elif em.ycontains(virtualpos):
                    self.setCursor(QCursor(Qt.SizeVerCursor))
                    self.inShape = True
                # 判断鼠标位置是否在已画矩形中
                elif em.contains(virtualpos):
                    if ev.modifiers() & Qt.ControlModifier:  # Ctrl按下
                        self.setCursor(QCursor(Qt.PointingHandCursor))
                    else:
                        self.setCursor(QCursor(Qt.SizeAllCursor))
                    self.inShape = True
                if self.inShape:
                    break
                i = i + 1
            if not self.inShape:
                self.setCursor(QCursor(Qt.ArrowCursor))
        # 鼠标左键按下并移动
        if ev.buttons() & Qt.LeftButton and self.curElement >= 0:
            em = self.voucher.getElement(self.curElement)
            if self.xExpand:  # 向右扩展，不能超出凭证范围
                if evpos.x() > em.getStartPoint().x() and self.voucher.contains(virtualpos):
                    width = evpos.x() - em.getStartPoint().x()
                    em.setWidth(width)
                    self.voucher.updateElement(self.curElement, em)
            elif self.yExpand:  # 向下扩展，不能超出凭证范围
                if evpos.y() > em.getStartPoint().y() and self.voucher.contains(virtualpos):
                    height = evpos.y() - em.getStartPoint().y()
                    em.setHeight(height)
                    self.voucher.updateElement(self.curElement, em)
            elif self.drag:  # 按左键拖动，不能超出凭证范围
                x = evpos.x() - self.BeginPos.x()
                y = evpos.y() - self.BeginPos.y()
                ltpoint = QPoint(em.getStartPoint().x() + x, em.getStartPoint().y() + y)  # 新位置左上角
                rbpoint = QPoint(ltpoint.x() + em.getWidth(), ltpoint.y() + em.getHeight())  # 新位置右下角
                if self.voucher.contains(rbpoint) and self.voucher.contains(ltpoint):  # 新位置在凭证范围内
                    em.movedist(x, y)
                    self.voucher.updateElement(self.curElement, em)
                    self.BeginPos = evpos
        self.update()

    # 鼠标点击事件，点击左键和右键是同一个事件
    def mousePressEvent(self, ev):
        if self.voucher is None:
            return
        if self.xExpand or self.yExpand or self.drag:  # 已处于扩展或拖动状态，取消处理
            return
        evpos = ev.pos()  # 得到鼠标位置
        virtualpos = QPoint(evpos.x() - self.startPoint.x(), evpos.y() - self.startPoint.y())
        if not self.mouseInCanvas(evpos):  # 不在画板中，则不处理
            return
        if ev.button() == Qt.LeftButton:  # 鼠标左键
            if ev.modifiers() & Qt.ControlModifier:  # 鼠标左键及Ctrl同时按下，执行多选操作
                self.multiSelect = True

                for i in range(0, self.voucher.getElementNumbers()):  # 判断是否选中元素，需检测所有元素
                    em = self.voucher.getElement(i)
                    if em.contains(virtualpos):  # 鼠标在矩形中
                        self.multiSelectList.append(i)
                        break

            else:  # 普通鼠标左键处理
                self.multiSelect = False
                self.BeginPos = evpos
                hit = -1   # 选中的元素编号
                for i in range(0, self.voucher.getElementNumbers()):  # 三个类型，判断是否选中元素，需检测所有元素
                    hit = i
                    em = self.voucher.getElement(i)
                    if em.xcontains(virtualpos):  # 鼠标在右边上
                        self.xExpand = True
                        width = evpos.x() - em.getStartPoint().x()
                        em.setWidth(width)
                        self.setCursor(QCursor(Qt.SizeHorCursor))
                        break
                    elif em.ycontains(virtualpos):  # 鼠标在下边上
                        self.yExpand = True
                        height = evpos.y() - em.getStartPoint().y()
                        em.setHeight(height)
                        self.setCursor(QCursor(Qt.SizeVerCursor))
                        break
                    elif em.contains(virtualpos):  # 鼠标在矩形中
                        self.drag = True
                        self.setCursor(QCursor(Qt.ClosedHandCursor))
                        break

                if self.xExpand or self.yExpand or self.drag:  # 已处于扩展或拖动状态
                    self.curElement = hit
                    self.edited = True
        elif ev.button() == Qt.RightButton:  # 鼠标右键，弹出右键菜单
            if self.multiSelect:
                self.contextMultiMenu.exec_(QCursor.pos())  # 在鼠标位置显示
            elif self.setCurrElementByMouse(ev):  # 如果选中
                self.contextMenu.exec_(QCursor.pos())  # 在鼠标位置显示

        self.update()

    # 鼠标释放，单击双击是同一个事件
    def mouseReleaseEvent(self, ev):
        if self.voucher is None:
            return
        if ev.button() == Qt.LeftButton:
            self.setCursor(QCursor(Qt.ArrowCursor))
            self.curElement = -1
            if not (ev.modifiers() & Qt.ControlModifier):  # 释放鼠标时没有按Ctrl键，则取消多选
                self.setMultiSelect(False)
        self.drag = False
        self.xExpand = False
        self.yExpand = False
        self.update()

    # 双击事件
    def mouseDoubleClickEvent(self, ev):
        if self.voucher is None:
            return
        if self.setCurrElementByMouse(ev):
            # 弹出被双击元素的属性修改对话框
            self.modifyElement()

    def paintEvent(self, ev):
        if self.voucher is None:
            return
        p = self.painter
        p.begin(self)
        brush = QBrush(Qt.NoBrush)
        p.setBrush(brush)
        # 画背景，如无背景则画一矩形
        if self.voucher.getBackground() is None:
            p.setBrush(self.drawingRectColor)  # 实心
            p.drawRect(self.startPoint.x(), self.startPoint.y(), self.voucher.getPixelWidth(),
                       self.voucher.getPixelHeight())
        else:
            imgdata = base64.b64decode(self.voucher.getBackground())  # 图片数据以base64格式存放
            pixImg = QPixmap()
            pixImg.loadFromData(imgdata)  # 生成QPixmap图片
            p.drawPixmap(self.startPoint.x(), self.startPoint.y(), self.voucher.getPixelWidth(),
                         self.voucher.getPixelHeight(), pixImg)
        # 画各个元素矩形
        p.setBrush(brush)
        for i in range(0, self.voucher.getElementNumbers()):
            if i == self.curElement or i == self.currElement or i in self.multiSelectList:  # 选中元素矩形边框不同
                pen = QPen(QColor(0, 0, 0), 2, Qt.DotLine)
            else:
                pen = QPen(QColor(0, 0, 0), 1, Qt.SolidLine)
            p.setPen(pen)
            em = self.voucher.getElement(i)
            rect = QRect(self.startPoint.x() + em.getStartPoint().x(), self.startPoint.y() + em.getStartPoint().y(),
                         em.getWidth(), em.getHeight())
            p.drawRect(rect)  # 画方框
            txt = em.getText()
            if em.meanCol and em.getType() in ['num', 'money']:  # 均列打印
                txt = txt.replace('.', '')  # 删除其中的小数点
                ft = em.font
                ft.setLetterSpacing(QFont.AbsoluteSpacing, em.meanColVal)  # 设置间隔
                p.setFont(ft)  # 设置字体
            else:  # 普通文本
                p.setFont(em.font)  # 设置字体
            p.drawText(rect, em.getHAlign() | em.getVAlign(), str(i + 1) + ":" + txt)

        p.end()

    # 修改元素属性对话框处理
    def modifyElement(self):
        if self.currElement < 0:
            return
        itemPropertyDialog = ItemPropertyDialog()
        itemPropertyDialog.element = self.voucher.getElement(self.currElement)
        itemPropertyDialog.icode = int(self.currElement) + 1
        itemPropertyDialog.InitUi()
        if itemPropertyDialog.exec_():
            itemPropertyDialog.element.setVal(itemPropertyDialog.element.getVal())  # 更新元素控件显示文本
            self.voucher.updateElement(self.currElement, itemPropertyDialog.element)  # 更新当前模板中元素属性
            self.edited = True
        # 完毕后取消当前元素选定
        self.currElement = -1
        self.update()

    # 删除元素属性对话框处理
    def deleteElement(self):
        if self.currElement < 0:
            return
        ret = QMessageBox.information(self, "Question", "是否删除元素" + str(self.currElement + 1),
                                      QMessageBox.Yes | QMessageBox.No)
        if ret == QMessageBox.Yes:
            self.voucher.delElement(self.currElement)
            QMessageBox.information(self, "Question", "删除" + str(self.currElement + 1), QMessageBox.Yes)
            self.edited = True
        # 完毕后取消当前元素选定
        self.currElement = -1
        self.update()

    # 设置当前元素，双击或右击时调用
    def setCurrElementByMouse(self, ev):
        if self.voucher is None:
            return False
        pos = ev.pos()  # 得到鼠标位置
        virtualpos = QPoint(pos.x() - self.startPoint.x(), pos.y() - self.startPoint.y())
        self.currElement = -1
        for i in range(0, self.voucher.getElementNumbers()):
            em = self.voucher.getElement(i)
            if em.contains(virtualpos):  # 鼠标在矩形中
                self.currElement = i
                break

        if self.currElement >= 0:
            return True
        else:
            return False

    # 修改元素属性动作
    def actionHandlerModify(self):
        self.modifyElement()

    # 删除当前元素动作
    def actionHandlerDelete(self):
        self.deleteElement()

        # 左对齐

    def actionHandlerAlignLeft(self):
        if not self.getMultiSelect():
            return
        self.edited = True
        lst = self.getMultiSelectList()
        em = self.voucher.getElement(lst[0])  # 按第一个元素对齐
        x = em.getStartPoint().x()
        for i in lst:
            em = self.voucher.getElement(i)
            em.movedist(x - em.getStartPoint().x(), 0)
            self.voucher.updateElement(i, em)
        self.setMultiSelect(False)
        self.update()

    # 右对齐
    def actionHandlerAlignRight(self):
        if not self.getMultiSelect():
            return
        self.edited = True
        lst = self.getMultiSelectList()
        em = self.voucher.getElement(lst[0])  # 按第一个元素对齐
        x = em.getStartPoint().x() + em.getWidth()
        for i in lst:
            em = self.voucher.getElement(i)
            em.movedist(x - em.getWidth() - em.getStartPoint().x(), 0)
            self.voucher.updateElement(i, em)
        self.setMultiSelect(False)
        self.update()

    # 上对齐
    def actionHandlerAlignTop(self):
        if not self.getMultiSelect():
            return
        self.edited = True
        lst = self.getMultiSelectList()
        em = self.voucher.getElement(lst[0])  # 按第一个元素对齐
        y = em.getStartPoint().y()
        for i in lst:
            em = self.voucher.getElement(i)
            em.movedist(0, y - em.getStartPoint().y())
            self.voucher.updateElement(i, em)
        self.setMultiSelect(False)
        self.update()

    # 下对齐
    def actionHandlerAlignBottom(self):
        if not self.getMultiSelect():
            return
        self.edited = True
        lst = self.getMultiSelectList()
        em = self.voucher.getElement(lst[0])  # 按第一个元素对齐
        y = em.getStartPoint().y() + em.getHeight()
        for i in lst:
            em = self.voucher.getElement(i)
            em.movedist(0, y - em.getHeight() - em.getStartPoint().y())
            self.voucher.updateElement(i, em)
        self.setMultiSelect(False)
        self.update()

    # 相同宽度
    def actionHandlerSameWidth(self):
        if not self.getMultiSelect():
            return
        self.edited = True
        lst = self.getMultiSelectList()
        em = self.voucher.getElement(lst[0])  # 按第一个元素对齐
        w = em.getWidth()
        for i in lst:
            em = self.voucher.getElement(i)
            em.setWidth(w)
            self.voucher.updateElement(i, em)
        self.setMultiSelect(False)
        self.update()

    # 相同高度
    def actionHandlerSameHeight(self):
        if not self.getMultiSelect():
            return
        self.edited = True
        lst = self.getMultiSelectList()
        em = self.voucher.getElement(lst[0])  # 按第一个元素对齐
        h = em.getHeight()
        for i in lst:
            em = self.voucher.getElement(i)
            em.setHeight(h)
            self.voucher.updateElement(i, em)
        self.setMultiSelect(False)
        self.update()

    # 取消多选
    def actionHandlerMultiCancel(self):
        self.setMultiSelect(False)
        self.update()
