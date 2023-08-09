from sqlalchemy import Column, Integer, String, DateTime, Boolean, VARCHAR, DATE, TIME, ForeignKey
from DataBase.Base import Base
import datetime


class Expanse(Base):
    __tablename__ = 'Expanse_settings'

    id = Column(Integer, primary_key=True)
    id_user = Column(Integer, ForeignKey('users.telegram_id'))

    soloraidboss = Column(Boolean, default=False)
    loa = Column(Boolean, default=False)
    frost = Column(Boolean, default=False)
    balok = Column(Boolean, default=False)
    olympiad = Column(Boolean, default=False)
    hellbound = Column(Boolean, default=False)
    siege = Column(Boolean, default=False)
    event = Column(Boolean, default=False)

    fulltime = Column(Boolean, default=False)
