# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import json
from scrapy.conf import settings
import pymongo

class JinritoutiaoPipeline(object):
    def __init__(self):
        self.f  = open("down.json","a")
        #主机号
        host = settings["MONGODB_HOST"]
        # 端口号，默认是27017
        port = settings["MONGODB_PORT"]
        # 设置数据库名称
        db = settings["MONGODB_DBNAME"]
        # 存放本次数据的表名称
        dbc = settings["MONGODB_DOCNAME"]
        client = pymongo.MongoClient(host=host,port=port)
        dblink = client[db]
        self.post = dblink[dbc]
    def process_item(self, item, spider):
        jsonfile = json.dumps(dict(item),ensure_ascii=False)
        # link = item["url"]
        # num = self.post.find({"url": link})
        # print num
        # if not num.count():
        self.post.insert(dict(item))
        self.f.write(jsonfile.encode("utf-8")+"\n")
        return item
    def close_spider(self,item):
        self.f.close()

