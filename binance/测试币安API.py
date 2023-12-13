import binance
from binance.spot import Spot

# pip包：binance-connector
# python包文档：https://binance-connector.readthedocs.io/en/latest/
# API文档：https://binance-docs.github.io/apidocs/spot/en/

# 强平数据API：https://binance-docs.github.io/apidocs/futures/cn/#2f03186fe7

client = Spot()

# Get server timestamp
print(client.time())
# Get klines of BTCUSDT at 1m interval
print(client.klines("BTCUSDT", "1m"))
# Get last 10 klines of BNBUSDT at 1h interval
print(client.klines("BNBUSDT", "1h", limit=10))

# # API key/secret are required for user data endpoints
# client = Spot(api_key='<api_key>', api_secret='<api_secret>')

# # Get account and balance information
# print(client.account())

# # Post a new order
# params = {
#     'symbol': 'BTCUSDT',
#     'side': 'SELL',
#     'type': 'LIMIT',
#     'timeInForce': 'GTC',
#     'quantity': 0.002,
#     'price': 9500
# }

# response = client.new_order(**params)
# print(response)