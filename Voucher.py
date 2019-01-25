# -*- coding: utf-8 -*-
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from MyTools import MyTools
import sqlite3
import os


# 凭证元素类
# noinspection SpellCheckingInspection
class Element:
    def __init__(self):
        self.startPoint = QPoint(0, 0)  # 左上角点
        self.width = 120  # 宽
        self.height = 26  # 高

        self.name = 'name'  # 元素名称
        self.val = '文本'  # 元素值
        self.text = '文本'  # 显示文本，与self.val关联
        self.type = 'text'  # 当前元素类别,默认文本text
        self.allTypes = ['text', 'num', 'numcap', 'money', 'moneycap', 'check']  # 所有元素类别
        self.allChineseTypes = ['文本', '数字', '数字大写', '金额', '金额大写', '打勾项']  # 所有元素类别中文名称
        self.numTypes = ['num', 'numcap', 'money', 'moneycap']  # 元素数值类别
        self.len = 10  # 元素长度，半角字符数，一个全角字符按2个字符长度计算
        self.font = QFont('宋体', 10, QFont.Normal)  # 默认字体
        # {"name":"宋体","height":180,"width":90, }        #默认字体
        # 以下为元素附加属性
        self.trim = True  # 输入值是否要删除首尾空格
        self.prefix = False  # 是否有前缀
        self.prefixText = '¥'  # 前缀文本，如人民币符号¥等
        self.postfix = False  # 是否有后缀，如大写金额整
        self.postfixText = ''  # 后缀文本
        self.meanCol = False  # 是否均列打印
        self.meanColVal = 0  # 均列打印间隔
        self.checkVal = '√'  # check类型，取值预置为√×*等
        self.hAlign = Qt.AlignLeft  # 水平对齐left、center、right
        self.vAlign = Qt.AlignVCenter  # 垂直对齐 top、center、bottom
        self.lineWrap = False  # 是否折行
        self.printBorder = False  # 是否打印边框

    # 矩形左上角点
    def setStartPoint(self, s):
        self.startPoint = s
        self.adjustPoint()

    # 矩形左上角点
    def getStartPoint(self):
        return self.startPoint

    # 宽
    def setWidth(self, w):
        self.width = int(w)

    # 宽
    def getWidth(self):
        return self.width

    # 高
    def setHeight(self, h):
        self.height = int(h)

    # 高
    def getHeight(self):
        return self.height

    # 元素名称
    def setName(self, e):
        self.name = e

    # 元素名称
    def getName(self):
        return self.name

    # 元素值
    def setVal(self, s):
        mytools = MyTools()
        # 保存同时处理显示文本
        if self.type in self.numTypes:  # 数值类型
            ss = mytools.trim(s)  # 需先删除所有空格，然后判断
            if mytools.legal_numbers(ss):  # 合法数值
                v = float(ss)
                if self.type == 'num':
                    self.val = int(v)
                    self.text = str(int(v))
                elif self.type == 'money':
                    self.val = float('%.2f' % v)
                    self.text = '%.2f' % v
                elif self.type == 'numcap':
                    self.val = int(v)
                    self.text = mytools.convertNumToCap(self.val)
                elif self.type == 'moneyCap':
                    self.val = float('%.2f' % v)
                    self.text = mytools.convertNumToChinese(self.val)
            else:  # 非法数值，置空值
                self.val = ''
                self.text = ''
        elif self.type == 'check':  # check类型，只有两个值，空与非空
            v = mytools.trim(s)  # 需先删除所有空格，然后判断
            if v:  # 非空值
                self.val = self.checkVal
                self.text = self.checkVal
            else:
                self.text = ''
                self.val = ''
        else:  # 其他类型，默认处理同text
            if self.trim:  # 是否删除首尾空格
                v = s.strip()
            else:
                v = s
            self.val = v
            self.text = v

        if self.prefix:  # 前缀
            self.text = self.prefixText + self.text
        if self.postfix:  # 后缀
            self.text = self.text + self.postfixText

    # 元素值
    def getVal(self):
        return self.val

    # 显示文本
    def getText(self):
        return self.text

    # 当前元素类别
    def setType(self, t):
        if t in self.allTypes:
            self.type = t
        else:
            self.type = 'text'

    def getType(self):
        return self.type

    def getTypeChinese(self):
        i = self.allTypes.index(self.type)
        return self.allChineseTypes[i]

    def getAllTypes(self):
        return self.allTypes

    def getAllChineseTypes(self):
        return self.allChineseTypes

    # 元素长度
    def setLen(self, l):
        if int(l) > 0:
            self.len = int(l)
        else:
            self.len = 0

    def getLen(self):
        return self.len

    # 字体
    def setFont(self, f):
        self.font = f

    def getFont(self):
        return self.font

    # 各个附加选项
    # 输入值是否要删除首尾空格
    def setTrim(self, t):
        if t:
            self.trim = True
        else:
            self.trim = False

    def getTrim(self):
        return self.trim

    # 是否有前缀
    def setPrefix(self, t):
        if t:
            self.prefix = True
        else:
            self.prefix = False

    def getPrefix(self):
        return self.prefix

    # 前缀文本
    def setPrefixText(self, t):
        self.prefixText = t

    def getPrefixText(self):
        return self.prefixText

    # 是否有后缀
    def setPostfix(self, t):
        if t:
            self.postfix = True
        else:
            self.postfix = False

    def getPostfix(self):
        return self.postfix

    # 后缀文本
    def setPostfixText(self, t):
        self.postfixText = t

    def getPostfixText(self):
        return self.postfixText

    # 是否均列打印
    def setMeanCol(self, t):
        if t:
            self.meanCol = True
        else:
            self.meanCol = False

    def getMeanCol(self):
        return self.meanCol

    # 均列打印值
    def setMeanColVal(self, v):
        self.meanColVal = v

    def getMeanColVal(self):
        return self.meanColVal

    # check类型，取值
    def setCheckVal(self, v):
        self.checkVal = v

    def getCheckVal(self):
        return self.checkVal

    # 水平对齐left、center、right
    def setHAlign(self, v):
        self.hAlign = v

    def getHAlign(self):
        return self.hAlign

    # 垂直对齐 top、center、bottom
    def setVAlign(self, v):
        self.vAlign = v

    def getVAlign(self):
        return self.vAlign

    # 是否折行
    def setLineWrap(self, t):
        if t:
            self.lineWrap = True
        else:
            self.vAlign = False

    def getLineWrap(self):
        return self.lineWrap

    # 是否打印边框
    def setPrintBorder(self, t):
        if t:
            self.printBorder = True
        else:
            self.printBorder = False

    def getPrintBorder(self):
        return self.printBorder

    # 点在矩形中
    def contains(self, e):
        x = e.x() - self.startPoint.x()
        y = e.y() - self.startPoint.y()
        if x < 0 or x > self.width or y < 0 or y > self.height:
            return False
        else:
            return True

    # 点在右边上
    def xcontains(self, e):
        x = e.x() - self.startPoint.x()
        y = e.y() - self.startPoint.y()
        if (self.width - 2 <= x <= self.width + 2) and (0 <= y <= self.height):
            return True
        else:
            return False

    # 点在下边上
    def ycontains(self, e):
        x = e.x() - self.startPoint.x()
        y = e.y() - self.startPoint.y()
        if (0 <= x <= self.width) and (self.height - 2 <= y <= self.height + 2):
            return True
        else:
            return False

    # 移动,x和y分别为X和Y方向的偏移量
    def movedist(self, x, y):
        startPos = QPoint(self.startPoint.x() + x, self.startPoint.y() + y)
        self.startPoint = startPos


