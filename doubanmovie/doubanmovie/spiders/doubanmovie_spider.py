#! /usr/bin/env python
# -*- coding: UTF-8 -*-
'''
    create by: Yiwan
    create on: 2017/11/11 0011
'''

import scrapy
from scrapy import Selector


class DmoxSpider(scrapy.Spider):
    name = 'doubanmovie'
    start_urls = ['http://seniu1.com/tupian/yazhoutupian/']

    def parse(self, response):
        selector = Selector(response)
        results = selector.xpath('//div[@id="text_list"]/div/dl')
        print "**********",results
