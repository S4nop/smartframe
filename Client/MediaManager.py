import os
import cv2
import threading
from PyQt5.QtGui import *
import numpy as np
from Client.BufferManager import BufferManager
import Client.Utils as utils


class MediaManager:
    buffer_manager: BufferManager

    def __init__(self, buffer_manager):
        self.buffer_manager = buffer_manager

    def loadImage(self, filename, idx, toPrev=False):
        image = cv2.imread(filename)
        result = None
        if image is not None:
            image = cv2.cvtColor(self.__resize(image, self.__getProperSizeOfImg(image)), cv2.COLOR_BGR2RGB)
            result = QPixmap.fromImage(self.__toQImage(image))
        if toPrev:
            self.buffer_manager.putPrevBuffer([True, idx, result])
        else:
            self.buffer_manager.putNextBuffer([True, idx, result])

    def loadVideo(self, filename, idx, toPrev=False):
        cap = cv2.VideoCapture(filename)

        if toPrev:
            self.buffer_manager.putPrevBuffer([False, idx, [cap, filename]])
        else:
            self.buffer_manager.putNextBuffer([False, idx, [cap, filename]])

    def sendFramesToBuffer(self, cap, filename):
        if not cap.isOpened():
            cap = cv2.VideoCapture(filename)
        ret, frame = cap.read()
        width, height, bWidth, bHeight = self.__getProperSizeOfImg(frame)
        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break
            frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            frame = self.__toQImage(self.__resize(frame, [width, height, bWidth, bHeight]))
            frame = QPixmap.fromImage(frame)
            self.buffer_manager.addToQueue([True, frame])
            self.buffer_manager.queueTaskDone()
        cap.release()

        self.buffer_manager.addToQueue([False, None])
        self.buffer_manager.queueTaskDone()

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
        width, height = utils.getFrameSize()
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
