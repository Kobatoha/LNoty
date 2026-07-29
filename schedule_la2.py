import asyncio
from datetime import datetime, timedelta
from colorama import init, Fore, Back, Style

# Инициализация colorama (автосброс цветов)
init(autoreset=True)

# 🗓️ Планировщик с условиями по дням недели
# weekday(): 0=Пн, 1=Вт, 2=Ср, 3=Чт, 4=Пт, 5=Сб, 6=Вс
SCHEDULE = {
    "09:00": {"text": "🔥 Проюзать все проходки и светочи до профилактики", "days": [2]},
    "09:57": {"text": "🔥 Остров Ада", "days": [5]},
    "10:57": {"text": "🔥 Фестиваль цветов - Желтопухи и Розовопухи на острове грёз", "days": None},
    "17:57": {"text": "🔥 Остров Ада. Цитадель", "days": [5]},
    "19:00": {"text": "🔥 Валакас на старых", "days": [6]},
    "20:27": {"text": "🔥 Лес Состязаний", "days": None},
    "21:00": {"text": "🔥 Мафия", "days": None},
    "21:27": {"text": "🔥 Олимп: нужно выгрузить окна", "days": [0, 1, 2, 3, 4]},
    "21:28": {"text": "🔥 Сады", "days": None},
    "22:00": {"text": "🔥 Антарас на старых", "days": [6]},
}

BEORO_TIMES = ["19:25"]

# 🍪 Расписание для "Куки"
COOKIE_TIMES = [
    "08:47", "10:47", "12:47", "14:47", "16:47", "18:47", "20:47", "22:47"
]
COOKIE_TEXT = "🍪 Кука через 3 минуты"

# ⚔ Вторжение (каждые 4 часа после стартового времени)
INVASION_START = ["17:15"]
INVASION_TEXT = "⚔ Вторжение"
INVASION_TIMES = []

for time in INVASION_START:
    current_time = datetime.strptime(time, "%H:%M")
    for i in range(6):
        INVASION_TIMES.append(current_time.strftime("%H:%M"))
        current_time += timedelta(hours=4)

# Убираем дубликаты и сортируем (на всякий случай)
INVASION_TIMES = sorted(set(INVASION_TIMES))

# Словарь дней недели для красивого вывода
DAY_NAMES = {
    0: "Пн", 1: "Вт", 2: "Ср", 3: "Чт", 4: "Пт", 5: "Сб", 6: "Вс"
}


def print_header(text: str):
    """Красивый заголовок"""
    print(f"\n{Back.CYAN}{Fore.BLACK}{Style.BRIGHT} {'=' * 60} {Style.RESET_ALL}")
    print(f"{Back.CYAN}{Fore.BLACK}{Style.BRIGHT} {text:^60} {Style.RESET_ALL}")
    print(f"{Back.CYAN}{Fore.BLACK}{Style.BRIGHT} {'=' * 60} {Style.RESET_ALL}\n")


def print_event(time: str, text: str, status: str = "sent"):
    """Красивое логирование события"""
    time_colored = f"{Fore.YELLOW}{Style.BRIGHT}[{time}]{Style.RESET_ALL}"

    if status == "sent":
        icon = f"{Fore.GREEN}✓{Style.RESET_ALL}"
        status_text = f"{Fore.GREEN}ОТПРАВЛЕНО{Style.RESET_ALL}"
    elif status == "skipped_day":
        icon = f"{Fore.RED}✗{Style.RESET_ALL}"
        status_text = f"{Fore.RED}ПРОПУЩЕНО (не тот день){Style.RESET_ALL}"
    elif status == "skipped_night":
        icon = f"{Fore.MAGENTA}⊙{Style.RESET_ALL}"
        status_text = f"{Fore.MAGENTA}ПРОПУЩЕНО (ночь){Style.RESET_ALL}"
    else:
        icon = f"{Fore.CYAN}→{Style.RESET_ALL}"
        status_text = f"{Fore.CYAN}{status}{Style.RESET_ALL}"

    print(f"  {icon} {time_colored} │ {status_text} │ {Fore.WHITE}{text}{Style.RESET_ALL}")


def print_cookie(time: str):
    """Специальное оформление для куки"""
    print(f"  {Fore.MAGENTA}🍪{Style.RESET_ALL} {Fore.YELLOW}[{time}]{Style.RESET_ALL} │ "
          f"{Fore.MAGENTA}КУКА{Style.RESET_ALL} │ "
          f"{Fore.WHITE}{COOKIE_TEXT} {Fore.CYAN}(@gr0m4){Style.RESET_ALL}")


