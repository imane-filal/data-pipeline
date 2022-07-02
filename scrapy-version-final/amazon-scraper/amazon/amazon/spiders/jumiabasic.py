import scrapy


class JumiabasicSpider(scrapy.Spider):
    name = 'jumiabasic'
    allowed_domains = ['jumia.ma']
    start_urls = ['http://www.jumia.ma/']

    # def stra

    def parse(self, response):
        pass
