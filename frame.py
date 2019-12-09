import numpy as np
import cv2
import subprocess
import os
import threading
from time import sleep
import requests

updated = 0

class PhotoUpdater:

    def svFile(self, content, filename):
        with open("./img/" + filename, "wb") as file:
            file.write(content)

    def chkUpdate(self, number):
        f = open("./unum", 'r')
        unum = f.readline()
        return unum == number

    def updateUpNum(self, number):
        f = open("./unum", 'w')
        f.write(number)

    def getUpdatedPhotos(self, uList):
        imgList = os.listdir("./img")
        svImgList = uList.split(",")
        return list(set(svImgList) - set(imgList))

    def idCheck(self, server, id):
        param = {
            'id': id
        }
        url = server + "/idcheck"
        resp = requests.get(url, params=param)
        return resp.content.decode('utf-8')

    def getPhoto(self, server, photoName, id):
        param = {
            'id': id,
            'picName': photoName
        }
        url = server + "/getphoto"
        self.svFile(requests.get(url, params=param).content, photoName)
    
    def updateJob(self, server, uid):
        global updated
        chkRslt = self.idCheck(server, uid) 
        upNumber = chkRslt.split("&!&")[0]
        if not self.chkUpdate(upNumber):
            newPhotos = self.getUpdatedPhotos(chkRslt.split("&!&")[1])
            print("new Photos: ", newPhotos)
            for photo in newPhotos:
                self.getPhoto(server, photo, uid)
            self.updateUpNum(upNumber)
        updated = 1
        sleep(10)


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
        cv2.waitKey(100)

    def showNextImg(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            if self.imgNum == len(self.imgList) - 1:
                self.imgNum = 0
                print("imgNum = 0")
            else:
                self.imgNum = self.imgNum + 1
                print(self.imgNum)
    
    def setImgNum(self, num):
        self.imgNum = num
    
    def chkImgUpdated(self):
        global updated
        if updated == 1:
            self.updateImageList()
            self.setImgNum(0)     
            updated = 0
        self.showPicture()

def photoViewer_Thread():
    print("PhotoViewr_Thread_Started")
    global updated
    pv = PictureViewer()
    pv.updateImageList()
    while True:
        pv.chkImgUpdated()
    
def photoUpdater_Thread(server, uid):
    print("PhotoUpdater_Thread_Started")
    cs = PhotoUpdater()
    while True:
        cs.updateJob(server, uid)

if __name__ == "__main__":
   vw_thread = threading.Thread(target = photoViewer_Thread) 
   up_thread = threading.Thread(target = photoUpdater_Thread, args=("http://192.168.43.121:2905", "rshtiger")) 
   up_thread.daemon=True
   vw_thread.daemon=True
   up_thread.start()
   vw_thread.start()
   up_thread.join()
   vw_thread.join()
