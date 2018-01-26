#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/1/26 16:56
# @Author  : Cgy
# @Site    : 
# @File    : main.py
# @Software: PyCharm

import phone_operation
import config



if __name__ == '__main__':
    # 获取配置
    config = config.Config('config.xml')

    # 初始化adb路径
    adb = phone_operation.GameOperation(config.get_adb_path())

    # 初始化按键位置信息
    postion = phone_operation.Position()

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

