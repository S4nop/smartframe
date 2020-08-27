from queue import Queue

class BufferManager:
    frameBuffer: Queue
    prevBuffer: object
    mainBuffer: object
    nextBuffer: object
    prevIdx: int
    mainIdx: int
    nextIdx: int

    def putPrevBuffer(self, obj):
        self.pushToNext()
        self.prevBuffer = obj
        self.prevIdx = obj[1]

    def setMainBuffer(self, obj):
        self.mainBuffer = obj
        self.mainIdx = obj[1]

    def putNextBuffer(self, obj):
        self.pullToPrev()
        self.nextBuffer = obj
        self.nextIdx = obj[1]

    def getPrevBuffer(self):
        return self.prevBuffer

    def getMainBuffer(self):
        return self.mainBuffer

    def getNextBuffer(self):
        return self.nextBuffer

    def pushToNext(self):
        self.nextBuffer = self.mainBuffer
        self.mainBuffer = self.prevBuffer
        self.nextIdx = self.mainIdx
        self.mainIdx = self.prevIdx
        self.prevBuffer = [-1, None]

    def pullToPrev(self):
        self.prevBuffer = self.mainBuffer
        self.mainBuffer = self.nextBuffer
        self.prevIdx = self.mainIdx
        self.mainIdx = self.nextIdx
        self.nextBuffer = [-1, -1, None]

    def addToQueue(self, obj):
        self.frameBuffer.put(obj)

    def popFromQueue(self):
        return self.frameBuffer.get()

    def clearQueue(self):
        self.frameBuffer = Queue()

    def queueTaskDone(self):
        self.frameBuffer.task_done()

    def __init__(self):
        self.prevBuffer = [True, -1, None]
        self.mainBuffer = [True, -1, None]
        self.nextBuffer = [True, -1, None]
        self.prevIdx = -1
        self.mainIdx = -1
        self.nextIdx = -1
        self.frameBuffer = Queue()
