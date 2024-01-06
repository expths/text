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

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "user_account"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String(30))
    fullname: Mapped[Optional[str]]
    addresses: Mapped[List["Address"]] = relationship(
        back_populates="user", cascade="all, delete-orphan"
    )
    def __repr__(self) -> str:
        return f"User(id={self.id!r}, name={self.name!r}, fullname={self.fullname!r})"

class Address(Base):
    __tablename__ = "address"
    id: Mapped[int] = mapped_column(primary_key=True)
    email_address: Mapped[str]
    user_id: Mapped[int] = mapped_column(ForeignKey("user_account.id"))
    user: Mapped["User"] = relationship(back_populates="addresses")
    def __repr__(self) -> str:
        return f"Address(id={self.id!r}, email_address={self.email_address!r})"
    

class Asset_status(Base):
    __tablename__ = "asset_status"

    # id是按分钟数计算的时间戳。
    id:Mapped[int] = mapped_column(primary_key=True)
    accountEquity: Mapped[str]
    unrealizedPL: Mapped[str]
    crossedRiskRate: Mapped[str]

    def __repr__(self) -> str:
        return f"当前资产(时间{self.id}, 数量{self.accountEquity})"


# 创建引擎，echo参数启动调试数据。
engine = create_engine("sqlite:///data/test.db", echo=True)
Base.metadata.create_all(engine)
dbsession = Session(engine)


with Session(engine) as session:
    spongebob = User(
        name="spongebob",
        fullname="Spongebob Squarepants",
        addresses=[Address(email_address="spongebob@sqlalchemy.org")],
    )
    sandy = User(
        name="sandy",
        fullname="Sandy Cheeks",
        addresses=[
            Address(email_address="sandy@sqlalchemy.org"),
            Address(email_address="sandy@squirrelpower.org"),
        ],
    )
    patrick = User(name="patrick", fullname="Patrick Star")

    # 使用add方法将对象加入缓存区，使用commit方法提交所有对象。
    session.add_all([spongebob, sandy, patrick])
    session.commit()



with Session(engine)as session:
    # 查询数据库中的数据
    stmt = (
        select(User)
        .where(User.name.in_(["spongebob", "sandy"]))
        )
    for user in session.scalars(stmt):
        print(user)

dbsession.close()