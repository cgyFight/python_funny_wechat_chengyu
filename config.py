#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/1/23 20:20
# @Author  : Cgy
# @Site    : 
# @File    : config.py
# @Software: PyCharm

from xml.dom.minidom import parse


global_config_name = 'config.xml'
xml_phone_pic_name = 'phone_pic_name'
xml_phone_pic_dir = 'phone_pic_dir'
xml_phone_pc_dir = 'pc_save_pic_dir'
xml_phone_pc_name = 'pc_save_pic_name'
xml_adb_path = 'adb_path'
xml_recognition_type = 'pic_recognition'
xml_recognition_type_attr = 'type'
xml_baidu_element = 'baidu'
xml_baidu_attr_SECRET_KEY = 'SECRET_KEY'
xml_baidu_attr_API_KEY = 'API_KEY'
xml_baidu_attr_APP_ID = 'APP_ID'


class Config(object):
    def __init__(self, config_name):
        self.__config_name = config_name
        self.__init_config()

    @staticmethod
    def __get_text_data_from_document(dom, tag_name):
        return dom.getElementsByTagName(tag_name)[0].childNodes[0].data

    @staticmethod
    def __get_attr_value_from_document(dom, element_tag_name, attr_name):
        return dom.getElementsByTagName(element_tag_name)[0].getAttribute(attr_name)

    def __init_config(self):
        dom = parse(self.__config_name)
        self.__pic_name = self.__get_text_data_from_document(dom, xml_phone_pic_name)
        self.__phone_pic_dir = self.__get_text_data_from_document(dom, xml_phone_pic_dir)
        self.__pc_save_pic_name = self.__get_text_data_from_document(dom, xml_phone_pc_name)
        self.__pc_save_pic_dir = self.__get_text_data_from_document(dom, xml_phone_pc_dir)
        self.__adb_path = self.__get_text_data_from_document(dom, xml_adb_path)
        self.__recognition_type = self.__get_attr_value_from_document(dom, xml_recognition_type,
                                                                      xml_recognition_type_attr)
        self.__baidu_app_id = self.__get_attr_value_from_document(dom, xml_baidu_element, xml_baidu_attr_APP_ID)
        self.__baidu_api_key = self.__get_attr_value_from_document(dom, xml_baidu_element, xml_baidu_attr_API_KEY)
        self.__baidu_secret_key = self.__get_attr_value_from_document(dom, xml_baidu_element, xml_baidu_attr_SECRET_KEY)

    def get_adb_path(self):
        return self.__adb_path

    def get_pic_place_in_pc(self):
        return self.__pc_save_pic_dir + self.__pc_save_pic_name

    def get_pic_place_in_phone(self):
        return self.__phone_pic_dir + self.__pic_name

    def get_baidu_para(self):
        return [self.__baidu_secret_key, self.__baidu_api_key, self.__baidu_app_id]


if __name__ == '__main__':
    config_path = 'config.xml'
    config = Config(config_path)
    print(config.get_baidu_para())
    # print(config.get_adb_path(), config.get_pic_place_in_pc(), config.get_pic_place_in_phone())



