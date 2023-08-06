from ticsummary.ui.MainWindow import ModeInterface
from ticsummary import backWorking, loaderData, inputDataHandler,databaseMYSQL

import numpy as np
from enum import Enum
from PyQt6.QtCore import QTimer

def manualInit(model):
    __manualSetData(model)
    model.mainWindow.setIdValue(model.currentManualIdData)
    model.mainWindow.setButtonPrevEnabled(not model.currentManualIdData == 1)
    model.mainWindow.setButtonNextEnabled(not model.currentManualIdData == model.countRecordsInDB)
    model.mainWindow.autoRangeAllProfileDocks()
    print("Manual mode init")
def manualUninit(model):
    None
def __manualSetData(model):
    model.taskRunner = backWorking.factoryTaskRunnerByTask(lambda:loaderData.loadDataById(model.currentManualIdData,model.sqlParameters, model.connector))
    model.taskRunner.task.finished.connect(lambda:model.__plotData__(model.taskRunner.getResult()))
    model.threadPool.start(model.taskRunner)
def manualIterationId(model, it):
    if (model.currentManualIdData + it > 0 or model.currentManualIdData + it <= model.countRecordsInDB):
        model.mainWindow.flagControlKeysOff = True
        model.currentManualIdData = model.currentManualIdData + it
        model.mainWindow.setIdValue(model.currentManualIdData)
        __manualSetData(model)
        model.mainWindow.setButtonPrevEnabled(not model.currentManualIdData == 1)
        model.mainWindow.setButtonNextEnabled(not model.currentManualIdData == model.countRecordsInDB)
        model.mainWindow.flagControlKeysOff = True
        #model.controlerBWTask = factoryThreadByTask(model.__loadDataById__, model.__plotData__,id=model.currentManualIdData,connector=model.connector)
        #model.controlerBWTask.start()
def manualSetId(model, value):
    if (value > 0 or value <= model.countRecordsInDB):
        model.mainWindow.flagControlKeysOff = True
        model.currentManualIdData = value
        model.mainWindow.setIdValue(value)
        __manualSetData(model)
        model.mainWindow.setButtonPrevEnabled(not model.currentManualIdData == 1)
        model.mainWindow.setButtonNextEnabled(not model.currentManualIdData == model.countRecordsInDB)
        model.mainWindow.flagControlKeysOff = False

def manualSumInit(model):
    '''model.mainWindow.setBusyMode(True)
    model.mainWindow.flagControlKeysOff = True
    model.multiTaskRunner =  backWorking.MultiTaskRunner(lambda id: loaderData.loadDataById(id + model.currentManualSumIdData,
                                                                                            model.sqlParameters), 
                                                        model.currentManualSumCountData)
    model.multiTaskRunner.finished.connect(lambda:model.__plotData__(inputDataHandler.getSumDataByLoadMultiData(model.multiTaskRunner.getAllResult())))
    model.multiTaskRunner.runAll(model.threadPool)'''
    #print("Manual sum mode uninit")
    model.taskRunner = backWorking.factoryTaskRunnerByTask(lambda:loaderData.loadDataByIdRange(model.currentManualSumIdData, model.currentManualSumCountData, model.sqlParameters,model.connector))
    model.taskRunner.task.finished.connect(lambda:model.__plotData__(inputDataHandler.getSumDataByLoadMultiData(model.taskRunner.getResult())))
    model.threadPool.start(model.taskRunner)
    model.mainWindow.setIdValue(model.currentManualSumIdData)
    model.mainWindow.setButtonPrevEnabled(not model.currentManualSumIdData - model.currentManualSumCountData < 1)
    model.mainWindow.setButtonNextEnabled(not model.currentManualSumIdData + model.currentManualSumCountData > model.countRecordsInDB)
    model.mainWindow.autoRangeAllProfileDocks()
    print("Manual sum mode init")
    '''model.mainWindow.setIdValue(model.currentManualSumIdData)
    model.loadSumData(model.currentManualSumIdData, model.currentManualSumCountData)
    model.__plotData__()'''
