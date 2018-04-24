#!/usr/bin/env python
# coding=utf-8

import pymysql
import sys, os
import uuid
import datetime
from openpyxl import Workbook
#from openpyxl import load_workbook

class GenLicense():

    def __init__(self):
        # 数据库配置
        self.dbName = 'android_uuid'
        self.dbTable = 'my_uuid'
        self.dbHost = 'vps.craftor.org'
        self.dbUser = 'test'
        self.dbPwd = 'test'
        self.dbOK = False

    def ConnectDB(self):
        #print('连接服务器...')
        # 打开数据库连接
        try:
            self.db = pymysql.connect(host=self.dbHost,
                                user=self.dbUser,
                                password=self.dbPwd,
                                db=self.dbName)
            #print('连接上了')
            self.dbOK = True
            return True
        except:
            #print(u"连接服务器失败!")
            return False

    def CreatTable(self):
        if (self.dbOK == False):
            print(u"服务器未连接")
            return 0
        # 使用cursor()方法获取操作游标
        cursor = self.db.cursor()

        # 如果存在表Sutdent先删除
        cursor.execute("DROP TABLE IF EXISTS " + self.dbTable)

        # 数据库操作指令
        sql = "CREATE TABLE " + self.dbTable + \
                "(GenTime CHAR(32) NOT NULL, \
                  License CHAR(128) NOT NULL, \
                  Expired INT NOT NULL , \
                  Phone CHAR(11) NOT NULL, \
                  Sales CHAR(32) )"

        # 创建my_uuid表
        cursor.execute(sql)

    # 批量生成License
    def GenUID_N(self, expired, phone, sales, n):
        # 检查数据库是否连接
        if (self.dbOK == False):
            print(u"服务器未连接")
            return 0

        # 打开Excel
        wb = Workbook()
        ws = wb.active
        ws.append([u"生成时间", u"序列号", u"有效期（天）", u"手机号", u"客户经理"])

        failed = False
        for i in range(n):
            tmpUID = uuid.uuid1()
            now = datetime.datetime.now()
            otherStyleTime = now.strftime("%Y-%m-%d-%H:%M:%S")
            date = now.strftime("%Y-%m-%d")
            if (self.Insert(otherStyleTime, tmpUID, expired, phone, sales)):
                print(u"序列号已生成：", tmpUID, u"| 有效期：", expired, u"天 | 第", i, u"个")
                ws.append([otherStyleTime, str(tmpUID), expired, phone, sales])
            else:
                print(u"序列号生成失败")
                failed = True
        # 提交数据库写入
        self.db.commit()
        # 保存excel文件
        now = datetime.datetime.now()
        t2 = now.strftime("%Y-%m-%d-%H-%M-%S")
        excelName = t2 + ".xlsx"
        wb.save(t2)

        if (failed):
            print("批量生成失败（部分）")
        else:
            print("批量生成成功（全部）")

    # 生成License
    def GenUID(self, expired, phone, sales):
        if (self.dbOK == False):
            print(u"服务器未连接")
            return 0
        tmpUID = uuid.uuid1()
        now = datetime.datetime.now()
        otherStyleTime = now.strftime("%Y-%m-%d %H:%M:%S")
        if (self.Insert(otherStyleTime, tmpUID, expired, phone, sales)):
            self.db.commit()
            print(u"序列号已生成：", tmpUID, u" 有效期：", expired, u"天")
            return tmpUID
        else:
            print(u"序列号生成失败")
            return None

    # 检查License是否有效
    def CheckUID(self, license):
        if (self.dbOK == False):
            print(u"服务器未连接")
            return 0
        data = self.Query(license)
        if (data != None):
            print (u"\r\n序列号:", str(license), "有效期剩余:", data[2], u"天")
        else:
            print (u"\r\n无效序列号")

    # 查询数据库
    def Query(self, license):
        if (self.dbOK == False):
            print(u"服务器未连接")
            return 0
        cursor = self.db.cursor()
        tmpUID = license
        sql = "SELECT * FROM `my_uuid` WHERE License=" + "'" + str(license) + "'"
        cursor.execute(sql)
        data = cursor.fetchone()
        #self.db.commit()
        return data

    # 写数据库
    def Insert(self, gentime, id, expired, phone, sales):
        if (self.dbOK == False):
            print(u"服务器未连接")
            return 0
        # 使用cursor()方法获取操作游标
        cursor = self.db.cursor()
        # SQL 插入语句
        sql = "INSERT INTO my_uuid(GenTime, License, Expired, Phone, Sales)" + \
                " VALUES('" + \
                str(gentime) + "' , '" + \
                str(id) + "' , '" + \
                str(expired) + "' , '" + \
                str(phone) + "' , '" + \
                str(sales) + \
                "' )"
        #print (sql)
        try:
            # 执行sql语句
            cursor.execute(sql)
            # 提交到数据库执行
            #self.db.commit()
            return True
        except:
            # Rollback in case there is any error
            print ('插入数据失败!')
            self.db.rollback()
            return False
