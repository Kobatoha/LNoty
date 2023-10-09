from sqlalchemy import Column, Integer, String, DateTime, Boolean, VARCHAR, DATE, TIME, ForeignKey, BigInteger
from DataBase.Base import Base
import datetime


class Feedback(Base):
    __tablename__ = 'feedbacks'

    id = Column(Integer, primary_key=True)
    telegram_id = Column(BigInteger, nullable=False)
    username = Column(VARCHAR(32), nullable=True)
    text = Column(VARCHAR(300), nullable=False)
    date = Column(DATE, default=datetime.date.today().strftime("%Y-%m-%d %H:%M"))
