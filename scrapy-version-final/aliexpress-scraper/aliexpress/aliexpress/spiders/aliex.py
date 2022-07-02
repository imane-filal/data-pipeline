import scrapy


class AliexSpider(scrapy.Spider):
    name = 'aliex'
    allowed_domains = ['aliexpress.com']
    start_urls = ['http://aliexpress.com/']

    def parse(self, response):
        pass
