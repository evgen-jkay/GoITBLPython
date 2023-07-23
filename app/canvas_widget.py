import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


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
