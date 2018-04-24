#!/usr/bin/env python
# coding=utf-8

import pymysql
import sys, os
import uuid
import datetime

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
        # 使用cursor()方法获取操作游标
        cursor = self.db.cursor()

        # 如果存在表Sutdent先删除
        #cursor.execute("DROP TABLE IF EXISTS " + self.dbTable)

        # 数据库操作指令
        sql = "CREATE TABLE " + self.dbTable + \
                "(GenTime CHAR(32) NOT NULL, \
                  License CHAR(128) NOT NULL, \
                  Expired INT NOT NULL , \
                  Phone CHAR(11) NOT NULL, \
                  Sales CHAR(32) )"

        # 创建my_uuid表
        cursor.execute(sql)

    # 生成License
    def GenUID(self, expired, phone, sales):
        tmpUID = uuid.uuid1()
        now = datetime.datetime.now()
        otherStyleTime = now.strftime("%Y-%m-%d %H:%M:%S")
        if (self.Insert(otherStyleTime, tmpUID, expired, phone, sales)):
            print(u"序列号已生成：", tmpUID, u" 有效期：", expired, u"天")
            return tmpUID
        else:
            print(u"序列号生成失败")
            return "000000"

    # 检查License是否有效
    def CheckUID(self, license):
        data = self.Query(license)
        if (data != None):
            print (u"\r\n序列号:", str(license), "有效期剩余:", data[2], u"天")
        else:
            print (u"\r\n无效序列号")

    # 查询数据库
    def Query(self, license):
        cursor = self.db.cursor()
        tmpUID = license
        sql = "SELECT * FROM `my_uuid` WHERE License=" + "'" + str(license) + "'"
        cursor.execute(sql)
        data = cursor.fetchone()
        #self.db.commit()
        return data

    # 写数据库
    def Insert(self, gentime, id, expired, phone, sales):
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
            self.db.commit()
            return True
        except:
            # Rollback in case there is any error
            print ('插入数据失败!')
            self.db.rollback()
            return False
