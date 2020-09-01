import os
import requests
from time import sleep

class UpdateManager:
    def chkUpdate(self, server, id):
        new_fVer = self.__getNewfVerFromServer(server, id)
        return new_fVer, new_fVer == self.__getNowfVer()

    def findNewPhotosFromList(self, uList):
        fileList = os.listdir("./usr")
        svfileList = uList.split(",")
        return list(set(svfileList) - set(fileList))

    def dlPhoto(self, server, photoName, id):
        param = {
            'id': id,
            'picName': photoName
        }
        url = server + "/getphoto"
        self.__saveFile(requests.get(url, params=param).content, photoName)

    def requestPhotolist(self, server, id):
        param = {
            'id': id
        }
        url = server + "/photo_list"
        return requests.get(url, params=param).content.decode('utf-8')

    def updateJob(self, server, uid):
        new_fVer, need_update = self.chkUpdate(server, id)
        if need_update:
            self.__updatefVer(new_fVer)
            newPhotos = self.findNewPhotosFromList(self.requestPhotolist(server, uid))
            print("new Photos/Videos: ", newPhotos)
            for photo in newPhotos:
                self.dlPhoto(server, photo, uid)
        sleep(10)

    def __saveFile(self, content, filename):
        with open("./usr/" + filename, "wb") as file:
            file.write(content)

    def __getNowfVer(self):
        f = open("Client/data/fVer", 'r')
        return f.readline()

    def __updatefVer(self, number):
        f = open("Client/data/fVer", 'w')
        f.write(number)

    def __getNewfVerFromServer(self, server, id):
        param = {
            'id': id
        }
        url = server + "/fVer"
        resp = requests.get(url, params=param)
        return resp.content.decode('utf-8')
