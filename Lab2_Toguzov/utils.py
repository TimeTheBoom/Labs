import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from datetime import datetime
import math

## @package utils
# @brief Данный модуль содержит в себе вспомогательные функци


## @brief Класс для фильтрации шума
# @param data Исходные данные
# @retval data Отфильтрованые данные
def internal_filter(data):
    filter_val = 3.0

    data = np.array(data)
    data[(data >= filter_val) | (data <= -filter_val)] = 0

    return data.tolist()

## @brief Класс для чтения данных
#
# @param filename Имя файла с данными
# @retval data_array Массив c 3 потоками данных
# @retval time Время соответствующее данным
#
# Класс читает данные из файла с заданным названием
#
# Читаемые данные являются .txt файлами
#
# Из файла извлекается время и 3 потока данных
def get_data(filename):
    # Открыть файл
    with open(filename, "r") as file:
        lines = file.readlines()

    # Пропустить линии с мета-данными
    data_lines = lines[20:]

    time = []
    first_channel = []
    second_channel = []
    third_channel = []

    # Чтение данных с файла
    for line in data_lines:
        values = line.split()

        # Преобразование данных
        if len(values) == 4:
            time.append(float(values[0]))
            first_channel.append(float(values[1]))
            second_channel.append(float(values[2]))
            third_channel.append(float(values[3]))

    # Итоговая форма данных
    data_array = [first_channel, second_channel, third_channel]

    return data_array, time

## @brief Класс для обрезания данных
#
# @param data Входные данные
# @param time Время соответствующее данным
# @param start_time Время начала
# @param point Количество точек измерения
#
# @retval data Обрезанные данные
# @retval time Обрезанное время соответствующее данным
#
# Данный класс получает на вход данные и вырезает из них сегмент задающийся параметрами
def get_local_data(data, time, start_time, points):
    # Найти индекс соответствующего времени
    start_index = 0
    for index, el in enumerate(time):
        if el >= start_time:
            start_index = index - 1
            break

    # Вырезать точки вне времени
    if start_index >= 0:
        data = data[start_index:]
        time = time[start_index:]

    # Вырезать точки вне точек
    if len(time) >= points:
        data = data[:points]
        time = time[:points]

    return data, time

## @brief Класс для преобразования фурье
#
# @param data Входные данные
# @param step Шаг между измерениями
#
# @retval data Преобразованный сигнал
# @retval freq Разброс частот между преобразованным сигналом
#
# Данный класс получает на вход данные и применяет на них быстрое преобразование фурье
def get_fft_data(data, step):
    fft_data = np.abs(np.fft.fft(data))
    freq = np.fft.fftfreq(len(fft_data), step)

    # Удалить фурье слева
    freq = freq[freq >= 0]
    fft_data = fft_data[: len(freq)]

    # Удалить высокочастотное фурье
    freq = freq[: int(len(freq) / 2)]
    fft_data = fft_data[: len(freq)]

    return fft_data, freq

## @brief Класс для вывода графика
#
# @param freq Координата x
# @param amplitude Координата y
# @param subplot Количество графиков на выводе
# @param channel Номер выводимого графика
#
# @return Выводит на экран график
#
# Данный класс выводит на экран график
#
# На 1 окне можно выводить несколько графиков
def make_plot(freq, amplitude, subplot, channel):
    plt.subplot(subplot)
    plt.plot(freq, amplitude)
    plt.title(f"Channel {channel}")
    plt.xlabel("Frequency (Hz)")
    plt.ylabel("Magnitude")

## @brief Класс для сохранения преобразования фурье
#
# @param filename Имя файла с данными
# @param start_time Время начала
# @param points Количество точек
#
# @return Сохраняет на диск excel файл
#
# Данный класс получает на вход данные, выполняет преобразование фурье и сохраняет данные в excel файл
def save_local_fourier(filename, start_time, points):
    data, time = get_data(filename)
    ex_data = {}
    old_time = time
    # Получить локальный сигнал
    for channel in range(len(data)):
        time = old_time
        data[channel], time = get_local_data(data[channel], time, start_time, points)

        if (len(time) < points) or (len(time) < 2):
            return

        data[channel] = internal_filter(data[channel])

        data[channel], freq = get_fft_data(data[channel], time[1] - time[0])
        for index, el in enumerate(data[channel]):
            data[channel][index] = round(el, 4)

        ex_data.update({"Frequency (Hz)": freq})
        ex_data.update({f"Channel {channel}": data[channel]})

    # Преобразовать в excel
    df = pd.DataFrame(ex_data)
    excel_filename = (
        f"{filename.split('.')[0]}_"
        f"{start_time.__str__().split('.')[0]}_"
        f"{start_time.__str__().split('.')[1]}s_"
        f"{points}_{datetime.now().strftime('%H_%M_%S')}.xlsx"
    )

    df.to_excel(excel_filename, index=False)
    print(f"Saved as {excel_filename}")

