import os
import pandas as pd

class FileManager:
    data: pd

    def loadFileList(self):
        self.data = pd.read_csv("data/fileList", sep='?', index_col=0)

    def chkIsImage(self, idx):
        if self.data[idx].TYPE == "IMG":
            return True
        return False

    def getNumOfFiles(self):
        return self.data.size()

    def getFilenameByIdx(self, idx):
        return self.data[idx].FILENAME
