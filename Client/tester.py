from PyQt5.QtCore import QDir, Qt
from PyQt5.QtGui import QImage, QPainter, QPalette, QPixmap, qRgb
from PyQt5.QtWidgets import (QAction, QApplication, QFileDialog, QLabel,
                             QMainWindow, QMenu, QMessageBox, QScrollArea, QSizePolicy, QInputDialog)
from PyQt5.QtPrintSupport import QPrintDialog, QPrinter
from Client.FileManager import FileManager
from Client.MediaManager import MediaManager
import cv2, os, glob, sys
import numpy as np


class ImageViewer(QMainWindow):
    def __init__(self):
        super(ImageViewer, self).__init__()
        self.printer = QPrinter()
        self.width = 620
        self.height = 620

        self.imageLabel = QLabel()
        self.imageLabel.setBackgroundRole(QPalette.Base)
        self.imageLabel.setSizePolicy(QSizePolicy.Ignored, QSizePolicy.Ignored)
        self.imageLabel.setScaledContents(True)

        self.setCentralWidget(self.imageLabel)

        self.createActions()

        self.setWindowTitle("Image Viewer")
        self.resize(self.width, self.height)
        fm = FileManager()
        filename = fm.getFilenameByIdx(0)
        mm = MediaManager()

        self.openImage(image=mm.loadImage(filename))

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


    def openImage(self, image=None, fileName=None):
        self.imageLabel.setPixmap(image)

        self.fitToWindowAct.setEnabled(True)
        self.updateActions()
        if not self.fitToWindowAct.isChecked():
            self.imageLabel.adjustSize()


if __name__ == '__main__':

    app = QApplication(sys.argv)
    imageViewer = ImageViewer()
    imageViewer.show()
    sys.exit(app.exec_())