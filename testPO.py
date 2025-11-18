import unittest, tempfile, os
from datetime import datetime
from PO import (TempMeasure, FileManager, parse_string, print_measures, print_measures_range, sort_measures,
                place_pattern, date_pattern, value_pattern)

class TestTempMeasure(unittest.TestCase):
    def setUp(self):
        self.valid_input = '2025.10.10 "Красноярск" 35'
        self.valid_measure = TempMeasure.from_string(self.valid_input)

    def test_from_string_creates_correct_object(self):
        self.assertEqual(self.valid_measure.date, datetime(2025, 10, 10))
        self.assertEqual(self.valid_measure.place, 'Красноярск')
        self.assertEqual(self.valid_measure.result, 35.0)

    def test_str_method(self):
        expected = '2025.10.10 Красноярск 35.0'
        self.assertEqual(str(self.valid_measure), expected)

    def test_invalid_inputs(self):
        # Неверный ввод
        invalid_input = 'a b c'
        with self.assertRaises(ValueError):
            TempMeasure.from_string(invalid_input)

        # Неверный формат даты
        invalid_date = '2025/10/10 "Красноярск" 35'
        with self.assertRaises(ValueError) as context:
            TempMeasure.from_string(invalid_date)
        self.assertIn('Не найдено значение', str(context.exception))

        # Несуществующая дата
        nonexist_date = '2025.02.29 "Красноярск" 30'
        with self.assertRaises(ValueError) as context:
            TempMeasure.from_string(nonexist_date)
        self.assertIn('Неверный формат даты', str(context.exception))

        # Неверный формат температуры
        invalid_temp1 = '2025.10.10 "Красноярск" тридцать-пять'
        with self.assertRaises(ValueError) as context:
            TempMeasure.from_string(invalid_temp1)
        self.assertIn('Не найдено значение', str(context.exception))

        # Неверный формат температуры
        invalid_temp2 = '2025.10.10 "Красноярск" 35a'
        with self.assertRaises(ValueError) as context:
            TempMeasure.from_string(invalid_temp2)
        self.assertIn('Не найдено значение', str(context.exception))

        # Слишком высокая температура
        high_temp = '2025.10.10 "Красноярск" 101.0'
        with self.assertRaises(ValueError) as context:
            TempMeasure.from_string(high_temp)
        self.assertIn('вне реалистичного диапазона', str(context.exception))

    def test_edge_cases(self):
        # Минимальная допустимая температура
        min_temp = TempMeasure.from_string('2025.10.10 "Якутия" -100.0')
        self.assertEqual(min_temp.result, -100.0)

        # Максимальная допустимая температура
        max_temp = TempMeasure.from_string('2025.10.10 "Сочи" 100.0')
        self.assertEqual(max_temp.result, 100.0)

        # Минимальный год
        min_year = TempMeasure.from_string('1900.01.01 "Бангкок" 0.0')
        self.assertEqual(min_year.date.year, 1900)

        # Максимальный (текущй) год
        current_year = datetime.now().year
        max_year_str = f'{current_year}.12.31 "назарово" 0.0'
        max_year_measure = TempMeasure.from_string(max_year_str)
        self.assertEqual(max_year_measure.date.year, current_year)


class TestParseString(unittest.TestCase):
    def test_parse_date(self):
        text = '2023.12.15 "Красноярск1111" 25.5'
        result = parse_string(text, date_pattern)
        self.assertEqual(result, "2023.12.15")

    def test_parse_place(self):
        text = '2023.12.15 "12345Красноярск" 25.5'
        result = parse_string(text, place_pattern)
        self.assertEqual(result, "12345Красноярск")

    def test_parse_temperature(self):
        text = '2023.12.15 "Красноярск54321" 25.5'
        result = parse_string(text, value_pattern)
        self.assertEqual(result, "25.5")

    def test_parse_negative_temperature(self):
        text = '2023.12.15 "Красноярск" -25.5'
        result = parse_string(text, value_pattern)
        self.assertEqual(result, "-25.5")

    def test_parse_not_found(self):
        text = '2023.12.15 "Красноярск"'
        with self.assertRaises(ValueError) as context:
            parse_string(text, value_pattern)
        self.assertIn('Не найдено значение', str(context.exception))

class TestFileManager(unittest.TestCase):
    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, mode='w', encoding='utf-8')
        self.temp_file.close()
        self.original_filename = FileManager.FILENAME
        FileManager.FILENAME = self.temp_file.name

    def test_read_empty_file(self):
        FileManager.write_measures([])
        loaded = FileManager.read_measures()
        self.assertEqual(loaded, [])

    def test_write_and_read(self):
        m1 = TempMeasure(datetime(2025, 1, 1), 'A', 10.0)
        m2 = TempMeasure(datetime(2025, 1, 2), 'B', -5.0)
        FileManager.write_measures([m1, m2])
        loaded = FileManager.read_measures()
        self.assertEqual(len(loaded), 2)
        self.assertEqual(loaded[0].place, 'A')
        self.assertEqual(loaded[1].result, -5.0)

    def test_append(self):
        FileManager.write_measures([])
        date = datetime(2025, 1, 3)
        m = TempMeasure(date, 'C', 0.0)
        FileManager.append_measure(m)
        loaded = FileManager.read_measures()
        self.assertEqual(len(loaded), 1)
        self.assertEqual(loaded[0].date, date)

    def tearDown(self):
        FileManager.FILENAME = self.original_filename

class TestSort(unittest.TestCase):
    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, mode='w', encoding='utf-8')
        self.temp_file.close()
        self.original_filename = FileManager.FILENAME
        FileManager.FILENAME = self.temp_file.name

    def test_sort(self):
        m1 = TempMeasure(datetime(2025, 1, 1), 'A', 30.0)
        m2 = TempMeasure(datetime(2025, 1, 2), 'B', 10.0)
        m3 = TempMeasure(datetime(2025, 1, 2), 'C', -10.0)
        FileManager.write_measures([m1, m2, m3])

        sort_measures()

        loaded = FileManager.read_measures()
        self.assertEqual(loaded[0].result, -10.0)
        self.assertEqual(loaded[1].result, 10.0)
        self.assertEqual(loaded[2].result, 30.0)

    def tearDown(self):
        FileManager.FILENAME = self.original_filename

if __name__ == '__main__':
    unittest.main()