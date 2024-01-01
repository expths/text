import scrapy


class BitgetSpider(scrapy.Spider):
    name = 'bitget'
    allowed_domains = ['bitget.com']
    start_urls = ['http://bitget.com/']

    def parse(self, response):
        pass
