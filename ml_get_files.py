# coding=utf-8
import os
import numpy as np
# from PIL import Image
import tensorflow as tf
import matplotlib.pyplot as plt

from user import User

ava_dir = 'ava/'


def gen_gender_train_data():
    male_files = []
    male_label = []
    female_files = []
    female_label = []

    users = (User.select().where((User.avatar_file_name != "") & ((User.gender == 1) | (User.gender == 2))))
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

    label_list = [round(float(i)) for i in label_list]

    return image_list, label_list


def get_batch(image, label, image_w, image_h, batch_size, capacity):
    image = tf.cast(image, tf.string)
    label = tf.cast(label, tf.int32)
    # tf.cast()用来做类型转换

    input_queue = tf.train.slice_input_producer([image, label])
    # 加入队列

    label = input_queue[1]
    image_contents = tf.read_file(input_queue[0])
    image = tf.image.decode_jpeg(image_contents, channels=3)
    # jpeg或者jpg格式都用decode_jpeg函数，其他格式可以去查看官方文档

    image = tf.image.resize_image_with_crop_or_pad(image, image_w, image_h)
    # resize

    image = tf.image.per_image_standardization(image)
    # 对resize后的图片进行标准化处理

    image_batch, label_batch = tf.train.batch([image, label], batch_size=batch_size, num_threads=16, capacity=capacity)

    label_batch = tf.reshape(label_batch, [batch_size])
    return image_batch, label_batch
    # 获取两个batch，两个batch即为传入神经网络的数据


if __name__ == '__main__':
    BATCH_SIZE = 2
    CAPACITY = 64
    IMG_W = 208
    IMG_H = 208

    image_list, label_list = gen_gender_train_data()
    image_batch, label_batch = get_batch(image_list, label_list, IMG_W, IMG_H, BATCH_SIZE, CAPACITY)

    with tf.Session() as sess:
        i = 0
        coord = tf.train.Coordinator()
        threads = tf.train.start_queue_runners(coord=coord)
        try:
            while not coord.should_stop() and i < 2:
                # 提取出两个batch的图片并可视化。
                img, label = sess.run([image_batch, label_batch])

                for j in np.arange(BATCH_SIZE):
                    print('label: %d' % label[j])
                    plt.imshow(img[j, :, :, :])
                    plt.show()
                i += 1
        except tf.errors.OutOfRangeError:
            print('done!')
        finally:
            coord.request_stop()
        coord.join(threads)