## @brief Класс для отображения сегмента данных
#
# @param filename Имя файла с данными
# @param start_time Время начала
# @param point Количество точек измерения
#
# @return Выводит график на экран
#
# Данный класс получает на вход данные, вырезает из них сегмент и выводит его на экран
def show_local_signal(filename, start_time, points):
    data, time = get_data(filename)
    old_time = time
    current_integral = 0
    plt.figure(figsize=(10.8, 7.2))

    # Получить локальный сигнал
    for i in range(len(data) - 1):
        time = old_time
        data[i], time = get_local_data(data[i], time, start_time, points)

        if len(time) < points:
            return

        data[i] = internal_filter(data[i])

        # Подготовить графики
        data[i] = internal_filter(data[i])  # Фильтр сигнала
        make_plot(time, data[i], 411 + i * 2, i + 1)

        # Интеграл
        for j in range(len(data[i])):
            current_integral += (data[i][j] * -1)
            data[i][j] = current_integral

        constant_change = data[i][len(data[i]) - 1] / len(data[i])
        for j in range(len(data[i])):
            data[i][j] = data[i][j] - constant_change * j
        make_plot(time, data[i], 411 + i * 2 + 1, i + 1)
        current_integral = 0

    # Отобразить графики
    plt.tight_layout()
    plt.show()

## @brief Класс для отображения преобразования фурье
#
# @param filename Имя файла с данными
# @param start_time Время начала
# @param points Количество точек
#
# @return Сохраняет на диск excel файл
#
# Данный класс получает на вход данные, выполняет преобразование фурье и отображает данные в виде графика
def show_local_fourier(filename, start_time, points):
    data, time = get_data(filename)
    old_time = time
    plt.figure(figsize=(10.8, 7.2))

    # Получить локальный сигнал
    for channel in range(len(data)):
        time = old_time
        data[channel], time = get_local_data(data[channel], time, start_time, points)

        if (len(time) < points) or (len(time) < 2):
            return

        data[channel] = internal_filter(data[channel])

        fft_channel, freq = get_fft_data(data[channel], time[1] - time[0])
        make_plot(freq, fft_channel, 311 + channel, channel + 1)

    # Отобразить графики
    plt.tight_layout()
    plt.show()

## @brief Класс для отображения данных полностью
#
# @param filename Имя файла с данными
#
# @return Выводит график на экран
#
# Данный класс получает на вход данные и выводит на экран график
def show_full_signal(filename):
    # Получить сигнал
    current_integral = 0
    data, time = get_data(filename)
    plt.figure(figsize=(10.8, 7.2))

    # Подготовить графики
    for i in range(len(data) - 1):
        data[i] = internal_filter(data[i])  # Фильтр сигнала
        make_plot(time, data[i], 411 + i * 2, i + 1)

        #integral
        for j in range(len(data[i])):
            current_integral += (data[i][j] * -1)
            data[i][j] = current_integral

        constant_change = data[i][len(data[i]) - 1] / len(data[i])
        for j in range(len(data[i])):
            data[i][j] = data[i][j] - constant_change * j
        make_plot(time, data[i], 411 + i * 2 + 1, i + 1)
        current_integral = 0

    # Отобразить графики
    plt.tight_layout()
    plt.show()

## @brief Класс для поиска сигнала
#
# @param data Входные данные
# @param time Время соответствующее данным
# @param time_edited Был ли массив с временем уже отредактирован функцией
#
# @retval data Преобразованные данные
# @retval time Преобразованное время соответствующее данным
#
# Класс находит пик сигнала и возвращает 1000 точек с пиком в центре
def find_signal(data, time, time_edited):
    max_value = -2147483648
    max_value_index = 0
    # Найти максимальное значение
    for i in range(len(data)):
        if data[i] > max_value:
            max_value = data[i]
            max_value_index = i

    # Получить сигнал
    data = data[(max_value_index - 500):(max_value_index + 500)]
    if not time_edited:
        time = time[(max_value_index - 500):(max_value_index + 500)]
    return data, time

