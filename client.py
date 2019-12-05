import requests
import os

class ComServer:

    def svFile(self, content, filename):
        with open("./img/" + filename, "wb") as file:
            file.write(content)

    def chkUpdate(self, number):
        f = open("./unum", 'r')
        unum = f.readline()
        return unum == number

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



if __name__ == "__main__":
    cs = ComServer()
    chkRslt = cs.idCheck("http://127.0.0.1:2905", "rshtiger")
    if not cs.chkUpdate(chkRslt.split("&!&")[0]):
        newPhotos = cs.getUpdatedPhotos(chkRslt.split("&!&")[1])
        print("new Photos: ", newPhotos)
        for photo in newPhotos:
            cs.getPhoto("http://127.0.0.1:2905", photo, "rshtiger")
    #cs.getPhoto("http://127.0.0.1:2905", "20190215_170720.jpg", "rshtiger")