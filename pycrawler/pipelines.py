# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from scrapy import Spider
from pycrawler.items import BTCUSDT,ETHUSDT

class PycrawlerPipeline:
    """
    管道需要在settings中启用。
    """

    # @classmethod
    # def from_crawler(cls, crawler):
    #     return cls(
    #         mongo_uri=crawler.settings.get("MONGO_URI"),
    #         mongo_db=crawler.settings.get("MONGO_DATABASE", "items"),
    #     )

    def open_spider(self,spider:Spider):
        """
        当蜘蛛打开时会调用此方法。 

        spiser 被打开的蜘蛛
        """
        pass

    def close_spider(self, spider:Spider):
        """
        当蜘蛛关闭时调用此方法。
        """
        pass


    def process_item(self, item, spider:Spider):
        """
        每个项目管道组件都会调用此方法。 

        每一个管道的返回值都会成为下一个管道的输入值，
        因此如果管道没有返回Item对象就会产生None值。

        向管道中传入Request对象不会再返回调度器
        """
        print("管道",item)
        return item

class testPipeline():
    def process_item(self, item ,spider):
        print("测试管道",item)
        new_item = ETHUSDT()
        new_item['time'] = item['time']
        return new_item