async def scheduler():
    sent_today = set()

    print_header("📅 ПЛАНИРОВЩИК ИГРОВЫХ СОБЫТИЙ")
    print(f"  {Fore.CYAN}⏰{Style.RESET_ALL} Ожидание наступления событий...")
    print(f"  {Fore.CYAN}📋{Style.RESET_ALL} Всего событий в расписании: {Fore.YELLOW}{len(SCHEDULE)}{Style.RESET_ALL}")
    print(f"  {Fore.CYAN}🍪{Style.RESET_ALL} Кука-таймеров: {Fore.YELLOW}{len(COOKIE_TIMES)}{Style.RESET_ALL}")
    print(f"  {Fore.CYAN}⚔{Style.RESET_ALL} Таймеров вторжения: {Fore.YELLOW}{len(INVASION_TIMES)}{Style.RESET_ALL}")

    # Вывод расписания на сегодня
    now = datetime.now()
    current_day = now.weekday()
    print(f"\n  {Fore.CYAN}📅 Сегодня:{Style.RESET_ALL} {Fore.GREEN}{DAY_NAMES[current_day]}{Style.RESET_ALL}")
    print(f"  {'─' * 58}\n")

    while True:
        now = datetime.now()
        current_time = now.strftime("%H:%M")
        current_day = now.weekday()

        # --- Основные события ---
        if current_time in SCHEDULE and current_time not in sent_today:
            event = SCHEDULE[current_time]
            allow = True

            if "days" in event and event["days"] is not None:
                allow = current_day in event["days"]
            if "exclude" in event and current_day in event["exclude"]:
                allow = False

            if allow:
                # 🎯 Отправка (в консоль)
                print_event(current_time, event["text"], "sent")
                sent_today.add(current_time)
            else:
                print_event(current_time, event["text"], "skipped_day")
                sent_today.add(current_time)

        # --- Куки ---
        if current_time in COOKIE_TIMES and current_time not in sent_today:
            print_cookie(current_time)
            sent_today.add(current_time)

        # --- Беоро ---
        if current_time in BEORO_TIMES and current_time not in sent_today:
            print(f"  {Fore.BLUE}🐻{Style.RESET_ALL} {Fore.YELLOW}[{current_time}]{Style.RESET_ALL} │ "
                  f"{Fore.BLUE}БЕОРО{Style.RESET_ALL} │ "
                  f"{Fore.WHITE}Беоро через 5 минут{Style.RESET_ALL}")
            sent_today.add(current_time)

        # --- Вторжение ---
        if current_time in INVASION_TIMES and current_time not in sent_today:
            if "00:00" <= current_time <= "09:59":
                print_event(current_time, INVASION_TEXT, "skipped_night")
            else:
                print_event(current_time, INVASION_TEXT, "sent")
            sent_today.add(current_time)

        # --- Сброс в полночь ---
        if current_time == "00:00" and current_time not in sent_today:
            sent_today.clear()
            print(f"\n  {Fore.CYAN}{'─' * 58}{Style.RESET_ALL}")
            print(f"  {Fore.GREEN}🔄 [00:00] Список отправленных сообщений очищен{Style.RESET_ALL}")
            print(
                f"  {Fore.CYAN}📅 Новый день:{Style.RESET_ALL} {Fore.GREEN}{DAY_NAMES[(current_day + 1) % 7]}{Style.RESET_ALL}")
            print(f"  {Fore.CYAN}{'─' * 58}{Style.RESET_ALL}\n")
            sent_today.add(current_time)

        await asyncio.sleep(30)


async def main():
    print(f"\n{Back.GREEN}{Fore.BLACK}{Style.BRIGHT} {'=' * 60} {Style.RESET_ALL}")
    print(f"{Back.GREEN}{Fore.BLACK}{Style.BRIGHT}  🚀 ПЛАНИРОВЩИК ЗАПУЩЕН  {Style.RESET_ALL}")
    print(f"{Back.GREEN}{Fore.BLACK}{Style.BRIGHT}  Режим: КОНСОЛЬ (без Telegram)  {Style.RESET_ALL}")
    print(f"{Back.GREEN}{Fore.BLACK}{Style.BRIGHT} {'=' * 60} {Style.RESET_ALL}")

    await scheduler()


if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print(f"\n{Fore.YELLOW}{Style.BRIGHT}⏹️  Планировщик остановлен пользователем{Style.RESET_ALL}")
    except Exception as e:
        print(f"\n{Fore.RED}{Style.BRIGHT}❌ Ошибка: {e}{Style.RESET_ALL}")
