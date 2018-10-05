# -*- coding: utf-8 -*-
from scrapy.http import Request
from scrapy.spiders import CrawlSpider
from scrapy.selector import Selector
from douban.items import DoubanItem
class Doubn(CrawlSpider):
        name = "douban"
        start_urls = ['http://movie.douban.com/top250']
        url = 'http://movie.douban.com/top250'
        def parse(self, response):
            # print(response.body)
            item = DoubanItem()
            selector = Selector(response)
            # print selector
            Movies = selector.xpath('//div[@class="info"]')
            # print Movies
            for eachMoive in Movies:
                title = eachMoive.xpath('div[@class="hd"]/a/span/text()').extract()

                # 把两个名称合起来
                fullTitle = ''
                for each in title:
                    fullTitle += each
                movieInfo = eachMoive.xpath('div[@class="bd"]/p/text()').extract()
                star = eachMoive.xpath('div[@class="bd"]/div[@class="star"]/span[@class="rating_num"]/text()').extract()[0]
                quote = eachMoive.xpath('div[@class="bd"]/p[@class="quote"]/span/text()').extract()
                # quote可能为空，因此需要先进行判断
                if quote:
                    quote = quote[0]
                else:
                    quote = ''
                # print(fullTitle)
                # print(movieInfo)
                # print(star)
                # print(quote)
                item['title'] = fullTitle
                item['movieInfo'] = ';'.join(movieInfo)
                item['star'] = star
                item['quote'] = quote
                # # 剧情简介
                synopsis_url = eachMoive.xpath('div[@class="hd"]/a/@href').extract()
                tmp_url = str(synopsis_url[0])
                # item['synopsis_url'] = synopsis_url
                # yield  Request(url=tmp_url,callback=self.get_synopsis,meta={'item':item,'url':tmp_url})
                # synopsis = synopsis_selector.xpath('div[@class="indent"]/span[@property="v:summary"]/text()').extract()
                # item['synopsis'] = synopsis
                yield item
                nextLink = selector.xpath('//span[@class="next"]/link/@href').extract()

                if nextLink:
                    nextLink = nextLink[0]
                    print(nextLink)

                    yield Request(self.url + nextLink,callback=self.parse)



        # def get_synopsis(self,response):
        #     item = response.meta['item']
        #     synopsis = response.xpath('div[@class="indent"]/text()').extract()
        #     item['synopsis'] = synopsis
        #
        #     # selector = Selector(response)
        #     yield item
