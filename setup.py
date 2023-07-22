import sys
from cx_Freeze import setup, Executable

build_exe_options = {
    "packages": ["asyncio"],  # Додайте інші необхідні пакети, якщо є
    "include_files": ["C:/Users/Laptopchik/AppData/Local/Programs/Python/Python311/DLLs/tcl86t.dll", "C:/Users/Laptopchik/AppData/Local/Programs/Python/Python311/DLLs/tk86t.dll"]  # Замініть <path_to_python> на ваш шлях до Python
}

base = None
if sys.platform == "win32":
    base = "Win32GUI"  # Використовуйте "Win32GUI", якщо ваша програма має GUI, і "None", якщо вона має консольний інтерфейс

setup(
    name="YourAppName",
    version="1.0",
    description="Description of Your App",
    options={"build_exe": build_exe_options},
    executables=[Executable("main.py", base=base)]
)
