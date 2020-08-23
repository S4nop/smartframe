import sys
from Client.GUIManager import MainForm
from PyQt5.QtWidgets import *

app = QApplication(sys.argv)
w = MainForm()
sys.exit(app.exec())

