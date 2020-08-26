from queue import Queue

class BufferManager:
    frameBuffer: Queue
    prevBuffer: object
    mainBuffer: object
    nextBuffer: object

    def putPrevBuffer(self, obj):
        self.prevBuffer = obj
        self.pushToNext()

    def setMainBuffer(self, obj):
        self.mainBuffer = obj

    def putNextBuffer(self, obj):
        self.nextBuffer = obj
        self.pullToPrev()

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

    def addToQueue(self, obj):
        self.frameBuffer.put(obj)

    def popFromQueue(self):
        return self.frameBuffer.get()

    def __init__(self):
        self.prevBuffer = [True, None]
        self.mainBuffer = [True, None]
        self.nextBuffer = [True, None]
        self.frameBuffer = Queue()
