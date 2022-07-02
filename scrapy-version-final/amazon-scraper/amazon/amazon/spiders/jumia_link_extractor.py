import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_splash import SplashRequest
from datetime import date


class JumiaSpider(CrawlSpider):
    name = 'jumia_link_extractor'
    allowed_domains = ['jumia.ma']
    start_urls = [
        'https://www.jumia.ma',
    ]

    len_product_details = LinkExtractor(
        restrict_xpaths='//*[@class="flyout"]/a')
    product_details = Rule(len_product_details,
                           callback='parse_items', follow=False)

    rules = (
        product_details,
    )

    def parse_items(self, response):
        yield{
            'url': response.url
        }
