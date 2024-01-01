import scrapy


class BinanceSpider(scrapy.Spider):
    name = 'binance'
    # allowed_domains = ['binance.com']
    start_urls = ['https://binance.com/']

    def start_requests(self):
        url = ""

        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        pass
