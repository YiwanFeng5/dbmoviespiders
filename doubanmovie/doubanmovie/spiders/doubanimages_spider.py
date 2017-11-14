#! /usr/bin/env python
# -*- coding: UTF-8 -*-
'''
    create by: Yiwan
    create on: 2017/11/13 0013
'''
from urllib import unquote

import redis
from scrapy import Selector, Request
from scrapy.spiders import CrawlSpider, Rule
from scrapy_redis.spiders import RedisMixin
from scrapy.contrib.linkextractors import LinkExtractor

from doubanmovie.items import DoubanmovieItem


class DmoxSpider2(RedisMixin,CrawlSpider):
    name = "doubanimages"
    redis_key = "doubanmovie:albums"
    rules = (Rule(LinkExtractor('http://www\.tu11\.com/\w+/\d+/\d+\.html'),callback='parse'),
             Rule(LinkExtractor('http://www\.tu11\.com/\w+/\d+/\d+_\d+\.html'),callback='parse'),
             Rule(LinkExtractor('http://www\.tu11\.com/\w+/\d+/\d+/\d+\.html'),callback='parse'),
             Rule(LinkExtractor('http://www\.tu11\.com/\w+/\d+/\d+/\d+_\d+\.html'),callback='parse'),)

    # scrapy_redis连接
    def _set_crawler(self, crawler):
        CrawlSpider._set_crawler(self, crawler)
        RedisMixin.setup_redis(self)

    def parse(self, response):
        # 获取Redis连接池
        pool = redis.ConnectionPool(host='192.168.186.199', port=6379)
        if response.status == 200:
            selector = Selector(response)
            item = DoubanmovieItem()
            # 获取图片选择器
            images = selector.xpath('//div[@class="nry"]/p')
            # 获取标题
            title = selector.xpath('//div[@class="container nrxqy"]/p[1]/text()').extract()

            if len(title) != 0:
                print "***title****", title[0]
                item['title'] = unquote(title[0])
                for image in images:
                    # 获取图片地址
                    link = image.xpath('img/@src').extract()
                    if len(link) != 0:
                        print "+++imege_url++++",link[0]
                        item['link'] = link[0]
                        # 获取Redis链接
                        conn = redis.Redis(connection_pool=pool)
                        # 将获取到的图片放入Redis中保存
                        conn.lpush('doubanmovie:images',item)
            # 获取下一页链接
            next_url = selector.xpath('//div[@class="row dede_pages"]/ul/li[last()]/a/@href').extract()[0]
            next_url = response.url[:response.url.rindex("/")+1] + next_url
            print "!!!!next_url!!!!",next_url
            # 如果为#则本相册已经爬取完毕
            if next_url == "#":
                return
        else:
            conn = redis.Redis(connection_pool=pool)
            conn.lpush("doubanmovie:albums",response.url)
        # 继续爬取下一页
        yield Request(next_url,meta={},callback='parse')