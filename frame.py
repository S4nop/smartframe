import numpy as np
import cv2
import subprocess
import os
import threading
from time import sleep
import requests

updated = 0

class FileUpdater:

    def svFile(self, content, filename):
        with open("./usr/" + filename, "wb") as file:
            file.write(content)

    def chkUpdate(self, number):
        f = open("./unum", 'r')
        unum = f.readline()
        return unum == number

    def updateUpNum(self, number):
        f = open("./unum", 'w')
        f.write(number)

    def getUpdatedPhotos(self, uList):
        fileList = os.listdir("./usr")
        svfileList = uList.split(",")
        return list(set(svfileList) - set(fileList))

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
            print("new Photos/Videos: ", newPhotos)
            for photo in newPhotos:
                self.getPhoto(server, photo, uid)
            self.updateUpNum(upNumber)
        updated = 1
        sleep(10)


class FrameViewer:
    fileList = []
    fileNum = 0

    def getProperSizeOfImg(self,img):
        width, height = self.getFrameSize()
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
            
        
    def updateFileList(self):
        path = "./usr"
        self.fileList =  os.listdir(path);

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

    def chkPicOrVid(self, fName):
        pic = ['jpg', 'jpeg', 'png', 'bmp', 'raw']
        fSplit = fName.split('.')
        if fSplit[len(fSplit) - 1] in pic:
            return 1
        else:
            return 2

    def showFrame(self, imgCV, width, height, bWidth, bHeight, waitTime):
        imgCV = cv2.resize(imgCV, (int(width), int(height)), interpolation = cv2.INTER_AREA)
        imgCV = cv2.copyMakeBorder(imgCV, bHeight, bHeight, bWidth, bWidth, cv2.BORDER_CONSTANT, value=[0,0,0])
        cv2.setMouseCallback("Viewr", self.showNextImg)
        #cv2.namedWindow("Viewr", cv2.WINDOW_NORMAL)

        cv2.imshow("Viewr", imgCV)
        cv2.moveWindow("Viewr", 0, -24)
        cv2.waitKey(waitTime)
        return self.fileNum

    def showVideo(self, vName):
        nFileNum = self.fileNum
        cap = cv2.VideoCapture(vName)
        ret, frame = cap.read()
        width, height, bWidth, bHeight = self.getProperSizeOfImg(frame)
        while(cap.isOpened()):
            ret, frame = cap.read()
            if self.showFrame(frame, width, height, bWidth, bHeight, 5) != nFileNum:
                break
        cap.release()

    def showPicture(self, pName):
        imgCV = cv2.imread(pName)
        width, height, bWidth, bHeight = self.getProperSizeOfImg(imgCV)
        self.showFrame(imgCV, width, height, bWidth, bHeight, 100)
        
    def showNextImg(self, event, x, y, flags, param):
        if event == cv2.EVENT_LBUTTONDOWN:
            if self.fileNum == len(self.fileList) - 1:
                self.fileNum = 0
                print("fileNum = 0")
            else:
                self.fileNum = self.fileNum + 1
                print(self.fileNum)
    
    def setfileNum(self, num):
        self.fileNum = num
    
    def chkFileUpdated(self):
        global updated
        if updated == 1:
            self.updateFileList()
            self.setfileNum(0)     
            updated = 0
            
    def frameWork(self):
        if self.chkPicOrVid(self.fileList[self.fileNum]) == 1:
            self.showPicture("./usr/" + self.fileList[self.fileNum])
        else:
            self.showVideo("./usr/" + self.fileList[self.fileNum]) 
            

def FrameViewer_Thread():
    print("FrameViewer_Thread_Started")
    global updated
    pv = FrameViewer()
    pv.updateFileList()
    while True:
        pv.frameWork()
        pv.chkFileUpdated()
    
def FileUpdater_Thread(server, uid):
    print("FileUpdater_Thread_Started")
    cs = FileUpdater()
    while True:
        cs.updateJob(server, uid)

if __name__ == "__main__":
   vw_thread = threading.Thread(target = FrameViewer_Thread) 
   up_thread = threading.Thread(target = FileUpdater_Thread, args=("http://192.168.43.121:2905", "rshtiger")) 
   up_thread.daemon=True
   vw_thread.daemon=True
   up_thread.start()
   vw_thread.start()
   up_thread.join()
   vw_thread.join()
