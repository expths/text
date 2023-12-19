import plotly.graph_objects as go
import pandas as pd
import psycopg
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


symbol = 'BTCUSDT'
table_name = lambda symbol:f"{symbol}_market_data"
rag = " minute_stamp<28315679"
with psycopg.connect(**db) as conn:
    with conn.cursor() as cur:
        cur.execute(f"SELECT * FROM {table_name(symbol)} WHERE {rag} ORDER BY minute_stamp ASC")
        df = pd.DataFrame(cur.fetchall(), columns=['date', 'open', 'high', 'low', 'close','',''])
        df['date'] = pd.to_datetime(df['date'], unit='m')
        df.set_index('date', inplace=True)


# 创建交互式蜡烛图
fig = go.Figure(data=[go.Candlestick(x=df.index,
                open=df['open'],
                high=df['high'],
                low=df['low'],
                close=df['close'])])

# 设置图表布局
fig.update_layout(title='Interactive Candlestick Chart',
                  xaxis_title='Date',
                  yaxis_title='Price',
                  xaxis_rangeslider_visible=True)

# 显示图表
fig.show()