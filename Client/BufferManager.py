class BufferManager:
    prevBuffer: object
    mainBuffer: object
    nextBuffer: object

    def setPrevBuffer(self, obj):
        self.prevBuffer = obj

    def setMainBuffer(self, obj):
        self.mainBuffer = obj

    def setNextBuffer(self, obj):
        self.nextBuffer = obj

    def getPrevBuffer(self):
        return self.prevBuffer

    def getMainBuffer(self):
        return self.mainBuffer

    def getNextBuffer(self):
        return self.nextBuffer

    def pushToNext(self):
        self.nextBuffer = self.mainBuffer
        self.mainBuffer = self.prevBuffer

    def pullToPrev(self):
        self.prevBuffer = self.mainBuffer
        self.mainBuffer = self.nextBuffer

    def __init__(self):
        self.prevBuffer = [-1, -1]
        self.mainBuffer = [-1, -1]
        self.nextBuffer = [-1, -1]
