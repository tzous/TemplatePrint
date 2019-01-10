# -*- coding: utf-8 -*-
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5 import QtWidgets

from Ui_TypeNameDlg import Ui_TypeNameDlg


class TypeNameDlg(QtWidgets.QDialog, Ui_TypeNameDlg):
    def __init__(self):
        super(TypeNameDlg, self).__init__()
        self.setupUi(self)
