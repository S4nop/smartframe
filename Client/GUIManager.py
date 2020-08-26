from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt, QDir
from Client.FileManager import FileManager
from Client.MediaManager import MediaManager
import threading, time

class MainForm(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.show()
        work_thread = threading.Thread(target=self.work_inThread, daemon=True)
        work_thread.start()

    def initUI(self):
        self.__hideTitleBar()
        self.showFullScreen()
        self.__initImageViewer()
        self.setWindowTitle("Image Viewer")

    def __hideTitleBar(self):
        self.setWindowFlag(Qt.FramelessWindowHint)

    def __initImageViewer(self):
        self.imageLabel = QLabel()
        self.imageLabel.setBackgroundRole(QPalette.Base)
        self.imageLabel.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.setCentralWidget(self.imageLabel)
        #self.imageLabel.setScaledContents(True)

    def work_inThread(self):
        fm = FileManager()
        num = fm.getNumOfFiles()
        for i in range(0, num):
            filename = fm.getFilenameByIdx(i)
            viewer_thread = threading.Thread(target=self.openMedia_inThread, args=(filename, fm.chkIsImage(i)), daemon=True)
            viewer_thread.start()
            viewer_thread.join()

    def openMedia_inThread(self, filename=None, isImage=True):
        if filename == None:
            return

        mm = MediaManager()
        if isImage:
            self.imageLabel.setPixmap(mm.loadImage(filename))
            self.setCentralWidget(self.imageLabel)
        else:
            frames = mm.loadVideo(filename)
            for frame in frames:
                self.imageLabel.setPixmap(frame)
                time.sleep(0.0422225)
        time.sleep(3)


