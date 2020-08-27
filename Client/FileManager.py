import os
import pandas as pd

class FileManager:
    data: pd
    file_num: int
    def __init__(self):
        self.__loadFileList()
        self.file_num = self.getNumOfFiles()

    def chkIsImage(self, idx):
        if idx >= self.file_num:
            return None
        if self.data.TYPE.values[idx] == "IMG":
            return True
        return False

    def getNumOfFiles(self):
        return len(self.data)

    def getFilenameByIdx(self, idx):
        if idx >= self.file_num:
            return None
        return "./data/"+self.data.FILENAME.values[idx]

    def __loadFileList(self):
        self.data = pd.read_csv("data/fileList", sep='?', index_col=0)

