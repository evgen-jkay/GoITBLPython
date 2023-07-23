import matplotlib.pyplot as plt
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas


class CustomFigureCanvas(FigureCanvas):
    def __init__(self, *args, **kwargs):
        FigureCanvas.__init__(self, *args, **kwargs)
        self.setParent(None)

        # Initialize a flag to track if the canvas updates are paused
        self.updates_paused = False

    def pause_updates(self):
        # Pause canvas updates
        self.updates_paused = True

    def resume_updates(self):
        # Resume canvas updates
        self.updates_paused = False
        self.draw_idle()  # Force an update to the canvas

    def enterEvent(self, event):
        # Resume canvas updates when the mouse enters the canvas widget
        self.resume_updates()

    def leaveEvent(self, event):
        # Pause canvas updates when the mouse leaves the canvas widget
        self.pause_updates()


class CanvasContainer(QWidget):
    def __init__(self, canvas):
        super().__init__()
        layout = QVBoxLayout()
        layout.addWidget(canvas)
        self.setLayout(layout)
