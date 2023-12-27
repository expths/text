from logging import DEBUG
import scrapy


class BitgetHistoryDataSpider(scrapy.Spider):
    name = 'bitget_history_data'
    allowed_domains = ['img.bitgetimg.com']
    start_urls = ['http://img.bitgetimg.com/']

    def start_requests(self):
        # history_data_url = f'https://img.bitgetimg.com/online/kline/{symbol}/{symbol}_SP_1min_{date}.zip'
        # xlsx_name = f"{symbol}_SP_1min_{date}.xlsx"
        url = "https://img.bitgetimg.com/online/kline/BTCUSDT/BTCUSDT_SP_1min_20201111.zip"
        
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        print(response)
