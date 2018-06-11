# coding=utf-8
import os
import numpy as np
from PIL import Image
import tensorflow as tf
import matplotlib.pyplot as plt

from user import User

ava_dir = 'ava'


def gen_gender_train_data():
    male_files = []
    male_label = []
    female_files = []
    female_label = []

    users = User().select().where((User.avatar_file_name != "") & ((User.gender == 1) | (User.gender == 2))).get()
    for user in users:
        file_address = ava_dir + user.avatar_file_name
        if not os.path.isfile(file_address):
            continue
        if User.gender == 1:
            male_files.append(file_address)
            male_label.append(1)
        elif User.gender == 2:
            female_files.append(file_address)
            female_label.append(2)

    # 用来水平合并数组
    image_list = np.hstack((male_files, female_files))
    label_list = np.hstack((male_label, female_label))

    # 打乱数组
    temp = np.array([image_list, label_list])
    temp = temp.transpose()
    np.random.shuffle(temp)
    #
    image_list = list(temp[:, 0])
    label_list = list(temp[:, 1])
    label_list = [int(i) for i in label_list]

    return image_list, label_list


if __name__ == '__main__':
    gen_gender_train_data()
