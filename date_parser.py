import argparse
import datetime
import re

def parse_date(text):
    current_date = datetime.datetime.now()
    year = current_date.year
    current_month = current_date.month
    current_day = current_date.day

    numeric_months = {
        1: 'января',
        2: 'февраля',
        3: 'марта',
        4: 'апреля',
        5: 'мая',
        6: 'июня',
        7: 'июля',
        8: 'августа',
        9: 'сентября',
        10: 'октября',
        11: 'ноября',
        12: 'декабря'
    }

    weekdays = {
        "понедельник": 0,
        "вторник": 1,
        "среда": 2,
        "четверг": 3,
        "пятница": 4,
        "суббота": 5,
        "воскресенье": 6
    }

    pattern = r'(\d*)-?(й|я|яя)? (\w+)'

    match = re.match(pattern, text)
    if not match:
        print("Ошибка: неверный формат текста")
        return

    day = match.group(1)
    if not day:
        day = current_day
    else:
        day = int(day)

    weekday_word = match.group(2)
    if weekday_word:
        if 'й' in weekday_word:
            weekday_word = weekday_word.replace('й', 'яя')
        if 'яя' in weekday_word:
            weekday_value = weekday_word.replace('яя', '')
            weekday = (int(weekday_value) - 1) % 7 if weekday_value else current_date.weekday()
        else:
            weekday = weekdays.get(weekday_word.lower(), current_date.weekday())
    else:
        weekday = current_date.weekday()

    month_word = match.group(3).lower()
    if month_word.isdigit():
        month = int(month_word)
    else:
        month = None
        for key, value in numeric_months.items():
            if value.startswith(month_word):
                month = key
                break

    if month is None:
        month = current_month

    try:
        result_date = datetime.datetime(year, month, day)
        while result_date.weekday() != weekday:
            result_date += datetime.timedelta(days=1)
        print(result_date.strftime("%d.%m.%Y"))
    except ValueError as e:
        print(f"Ошибка: {e}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Разобрать дату из текста")
    parser.add_argument("text", help="Текст для разбора")
    args = parser.parse_args()

    parse_date(args.text)