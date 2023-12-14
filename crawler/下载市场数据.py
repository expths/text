from typing import Any
import requests
import psycopg
import zipfile
from io import BytesIO
import openpyxl
from datetime import datetime,timedelta
import time
import json
import hmac
import base64
import sys
from itertools import chain
import configparser
import bitget_api.v1.mix.order_api as maxOrderApi
import bitget_api.bitget_api as baseApi
from bitget_api.exceptions import BitgetAPIException
from abc import ABC, abstractmethod
import threading

try:
    config = configparser.ConfigParser()
    config.read('config.ini')
except FileNotFoundError:
    print("[ERR]配置文件缺失")
    config['bitget'] = {'APIKey':'','SecretKey':'','passphrase':''}
    with open('config.ini',mode='w')as config_file:
        config.write(config_file)


try:
    apiKey = config.get('bitget','APIKey')
    secretKey = config.get('bitget','SecretKey')
    passphrase = config.get('bitget','passphrase')
except configparser.NoSectionError:
    print("[ERR]缺少API配置")
    config['bitget'] = {'APIKey':'','SecretKey':'','passphrase':''}
    with open('config.ini',mode='w')as config_file:
        config.write(config_file)

try:
    db = {
        "dbname": config.get('postgreSQL','dbname'),
        "user": config.get('postgreSQL','user'),
        "password": config.get('postgreSQL','password')
    }
except configparser.NoSectionError:
    print("[ERR]缺少postgreSQL数据库配置")
    config['postgreSQL'] = {'dbname':'','user':'','password':''}
    with open('config.ini',mode='w')as config_file:
        config.write(config_file)

baseApi = baseApi.BitgetApi(apiKey, secretKey, passphrase)
API_url = "https://api.bitget.com/api/v2/spot/market/candles"
table_name = lambda symbol:f"{symbol}_market_data"
bitget_market_data_earliest_date = '20180725'

