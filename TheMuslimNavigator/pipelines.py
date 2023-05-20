# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import pymongo
from scrapy import conf
from scrapy.exceptions import DropItem
from scrapy import log


class MongoDBPipeline(object):
    def __init__(self):
        connection = pymongo.MongoClient(
            conf.settings['MONGODB_SERVER'],
            conf.settings['MONGODB_PORT']
        )
        db = connection[conf.settings['MONGODB_DB']]
        self.collection = db[conf.settings['MONGODB_COLLECTION']]

    def process_item(self, item, spider):
        valid = True
        for data in item:
            if not data:
                valid = False
                raise DropItem("Missing {0}!".format(data))
        if valid:
            self.collection.insert(dict(item))
            log.msg("event added to MongoDB database!",
                    level=log.DEBUG, spider=spider)
        return item
