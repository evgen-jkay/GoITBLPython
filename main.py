import locale
import sys
import webbrowser

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QCheckBox, QPushButton, \
    QMessageBox
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas

# Українська локалізація
try:
    locale.setlocale(locale.LC_TIME, 'uk_UA')
except locale.Error:
    locale.setlocale(locale.LC_TIME, 'Ukrainian_Ukraine')

# Массив міст
cities = ["Київ",
          "Одеса",
          "Львів",
          "Дніпро",
          "Харків",
          "Запоріжжя",
          "Тернопіль",
          "Кривий Ріг"]

fig, ax = plt.subplots(figsize=(10, 6))
canvas = None


def fetch_data(city):
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


def plot_data(city):
    global fig, ax

    # Побудова графіків
    data_frame = fetch_data(city)

    ax.clear()
    data_frame["rolling_mean"].plot(ax=ax)
    ax.set_title(f"Кількість вакансій у місті {city}")
    ax.set_xlabel('Дата')
    ax.set_ylabel('Вакансії')
    ax.set_ylim(bottom=0)
    ax.legend()

    if canvas is not None:
        canvas.draw()


def update_plot():
    global fig, ax, canvas

    # Get selected cities from checkboxes
    selected_cities = [city for city, checkbox in city_checkboxes.items() if checkbox.isChecked()]

    ax.clear()
    for city in selected_cities:
        data_frame = fetch_data(city)
        if len(data_frame) > 0:  # Check if there is data to plot for the city
            data_frame["rolling_mean"].plot(ax=ax, label=city)

    # Customize the plot
    ax.set_title(f'Вакансії у містах: {", ".join(selected_cities)}')
    ax.set_xlabel("Дата")
    ax.set_ylabel("Вакансії")
    ax.set_ylim(bottom=0)

    # Restore the legend
    if len(selected_cities) > 0:
        ax.legend()

    if canvas is not None:
        canvas.draw()

    # Update the main window title
    main_window.setWindowTitle("Кількість вакансій у містах України")


def style_button(button):
    button.setStyleSheet("""
            QPushButton {
                background-color: #007bff;
                color: white;
                padding: 5px 15px;
                border-radius: 5px;
            }
            QPushButton:hover {
                background-color: #0056b3;
            }
            QPushButton:pressed {
                background-color: #003f80;
            }
        """)


def change_language_ukrainian():
    locale.setlocale(locale.LC_TIME, 'uk-UA')
    # Create a custom QMessageBox with custom styling
    msg_box = QMessageBox(main_window)
    style_button(msg_box)
    msg_box.setWindowTitle("Зміна мови")
    msg_box.setText("Мова змінена на Українську.")

    msg_box.exec_()


def change_language_english():
    locale.setlocale(locale.LC_TIME, 'en-US')

    msg_box = QMessageBox(main_window)
    style_button(msg_box)
    msg_box.setWindowTitle("Change Language")
    msg_box.setText("Не працює. \nОчікуємо обнови")

    msg_box.exec_()


def open_github():
    webbrowser.open("https://github.com/evgen-jkay/GoITBLPython")


def open_goit():
    webbrowser.open("https://goit.global/ua/")


def show_help():
    help_text = "Це програма для відображення вакансій у різних містах України.\n\n" \
                "Версія: 2.0.4\n" \
                "Автор: Євген Ландаренко\n\n" \
                "Зробленна в рамках Битви мов программування GoIT."

    msg_box = QMessageBox(main_window)
    style_button(msg_box)
    msg_box.setWindowTitle("Довідка")
    msg_box.setText(help_text)

    msg_box.exec_()


class CustomFigureCanvas(FigureCanvas):
    def __init__(self, *args, **kwargs):
        FigureCanvas.__init__(self, *args, **kwargs)
        self.setParent(None)


class CanvasContainer(QWidget):
    def __init__(self, canvas):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(canvas)
        self.setLayout(layout)


if __name__ == "__main__":
    app = QApplication(sys.argv)

    # Set the style for the application
    app.setStyleSheet("""
        QMenu::item:selected {
            background-color: #e6e6e6;
            color: black;
        }

        QMenu::item:pressed {
            background-color: #c6c6c6;
            color: black;
        }
    """)

    main_window = QMainWindow()
    main_window.setWindowTitle("Графік вакансій в Україні")
    main_window.setGeometry(100, 100, 1100, 650)
    main_window.setStyleSheet("background-color: #fff")

    # Set the fixed window size to prevent resizing
    main_window.setFixedSize(1100, 650)

    # Create a vertical layout for the main window
    main_layout = QHBoxLayout()

    city_checkboxes = {city: QCheckBox(city) for city in cities}
    city_frame = QWidget(main_window)
    city_layout = QVBoxLayout(city_frame)
    for city_checkbox in city_checkboxes.values():
        city_checkbox.setChecked(False)  # Позначити всі міста за замовчуванням
        city_checkbox.stateChanged.connect(update_plot)
        city_layout.addWidget(city_checkbox)
    main_layout.addWidget(city_frame)

    # Create a vertical layout for buttons
    button_layout = QVBoxLayout()

    # Add buttons to the button layout
    github_button = QPushButton("GitHub")
    style_button(github_button)
    github_button.clicked.connect(open_github)
    button_layout.addWidget(github_button)

    goit_button = QPushButton("GoIT")
    style_button(goit_button)
    goit_button.clicked.connect(open_goit)
    button_layout.addWidget(goit_button)

    main_layout.addLayout(button_layout)  # Add the buttons layout to the main layout

    # Додайте обробник події закриття вікна
    main_window.setAttribute(Qt.WA_DeleteOnClose)
    main_window.destroyed.connect(app.quit)

    # Меню
    main_menu = main_window.menuBar()
    language_menu = main_menu.addMenu("Вибір мови")
    language_menu.addAction("Українська", change_language_ukrainian)
    language_menu.addAction("English", change_language_english)
    help_menu = main_menu.addMenu("Довідка")
    help_menu.addAction("Про програму", show_help)

    # Створення виджету для відображення графіка
    canvas = CustomFigureCanvas(fig)

    # Create the container for the canvas
    canvas_container = CanvasContainer(canvas)
    main_layout.addWidget(canvas_container)

    main_widget = QWidget()
    main_widget.setLayout(main_layout)
    main_window.setCentralWidget(main_widget)

    # Відображення графіка за замовчуванням
    update_plot()

    main_window.show()
    sys.exit(app.exec_())
