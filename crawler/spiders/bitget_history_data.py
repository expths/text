from logging import DEBUG
import scrapy
from crawler.items import myItem

class BitgetHistoryDataSpider(scrapy.Spider):
    name = 'bitget_history_data'
    allowed_domains = ['img.bitgetimg.com']
    start_urls = ['https://img.bitgetimg.com/']

    def start_requests(self):
        # history_data_url = f'https://img.bitgetimg.com/online/kline/{symbol}/{symbol}_SP_1min_{date}.zip'
        # xlsx_name = f"{symbol}_SP_1min_{date}.xlsx"
        url = "https://img.bitgetimg.com/online/kline/BTCUSDT/BTCUSDT_SP_1min_20201111.zip"
        
        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        item = myItem()
        item['accountEquity'] = 4
        item['unrealizedPL'] = 5
        item['crossedRiskRate'] = 6
        return item