## @brief Класс для вывода найденного сигнала
#
# @param filename Имя файла с данными
#
# @returns Выводит график на экран
#
# Данный класс получает на вход данные, находит в них сигнал с помощью функции find_data и выводит на экран график
def show_found_signal(filename):
    data, time = get_data(filename)
    time_edited = False
    plt.figure(figsize=(10.8, 7.2))
    current_integral = 0

    for i in range(len(data) - 1):

        data[i], time = find_signal(data[i], time, time_edited)
        time_edited = True

        # make channels plot
        data[i] = internal_filter(data[i])  # signal filter
        make_plot(time, data[i], 411 + i * 2, i + 1)

        # integral
        for j in range(len(data[i])):
            current_integral += (data[i][j] * -1)
            data[i][j] = current_integral

        constant_change = data[i][len(data[i]) - 1] / len(data[i])
        for j in range(len(data[i])):
            data[i][j] = data[i][j] - constant_change * j

        make_plot(time, data[i], 411 + i * 2 + 1, i + 1)
        current_integral = 0

    # Отобразить графики
    plt.tight_layout()
    plt.show()

## @brief Класс для сохранения среднего преобразования фурье
#
# @param filename Имя файла с данными
# @param merge Размер группы объеденённых сигналов
# @param is_split Был ли сигнал уже разделён (Если да - то не искать в нём данные)
#
# @retval data Обрезанные данные
# @retval time Обрезанное время соответствующее данным
#
# Данный класс получает на вход данные и вырезает из них сегмент задающийся параметрами
def save_average_fourier(filenames, merge, is_split):
    output_size = 71
    average_fourier = [[0] * output_size] + [[0] * output_size]
    merge_fourier = [[0] * output_size] + [[0] * output_size]
    merge_iterator = 0
    dispersion = [[0] * output_size] + [[0] * output_size]
    deviation = [[0] * output_size] + [[0] * output_size]
    ex_data = {}
    freq_updated = False
    # Чтение
    for i in range(len(filenames)):
        data, time = get_data(filenames[i])
        time_edited = False
        # Преобразование фурье
        for j in range(len(data) - 1):
            if not is_split:
                data[j], time = find_signal(data[j], time, time_edited)
                time_edited = True

            data[j] = internal_filter(data[j])
            data[j], freq = get_fft_data(data[j], time[1] - time[0])
            data[j] = data[j][:output_size]
            freq = freq[:output_size]
            # Вывод частот в excel
            if not freq_updated:
                ex_data.update({"Freq(Hz)": freq})
                freq_updated = True

        # Вычислить среднее фурье
        for j in range(len(data) - 1):
            for k in range(len(data[j])):
                average_fourier[j][k] += data[j][k]
                # Merge fourier
                merge_fourier[j][k] += data[j][k]

        merge_iterator += 1
        # Вывести фурье в excel
        # Объединить фурье
        if merge_iterator >= merge:
            for j in range(len(data) - 1):
                for k in range(len(merge_fourier[j])):
                    merge_fourier[j][k] = merge_fourier[j][k] / merge

                ex_data.update({f"Ex{i + 1} Ch{j + 1}": merge_fourier[j]})
            ex_data.update({f"{i}":None})
            merge_iterator = 0
            merge_fourier = [[0] * output_size] + [[0] * output_size]

    if merge_iterator < merge and merge_iterator != 0:
        for i in range(len(merge_fourier)):
            for j in range(len(merge_fourier[i])):
                merge_fourier[i][j] = merge_fourier[i][j] / merge_iterator

            ex_data.update({f"Ex{len(filenames)} Ch{i + 1}": merge_fourier[i]})
        ex_data.update({f"{len(filenames)}": None})
    # Вычислить среднее фурье
    for i in range(len(average_fourier)):
        for j in range(len(average_fourier[i])):
            average_fourier[i][j] = average_fourier[i][j] / len(filenames)

    # Вычислить дисперсию
    # Чтение
    for i in range(len(filenames)):
        data, time = get_data(filenames[i])
        time_edited = False
        # Преобразование фурье
        for j in range(len(data) - 1):
            if not is_split:
                data[j], time = find_signal(data[j], time, time_edited)
                time_edited = True
            data[j] = internal_filter(data[j])
            data[j], freq = get_fft_data(data[j], time[1] - time[0])
            data[j] = data[j][:output_size]
            # Дисперсия
            for k in range(len(data[j])):
                dispersion[j][k] += (data[j][k] - average_fourier[j][k]) * (data[j][k] - average_fourier[j][k])

    for i in range(len(dispersion)):
        for j in range(len(dispersion[i])):
            dispersion[i][j] = dispersion[i][j] / len(filenames)
    # Вычислить стандартное отклонение
    for i in range(len(deviation)):
        for j in range(len(deviation[i])):
            deviation[i][j] = math.sqrt(dispersion[i][j])
    # Вывести среднее фурье в excel
    for i in range(len(average_fourier)):
        ex_data.update({f"Aver ch{i + 1}": average_fourier[i]})

    ex_data.update({f"{len(filenames) + 1}": None})
    # Вывести дисперсию в excel
    for i in range(len(dispersion)):
        ex_data.update({f"Disp ch{i + 1}": dispersion[i]})

    ex_data.update({f"{len(filenames) + 2}": None})
    # Вывести отклонение в excel
    for i in range(len(deviation)):
        ex_data.update({f"Devia ch{i + 1}": deviation[i]})
    # Преобразовать в excel
    df = pd.DataFrame(ex_data)
    # Имя файла
    file_start_name = filenames[0].split('.')[0]
    file_end_name = filenames[len(filenames) - 1].split('/')
    file_end_name[len(file_end_name) - 1] = file_end_name[len(file_end_name) - 1].split('.')[0]
    excel_filename = file_start_name + '-' + file_end_name[len(file_end_name) - 1] + ' Average Fourier.xlsx'
    # Сохранение
    df.to_excel(excel_filename, index=False)
    print(f"Saved as {excel_filename}")

