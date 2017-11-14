#! /usr/bin/env python
# -*- coding: UTF-8 -*-
'''
    create by: Yiwan
    create on: 2017/11/11 0011
'''

from urllib import unquote

import redis
from scrapy import Selector, Request

from doubanmovie.items import DoubanmovieItem
from scrapy.spiders import Rule, CrawlSpider
from scrapy.contrib.linkextractors import LinkExtractor

from scrapy_redis.spiders import RedisMixin



class DmoxSpider1(RedisMixin,CrawlSpider):
    name = 'doubanitem'
    redis_key = 'doubanmovie:start_urls'
    rules = Rule(LinkExtractor(allow=('http://www.tu11.com/meituisiwatupian/list_2_\d+.html',)),callback='parse'),

    # 该方法是最关键的方法，该方法名以下划线开头，建立了和redis的关系
    def _set_crawler(self, crawler):
        CrawlSpider._set_crawler(self,crawler)
        RedisMixin.setup_redis(self)

    def parse(self, response):
        '''获取每个页面所有的相册链接'''

        print "!!!!!!!!!!!!!!!!",response.status

        # 获取Redis连接池
        pool = redis.ConnectionPool(host='192.168.186.199', port=6379)
        # 如果响应成功
        if response.status == 200:
            selector = Selector(response)

            # 获取当前页面所有相册
            albums = selector.xpath('//div[@class="row"]/ul/li')
            # 遍历获取每个相册信息
            for album in albums:
                # 获取相册标题
                title = album.xpath('div/p/a/b/text()').extract()
                # 获取相册链接
                link =  album.xpath('div/a/@href').extract()
                # 放入redis
                if len(title)!=0 and len(link)!=0:

                    print "**************",title[0],"-----",link[0]
                    conn = redis.Redis(connection_pool=pool)
                    conn.lpush('doubanmovie:albums',"http://www.tu11.com"+link[0])
        else:   # 失败请求失败的url重新加入待爬队列
            conn = redis.Redis(connection_pool=pool)
            conn.lpush('doubanmovie:start_urls',response.url)
        return
