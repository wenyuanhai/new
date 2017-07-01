# -*- coding: utf-8 -*-
import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from jinritoutiao.items import JinritoutiaoItem
import json
import jsonpath,time
import requests
from lxml import etree
from scrapy import selector
import datetime
import pymongo
from scrapy.conf import settings

class JinriSpider(scrapy.Spider):
    time = str(int(time.time()))
    url = "http://www.toutiao.com/api/pc/feed/?category=news_tech&utm_source =toutiao&widen=1" \
          "&max_behot_time=1498694400&max_behot_time_tmp="+time+"&tadrequire=true"
    name = 'jinri'
    allowed_domains = ['www.toutiao.com']
    start_urls = [url]
    def __init__(self):
        # 主机号
        host = settings["MONGODB_HOST"]
        # 端口号，默认是27017
        port = settings["MONGODB_PORT"]
        # 设置数据库名称
        db = settings["MONGODB_DBNAME"]
        # 存放本次数据的表名称
        dbc = settings["MONGODB_DOCNAME"]
        client = pymongo.MongoClient(host=host, port=port)
        dblink = client[db]
        self.post = dblink[dbc]

    def parse(self, response):
        jsont =  response.body
        pyt = json.loads(jsont)
        urls = jsonpath.jsonpath(pyt,"$..group_id")
        return self.deal_request(urls)

    def deal_links(self,link):
        url = "http://www.toutiao.com/a"+link
        return url

    def deal_request(self,urls):
        headers = {
            "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.111 Safari/537.36",
        }
        item = JinritoutiaoItem()
        for link in urls:
            now = datetime.datetime.now()
            url = self.deal_links(link)
            if self.post.find({"url":url}).count():
                continue
            else:
                rep = etree.HTML(requests.get(url, headers=headers).text)
                item["title"] = rep.xpath("//h1/text()")
                item["content"] = rep.xpath('//div[@class="article-content"]/div/p/text()')
                item["time"] = now.strftime("%Y-%m-%d %H:%M:%S")
                item["url"] = url
                if item["title"] == []:
                    continue
                else:
                    item["title"] = item["title"][0]

                if item["content"] == []:
                    continue
                else:
                    item["content"]="".join(item["content"])
                yield item