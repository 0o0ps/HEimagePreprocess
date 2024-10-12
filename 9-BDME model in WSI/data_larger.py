import PIL.Image as Image
import os
from torchvision import transforms as transforms
import os
import sys
import json
import pickle
import random

import torch
from tqdm import tqdm
import matplotlib.pyplot as plt


def read_split_data(root: str, val_rate: float = 0.1):
    random.seed(0)  # 保证随机结果可复现
    assert os.path.exists(root), "dataset root: {} does not exist.".format(root)

    # 遍历文件夹，一个文件夹对应一个类别
    flower_class = [cla for cla in os.listdir(root) if os.path.isdir(os.path.join(root, cla))]
    # 排序，保证各平台顺序一致
    flower_class.sort()
    # 生成类别名称以及对应的数字索引
    class_indices = dict((k, v) for v, k in enumerate(flower_class))
    json_str = json.dumps(dict((val, key) for key, val in class_indices.items()), indent=4)
    with open('class_indices.json', 'w') as json_file:
        json_file.write(json_str)

    train_images_path = []  # 存储训练集的所有图片路径
    train_images_label = []  # 存储训练集图片对应索引信息
    val_images_path = []  # 存储验证集的所有图片路径
    val_images_label = []  # 存储验证集图片对应索引信息
    every_class_num = []  # 存储每个类别的样本总数
    supported = [".jpg", ".JPG", ".png", ".PNG"]  # 支持的文件后缀类型
    # 遍历每个文件夹下的文件
    for cla in flower_class:
        cla_path = os.path.join(root, cla)
        # 遍历获取supported支持的所有文件路径
        images = [os.path.join(root, cla, i) for i in os.listdir(cla_path)
                  if os.path.splitext(i)[-1] in supported]
        # 排序，保证各平台顺序一致
        images.sort()
        # 获取该类别对应的索引
        image_class = class_indices[cla]
        # 记录该类别的样本数量
        every_class_num.append(len(images))
        # 按比例随机采样验证样本
        val_path = random.sample(images, k=int(len(images) * val_rate))

        for img_path in images:
            if img_path in val_path:  # 如果该路径在采样的验证集样本中则存入验证集
                val_images_path.append(img_path)
                val_images_label.append(image_class)
            else:  # 否则存入训练集
                train_images_path.append(img_path)
                train_images_label.append(image_class)

    print("{} images were found in the dataset.".format(sum(every_class_num)))
    print("{} images for training.".format(len(train_images_path)))
    print("{} images for validation.".format(len(val_images_path)))
    assert len(train_images_path) > 0, "number of training images must greater than 0."
    assert len(val_images_path) > 0, "number of validation images must greater than 0."

    plot_image = False
    if plot_image:
        # 绘制每种类别个数柱状图
        plt.bar(range(len(flower_class)), every_class_num, align='center')
        # 将横坐标0,1,2,3,4替换为相应的类别名称
        plt.xticks(range(len(flower_class)), flower_class)
        # 在柱状图上添加数值标签
        for i, v in enumerate(every_class_num):
            plt.text(x=i, y=v + 5, s=str(v), ha='center')
        # 设置x坐标
        plt.xlabel('image class')
        # 设置y坐标
        plt.ylabel('number of images')
        # 设置柱状图的标题
        plt.title('flower class distribution')
        plt.show()
    
    # /mnt/mydisk/chenying/HE_yxl/data_large/0/0_B10_ROI8_1.png
    # 0
    print(train_images_path[0])
    print(train_images_label[0])
    return train_images_path, train_images_label, val_images_path, val_images_label

train_images_path, train_images_label, val_images_path, val_images_label = read_split_data('/mnt/mydisk/chenying/HE_densnet/data')

for img_path in train_images_path:
    im = Image.open(img_path)
    im.save(img_path.replace('data', 'data_train'))

for img_path in val_images_path:
    im = Image.open(img_path)
    im.save(img_path.replace('data', 'data_val'))

img_list = os.listdir('/mnt/mydisk/chenying/HE_densnet/data_train/0/')
outfile = '/mnt/mydisk/chenying/HE_densnet/data_train_large/0/'
readfile = '/mnt/mydisk/chenying/HE_densnet/data_train/0/'

for img_name in img_list:
    print(img_name)
    im = Image.open(readfile + img_name)
    im.save(outfile + '0_' + img_name)
    new_im = transforms.RandomHorizontalFlip(p=1)(im)   # p表示概率
    new_im.save(outfile + '1_' + img_name)
    new_im = transforms.RandomVerticalFlip(p=1)(im)
    new_im.save(outfile + '2_' + img_name)
    new_im = transforms.ColorJitter(brightness=[0.8,0.8])(im)
    new_im.save(outfile + '3_' + img_name)

img_list = os.listdir('/mnt/mydisk/chenying/HE_densnet/data_train/1/')
outfile = '/mnt/mydisk/chenying/HE_densnet/data_train_large/1/'
readfile = '/mnt/mydisk/chenying/HE_densnet/data_train/1/'

for img_name in img_list:
    print(img_name)
    im = Image.open(readfile + img_name)
    im.save(outfile + '0_' + img_name)
    new_im = transforms.RandomHorizontalFlip(p=1)(im)   # p表示概率
    new_im.save(outfile + '1_' + img_name)
    new_im = transforms.RandomVerticalFlip(p=1)(im)
    new_im.save(outfile + '2_' + img_name)
    new_im = transforms.ColorJitter(brightness=[0.8,0.8])(im)
    new_im.save(outfile + '3_' + img_name)