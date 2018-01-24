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

def get_phone_img_to_pc(adb_path, pic_place_in_pc, pic_place_in_phone):
    # os.system(adb_path + ' devices')
    screen_capture_order = adb_path + ' shell screencap -p ' + pic_place_in_phone# + ' ' + pic_place_in_pc
    screen_push_order = adb_path + ' pull ' + pic_place_in_phone + ' ' + pic_place_in_pc
    os.system(screen_capture_order)
    os.system(screen_push_order)

def get_file_content(file_path):
    with open(file_path, 'rb') as fp:
        return fp.read()

startX = 52
startY = 1279
endX = 1031
endY = 1664
picW = 113
picH = 121
pic_ver_inter = 11 #图片左右距离
pic_hor_inter = 11 #上下图片距离

def pic_draw(draw, rectangle):
    draw.rectangle(rectangle, outline=255)

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

    def get_word_index(self, position):
        """
        传入识别的字的位置，返回这个字的属于__position_dict中的哪一个key
        :param position:
        :return word_key:
        """
        for key in self.__position_dict.keys():
            value = self.__position_dict.get(key)
            a = re
            if ()

        return key



Position



if __name__ == '__main__':
    # get_phone_img_to_pc()
    box = [47, 1267, 1059, 1681]
    config = config.Config('config.xml')
    # get_phone_img_to_pc(config.get_adb_path(), config.get_pic_place_in_pc(), config.get_pic_place_in_phone())
    # crop_pic(test_jpg, box)
    secret_key, api_key, app_id = config.get_baidu_para()
    baidu_client = AipOcr(app_id, api_key, secret_key)

    # pic_draw(test_jpg)
    word_position_init()

    options = dict()
    # options['recognize_granularity'] = 'big'
    # re = baidu_client.general(get_file_content(tmp_pic_name), options)
    # print(re)
    options['recognize_granularity'] = 'small'
    options['probability'] = 'true'
    # re = baidu_client.general(get_file_content(tmp_pic_name), options)
    # re = baidu_client.accurate(get_file_content(tmp_pic_name), options)
    # print(re)





