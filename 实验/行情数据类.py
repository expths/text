from abc import ABC
from datetime import datetime,timedelta

class Market_date(ABC):
    @classmethod
    def __instancecheck__(cls,obj):
        try:
            datetime.strptime(obj,'%Y%m%d')
            print(datetime.strptime(obj,'%Y%m%d'))
            return True
        except:
            return False

class Meta_minute_stamp(type):
    @classmethod
    def __instancecheck__(cls,obj):
        try:
            datetime.strptime(obj,'%Y%m%d')
            print(datetime.strptime(obj,'%Y%m%d'))
            return True
        except:
            return False

class Minute_stamp(metaclass=Meta_minute_stamp):
    pass

