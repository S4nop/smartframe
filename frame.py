import numpy as np
import cv2
import subprocess
import os

class PictureViewer:
    imgList = []
    imgNum = 0


    def updateImageList(self):
        path = "./img"
        self.imgList =  os.listdir(path);

    def getFrameSize(self):
        cmd = ['xrandr']
        cmd2 = ['grep', '*']
        p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
        p2 = subprocess.Popen(cmd2, stdin=p.stdout, stdout=subprocess.PIPE)
        p.stdout.close()

        resolution_string, junk = p2.communicate()
        resolution = resolution_string.split()[0]
        width, height = resolution.decode('utf-8').split("x")
        return width, height 

    def showPicture(self):
        width, height = self.getFrameSize()
        imgCV = cv2.imread("./img/" + self.imgList[self.imgNum])
        imgCV = cv2.resize(imgCV, (int(width), int(height)), interpolation = cv2.INTER_AREA)
        cv2.setMouseCallback("res", self.showNextImg)
        cv2.imshow("res", imgCV)
        cv2.waitKey(10)

    def showNextImg(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            if self.imgNum == len(self.imgList) - 1:
                self.imgNum = 0
                print("imgNum = 0")
            else:
                self.imgNum = self.imgNum + 1
                print(self.imgNum)

if __name__=="__main__":
    pv = PictureViewer()
    pv.updateImageList()
    while(1):
        pv.showPicture()

