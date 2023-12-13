import configparser
from binance_api.spot import Spot
import psycopg


try:
    config = configparser.ConfigParser()
    config.read('config.ini')
    client = Spot(config.get('binance','api_key'),
              config.get('binance','api_secret'),
              show_limit_usage=True)
except FileNotFoundError:
    print("[ERR]配置文件缺失")
    config['binance'] = {'api_key':'','api_secret':''}
    with open('config.ini',mode='w')as config_file:
        config.write(config_file)
except configparser.NoSectionError:
    config['binance'] = {'api_key':'','api_secret':''}
    with open('config.ini',mode='w')as config_file:
        config.write(config_file)


def c(func):
    """
    装饰器函数。限制请求速度。

    通过接口配置show_limit_usage后会在响应体中得到一个新的字段。
    'limit_usage': {'x-mbx-used-weight': '31', 'x-mbx-used-weight-1m': '31'}
    """
    def f(*args,**kargs):
        if client.time()['linit_usage'] == "":
            raise
        return func(*args,**kargs)
    return f


def db(database:str):
    """
    装饰器函数。自动管理数据库。

    选择数据库用于装饰函数。
    自动收集函数产生的返回值，并将其写入数据库。
    """

    sql = """
    S
    """
    def fc(func):# 装饰器
        def f(*args,**kargs):
            data = func(*args,**kargs)
            with psycopg.connect() as conn:# 登录程序未完成
                with conn.cursor() as cur:
                    cur.execute(query=sql)
                    return data
        return f
    return fc


@db("")
def klines():
    """
    读取k线数据。
    """
    pass


if __name__ == "__main__":
    print(client.time())
    print(client.klines("BNBUSDT", "1m", limit=2))
