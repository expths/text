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
    - 需要哪些签名
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
    def __new__(cls, clsname, bases, clsdict)->type:
        """
        追踪器构造函数。
        检查类定义，配置管理数据库相关的元数据。

        扫描所有字段，其中作为参数的字段用于构造数据库和请求参数。
        检查数据库名称函数是否用到了所有标记。
        检查数据类型构造数据库命令。

        注入请求函数的捕获函数。在其中检查请求函数的参数签名是否正确。
        如果有可选参数验证其是否可以自动推导。


        元类的构造函数在定义类的时候调用。因此可以在这里控制类型的定义。
        
        cls是元类本身。
        super().__new__函数实际上就是type工厂函数。可以用于新建类。

        """
        annotations = clsdict['__annotations__']
        tags = []
        for i in annotations:
            tags.append(i)
            if i == 'a':print(annotations[i].__args__)
        clsdict['create'] = cls.create_table
        clsdict['write'] = cls.write_data
        clsdict['__call__'] = cls.capture

        return super().__new__(cls,clsname, bases, clsdict)
        

    def __call__(cls, *args: Any, **kwds: Any) -> object:
        """
        追踪器实例函数。
        接受标记符号，返回装饰器捕获请求函数。
        
        检查输入类型是否正确。
        配置自动程序持续发起请求。

        使用享元模式，如果输入参数相同则返回同一个对象。

        
        在调用类的构造函数前会先调用元类的call函数。因此可以在这里进行一些定义控制。
        
        cls是定义的子类。
        super().__call__函数将会调用子类的构造函数。
        """

        print("构造函数参数",args,kwds)
        print("需要参数",cls.__annotations__)
        
        return super().__call__()# 返回一个call函数为装饰器的对象

    @property
    def table_name()->str: # 在构造函数中添加验证合法性的功能。
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

        # 将f函数注册到循环中。
        
        return "捕获函数"
    
    @property
    def exist_table()->bool:
        """
        检查是否存在数据库。

        检查数据库实际内容是否和类定义一致。
        """
        return True

    def create_table(self)->None:
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

    def write_data(self,data)->None:
        if not self.create_table:
            self.create_table()
        with psycopg.connect(**self.db) as conn:
            with conn.cursor() as cur:
                SQL = f"""INSERT INTO {self.table_name} 
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT (minute_stamp) DO NOTHING"""
                cur.executemany(SQL,data)


    def c(self):
        """
        元编程函数。通过识别数据表名称定义函数自动逆向分析得到逆函数。
        """
        pass
        

########################### 以下测试

class Trade_Symbol(metaclass=Data_Source_Tracker):
    symbol:str
    exchange:str
    a:tuple[int,int,int,int,int,int,int]


if __name__ == "__main__":
    a = Trade_Symbol()
    print(a(lambda x:x*x))
