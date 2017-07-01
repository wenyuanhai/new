#coding=utf-8
import pymongo
from scrapy.conf import settings

class IgnoreRequest(object):
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

    def process_request(self,request, spider):
        # print 66666666666
        # print request.url
        # if self.post.find({"url":})
        pass
    def process_response(self,request, response, spider):
        # print response.url
        return response