from typing import Any
import psycopg


class Data_Source_Tracker(type):
    """
    自动跟踪所有数据来源。
    通过捕获类定义中的属性字段，自动管理数据库表的创建、写入和维护。
    - 使用装饰器将请求函数加入跟踪列表。
    - 自动管理泛型参数。
    - 自动限制请求速率。
    - 当数据库不正常时发起交互确认配置。
    - 当数据表不存在时自动建立数据表。
    - 当数据存在缺失时自动回调请求函数。

    子类中需要定义：
    - 需要哪些参数标记
    - 数据的字段和类型
    - 如何定义数据表名称


    设计目标：

    一个追踪器可以针对某一类数据最终和管理。
    一类数据可以有多个来源。
    不同的来源可能需要不同的接口。

    因此定义追踪器元类组织控制代码。
    按数据类型定义追踪器实例。
    最后通过定义请求函数编写具体的代码。

    """
    def __new__(cls, clsname, bases, clsdict):
        """
        追踪器构造函数。
        检查类定义，配置管理数据库相关的元数据。

        例如字段的数量和名称。
        

        元类的构造函数在定义类的时候调用。因此可以在这里控制类型的定义。
        
        cls是元类本身。
        super().__new__函数实际上就是type工厂函数。可以用于新建类。

        """
        annotations = clsdict['__annotations__']
        for i in annotations:
            print("追踪字段",i)
        return super().__new__(cls,clsname, bases, clsdict)
        

    def __call__(cls, *args: Any, **kwds: Any) -> Any:
        """
        追踪器实例函数。
        接受标记符号，返回装饰器捕获请求函数。
        
        
        在调用类的构造函数前会先调用元类的call函数。因此可以在这里进行一些定义控制。
        
        cls是定义的子类。
        super().__call__函数将会调用子类的构造函数。
        """
        print("元类call函数",cls,args,kwds)
        return cls

    @property
    def table_name():
        """
        定义使用的数据表的名称。

        需要子类定义。
        """
        pass

    ############### 以下重构

    def capture(self,request_func) -> Any:
        """
        装饰器函数，可以捕获定义的请求函数用于回调。
        """
        def f()->None:
            data = request_func(symbol = self.symbol,
                                exchange = self.exchange,
                                granularity = self.granularity)
            self.write_data(data)
        return None

    def create_table(self):
        sql = f"""CREATE TABLE IF NOT EXISTS public.{self.table_name}
                (
                    minute_stamp bigserial NOT NULL,
                    opening_price bigserial NOT NULL,
                    highest_price bigserial NOT NULL,
                    lowest_price bigserial NOT NULL,
                    closing_price bigserial NOT NULL,
                    basic_volume bigserial NOT NULL,
                    pricing_volume bigserial NOT NULL,
                    PRIMARY KEY (minute_stamp)
                )"""
        if self.exist_table:return
        with psycopg.connect(**self.db) as conn:
            with conn.cursor() as cur:
                cur.execute(sql)

    def write_data(self,data):
        if not self.create_table:
            self.create_table()
        with psycopg.connect(**self.db) as conn:
            with conn.cursor() as cur:
                SQL = f"""INSERT INTO {self.table_name} 
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (minute_stamp) DO NOTHING"""
                cur.executemany(SQL,data)
        

########################### 以下测试

class Trade_Symbol(metaclass=Data_Source_Tracker):
    symbol:str
    exchange:str


if __name__ == "__main__":
    a = Trade_Symbol()
    print(a.__dict__)