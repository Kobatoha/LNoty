from sqlalchemy import Column, Integer, String, DateTime, Boolean, VARCHAR, DATE, TIME, ForeignKey
from DataBase.Base import Base
import datetime


class Setting(Base):
    __tablename__ = 'settings'

    id = Column(Integer, primary_key=True)
    id_user = Column(Integer, ForeignKey('users.telegram_id'))

    soloraidboss = Column(Boolean, default=False)
    kuka = Column(Boolean, default=False)
    loa = Column(Boolean, default=False)
    frost = Column(Boolean, default=False)
    fortress = Column(Boolean, default=False)
    balok = Column(Boolean, default=False)
    olympiad = Column(Boolean, default=False)
    hellbound = Column(Boolean, default=False)
    siege = Column(Boolean, default=False)
    primetime = Column(Boolean, default=False)
    purge = Column(Boolean, default=False)

    event = Column(Boolean, default=False)

    # telegram bot time work - 00:00 - 23:59 if True, else 9:00 - 23:00
    fulltime = Column(Boolean, default=False)



