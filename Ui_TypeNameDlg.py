# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Works\Python\SimplePrint\TypeNameDlg.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_TypeNameDlg(object):
    def setupUi(self, TypeNameDlg):
        TypeNameDlg.setObjectName("TypeNameDlg")
        TypeNameDlg.resize(310, 96)
        TypeNameDlg.setSizeGripEnabled(True)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(TypeNameDlg)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(TypeNameDlg)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.edtTypeName = QtWidgets.QLineEdit(TypeNameDlg)
        self.edtTypeName.setObjectName("edtTypeName")
        self.horizontalLayout.addWidget(self.edtTypeName)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.btnOK = QtWidgets.QPushButton(TypeNameDlg)
        self.btnOK.setObjectName("btnOK")
        self.horizontalLayout_2.addWidget(self.btnOK)
        self.btnCancel = QtWidgets.QPushButton(TypeNameDlg)
        self.btnCancel.setObjectName("btnCancel")
        self.horizontalLayout_2.addWidget(self.btnCancel)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3.addLayout(self.verticalLayout)

        self.retranslateUi(TypeNameDlg)
        self.btnOK.clicked.connect(TypeNameDlg.accept)
        self.btnCancel.clicked.connect(TypeNameDlg.reject)
        QtCore.QMetaObject.connectSlotsByName(TypeNameDlg)

    def retranslateUi(self, TypeNameDlg):
        _translate = QtCore.QCoreApplication.translate
        TypeNameDlg.setWindowTitle(_translate("TypeNameDlg", "类别名称维护"))
        self.label.setText(_translate("TypeNameDlg", "请输入类别名称："))
        self.btnOK.setText(_translate("TypeNameDlg", "确定"))
        self.btnCancel.setText(_translate("TypeNameDlg", "取消"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    TypeNameDlg = QtWidgets.QDialog()
    ui = Ui_TypeNameDlg()
    ui.setupUi(TypeNameDlg)
    TypeNameDlg.show()
    sys.exit(app.exec_())

