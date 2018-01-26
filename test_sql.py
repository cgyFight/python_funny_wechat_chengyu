#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/1/26 18:21
# @Author  : Cgy
# @Site    : 
# @File    : test_sql.py
# @Software: PyCharm

import sqlite3
import os
import time



tab_name = 'chengyu'
def create_database_and_init(file_name):
    # 创建数据库
    db_name = 'example.db'
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    zi_duan = ('1', '2', '3', '4')

    create_order = '''CREATE TABLE ''' + tab_name + '''('%s', '%s', '%s', '%s')''' % zi_duan
    cursor.execute(create_order)
    print(os.getcwd())

    with open(file_name, 'r', encoding='UTF-8') as f:
        cheng_yu_count = 0
        allc = 0
        for cheng_yu in f.readlines():
            allc += 1
            cheng_yu = cheng_yu.strip()
            if len(cheng_yu) == 4:
                cheng_yu_count += 1
                print(cheng_yu_count)
                insert_order = "INSERT INTO " + tab_name + ' VALUES' + " ('%s', '%s', '%s', '%s')" % tuple(cheng_yu)
                print(insert_order)
                cursor.execute(insert_order)
            else:
                print(cheng_yu, 'is not 4\n')
        print('over loop')
        conn.commit()
        print('over commit')
        conn.close()


if __name__ == "__main__":
    file_name = 'data.txt'
    # create_database_and_init(file_name)
    db_name = 'example.db'
    conn = sqlite3.connect(db_name)
    cursor = conn.cursor()
    start = time.time()
    order = 'select * from ' + tab_name + ' where "1" = "一" or "2" = "一" '
    cursor.execute(order)
    end = time.time()
    print('use time', end - start)
    re = cursor.fetchall()
    print(re)
    print(len(re))




