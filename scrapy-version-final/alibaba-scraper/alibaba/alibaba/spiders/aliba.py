import scrapy


class AlibaSpider(scrapy.Spider):
    name = 'aliba'
    allowed_domains = ['alibaba.com']
    start_urls = ['http://alibaba.com/']

    def parse(self, response):
        pass
