# -*- coding: utf-8 -*-
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtWidgets
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog

from Ui_DesignWindow import Ui_DesignWindow  # 模板设计窗口
from DesignCanvas import DesignCanvas  # 画板
from Voucher import Voucher, Element  # 模板类
from NewVoucherDlg import NewVoucherDlg  # 新建模板对话框
from SysData import SysData

import base64


# noinspection SpellCheckingInspection,PyAttributeOutsideInit
class DesignWindow(QtWidgets.QMainWindow, Ui_DesignWindow):

    def __init__(self, callback, parent=None):
        super(DesignWindow, self).__init__(parent)
        self.callback = callback  # 回调函数
        self.setupUi(self)
        self.initUi()
        self.initEventPlot()
        self.setBtnEnabled(False)  # 初始化disable按钮
        self.voucher = None  # 凭证模板
        self.currType = 0  # 当前凭证类别
        self.edited = False  # 是否处于编辑状态
        self.newmod = False  # 是否新模板状态
        self.sysData = SysData()  # 系统参数

    # 自定义UI
    def initUi(self):
        self.statusBar.showMessage('模板设计')
        self.statusBar.show()
        self.labelCoordinates = QtWidgets.QLabel('')
        self.statusBar.addPermanentWidget(self.labelCoordinates)
        self.designCanvas = DesignCanvas(parent=self)
        self.scrollArea.setWidget(self.designCanvas)

    def setBtnEnabled(self, t):
        if t:
            tf = True
        else:
            tf = False
        self.btnAddItem.setEnabled(tf)
        self.btnLoadJpg.setEnabled(tf)
        self.btnDelJpg.setEnabled(tf)
        self.btnAlignLeft.setEnabled(tf)
        self.btnAlignRight.setEnabled(tf)
        self.btnAlignTop.setEnabled(tf)
        self.btnAlignBottom.setEnabled(tf)
        self.btnSameWidth.setEnabled(tf)
        self.btnSameHeight.setEnabled(tf)
        self.btnSaveModel.setEnabled(tf)
        self.btnPreview.setEnabled(tf)

    # 事件初始化
    def initEventPlot(self):
        # 新建模板
        self.btnNewModel.clicked.connect(self.clickedbtnNewModel)
        # 保存模板
        self.btnSaveModel.clicked.connect(self.clickedbtnSaveModel)
        # 退出
        self.btnCancel.clicked.connect(self.clickedbtnCancel)
        # 导入背景
        self.btnLoadJpg.clicked.connect(self.clickedbtnLoadJpg)
        # 删除背景
        self.btnDelJpg.clicked.connect(self.clickedbtnDelJpg)
        # 新增元素
        self.btnAddItem.clicked.connect(self.clickedbtnAddItem)
        # 左对齐
        self.btnAlignLeft.clicked.connect(self.clickedbtnAlignLeft)
        # 右对齐
        self.btnAlignRight.clicked.connect(self.clickedbtnAlignRight)
        # 上对齐
        self.btnAlignTop.clicked.connect(self.clickedbtnAlignTop)
        # 下对齐
        self.btnAlignBottom.clicked.connect(self.clickedbtnAlignBottom)
        # 相同宽度
        self.btnSameWidth.clicked.connect(self.clickedbtnSameWidth)
        # 相同高度
        self.btnSameHeight.clicked.connect(self.clickedbtnSameHeight)
        # 测试打印
        self.btnPreview.clicked.connect(self.clickedbtnPreview)

    # 新建模板
    def clickedbtnNewModel(self):
        self.designCanvas.setMultiSelect(False)  # 取消多选状态
        if (self.edited or self.designCanvas.edited) and self.voucher is not None:
            ret = QtWidgets.QMessageBox.information(self, "Question", "当前模板已更改，是否需要保存？",
                                                    QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            if ret == QtWidgets.QMessageBox.Yes:
                self.clickedbtnSaveModel()  # 保存模板
        # 后续初始化新模板操作
        newVoucherDlg = NewVoucherDlg()
        newVoucherDlg.setCurrType(self.currType)  # 设置下拉框类别
        if newVoucherDlg.exec_() == QtWidgets.QDialog.Accepted:
            self.voucher = Voucher()  # 读入模板信息
            self.voucher.setName(newVoucherDlg.edtName.text())
            self.voucher.setText(newVoucherDlg.edtDisplayText.text())
            self.voucher.setSize(int(newVoucherDlg.edtWidth.text()), int(newVoucherDlg.edtHeight.text()))
            self.currType = int(newVoucherDlg.getCurrType())
            self.newmod = True  # 新模板
            self.edited = True  # 置已编辑状态
            self.designCanvas.edited = True  # 置画板已编辑状态
            self.designCanvas.setVoucher(self.voucher)  # 设置模板到画板
            self.designCanvas.setMinimumSize(QSize(self.voucher.pixelWidth, self.voucher.pixelHeight))
            self.designCanvas.update()
            self.setBtnEnabled(True)  # 显示工具栏图标

    # 保存新模板
    def clickedbtnSaveModel(self):
        self.designCanvas.setMultiSelect(False)  # 取消多选状态
        if (self.edited or self.designCanvas.edited) and self.voucher is not None:
            # 模板保存处理
            if self.sysData.existVoucher(self.voucher.name) and self.newmod:
                ret = QtWidgets.QMessageBox.information(self, "Question", "当前库中存在相同名称的模板，是否覆盖？",
                                                        QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
                if ret == QtWidgets.QMessageBox.No:
                    return
            # 保存到模板库中
            self.voucher.save(self.sysData.templatePath)
            if self.newmod:  # 模板修改或者已保存过，则无需再保存到系统库中
                # 保存到系统数据库中s
                self.sysData.saveNewVoucher(self.voucher, self.currType)
                self.newmod = False
            self.designCanvas.edited = False
            self.edited = False
            QtWidgets.QMessageBox.information(self, "Information", "保存完成", QtWidgets.QMessageBox.Ok)

            # 保存新模板后续处理，如刷新父窗口模板列表
            self.callback()

    # 退出
    def clickedbtnCancel(self):
        self.designCanvas.setMultiSelect(False)  # 取消多选状态
        if (self.edited or self.designCanvas.edited) and self.voucher is not None:
            ret = QtWidgets.QMessageBox.information(self, "Question", "当前模板已更改，是否需要保存？",
                                                    QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
            if ret == QtWidgets.QMessageBox.Yes:
                self.clickedbtnSaveModel()  # 保存
        # 删除当前模板信息
        self.voucher = None
        self.edited = False
        self.modified = False
        self.newmod = False
        self.designCanvas.setVoucher(None)
        self.designCanvas.update()
        self.setBtnEnabled(False)
        self.close()

    # 导入背景
    def clickedbtnLoadJpg(self):
        if self.voucher is None:  # 在已打开凭证模板的情况下才能操作
            return
        self.designCanvas.setMultiSelect(False)  # 取消多选状态
        filename, _ = QtWidgets.QFileDialog.getOpenFileName(self, '请选择凭证背景文件', '*.jpg')
        if filename:
            with open(filename, 'rb') as f:
                data = base64.b64encode(f.read())  # base64格式
            self.voucher.setBackground(data)
            self.edited = True
            self.designCanvas.update()

            # 删除背景

    def clickedbtnDelJpg(self):
        if self.voucher is None:  # 在已打开凭证模板的情况下才能操作
            return
        self.designCanvas.setMultiSelect(False)  # 取消多选状态
        ret = QtWidgets.QMessageBox.information(self, "Question", "是否从模板中删除当前背景图？",
                                                QtWidgets.QMessageBox.Yes | QtWidgets.QMessageBox.No)
        if ret == QtWidgets.QMessageBox.Yes:
            self.voucher.setBackground(None)
            self.edited = True
            self.designCanvas.update()

            # 新增元素

    def clickedbtnAddItem(self):
        if self.voucher is None:  # 在已打开凭证模板的情况下才能操作
            return
        self.designCanvas.setMultiSelect(False)  # 取消多选状态
        em = Element()  # 新元素
        self.voucher.appendElement(em)
        self.edited = True
        self.designCanvas.update()

        # 左对齐

    def clickedbtnAlignLeft(self):
        self.edited = True
        self.designCanvas.actionHandlerAlignLeft()

    # 右对齐
    def clickedbtnAlignRight(self):
        self.edited = True
        self.designCanvas.actionHandlerAlignRight()

    # 上对齐
    def clickedbtnAlignTop(self):
        self.edited = True
        self.designCanvas.actionHandlerAlignTop()

    # 下对齐
    def clickedbtnAlignBottom(self):
        self.edited = True
        self.designCanvas.actionHandlerAlignBottom()

    # 相同宽度
    def clickedbtnSameWidth(self):
        self.edited = True
        self.designCanvas.actionHandlerSameWidth()

    # 相同高度
    def clickedbtnSameHeight(self):
        self.edited = True
        self.designCanvas.actionHandlerSameHeight()

    # 测试打印
    def clickedbtnPreview(self):
        if self.voucher is None:  # 在已打开凭证模板的情况下才能操作
            return
        self.printer = QPrinter()
        self.printer.setPageSize(QPrinter.A4)
        dialog = QPrintDialog(self.printer, self)
        if not dialog.exec_():
            return

        painter = QPainter(self.printer)
        self.voucher.leftmargin = self.sysData.leftmargin
        self.voucher.topmargin = self.sysData.topmargin

        painter.save()
        self.voucher.paintElements(painter)  # 调用Voucher类元素打印功能
        painter.restore()
