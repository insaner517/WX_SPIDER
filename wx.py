#!/usr/bin/env python3
# coding: utf-8
from wxpy import *
import pymysql  
import time

bot = Bot()
namelist = []
wx_groups = bot.groups().search()
db = pymysql.connect(host='127.0.0.1', port=3306, user='root', passwd='gzy517', db='mydb', charset='utf8')
cursor = db.cursor()  
@bot.register(Group, TEXT)
def print_group_msg(msg):
    print(msg)
def spide ():
	wx_groups = bot.groups().search()
	x = len(wx_groups)
	for i in range(0,x) :
		if not wx_groups[i].name in namelist :
			newuser = wx_groups[i]
			newuser.update_group(members_details=True)
			newgroup = newuser.search()
			for nx in newgroup :
				try:
					sql = "SELECT * FROM WXDATA WHERE NAME = '%s'" % (nx.name)
					# 执行SQL语句
					cursor.execute(sql)
					# 获取所有记录列表
					result = cursor.fetchall()
					if not len(result):
						sql = "INSERT INTO WXDATA (NAME, SEX, SIG ) VALUES ('%s','%d', '%s')" % (nx.name, nx.sex, nx.signature)
						cursor.execute(sql)
						db.commit()
						nx.get_avatar(save_path="./ava/%s" %(nx.name))
						print (nx.name)
						print (nx.sex)
					else :
						print("next")
						continue
				except:
						print ("new nx.name")
						sql = "INSERT INTO WXDATA (NAME, SEX, SIG ) VALUES ('%s','%d', '%s')" % (nx.name, nx.sex, nx.signature)
						print (nx.name)
						print (nx.sex)
						try:
							cursor.execute(sql)
							db.commit()
						except:
							db.rollback()
						
			namelist.append(newuser.name)			
while True :
	spide()
	print("pause")
	time.sleep(10)
	print("end pause")

db.close