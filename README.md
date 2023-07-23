## GoIT Battle Language Program

> app.py - консольна версія
> 
> main.py - версія с GUI

### Встановлення

1. Для встановлення та запуску потрібно мати Python 3
2. Встановити всі залежності які знаходятся в файлі ```requirement.txt``` можна за допомогою команди:
3. Программа працює з сайтом [uadata.net](https://uadata.net)

```shell
pip install -r requirements.txt
```

### Компіляція .py в .exe

```shell
pyinstaller --clean --onefile --noconsole main.py
```
