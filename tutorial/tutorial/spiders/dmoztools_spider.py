import scrapy

from tutorial.items import DmoztoolsItem


class DmozSpider(scrapy.Spider):
    # 用于区别Spider。 该名字必须是唯一的，您不可以为不同的Spider设定相同的名字。
    name = "dmoztools"

    allowed_domains = ["dmoztools.net"]
    # 包含了Spider在启动时进行爬取的url列表。 因此，第一个被获取到的页面将是其中之一。 后续的URL则从初始的URL获取到的数据中提取。
    start_urls = [
        "https://dmoztools.net/Computers/Programming/Languages/Python/Books/",
        "https://dmoztools.net/Computers/Programming/Languages/Python/Resources/"
    ]

    def parse(self, response):
        # filename = response.url.split("/")[-2]
        # with open(filename, 'wb') as f:
        #     f.write(response.body)
        for sel in response.xpath('//ul/li'):
            item = DmoztoolsItem()
            item['title'] = sel.xpath('a/text()').extract()
            item['link'] = sel.xpath('a/@href').extract()
            item['desc'] = sel.xpath('text()').extract()
            yield item