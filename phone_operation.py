#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/1/23 16:40
# @Author  : Cgy
# @Site    : 
# @File    : phone_operation2.py
# @Software: PyCharm

import os
from PIL import Image, ImageDraw
import config
from aip import AipOcr

tmp_pic_name = 'tmp.jpg'
test_jpg = './tmp/test.jpg'


def crop_pic(pic_name, targ_box):
    im = Image.open(pic_name)
    assert isinstance(im, Image.Image)
    new_im = im.crop(targ_box)
    new_im.save(tmp_pic_name)
    # new_im.show()


def get_file_content(file_path):
    with open(file_path, 'rb') as fp:
        return fp.read()


def pic_draw(draw, rectangle):
    draw.rectangle(rectangle, outline=255)


class GameOperation(object):
    def __init__(self, adb_path):
        self.__adb_path = adb_path

    # 模拟点击
    def simulation_click(self, point):
        click_order = self.__adb_path + ' shell input tap %d %d' % point
        os.system(click_order)

    # 将图片从手机移动到图片
    def get_phone_img_to_pc(self, pic_place_in_pc, pic_place_in_phone):
        # os.system(adb_path + ' devices')
        screen_capture_order = self.__adb_path + ' shell screencap -p ' + pic_place_in_phone
        screen_push_order = self.__adb_path + ' pull ' + pic_place_in_phone + ' ' + pic_place_in_pc
        os.system(screen_capture_order)
        os.system(screen_push_order)

    def cancer_answer(self, index):
        """
        取消答案
        :param index: 取消填入的第几个1,2,3,4
        :return:
        """
        y = 1169
        switch = {
            '1': (325, y),
            '2': (447, y),
            '3': (575, y),
            '4': (707, y),
        }
        self.simulation_click(switch[str(index)])


startX = 52
startY = 1279
endX = 1031
endY = 1664
picW = 113
picH = 121
pic_ver_inter = 11 #图片左右距离
pic_hor_inter = 11 #上下图片距离


class Position(object):
    def __init__(self):
        self.__position_dict = self.__word_position_init()

    # 初始化各个字的位置
    @staticmethod
    def __word_position_init():
        dic_position = dict()
        # im = Image.open(test_jpg)
        # draw = ImageDraw.Draw(im)
        for i in range(0, 3):
            for j in range(0, 8):
                key = '%d%d' % (i, j)
                left = j * (pic_ver_inter + picW) + startX
                top = startY + i * (picH + pic_hor_inter)
                right = left + picW
                bottom = top + picH
                dic_position[key] = [left, top, right, bottom]
                # pic_draw(draw, abc[key])
        # im.show()
        # print(abc)
        return dic_position

    @staticmethod
    def transform_word_position_to_rectangle(position):
        """
        :param position: {'left':x, 'top':y, 'height':h, 'width':w}
        :return rectangle:[left, top, right, bottom]:
        """
        return [position['left'], position['top'],
                position['left'] + position['width'], position['top'] + position['height']]

    def get_word_index(self, position, crop_box):
        """
        传入识别的字的位置，返回这个字的属于__position_dict中的哪一个key
        :param position:
        :param crop_box: 截图的区域，需要使用这个参数去恢复到原图坐标
        :return word_key:
        """
        position_in_src_pic = dict().fromkeys(position.keys())
        for k in position_in_src_pic:
            position_in_src_pic[k] = position[k]
        position_in_src_pic['left'] += crop_box[0]
        position_in_src_pic['top'] += crop_box[1]

        position = self.transform_word_position_to_rectangle(position_in_src_pic)
        # for key, value in self.__position_dict.keys():
        for key, value in self.__position_dict.items():
            if position[0] > value[0] and position[1] > value[1] and position[2] < value[2] and position[3] < value[3] :
                return key
        return ''

    # 取中点
    def get_point_of_word(self, key):
        rectangle = self.__position_dict[key]
        return ((rectangle[0] + rectangle[2]) / 2,
                (rectangle[1] + rectangle[3]) / 2)


if __name__ == '__main__':
    # 获取配置
    config = config.Config('config.xml')

    # 初始化adb路径
    adb = GameOperation(config.get_adb_path())

    # 初始化按键位置信息
    postion = Position()

    # 初始化百度识字
    # secret_key, api_key, app_id = config.get_baidu_para()
    # baidu_client = AipOcr(app_id, api_key, secret_key)

    # 从手机上截屏并推送到电脑
    # adb.get_phone_img_to_pc(config.get_adb_path(), config.get_pic_place_in_pc(), config.get_pic_place_in_phone())
    # 裁剪到文字部分
    box = [47, 1267, 1059, 1681]
    # crop_pic(test_jpg, box)

    # 识字
    options = dict()
    # options['recognize_granularity'] = 'big'
    # re = baidu_client.general(get_file_content(tmp_pic_name), options)
    # print(re)
    options['recognize_granularity'] = 'small'
    options['probability'] = 'true'
    # re = baidu_client.general(get_file_content(tmp_pic_name), options)
    # re = baidu_client.accurate(get_file_content(tmp_pic_name), options)
    # print(re)

    # 解析字
    # 查询是否有成语
    # 获取成语字的位置
    a_char = {'char': '小', 'location': {'width': 42, 'top': 47, 'height': 53, 'left': 163}}
    b_char = {'char': '长', 'location': {'width': 42, 'top': 47, 'height': 53, 'left': 289}}
    c_char = {'char': '日', 'location': {'width': 40, 'top': 312, 'height': 49, 'left': 294}}
    print(postion.get_word_index(a_char['location'], box))
    print(postion.get_word_index(b_char['location'], box))
    print(postion.get_word_index(c_char['location'], box))
    # 模拟点击
    point = postion.get_point_of_word( postion.get_word_index(a_char['location'], box))
    adb.simulation_click(point)
    point = postion.get_point_of_word( postion.get_word_index(b_char['location'], box))
    adb.simulation_click(point)
    point = postion.get_point_of_word( postion.get_word_index(c_char['location'], box))
    adb.simulation_click(point)

    adb.cancer_answer(1)
    adb.cancer_answer(2)
    adb.cancer_answer(3)

    # pic_draw(test_jpg)








