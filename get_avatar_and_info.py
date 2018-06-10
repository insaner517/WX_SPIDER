#!/usr/bin/env python3
# coding: utf-8
import time

from wxpy import *
from peewee import *
import pymysql

from md5 import get_md5

bot = Bot()
namelist = []
wx_groups = bot.groups().search()
db = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='gzy517', db='mydb', charset='utf8')
cursor = db.cursor()


@bot.register(Group, TEXT)
def print_group_msg(msg):
    print(msg)


def spide():
    wx_groups = bot.groups().search()
    x = len(wx_groups)
    for i in range(0, x):
        if not wx_groups[i].name in namelist:
            newuser = wx_groups[i]
            newuser.update_group(members_details=True)
            newgroup = newuser.search()
            for nx in newgroup:
                sql = "SELECT * FROM WXDATA WHERE NAME = %s"
                # 执行SQL语句
                params = (nx.name)
                cursor.execute(sql, params)
                # 获取所有记录列表
                result = cursor.fetchall()
                try:
                    if not len(result):
                        nx.get_avatar(save_path="./ava/ava.jpg")
                        md5 = get_md5("./ava/ava.jpg")
                        sql = "INSERT INTO WXDATA (NAME, SEX, SIG, TAG, AVA ) VALUES (%s,%d, %s,%s,%s)"
                        params = (nx.name, nx.sex, nx.signature, "", md5)
                        nx.get_avatar(save_path="./ava/%s.jpg" % (md5))
                        cursor.execute(sql, params)
                        db.commit()
                        print(nx.name)
                        print(nx.sex)
                    else:
                        print("next")
                        continue
                except:
                    print ("name error")
                # sql = "INSERT INTO WXDATA (NAME, SEX, SIG ) VALUES ('%s','%d', '%s')" % (nx.name, nx.sex, nx.signature)
                # print (nx.name)
                # print (nx.sex)
                # try:
                # 	cursor.execute(sql)
                # 	db.commit()
                # except:
                # 	db.rollback()

            namelist.append(newuser.name)


while True:
    spide()
    print("pause")
    time.sleep(10)
    print("end pause")

db.close