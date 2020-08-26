import sys
from Client.MainActivity import MainWindow
from PyQt5.QtWidgets import *

app = QApplication(sys.argv)
w = MainWindow()
sys.exit(app.exec())

