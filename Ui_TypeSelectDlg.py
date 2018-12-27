# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Works\Python\SimplePrint\TypeSelectDlg.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_TypeSelectDlg(object):
    def setupUi(self, TypeSelectDlg):
        TypeSelectDlg.setObjectName("TypeSelectDlg")
        TypeSelectDlg.resize(188, 313)
        TypeSelectDlg.setSizeGripEnabled(True)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(TypeSelectDlg)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.lstTypes = QtWidgets.QListWidget(TypeSelectDlg)
        self.lstTypes.setObjectName("lstTypes")
        self.verticalLayout.addWidget(self.lstTypes)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.btnOK = QtWidgets.QPushButton(TypeSelectDlg)
        self.btnOK.setObjectName("btnOK")
        self.horizontalLayout.addWidget(self.btnOK)
        self.btnCancel = QtWidgets.QPushButton(TypeSelectDlg)
        self.btnCancel.setObjectName("btnCancel")
        self.horizontalLayout.addWidget(self.btnCancel)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayout_2.addLayout(self.verticalLayout)

        self.retranslateUi(TypeSelectDlg)
        self.btnOK.clicked.connect(TypeSelectDlg.accept)
        self.btnCancel.clicked.connect(TypeSelectDlg.reject)
        QtCore.QMetaObject.connectSlotsByName(TypeSelectDlg)

    def retranslateUi(self, TypeSelectDlg):
        _translate = QtCore.QCoreApplication.translate
        TypeSelectDlg.setWindowTitle(_translate("TypeSelectDlg", "请选择类别"))
        self.btnOK.setText(_translate("TypeSelectDlg", "确定"))
        self.btnCancel.setText(_translate("TypeSelectDlg", "取消"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    TypeSelectDlg = QtWidgets.QDialog()
    ui = Ui_TypeSelectDlg()
    ui.setupUi(TypeSelectDlg)
    TypeSelectDlg.show()
    sys.exit(app.exec_())

