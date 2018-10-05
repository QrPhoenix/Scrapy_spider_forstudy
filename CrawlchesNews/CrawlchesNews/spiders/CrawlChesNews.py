# coding:utf-8
import scrapy

from scrapy import Request
from scrapy.selector import Selector
from CrawlchesNews.items import *


class CrawlChesNews(scrapy.Spider):
# 爬虫名称
    name = "appendix"
    allowed_domains = ['ches.org.cn']
    # 目标网址，爬虫启动后自动爬取得链接，列表内可以放多个链接
    start_urls = ['http://www.ches.org.cn/ches/hyxw_22318/']
    # 一共有40个页面
    Index = 40

    def parse(self, response):
        purl = self.start_urls[0]
        # 获得第一个页面下的所有url地址
        url_list = response.xpath("/html/body/div/div[1]/div[4]/div/div[2]/div/div/div/div/div[1]/h5/a/@href").extract()
        for url in url_list:
            # 实例化item对象//注意这里是要生成多个item对象，不要把item对象放到for循环外面
            kp = CrawlchesnewsItem()
            # 获取下一个页面的根地址，为获得图片的url做准备
            img_url = purl + url.split('/')[1]
            url = purl + url[2:]
            # 多层处理（这里是两层），在content_parse中处理目标文章页面信息的处理
            yield scrapy.Request(url, callback=self.content_parse, meta={'item': kp,'img_url':img_url})
        for index in range(1,self.Index):
            purl = self.start_urls[0]+'index_'+str(index)+'.html'
            yield scrapy.Request(purl,callback=self.parse)
    def content_parse(self, response):

        # 获取KPItem
        kp = response.meta['item']
        img_url = response.meta['img_url']
        content = ''
        p_list = response.xpath("//div[@class='juzhongtupian']//p")
        # 匹配多种xpath，以爬取正确的文章内容
        if p_list == []:
            try:
                p_list = response.xpath("//div[@class='juzhongtupian']/div/p")
            except ValueError:
                print("Error:xpath cannot match the web page!")
        if p_list == []:
            try:
                p_list = response.xpath("//div[@class='juzhongtupian']/div/")
            except ValueError:
                print("Error:xpath cannot match the web page!")
        if p_list == []:
            try:
                p_list = response.xpath("//div[@class='juzhongtupian']/div/div/")
            except ValueError:
                print("Error:xpath cannot match the web page!")
        if p_list == []:
            try:
                p_list = response.xpath("//div[@class='juzhongtupian']")
            except ValueError:
                print("Error:xpath cannot match the web page!")
        # 处理含有图片的文章页面
        for p in p_list:
            c = p.xpath('string(.)').extract_first()
            img = p.xpath('img/@src').extract()
            img
            if img != []:
                if 'http' in img[0]:
                    img_url = ''
                picture_url = img_url + img[0][1:]
                content = content + '#' + picture_url
            elif c != '':
                content =  c+ '/n' +content

        # if content == '':调试用
        #     content
        #     content

        # 将爬取的数据写入到item中
        kp['content'] = content
        pubTime = response.xpath(
            "//div[@class='col-lg-2 col-md-3 col-sm-3 col-xs-12 fenxiang_time ']/h6/text()").extract()
        kp['pubTime'] = pubTime[0]
        title = response.xpath("//div[@class='col-lg-12 col-md-12 col-sm-12 col-xs-12']/h3/text()").extract()
        kp['title'] = title[0]

        yield kp