# 凭证模板类
# noinspection SpellCheckingInspection
class Voucher:
    def __init__(self):
        self.name = ''  # 凭证名称
        self.text = ''  # 显示的凭证中文名称
        self.width = 180  # 凭证宽度，毫米
        self.height = 100  # 凭证高度，毫米
        self.dpi = 96  # 屏幕dpi
        self.pixelWidth = 850  # 凭证宽度，像素
        self.pixelHeight = 377  # 凭证高度，像素
        self.voucherType = 0  # 凭证分类
        self.elements = {}  # 凭证元素，使用字典保存，元素在表中的序号作为key
        self.background = None  # 凭证背景,base64编码
        self.offsetx = 0  # 横向打印偏移量（不用）
        self.offsety = 0  # 纵向打印偏移量（不用）
        self.leftmargin = 11  # 打印左边距
        self.topmargin = 11  # 打印上边距

    def setName(self, s):
        self.name = s

    def getName(self):
        return self.name

    def setText(self, s):
        self.text = s

    def getText(self):
        return self.text

    # w为宽，h为高，单位为mm
    def setSize(self, w, h):
        self.width = int(w)
        self.height = int(h)

        self.pixelWidth = int(w * self.dpi / 25.4)
        self.pixelHeight = int(h * self.dpi / 25.4)

    def getWidth(self):
        return self.width

    def getHeight(self):
        return self.height

    def getPixelWidth(self):
        return self.pixelWidth

    def getPixelHeight(self):
        return self.pixelHeight

    def setVoucherType(self, vt):
        self.voucherType = vt

    def getVoucherType(self):
        return self.adjustPoint

    # 清空凭证元素列表
    def emptyElements(self):
        self.elements.clear()

    # 追加凭证元素
    def appendElement(self, e):
        n = len(self.elements)  # 将当前凭证数作为key
        ename = "e%04d" % n  # 元素命名：'e'+序号
        e.setName(ename)
        self.elements[n] = e

    # 更新凭证元素
    def updateElement(self, i, e):
        n = len(self.elements)
        if i < 0 or i > n:  # 将非法key，不更新
            return
        self.elements[i] = e

    # 删除制定凭证元素
    def delElement(self, i):
        n = len(self.elements)
        if i < n - 1:  # 非最后一个
            for k in range(i, n - 1):  # 所有元素往前移
                self.elements[k] = self.elements[k + 1]
        # 删除最后一个元素
        self.elements.pop(n - 1)

    # 取指定凭证元素
    def getElement(self, i):
        if len(self.elements) == 0:  # 元素表为空
            return None
        if i >= len(self.elements):
            i = len(self.elements) - 1
        if i < 0:
            i = 0
        return self.elements[i]

    # 元素个数
    def getElementNumbers(self):
        return len(self.elements)

    # 将指定元素位置从i移到k位
    def moveElement(self, i, k):
        if i == k:  # 两个位置相同，无需移动
            return False
        if i >= len(self.elements) or i < 0 or k >= len(self.elements) or k < 0:  # 位置非法，无需移动
            return False
        ei = self.elements[i]  # 保存第i个位置
        if k > i:  # 往后移
            step = 1
        else:  # 往前移
            step = -1
        # 元素移位
        for j in range(i, k, step):
            self.elements[j] = self.elements[j + step]
        self.elements[k] = ei

        return True

    # 凭证背景
    def setBackground(self, p):
        self.background = p

    def getBackground(self):
        return self.background

    # 点在凭证矩形中
    def contains(self, e):
        if (0 <= e.x() <= self.pixelWidth) and (0 <= e.y() <= self.pixelHeight):
            return True
        else:
            return False

    # 保存模板到本地库
    def save(self, dbpath):
        db = dbpath + self.name + ".tdb"
        if not os.path.exists(db):  # 模板库不存在，则先建立
            conn = sqlite3.connect(db)
            c = conn.cursor()
            c.execute('''CREATE TABLE voucher
                (vname           TEXT    PRIMARY KEY NOT NULL,
                vtext            TEXT     NOT NULL,
                vwidth        INT NOT NULL,
                vheight    INT NOT NULL,
                vpixelwidth INT NOT NULL,
                vpixelheight INT NOT NULL);''')
            c.execute('''CREATE TABLE elements
                (ename           Text    PRIMARY KEY NOT NULL,
                epx            int     NOT NULL,
                epy        INT NOT NULL,
                ewidth    INT NOT NULL,
                eheight INT NOT NULL,
                eval TEXT NOT NULL,
                etext TEXT NOT NULL,
                etype TEXT NOT NULL,
                elen int not NULL,
                efont TEXT NOT NULL,
                etrim TEXT NOT NULL,
                eprefix TEXT NOT NULL,
                eprefixText TEXT ,
                epostfix TEXT NOT NULL,
                epostfixText TEXT,
                emeancol TEXT,
                emeancolval int,
                echeckval TEXT,
                ehaligh TEXT,
                evalign TEXT,
                elinewrap TEXT,
                eprintborder TEXT);''')
            c.execute('''CREATE TABLE background
                (jpg TEXT NOT NULL);''')

            conn.commit()
            conn.close()

        conn = sqlite3.connect(db)
        c = conn.cursor()

        # 凭证信息
        c.execute('DELETE FROM voucher')
        sql = "INSERT INTO voucher (vname,vtext,vwidth,vheight,vpixelwidth,vpixelheight) \
            values ('%s','%s',%d,%d,%d,%d)" % (
        self.name, self.text, int(self.width), int(self.height), int(self.pixelWidth), int(self.pixelHeight))
        c.execute(sql)
        # 字段信息
        c.execute('DELETE FROM elements')
        for i in range(len(self.elements)):
            # 保存每个字段
            em = self.getElement(i)
            sql = "INSERT INTO elements (ename,epx,epy,ewidth,eheight,eval,etext,etype,elen,efont,etrim,eprefix,eprefixText,epostfix,epostfixText,emeancol,emeancolval,echeckval,ehaligh,evalign,elinewrap,eprintborder) \
                values ('%s',%d,%d,%d,%d,'%s','%s','%s',%d,'%s','%s','%s','%s','%s','%s','%s',%d,'%s','%s','%s','%s','%s')" % (
            em.name, int(em.getStartPoint().x()), int(em.getStartPoint().y()), int(em.width), int(em.height), em.val,
            em.text, em.type, int(em.len), em.font.toString(), \
            em.trim, em.prefix, em.prefixText, em.postfix, em.postfixText, em.meanCol, int(em.meanColVal), em.checkVal,
            em.hAlign, em.vAlign, em.lineWrap, em.printBorder)
            c.execute(sql)

        # 背景图
        c.execute('DELETE FROM background')
        if self.background is not None:
            # self.background为bytes类型，转换为str后需要删除开头的"b'"及最后的"'"
            sql = "INSERT INTO background (jpg) values ('%s')" % (str(self.background)[2:-1])
            c.execute(sql)
        conn.commit()
        conn.close()

    # 根据凭证名称从本地库中读入
    def load(self, dbpath, name):
        db = dbpath + name + ".tdb"
        return self.loadfromdb(db)

    # 根据凭证名称从本地库中读入
    def loadfromdb(self, db):
        if not os.path.exists(db):  # 模板库不存在
            return None
        conn = sqlite3.connect(db)
        c = conn.cursor()
        sql = "select * from voucher"
        alldata = c.execute(sql)
        for data in alldata:
            self.name = data[0]
            self.text = data[1]  # 显示的凭证中文名称
            self.width = data[2]  # 凭证宽度，毫米
            self.height = data[3]  # 凭证高度，毫米
            self.pixelWidth = data[4]  # 凭证宽度，像素
            self.pixelHeight = data[5]  # 凭证高度，像素
            self.offsetx = 0  # 模板打印偏移量保存在系统库中
            self.offsety = 0

        self.emptyElements()
        sql = "select * from elements order by ename"
        alldata = c.execute(sql)
        for data in alldata:
            em = Element()
            em.name = data[0]  # 元素名称
            em.startPoint = QPoint(int(data[1]), int(data[2]))  # 左上角点
            em.width = int(data[3])  # 宽
            em.height = int(data[4])  # 高
            em.val = data[5]  # 元素值
            em.text = data[6]  # 显示文本，与em.val关联
            em.type = data[7]  # 当前元素类别,默认文本text
            em.len = int(data[8])  # 元素长度，半角字符数，一个全角字符按2个字符长度计算
            em.font.fromString(data[9])  # 字体，转换为QFont
            em.trim = MyTools.str_to_bool(data[10])  # 输入值是否要删除首尾空格
            em.prefix = MyTools.str_to_bool(data[11])  # 是否有前缀
            em.prefixText = data[12]  # 前缀文本，如人民币符号¥等
            em.postfix = MyTools.str_to_bool(data[13])  # 是否有后缀，如大写金额整
            em.postfixText = data[14]  # 后缀文本
            em.meanCol = MyTools.str_to_bool(data[15])  # 是否均列打印
            em.meanColVal = int(data[16])  # 均列打印间隔
            em.checkVal = data[17]  # check类型，取值预置为√×*等
            em.hAlign = int(data[18])  # 水平对齐left、center、right
            em.vAlign = int(data[19])  # 垂直对齐 top、center、bottom
            em.lineWrap = MyTools.str_to_bool(data[20])  # 是否折行
            em.printBorder = MyTools.str_to_bool(data[21])  # 是否打印边框
            self.appendElement(em)

        # 背景
        self.background = None
        sql = "select * from background"
        alldata = c.execute(sql)
        for data in alldata:
            self.background = bytes(data[0], encoding='utf-8')
        conn.close()
        return True

    # 凭证打印
    def paintElements(self, painter):
        for i in range(0, self.getElementNumbers()):
            em = self.getElement(i)

            x0 = em.getStartPoint().x() + self.offsetx - self.leftmargin
            y0 = em.getStartPoint().y() + self.offsety - self.topmargin
            x = em.getWidth()
            y = em.getHeight()
            rect = QRect(x0, y0, x, y)

            txt = em.getText()
            if em.meanCol and em.getType() in ['num', 'money']:  # 均列打印
                txt = txt.replace('.', '')  # 删除其中的小数点
                ft = em.font
                ft.setLetterSpacing(QFont.AbsoluteSpacing, em.meanColVal)  # 设置间隔
                painter.setFont(ft)  # 设置字体
            else:  # 普通文本
                painter.setFont(em.font)  # 设置字体

            painter.drawText(rect, em.getHAlign() | em.getVAlign(), txt)
