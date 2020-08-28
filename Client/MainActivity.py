from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from Client.FileManager import FileManager
from Client.MediaManager import MediaManager
from Client.BufferManager import BufferManager
from Client.KillableThread import ThreadWithExc
import Client.Utils as utils
import threading, time

class MainWindow(QMainWindow):
    work_thread: threading.Thread
    viewer_thread: threading.Thread
    loader_thread: threading.Thread
    sender_thread: ThreadWithExc
    now_page: int
    stop_request: bool

    def __init__(self):
        super().__init__()
        self.initUI()
        self.show()
        self.buffer_manager = BufferManager()
        self.media_manager = MediaManager(self.buffer_manager)
        self.file_manager = FileManager()
        self.stop_request = False
        self.onoffStatus = True
        self.now_page = -1
        self.loadPageToBuffer(0)
        self.join_checker()
        self.work_thread = threading.Thread(target=self.work_inThread, daemon=True)
        self.work_thread.start()

    def initUI(self):
        self.frame_width, self.frame_height = utils.getFrameSize()
        self.setStyleSheet("background-color : black")
        self.__initImageViewer()
        self.__initNextPrevBtn()
        self.__initOnOffButton()
        self.setWindowTitle("Image Viewer")
        self.showFullScreen()

    def mov_page(self, idx):
        toPrev, buf = self.__findBufferByIdx(idx)
        if buf is None:
            return
        self.viewer_thread = threading.Thread(target=self.showMedia_inThread,
                                         args=(buf, 3, ), daemon=True)
        self.viewer_thread.start()
        self.loadPageToBuffer(idx-1 if toPrev else idx+1, toPrev)
        self.join_checker()

    def loadPageToBuffer(self, idx, toPrev=False):
        self.loader_thread = threading.Thread(target=self.loadMedia_inThread, args=(idx, toPrev), daemon=True)
        self.loader_thread.start()

    def join_checker(self):
        if hasattr(self, 'loader_thread'):
            self.loader_thread.join()
        if hasattr(self, 'viewer_thread'):
            self.viewer_thread.join()

    def work_inThread(self, start_page=0):
        num = self.file_manager.getNumOfFiles()
        if start_page >= num:
            start_page = 0
        while True:
            for i in range(start_page, num):
                self.mov_page(i)
                if self.stop_request:
                    self.stop_request = False
                    return
            start_page = 0

    def loadMedia_inThread(self, file_idx, toPrev=False):
        if file_idx >= self.file_manager.getNumOfFiles():
            file_idx = 0
        filename = self.file_manager.getFilenameByIdx(file_idx)
        isImage = self.file_manager.chkIsImage(file_idx)
        self.media_manager.loadImage(filename, file_idx, toPrev) if isImage else self.media_manager.loadVideo(filename, file_idx, toPrev)

    def showMedia_inThread(self, med_data, sleep_time=3):
        isImage, idx, med = med_data
        if med is None:
            print("Buffer is empty")
            return
        self.now_page = idx
        if isImage:
            timer = 0
            self.imageLabel.setPixmap(med)
            while not self.stop_request and timer < sleep_time:
                time.sleep(0.5)
                timer += 0.5
        else:
            self.buffer_manager.clearQueue()
            self.sender_thread = ThreadWithExc(target=self.media_manager.sendFramesToBuffer, args=(med[0], med[1]), daemon=True)
            self.sender_thread.start()
            while True:
                ret, frame = self.buffer_manager.popFromQueue()
                if not ret or self.stop_request:
                    self.sender_thread.raiseExc(PermissionError)
                    return
                self.imageLabel.setPixmap(frame)
                time.sleep(0.0422225)

    def prevBtn_Click(self):
        self.stop_request = True
        self.work_thread.join()
        self.work_thread = threading.Thread(target=self.work_inThread, args=(self.now_page-1, ), daemon=True)
        self.work_thread.start()

    def nextBtn_Click(self):
        self.stop_request = True
        self.work_thread.join()
        self.work_thread = threading.Thread(target=self.work_inThread, args=(self.now_page+1, ), daemon=True)
        self.work_thread.start()

    def onoffBtn_Click(self):
        if self.onoffStatus:
            self.onoffStatus = False
            self.stop_request = True
            self.work_thread.join()
            self.__makeInvisible(self.imageLabel, 0)
            self.prevButton.setEnabled(False)
            self.nextButton.setEnabled(False)
        else:
            self.onoffStatus = True
            self.__makeInvisible(self.imageLabel, 1)
            self.prevButton.setEnabled(True)
            self.nextButton.setEnabled(True)
            self.work_thread = threading.Thread(target=self.work_inThread, args=(self.now_page, ), daemon=True)
            self.work_thread.start()

    def __findBufferByIdx(self, idx):
        if idx == self.buffer_manager.mainIdx:
            return False, self.buffer_manager.getMainBuffer()
        elif idx == self.buffer_manager.prevIdx:
            return True, self.buffer_manager.getPrevBuffer()
        elif idx == self.buffer_manager.nextIdx:
            return False, self.buffer_manager.getNextBuffer()
        else:
            return True, None

    def __initImageViewer(self):
        self.imageLabel = QLabel(self)
        self.imageLabel.setBackgroundRole(QPalette.Base)
        self.imageLabel.resize(self.frame_width, self.frame_height)
        self.imageLabel.move(0, 0)
        self.imageLabel.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)

    def __initOnOffButton(self):
        self.onoffButton = QPushButton('On/Off', self)
        self.onoffButton.setGeometry(int(self.frame_width / 10 * 9), 0,
                                     int(self.frame_width / 10), int(self.frame_height / 6))
        self.onoffButton.setStyleSheet("background-color : white")
        self.onoffButton.clicked.connect(self.onoffBtn_Click)

    def __initNextPrevBtn(self):
        self.prevButton = QPushButton(self)
        self.prevButton.setGeometry(0, 0, int(self.frame_width / 5), self.frame_height)
        self.prevButton.clicked.connect(self.prevBtn_Click)
        self.__makeInvisible(self.prevButton, 0)
        self.nextButton = QPushButton(self)
        self.nextButton.setGeometry(int(self.frame_width / 5 * 4), 0,
                                    int(self.frame_width / 5), self.frame_height)
        self.nextButton.clicked.connect(self.nextBtn_Click)
        self.__makeInvisible(self.nextButton, 0)

    def __makeInvisible(self, widget, opacity):
        opacity_effect = QGraphicsOpacityEffect()
        opacity_effect.setOpacity(opacity)
        widget.setGraphicsEffect(opacity_effect)

    def __initPrevBtn(self):
        opacity_effect = QGraphicsOpacityEffect()
        opacity_effect.setOpacity(0)
        self.prevButton = QPushButton(self)
