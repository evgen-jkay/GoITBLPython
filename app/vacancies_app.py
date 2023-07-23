import locale
import webbrowser
import requests
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QCheckBox, QPushButton, \
    QMessageBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from .canvas_widget import CustomFigureCanvas, CanvasContainer
from .styles import style_button

# Українська локалізація
try:
    locale.setlocale(locale.LC_TIME, 'uk_UA')
except locale.Error:
    locale.setlocale(locale.LC_TIME, 'Ukrainian_Ukraine')


class VacanciesApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Графік вакансій в Україні")
        self.setGeometry(100, 100, 1100, 650)
        self.setStyleSheet("background-color: #fff")

        # Set the fixed window size to prevent resizing
        self.setFixedSize(1100, 650)

        self.cities = ["Київ",
                       "Одеса",
                       "Львів",
                       "Дніпро",
                       "Харків",
                       "Запоріжжя",
                       "Тернопіль",
                       "Кривий Ріг"]

        self.fig, self.ax = plt.subplots(figsize=(10, 6))
        self.canvas = None

        self.create_widgets()
        self.create_menu()

        # Відображення графіка за замовчуванням
        self.update_plot()

    def create_widgets(self):
        # Create a vertical layout for the main window
        main_layout = QHBoxLayout()

        self.city_checkboxes = {city: QCheckBox(city) for city in self.cities}
        city_frame = QWidget(self)
        city_layout = QVBoxLayout(city_frame)
        for city_checkbox in self.city_checkboxes.values():
            city_checkbox.setChecked(False)  # Позначити всі міста за замовчуванням
            city_checkbox.stateChanged.connect(self.update_plot)
            city_layout.addWidget(city_checkbox)
        main_layout.addWidget(city_frame)

        # Create a vertical layout for buttons
        button_layout = QVBoxLayout()

        # Add buttons to the button layout
        github_button = QPushButton("GitHub")
        style_button(github_button)
        github_button.clicked.connect(self.open_github)
        button_layout.addWidget(github_button)

        goit_button = QPushButton("GoIT")
        style_button(goit_button)
        goit_button.clicked.connect(self.open_goit)
        button_layout.addWidget(goit_button)

        main_layout.addLayout(button_layout)  # Add the buttons layout to the main layout

        # Додайте обробник події закриття вікна
        self.setAttribute(Qt.WA_DeleteOnClose)
        self.destroyed.connect(QApplication.instance().quit)

        # Create the container for the canvas
        self.canvas = CustomFigureCanvas(self.fig)
        canvas_container = CanvasContainer(self.canvas)
        main_layout.addWidget(canvas_container)

        main_widget = QWidget()
        main_widget.setLayout(main_layout)
        self.setCentralWidget(main_widget)

    def create_menu(self):
        # Меню
        main_menu = self.menuBar()
        language_menu = main_menu.addMenu("Вибір мови")
        language_menu.addAction("Українська", self.change_language_ukrainian)
        language_menu.addAction("English", self.change_language_english)
        help_menu = main_menu.addMenu("Довідка")
        help_menu.addAction("Про програму", self.show_help)

    def fetch_data(self, city):
        # Отримання даних та створення DataFrame
        url = f"https://uadata.net/work-positions/cities.json?o={city}"
        response = requests.get(url)
        data_json = response.json()
        data_frame = pd.DataFrame(data_json["data"])

        # Підготовка даних
        data_frame["Дата"] = pd.to_datetime(data_frame["at"], format="%Y-%m-%d")
        data_frame["Вакансії"] = data_frame["val"].replace(0, np.nan).interpolate()
        data_frame.set_index("Дата", inplace=True)
        data_frame['rolling_mean'] = data_frame['Вакансії'].rolling(window=7).mean()
        return data_frame

    def plot_data(self, city):
        # Побудова графіків
        data_frame = self.fetch_data(city)

        self.ax.clear()
        data_frame["rolling_mean"].plot(ax=self.ax)
        self.ax.set_title(f"Кількість вакансій у місті {city}")
        self.ax.set_xlabel('Дата')
        self.ax.set_ylabel('Вакансії')
        self.ax.set_ylim(bottom=0)
        self.ax.legend()

        if self.canvas is not None:
            self.canvas.draw()

    def update_plot(self):
        # Get selected cities from checkboxes
        selected_cities = [city for city, checkbox in self.city_checkboxes.items() if checkbox.isChecked()]

        self.ax.clear()
        for city in selected_cities:
            data_frame = self.fetch_data(city)
            if len(data_frame) > 0:  # Check if there is data to plot for the city
                data_frame["rolling_mean"].plot(ax=self.ax, label=city)

        # Customize the plot
        self.ax.set_title(f'Вакансії у містах: {", ".join(selected_cities)}')
        self.ax.set_xlabel("Дата")
        self.ax.set_ylabel("Вакансії")
        self.ax.set_ylim(bottom=0)

        # Restore the legend
        if len(selected_cities) > 0:
            self.ax.legend()

        if self.canvas is not None:
            self.canvas.draw()

        # Update the main window title
        self.setWindowTitle("Кількість вакансій у містах України")

    def change_language_ukrainian(self):
        locale.setlocale(locale.LC_TIME, 'uk-UA')
        # Create a custom QMessageBox with custom styling
        msg_box = QMessageBox(self)
        style_button(msg_box)
        msg_box.setWindowTitle("Зміна мови")
        msg_box.setText("Мова змінена на Українську.")
        msg_box.exec_()

    def change_language_english(self):
        locale.setlocale(locale.LC_TIME, 'en-US')
        msg_box = QMessageBox(self)
        style_button(msg_box)
        msg_box.setWindowTitle("Change Language")
        msg_box.setText("Не працює. \nОчікуємо обнови.")
        msg_box.exec_()

    @staticmethod
    def open_github():
        webbrowser.open("https://github.com/evgen-jkay/GoITBLPython")

    @staticmethod
    def open_goit():
        webbrowser.open("https://goit.global/ua/")

    @staticmethod
    def show_help():
        help_text = "Це програма для відображення вакансій у різних містах України.\n\n" \
                    "Версія: 2.0.4\n" \
                    "Автор: Євген Ландаренко\n\n" \
                    "Зробленна в рамках Битви мов программування GoIT."

        msg_box = QMessageBox()
        msg_box.setWindowTitle("Довідка")
        msg_box.setText(help_text)

        msg_box.exec_()
