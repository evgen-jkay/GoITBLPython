import requests
import pandas as pd
import numpy as np
import locale
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import tkinter as tk
from tkinter import messagebox
import webbrowser

# Українська локалізація
try:
    locale.setlocale(locale.LC_TIME, 'uk_UA')
except locale.Error:
    locale.setlocale(locale.LC_TIME, 'Ukrainian_Ukraine')

# Розміри вікна
WINDOW_WIDTH = 1100
WINDOW_HEIGHT = 650

# Массив міст
cities = ["Київ",
          "Одеса",
          "Львів",
          "Дніпро",
          "Харків",
          "Запоріжжя",
          "Тернопіль",
          "Кривий Ріг"]

ukrainian_month_names = [
    'січень', 'лютий', 'березень', 'квітень', 'травень', 'червень',
    'липень', 'серпень', 'вересень', 'жовтень', 'листопад', 'грудень'
]


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
    # Побудова графіків
    data_frame = fetch_data(city)

    plt.figure(figsize=(10, 6))
    data_frame["rolling_mean"].plot()
    plt.title(f"Кількість вакансій у місті {city}")
    plt.xlabel('Дата')
    plt.ylabel('Вакансії')
    plt.ylim(bottom=0)
    fig = plt.gcf()

    return fig


def update_plot(*args):
    # Зміна назви головного вікна
    selected_city = city_var.get()
    fig = plot_data(selected_city)

    for widget in plot_frame.winfo_children():
        widget.destroy()

    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.draw()
    canvas.get_tk_widget().pack()

    root.title(f'Вакансії у місті {selected_city}')


def change_language_ukrainian():
    locale.setlocale(locale.LC_TIME, 'uk-UA')
    messagebox.showinfo("Зміна мови", "Мова змінена на Українську.")


def change_language_english():
    locale.setlocale(locale.LC_TIME, 'en-US')
    messagebox.showinfo("Change Language", "Не працює. \nОчікуємо обнови")


def open_github():
    webbrowser.open("https://github.com/evgen-jkay/GoITBLPython")


def open_goit():
    webbrowser.open("https://goit.global/ua/")


def show_help():
    help_text = "Це програма для відображення вакансій у різних містах України.\n\n" \
                "Версія: 1.3\n" \
                "Автор: Євген Ландаренко\n\n" \
                "Зробленна в рамках Битви мов программування GoIT."

    # Create the custom modal window
    help_window = tk.Toplevel()
    help_window.title("Довідка")

    help_label = tk.Label(help_window, text=help_text, justify="left", padx=10, pady=10)
    help_label.pack()

    github_button = tk.Button(help_window, text="GitHub repo.", command=open_github, width=30)
    github_button.pack(side=tk.LEFT, padx=5, pady=5)

    goit_button = tk.Button(help_window, text="GoIT", command=open_goit, width=30)
    goit_button.pack(side=tk.RIGHT, padx=5, pady=5)


if __name__ == "__main__":
    root = tk.Tk()
    root.title("Графік вакансій в Україні")
    root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
    root.configure(bg='#fff')
    root.resizable(width=False, height=False)

    # Меню
    main_menu = tk.Menu(root)
    root.config(menu=main_menu)

    # Меню "Вибір мови"
    language_menu = tk.Menu(main_menu, tearoff=False)
    main_menu.add_cascade(label="Вибір мови", menu=language_menu)
    language_menu.add_command(label="Українська", command=change_language_ukrainian)
    language_menu.add_command(label="English", command=change_language_english)

    # Меню "Довідка"
    help_menu = tk.Menu(main_menu, tearoff=False)
    main_menu.add_cascade(label="Довідка", menu=help_menu)
    help_menu.add_command(label="Про програму", command=show_help)

    city_var = tk.StringVar(root)
    city_var.set(cities[0])
    city_var.trace("w", update_plot)

    city_frame = tk.Frame(root, bg='#fff')
    city_frame.grid(row=0, column=0, padx=5, pady=5)

    for i, city in enumerate(cities):
        tk.Radiobutton(city_frame,
                       text=city,
                       variable=city_var,
                       value=city,
                       bg='#fff').pack(side=tk.TOP,
                                       padx=5,
                                       pady=5,
                                       anchor=tk.W)

    plt.gca().xaxis.set_major_formatter(plt.FuncFormatter(lambda index, _: ukrainian_month_names[int(index) - 1]))
    plot_frame = tk.Frame(root, bg='#fff')
    plot_frame.grid(row=0,
                    column=1,
                    padx=5,
                    pady=5)

    update_plot()

    root.mainloop()
