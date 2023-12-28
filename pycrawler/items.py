# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class PycrawlerItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    pass


def C(cls:type):
    """
    装饰器，通过交易对符号动态生成交易对类。

    对每一个交易对创建一个类型。
    """
    symbols:list[str] = ['BTCUSDT','ETHUSDT']

    # 将交易对类型发送到全局
    for symbol in symbols:
        c = type(symbol,(cls,),{})
        globals()[symbol] = c
    
    # 返回超类，支持未来动态创建子类
    return cls

@C
class mak(scrapy.Item):
    time = scrapy.Field()

