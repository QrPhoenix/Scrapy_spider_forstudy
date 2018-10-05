from scrapy import cmdline
cmdline.execute("scrapy crawl appendix -o items.json -t json".split())
