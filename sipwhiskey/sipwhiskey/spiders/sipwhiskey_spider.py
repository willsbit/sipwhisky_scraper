import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from datetime import date
import logging

# https://sipwhiskey.com/collections/japanese-whisky
# https://sipwhiskey.com/collections/japanese-whisky/products/yamazaki-12-years-old

class SipSpider(CrawlSpider):
    name = 'sip'
    allowed_domains = ['sipwhiskey.com']
    start_urls = ['http://sipwhiskey.com/']

    logging.basicConfig(filename='scraper.log', level=logging.DEBUG,
                        format='%(asctime)s - %(message)s',
                        datefmt='%d-%b-%y %H:%M:%S')
    rules = (
        Rule(LinkExtractor(allow='collections', deny='products')),
        Rule(LinkExtractor(allow='products'), callback='parse_item')
    )

    def parse_item(self, response):
        yield {
            'brand': response.css('div.vendor a::text').get(),
            'name': response.css('h1.title::text').get(),
            'price': response.css('span.price::text').get()
        }
        logging.info(response)

