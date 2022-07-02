
import scrapy
from scrapy_splash import SplashRequest


class AmazonspiderSpider(scrapy.Spider):
    name = 'amazonSpider'
    allowed_domains = ['amazon.com']
    start_urls = ['']

    def __init__(self):
        with open('/home/redone/scrpyfinal/amazon/amazon/data/url.txt', 'r') as f:
            self.start_urls = f.readlines()

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

    def start_requests(self):
        for url in self.start_urls:
            yield SplashRequest(url, self.parse,
                                endpoint="execute",
                                args={'lua_source': self.script()})

    def parse(self, response):
        data = {

            "categorie_0": response.xpath('//*[@id="wayfinding-breadcrumbs_feature_div"]/ul/li[1]/span/a/text()').get(),
            "categorie_1": response.xpath('//*[@id="wayfinding-breadcrumbs_feature_div"]/ul/li[3]/span/a/text()').get(),
            "title": response.css('h1 > span ::text').get(),
            "price": response.xpath('//div[@id="corePrice_feature_div"]/div/span/span[1]//text()').get(),
            "shiping_fees": response.xpath('//*[@id="exports_desktop_qualifiedBuybox_tlc_feature_div"]/span[1]/text()').get(),
            "delevery_period": response.xpath('//*[@id="mir-layout-DELIVERY_BLOCK-slot-PRIMARY_DELIVERY_MESSAGE_LARGE"]/span/span/text()').get(),
            "delevery_destination": response.xpath('//*[@id="contextualIngressPtLabel_deliveryShortLine"]/span[2]/text()').get(),
            "in_stock": response.xpath('//*[@id="availability"]/span/text()').get(),
            "quantity": "not_exist",
            "ship_from": response.xpath('//*[@id="tabular-buybox"]/div[1]/div[2]/div/span/text()').get(),
            "sold_by": {
                "name": response.xpath('//*[@id="sellerProfileTriggerId"]/text()').get(),
                'store_url': response.xpath('//*[@id="sellerProfileTriggerId"]/@href').get(),
                'packaging': response.xpath('//*[@id="tabular-buybox"]/div[1]/div[6]/div/span/text()').get()
            },
            "description": response.xpath('//*[@id="productDescription"]/p/text()').getall(),
            "is_returned": response.xpath('//*[@id="productSupportAndReturnPolicy-return-policy-popover-celWidget"]/div/div[1]/text()').get(),
            "details": [],
            "extra_info": [],
            "about_this_item": [],
            "note": response.xpath('//*[@id="universal-product-alert"]/div/span[2]/text()').get(),
            "Q_AW": [],
            "Customer_reviews": {
                "customer_rate": response.xpath('//*[@id="reviewsMedley"]/div/div[1]/div[2]/div[1]/div/div[2]/div/span/span/text()').get(),
                "total_rate": response.xpath('//*[@id="reviewsMedley"]/div/div[1]/div[2]/div[2]/span/text()').get(),
                "global_rate": {
                    "1_star": response.xpath('//*[@id="histogramTable"]/tbody/tr[5]/td[3]/span[2]/a/text()').get(),
                    "2_star": response.xpath('//*[@id="histogramTable"]/tbody/tr[4]/td[3]/span[2]/a/text()').get(),
                    "3_star": response.xpath('//*[@id="histogramTable"]/tbody/tr[3]/td[3]/span[2]/a/text()').get(),
                    "4_star": response.xpath('//*[@id="histogramTable"]/tbody/tr[2]/td[3]/span[2]/a/text()').get(),
                    "5_star": response.xpath('//*[@id="histogramTable"]/tbody/tr[1]/td[3]/span[2]/a/text()').get(),
                },
                "product_reviews": []

            },
            "url": response.url

        }
        for reveiw in response.xpath('//*[@id="cm-cr-dp-review-list"]/div'):
            data["Customer_reviews"]["product_reviews"].append(
                {
                    "rate": reveiw.xpath('div/div/div[2]/a/i/span/text()').get(),
                    "feature": reveiw.xpath('div/div/div[2]/a[2]/span/text()').get(),
                    "date_from": reveiw.xpath('div/div/span/text()').get(),
                    "verified": reveiw.xpath('div/div/div[3]/span[2]/text()').get(),
                    "review": reveiw.xpath('div/div/div[4]/span/div/div[1]/span/text()').get(),
                    'viewers_reaction': reveiw.xpath('div/div/div[5]/span[1]/div[1]/span/text()').get()
                }
            )

        for cr_rf in response.xpath('//*[@id="cr-summarization-attributes-list"]/div'):
            data["Customer_reviews"]["rate_by_feature"].append(
                {
                    "key": cr_rf.xpath('div/div/div/div/span/text()').get(),
                    "value": cr_rf.xpath('div/div/div[2]/span[2]/text()').get()
                }
            )

        for Q_AW in response.xpath('//*[@id="ask-btf-container"]/div/div/div[2]/span/div/div'):
            data["Q_AW"].append(
                {
                    "Question": Q_AW.xpath('div/div[2]/div/div/div[2]/a/span/text()').get(),
                    "Answer":  Q_AW.xpath('div/div[2]/div[2]/div/div[2]/span/span[2]/text()').get(),
                    "vote": Q_AW.xpath('div/div/ul/li[2]/span[1]/text()').get(),
                    "date_answer": Q_AW.xpath('div/div[2]/div[2]/div/div[2]/span[3]/text()').get()
                }
            )

        for extra_info in response.xpath('//*[@id="productDetails_detailBullets_sections1"]/tbody/tr'):
            data["extra_info"].append(
                {
                    "key": extra_info.css('th::text').get(),
                    "value": extra_info.css('td::text').get()
                }
            )
        for index, about_this_item in enumerate(response.xpath('//*[@id="feature-bullets"]/ul/li')):
            data["about_this_item"].append(
                {
                    index+1: about_this_item.xpath('span/text()').get(),

                }
            )
        for extra in response.xpath('//*[@id="productOverview_feature_div"]/div/table/tbody/tr'):
            data['details'].append(
                {
                    "key": extra.xpath('td[1]/span/text()').get(),
                    "value": extra.xpath('td[2]/span/text()').get()
                }
            )

        yield data
