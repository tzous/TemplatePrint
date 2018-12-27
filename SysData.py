# -*- coding: utf-8 -*-
from PyQt5 import QtGui

import sqlite3
import os


# 凭证元素类
class SysData:
    def __init__(self):
        self.sysparm = []  # 系统数据
        self.types = []  # 模板分组
        self.vouchers = []  # 模板列表
        self.appPath = ''  # 系统路径
        self.sysName = ''  # 本系统名称
        self.maxtypeid = 0
        self.maxvoucherid = 0
        # 凭证默认最大为A4大小210*297
        self.offsetx = 0  # 打印偏移量x轴（不用）
        self.offsety = 0  # 打印偏移量y轴（不用）
        self.leftmargin = 11  # 打印机默认左边距
        self.topmargin = 11  # 打印机默认上边距
        self.batchprint = True  # 批量数据第一行为字段标题
        self.font = QtGui.QFont('宋体', 10, QtGui.QFont.Normal)  # 默认字体
        self.printer = None  # 默认打印机
        self.autosave = False  # 打印记录是否自动保存
        self.appPath, filename = os.path.split(os.path.abspath(__file__))
        self.parmdb = self.appPath + '/data/sysdata.db'
        self.dataPath = self.appPath + '/data/'  # 系统数据路径
        self.templatePath = self.appPath + '/template/'  # 系统模板路径

        self.loadSysData()

    def loadSysData(self):  # 初始化系统数据等
        if not os.path.exists(self.parmdb):  # 系统数据库不存在，则先建立
            conn = sqlite3.connect(self.parmdb)
            c = conn.cursor()
            c.execute('''CREATE TABLE sysparm
                (sysname           TEXT    PRIMARY KEY NOT NULL, 
                maxtypeid INT NOT NULL,
                maxvoucherid INT NOT NULL,
                leftmargin INT NOT NULL,
                topmargin INT NOT NULL,
                printer TEXT,
                defaultfont TEXT,
                autosave TEXT,
                batchprint TEXT);''')
            c.execute('''CREATE TABLE types
                (typeid           int    PRIMARY KEY NOT NULL,
                typename            TEXT     NOT NULL,
                parentid        INT NOT NULL);''')
            c.execute('''CREATE TABLE vouchers
                (vid           int    PRIMARY KEY NOT NULL,
                vname            TEXT     NOT NULL,
                vtext            TEXT     NOT NULL,
                typeid        INT NOT NULL,
                offsetx   INT,
                offsety   INT);''')

            # 本系统名称,当前最大类别编号,当前最大凭证编号,x偏移,y偏移,默认打印机,默认字体,打印记录是否自动保存
            sql = "INSERT INTO sysparm (sysname,maxtypeid,maxvoucherid,leftmargin,topmargin,printer,defaultfont,autosave,batchprint) \
                values ('%s',%d,%d,%d,%d,'%s','%s','%s','%s')" % (
            '简单凭证打印', 3, 5, 11, 11, '', QtGui.QFont('宋体', 10, QtGui.QFont.Normal).toString(), 'False', 'True')
            c.execute(sql)
            # 类别编号，类别名称，父类别编号
            sql = "INSERT INTO types (typeid,typename,parentid) \
                values (%d,'%s',%d)" % (1, '常用', 0)
            c.execute(sql)
            sql = "INSERT INTO types (typeid,typename,parentid) \
                values (%d,'%s',%d)" % (2, '农行', 0)
            c.execute(sql)
            sql = "INSERT INTO types (typeid,typename,parentid) \
                values (%d,'%s',%d)" % (3, '其他', 0)
            c.execute(sql)
            # 凭证编号，凭证名称，凭证显示名称，类别编号
            #            sql = "INSERT INTO vouchers (vid,vname,vtext,typeid,offsetx,offsety) \
            #                values (%d,'%s','%s',%d,%d,%d)" %(1,'支票','支票', 1, 0, 0)
            #            c.execute(sql)
            #            sql = "INSERT INTO vouchers (vid,vname,vtext,typeid,offsetx,offsety) \
            #                values (%d,'%s','%s',%d,%d,%d)" %(2,'手工发票','手工发票', 3, 0, 0)
            #            c.execute(sql)
            #            sql = "INSERT INTO vouchers (vid,vname,vtext,typeid,offsetx,offsety) \
            #                values (%d,'%s','%s',%d,%d,%d)" %(3,'快递单','快递单',  3, 0, 0)
            #            c.execute(sql)
            #            sql = "INSERT INTO vouchers (vid,vname,vtext,typeid,offsetx,offsety) \
            #                values (%d,'%s','%s',%d,%d,%d)" %(4,'收款收据','收款收据', 2, 0, 0)
            #            c.execute(sql)
            #            sql = "INSERT INTO vouchers (vid,vname,vtext,typeid,offsetx,offsety) \
            #                values (%d,'%s','%s',%d,%d,%d)" %(5,'汇票','汇票', 2, 0, 0)
            #            c.execute(sql)

            conn.commit()
            conn.close()

        conn = sqlite3.connect(self.parmdb)
        c = conn.cursor()
        sql = "select * from sysparm"
        alldata = c.execute(sql)
        self.sysparm = []
        for data in alldata:
            self.sysparm.append(data)
            self.sysName = data[0]
            self.maxtypeid = int(data[1])
            self.maxvoucherid = int(data[2])
            self.leftmargin = data[3]  # 打印机默认左边距
            self.topmargin = data[4]  # 打印机默认上边距
            self.printer = data[5]  # 默认打印机
            self.font.fromString(data[6])  # 默认字体
            if data[7] == 'True':
                self.autosave = True  # 打印记录是否自动保存
            else:
                self.autosave = False
            if data[8] == 'True':
                self.batchprint = True  # 批量打印数据第一行为字段标题
            else:
                self.batchprint = False

        sql = "select * from types"
        alldata = c.execute(sql)
        self.types = []
        for data in alldata:
            self.types.append(data)
        sql = "select * from vouchers"
        alldata = c.execute(sql)
        self.vouchers = []
        for data in alldata:
            self.vouchers.append(data)
        conn.commit()
        conn.close()

    def saveSysData(self):  # 保存系统参数
        conn = sqlite3.connect(self.parmdb)
        c = conn.cursor()
        # 本系统名称,当前最大类别编号,当前最大凭证编号,x偏移,y偏移,默认打印机,默认字体,打印记录是否自动保存
        sql = "update sysparm set leftmargin=%d,topmargin=%d,batchprint='%s' " % (
        self.leftmargin, self.topmargin, str(self.batchprint))
        c.execute(sql)

        conn.commit()
        conn.close()

    # 保存新凭证信息至系统数据库,v-凭证类 tid-分类
    def SaveNewVoucher(self, v, tid):
        conn = sqlite3.connect(self.parmdb)
        c = conn.cursor()
        # 删除库中其他相同名称和类别的凭证
        sql = "DELETE FROM vouchers where vname='%s' and  typeid=%d" % (v.getName(), int(tid))
        c.execute(sql)
        # 更新maxvoucherid
        self.maxvoucherid = self.maxvoucherid + 1
        sql = "UPDATE sysparm set maxvoucherid=%d " % (self.maxvoucherid)
        c.execute(sql)

        # 凭证编号，凭证名称，凭证显示名称，类别编号
        sql = "INSERT INTO vouchers (vid,vname,vtext,typeid,offsetx,offsety) \
                values (%d,'%s','%s',%d,%d,%d)" % (
        self.maxvoucherid, v.getName(), v.getText(), int(tid), int(v.offsetx), int(v.offsety))
        c.execute(sql)
        conn.commit()
        conn.close()
        self.loadSysData()
        return 0

    # 保存新类别至系统库
    def existVoucher(self, vname):
        conn = sqlite3.connect(self.parmdb)
        c = conn.cursor()
        sql = "select count(*) from vouchers where vname='%s'" % (vname)
        ts = c.execute(sql)
        icount = 0
        for t in ts:
            icount = int(t[0])
        conn.commit()
        conn.close()
        return True if icount > 0 else False

    # 根据凭证id将凭证信息从系统库中删除
    def DeleteVoucherByID(self, vid):
        conn = sqlite3.connect(self.parmdb)
        c = conn.cursor()
        # 凭证编号，凭证名称，凭证显示名称，类别编号
        sql = "DELETE FROM vouchers WHERE vid=%d " % (int(vid))
        c.execute(sql)
        conn.commit()
        conn.close()
        self.loadSysData()
        return 0

    # 根据类别id和凭证名称将凭证信息从系统库中删除???
    def DeleteVoucherByTypeIDName(self, tid, vname):
        conn = sqlite3.connect(self.parmdb)
        c = conn.cursor()
        # 凭证编号，凭证名称，凭证显示名称，类别编号
        sql = "DELETE FROM vouchers WHERE typeid=%d and vname='%s'" % (int(tid), vname)
        c.execute(sql)
        conn.commit()
        conn.close()
        self.loadSysData()
        return 0

    # 将模板移动到新类别中
    def UpdateVoucherType(self, vid, typeid):
        conn = sqlite3.connect(self.parmdb)
        c = conn.cursor()
        # 凭证编号，凭证名称，凭证显示名称，类别编号
        sql = "update vouchers set typeid=%d WHERE vid=%d " % (int(typeid), int(vid))
        c.execute(sql)
        conn.commit()
        conn.close()
        self.loadSysData()
        return 0

    # 保存新类别至系统库
    def SaveNewType(self, tname):
        conn = sqlite3.connect(self.parmdb)
        c = conn.cursor()
        sql = "select count(*) from types where typename='%s'" % (tname)
        ts = c.execute(sql)
        for t in ts:
            if int(t[0]) > 0:
                return -1
        self.maxtypeid = self.maxtypeid + 1
        sql = "UPDATE sysparm set maxtypeid=%d " % (self.maxtypeid)
        c.execute(sql)
        # 类别编号，类别名称，父类别编号
        sql = "INSERT INTO types (typeid,typename,parentid) \
                values (%d,'%s',%d)" % (self.maxtypeid, tname, 0)
        c.execute(sql)
        conn.commit()
        conn.close()
        self.loadSysData()
        return 0

    # 更新类别至系统库
    def UpdateTypeByID(self, tid, tname):
        conn = sqlite3.connect(self.parmdb)
        c = conn.cursor()
        # 类别编号，类别名称，父类别编号
        sql = "update types set typename='%s' where typeid=%d " % (tname, tid)
        c.execute(sql)
        conn.commit()
        conn.close()
        self.loadSysData()
        return 0

    # 从系统库中删除类别信息
    def DeleteTypeByID(self, tid):
        conn = sqlite3.connect(self.parmdb)
        c = conn.cursor()
        sql = "select count(*) from vouchers WHERE typeid=%d" % (tid)
        ts = c.execute(sql)
        for t in ts:
            if int(t[0]) > 0:
                return -1

        # 类别编号，类别名称，父类别编号
        sql = "DELETE FROM types WHERE typeid=%d " % (int(tid))
        c.execute(sql)
        conn.commit()
        conn.close()
        self.loadSysData()
        return 0