def manualSumUninit(model):
    None
def manualSumIterationId(model, it):
    model.mainWindow.flagControlKeysOff = True
    model.currentManualSumIdData = model.currentManualSumIdData + model.currentManualSumCountData*it
    model.mainWindow.setIdValue(model.currentManualSumIdData)
    model.mainWindow.setButtonPrevEnabled(not model.currentManualSumIdData - model.currentManualSumCountData < 1)
    model.mainWindow.setButtonNextEnabled(not model.currentManualSumIdData + model.currentManualSumCountData > model.countRecordsInDB)
    model.mainWindow.setBusyMode(True)
    model.taskRunner = backWorking.factoryTaskRunnerByTask(lambda:loaderData.loadDataByIdRange(model.currentManualSumIdData, model.currentManualSumCountData, model.sqlParameters,model.connector))
    model.taskRunner.task.finished.connect(lambda:model.__plotData__(inputDataHandler.getSumDataByLoadMultiData(model.taskRunner.getResult())))
    model.threadPool.start(model.taskRunner)
def manualSumSetId(model, value):
    model.mainWindow.flagControlKeysOff = True
    model.currentManualSumIdData = value
    model.mainWindow.setIdValue(model.currentManualSumIdData)
    model.mainWindow.setButtonPrevEnabled(not model.currentManualSumIdData - model.currentManualSumCountData < 1)
    model.mainWindow.setButtonNextEnabled(not model.currentManualSumIdData + model.currentManualSumCountData > model.countRecordsInDB)
    model.mainWindow.setBusyMode(True)
    model.taskRunner = backWorking.factoryTaskRunnerByTask(lambda:loaderData.loadDataByIdRange(model.currentManualSumIdData, model.currentManualSumCountData, model.sqlParameters,model.connector))
    model.taskRunner.task.finished.connect(lambda:model.__plotData__(inputDataHandler.getSumDataByLoadMultiData(model.taskRunner.getResult())))
    model.threadPool.start(model.taskRunner)
def __stepOnline__(model):
    count = databaseMYSQL.getCountRecords(model.sqlParameters.table,model.connector)
    if count > model.lastCount:
        model.lastCount = count
        runId = databaseMYSQL.getRunId(count-1, model.sqlParameters.table, model.connector)
        model.updateSizeDB(runId)
        model.mainWindow.setIdValue(databaseMYSQL.getRunId(count-1, model.sqlParameters.table, model.connector))
        model.taskRunner = backWorking.factoryTaskRunnerByTask(lambda:loaderData.loadDataByIdRange(model.currentManualSumIdData, model.currentManualSumCountData, model.sqlParameters,model.connector))
        model.taskRunner.task.finished.connect(lambda:model.__plotData__(inputDataHandler.getSumDataByLoadMultiData(model.taskRunner.getResult())))
        model.threadPool.start(model.taskRunner)
def onlineInit(model):
    print("Online mode init")
    #model.realTimeModeOn = True
    model.realTimeModeTimer = QTimer()
    model.realTimeModeTimer.timeout.connect(lambda:__stepOnline__(model))
    model.lastCount = 0
    model.realTimeModeTimer.start(1000)
def onlineUninit(model):
    model.realTimeModeTimer.stop()
def onlineIterationId(model, it):
    print(i)
def onlineSetId(model, value):
    print(i)

class modeShowData(Enum):
    MANUALMODE      = (manualInit,manualUninit,manualSetId,manualIterationId,ModeInterface.MANUAL)
    MANUALSUMMODE   = (manualSumInit,manualSumUninit,manualSumSetId,manualSumIterationId,ModeInterface.MANUALSUM)
    ONLINE          = (onlineInit,onlineUninit,onlineSetId,onlineIterationId,ModeInterface.ONLINE)
    def __init__(self,init,uninit,setId,iterationId,modeInterface):
        self.init = init
        self.uninit = uninit
        self.setId = setId
        self.iterationId = iterationId
        self.modeInterface = modeInterface