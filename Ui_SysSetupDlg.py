# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Works\Python\SimplePrint\SysSetupDlg.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_SysSetupDlg(object):
    def setupUi(self, SysSetupDlg):
        SysSetupDlg.setObjectName("SysSetupDlg")
        SysSetupDlg.resize(341, 182)
        SysSetupDlg.setSizeGripEnabled(True)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout(SysSetupDlg)
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.groupBox = QtWidgets.QGroupBox(SysSetupDlg)
        self.groupBox.setObjectName("groupBox")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.groupBox)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.edtLeftMargin = QtWidgets.QLineEdit(self.groupBox)
        self.edtLeftMargin.setObjectName("edtLeftMargin")
        self.horizontalLayout.addWidget(self.edtLeftMargin)
        self.label_3 = QtWidgets.QLabel(self.groupBox)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.edtTopMargin = QtWidgets.QLineEdit(self.groupBox)
        self.edtTopMargin.setObjectName("edtTopMargin")
        self.horizontalLayout_2.addWidget(self.edtTopMargin)
        self.label_4 = QtWidgets.QLabel(self.groupBox)
        self.label_4.setObjectName("label_4")
        self.horizontalLayout_2.addWidget(self.label_4)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.cbBatchPrint = QtWidgets.QCheckBox(self.groupBox)
        self.cbBatchPrint.setObjectName("cbBatchPrint")
        self.verticalLayout.addWidget(self.cbBatchPrint)
        self.horizontalLayout_4.addLayout(self.verticalLayout)
        self.verticalLayout_2.addWidget(self.groupBox)
        spacerItem = QtWidgets.QSpacerItem(20, 40, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Expanding)
        self.verticalLayout_2.addItem(spacerItem)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem1)
        self.btnOK = QtWidgets.QPushButton(SysSetupDlg)
        self.btnOK.setObjectName("btnOK")
        self.horizontalLayout_3.addWidget(self.btnOK)
        self.btnCancel = QtWidgets.QPushButton(SysSetupDlg)
        self.btnCancel.setObjectName("btnCancel")
        self.horizontalLayout_3.addWidget(self.btnCancel)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_5.addLayout(self.verticalLayout_2)

        self.retranslateUi(SysSetupDlg)
        self.btnCancel.clicked.connect(SysSetupDlg.reject)
        QtCore.QMetaObject.connectSlotsByName(SysSetupDlg)

    def retranslateUi(self, SysSetupDlg):
        _translate = QtCore.QCoreApplication.translate
        SysSetupDlg.setWindowTitle(_translate("SysSetupDlg", "打印设置"))
        self.groupBox.setTitle(_translate("SysSetupDlg", "参数"))
        self.label.setText(_translate("SysSetupDlg", "打印机默认左边距："))
        self.edtLeftMargin.setInputMask(_translate("SysSetupDlg", "99"))
        self.label_3.setText(_translate("SysSetupDlg", "（点）"))
        self.label_2.setText(_translate("SysSetupDlg", "打印机默认上边距："))
        self.edtTopMargin.setInputMask(_translate("SysSetupDlg", "99"))
        self.label_4.setText(_translate("SysSetupDlg", "（点）"))
        self.cbBatchPrint.setText(_translate("SysSetupDlg", "批量打印文件数据包含标题行（数据从第二行开始）"))
        self.btnOK.setText(_translate("SysSetupDlg", "确认"))
        self.btnCancel.setText(_translate("SysSetupDlg", "取消"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    SysSetupDlg = QtWidgets.QDialog()
    ui = Ui_SysSetupDlg()
    ui.setupUi(SysSetupDlg)
    SysSetupDlg.show()
    sys.exit(app.exec_())

