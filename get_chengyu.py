#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2018/1/25 15:39
# @Author  : Cgy
# @Site    : 
# @File    : get_chengyu.py
# @Software: PyCharm

from threading import Thread
import time
import requests
from queue import Queue
import queue
import json
from asyncio import Semaphore

url = 'https://sp0.baidu.com/8aQDcjqpAAV3otqbppnN2DJv/api.php?resource_id=28204&from_mid=1&&format=json&ie=utf-8&oe=utf-8&query=%E6%88%90%E8%AF%AD%E5%A4%A7%E5%85%A8&sort_key=&sort_type=1&stat0=&stat1=&stat2=&stat3=&pn='
url_end = '&rn=30&_=1516885908487'
data_file = 'data.txt'
err_url_file = 'errUrl.txt'


class NetThread(Thread):
    def __init__(self, name, url_queue, data_queue, err_url_queue, semaphore=None):
        Thread.__init__(self)
        self.__url_queue = url_queue
        self.__data_queue = data_queue
        self.__erro_url_queue = err_url_queue
        self.__name = name
        self.__semaphore = semaphore

    def run(self):
        # 当url队列中的数据全部取完时结束线程
        while self.__url_queue.qsize() != 0:
            new_url = self.__url_queue.get()
            re = requests.get(new_url)
            if re.status_code != 200:
                print('url 200:', new_url)
                if isinstance(self.__semaphore, Semaphore):
                    self.__erro_url_queue.put(new_url)
                    self.__semaphore.release()
            else:
                print(re.text)
                js = json.loads(re.text)
                print(js)
                if js['data'] == [None]:
                    if isinstance(self.__semaphore, Semaphore):
                        s = '====data none===\n'
                        self.__erro_url_queue.put(s + new_url)
                        self.__semaphore.release()
                else:
                    result = js["data"][0]["result"]
                    for name in result:
                        self.__data_queue.put(name['ename'])


class WriteThread(Thread):
    def __init__(self, data_queue, file_name, time_out=None, semaphore=None):
        Thread.__init__(self)
        self.__data_queue = data_queue
        self.__stop = False
        self.__file_name = file_name
        self.__time_out = time_out
        self.__semaphore = semaphore

    def stop(self):
        print('stop')
        self.__stop = True

    def run(self):
        count = 0
        with open(self.__file_name, 'a', encoding='utf-8') as f:
            while not self.__stop:
                if isinstance(self.__semaphore, Semaphore):
                    self.__semaphore.acquire()
                    print('-----get-----err---------url-------')
                try:
                    f.write(self.__data_queue.get(timeout=self.__time_out))
                    f.write("\n")
                    count += 1
                except queue.Empty:
                    print('rase')

        print('count = ', count)
        return


class ChengYuCrawler(object):
    def __init__(self, thread_num, ye_shu, semaphore, timeout):
        self.__url_queue = Queue()
        self.__data_queue = Queue()
        self.__erro_url_queue = Queue()
        self.__thread_store = []
        self.__yeshu = ye_shu
        self.__semaphore = semaphore
        self.__init_url_queue()
        self.__timeout = timeout

        for i in range(0, thread_num):
            # 创建线程
            thread = NetThread('thread-' + ('%d' % i).zfill(2),
                               self.__url_queue,
                               self.__data_queue,
                               self.__erro_url_queue,
                               self.__semaphore)
            # 将线程变量保存
            self.__thread_store.append(thread)

    def __init_url_queue(self):
        for i in range(0, self.__yeshu):
            new_url = url + str(i * 30) + url_end
            self.__url_queue.put(new_url)

    def begin(self):
        for thread in self.__thread_store:
            thread.start()

        # 不使用信号量，设置为保存erro url时设置
        write_thread = WriteThread(self.__data_queue, data_file, time_out=self.__timeout)
        write_thread.start()

        write_err_thread = WriteThread(self.__erro_url_queue,
                                       err_url_file,
                                       time_out=self.__timeout,
                                       semaphore=self.__semaphore
                                       )
        write_err_thread.start()

        print('start-wait')
        for thread in self.__thread_store:
            thread.join()
        print('over thread')
        while True:
            if self.__url_queue.qsize() != 0:
                print('data queue size is ', self.__data_queue.qsize())
                time.sleep(1)
                continue
            else:
                print('stop - write thread')
                write_thread.stop()
                write_thread.join()
                print('all - over!')
                if self.__data_queue.qsize() == 0:
                    write_err_thread.stop()
                    write_err_thread.join()
                    print('all write - over!')
                return


def test_write_thread():
    __data_queue = Queue()
    for i in range(0, 200):
        __data_queue.put(u'你好\n')
        __data_queue.put(u'我好\n')
        __data_queue.put(u'大家好\n')
    print('test init over')
    write_thread = WriteThread(__data_queue, 'test.txt' )
    write_thread.start()
    while write_thread.is_alive():
        if __data_queue.qsize() == 0:
            print('stop - write thread')
            write_thread.stop()
            write_thread.join()
            print('all - over!')
        else:
            print('not over')
            time.sleep(1)
            continue


if __name__ == '__main__':
    # test_write_thread()
    s = Semaphore(0)
    c = ChengYuCrawler(10, 1030, s, 5)
    c.begin()








