from dataclasses import dataclass

@dataclass
class trading_pair:
    name:str

@dataclass
class price:
    price:int

@dataclass
class trading_volume:
    volume:int

@dataclass
class ticker_information:
    symbol:trading_pair
    high24h:price

@dataclass
class candlestick_data:
    time:trading_pair
    open:price
    high:price
    low:price
    close:price
    base_volume:trading_volume
    quote_volume:trading_volume

def test(symbol:trading_pair)->candlestick_data:
    data = (1,1,1,1,1,1,1)
    return data
