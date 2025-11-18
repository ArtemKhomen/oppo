import re
from datetime import datetime

date_pattern = r'\d{4}\.\d{2}\.\d{2}'
place_pattern = r'"([^"]+)"'
value_pattern = r'(?<!\S)(-?\d+(?:\.\d+)?)(?!\S)\s*$'

class TempMeasure:
    MIN_TEMP = -100.0
    MAX_TEMP = 100.0

    def __init__(self, date: datetime, place: str, result: float):

        self.date = date # Дата описывается в формате гггг.мм.дд
        self.place = place
        self.result = result

    @classmethod
    def from_string(cls, input_string: str):
        date_str = parse_string(input_string, date_pattern)
        city = parse_string(input_string, place_pattern)
        value_str = parse_string(input_string, value_pattern)

        try:
            date = datetime.strptime(date_str, "%Y.%m.%d")
            if not (0 <= date.year <= datetime.now().year):
                raise ValueError(f"Год {date.year} вне реалистичного диапазона (0-{datetime.now().year})")
        except ValueError as e:
            raise ValueError(f"Неверный формат даты '{date_str}': {e}")

        try:
            value = float(value_str)
            if not (cls.MIN_TEMP <= value <= cls.MAX_TEMP):
                raise ValueError(f"Температура {value} вне реалистичного диапазона ({cls.MIN_TEMP}-{cls.MAX_TEMP})")
        except ValueError as e:
            raise ValueError(f"Неверный формат температуры '{value_str}': {e}")

        return cls(date, city, value)

    def __str__(self):
        return f'{self.date.strftime("%Y.%m.%d")} {self.place} {self.result}'

class FileManager:
    FILENAME = 'values.txt'

    @classmethod
    def read_measures(cls):
        measures = []
        with open(cls.FILENAME, 'r', encoding='utf-8') as f:
            for line in f:
                m = line.strip().split()
                date_str = m[0]
                try:
                    date = datetime.strptime(date_str, "%Y.%m.%d")
                except ValueError as e:
                    print(f"Предупреждение: пропущена некорректная строка '{line}': {e}")
                    continue
                measures.append(TempMeasure(date, m[1], float(m[2])))
        return measures

    @classmethod
    def write_measures(cls, measures):
        with open(cls.FILENAME, 'w', encoding='utf-8') as f:
            for m in measures:
                f.write(f'{m}\n')

    @classmethod
    def append_measure(cls, measure):
        with open(cls.FILENAME, 'a', encoding='utf-8') as f:
            f.write(f'{measure}\n')

patterns = {
    date_pattern: 'Дата в формате ГГГГ.ММ.ДД',
    place_pattern: 'Место измерения в кавычках',
    value_pattern: 'Значение температуры числом'}

def parse_string(text, pattern):
    parsed_string = re.findall(pattern, text)
    if not parsed_string:
        raise ValueError(f'Не найдено значение для: {patterns.get(pattern)}')
    return parsed_string[0]

def input_measure():
    print('Формат: (ГГГГ.ММ.ДД "Город" значение) в любом порядке')
    new_measure = input('Введите новое измерение: ')
    measure = TempMeasure.from_string(new_measure)
    FileManager.append_measure(measure)

def print_measures():
    measures = FileManager.read_measures()
    for measure in measures:
        print(measure)

def print_measures_range():
    print('Введите границы диапазона температур')
    try:
        ran1 = float(input('  От (минимальная температура): '))
        ran2 = float(input('  До (максимальная температура): '))
        measures = FileManager.read_measures()
        for measure in measures:
            if ran1 <= measure.result <= ran2:
                print(measure)
    except ValueError:
        print('Ошибка: Температура должна быть числом')

def sort_measures():
    measures = FileManager.read_measures()
    measures.sort(key=lambda x: x.result)
    FileManager.write_measures(measures)

def exit_program():
    exit()

def menu():
    options = {
        '0': {'name': 'Выход', 'action': exit_program},
        '1': {'name': 'Ввести новое измерение', 'action': input_measure},
        '2': {'name': 'Вывести все измерения', 'action': print_measures},
        '3': {'name': 'Вывести измерения в диапазоне температур', 'action': print_measures_range},
        '4': {'name': 'Отсортировать измерения', 'action': sort_measures},
    }
    while True:
        print('\nМеню:')
        for key in options:
            print(f'{key} - {options[key]["name"]}')
        choice = input('Введите опцию: ')
        item = options.get(choice)
        if item:
            try:
                item['action']()
            except ValueError as error:
                print(f'Ошибка: {error}')
            except Exception as error:
                print(f'Неизвестная ошибка: {error}')
        else:
            print("Неверная опция. Попробуйте снова.")

def main():
    menu()

if __name__ == '__main__':
    main()
