# -*- coding: utf-8 -*-
import sqlite3
import os
import time
import sys

#凭证元素类
class PrintLog:
    def __init__(self):
        #self.appPath, filename = os.path.split(os.path.abspath( __file__))
        if hasattr(sys, '_MEIPASS'):
            # PyInstaller会创建临时文件夹temp
            # 并把路径存储在_MEIPASS中
            self.appPath = os.path.dirname(os.path.realpath(sys.executable))
        else:
            self.appPath, filename = os.path.split(os.path.abspath(__file__))

        self.logdb = self.appPath + '/data/printlog.db'
        self.prlogs = [] #打印记录
        self.emdatas = [] #明细数据       
        self.initPrintLog()
        
    def initPrintLog(self):  #初始化数据库        
        if not os.path.exists(self.logdb):   #数据库不存在，则先建立
            conn = sqlite3.connect(self.logdb)
            c = conn.cursor()
            c.execute('''CREATE TABLE prlog
                (lid           INTEGER    PRIMARY KEY autoincrement NOT NULL, 
                prdate TEXT NOT NULL,
                vname TEXT NOT NULL,
                vtext TEXT,
                em1 TEXT,
                em2 TEXT,
                em3 TEXT,
                em4 TEXT,
                em5 TEXT,
                em6 TEXT,
                em7 TEXT,
                em8 TEXT,
                em9 TEXT,
                em10 TEXT);''')
            c.execute('''CREATE TABLE emdata
                (eid           INTEGER    PRIMARY KEY autoincrement NOT NULL,
                lid            INTEGER     NOT NULL,
                emval        TEXT,
                emtext     TEXT);''')
                         
            conn.commit()
            conn.close()

    #根据日期和模板显示名查询总记录数
    def getTotalRows(self, prdate, vtext):  #        
        conn = sqlite3.connect(self.logdb)
        c = conn.cursor()
        if prdate != '' and vtext == '':
            sql = "select count(*) from prlog where prdate='%s'" %(prdate)
        elif prdate == '' and vtext != '':
            sql = "select count(*) from prlog where vtext like '%s%%'" %(vtext)
        elif prdate != '' and vtext != '':
            sql = "select count(*) from prlog where prdate='%s' and vtext like '%s%%' " %(prdate, vtext)
        else:
            sql = "select count(*) from prlog" 
        alldata = c.execute(sql)
        self.totalrows = 0
        for data in alldata:
            self.totalrows = int(data[0])
            
        conn.commit()
        conn.close()
        return self.totalrows
        
    #根据日期和模板显示名查询
    def loadPrintLog(self, prdate, vtext, nbegin, nend):  #        
        conn = sqlite3.connect(self.logdb)
        c = conn.cursor()
        if prdate != '' and vtext == '':
            sql = "select * from prlog where prdate='%s' limit %d,%d" %(prdate, nbegin, nend)
        elif prdate == '' and vtext != '':
            sql = "select * from prlog where vtext like '%s%%' limit %d,%d" %(vtext, nbegin, nend)
        elif prdate != '' and vtext != '':
            sql = "select * from prlog where prdate='%s' and vtext like '%s%%' limit %d,%d" %(prdate, vtext, nbegin, nend)
        else:
            sql = "select * from prlog limit %d,%d" %(nbegin, nend)
        alldata = c.execute(sql)
        self.prlogs = []
        for data in alldata:
            self.prlogs.append(data)
            
        conn.commit()
        conn.close()

    #根据日期和模板显示名清理日志
    def DeletePrintLog(self, prdate, vtext):  #        
        conn = sqlite3.connect(self.logdb)
        c = conn.cursor()
        if prdate != '' and vtext == '':
            sql = "delete from prlog where prdate='%s'" %(prdate)
        elif prdate == '' and vtext != '':
            sql = "delete from prlog where vtext like '%s%%'" %(vtext)
        elif prdate != '' and vtext != '':
            sql = "delete from prlog where prdate='%s' and vtext like '%s%%'" %(prdate, vtext)
        else:
            sql = "delete from prlog " 
        c.execute(sql)            
        conn.commit()
        conn.close()
        
    #根据日志ID清理日志
    def DeletePrintLogByID(self,lid):  #        
        conn = sqlite3.connect(self.logdb)
        c = conn.cursor()
        sql = "delete from prlog where lid=%d" %(lid)
        c.execute(sql)            
        conn.commit()
        conn.close()

        

    def loadEmDataByLid(self, lid):  #        
        conn = sqlite3.connect(self.logdb)
        c = conn.cursor()
        sql = "select * from emdata where lid=%d" %(lid)
            
        alldata = c.execute(sql)
        self.emdatas = []
        for data in alldata:
            self.emdatas.append(data)
        conn.commit()
        conn.close()
        
    def savePrintLog(self, voucher):  #   
        conn = sqlite3.connect(self.logdb)
        c = conn.cursor()
        sql = "INSERT INTO prlog (prdate,vname,vtext,em1,em2,em3,em4,em5,em6,em7,em8,em9,em10) values ('%s','%s','%s'" %(time.strftime("%Y-%m-%d", time.localtime()), voucher.name, voucher.text)
        for i in range(len(voucher.elements)):
            if i < 10:
                #拼接最长10个字段到sql
                em = voucher.getElement(i)
                sql = sql + ",'" + em.getText() + "'"
        if len(voucher.elements) < 10:
            for i in range(len(voucher.elements), 10):
                sql = sql + ",''"
        sql = sql + ")"
        c.execute(sql)
        lid = c.lastrowid  #插入prlog后返回的lid值
        
        for i in range(len(voucher.elements)):
            #保存每个字段到emdata
            em = voucher.getElement(i)
            sql = "INSERT INTO emdata (lid,emval,emtext) \
                values (%d,'%s','%s')" %(lid, em.getVal(), em.getText())  
            c.execute(sql)

        conn.commit()
        conn.close()
  

