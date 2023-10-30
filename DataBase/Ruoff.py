from sqlalchemy import Column, Integer, String, DateTime, Boolean, VARCHAR, DATE, TIME, ForeignKey, BigInteger
from DataBase.Base import Base
import datetime


class Setting(Base):
    __tablename__ = 'settings'

    id = Column(Integer, primary_key=True)
    id_user = Column(Integer, ForeignKey('users.telegram_id'))

    soloraidboss = Column(Boolean, default=False)           # Соло Боссы
    kuka = Column(Boolean, default=False)                   # Кука и Джисра
    loa = Column(Boolean, default=False)                    # Логово Антараса
    frost = Column(Boolean, default=False)                  # Замок Монарха Льда
    fortress = Column(Boolean, default=False)               # Крепость Орков
    balok = Column(Boolean, default=False)                  # Битва с Валлоком
    olympiad = Column(Boolean, default=False)               # Всемирная Олимпиада
    hellbound = Column(Boolean, default=False)              # Остров Ада
    siege = Column(Boolean, default=False)                  # Осада Гирана
    primetime = Column(Boolean, default=False)              # Хот-тайм зачистки
    purge = Column(Boolean, default=False)                  # Сбор зачистки

    event = Column(Boolean, default=False)                  # Ивент [меняется]
    calendar = Column(Boolean, default=False)               # Календарь [меняется]

    fulltime = Column(Boolean, default=False)               # '00:00 - 23:59' if True else '9:00 - 23:00'


class RuoffCustomSetting(Base):
    __tablename__ = 'RuoffCustom_settings'

    id = Column(Integer, primary_key=True)
    id_user = Column(Integer, ForeignKey('users.telegram_id'))

    dream_day = Column(VARCHAR)             # Грезы [день]
    dream_time = Column(VARCHAR(5))         # Грезы [время]

    valakas_day = Column(VARCHAR)           # Храм Валакаса [день]
    valakas_time = Column(VARCHAR(5))       # Храм Валакаса [время]

    frintezza_day = Column(VARCHAR)         # Битва с Фринтезой [день]
    frintezza_time = Column(VARCHAR(5))     # Битва с Фринтезой [время]

    gardens = Column(VARCHAR(5))            # Забытые сады [ежедневно]
    goddard = Column(VARCHAR(5))            # Исследование Годдарда [ежедневно]
    training = Column(VARCHAR(5))           # Тренировочное подземелье [ежедневно]
    transcendent = Column(VARCHAR(5))       # Невероятная временная зона [ежедневно]
    toi = Column(VARCHAR(5))                # Башня Дерзости [ежедневно]
    pagan = Column(VARCHAR(5))              # Языческий Храм\Крепость Кельбима [пн-пт + вс после 00:00]
    aztacan = Column(VARCHAR(5))            # Храм Ацтакана [ежедневно]

    tattoo = Column(VARCHAR(5))             # Прокачать тату


class RuoffClanDangeon(Base):
    __tablename__ = 'RuoffClanDangeon_settings'

    id = Column(Integer, primary_key=True)
    id_user = Column(BigInteger, ForeignKey('users.telegram_id'))

    clan_dangeon_time = Column(VARCHAR(5))              # Подземелье клана [время]

    clan_dangeon_mo = Column(Boolean, default=False)    # Подземелье клана [monday]
    clan_dangeon_tu = Column(Boolean, default=False)    # Подземелье клана [tuesday]
    clan_dangeon_we = Column(Boolean, default=False)    # Подземелье клана [wednesday]
    clan_dangeon_th = Column(Boolean, default=False)    # Подземелье клана [thursday]
    clan_dangeon_fr = Column(Boolean, default=False)    # Подземелье клана [friday]
    clan_dangeon_sa = Column(Boolean, default=False)    # Подземелье клана [saturday]
    clan_dangeon_su = Column(Boolean, default=False)    # Подземелье клана [sunday]


class RuoffBigWar(Base):
    __tablename__ = 'bigwar_settings'

    id = Column(Integer, primary_key=True)
    id_user = Column(BigInteger, ForeignKey('users.telegram_id'))

    toi = Column(Boolean, default=False)
    gardens = Column(Boolean, default=False)
    pagan = Column(Boolean, default=False)
    antharas = Column(Boolean, default=False)
    hellbound = Column(Boolean, default=False)
    chaotic = Column(Boolean, default=False)
    lilith = Column(Boolean, default=False)
    anakim = Column(Boolean, default=False)
    gord = Column(Boolean, default=False)
    frost = Column(Boolean, default=False)
    loa = Column(Boolean, default=False)
