import json
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from datetime import date


class JumiaSpider(CrawlSpider):
    name = 'jumia'
    allowed_domains = ['jumia.ma']
    start_urls = [
    ]

    len_product_details = LinkExtractor(
        restrict_xpaths='//*[@id="jm"]/main/div[2]/div[3]/section/div[1]/article/a')
    product_details = Rule(len_product_details,
                           callback='parse_items', follow=False)

    len_products_pagination = LinkExtractor(
        restrict_xpaths='//*[@id="jm"]/main/div[2]/div[3]/section/div[2]/a[6]')
    products_pagination = Rule(len_products_pagination, follow=True)
    rules = (
        product_details, products_pagination
    )

    def __init__(self,*a, **kw):
        super().__init__(*a, **kw)
        with open('/home/redone/scrpyfinal/amazon/amazon/jumia-url.json','r') as f:
            urls = json.load(f)
            for url in urls:
                self.start_urls.append(url['url'])

    # def parsstar_1t_url(self, response):
    #     yield SplshRequest(response.url, self.parse_items,
    #                         endpoint="execute",
    #                         args={'lua_source': self.script()})
    # def start_requests(self):
    #     url = 'https://www.jumia.ma/oppo-a3s-4gb-ram64gb-4g-lte-dual-sim-6.2-inch-display-face-unlock-rose-49543678.html'
    #     yield SplashRequest(url, self.parse,
    #                         endpoint="execute",
    #                        args={'lua_source': self.script()})

    def parse_items(self, response):
        # for
        data = {
            "categorie":response.xpath('//*[@id="jm"]/main/div[1]/div[1]/a[2]/text()').get(),
            'title': response.xpath('//*[@id="jm"]/main/div[1]/section/div/div[2]/div[1]/div/h1/text()').get(),
            'price': response.xpath('//*[@id="jm"]/main/div[1]/section/div/div[2]/div[2]/div[3]/div/span/text()').get(),
            'promo': response.xpath('//*[@id="jm"]/main/div[1]/section/div/div[2]/div[2]/div[3]/div/div/span[1]/text()').get(),
            'percentage': response.xpath('//*[@id="jm"]/main/div[1]/section/div/div[2]/div[2]/div[3]/div/div/span[2]/text()').get(),
            'shipping_fees': response.xpath('//*[@id="jm"]/main/div[1]/section/div/div[2]/div[2]/div[4]/em/text()').get(),
            "Customer_reviews": {
                "customer_rate": response.xpath('//*[@id="jm"]/main/div[2]/div[2]/section[3]/div[2]/div[1]/div/div[1]/span/text()').get(),
                "total_rate": response.xpath('//*[@id="jm"]/main/div[2]/div[2]/section[3]/div[2]/div[1]/div/p/text()').get(),
                "global_rate": {
                    "star_1": response.xpath('//*[@id="jm"]/main/div[2]/div[2]/section[3]/div[2]/div[1]/ul/li[5]/p/text()').get(),
                    "star_2": response.xpath('//*[@id="jm"]/main/div[2]/div[2]/section[3]/div[2]/div[1]/ul/li[4]/p/text()').get(),
                    "star_3": response.xpath('//*[@id="jm"]/main/div[2]/div[2]/section[3]/div[2]/div[1]/ul/li[3]/p/text()').get(),
                    "star_4": response.xpath('//*[@id="jm"]/main/div[2]/div[2]/section[3]/div[2]/div[1]/ul/li[2]/p/text()').get(),
                    "star_5": response.xpath('//*[@id="jm"]/main/div[2]/div[2]/section[3]/div[2]/div[1]/ul/li[1]/p/text()').get(),
                },
                "product_reviews": []

            },
            'date': date.today(),
            'from': 'jumia',
            "url": response.url
        }
        for reveiw in response.xpath('//*[@id="jm"]/main/div[2]/div[2]/section[2]/div[2]/div[2]/article'):
            data["Customer_reviews"]["product_reviews"].append(
                {
                    "rate": reveiw.xpath('div[1]/text()').get(),
                    "feature": reveiw.xpath('h3/text()').get(),
                    "date_from": reveiw.xpath('div[2]/div[1]/span[1]/text()').get(),
                    "verified": reveiw.xpath('div[2]/div[2]/text()').get(),
                    "review": reveiw.xpath('p/text()').get(),
                }
            )
        yield data

    def script(self):
        _script = """
                    function main(splash, args)
                        assert(splash:go(args.url))
                        splash:wait(0.5)
                        splash:set_viewport_full()
                        splash:wait(0.5)
                        
                        return {
                            html = splash:html(),
                            png = splash:png(),
                            har = splash:har(),
                        }
                    end
            """
        return _script
