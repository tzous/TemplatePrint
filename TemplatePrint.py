# -*- coding: utf-8 -*-
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtPrintSupport import QPrinter, QPrintDialog

import sys
import os
import os.path
import shutil
from MyTools import MyTools
import six
import packaging
import packaging.version
import packaging.specifiers
import packaging.requirements

from SysData import SysData  # 系统参数类
from Voucher import Voucher  # 模板类
from PrintCanvas import PrintCanvas  # 打印录入部件
from PrintLog import PrintLog  # 打印历史纪录
from Ui_MainWindow import Ui_MainWindow  # 主窗口
from DesignWindow import DesignWindow  # 模板设计窗口
from BatchPrintDlg import BatchPrintDlg  # 批量打印对话框
from ImportVoucherDlg import ImportVoucherDlg  # 模板导入对话框
from TypeManageDlg import TypeManageDlg  # 类别管理对话框
from SysSetupDlg import SysSetupDlg  # 打印参数设置对话框
from PrintLogDlg import PrintLogDlg  # 数据仓库对话框
from TypeSelectDlg import TypeSelectDlg  # 类别选择对话框
from TypeNameDlg import TypeNameDlg  # 类别名称对话框


class MainWindow(QMainWindow, Ui_MainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()
        self.setupUi(self)
        self.sysData = SysData()  # 系统参数
        self.voucher = None  # 当前模板
        self.curvid = -1  # 当前模板ID
        self.currtype = None  # 当前模板所属类别
        self.typelist = []  # 树形控件中的分组列表
        self.voucherlist = []  # 树形控件中的模板列表
        self.printlog = PrintLog()  # 打印历史纪录

        self.initData()  # 初始化系统数据
        self.initEventPlot()  # 初始化事件
        self.printCanvas = PrintCanvas(parent=self)  # 凭证显示输入画板
        self.scrollArea.setWidget(self.printCanvas)

        # 初始化模板设计窗口
        self.DesignWindow = DesignWindow(self.refreshModel, self)  # 保存新模板后需要刷新模板列表

    def initEventPlot(self):
        # 新建模板
        self.btnModNew.clicked.connect(self.onClickedbtnModNew)
        self.actionmenuModNew.triggered.connect(self.onClickedbtnModNew)
        # 修改模板
        self.btnModModi.clicked.connect(self.onClickedbtnModModi)
        self.actionmenuModModify.triggered.connect(self.onClickedbtnModModi)
        # 删除模板
        self.btnModDel.clicked.connect(self.onClickedbtnModDel)
        self.actionmenuModDelete.triggered.connect(self.onClickedbtnModDel)
        # 模板类别管理
        self.btnModType.clicked.connect(self.onClickedbtnModType)
        self.actionmenuType.triggered.connect(self.onClickedbtnModType)

        # 模板列表控件事件
        self.treeWidget.clicked.connect(self.onClickedTreeWidget)
        # 模板查询按钮
        self.btnQuery.clicked.connect(self.onClickedbtnQuery)
        # 单张打印
        self.btnPrintSingle.clicked.connect(self.onClickedbtnPrintSingle)
        # 重新录入
        self.btnPrintNewData.clicked.connect(self.onClickedbtnPrintNewData)
        # 导出模板
        self.btnModExp.clicked.connect(self.onClickedbtnModExp)
        self.actionmodexport.triggered.connect(self.onClickedbtnModExp)
        # 导入模板
        self.btnModLoad.clicked.connect(self.onClickedbtnModLoad)
        self.actionmodload.triggered.connect(self.onClickedbtnModLoad)
        # 批量打印
        self.btnBatchPrint.clicked.connect(self.onClickedbtnBatchPrint)
        # 打印参数设置
        self.btnPrintSetup.clicked.connect(self.onClickedbtnPrintSetup)
        self.actionprintsetup.triggered.connect(self.onClickedbtnPrintSetup)
        # 保存打印数据
        self.btnPrintSaveData.clicked.connect(self.onClickedbtnPrintSaveData)
        # 票据仓库
        self.btnPrintDatas.clicked.connect(self.onClickedbtnPrintDatas)
        self.actionprintdatas.triggered.connect(self.onClickedbtnPrintDatas)

        # 关于...
        self.actionabout.triggered.connect(self.ontriggeredAbout)
        # 帮助
        self.actionhelp.triggered.connect(self.ontriggeredHelp)

        # 树形控件右键菜单
        # self.treeWidget.setMouseTracking(True)#保证得到鼠标信息

        self.treeWidget.setContextMenuPolicy(Qt.CustomContextMenu)
        self.treeWidget.customContextMenuRequested.connect(self.showContextMenu)
        self.contextMenu = QMenu(self)  # 模板右键菜单
        self.actionModify = self.contextMenu.addAction('更改模板')
        self.actionMove = self.contextMenu.addAction('变更类别')
        self.actionExport = self.contextMenu.addAction('导出模板')
        self.contextMenu.addSeparator()
        self.actionDelete = self.contextMenu.addAction('删除模板')
        self.actionModify.triggered.connect(self.onClickedbtnModModi)
        self.actionDelete.triggered.connect(self.onClickedbtnModDel)
        self.actionMove.triggered.connect(self.onactionMove)
        self.actionExport.triggered.connect(self.onClickedbtnModExp)

        self.contextMenuType = QMenu(self)  # 类别右键菜单
        self.actionNewMod = self.contextMenuType.addAction('新建模板')
        self.contextMenuType.addSeparator()
        self.actionNewType = self.contextMenuType.addAction('新增类别')
        self.actionModifyType = self.contextMenuType.addAction('类别改名')
        self.contextMenuType.addSeparator()
        self.actionDeleteType = self.contextMenuType.addAction('删除类别')
        self.actionNewMod.triggered.connect(self.onClickedbtnModNew)
        self.actionNewType.triggered.connect(self.onactionNewType)
        self.actionModifyType.triggered.connect(self.onactionModifyType)
        self.actionDeleteType.triggered.connect(self.onactionDeleteType)

    # 初始化系统数据，简单处理，直接调用
    def initData(self):
        self.refreshModel()

    # 模板列表控件单击事件
    def onClickedTreeWidget(self):
        item = self.treeWidget.currentItem()
        if item in self.voucherlist:
            self.voucher = Voucher()
            self.voucher.load(self.sysData.templatePath, item.text(5))  # 按凭证名称导入凭证模板信息
            self.voucher.offsetx = int(item.text(3))  # 打印偏移量，在本地系统数据中，所以要另外赋值
            self.voucher.offset = int(item.text(4))
            self.currtype = int(item.text(2))  # 读入当前模板所属的类别
            self.curvid = int(item.text(1))  # 读入当前模板ID
            self.printCanvas.setVoucher(self.voucher)
            self.printCanvas.setMinimumSize(QSize(self.voucher.pixelWidth, self.voucher.pixelHeight))  # 滚动条
            self.printCanvas.initUi()
            self.printCanvas.update()
        elif item in self.typelist:
            self.currtype = int(item.text(1))  # 读入当前类别ID

    # 新建模板
    def onClickedbtnModNew(self):
        self.voucher = None   #当前凭证设为None
        self.treeWidget.clearSelection()   #清除模板列表选择
        self.printCanvas.setVoucher(None)  # 凭证显示输入画板重置
        self.printCanvas.initUi()    #打印数据录入画板初始化，更新显示
        self.printCanvas.update()

        self.DesignWindow.show()    #显示模板设计窗口
        if self.currtype != None:
            self.DesignWindow.currType = self.currtype
        self.DesignWindow.clickedbtnNewModel()    #执行新建模板功能

    # 修改模板
    def onClickedbtnModModi(self):
        if self.voucher == None:
            return
        self.DesignWindow.voucher = self.voucher  # 当前模板
        self.DesignWindow.designCanvas.setVoucher(self.voucher)
        self.DesignWindow.designCanvas.setMinimumSize(
            QSize(self.voucher.pixelWidth, self.voucher.pixelHeight))  # 设置窗口大小
        self.DesignWindow.setBtnEnabled(True)  # 激活工具栏按钮
        self.DesignWindow.currType = self.currtype  # 得到当前类别
        self.DesignWindow.newmod = False  # 置新模板状态
        self.DesignWindow.edited = True  # 置模板可编辑状态
        self.DesignWindow.designCanvas.update()  # 刷新，显示模板设计窗口
        self.DesignWindow.show()

    # 删除模板
    def onClickedbtnModDel(self):
        if self.voucher == None:
            return
        ret = QMessageBox.information(self, "Question", "是否删除当前模板？", QMessageBox.Yes | QMessageBox.No)
        if ret != QMessageBox.Yes:
            return
        # 按类别及模板名称删除系统库中模板信息，初始化当前模板等数据
        self.sysData.DeleteVoucherByTypeIDName(self.currtype, self.voucher.name)
        self.voucher = None
        self.currtype = None
        self.printCanvas.setVoucher(None)  # 凭证显示输入画板重置
        self.printCanvas.initUi()
        self.printCanvas.update()
        self.refreshModel()  # 刷新

    # 模板类别管理
    def onClickedbtnModType(self):
        dlg = TypeManageDlg()
        dlg.exec_()
        self.refreshModel()

    # 刷新树形控件模板列表及字段录入模板
    def refreshModel(self):
        self.typelist = []  # 树形控件中的分组列表
        self.voucherlist = []  # 树形控件中的模板列表
        self.sysData.loadSysData()  # 重新读取系统数据
        self.treeWidget.clear()  # 清空树形控件
        self.treeWidget.setColumnCount(6)  # 设表头为6列
        # 设置头部信息，
        # self.treeWidget.setHeaderLabels(['Key','Value1','Value2'])
        self.treeWidget.setColumnWidth(0, 230)  # 第一列宽度超过控件宽度，目的是使后面几列不显示
        self.treeWidget.setColumnWidth(1, 50)  # 第二列不显示
        self.treeWidget.setColumnWidth(2, 50)  # 第三列不显示
        self.treeWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # 水平滚动条关闭
        self.treeWidget.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)  # 垂直滚动条需要时出现
        self.treeWidget.setHeaderLabels(["模板列表"])
        for t in self.sysData.types:
            if t[2] == 0:  # 添加类别
                child = QTreeWidgetItem(self.treeWidget)
                child.setText(0, t[1])  # 类别名称
                child.setText(1, str(t[0]))  # 类别编号ID
                child.setText(2, str(t[2]))  # 父类别编号
                child.setText(3, '')  #
                child.setText(4, '')  #
                child.setText(5, '')  #
                self.typelist.append(child)

                for v in self.sysData.vouchers:
                    if v[3] == t[0]:  # 添加模板信息
                        child1 = QTreeWidgetItem(child)
                        child1.setText(0, v[2])  # 凭证显示名称
                        child1.setText(1, str(v[0]))  # 凭证编号ID
                        child1.setText(2, str(v[3]))  # 凭证类别编号
                        child1.setText(3, str(v[4]))  # 横向偏移量，不用
                        child1.setText(4, str(v[5]))  # 纵向偏移量，不用
                        child1.setText(5, v[1])  # 凭证名称
                        self.voucherlist.append(child1)
        # 以下为刷新字段录入画板
        if self.voucher == None:
            return
        self.voucher.load(self.sysData.templatePath, self.voucher.name)  # 按凭证名称重新导入凭证模板信息,用于模板修改后刷新屏幕
        self.printCanvas.setVoucher(self.voucher)
        self.printCanvas.setMinimumSize(QSize(self.voucher.pixelWidth, self.voucher.pixelHeight))
        self.printCanvas.initUi()
        self.printCanvas.update()

        # 查询模板

    def onClickedbtnQuery(self):
        queryString = self.lineEditQuery.text()
        if queryString == '':  # 查询关键字为空，则默认全部
            self.refreshModel()
            return
        self.typelist = []  # 树形控件中的分组列表
        self.voucherlist = []  # 树形控件中的模板列表
        self.treeWidget.clear()  # 清空树形控件
        self.treeWidget.setColumnCount(6)
        # 设置头部信息，因为上面设置列数为3，所以要设置三个标识符
        # self.treeWidget.setHeaderLabels(['Key','Value1','Value2'])
        self.treeWidget.setColumnWidth(0, 230)  # 第一列宽度超过控件宽度，目的是使后面几列不显示
        self.treeWidget.setColumnWidth(1, 50)  # 第二列不显示
        self.treeWidget.setColumnWidth(2, 50)  # 第三列不显示
        self.treeWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)  # 水平滚动条关闭
        self.treeWidget.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)  # 垂直滚动条需要时出现
        self.treeWidget.setHeaderLabels(["模板列表"])
        for v in self.sysData.vouchers:
            if v[2].find(queryString) >= 0:
                child1 = QTreeWidgetItem(self.treeWidget)
                child1.setText(0, v[2])  # 凭证显示名称
                child1.setText(1, str(v[0]))  # 凭证编号
                child1.setText(2, str(v[3]))  # 凭证类别编号
                child1.setText(3, str(v[4]))  # 横向偏移量
                child1.setText(4, str(v[5]))  # 纵向偏移量
                child1.setText(5, v[1])  # 凭证名称
                self.voucherlist.append(child1)

    # 单笔打印
    def onClickedbtnPrintSingle(self):
        if self.voucher == None:
            return
        self.printer = QPrinter()  # 初始化QPrinter实例
        self.printer.setPageSize(QPrinter.A4)  # 打印纸默认使用A4纸
        # self.printer.setPageSize(QPrinter.Custom) #自定义纸张大小
        # self.printer.setPaperSize(QSizeF(self.voucher.pixelWidth,self.voucher.pixelHeight),QPrinter.Point)
        dialog = QPrintDialog(self.printer, self)  # 选择打印机
        if not dialog.exec_():
            return

        painter = QPainter(self.printer)  # 生成画笔

        for i in range(0, self.voucher.getElementNumbers()):
            em = self.voucher.getElement(i)  # 将输入控件值读到每个元素中，只分2种情况
            txt = ''
            if em.type == 'check':
                if self.printCanvas.elementList[i].isChecked():
                    txt = em.checkVal
            else:
                txt = self.printCanvas.elementList[i].text()
            em.setVal(txt)
            self.voucher.updateElement(i, em)

        self.voucher.leftmargin = self.sysData.leftmargin  # 打印机默认上下边距，该偏移量由本地打印设置进行配置
        self.voucher.topmargin = self.sysData.topmargin

        painter.save()
        self.voucher.paintElements(painter)  # 调用模板元素打印功能
        painter.restore()
        QMessageBox.information(self, "Information", "单笔打印完成", QMessageBox.Ok)

    # 清初控件输入内容，重新录入
    def onClickedbtnPrintNewData(self):
        ret = QMessageBox.information(self, "Question", "是否清初当前录入的所有内容？", QMessageBox.Yes | QMessageBox.No)
        if ret != QMessageBox.Yes:
            return
        self.printCanvas.initUi()

    # 导出模板，实际操作就是将模板拷入指定文件夹
    def onClickedbtnModExp(self):
        if self.voucher == None:
            return
        filename, _ = QFileDialog.getSaveFileName(self, '请输入导出模板名称', '', '模板 (*.tdb)')
        if filename:
            sourcefile = self.sysData.templatePath + self.voucher.name + ".tdb"
            shutil.copy(sourcefile, targetfile)
            QMessageBox.information(self, "Information", "导出完成", QMessageBox.Ok)

    # 导入模板，实际操作就是从其他文件夹将模板文件拷入系统，并写入系统库
    def onClickedbtnModLoad(self):
        dlg = ImportVoucherDlg()
        if dlg.exec_():
            sourcefile = dlg.edtfilename.text()
            targetfile = self.sysData.templatePath + dlg.edtName.text() + ".tdb"
            if os.path.exists(targetfile):  # 模板库存在
                ret = QMessageBox.information(self, "Question", "模板库中已存在相同名称模板，是否覆盖？", QMessageBox.Yes | QMessageBox.No)
                if ret != QMessageBox.Yes:
                    return
            shutil.copy(sourcefile, targetfile)  # 拷贝文件
            voucher = Voucher()
            voucher.load(self.sysData.templatePath, dlg.edtName.text())  # 按凭证名称导入凭证模板信息
            self.sysData.SaveNewVoucher(voucher, dlg.getCurrType())  # 写入系统库
            self.refreshModel()

    # 批量打印，调用批量打印对话框，打印前需先选择当前模板
    def onClickedbtnBatchPrint(self):
        if self.voucher == None:
            return
        self.voucher.leftmargin = self.sysData.leftmargin
        self.voucher.topmargin = self.sysData.topmargin

        dlg = BatchPrintDlg()
        dlg.voucher = self.voucher
        dlg.exec_()

    # 打印参数设置
    def onClickedbtnPrintSetup(self):
        dlg = SysSetupDlg()
        dlg.exec_()
        self.sysData.loadSysData()  # 设置完成后，重新读入系统数据

    # 保存打印数据到打印数据仓库
    def onClickedbtnPrintSaveData(self):
        if self.voucher == None:
            return

        for i in range(0, self.voucher.getElementNumbers()):
            em = self.voucher.getElement(i)
            txt = ''
            if em.type == 'check':  # 从控件中获取输入值
                if self.printCanvas.elementList[i].isChecked():
                    txt = em.checkVal
            else:
                txt = self.printCanvas.elementList[i].text()
            em.setVal(txt)
            self.voucher.updateElement(i, em)

        log = PrintLog()
        log.savePrintLog(self.voucher)
        QMessageBox.information(self, "Information", "已保存到打印数据仓库", QMessageBox.Ok)

    # 票据仓库，可以从中选择历史打印数据用于重新打印，或者清理打印历史记录
    def onClickedbtnPrintDatas(self):
        dlg = PrintLogDlg()
        if dlg.exec_():
            if dlg.logdatas == []:
                return
            self.voucher = Voucher()
            self.voucher.load(self.sysData.templatePath, dlg.logdatas[2])
            if self.voucher == None:
                QMessageBox.information(self, "Erroe", "打开凭证模板出错！", QMessageBox.Ok)
                return

            for i in range(0, self.voucher.getElementNumbers()):
                em = self.voucher.getElement(i)
                txt = dlg.emdatas[i][2]  # 从录入明细中获得输入值，更新至输入控件中
                em.setVal(txt)
                self.voucher.updateElement(i, em)

            # 刷新当前模板显示录入画板
            self.printCanvas.setVoucher(self.voucher)
            self.printCanvas.setMinimumSize(QSize(self.voucher.pixelWidth, self.voucher.pixelHeight))
            self.printCanvas.initUi()
            self.printCanvas.initUiData()
            self.printCanvas.update()

            # About...

    def ontriggeredAbout(self):
        QMessageBox.information(self, "About...", "欢迎使用套打助手\r\n联系方式：tzous@126.com", QMessageBox.Ok)

    # Help
    def ontriggeredHelp(self):
        os.system(self.sysData.dataPath + 'help.doc')

    # 移动模板到其他类别中
    def onactionMove(self):
        dlg = TypeSelectDlg()
        if dlg.exec_():
            if dlg.curTypeid == -1:
                return
            self.sysData.UpdateVoucherType(self.curvid, dlg.curTypeid)
            self.refreshModel()  # 移动后刷新窗口

    # 新增类别
    def onactionNewType(self):
        dlg = TypeNameDlg()
        if dlg.exec_():
            mytools = MyTools()
            typeName = mytools.trim(dlg.edtTypeName.text())
            if typeName == '':
                return
            self.sysData.SaveNewType(typeName)
            self.refreshModel()  # 新增后刷新窗口

    # 修改类别名称
    def onactionModifyType(self):
        dlg = TypeNameDlg()
        if dlg.exec_():
            mytools = MyTools()
            typeName = mytools.trim(dlg.edtTypeName.text())
            if typeName == '':
                return
            self.sysData.UpdateTypeByID(self.currtype, typeName)
            self.refreshModel()  # 修改后刷新窗口

    # 删除类别
    def onactionDeleteType(self):
        ret = QMessageBox.information(self, "Question", "是否删除当前类别？", QMessageBox.Yes | QMessageBox.No)
        if ret != QMessageBox.Yes:
            return
        ret = self.sysData.DeleteTypeByID(self.currtype)
        if ret < 0:
            QMessageBox.information(self, "Information", "当前类别下有模板，不能删除！", QMessageBox.Ok)
        else:
            self.refreshModel()  # 删除后刷新窗口

    # 树形控件右键事件
    def showContextMenu(self, ev):
        item = self.treeWidget.itemAt(ev)  # ev为鼠标右击位置，相对于控件内部的QPoint
        if item == None:                   #不是点在树控件的项目上，则清除当前选择
            self.treeWidget.clearSelection()
            return
        self.onClickedTreeWidget()  # 先执行左键单击事件，设定当前模板等信息
        item = self.treeWidget.currentItem()
        pos = QCursor.pos()  # 使用当前鼠标位置，相对于屏幕的QPoint对象
        if item in self.voucherlist:  # 右击了模板名
            self.contextMenu.exec_(pos)  # 在当前模板名称位置显示
        elif item in self.typelist:  # 右击了类别名
            self.contextMenuType.exec_(pos)  # 在当前类别名称位置显示


if __name__ == '__main__':
    app = QApplication(sys.argv)
    dlg = MainWindow()
    dlg.show()
    sys.exit(app.exec_())
