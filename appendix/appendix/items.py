# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html

import scrapy


class KPItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    module = scrapy.Field()
    title = scrapy.Field()
    pubTime = scrapy.Field()
    content = scrapy.Field()


class SingleModuleItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    # module = scrapy.Field()
    content = scrapy.Field()
    pubTime = scrapy.Field()
    title = scrapy.Field()