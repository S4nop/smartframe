from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import Qt, QDir
from Client.FileManager import FileManager
from Client.MediaManager import MediaManager
from Client.BufferManager import BufferManager
import Client.Utils as utils
import threading, time

class MainWindow(QMainWindow):
    viewer_thread: threading.Thread
    loader_thread: threading.Thread

    def __init__(self):
        super().__init__()
        self.initUI()
        self.show()
        self.buffer_manager = BufferManager()
        self.media_manager = MediaManager(self.buffer_manager)
        self.file_manager = FileManager()
        work_thread = threading.Thread(target=self.work_inThread, daemon=True)
        work_thread.start()

    def initUI(self):
        self.frame_width, self.frame_height = utils.getFrameSize()
        self.__initImageViewer()
        self.__initNextPrevBtn()
        self.__initMenuButton()
        self.setWindowTitle("Image Viewer")
        self.showFullScreen()

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
        self.media_manager.loadImage(filename) if isImage else self.media_manager.loadVideo(filename)

    def showMedia_inThread(self):
        isImage, med = self.buffer_manager.getMainBuffer()
        if med is None:
            return

        if isImage:
            self.imageLabel.setPixmap(med)
            time.sleep(3)
        else:
            sender_thread = threading.Thread(target=self.media_manager.sendFramesToBuffer, args=(med,), daemon=True)
            sender_thread.start()
            while True:
                ret, frame = self.buffer_manager.popFromQueue()
                if not ret:
                    return
                self.imageLabel.setPixmap(frame)
                time.sleep(0.0422225)

    def prevBtn_Click(self):
        pass

    def nextBtn_Click(self):
        pass

    def menuBtn_Click(self):
        pass

    def __initImageViewer(self):
        self.imageLabel = QLabel(self)
        self.imageLabel.setBackgroundRole(QPalette.Base)
        self.imageLabel.resize(self.frame_width, self.frame_height)
        self.imageLabel.move(0, 0)
        self.imageLabel.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)

    def __initMenuButton(self):
        self.menuButton = QPushButton('MENU', self)
        self.menuButton.setGeometry(int(self.frame_width / 10 * 9), 0, int(self.frame_width / 10), int(self.frame_height / 6))
        self.menuButton.setStyleSheet("background-color : white")
        self.menuButton.clicked.connect(self.menuBtn_Click)

    def __initNextPrevBtn(self):
        self.prevButton = QPushButton(self)
        self.prevButton.setGeometry(0, 0, int(self.frame_width / 5), self.frame_height)
        self.prevButton.clicked.connect(self.prevBtn_Click)
        self.__makeInvisible(self.prevButton)
        self.nextButton = QPushButton(self)
        self.nextButton.setGeometry(int(self.frame_width / 5 * 4), 0, int(self.frame_width / 5), self.frame_height)
        self.nextButton.clicked.connect(self.nextBtn_Click)
        self.__makeInvisible(self.nextButton)

    def __makeInvisible(self, widget):
        opacity_effect = QGraphicsOpacityEffect()
        opacity_effect.setOpacity(0)
        widget.setGraphicsEffect(opacity_effect)

    def __initPrevBtn(self):
        opacity_effect = QGraphicsOpacityEffect()
        opacity_effect.setOpacity(0)
        self.prevButton = QPushButton(self)
