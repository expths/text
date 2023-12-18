import mplfinance as mpf
import numpy as np
import pandas as pd
from random import randint
import psycopg
import matplotlib.pyplot as plt
import configparser

try:
    config = configparser.ConfigParser()
    config.read('config.ini')
except FileNotFoundError:
    print("[ERR]配置文件缺失")

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


table_name = lambda symbol:f"{symbol}_market_data"
rag = " minute_stamp<28315679"

def a(symbol):
    """
    读取数据返回Ndarray。
    """
    with psycopg.connect(**db) as conn:
        with conn.cursor() as cur:
            cur.execute(f"SELECT * FROM {table_name(symbol)} WHERE {rag} ORDER BY minute_stamp ASC")
            return np.array(cur.fetchall())

data = a('BTCUSDT')

# 将 n 维数组转换成 DataFrame，手动设置日期列和索引
df = pd.DataFrame(data, columns=['date', 'open', 'high', 'low', 'close','',''])
df['date'] = pd.to_datetime(df['date'], unit='m')
df.set_index('date', inplace=True)

# 配置样式
mpfstyle = mpf.make_mpf_style(
    marketcolors=mpf.make_marketcolors( # 蜡烛样式
        up='#00BFFF', # 上昇時のろうそくの塗りつぶし色
        down='#DC143C', # 下降時のろうそくの塗りつぶし色
        edge='lightgray', # ろうそくの端の線の色
        wick={
            # 辞書形式で、ろうそく足の真の色を指定
            'up':'#00BFFF', # 上昇時のろうそくの芯の色
            'down':'#DC143C' # 下降時のろうそくの芯の色
        }
    ),
    gridcolor='lightgray', # チャートのグリッドの色
    facecolor='white', # チャートの背景の色
    edgecolor='black', # チャートの外枠の色
    figcolor='white', # チャートの外側の色
    gridstyle='-', # チャートのグリッドの種類 "--":実線, "--":破線, ":":点線, "-.":破線と点線の組み合わせ
    gridaxis='both', # チャートのグリッドの有無を指定 both:縦横双方, horizontal:横線のみ, vertical:縦線のみ
    y_on_right=False, # y軸を右に表示するかどうかを指定
    rc = {
        'xtick.color': 'black', # X軸の色
        'xtick.labelsize': 8, # X軸の文字サイズ
        'ytick.color': 'black', # Y軸の色
        'ytick.labelsize': 8, # Y軸の文字サイズ
        'axes.labelsize': 10, # 軸ラベルの文字サイズ
        'axes.labelcolor': 'black', # 軸ラベルの色
        # 'font.family': 'IPAexGothic', # タイトル,ラベルのフォントを指定
    }
)

# 使用 'yahoo' 样式绘制蜡烛图
mpf.plot(df, type='line', style=mpfstyle, title='Candlestick Chart with NumPy Array',datetime_format='%Y/%m/%d',axisoff=False,mav=(5, 25, 75))
