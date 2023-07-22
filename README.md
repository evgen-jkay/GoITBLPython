## GoIT Battle Language Program

> app.py - консольна версія
> main.py - версія с GUI tkinter

### Встановлення

1. Для встановлення та запуску потрібно мати Python 3
2. Встановити всі залежності які знаходятся в файлі ```requirement.txt``` можна за допомогою команди:

```commandline
pip install -r requirements.txt
```

### .py -> .exe

```commandline
pyinstaller --clean --onefile --noconsole main.py
```