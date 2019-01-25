# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'BatchPrintDlg.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_BatchPrintDlg(object):
    def setupUi(self, BatchPrintDlg):
        BatchPrintDlg.setObjectName("BatchPrintDlg")
        BatchPrintDlg.resize(708, 512)
        BatchPrintDlg.setSizeGripEnabled(True)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(BatchPrintDlg)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(BatchPrintDlg)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.edtFileName = QtWidgets.QLineEdit(BatchPrintDlg)
        self.edtFileName.setEnabled(False)
        self.edtFileName.setObjectName("edtFileName")
        self.horizontalLayout.addWidget(self.edtFileName)
        self.btnOpenFile = QtWidgets.QPushButton(BatchPrintDlg)
        self.btnOpenFile.setObjectName("btnOpenFile")
        self.horizontalLayout.addWidget(self.btnOpenFile)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.label_2 = QtWidgets.QLabel(BatchPrintDlg)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.edtTotalPages = QtWidgets.QLineEdit(BatchPrintDlg)
        self.edtTotalPages.setEnabled(False)
        self.edtTotalPages.setMaximumSize(QtCore.QSize(50, 16777215))
        self.edtTotalPages.setObjectName("edtTotalPages")
        self.horizontalLayout_2.addWidget(self.edtTotalPages)
        self.label_3 = QtWidgets.QLabel(BatchPrintDlg)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_2.addWidget(self.label_3)
        self.edtBeginPage = QtWidgets.QLineEdit(BatchPrintDlg)
        self.edtBeginPage.setMaximumSize(QtCore.QSize(50, 16777215))
        self.edtBeginPage.setObjectName("edtBeginPage")
        self.horizontalLayout_2.addWidget(self.edtBeginPage)
        self.label_4 = QtWidgets.QLabel(BatchPrintDlg)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_2.addWidget(self.label_4)
        self.edtEndPage = QtWidgets.QLineEdit(BatchPrintDlg)
        self.edtEndPage.setMaximumSize(QtCore.QSize(50, 16777215))
        self.edtEndPage.setObjectName("edtEndPage")
        self.horizontalLayout_2.addWidget(self.edtEndPage)
        self.btnPrint = QtWidgets.QPushButton(BatchPrintDlg)
        self.btnPrint.setObjectName("btnPrint")
        self.horizontalLayout_2.addWidget(self.btnPrint)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.tvContent = QtWidgets.QTableView(BatchPrintDlg)
        self.tvContent.setObjectName("tvContent")
        self.verticalLayout.addWidget(self.tvContent)
        self.horizontalLayout_3.addLayout(self.verticalLayout)

        self.retranslateUi(BatchPrintDlg)
        QtCore.QMetaObject.connectSlotsByName(BatchPrintDlg)

    def retranslateUi(self, BatchPrintDlg):
        _translate = QtCore.QCoreApplication.translate
        BatchPrintDlg.setWindowTitle(_translate("BatchPrintDlg", "批量打印"))
        self.label.setText(_translate("BatchPrintDlg", "批量打印文件："))
        self.btnOpenFile.setText(_translate("BatchPrintDlg", "选择"))
        self.label_2.setText(_translate("BatchPrintDlg", "总页数："))
        self.label_3.setText(_translate("BatchPrintDlg", "打印起始页："))
        self.edtBeginPage.setInputMask(_translate("BatchPrintDlg", "9999"))
        self.label_4.setText(_translate("BatchPrintDlg", "终止页："))
        self.edtEndPage.setInputMask(_translate("BatchPrintDlg", "9999"))
        self.btnPrint.setText(_translate("BatchPrintDlg", "打印"))

