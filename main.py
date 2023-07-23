import sys
from PyQt5.QtWidgets import QApplication
from app.vacancies_app import VacanciesApp

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

    # Create the main application instance
    main_app = VacanciesApp()
    main_app.show()

    sys.exit(app.exec_())