def format_market_data(func):
    """
    格式化网络返回的数据。

    将所有数据转换为int值。
    时间戳改为了分钟数。
    价格和成交额均乘100。
    """
    def f(*args,**kargs):
        try:
            data = func(*args,**kargs)
            datetime.fromtimestamp(int(data[0][0]))
            divisor = 60
        except OSError:
            divisor = 60000
        except TypeError:
            divisor = 60
        return map(lambda d:[int(d[0])//divisor]+[int(float(i)*100) for i in d[1:7]],data)
    return f

def frequency_limit(frequency,number_of_seconds=1):
    """
    给定频率限制函数运行速度。
    """
    def decorator(func):
        last_time = datetime.now()
        number_of_time = 0
        def f(*args,**kargs):
            nonlocal last_time
            nonlocal number_of_time
            now_time = datetime.now()
            if now_time - last_time <= timedelta(seconds=number_of_seconds) and number_of_time >= frequency:
                number_of_time = 0
                time.sleep(1)
            else:
                number_of_time += 1
            last_time = now_time
            return func(*args,**kargs)
        return f
    return decorator

def sign(message, secret_key):
  """
  使用密钥签名信息。

  签名转换为base64编码。
  """
  print(message)
  mac = hmac.new(bytes(secret_key, encoding='utf8'), bytes(message, encoding='utf-8'), digestmod='sha256')
  d = mac.digest()
  return base64.b64encode(d).decode('utf-8')

def parse_params_to_str(params):
  """
  将GET参数转换为字符串。
  """
  url = '?'
  for key, value in params.items():
    url = url + str(key) + '=' + str(value) + '&'
  return url


def pre_hash(timestamp:str, method:str, request_path:str, queryString:str='', body:str=''):
  """
  合成待签名信息。

  签名各字段说明:

    timestamp：与 ACCESS-TIMESTAMP 请求头相同。
    method：请求方法(POST/GET)，字母全部大写。
    requestPath：请求接口路径。
    queryString：请求URL中(?后的请求参数)的查询字符串。
    body：请求主体对应的字符串，如果请求没有主体(通常为GET请求)则body可省略。
  """
  if not isinstance(queryString,str):
    queryString = parse_params_to_str(queryString)
  if not isinstance(body,str):
    json.dumps(body)
  return str(timestamp) + str.upper(method) + request_path + queryString + body


def construct_request_header(access:map,method:str,requestPath:str,queryString:str='',body:str=''):
    """
    配置签名并构造请求头。

    所有REST请求的header都必须包含以下key：

        ACCESS-KEY：API KEY作为一个字符串。
        ACCESS-SIGN：使用base64编码签名 (参考 HMAC 与 RSA)。
        ACCESS-TIMESTAMP：您请求的时间戳。
        ACCESS-PASSPHRASE：您在创建API KEY时设置的口令。
        Content-Type：统一设置为application/json。
        locale: 支持多语言, 如：中文(zh-CN),英语(en-US)
    """
    timestamp = int(time.time() * 1000)
    message = pre_hash(timestamp=timestamp,method=method,request_path=requestPath,queryString=queryString,body=body)
    header = {'ACCESS-KEY':access['APIKey'],
          'ACCESS-SIGN':sign(message, access['SecretKey']),
          'ACCSEE-TIMESTAZMP':str(timestamp),
          'ACCESS-PASSPHRASE':access['passphrase'],
          'Content-Type':'application/json',
          'locale':'zh-CN'}
    return header

@frequency_limit(20,1)
@format_market_data
def get_bitget_candles(symbol):
    """
    通过bitget_API获取市场行情数据，并返回迭代器。

    加入可选的时间参数将通过bitget_API获取历史行情数据。

    为了优化数据库查询操作，将所有数据转换为int值。
    特别的，时间戳改为了分钟数，价格和成交额均乘100。
    """
    payload = {'symbol':symbol,'granularity':'1min'}

    # 发起请求
    response = requests.get(API_url,params=payload)
    if response.status_code != 200:
        raise RuntimeError("请求失败！")
    print("[OK]请求成功")

    return response.json()['data']


@format_market_data
def request_bitget_history_data(symbol,date):
    """
    请求bitget历史行情数据。

    在bitget的储存库中数据被包含在zip压缩下的xlsx文件内。
    因此利用二进制IO处理压缩包和文件
    """
    if isinstance(date,datetime):
        date = date.strftime('%Y%m%d')
    if isinstance(date,str):
        date = int(date)
    if not isinstance(date,int):
        raise RuntimeError("日期异常")

    history_data_url = f'https://img.bitgetimg.com/online/kline/{symbol}/{symbol}_SP_1min_{date}.zip'
    xlsx_name = f"{symbol}_SP_1min_{date}.xlsx"

    # 发起请求
    print(f"请求{date}的{symbol}行情")
    response = requests.get(history_data_url)
    if response.status_code != 200:
        print(response.status_code)
        raise RuntimeWarning("请求失败")
    
    # 提取文件并解压zip提取xlsx工作表
    zip_file = BytesIO(response.content)
    with zipfile.ZipFile(zip_file,"r")as z:
        xlsx_file = BytesIO(z.read(xlsx_name))
    workbook = openpyxl.load_workbook(xlsx_file)

    # 清除表头并返回迭代器
    data = iter(workbook.active.iter_rows(values_only=True))
    next(data)
    return data

def minute_stamp_to_date(minute_stamp):
    """
    将分钟数转换为日期
    """
    if isinstance(minute_stamp,str):minute_stamp = int(minute_stamp)
    return datetime.fromtimestamp(minute_stamp*60).strftime('%Y%m%d')

def date_iterator(start_data:datetime,end_data:datetime=datetime.now(),step_data:timedelta=timedelta(days=1)):
    """
    生成器迭代两个日期之间的所有日期。
    """
    if isinstance(start_data,str):
        start_data = datetime.strptime(start_data,'%Y%m%d')
    if isinstance(end_data,str):
        end_data = datetime.strptime(end_data,'%Y%m%d')
    if isinstance(step_data,int):
        step_data = timedelta(days=step_data)
    
    while start_data <= end_data:
        yield start_data
        start_data += step_data

def find_date_with_missing_data(symbol):
    """
    检查数据库中所有缺失数据的时刻并返回其日期。
    """
    with psycopg.connect(**db) as conn:
        with conn.cursor() as cur:
            cur.execute(f"SELECT minute_stamp FROM {table_name(symbol)} ORDER BY minute_stamp DESC")
            market_time_list = cur.fetchall()
    missing_time_range_list = ((i[0],j[0]) for i,j in zip(market_time_list,market_time_list[1:])if i[0]-j[0]!=1)
    date_with_missing_data = chain(*(date_iterator(minute_stamp_to_date(j),minute_stamp_to_date(i)) for i,j in missing_time_range_list))
    return date_with_missing_data

def create_market_database(symbol):
    """
    创建行情数据库。
    """
    with psycopg.connect(**db) as conn:
        with conn.cursor() as cur:
            cur.execute(f"""CREATE TABLE IF NOT EXISTS public.{table_name(symbol)}
                        (
                            minute_stamp bigserial NOT NULL,
                            opening_price bigserial NOT NULL,
                            highest_price bigserial NOT NULL,
                            lowest_price bigserial NOT NULL,
                            closing_price bigserial NOT NULL,
                            basic_volume bigserial NOT NULL,
                            pricing_volume bigserial NOT NULL,
                            PRIMARY KEY (minute_stamp)
                        )""")

def write_market_data_to_database(symbol,data):
    """
    将数据写入数据库。
    """
    with psycopg.connect(**db) as conn:
        with conn.cursor() as cur:
            SQL = f"""INSERT INTO {table_name(symbol)} 
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            ON CONFLICT (minute_stamp) DO NOTHING"""
            cur.executemany(SQL,data)

def auto_worker(status_flag):
    """
    守护进程
    """
    while not status_flag.is_set():
        time.sleep(1)
        print("守护进程")
    pass

def signal_handler(sig, frame):
    """
    捕获操作系统信号
    """
    print("\n捕获到信号(SIGINT)，程序将退出。")
    # 可以在这里执行一些清理操作或记录日志
    sys.exit(0)

def function_fitting():
    """
    许多算法内部无法介绍其工作原理，是一个黑箱。
    
    通过统计大量历史记录，可以拟合它的行动。
    """


def coinmarketcap():
    """
    https://pro.coinmarketcap.com/features/
    """

def coingecko():
    """
    https://www.coingecko.com/api/documentation
    """

def dydx():
    """
    https://dydxprotocol.github.io/v3-teacher/#rate-limit-api
    """

def kine():
    """
    https://kine-api-docs.github.io/zh-cn/#fce908f544
    """





class Data_Table(ABC):# 待实现
    """
    机器人可能需要爬取来自各种API的数据。
    但无论数据来自于何处，都离不开数据库操作。
    因此可以将数据库相关程序抽象出来构造数据表类。

    但这个类不仅仅控制读写数据库。同时也是发起请求的控制器。
    当数据库中出现异常或缺失的数据时，需要隐式地发起请求填补缺漏。

    ---

    继承数据表类产生各种具体的数据表类，在它们内部实现具体的数据库操作。
    在同一类型的不同表使用符号加以区分。
    
    例如：

    所有的k线数据都有7个字段。分别是时间、四个价格和两个成交额。
    这些数据的种类不会因为交易所或交易对的不同而改变。
    因此归纳创建一个k线表类。
    使用交易所、交易对、时间度量三个符号区分不同的实例。

    ---

    在使用上，所有控制器都通过装饰器来接收数据。
    这样做的好处是不需要在显示得编写各种控制函数。

    例如：

    @控制器实例(参数)
    def 请求函数(请求参数):
        请求操作代码
        return 数据

    在控制器内部不仅需要实现数据库的读写。
    同时还要自动在需要的时候调用函数发起操作。
    装饰器返回的函数用于手动显式执行函数，它应该返回操作状况。
    """
    db = db

    @abstractmethod
    def __init__(self) -> None:
        """
        定义数据库。

        其中应该定义包含哪些标志。
        """

    @abstractmethod
    def __call__(self,request_func) -> Any:
        """
        装饰器函数,用于包装请求函数以自动管理数据库。

        自动检查数据表是否存在。如果不存在则调用创建函数。
        将数据标志符号输入请求函数，并自动捕获数据并写入数据库。
        """

    @property
    @abstractmethod
    def table_name(self)->str:
        """
        定义表的名称如何生成。

        它会被用于数据库的创建和读取，应该避免冲突。
        """

    @abstractmethod
    def create_table(self):
        """
        需要定义如何创建表。

        调用一个新表时自动创建。
        """

    @abstractmethod
    def write_data(self,data):
        """
        需要定义如何写入数据库。
        """

    @property
    def exist_table(self):
        """
        检查数据库是否存在。
        """
        sql = f"SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = '{self.table_name}');"
        with psycopg.connect(**self.db) as conn:
            with conn.cursor() as cur:
                cur.execute(sql)
                return bool(cur.fetchall()[0][0])




class Candles_Data_Table(Data_Table):
    """
    行情数据库。

    由交易对、交易所、时间度量三个标志
    
    包含时间、四个价格和两个成交额七个字段。
    """

    @property
    def symbols(self):
        """
        所有交易对
        """
        return ['BTCUSDT']

    @property
    def symbol(self):
        return self._symbol

    @symbol.setter
    def symbol(self,s):
        if s not in self.symbols:
            raise TypeError
        self._symbol = s

    def __init__(self,symbol:str|[str],exchange:str,granularity:str) -> None:
        self.symbol = symbol
        self.exchange = exchange
        self.granularity = granularity
        if not self.exist_table:
            create_market_database(symbol)

    def __call__(self,request_func) -> Any:
        def f()->None:
            data = request_func(symbol = self.symbol,
                                exchange = self.exchange,
                                granularity = self.granularity)
            self.write_data(data)
        self.thread = threading.Thread(target=f)
        self.thread.start()
        return None

    @property
    def table_name(self)->str:
        return f"[{self.symbol}]"

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




@Candles_Data_Table('BTCUSDT','bitget','1m')
def get_candles(symbol,granularity):
    """
    下载行情数据。
    """
    params = {'symbol':symbol,'granularity':granularity}
    a = baseApi.get("/api/v2/spot/market/candles",params)
    return a



if __name__ == "__main__":
    # try:
    #     write_market_data_to_database('BTCUSDT',get_bitget_candles('BTCUSDT'))
    #     write_market_data_to_database('BTCUSDT',request_bitget_history_data('BTCUSDT','20231001'))
    # except psycopg.errors.UndefinedTable:
    #     create_market_database('BTCUSDT')

    # # 请求所有缺失数据
    # list(map(lambda date:write_market_data_to_database('BTCUSDT',request_bitget_history_data('BTCUSDT',date)),find_date_with_missing_data('BTCUSDT')))

    # get_candles()
    print(Candles_Data_Table("USD","bitget","1m")())