## @brief Класс для поиска начала и конца сигнала
#
# @param filenames Имя файлов с данными
#
# Данный класс получает на вход данные, находит в них начало и конец сигнала
#
# Преобразованный сигнал передаётся в функцию save_data_fragments для разделения и сохранения в файл
def separate_signals(filenames):
    # Чтение
    for i in range(len(filenames)):
        data, time = get_data(filenames[i])
        start_index = 0
        end_index = 0

        iterator = 0
        end = False
        # Поиск начала
        while not end:
            if data[0][iterator] > 0.04 or data[0][iterator] < -0.04:
                start_index = iterator
                end = True
            iterator += 1

        end = False

        # Поиск конца
        iterator = len(data[1]) - 1
        while not end:
            if data[0][iterator] > 0.04 or data[0][iterator] < -0.04:
                end_index = iterator
                end = True
            iterator -= 1

        save_data_fragments(data, time, start_index, end_index, filenames[i])

## @brief Класс для разделения и сохранения данных
#
# @param data Входные данные
# @param time Время соответствующее данным
# @param start_index Индекс начала
# @param end_index Индекс конца
# @param filename Название сохраняемых данных
#
# @returns Файл с разделённым сигналом
#
# Данный класс получает на вход данные, вырезает из них сегмент и сохраняет в файлы с размером сигнала не более 1000 точек измерения
def save_data_fragments(data, time, start_index, end_index, filename):
    iterator = start_index
    for i in range((end_index - start_index) // 1000):
        # Имя файла
        file_end_name = filename.split('/')
        filename_save = filename[:len(filename) - len(file_end_name[len(file_end_name) - 1])]
        filename_save = filename_save + "split " + str(i + 1) + " " + file_end_name[len(file_end_name) - 1]
        # Открыть файл
        with open(filename_save, "w") as file:
            for j in range(20):
                file.write("\n")

            for j in range(iterator, iterator + 1000):
                file.write("       ")
                file.write((str(time[j])).ljust(6, '0'))
                file.write("      ")
                if data[0][j] < 0:
                    file.write(str(data[0][j]).ljust(7, '0'))
                else:
                    file.write((" " + str(data[0][j])).ljust(6, '0'))
                file.write("     ")
                if data[1][j] < 0:
                    file.write(str(data[1][j]).ljust(7, '0'))
                else:
                    file.write((" " + str(data[1][j])).ljust(6, '0'))
                file.write("     ")
                if data[2][j] < 0:
                    file.write(str(data[2][j]).ljust(7, '0'))
                else:
                    file.write((" " + str(data[2][j])).ljust(6, '0'))
                file.write("\n")
            iterator += 1000

    # Завершение записи
    # Имя файла
    file_end_name = filename.split('/')
    filename_save = filename[:len(filename) - len(file_end_name[len(file_end_name) - 1])]
    filename_save = filename_save + "split " + str(((end_index - start_index) // 1000) + 1) + " " + file_end_name[len(file_end_name) - 1]
    # Открыть файл
    if (end_index - start_index) - ((end_index - start_index) // 1000) * 1000 > 500:
        with open(filename_save, "w") as file:
            for j in range(20):
                file.write("\n")

            for j in range(iterator, end_index):
                file.write("       ")
                file.write((str(time[j])).ljust(6, '0'))
                file.write("      ")
                if data[0][j] < 0:
                    file.write(str(data[0][j]).ljust(7, '0'))
                else:
                    file.write((" " + str(data[0][j])).ljust(6, '0'))
                file.write("     ")
                if data[1][j] < 0:
                    file.write(str(data[1][j]).ljust(7, '0'))
                else:
                    file.write((" " + str(data[1][j])).ljust(6, '0'))
                file.write("     ")
                if data[2][j] < 0:
                    file.write(str(data[2][j]).ljust(7, '0'))
                else:
                    file.write((" " + str(data[2][j])).ljust(6, '0'))
                file.write("\n")