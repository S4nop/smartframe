import numpy as np
import cv2
import subprocess
import os

global imgList
global imgNum

def updateImageList():
    path = "./img"
    return os.listdir(path);

def getFrameSize():
    cmd = ['xrandr']
    cmd2 = ['grep', '*']
    p = subprocess.Popen(cmd, stdout=subprocess.PIPE)
    p2 = subprocess.Popen(cmd2, stdin=p.stdout, stdout=subprocess.PIPE)
    p.stdout.close()

    resolution_string, junk = p2.communicate()
    resolution = resolution_string.split()[0]
    width, height = resolution.decode('utf-8').split("x")
    return width, height 

def showPicture():
    width, height = getFrameSize()
    imgCV = cv2.imread("./img/" + imgList[imgNum])
    imgCV = cv2.resize(imgCV, (int(width), int(height)), interpolation = cv2.INTER_AREA)
    cv2.setMouseCallback("res", showNextImg)
    cv2.imshow("res", imgCV)
    cv2.waitKey(100)

def showNextImg(event, x, y, flags, param):
    global imgList, imgNum
    if event == cv2.EVENT_LBUTTONDOWN:
        if imgNum == len(imgList) - 1:
            imgNum = 0
            print("imgNum = 0")
        else:
            imgNum = imgNum + 1
            print(imgNum)


if __name__=="__main__":
    imgList = updateImageList()
    imgNum = 0
    while(1):
        showPicture()
