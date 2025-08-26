# -*- coding: utf-8 -*-

# Чтение из файла
from math import sqrt

file = open("input.txt", "r")
data = file.read()
file.close()

#Тест чтения файла
assert data == "19 13 26 16 27 19 23 32 18 18 14 17 21 22 23 24 25 30 31 26"

# Преобразование в int
data_massive = data.split()
massive = []
for i in data_massive:
    massive.append(int(i))

#Тест размера сконвертированного массива
assert len(massive) == len(data_massive)

#Тест конвертации значений
assert massive[0] == 19
assert massive[1] == 13
assert massive[2] == 26
assert massive[3] == 16
assert massive[4] == 27
assert massive[5] == 19
assert massive[6] == 23
assert massive[7] == 32
assert massive[8] == 18
assert massive[9] == 18
assert massive[10] == 14
assert massive[11] == 17
assert massive[12] == 21
assert massive[13] == 22
assert massive[14] == 23
assert massive[15] == 24
assert massive[16] == 25
assert massive[17] == 30
assert massive[18] == 31
assert massive[19] == 26

print("Введённый набор чисел: ", massive)
average = float()  # Среднее
mode = int()  # Мода
median = float()  # Медиана
dispersion = float()  # Дисперсия
standard_deviation = float()  # Стандартное отклонение
asymmetry = float()  # Ассиметрия
excess = float()  # Эксцесс

summ = 0
# Суммирование всех элементов
for i in range(len(massive)):
    summ = summ + massive[i]

# Тест суммирования всех элементов
assert summ == 444

# Вычисление среднего
average = summ / len(massive)

# Тест вычисления среднего
assert average == 22.2

# Сортировка массива
for i in range(len(massive)):
    for j in range(len(massive)):
        if massive[i] < massive[j]:
            buffer = massive[i]
            massive[i] = massive[j]
            massive[j] = buffer

# Проверка сортировки
for i in range(len(massive) - 1):
    assert massive[i] <= massive[i + 1]

# Вычисление моды
mode_numbers_amount = 1
current_numbers_amount = 1
mode = massive[0]
for i in range(len(massive) - 1):

    mode_current = massive[i]

    if mode_current == massive[i + 1]:
        current_numbers_amount = current_numbers_amount + 1
    else:
        current_numbers_amount = 1

    if current_numbers_amount > mode_numbers_amount:
        mode = mode_current
        mode_numbers_amount = current_numbers_amount

# Проверка моды
assert mode == 18

# Вычисление медианы
median = (massive[int(len(massive) / 2)] + massive[int((len(massive) / 2) + 1)]) / 2

# Проверка медианы
assert median == 23.0

# Вычисление суммируемой части дисперсии
dispersion_summ = 0
for i in massive:
    dispersion_summ = dispersion_summ + ((i - average) * (i - average))

# Проверка суммируемой части дисперсии
assert dispersion_summ == 573.2

# Вычисление дисперсии
dispersion = dispersion_summ / len(massive)

# Проверка дисперсии
assert dispersion == 28.66

# Вычисление стандартного отклонения
standard_deviation = sqrt(dispersion_summ / len(massive))
# Вычисление суммируемой части ассиметрии
asymmetry_summ = 0
for i in massive:
    asymmetry_summ = asymmetry_summ + ((i - average) * (i - average) * (i - average))

asymmetry_summ = asymmetry_summ / len(massive)
# Вычисление ассиметрии
asymmetry = asymmetry_summ / (standard_deviation * standard_deviation * standard_deviation)
# Вычисление суммируемой части эксцесса
excess_summ = 0
for i in massive:
    excess_summ = excess_summ + ((i - average) * (i - average) * (i - average) * (i - average))

excess_summ = excess_summ / len(massive)
# Вычисление эксцесса
excess = (excess_summ / (standard_deviation * standard_deviation * standard_deviation * standard_deviation)) - 3

# Вывод на консоль
print("Среднее = ", average)
print("Мода = ", mode)
print("Медиана = ", median)
print("Дисперсия = ", dispersion)
print("Стандартное отклонение = ", standard_deviation)
print("Ассиметрия = ", asymmetry)
print("Эксцесс = ", excess)
# Вывод в файл
file = open("output.txt", "w")
file.write("Среднее = " + str(average) + "\n")
file.write("Мода = " + str(mode) + "\n")
file.write("Медиана = " + str(median) + "\n")
file.write("Дисперсия = " + str(dispersion) + "\n")
file.write("Стандартное отклонение = " + str(standard_deviation) + "\n")
file.write("Ассиметрия = " + str(asymmetry) + "\n")
file.write("Эксцесс = " + str(excess) + "\n")
file.close()
