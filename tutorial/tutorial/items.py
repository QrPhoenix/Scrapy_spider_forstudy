# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://doc.scrapy.org/en/latest/topics/items.html
# 爬取的主要目标就是从非结构性的数据源提取结构性数据，例如网页。 Scrapy提供 Item 类来满足这样的需求。
import scrapy


class TutorialItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class DmoztoolsItem(scrapy.Item):
    # Field 仅仅是内置的 dict 类的一个别名，并没有提供额外的方法或者属性。换句话说， Field 对象完完全全就是Python字典(dict)。被用来基于类属性(class attribute)的方法来支持 item声明语法 。
    title = scrapy.Field()
    link = scrapy.Field()
    desc = scrapy.Field()
