# import crawler.bitget_api.v1.mix.order_api as maxOrderApi
import bitget_api.bitget_api as baseApi
from bitget_api.exceptions import BitgetAPIException
import configparser
from typing import List
from typing import Optional
from sqlalchemy import ForeignKey
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from sqlalchemy import select
from sqlalchemy.exc import IntegrityError
from celery import Celery


try:
    config = configparser.ConfigParser()
    config.read('config.ini')
    api = baseApi.BitgetApi(config.get('bitget','APIKey'),
                            config.get('bitget','SecretKey'),
                            config.get('bitget','passphrase'))

except FileNotFoundError:
    print("[ERR]配置文件缺失")

except configparser.NoSectionError:
    print("[ERR]缺少API配置")


class Base(DeclarativeBase):
    pass


class Asset_status(Base):
    __tablename__ = "asset_status"

    # id是按分钟数计算的时间戳。
    id:Mapped[int] = mapped_column(primary_key=True)
    accountEquity: Mapped[str]
    unrealizedPL: Mapped[str]
    crossedRiskRate: Mapped[str]

    def __repr__(self) -> str:
        return f"当前资产(时间{self.id}, 数量{self.accountEquity})"


bitgetWorker = Celery('a_tasks'
engine = create_engine("sqlite:///test.db", echo=True)
Base.metadata.create_all(engine)
dbsession = Session(engine)


@bitgetWorker.task(ignore_result=True)
def get_asset_now():
    """
    请求当前账户资产情况。

    用于未来分析投资状况。

    - unrealizedPL 未实现盈亏
    - accountEquity 账户权益
    - crossedRiskRate 风险率

    每分钟请求一次，绘制图表。
    通过requestTime字段获得当前时间。
    """

    # 请求账户资产数据
    # response对象中包含有4个元素['code', 'msg', 'requestTime', 'data']
    resp = api.get("/api/v2/mix/account/accounts",{"productType":"USDT-FUTURES"})
    if resp['msg'] != "success":
        print("请求失败！")
        return
    
    # 提取数据，只有一个账户。
    time = int(resp['requestTime'])//60000
    data = resp['data'][0]

    # 保存数据，将数据存入管道。
    dbsession.add(Asset_status(
        id=time,
        accountEquity=data['accountEquity'],
        unrealizedPL=data['unrealizedPL'],
        crossedRiskRate=data['crossedRiskRate']
        ))
    try:
        dbsession.commit()
    except IntegrityError:
        dbsession.rollback()
    print(f"当前资产：{data['accountEquity']} {data['unrealizedPL']}")

@bitgetWorker.task(ignore_result=True)
def print_all_asset_status():
    """
    打印历史资产状况
    """
    stmt = (
        select(Asset_status)
        # .where(Asset_status)
        )
    for i in dbsession.scalars(stmt):
        print(i)


@bitgetWorker.on_after_configure.connect
def setup_periodic_tasks(sender, **kwargs):
    # Calls test('hello') every 10 seconds.
    # sender.add_periodic_task(10.0, test.s('hello'), name='add every 10')

    # Calls test('hello') every 30 seconds.
    # It uses the same signature of previous task, an explicit name is
    # defined to avoid this task replacing the previous one defined.
    # sender.add_periodic_task(30.0, test.s('hello'), name='add every 30')

    # Calls test('world') every 30 seconds
    # sender.add_periodic_task(30.0, test.s('world'), expires=10)

    # Executes every Monday morning at 7:30 a.m.
    # sender.add_periodic_task(
    #     crontab(hour=7, minute=30, day_of_week=1),
    #     test.s('Happy Mondays!'),
    # )

    sender.add_periodic_task(60.0,get_asset_now.s(),name="每分钟检查资产")

bitgetWorker.conf.timezone = 'UTC'
bitgetWorker.conf.beat_schedule = {
    '每分钟检查资产': {
        'task': 'bitget.get_asset_now',
        'schedule': 60.0,
        'args': ()
    },
}

