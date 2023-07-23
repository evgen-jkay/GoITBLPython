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
