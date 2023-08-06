from PyQt6.QtCore import QObject, QThread, pyqtSignal, QRunnable, QThreadPool

def factoryThreadByTask(task,callback,**kwargs):
    thread = QThread()
    worker = __Worker__(thread, task,**kwargs)
    worker.finished.connect(callback)
    worker.moveToThread(thread)
    return ControllerBWTask(thread,worker)

class __Worker__(QObject):
    finished = pyqtSignal()
    def __init__(self,thread,task,**kwargs):
        super().__init__()
        self.task=task
        self.kwargs=kwargs
        thread.started.connect(self.run)
        self.finished.connect(thread.quit)
        self.finished.connect(self.deleteLater)
        thread.finished.connect(thread.deleteLater)
    def run(self):
        self.task(**self.kwargs)
        self.finished.emit()

class ControllerBWTask():
    def __init__(self,thread:QThread,worker:__Worker__):
        self.thread = thread
        self.worker = worker
    def start(self):
        self.thread.start()

from PyQt6.QtCore import QRunnable, QThreadPool, pyqtSignal, QObject

class Task(QObject):
    finished = pyqtSignal()
    result = None
    def __init__(self,func):
        super().__init__()
        self.func = func
        self.callbackFunc = None
    def setCallbackFunc(self,func):
        self.callbackFunc = func
    def run(self):
        #self.model.__loadDataById__(self.model.currentManualIdData,self.model.connector)
        self.result = self.func()
        if self.callbackFunc != None: self.callbackFunc()
        self.finished.emit()

class Task(QObject):
    finished = pyqtSignal()
    result = None
    def __init__(self,func):
        super().__init__()
        self.func = func
        self.callbackFunc = None
    def setCallbackFunc(self,func):
        self.callbackFunc = func
    def run(self):
        #self.model.__loadDataById__(self.model.currentManualIdData,self.model.connector)
        self.result = self.func()
        if self.callbackFunc != None: self.callbackFunc()
        self.finished.emit()

class TaskRunner(QRunnable):
    def __init__(self,task:Task,id):
        super().__init__()
        self.task = task
        self.id = id
    def getResult(self):
        return self.task.result
    def getId(self):
        return self.id
    def setCallbackFunc(self,func):
        self.task.setCallbackFunc(lambda: func(self.id))
    def run(self):
        self.task.run()
        #print("{0} task run".format(self.id))
        #self.model.__loadDataById__(self.model.currentManualIdData,self.model.connector)

def factoryTaskRunnerByTask(taskFunc):
    task = Task(taskFunc)
    taskRunner = TaskRunner(task,0)
    return taskRunner

def factoryTaskRunnerByIDTask(taskFunc,idTask=None):
    idTask = 0 if idTask==None else idTask
    task = Task(lambda:taskFunc(idTask))
    taskRunner = TaskRunner(task,0 if idTask==None else idTask)
    return taskRunner

class MultiTaskRunner(QObject):
    finished = pyqtSignal()
    def __init__(self,task,countTask):
        super().__init__()
        self.count = countTask
        self.taskRunnerList = list()
        for idTask in range(0,countTask):
            self.taskRunnerList.append(factoryTaskRunnerByIDTask(lambda id:task(id),idTask))
            self.taskRunnerList[idTask].setCallbackFunc(lambda id: self.setEndTaskById(id))
    def runAll(self, threadPool):
        #threadPool.start(self.taskRunnerList[0])
        for taskRunner in self.taskRunnerList:
            threadPool.start(taskRunner)
    def setEndTaskById(self,id):#,taskRunner):
        #print ("{0} task is end".format(id))
        self.count-=1
        if self.count == 0:
            self.finished.emit()
    def getAllResult(self):
        resultList = list()
        for taskRunner in self.taskRunnerList:
            resultList.append(taskRunner.getResult())
        return resultList
