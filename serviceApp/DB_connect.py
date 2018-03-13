#!/usr/bin/env python
# -*- coding: utf-8 -*-
import pymysql
from serviceApp.analysisDb import analysis


CONFIG_NAME = "db.conf"
CONFIG_PATH = "serviceApp/config/db"

class DBMethods:
    def __init__(self):
       pass


    def connectMysql(self):
        db = analysis(CONFIG_NAME, CONFIG_PATH)
        db_info = db.get_result()
        conn = None
        if db_info == False:
            return False
        try:
            conn=pymysql.connect(host=str(db_info["HOST"].decode("utf-8")), user=str(db_info["USER"].decode("utf-8")), passwd=str(db_info["PASSWORD"].decode("utf-8")), db=str(db_info["NAME"].decode("utf-8")), port=int(db_info["PORT"].decode("utf-8")), charset="utf8")
        except Exception as e:
            print(e)
        return conn

    def selectMethods(self, dbStr, num=-1):
        e = None
        retData = None
        try:
            conn = self.connectMysql()
            cur=conn.cursor()
            cur.execute(dbStr)
            if num == -1:
                retData = cur.fetchall()
            else:
                retData = cur.fetchmany(num)
            cur.close()
            conn.close()
        except pymysql.Error as e:
            raise e
        except Exception as e:
            print(e)
        return retData

    def updateMethods(self, dbStr):

        e = None
        try:
            conn = self.connectMysql()
            cur=conn.cursor()
            retData = cur.execute(dbStr)
            conn.commit()
            cur.close()
            conn.close()

        except(pymysql.Error,e):
            raise e
        return retData