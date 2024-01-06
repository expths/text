# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class DcrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass

class myItem(scrapy.Item):
    accountEquity = scrapy.Field()
    unrealizedPL = scrapy.Field()
    crossedRiskRate = scrapy.Field()