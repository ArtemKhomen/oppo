import unittest, tempfile, os
from PO import TempMeasure, FileManager, parse_string, print_measures, print_measures_range, sort_measures

class TestTempMeasure(unittest.TestCase):
    def test_temp_measure_creation(self):
        measure = TempMeasure('2025.01.01', 'Красноярск', 25.5)
        self.assertEqual(measure.date, '2025.01.01')
        self.assertEqual(measure.place, 'Красноярск')
        self.assertEqual(measure.result, 25.5)

    def test_temp_measure_str(self):
        measure = TempMeasure('2025.01.01', 'Красноярск', 25.5)
        expected_str = '2025.01.01 Красноярск 25.5'
        self.assertEqual(str(measure), expected_str)

class TestParseString(unittest.TestCase):
    def test_date(self):
        result = parse_string('2005.08.24 "Nazarovo" -50.6', r'\d{4}\.\d{2}\.\d{2}')
        self.assertEqual(result, '2005.08.24')
    def test_city(self):
        result = parse_string('"Moscow" 2025.05.09 10.5', r'"([^"]+)"')
        self.assertEqual(result, 'Moscow')
    def test_value(self):
        result = parse_string('23 2020.01.01 "Irkutsk"', r'-?\d+(?:\.\d+)?')
        self.assertEqual(result, '23')

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
        m1 = TempMeasure('2025.01.01', 'A', 10.0)
        m2 = TempMeasure('2025.01.02', 'B', -5.0)
        FileManager.write_measures([m1, m2])
        loaded = FileManager.read_measures()
        self.assertEqual(len(loaded), 2)
        self.assertEqual(loaded[0].place, 'A')
        self.assertEqual(loaded[1].result, -5.0)

    def test_append(self):
        FileManager.write_measures([])
        m = TempMeasure('2025.01.03', 'C', 0.0)
        FileManager.append_measure(m)
        loaded = FileManager.read_measures()
        self.assertEqual(len(loaded), 1)
        self.assertEqual(loaded[0].date, '2025.01.03')

    def tearDown(self):
        FileManager.FILENAME = self.original_filename

class TestSort(unittest.TestCase):
    def setUp(self):
        self.temp_file = tempfile.NamedTemporaryFile(delete=False, mode='w', encoding='utf-8')
        self.temp_file.close()
        self.original_filename = FileManager.FILENAME
        FileManager.FILENAME = self.temp_file.name

    def test_sort(self):
        m1 = TempMeasure('2025.01.01', 'A', 30.0)
        m2 = TempMeasure('2025.01.02', 'B', 10.0)
        FileManager.write_measures([m1, m2])

        sort_measures()

        loaded = FileManager.read_measures()
        self.assertEqual(loaded[0].result, 10.0)
        self.assertEqual(loaded[1].result, 30.0)

    def tearDown(self):
        FileManager.FILENAME = self.original_filename

if __name__ == '__main__':
    unittest.main()