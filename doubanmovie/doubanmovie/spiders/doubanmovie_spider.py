#! /usr/bin/env python
# -*- coding: UTF-8 -*-
'''
    create by: Yiwan
    create on: 2017/11/11 0011
'''
import os
from urllib import unquote, urlretrieve

import scrapy
from scrapy import Selector, Request, spider

from doubanmovie.items import DoubanmovieItem
from scrapy.spiders import Rule, CrawlSpider
from scrapy.contrib.linkextractors import LinkExtractor
import scrapy_redis
from scrapy_redis.spiders import RedisMixin
import redis

pages = 0   # 页数计数器
spider_list = ['']    # 待爬序列

class DmoxSpider(scrapy.Spider):
    name = 'doubanmovie'
    start_urls = ['http://www.tu11.com/meituisiwatupian']
    # redis_key = 'doubanmovie:start_urls'
    rules = Rule(LinkExtractor(allow=('http://www.tu11.com/meituisiwatupian/list_2_\d+.html',)),callback='parse'),

    # 该方法是最关键的方法，该方法名以下划线开头，建立了和redis的关系
    # def _set_crawler(self, crawler):
    #     CrawlSpider._set_crawler(self,crawler)
    #     RedisMixin.setup_redis(self)

    def parse(self, response):
        '''获取每个页面所有的相册链接'''

        print "!!!!!!!!!!!!!!!!",response.status
        if response.status == 200:
            selector = Selector(response)
            item = DoubanmovieItem()
            # 绑定全局变量
            global pages
            global spider_list
            # 获取最大页数
            end_page_url = selector.xpath('//div[@class="pageinfo"]/a[last()]/@href').extract()[0]
            end_page_str = end_page_url[end_page_url.index("2_")+2:end_page_url.index(".")]
            end_page = int(end_page_str)
            # print "mmmmmmmmmmmmmmm", pages

            # 如果pages小于最大页数，就获取下一页地址

            if pages < end_page:

                next_url_end = selector.xpath('//div[@class="pageinfo"]/a[last()-1]/@href').extract()[0]
                next_url = "http://www.tu11.com/meituisiwatupian/" + next_url_end
                print "+++++++++++++++++",next_url
                spider_list.append(next_url)
                # 获取redis连接
                conn = redis.Redis(host='192.168.186.199',port=6379)
                conn.lpush('doubanmovie:start_urls',next_url)
                # 爬取当前页面所有li
                # lis = selector.xpath('//div[@class="row"]/ul/li')
                #
                # for li in lis:
                #     link = li.xpath('div/a/@href').extract()
                #     title = li.xpath('div/p/a[1]/b/text()').extract()
                #
                #     # 根据title创建文件夹
                #     # os.makedirs('c:\\Users\\Yiwan\\Desktop\\images\\%s' % (title[0].encode("GBK")))
                #
                #     if len(title)!=0 and len(link)!=0:
                #         # 将title和link放到item中
                #         item['title'] = unquote(title[0])
                #         item['link'] = "http://www.tu11.com" + link[0]
                #
                #         print "***********",title[0],"-----",link[0]

                pages += 1
        else:
            conn = redis.Redis(host='192.168.186.199',port=6379)
            conn.lpush("doubanmovie:start_urls")
        if pages == end_page:
            print "爬取完毕！！！"
            return
        yield Request(next_url,meta={},callback=self.parse)

    #     print "++++++++++++++++",results
    #     for result in results:
    #         link = result.xpath('li/div/a/@href').extract()
    #         title = result.xpath('li/div/p/a/b/text()').extract()
    #         print "********", title, "---", link
    #         item['link'] = 'http://www.tu11.com' + link[0]
    #         item['title'] = unquote(title[0])
    #
    #         yield Request(item['link'],meta={'item':item,'title':title},callback=self.parse2)
    # def parse2(self,response):
        # item = response.meta['item']
        # title = response.meta['title']
        # selector = Selector(response)
        # results = selector.xpath('//div[@class="row"]/ul')
        # print "2222222222222222222", results
        # for result in results:
        #     os.makedirs('c:\\Users\\Yiwan\\Desktop\\images\\%s' % (title[0].encode("GBK")))
        #     images =  result.xpath('p/img/@src').extract()
        #     index = 0
        #     for image in images:
        #         urlretrieve(image, "c:\\Users\\Yiwan\\Desktop\\images\\%s\\%s.jpg" % (title[0].encode("GBK"), str(index)))
        #         index += 1
        # return item

# class GoSpider():
#     next_url = spider_list.pop()
#     yield Request()