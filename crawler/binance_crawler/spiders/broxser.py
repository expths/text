import scrapy


class BroxserSpider(scrapy.Spider):
    name = 'broxser'
    start_urls = ['https://broxser/']

    def start_requests(self):
        yield scrapy.Request(url="")

    def parse(self, response):
        pass
