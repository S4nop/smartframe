import os
import cv2
from PyQt5.QtGui import *
import numpy as np


class MediaManager:
    def loadImage(self, filename):
        image = cv2.imread(filename)
        if image is None:
            return None
        return QPixmap.fromImage(self.__toQImage(image))

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

