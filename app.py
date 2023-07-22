import requests
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

# Отримання даних та створення DataFrame
url = "https://uadata.net/work-positions/cities.json?o=Київ"
response = requests.get(url)
data_json = response.json()
data_frame = pd.DataFrame(data_json["data"])

# Підготовка даних
data_frame["Дата"] = pd.to_datetime(data_frame["at"])
data_frame["Вакансії"] = data_frame["val"].replace(0, np.nan).interpolate()
data_frame.set_index("Дата", inplace=True)

# Обчислення ковзного середнього за 7 днів та опис даних
data_frame['rolling_mean'] = data_frame['Вакансії'].rolling(window=7).mean()
data_frame_description = data_frame.describe()

# Побудова графіків
plt.figure(figsize=(10, 6))
data_frame["rolling_mean"].plot()
plt.title("Кількість вакансій по Києву")
plt.xlabel('Дата')
plt.ylabel('Вакансії')
plt.ylim(bottom=0)

# Зміна назви головного вікна
plt.get_current_fig_manager().set_window_title('Вакансії в Києві')

plt.show()
