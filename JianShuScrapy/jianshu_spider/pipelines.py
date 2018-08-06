# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
from pymongo import MongoClient
from pymongo.errors import DuplicateKeyError
from traceback import format_exc
from .items import *
from .utils.init_utils import init_add_request


class JianShuMongoPipeline(object):
    def __init__(self, mongo_uri, mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db
        self.client = None
        self.db = None

    @classmethod
    def from_crawler(cls, crawler):
        return cls(
            mongo_uri=crawler.settings.get('MONGODB_URI'),
            mongo_db=crawler.settings.get('MONGODB_DATABASE', 'items')
        )

    def open_spider(self, spider):
        self.client = MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]
        self.db['article'].ensure_index('article_url', unique=True)
        items = self.db['article'].find({})
        for item in items:
            init_add_request(spider, item['article_url'])

    def close_spider(self, spider):
        _ = spider
        self.client.close()

    def process_item(self, item, spider):
        print(item)
        try:
            if isinstance(item, ArticleItem):
                self.db['article'].update({'article_url': item['article_url']}, {'$set': item}, upsert=True)
        except DuplicateKeyError:
            spider.logger.debug('duplicate key error collection')
        except Exception as e:
            _ = e
            spider.logger.error(format_exc())
        return item
