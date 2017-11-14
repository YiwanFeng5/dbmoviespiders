#! /usr/bin/env python
# -*- coding: UTF-8 -*-
'''
    create by: Yiwan
    create on: 2017/11/13 0013
'''

import os

import threading

from urllib import urlretrieve
from threading import Thread
import demjson
import redis

index = 0
def saveImage(title,url):
    global index
    # 保存图片
    threading.Thread(target=urlretrieve,args=(url,"E:\\Media\\images\\%s\\%s.jpg" % (title.encode("GBK"), str(index)))).start()
    # urlretrieve(url, "E:\\Media\\images\\%s\\%s.jpg" % (title.encode("GBK"), str(index)))
    print "************nodes['title']: ",title," nodes['link']: ",url
    index += 1

class saveThread(threading.Thread):
    def __init__(self,threadID,name,counter,redis_pool):
        threading.Thread.__init__(self)
        self.threadID = threadID
        self.name = name
        self.counter = counter
        self.redis_pool = redis_pool
    def run(self):
        print "--------------Starting: ",self.name
        redis_conn = redis.Redis(connection_pool=self.redis_pool)
        while str(redis_conn.lpop("doubanmovie:images")) != "nil":
            image_item = str(redis_conn.lpop("doubanmovie:images")).replace(" u"," ",2)
            print "!!!!!!!!" + image_item
            if image_item == 'None':
                print "图片已经全部保存完成！！！"
                return
            # image_item_json = demjson.encode(image_item)
            nodes = demjson.decode(image_item)
            # 获取标题并创建文件夹
            image_title = nodes['title']
            # 命名文件夹
            image_path = 'E:\\Media\\images\\%s' % (image_title.encode("GBK"))
            # 判断文件夹名是否已经存在
            if not os.path.exists(image_path):
                os.makedirs(image_path)
            # 获取图片地址
            image_url = nodes['link']
            saveImage(title=image_title,url=image_url)
        print "--------------Exiting: ",self.name


if __name__ == '__main__':
    pool = redis.ConnectionPool(host='192.168.186.199',port=6379)
    # 创建多线程运代码
    for i in range(1,4,1):
        saveThread(i,"SaveThread - "+str(i),i,pool).start()