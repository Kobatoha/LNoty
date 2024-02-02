from sqlalchemy import Column, Integer, VARCHAR
from DataBase.Base import Base


class RaidBoss(Base):
    __tablename__ = 'raidbosses'

    id = Column(Integer, primary_key=True)

    name = Column(VARCHAR(50))                              # Название Босса
    level = Column(Integer, default=80)                     # Уровень Босса
    coral_time = Column(VARCHAR(5))                         # Время респа на сервере Coral
    aqua_time = Column(VARCHAR(5))                          # Время респа на сервере Aqua
    magenta_time = Column(VARCHAR(5))                       # Время респа на сервере Magenta
    bluesky_time = Column(VARCHAR(5))                       # Время респа на сервере BlueSky
