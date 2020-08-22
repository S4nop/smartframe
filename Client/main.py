import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt


class MainForm(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.__hideTitleBar()
        self.__setBackgroundColor()
        self.showFullScreen()

    def __hideTitleBar(self):
        self.setWindowFlag(Qt.FramelessWindowHint)

    def __setBackgroundColor(self):
        self.setStyleSheet("background-color: black")

app = QApplication(sys.argv)
w = MainForm()
sys.exit(app.exec())
