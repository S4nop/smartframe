import os
import cv2
import subprocess
import threading
from PyQt5.QtGui import *
import numpy as np
from Client.BufferManager import BufferManager


class MediaManager:
    buffer_manager: BufferManager

    def __init__(self, buffer_manager):
        self.buffer_manager = buffer_manager

    def loadImage(self, filename, toPrev=False):
        image = cv2.imread(filename)
        if image is None:
            return None
        image = cv2.cvtColor(self.__resize(image, self.__getProperSizeOfImg(image)), cv2.COLOR_BGR2RGB)
        result = QPixmap.fromImage(self.__toQImage(image))
        if toPrev:
            self.buffer_manager.putPrevBuffer([False, result])
        else:
            self.buffer_manager.putNextBuffer([False, result])

    def loadVideo(self, filename, toPrev=False):
        cap = cv2.VideoCapture(filename)
        if cap is None:
            return None

        if toPrev:
            self.buffer_manager.putPrevBuffer(cap.read())
        else:
            self.buffer_manager.putNextBuffer(cap.read())

        sender_thread = threading.Thread(target=self.sendFramesToBuffer, args=(cap, ), daemon=True)
        sender_thread.start()

    def sendFramesToBuffer(self, cap):
        ret, frame = cap.read()
        width, height, bWidth, bHeight = self.__getProperSizeOfImg(frame)
        while(cap.isOpened()):
            ret, frame = cap.read()
            if not ret:
                break
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = self.__toQImage(self.__resize(frame, [width, height, bWidth, bHeight]))
            frame = QPixmap.fromImage(frame)
            self.buffer_manager.addToQueue([True, frame])

        self.buffer_manager.addToQueue([False, None])


    def __toQImage(self, im, copy=False):
        if im.dtype == np.uint8:
            if len(im.shape) == 2:
                qim = QImage(im.data, im.shape[1], im.shape[0], im.strides[0], QImage.Format_Indexed8)
                qim.setColorTable([qRgb(i, i, i) for i in range(256)])
                return qim.copy() if copy else qim

            elif len(im.shape) == 3:
                if im.shape[2] == 3:
                    qim = QImage(im.data, im.shape[1], im.shape[0], im.strides[0], QImage.Format_RGB888)
                    return qim.copy() if copy else qim
                elif im.shape[2] == 4:
                    qim = QImage(im.data, im.shape[1], im.shape[0], im.strides[0], QImage.Format_ARGB32)
                    return qim.copy() if copy else qim


    def __resize(self, img, size):
        width, height, bWidth, bHeight = size
        img = cv2.resize(img, (int(width), int(height)), interpolation=cv2.INTER_AREA)
        img = cv2.copyMakeBorder(img, bHeight, bHeight, bWidth, bWidth, cv2.BORDER_CONSTANT, value=[0,0,0])
        return img

    def __getProperSizeOfImg(self, img):
        width, height = self.__getFrameSize()
        imHeight = img.shape[0]
        imWidth = img.shape[1]
        width = int(width)
        height = int(height)
        newWidth = imWidth * (int(height) / imHeight)
        newHeight = imHeight * (int(width) / imWidth)

        if imHeight / imWidth > height / width:
            return newWidth, height, abs(int((width - newWidth) / 2)) + 2, 0
        else:
            return width, newHeight, 0, abs(int((height - newHeight) / 2)) + 2

    def __getFrameSize(self):
        cmd = ['xrandr']
        cmd2 = ['grep', '*']
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        p2 = subprocess.Popen(cmd2, stdin=p.stdout, stdout=subprocess.PIPE)
        p.stdout.close()

        resolution_string, junk = p2.communicate()
        resolution = resolution_string.split()[0]
        width, height = resolution.decode('utf-8').split("x")
        return width, height
