# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Works\python\SimplePrint\ImportVoucherDlg.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_ImportVoucherDlg(object):
    def setupUi(self, ImportVoucherDlg):
        ImportVoucherDlg.setObjectName("ImportVoucherDlg")
        ImportVoucherDlg.resize(412, 175)
        ImportVoucherDlg.setSizeGripEnabled(True)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(ImportVoucherDlg)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.groupBox = QtWidgets.QGroupBox(ImportVoucherDlg)
        self.groupBox.setTitle("")
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.groupBox)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.label_2 = QtWidgets.QLabel(self.groupBox)
        self.label_2.setObjectName("label_2")
        self.horizontalLayout_2.addWidget(self.label_2)
        self.edtfilename = QtWidgets.QLineEdit(self.groupBox)
        self.edtfilename.setEnabled(False)
        self.edtfilename.setReadOnly(False)
        self.edtfilename.setObjectName("edtfilename")
        self.horizontalLayout_2.addWidget(self.edtfilename)
        self.btnopenfile = QtWidgets.QToolButton(self.groupBox)
        self.btnopenfile.setObjectName("btnopenfile")
        self.horizontalLayout_2.addWidget(self.btnopenfile)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.groupBox)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.edtName = QtWidgets.QLineEdit(self.groupBox)
        self.edtName.setEnabled(False)
        self.edtName.setObjectName("edtName")
        self.horizontalLayout.addWidget(self.edtName)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.label_7 = QtWidgets.QLabel(self.groupBox)
        self.label_7.setObjectName("label_7")
        self.horizontalLayout_6.addWidget(self.label_7)
        self.edtDisplayText = QtWidgets.QLineEdit(self.groupBox)
        self.edtDisplayText.setEnabled(False)
        self.edtDisplayText.setObjectName("edtDisplayText")
        self.horizontalLayout_6.addWidget(self.edtDisplayText)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_6 = QtWidgets.QLabel(self.groupBox)
        self.label_6.setObjectName("label_6")
        self.horizontalLayout_4.addWidget(self.label_6)
        self.cmbType = QtWidgets.QComboBox(self.groupBox)
        self.cmbType.setMinimumSize(QtCore.QSize(150, 0))
        self.cmbType.setObjectName("cmbType")
        self.horizontalLayout_4.addWidget(self.cmbType)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        spacerItem1 = QtWidgets.QSpacerItem(373, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem1)
        self.btnOK = QtWidgets.QPushButton(self.groupBox)
        self.btnOK.setObjectName("btnOK")
        self.horizontalLayout_5.addWidget(self.btnOK)
        self.btnCancel = QtWidgets.QPushButton(self.groupBox)
        self.btnCancel.setObjectName("btnCancel")
        self.horizontalLayout_5.addWidget(self.btnCancel)
        self.verticalLayout.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_3.addWidget(self.groupBox)

        self.retranslateUi(ImportVoucherDlg)
        self.btnCancel.clicked.connect(ImportVoucherDlg.reject)
        self.btnOK.clicked.connect(ImportVoucherDlg.accept)
        QtCore.QMetaObject.connectSlotsByName(ImportVoucherDlg)

    def retranslateUi(self, ImportVoucherDlg):
        _translate = QtCore.QCoreApplication.translate
        ImportVoucherDlg.setWindowTitle(_translate("ImportVoucherDlg", "导入模板"))
        self.label_2.setText(_translate("ImportVoucherDlg", "模板文件："))
        self.btnopenfile.setText(_translate("ImportVoucherDlg", "..."))
        self.label.setText(_translate("ImportVoucherDlg", "凭证名称："))
        self.label_7.setText(_translate("ImportVoucherDlg", "显示名称："))
        self.label_6.setText(_translate("ImportVoucherDlg", "凭证类别："))
        self.btnOK.setText(_translate("ImportVoucherDlg", "确认"))
        self.btnCancel.setText(_translate("ImportVoucherDlg", "取消"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    ImportVoucherDlg = QtWidgets.QDialog()
    ui = Ui_ImportVoucherDlg()
    ui.setupUi(ImportVoucherDlg)
    ImportVoucherDlg.show()
    sys.exit(app.exec_())

