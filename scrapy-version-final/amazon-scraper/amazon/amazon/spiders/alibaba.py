import scrapy


class AlibabaSpider(scrapy.Spider):
    name = 'alibaba'
    allowed_domains = ['alibaba.com']
    start_urls = ['https://www.alibaba.com/']

    def parse(self, response):
        pass
