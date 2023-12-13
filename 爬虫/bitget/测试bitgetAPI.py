import bitget_api.v1.mix.order_api as maxOrderApi
import bitget_api.bitget_api as baseApi
from bitget_api.exceptions import BitgetAPIException
from config_manager import BITGET_API

apiKey = BITGET_API["APIKey"]
secretKey = BITGET_API["SecretKey"]
passphrase = BITGET_API["passphrase"]
baseApi = baseApi.BitgetApi(apiKey, secretKey, passphrase)

# try:
#     params = {}
#     params["symbol"] = "BTCUSDT_UMCBL"
#     params["marginCoin"] = "USDT"
#     params["side"] = "open_long"
#     params["orderType"] = "limit"
#     params["price"] = "27012"
#     params["size"] = "0.01"
#     params["timInForceValue"] = "normal"
#     response = baseApi.post("/api/mix/v1/order/placeOrder", params)
#     print(response)
# except BitgetAPIException as e:
#     print("error:" + e.message)

p = {'productType':'USDT-FUTURES','marginCoin':'USDT'}
a = baseApi.get('/api/v2/mix/position/all-position',p)
a = map(lambda order:order['symbol'],a['data'])
a = (baseApi.get('/api/v2/spot/market/candles',{'symbol':x,'granularity':'1min'})for x in a)
a = map(lambda line:line['data'],a)
print(list(a))

