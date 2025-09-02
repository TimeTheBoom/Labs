#!./venv/Scripts/python


import tkinter
from tkinter import filedialog
import customtkinter
from functools import partial
import utils


## @package main
# @brief Данный модуль содержит в себе интерфейс программы
#
# Текущий интерфейс программы:
#
# @image html C:\users\User\Desktop\interface.png "Интерфейс"
class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()

        # Buttons
        self.btnSeparate = None
        self.btnFourierMerge = None
        self.btnSignal = None
        self.btnLocalSignal = None
        self.btnFourier = None
        self.btnCompileSignal = None
        self.btnFilepath = None
        self.chbxSplit = None

        # Entries
        self.leDownBorder = None
        self.lePoints = None
        self.leFilepath = None
        self.leFourierMerge = None

        self.initUI()

## @brief Класс для инициализации пользовательского интерфейса
#
# @param self
#
# @returns Инициализированный интерфейс
    def initUI(self):
        # Theme
        customtkinter.set_appearance_mode("Dark")

        # Main window
        self.geometry("600x500")
        self.title("Grain sourness")
        self.resizable(width=False, height=False)

        # ----------------
        # Блок с кнопками
        # ----------------

        # Начальное время
        self.leDownBorder = customtkinter.CTkEntry(
            self, placeholder_text="Start time", width=75
        )
        self.leDownBorder.place(relx=0.4, rely=0.6, anchor=tkinter.CENTER)
        self.leDownBorder.insert(-1, 0.0000)

        # Количество точек
        self.lePoints = customtkinter.CTkEntry(
            self, placeholder_text="Points", width=75
        )
        self.lePoints.place(relx=0.6, rely=0.6, anchor=tkinter.CENTER)
        self.lePoints.insert(-1, 5000)

        # По скольку объединять преобразование фурье
        self.leFourierMerge = customtkinter.CTkEntry(
            self, placeholder_text="Four Merge", width=75
        )
        self.leFourierMerge.place(relx=0.75, rely=0.8, anchor=tkinter.CENTER)
        self.leFourierMerge.insert(-1, 10)

        # Окно ввода пути файла
        self.leFilepath = customtkinter.CTkEntry(
            self, placeholder_text="Filepath", width=300
        )
        self.leFilepath.place(relx=0.35, rely=0.1, anchor=tkinter.CENTER)

        # Выбрать файл
        self.btnFilepath = customtkinter.CTkButton(
            self, text="Browse file", command=partial(self.on_clicked, 0)
        )
        self.btnFilepath.place(relx=0.75, rely=0.1, anchor=tkinter.CENTER)

        # Показать полный сигнал
        self.btnLocalSignal = customtkinter.CTkButton(
            self, text="Show full signal", command=partial(self.on_clicked, 1)
        )
        self.btnLocalSignal.place(relx=0.5, rely=0.4, anchor=tkinter.CENTER)

        # Показать локальный сигнал
        self.btnSignal = customtkinter.CTkButton(
            self, text="Show local signal", command=partial(self.on_clicked, 2)
        )
        self.btnSignal.place(relx=0.2, rely=0.7, anchor=tkinter.CENTER)

        # Сохранить преобразование фурье
        self.btnCompileSignal = customtkinter.CTkButton(
            self,
            text="Save local as fourier",
            command=partial(self.on_clicked, 3),
        )
        self.btnCompileSignal.place(relx=0.5, rely=0.7, anchor=tkinter.CENTER)

        # Показать локальное преобразование фурье
        self.btnFourier = customtkinter.CTkButton(
            self, text="Show local fourier", command=partial(self.on_clicked, 4)
        )
        self.btnFourier.place(relx=0.8, rely=0.7, anchor=tkinter.CENTER)

        # Найти сигнал
        self.btnSignal = customtkinter.CTkButton(
            self, text="Find signal", command=partial(self.on_clicked, 5)
        )
        self.btnSignal.place(relx=0.2, rely=0.8, anchor=tkinter.CENTER)

        # Сохранить среднее преобразование фурье
        self.btnFourierMerge = customtkinter.CTkButton(
            self, text="Save average fourier", command=partial(self.on_clicked, 6)
        )
        self.btnFourierMerge.place(relx=0.5, rely=0.8, anchor=tkinter.CENTER)

        # Разделить сигналы
        self.btnSeparate = customtkinter.CTkButton(
            self, text="Separate signals", command=partial(self.on_clicked, 7)
        )
        self.btnSeparate.place(relx=0.2, rely=0.9, anchor=tkinter.CENTER)

        is_split = customtkinter.BooleanVar()
        self.chbxSplit = customtkinter.CTkCheckBox(self, text="Import split signals?", variable = is_split)

        self.chbxSplit.place(relx=0.8, rely=0.9, anchor=tkinter.CENTER)
## @brief Класс для выбора файла
#
# @param self
#
# @returns Полный путь к файлу
#
# Данный класс вызывает окно выбора файла
    def choose_file(self):
        filepath = filedialog.askopenfilenames(filetypes=[("Text files", "*.txt")])
        if filepath is not None:

            self.leFilepath.delete(-1, tkinter.END)
            self.leFilepath.insert(-1, filepath)

## @brief Класс для обработки нажатия кнопок
#
# @param self
# @param index Номер нажимаемой кнопки
#
# Данный класс вызывает соответствующую нажатой кнопке функцию
    def on_clicked(self, index):
        full_filepath = self.leFilepath.get()
        current_filepath = full_filepath.split("} {")

        current_filepath[0] = current_filepath[0][1:]
        current_filepath[len(current_filepath) - 1] = current_filepath[len(current_filepath) - 1][:len(current_filepath[len(current_filepath) - 1]) - 1]

        btn_finder = {
            0: self.choose_file,
            1: utils.show_full_signal,
            2: utils.show_local_signal,
            3: utils.save_local_fourier,
            4: utils.show_local_fourier,
            5: utils.show_found_signal,
            6: utils.save_average_fourier,
            7: utils.separate_signals
        }

        func = btn_finder.get(index)

        if index == 0:
            func()
        else:
            if current_filepath == "":
                return

            if index in range(1, 2):
                func(current_filepath[0])
            elif index in range(2, 5):
                func(
                    current_filepath[0],
                    float(self.leDownBorder.get()),
                    int(self.lePoints.get()),
                )
            elif index == 5:
                func(current_filepath[0])
            elif index == 6:
                func(current_filepath, int(self.leFourierMerge.get()), self.chbxSplit.get())
            elif index == 7:
                func(current_filepath)


if __name__ == "__main__":
    app = App()
    app.mainloop()
