import re

class TempMeasure:
    def __init__(self, date: str, place: str, result: float):
        self.date = date # Дата описывается в формате гггг.мм.дд
        self.place = place
        self.result = result

    def __str__(self):
        return f'{self.date} {self.place} {self.result}'

class FileManager:
    FILENAME = 'values.txt'

    @classmethod
    def read_measures(cls):
        measures = []
        with open(cls.FILENAME, 'r', encoding='utf-8') as f:
            for line in f:
                m = line.strip().split()
                measures.append(TempMeasure(m[0], m[1], float(m[2])))
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

def parse_string(text, pattern):
    parsed_string = re.findall(pattern, text)
    if not parsed_string:
        raise ValueError('Строка введена неверно')
    return parsed_string[0]

def input_measure():
    new_measure = input('Введите новое измерение: ')
    date = parse_string(new_measure, r'\d{4}\.\d{2}\.\d{2}')
    city = parse_string(new_measure, r'"([^"]+)"')
    value = parse_string(new_measure.replace(date, ''), r'-?\d+(?:\.\d+)?')
    FileManager.append_measure(TempMeasure(date, city, float(value)))

def print_measures():
    measures = FileManager.read_measures()
    for measure in measures:
        print(measure)

def print_measures_range(ran1, ran2):
    measures = FileManager.read_measures()
    for measure in measures:
        if ran1 <= measure.result <= ran2:
            print(measure)

def sort_measures():
    measures = FileManager.read_measures()
    measures.sort(key=lambda x: x.result)
    FileManager.write_measures(measures)

def menu():
    while True:
        print("""
        1 - Ввести новое измерение
        2 - Вывести все измерения
        3 - Вывести измерения в диапазоне температур
        4 - Отсортировать измерения
        0 - Выход
        """)
        choice = int(input('Введите опцию: '))
        if choice == 0:
            break
        if choice == 1:
            try:
                input_measure()
            except ValueError as error:
                print(f'Ошибка: {error}')
        if choice == 2:
            print_measures()
        if choice == 3:
            print('Введите границы диапазона температур')
            try:
                ran1 = float(input('  От (минимальная температура): '))
                ran2 = float(input('  До (максимальная температура): '))
                print_measures_range(ran1, ran2)
            except ValueError:
                print('Ошибка: Температура должна быть числом')
        if choice == 4:
            sort_measures()

def main():
    menu()

if __name__ == '__main__':
    main()
