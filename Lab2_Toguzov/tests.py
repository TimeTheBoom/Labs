import unittest

import utils


# Класс для проверки работы с файлами
class GetDataTest(unittest.TestCase):
    # Проверить чтение целочисленных данных
    def test_integer(self):
        # Подготовка
        filename = "test integer.txt"
        # Действие
        data_array, time = utils.get_data(filename)
        # Проверка
        self.assertEqual(time[0], 0)
        self.assertEqual(time[1], 1)
        self.assertEqual(data_array[0][0], 1)
        self.assertEqual(data_array[0][1], 2)
        self.assertEqual(data_array[1][0], 10)
        self.assertEqual(data_array[1][1], 20)
        self.assertEqual(data_array[2][0], -100)
        self.assertEqual(data_array[2][1], -200)

    # Проверить чтение вещественных данных
    def test_float(self):
        # Подготовка
        filename = "test float.txt"
        # Действие
        data_array, time = utils.get_data(filename)
        # Проверка
        self.assertEqual(time[0], 0.1)
        self.assertEqual(time[1], 0.2)
        self.assertEqual(data_array[0][0], -0.001)
        self.assertEqual(data_array[0][1], -0.002)
        self.assertEqual(data_array[1][0], 0.1)
        self.assertEqual(data_array[1][1], 0.2)
        self.assertEqual(data_array[2][0], 1.2)
        self.assertEqual(data_array[2][1], -9.55)

    # Проверить чтение на реальном примере
    def test_real(self):
        # Подготовка
        filename = "test real.txt"
        # Действие
        data_array, time = utils.get_data(filename)
        # Проверка
        self.assertEqual(time[0], 0.0000)
        self.assertEqual(time[1], 0.0001)
        self.assertEqual(data_array[0][0], -0.0037)
        self.assertEqual(data_array[0][1], 0.0009)
        self.assertEqual(data_array[1][0], -0.0041)
        self.assertEqual(data_array[1][1], 0.0013)
        self.assertEqual(data_array[2][0], 0.0022)
        self.assertEqual(data_array[2][1], -0.0022)

# Класс для проверки обрезания данных
class GetLocalData(unittest.TestCase):
    # Проверить обрезание данных в нормальном случае
    def test_smaller(self):
        # Подготовка
        data_array = [[0.1, 0.2, 0.3, 0.4, 0.5],[1, 2, 3, 4, 5],[10, 20, 30, 40, 50]]
        time = [0.0000, 0.0001, 0.0002, 0.0003, 0.0004]
        # Действие
        data_array[0], time = utils.get_local_data(data_array[0], time, 0.0002 , 2)
        time = [0.0000, 0.0001, 0.0002, 0.0003, 0.0004]
        data_array[1], time = utils.get_local_data(data_array[1], time, 0.0002, 2)
        time = [0.0000, 0.0001, 0.0002, 0.0003, 0.0004]
        data_array[2], time = utils.get_local_data(data_array[2], time, 0.0002, 2)
        # Проверка
        self.assertEqual(data_array[0][0], 0.2)
        self.assertEqual(data_array[0][1], 0.3)
        self.assertEqual(data_array[1][0], 2)
        self.assertEqual(data_array[1][1], 3)
        self.assertEqual(data_array[2][0], 20)
        self.assertEqual(data_array[2][1], 30)
        self.assertEqual(time[0], 0.0001)
        self.assertEqual(time[1], 0.0002)

    # Проверить обрезание данных в случае выхода за границы массива
    def test_out_of_range(self):
        # Подготовка
        data_array = [[0.1],[1],[10]]
        time = [0.0000]
        # Действие
        data_array[0], time = utils.get_local_data(data_array[0], time, 10 , 100)
        time = [0.0000]
        data_array[1], time = utils.get_local_data(data_array[1], time, 10, 100)
        time = [0.0000]
        data_array[2], time = utils.get_local_data(data_array[2], time, 10, 100)
        # Проверка
        self.assertEqual(data_array[0][0], 0.1)
        self.assertEqual(data_array[1][0], 1)
        self.assertEqual(data_array[2][0], 10)
        self.assertEqual(time[0], 0.0)

    # Проверить обрезание данных в случае выхода за границы времени
    def test_out_of_time(self):
        # Подготовка
        data_array = [[0.1, 0.2, 0.3, 0.4, 0.5],[1, 2, 3, 4, 5],[10, 20, 30, 40, 50]]
        time = [0.0000, 0.0001, 0.0002, 0.0003, 0.0004]
        # Действие
        data_array[0], time = utils.get_local_data(data_array[0], time, -0.0003 , 3)
        time = [0.0000, 0.0001, 0.0002, 0.0003, 0.0004]
        data_array[1], time = utils.get_local_data(data_array[1], time, -0.0003, 3)
        time = [0.0000, 0.0001, 0.0002, 0.0003, 0.0004]
        data_array[2], time = utils.get_local_data(data_array[2], time, -0.0003, 3)
        # Проверка
        self.assertEqual(data_array[0][0], 0.1)
        self.assertEqual(data_array[0][1], 0.2)
        self.assertEqual(data_array[0][2], 0.3)
        self.assertEqual(data_array[1][0], 1)
        self.assertEqual(data_array[1][1], 2)
        self.assertEqual(data_array[1][2], 3)
        self.assertEqual(data_array[2][0], 10)
        self.assertEqual(data_array[2][1], 20)
        self.assertEqual(data_array[2][2], 30)
        self.assertEqual(time[0], 0.0)
        self.assertEqual(time[1], 0.0001)
        self.assertEqual(time[2], 0.0002)

    # Проверить обрезание данных в случае выхода за количество точек измерения
    def test_out_of_points(self):
        # Подготовка
        data_array = [[0.1, 0.2, 0.3, 0.4, 0.5], [1, 2, 3, 4, 5], [10, 20, 30, 40, 50]]
        time = [0.0000, 0.0001, 0.0002, 0.0003, 0.0004]
        # Действие
        data_array[0], time = utils.get_local_data(data_array[0], time, 0.0004, 30)
        time = [0.0000, 0.0001, 0.0002, 0.0003, 0.0004]
        data_array[1], time = utils.get_local_data(data_array[1], time, 0.0004, 30)
        time = [0.0000, 0.0001, 0.0002, 0.0003, 0.0004]
        data_array[2], time = utils.get_local_data(data_array[2], time, 0.0004, 30)
        # Проверка
        self.assertEqual(data_array[0][0], 0.4)
        self.assertEqual(data_array[0][1], 0.5)
        self.assertEqual(data_array[1][0], 4)
        self.assertEqual(data_array[1][1], 5)
        self.assertEqual(data_array[2][0], 40)
        self.assertEqual(data_array[2][1], 50)
        self.assertEqual(time[0], 0.0003)
        self.assertEqual(time[1], 0.0004)

