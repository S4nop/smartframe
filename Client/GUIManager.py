from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt, QDir
from Client.FileManager import FileManager
from Client.MediaManager import MediaManager
from Client.BufferManager import BufferManager
import threading, time

class MainForm(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.show()
        self.buffer_manager = BufferManager()
        self.media_manager = MediaManager()
        self.file_manager = FileManager()
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

    def work_inThread(self):
        fm = FileManager()
        num = fm.getNumOfFiles()
        for i in range(0, num):
            viewer_thread = threading.Thread(target=self.showMedia_inThread, daemon=True)
            viewer_thread.start()
            loader_thread = threading.Thread(target=self.loadMedia_inThread, args=(i, ), daemon=True)
            loader_thread.start()
            viewer_thread.join()
            loader_thread.join()

    def loadMedia_inThread(self, file_idx, toPrev=False):
        filename = self.file_manager.getFilenameByIdx(file_idx)
        isImage = self.file_manager.chkIsImage(file_idx)
        targ = self.media_manager.loadImage(filename) if isImage else self.media_manager.loadVideo(filename)

        if toPrev:
            self.buffer_manager.pushToNext()
            self.buffer_manager.setPrevBuffer([file_idx, targ])
        else:
            self.buffer_manager.pullToPrev()
            self.buffer_manager.setNextBuffer([file_idx, targ])

    def showMedia_inThread(self):
        idx, med = self.buffer_manager.getMainBuffer()
        if idx < 0:
            return
        isImage = self.file_manager.chkIsImage(idx)

        if isImage:
            self.imageLabel.setPixmap(med)
            self.setCentralWidget(self.imageLabel)
            time.sleep(3)
        else:
            for frame in med:
                self.imageLabel.setPixmap(frame)
                time.sleep(0.0422225)


