#!/usr/bin/env python3
# coding: utf-8
import time
import os
import shutil

from wxpy import *
from peewee import *
import pymysql

from md5 import get_md5
from user import User

waitTime = 10

bot = Bot(cache_path="cache/auth2.pkl")
namelist = []
wx_groups = bot.groups().search()


@bot.register(Group, TEXT)
def print_group_msg(msg):
    print(msg)

def spide():
    wx_groups = bot.groups().search()
    for group in wx_groups:
        if not group.name in namelist:
            group.update_group(members_details=True)
            users = group.search()
            for u in users:
                has_instance = True
                try:
                    result = User.select().where((User.display_name == (u.display_name or u.name)) & (User.from_group == group.name)).get()
                except Exception:
                    has_instance = False
                if not has_instance:
                    tmpFile = "./ava/ava2.jpg"
                    u.get_avatar(save_path=tmpFile)
                    md5 = get_md5(tmpFile)
                    from_id = bot.self.name
                    user = User(name=u.name, gender=u.sex, signature=u.signature,
                                avatar_file_name=md5+".jpg", from_id=from_id, from_group=(group.name or ''),
                                province=u.province, city=u.city, is_friend=u.is_friend, display_name=u.display_name)
                    user.save()
                    file_location = "./ava/%s.jpg" % md5
                    if os.path.isfile(file_location):
                        print("File already Exist!")
                    else:
                        shutil.copyfile(tmpFile, file_location)
                    print("写入成功【%s】{%s}[%d]%s" % (u.name, u.display_name, u.sex, md5))
                else:
                    print("skip: %s / %s" % (u.name, u.display_name))
                    continue

            namelist.append(group.name)


while True:
    spide()
    print("pause")
    time.sleep(waitTime)
    print("end pause")
