import scrapy


class BitgetHistoryDataSpider(scrapy.Spider):
    name = 'bitget_history_data'
    allowed_domains = ['img.bitgetimg.com']
    start_urls = ['http://img.bitgetimg.com/']

    def parse(self, response):
        pass
