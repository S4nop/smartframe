import os
import cv2
import subprocess
from PyQt5.QtGui import *
import numpy as np


class MediaManager:
    def loadImage(self, filename):
        image = cv2.imread(filename)
        if image is None:
            return None
        image = cv2.cvtColor(self.__resize([image, ])[0], cv2.COLOR_BGR2RGB)
        return QPixmap.fromImage(self.__toQImage([image, ])[0])

    def loadVideo(self, filename):
        frames = []
        cap = cv2.VideoCapture(filename)

        if cap is None:
            return None

        while(cap.isOpened()):
            ret, frame = cap.read()
            if not ret:
                break
            frames.append(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB))

        frames = self.__toQImage(self.__resize(frames))

        for i in range(0, len(frames)):
            frames[i] = QPixmap.fromImage(frames[i])

        return frames

    def __toQImage(self, ims, copy=False):
        results = []
        for i in range(0, len(ims)):
            if ims[i].dtype == np.uint8:
                if len(ims[i].shape) == 2:
                    qim = QImage(ims[i].data, ims[i].shape[1], ims[i].shape[0], ims[i].strides[0], QImage.Format_Indexed8)
                    qim.setColorTable([qRgb(i, i, i) for i in range(256)])
                    results.append(qim.copy() if copy else qim)

                elif len(ims[i].shape) == 3:
                    if ims[i].shape[2] == 3:
                        qim = QImage(ims[i].data, ims[i].shape[1], ims[i].shape[0], ims[i].strides[0], QImage.Format_RGB888)
                        results.append(qim.copy() if copy else qim)
                    elif ims[i].shape[2] == 4:
                        qim = QImage(ims[i].data, ims[i].shape[1], ims[i].shape[0], ims[i].strides[0], QImage.Format_ARGB32)
                        results.append(qim.copy() if copy else qim)

        return results

    def __resize(self, imgs):
        first_image = imgs[0]
        width, height, bWidth, bHeight = self.__getProperSizeOfImg(first_image)
        if not imgs[0].shape[0] == height and not imgs[0].shape[1] == width:
            for i in range(0, len(imgs)):
                imgs[i] = cv2.resize(imgs[i], (int(width), int(height)), interpolation=cv2.INTER_AREA)
                imgs[i] = cv2.copyMakeBorder(imgs[i], bHeight, bHeight, bWidth, bWidth, cv2.BORDER_CONSTANT, value=[0,0,0])

        return imgs

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
