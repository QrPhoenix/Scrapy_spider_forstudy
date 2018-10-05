from scrapy import cmdline
cmdline.execute("scrapy crawl appendix -o items.csv -t csv".split())
