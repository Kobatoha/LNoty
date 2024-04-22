from sqlalchemy import Column, Integer, String, DateTime, Boolean, VARCHAR, DATE, TIME, ForeignKey, BigInteger
from DataBase.Base import Base
import datetime


class EssenceSetting(Base):
    __tablename__ = 'settings'

    id = Column(Integer, primary_key=True)
    id_user = Column(BigInteger, ForeignKey('users.telegram_id'))

    soloraidboss = Column(Boolean, default=False)           # Соло Боссы
    kuka = Column(Boolean, default=False)                   # Кука и Джисра
    keber = Column(Boolean, default=False)                  # Кебер
    loa = Column(Boolean, default=False)                    # Логово Антараса
    frost = Column(Boolean, default=False)                  # Замок Монарха Льда
    fortress = Column(Boolean, default=False)               # Крепость Орков
    balok = Column(Boolean, default=False)                  # Битва с Валлоком
    olympiad = Column(Boolean, default=False)               # Всемирная Олимпиада
    hellbound = Column(Boolean, default=False)              # Остров Ада
    siege = Column(Boolean, default=False)                  # Осада Гирана
    invasion = Column(Boolean, default=False)               # Вторжение
    primetime = Column(Boolean, default=False)              # Хот-тайм зачистки
    purge = Column(Boolean, default=False)                  # Сбор зачистки
    sevensings = Column(Boolean, default=False)             # Семь Печатей

    event = Column(Boolean, default=False)                  # Ивент [меняется]
    calendar = Column(Boolean, default=False)               # Календарь [меняется]
    festival = Column(Boolean, default=False)               # Фестиваль [меняется]

    fulltime = Column(Boolean, default=False)               # '00:00 - 23:59' if True else '9:00 - 23:00'


class EssenceCustomSetting(Base):
    __tablename__ = 'RuoffCustom_settings'

    id = Column(Integer, primary_key=True)
    id_user = Column(BigInteger, ForeignKey('users.telegram_id'))

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


class EssenceClanDangeon(Base):
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


class EssenceBigWar(Base):
    __tablename__ = 'bigwar_settings'

    id = Column(Integer, primary_key=True)
    id_user = Column(BigInteger, ForeignKey('users.telegram_id'))

    toi = Column(Boolean, default=False)                # Башня Дерзости 15:00 | 21:00 [ежедневно]
    gardens = Column(Boolean, default=False)            # Забытый Сад 23:00 [ежедневно]
    pagan = Column(Boolean, default=False)              # Языческий Храм 22:00 [пятница]
    kelbim = Column(Boolean, default=False)             # Крепость Кельбима 22:00 [пятница]
    antharas = Column(Boolean, default=False)           # Битва с Антарасом 22:00 [воскресенье]
    hellbound = Column(Boolean, default=False)          # Остров Ада 11:00 | 22:00 | 23:00 [суббота]
    chaotic = Column(Boolean, default=False)            # Хаотический Босс 20:00 [ежедневно]
    lilith = Column(Boolean, default=False)             # Лилит 19:00 [понедельник, четверг]
    anakim = Column(Boolean, default=False)             # Анаким 19:00 [вторник, пятница]
    gord = Column(Boolean, default=False)               # Горд 21:00 [ежедневно]
    frost = Column(Boolean, default=False)              # Замок Монарха Льда 21:30 | 22:00 [вторник, четверг]
    loa = Column(Boolean, default=False)                # Логово Антараса 22:00 [понедельник, среда]
    coral = Column(Boolean, default=False)              # Рейдовые Боссы 80-го, 85-го, 90-го уровней [22 часа]


class LegacySetting(Base):
    __tablename__ = 'legacy_settings'

    id = Column(Integer, primary_key=True)
    id_user = Column(BigInteger, ForeignKey('users.telegram_id'))

    prison = Column(Boolean, default=False)             # Тюрьма Бездны
    olympiad = Column(Boolean, default=False)           # Олимпиада
    goldberg = Column(Boolean, default=False)           # Комната Голдберга
    garden = Column(Boolean, default=False)             # Забытый Первобытный Сад
    frost = Column(Boolean, default=False)              # Замок Монарха Льда
    tantar = Column(Boolean, default=False)             # Руины Тантар
    pagan = Column(Boolean, default=False)              # Языческий Храм
    pirates = Column(Boolean, default=False)            # Гробница Древних Пиратов
    antharas = Column(Boolean, default=False)           # Рыцари Балтуса - Антарас
    frintezza = Column(Boolean, default=False)          # Гробница Последнего Императора - Фринтеза
    four_tomb = Column(Boolean, default=False)          # Четыре Гробницы
    purge = Column(Boolean, default=False)              # Сбор зачистки
    primetime = Column(Boolean, default=False)          # Прайм тайм
    bauim = Column(Boolean, default=False)              # Рыцари Балтуса - Баюм
    zaken = Column(Boolean, default=False)              # Рыцари Балтуса - Закен
    arena = Column(Boolean, default=False)              # Арена Клана
    elemental = Column(Boolean, default=False)          # Стихийные Короли

    event = Column(Boolean, default=False)              # Ивент [меняется]

    fulltime = Column(Boolean, default=False)           # '00:00 - 23:59' if True else '9:00 - 23:00'
