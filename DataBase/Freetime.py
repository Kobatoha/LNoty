from sqlalchemy import Column, Integer, String, DateTime, Boolean, VARCHAR, DATE, TIME, ForeignKey, BigInteger
from DataBase.Base import Base
import datetime


class Freetime(Base):
    __tablename__ = 'freetime'

    id = Column(Integer, primary_key=True)
    id_user = Column(BigInteger, ForeignKey('users.telegram_id'))

    kuka = Column(VARCHAR(5))                   # Кука и Джисра
    loa_day = Column(VARCHAR(15))               # Логово Антараса [DAY]
    loa_time = Column(VARCHAR(5))               # Логово Антараса [TIME]
    frost = Column(VARCHAR(5))                  # Замок Монарха Льда
    fortress = Column(VARCHAR(5))               # Крепость Орков
    balok = Column(VARCHAR(5))                  # Битва с Валлоком
    olympiad = Column(VARCHAR(5))               # Всемирная Олимпиада
    hellbound = Column(VARCHAR(5))              # Остров Ада
    siege = Column(VARCHAR(5))                  # Осада Гирана
    primetime = Column(VARCHAR(5))              # Хот-тайм зачистки
    purge = Column(VARCHAR(5))                  # Сбор зачистки

    event = Column(VARCHAR(5))                  # Ивент [меняется]
    calendar = Column(VARCHAR(5))               # Календарь [меняется]
    festival = Column(VARCHAR(5))               # Фестиваль [меняется]

    dream_day = Column(VARCHAR)                 # Грезы [день]
    dream_time = Column(VARCHAR(5))             # Грезы [время]

    gardens = Column(VARCHAR(5))                # Забытые сады [ежедневно]
    goddard = Column(VARCHAR(5))                # Исследование Годдарда [ежедневно]
    training = Column(VARCHAR(5))               # Тренировочное подземелье [ежедневно]
    transcendent = Column(VARCHAR(5))           # Невероятная временная зона [ежедневно]
    toi = Column(VARCHAR(5))                    # Башня Дерзости [ежедневно]
    pagan = Column(VARCHAR(5))                  # Языческий Храм\Крепость Кельбима [пн-пт + вс после 00:00]
    aztacan = Column(VARCHAR(5))                # Храм Ацтакана [ежедневно]

    tattoo = Column(VARCHAR(5))                 # Прокачать тату