# Класс для проверки преобразования фурье
class TestGetFFTData(unittest.TestCase):
    # Проверить преобразование фурье
    def test_normal(self):
        # Подготовка
        data_array = [[0.1, 0.2, 0.3, 0.4, 0.5, 0.1, 0.2, 0.3, 0.4, 0.5], [1, 2, 3, 4, 5, 1, 2, 3, 4, 5], [10, 20, 30, 40, 50, 10, 20, 30, 40, 50]]
        time = [0.0000, 0.0001]
        # Действие
        data_array[0], freq = utils.get_fft_data(data_array[0], time[1] - time[0])
        data_array[1], freq = utils.get_fft_data(data_array[1], time[1] - time[0])
        data_array[2], freq = utils.get_fft_data(data_array[2], time[1] - time[0])
        # Проверка
        self.assertEqual(data_array[0][0], 3.)
        self.assertEqual(data_array[0][1], 0.)
        self.assertEqual(data_array[1][0], 30.)
        self.assertEqual(data_array[1][1], 0.)
        self.assertEqual(data_array[2][0], 300.)
        self.assertEqual(data_array[2][1], 0.)
        self.assertEqual(freq[0], 0.)
        self.assertEqual(freq[1], 1000.)

# Класс для проверки поиска сигнала
class TestFindSignal(unittest.TestCase):
    # Проверить поиск сигнала при размерах сигнала меньше 1000
    def test_small(self):
        # Подготовка
        data_array = [[0.1, 0.2, 0.3], [1, 2, 3], [10, 20, 30]]
        time = [0.0000, 0.0001, 0.0002]
        # Действие
        data_array[0], time = utils.find_signal(data_array[0], time, False)
        data_array[1], time = utils.find_signal(data_array[1], time, True)
        data_array[2], time = utils.find_signal(data_array[2], time, True)
        # Проверка
        self.assertEqual(time[0], 0.0)
        self.assertEqual(time[1], 0.0001)
        self.assertEqual(time[2], 0.0002)
        self.assertEqual(data_array[0][0], 0.1)
        self.assertEqual(data_array[0][1], 0.2)
        self.assertEqual(data_array[0][2], 0.3)
        self.assertEqual(data_array[1][0], 1)
        self.assertEqual(data_array[1][1], 2)
        self.assertEqual(data_array[1][2], 3)
        self.assertEqual(data_array[2][0], 10)
        self.assertEqual(data_array[2][1], 20)
        self.assertEqual(data_array[2][2], 30)

    # Проверить поиск сигнала при размерах сигнала больше 1000
    def test_big(self):
        # Подготовка
        data_array = [[],[],[]]
        time = []
        for i in range(0, 1300):
            data_array[0].append(i / 10)
            data_array[1].append(i)
            data_array[2].append(i * 10)
            time.append(i / 10000)
        for i in range(0, 700):
            time.append(i / 10000)
        for i in range(700, 0, -1):
            data_array[0].append(i / 10)
            data_array[1].append(i)
            data_array[2].append(i * 10)
        # Действие
        data_array[0], time = utils.find_signal(data_array[0], time, False)
        data_array[1], time = utils.find_signal(data_array[1], time, True)
        data_array[2], time = utils.find_signal(data_array[2], time, True)
        # Проверка
        self.assertEqual(data_array[0][0], 79.9)
        self.assertEqual(data_array[1][0], 799.0)
        self.assertEqual(data_array[2][0], 7990.0)
        self.assertEqual(data_array[0][len(data_array)], 80.2)
        self.assertEqual(data_array[1][len(data_array)], 802.0)
        self.assertEqual(data_array[2][len(data_array)], 8020.0)
        self.assertEqual(time[0], 0.0799)
        self.assertEqual(time[len(time) - 1], 0.0498)
if __name__ == '__main__':
    unittest.main()

