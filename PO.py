import re

class TempMeasure:
    def __init__(self, date: str, place: str, result: float):
        self.date = date # Дата описывается в формате гггг.мм.дд
        self.place = place
        self.result = result

    def __str__(self):
        return f'{self.date} {self.place} {self.result}'

    def write_file(self):
        f = open('values.txt', 'a', encoding="utf8")
        f.write(f'{self.date} {self.place} {self.result}\n')
        f.close()

def parse_string(text):
    city_pattern = r'"([^"]+)"'
    city = re.findall(city_pattern, text)
    text = text.replace(city[0], "")

    date_pattern = r'\d{4}\.\d{2}\.\d{2}'
    date = re.findall(date_pattern, text)
    text = text.replace(date[0], "")

    value_pattern = r'-?\d+(?:\.\d+)?'
    value = re.findall(value_pattern, text)
    return date[0], city[0], float(value[0])

def get_values_arr():
    f = open('values.txt', 'r', encoding="utf8")
    measures = []
    for m in f.readlines():
        m = m.split()
        measure = TempMeasure(m[0], m[1], float(m[2]))
        measures.append(measure)
    f.close()
    return measures

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
            f = open('values.txt', 'a', encoding="utf8")
            new_measure = input('Введите новое измерение: ')
            date, city, value = parse_string(new_measure)
            measure = TempMeasure(date, city, value)
            measure.write_file()
            f.close()
        if choice == 2:
            f = open('values.txt', encoding="utf8")
            print(f.read())
            f.close()
        if choice == 3:
            ran1 = float(input("Введите левую границу диапазона: "))
            ran2 = float(input("Введите вторую границу диапазона: "))
            measures = get_values_arr()
            for measure in measures:
                if ran1 <= measure.result <= ran2:
                    print(measure)
        if choice == 4:
            measures = get_values_arr()
            l = len(measures)
            for i in range(l):
                for j in range(l-i-1):
                    if measures[j].result > measures[j+1].result:
                        temp = measures[j]
                        measures[j] = measures[j+1]
                        measures[j+1] = temp
            f = open('values.txt', 'w')
            f.close()
            for measure in measures:
                measure.write_file()

def main():
    menu()

if __name__ == '__main__':
    main()
