import numpy as np
import cv2
import subprocess

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

def showPicture(imgName):
    width, height = getFrameSize()
    img = cv2.imread(imgName)
    img = cv2.resize(img, (int(width), int(height)), interpolation = cv2.INTER_AREA)
    cv2.imshow("res", img)
    cv2.waitKey(0)
        
if __name__=="__main__":
    showPicture("./img/elise-st-clair-53eLrhkux-k-unsplash.jpg")
    

