from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt, QDir
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter
from Client.FileManager import FileManager
from Client.MediaManager import MediaManager
import threading, time

class MainForm(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.show()
        work_thread = threading.Thread(target=self.work, daemon=True)
        work_thread.start()

    def initUI(self):
        self.__hideTitleBar()
        self.showFullScreen()
        self.__initImageViewer()
        self.createActions()
        self.setWindowTitle("Image Viewer")

    def __hideTitleBar(self):
        self.setWindowFlag(Qt.FramelessWindowHint)

    def __initImageViewer(self):
        self.imageLabel = QLabel()
        self.imageLabel.setBackgroundRole(QPalette.Base)
        self.imageLabel.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.imageLabel.setScaledContents(True)
        self.setCentralWidget(self.imageLabel)

    def work(self):
        fm = FileManager()
        mm = MediaManager()
        num = fm.getNumOfFiles()
        for i in range(0, num):
            filename = fm.getFilenameByIdx(i)
            viewer_thread = threading.Thread(target=self.openImage_inThread, args=(mm.loadImage(filename),), daemon=True)
            viewer_thread.start()
            viewer_thread.join()

    def normalSize(self):
        self.imageLabel.adjustSize()

    def fitToWindow(self):
        fitToWindow = self.fitToWindowAct.isChecked()
        self.scrollArea.setWidgetResizable(fitToWindow)
        if not fitToWindow:
            self.normalSize()
        self.updateActions()

    def createActions(self):
        self.normalSizeAct = QAction("&Normal Size", self, shortcut="Ctrl+S",
                                     enabled=False, triggered=self.normalSize)

        self.fitToWindowAct = QAction("&Fit to Window", self, enabled=False,
                                      checkable=True, shortcut="Ctrl+F", triggered=self.fitToWindow)

    def updateActions(self):
        self.normalSizeAct.setEnabled(not self.fitToWindowAct.isChecked())

    def adjustScrollBar(self, scrollBar, factor):
        scrollBar.setValue(int(factor * scrollBar.value()
                               + ((factor - 1) * scrollBar.pageStep() / 2)))

    def openImage_inThread(self, image=None):
        if image == None:
            return

        self.imageLabel.setPixmap(image)
        time.sleep(3)


