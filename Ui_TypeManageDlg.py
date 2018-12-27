# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'C:\Works\Python\SimplePrint\TypeManageDlg.ui'
#
# Created by: PyQt5 UI code generator 5.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_TypeManageDlg(object):
    def setupUi(self, TypeManageDlg):
        TypeManageDlg.setObjectName("TypeManageDlg")
        TypeManageDlg.resize(184, 337)
        TypeManageDlg.setSizeGripEnabled(True)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(TypeManageDlg)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.label_2 = QtWidgets.QLabel(TypeManageDlg)
        self.label_2.setObjectName("label_2")
        self.verticalLayout.addWidget(self.label_2)
        self.lstTypes = QtWidgets.QListWidget(TypeManageDlg)
        self.lstTypes.setObjectName("lstTypes")
        self.verticalLayout.addWidget(self.lstTypes)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.label = QtWidgets.QLabel(TypeManageDlg)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.edtTypeName = QtWidgets.QLineEdit(TypeManageDlg)
        self.edtTypeName.setObjectName("edtTypeName")
        self.verticalLayout_2.addWidget(self.edtTypeName)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.btnAdd = QtWidgets.QPushButton(TypeManageDlg)
        self.btnAdd.setObjectName("btnAdd")
        self.horizontalLayout.addWidget(self.btnAdd)
        self.btnSave = QtWidgets.QPushButton(TypeManageDlg)
        self.btnSave.setObjectName("btnSave")
        self.horizontalLayout.addWidget(self.btnSave)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.btnDelete = QtWidgets.QPushButton(TypeManageDlg)
        self.btnDelete.setObjectName("btnDelete")
        self.horizontalLayout_2.addWidget(self.btnDelete)
        self.btnQuit = QtWidgets.QPushButton(TypeManageDlg)
        self.btnQuit.setObjectName("btnQuit")
        self.horizontalLayout_2.addWidget(self.btnQuit)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_3.addLayout(self.verticalLayout_2)

        self.retranslateUi(TypeManageDlg)
        self.btnQuit.clicked.connect(TypeManageDlg.accept)
        QtCore.QMetaObject.connectSlotsByName(TypeManageDlg)

    def retranslateUi(self, TypeManageDlg):
        _translate = QtCore.QCoreApplication.translate
        TypeManageDlg.setWindowTitle(_translate("TypeManageDlg", "模板类别管理"))
        self.label_2.setText(_translate("TypeManageDlg", "类别："))
        self.label.setText(_translate("TypeManageDlg", "类别名称："))
        self.btnAdd.setText(_translate("TypeManageDlg", "新增"))
        self.btnSave.setText(_translate("TypeManageDlg", "保存"))
        self.btnDelete.setText(_translate("TypeManageDlg", "删除"))
        self.btnQuit.setText(_translate("TypeManageDlg", "退出"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    TypeManageDlg = QtWidgets.QDialog()
    ui = Ui_TypeManageDlg()
    ui.setupUi(TypeManageDlg)
    TypeManageDlg.show()
    sys.exit(app.exec_())

