# coding:utf-8
import scrapy
from scrapy import Request
from scrapy.selector import Selector
from appendix.items import *


class AppendixSpider(scrapy.Spider):
    # 爬虫名称
    name = "appendix"
    allowed_domains = ['ches.org.cn']
    # 目标网址，爬虫启动后自动爬取得链接，列表内可以放多个链接
    start_urls = ['http://www.ches.org.cn/ches/slkp/kpdyd/']

    # 爬虫启动时，爬取链接成功后自动回调的函数，默认parse，参数self和response
    # 爬取总目录下的所有模块
    # def parse(self, response):
    #     # 实例化item对象
    #     title_list = response.xpath("/html/body/div[3]/div/div[1]/div[2]/ul/li/a/p/text()").extract()
    #     url_list = response.xpath("/html/body/div[3]/div/div[1]/div[2]/ul/li/a/@href").extract()
    #     print(url_list)
    #     for i, j in zip(title_list, url_list):
    #         # 将爬取的数据写入到item中
    #         kp = KPItem()
    #         kp['module'] = i
    #         url ='http://www.ches.org.cn/ches' + j[5:] + '/'
    #         # 注意这里要用yield，因为item是单个传递的
    #         # yield可以理解为return，将pr返回，但是下一次警戒着上次的循环继续执行, meta={'item': kp}
    #         yield scrapy.Request(url, callback=self.title_parse, meta={'item': kp, 'url': url})
    #         # print(i, ':', url)
    #
    # 爬取单一模块
    def parse(self, response):
    # 实例化item对象
    #     title_list = response.xpath("/html/body/div[3]/div/div[1]/div[2]/ul/li/a/p/text()").extract()
    #     url_list = response.xpath("/html/body/div[3]/div/div[1]/div[2]/ul/li/a/@href").extract()
    #     print(url_list)
    #     for i, j in zip(title_list, url_list):
            # 将爬取的数据写入到item中
            kp = SingleModuleItem()
            # kp['module'] = i
            url ='http://www.ches.org.cn/ches/' + 'kpyd/js/'
            # 注意这里要用yield，因为item是单个传递的
            # yield可以理解为return，将pr返回，但是下一次警戒着上次的循环继续执行, meta={'item': kp}
            yield scrapy.Request(url, callback=self.title_parse, meta={'item': kp, 'url': url})
            # print(i, ':', url)
    def title_parse(self, response):
        # 获取KPItem
        kp = response.meta['item']
        purl = response.meta['url']
        # title_list = response.xpath("/html/body/div/div/div[4]/div[1]/div/div[1]/div/div/div/div/div/h5/a/text()").extract()

        url_list = response.xpath("/html/body/div/div/div[4]/div[1]/div/div[1]/div/div/div/div/div/h5/a/@href").extract()
        # time_list = response.xpath("/html/body/div/div/div[4]/div[1]/div/div[1]/div/div/div/div/div/h6/text()").extract()
        # # pageUrl_list = response.xpath("/html/body/div/div/div[4]/div[1]/div/div[1]/div/div/div[17]/nav/ul/a[4]").extract()
        # /html/body/div/div/div[4]/div[1]/div/div[1]/div/div/div[17]/nav/ul/a[1]
        for url in url_list:
            # kp['title'] = title
            # kp['pubTime'] = time
            url = purl + url[2:]
            # print(title, ':', time, ':', url)
            yield scrapy.Request(url, callback=self.content_parse, meta={'item': kp})
        selector = Selector(response)
        nextLink = selector.xpath("/html/body/div/div/div[4]/div[1]/div/div[1]/div/div/div[17]/nav/ul/a/@href").extract()
        # /html/body/div/div/div[4]/div[1]/div/div[1]/div/div/div[17]/nav/ul/a[4]
        # /html/body/div/div/div[4]/div[1]/div/div[1]/div/div/div[17]/nav/ul/a[6]
        # /html/body/div/div/div[4]/div[1]/div/div[1]/div/div/div[17]/nav/ul
        # /html/body/div/div/div[4]/div[1]/div/div[1]/div/div/div[17]
        # /html/body/div/div/div[4]/div[1]/div/div[1]/div/div/div[17]/nav/ul/a[1]
        # /html/body/div/div/div[4]/div[1]/div/div[1]/div/div/div[17]/nav/ul/a[1]
        if nextLink:
            nextLink = nextLink[0]
            print(nextLink)
            yield scrapy.Request(purl + nextLink, callback=self.title_parse)

    def content_parse(self, response):

        # 获取KPItem
        kp = response.meta['item']
        content = ''
        p_list = response.xpath("//div[@class='juzhongtupian']")
        content = p_list.xpath('string(.)').extract()[0]
        # for p in p_list:
        #     c = p.xpath('string(.)').extract_first()
        #     img = p.xpath('img/@src').extract()
        #     if img != '':
        #         kp['picture'] = 'http://www.ches.org.cn/ches'+img[2:]
        #         content = content + '#' + kp['picture']
        #     elif c != '':
        #         content = content + '#' + c.xpath('string(.)').extract_first()
        kp['content'] = content
        pubTime = response.xpath(
            "//div[@class='col-lg-2 col-md-3 col-sm-3 col-xs-12 fenxiang_time ']/h6/text()").extract()
        kp['pubTime'] = pubTime
        title = response.xpath("//div[@class='col-lg-12 col-md-12 col-sm-12 col-xs-12']/h3/text()").extract()
        kp['title'] = title

        yield kp
        # content = response.xpath("div[class='juzhongtupian']p")
        # kp['content']= content
        # yield kp