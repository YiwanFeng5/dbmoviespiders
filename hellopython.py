#! /usr/bin/env python
# -*- coding: UTF-8 -*-
'''
    create by: Yiwan
    create on: 2017/11/11 0011
'''

import redis

conn = redis.Redis(host='192.168.186.199',port=6379)
# conn.set("test","zhang")
print "redis测试添加数据完成"
print "redis测试读取数据："
print conn.lrange("doubanmovie:albums",0,-1)
