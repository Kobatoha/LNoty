from sqlalchemy import Column, Integer, String, DateTime, Boolean, VARCHAR, DATE, TIME, ForeignKey, BigInteger
from DataBase.Base import Base
import datetime


class Freetime(Base):
    __tablename__ = 'freetime'

    id = Column(Integer, primary_key=True)
    id_user = Column(BigInteger, ForeignKey('users.telegram_id'))

    kuka_time = Column(VARCHAR(5))              # Кука и Джисра [TIME EVERYDAY]

    loa_day_one = Column(VARCHAR(15))           # Логово Антараса [DAY ONE]
    loa_day_two = Column(VARCHAR(15))           # Логово Антараса [DAY TWO]
    loa_time = Column(VARCHAR(5))               # Логово Антараса [TIME]

    frost_day_one = Column(VARCHAR(15))         # Замок Монарха Льда [DAY ONE]
    frost_day_two = Column(VARCHAR(15))         # Замок Монарха Льда [DAY TWO]
    frost_time = Column(VARCHAR(5))             # Замок Монарха Льда [TIME]

    fortress_time = Column(VARCHAR(5))          # Крепость Орков [TIME EVERYDAY]

    # balok = Column(VARCHAR(15))                    # Битва с Валлоком
    # olympiad = Column(VARCHAR(5))               # Всемирная Олимпиада

    hellbound_day = Column(VARCHAR(5))          # Остров Ада [DAY]
    hellbound_time = Column(VARCHAR(5))         # Остров Ада [TIME]

    siege_day = Column(VARCHAR(15))             # Осада Гирана [DAY]
    siege_time = Column(VARCHAR(5))             # Осада Гирана [TIME]

    # primetime_time = Column(VARCHAR(5))         # Хот-тайм зачистки [EVERYDAY]

    purge_day = Column(VARCHAR(5))              # Сбор зачистки [DAY]
    purge_time = Column(VARCHAR(5))             # Сбор зачистки [TIME]

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


