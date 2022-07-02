import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from scrapy_splash import SplashRequest


class AliexpresSpider(scrapy.Spider):
    name = 'aliexpress'
    allowed_domains = ['aliexpress.com']

    start_urls = ['https://pt.aliexpress.com/category/201005148/dresses.html']

    len_product_details = LinkExtractor(restrict_xpaths='//*[@class="JIIxO"]/a')
    product_details = Rule(len_product_details,
                           callback='parse_start_url', follow=False)

    len_products_pagination = LinkExtractor(
        restrict_xpaths='//*[@id="search"]/div[1]/div[1]/div/span[3]/div[2]/div[37]/div/div/span/a[3]')
    products_pagination = Rule(len_products_pagination, follow=True)
    rules = (
        product_details, products_pagination
    )

    def parse_start_url(self,response):
         yield SplashRequest(response.url, self.parse_item, args={'wait': 0.5})
    def start_requests(self):
        url = 'https://www.aliexpress.com/item/1005001775429165.html?spm=a2g0o.tm800071212.4439337570.4.65fa607a8MsD57&pdp_ext_f=%7B%22ship_from%22:%22CN%22,%22sku_id%22:%2212000021948965265%22%7D&&scm=1007.25281.269244.0&scm_id=1007.25281.269244.0&scm-url=1007.25281.269244.0&pvid=8d98f989-e31d-4f95-869c-06e251cfa66e&utparam=%257B%2522process_id%2522%253A%25221%2522%252C%2522x_object_type%2522%253A%2522product%2522%252C%2522pvid%2522%253A%25228d98f989-e31d-4f95-869c-06e251cfa66e%2522%252C%2522belongs%2522%253A%255B%257B%2522floor_id%2522%253A%252227548787%2522%252C%2522id%2522%253A%25221332581%2522%252C%2522type%2522%253A%2522dataset%2522%257D%252C%257B%2522id_list%2522%253A%255B%25221000244088%2522%255D%252C%2522type%2522%253A%2522gbrain%2522%257D%255D%252C%2522pageSize%2522%253A%25226%2522%252C%2522language%2522%253A%2522en%2522%252C%2522scm%2522%253A%25221007.25281.269244.0%2522%252C%2522countryId%2522%253A%2522MA%2522%252C%2522scene%2522%253A%2522TopSelection-Waterfall%2522%252C%2522tpp_buckets%2522%253A%252221669%25230%2523186385%252376_21669%25234190%252319161%2523313_15281%25230%2523269244%25231%2522%252C%2522x_object_id%2522%253A%25221005001775429165%2522%257D'
        yield SplashRequest(url, self.parse,
                            endpoint="execute",
                            args={'lua_source': self.script()})

    def parse(self, response):

        data = {

            "title": response.css('h1::text').get(),
            "price": response.xpath('//*[@class="uniform-banner-box"]/div/span[1]/text()').get(),
            "orders": response.xpath('//*[@class="product-reviewer"]/span[2]/text()').get(),
            "quantity": response.xpath('//*[@class="product-quantity-tip"]/span/span/text()').get(),
            "sold_by": {
                "name": response.xpath('//*[@id="product-detail"]/div[1]/div[1]/div[1]/div/a/text()').get(),
                'store_url': response.xpath('//*[@id="product-detail"]/div[1]/div[1]/div[1]/div/a/@href').get(),
                'followers': response.xpath('//*[@id="product-detail"]/div[1]/div[1]/div[2]/div[2]/div[2]/text()[1]').get(),
                'feed_back': response.xpath('//*[@id="product-detail"]/div[1]/div[1]/div[2]/div[2]/div[1]/text()[1]').get()
            },
            # "Customer_reviews": {
            #     "customer_rate": response.xpath('//*[@class="rate-score"]/span/bb/text()').get(),
            #     "total_rate": response.xpath('//*[@id="transction-feedback"]/div[1]/text()').get(),
            #     "global_rate": {
            #         "1_star": response.xpath('//*[@id="transction-feedback"]/div[2]/ul/li[5]/span[3]/text()').get(),
            #         "2_star": response.xpath('//*[@id="transction-feedback"]/div[2]/ul/li[4]/span[3]/text()').get(),
            #         "3_star": response.xpath('//*[@id="transction-feedback"]/div[2]/ul/li[3]/span[3]/text()').get(),
            #         "4_star": response.xpath('//*[@id="transction-feedback"]/div[2]/ul/li[2]/span[3]/text()').get(),
            #         "5_star": response.xpath('//*[@id="transction-feedback"]/div[2]/ul/li[1]/span[3]/text()').get(),
            #     },
            #     'product_reviews': []


            # },
            "url": response.url

        }
        # for reveiw in response.xpath('//*[@id="transction-feedback"]/div[5]/div'):
        #     data["Customer_reviews"]["product_reviews"].append(
        #         {
        #             "is_helpful": {
        #                 'yes': reveiw.xpath('div[2]/div[3]/dl/div/span[2]/span[2]/text()').get(),
        #                 'no': reveiw.xpath('div[2]/div[3]/dl/div/span[3]/span[2]/text()').get()
        #             },
        #             "date": reveiw.xpath('div[2]/div[3]/dl/dt/span[2]/text()').get(),
        #             "review": reveiw.xpath('div[2]/div[3]/dl/dt/span[1]/text()').get(),
        #         }
        #     )

        

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
