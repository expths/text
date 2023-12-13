
import requests
from datetime import datetime


url = "https://open-api.coinglass.com/public/v2/indicator/liquidation_pair"

def requests_coinglass():
    """
    通过API向coinglass请求爆仓数据。

    API参考文档：
    https://coinglass.readme.io/reference/getting-started-with-your-api

    典型回复：
    {
      "turnoverNumber": 100,
      "buyTurnoverNumber": 36,
      "sellTurnoverNumber": 64,
      "sellQty": 0,
      "buyQty": 0,
      "buyVolUsd": 158856.74009,
      "sellVolUsd": 223262.66953,
      "volUsd": 382119.40962,
      "createTime": 1702303200000,
      "t": 0
    }

    异常回复：
    {
        'sellQty': 0,
        'buyQty': 0,
        'createTime': 1702303200000,
        't': 0
    }
    """
    # 配置时间
    time = int(datetime.now().timestamp()*1000)

    # 构造请求头
    payload = {
        "ex":"Binance",
        "pair":'BTCUSDT',
        "interval":"h1",
        "limit":500,# 最大500
        "start_time":"",
        "end_time":""
    }
    headers = {
        "accept": "application/json",
        "coinglassSecret": "d3fceb1c02e149169f2a78bbbe0bcba3"
    }

    # 发起请求
    response = requests.get(url,params=payload,headers=headers)
    if response.status_code != 200:
        raise RuntimeError("请求失败！")

    data = response.json()
    if data['msg'] == 'API key missing.':
        print("API异常")
    if data['msg'] == 'Upgrade plan':
        print("请求套餐异常")

    if data['msg'] == 'success':
        print("[OK]请求成功")

    return data['data']


for i in requests_coinglass():
    try:
        print("[OK]",i['sellQty'],i['buyQty'],i['volUsd'])
    except:
        print("[ERR]",i)
        continue