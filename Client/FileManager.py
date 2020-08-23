import os
import pandas as pd

class FileManager:
    data: pd
    def __init__(self):
        self.__loadFileList()

    def chkIsImage(self, idx):
        if self.data.TYPE.values[idx] == "IMG":
            return True
        return False

    def getNumOfFiles(self):
        return len(self.data)

    def getFilenameByIdx(self, idx):
        return "./data/"+self.data.FILENAME.values[idx]

    def __loadFileList(self):
        self.data = pd.read_csv("data/fileList", sep='?', index_col=0)

