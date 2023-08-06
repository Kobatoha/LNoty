from sqlalchemy import Column, Integer, String, DateTime, Boolean, VARCHAR, DATE, TIME, ForeignKey
from sqlalchemy.orm import declarative_base
import datetime

Base = declarative_base()


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    telegram_id = Column(Integer, unique=True, nullable=False)
    username = Column(VARCHAR(32), unique=False, nullable=True)
    server = Column(VARCHAR(50))
    reg_date = Column(DATE, default=datetime.date.today())
    upd_date = Column(DATE, onupdate=datetime.date.today())

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



