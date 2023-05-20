# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose, Join
from w3lib.html import remove_tags
import re


class TheMuslimNavigatorItem(scrapy.Item):
    # define the fields for your item here like:
    # event_name = scrapy.Field()
    # event_link = scrapy.Field()
    # prayer_eng = scrapy.Field()
    # athan_time = scrapy.Field()
    # iqama_time = scrapy.Field()
    # prayer_ar = scrapy.Field()
    # pass
    pass


class MasjidRahmaEventsItem(scrapy.Item):
    # define the fields for your item here like:
    event_name = scrapy.Field(input_processor=MapCompose(
        remove_tags), output_processor=TakeFirst())
    event_link = scrapy.Field(input_processor=MapCompose(
        remove_tags), output_processor=TakeFirst())
    event_description = scrapy.Field(
        input_processor=MapCompose(remove_tags), output_processor=Join())
    event_image = scrapy.Field(input_processor=MapCompose(
        remove_tags), output_processor=TakeFirst())


class MasjidRahmaPrayerItem(scrapy.Item):
    # define the fields for your item here like:
    prayer_eng = scrapy.Field()
    athan_time = scrapy.Field()
    iqama_time = scrapy.Field()
    prayer_ar = scrapy.Field()
