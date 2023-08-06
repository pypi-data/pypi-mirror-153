from ticsummary import databaseMYSQL, backWorking

from PyQt6.QtCore import QObject, pyqtSignal
import numpy as np

from collections import namedtuple



def loadDataById(id,sqlParameters,connector = None):
    if connector == None:
        connector = databaseMYSQL.openConnection(sqlParameters)
    dataB1 = databaseMYSQL.getRecordByIdFirstBank(sqlParameters.table, connector, id)
    dataB2 = databaseMYSQL.getRecordByIdSecondBank(sqlParameters.table, connector, id)
    description = 'Date-{0} Time-{1} TimeSliceB1={2}(usec) TimeSliceB2={3}(usec) DelayB1={4}(usec) DelayB2={5}(usec)'.format(
            dataB1.dateTime.strftime("%Y-%m-%d"),
            dataB1.dateTime.strftime("%H:%M:%S"),
            dataB1.timeslice,
            dataB2.timeslice,
            dataB1.delay,
            dataB2.delay)
    resultSignature = namedtuple('SingleResult','matrixB1 timeSliceB1 delayB1 matrixB2 timeSliceB2 delayB2 description')
    return resultSignature(dataB1.matrix,dataB1.timeslice ,dataB2.delay ,dataB2.matrix,dataB2.timeslice,dataB2.delay,description)
        
def loadDataByIdRange(id,count,sqlParameters,connector = None):
    if connector == None:
        connector = databaseMYSQL.openConnection(sqlParameters)
    idList = range(id,id+count)
    dataB1List = databaseMYSQL.getRecordByIdListFirstBank(sqlParameters.table, connector, idList)
    dataB2List = databaseMYSQL.getRecordByIdListSecondBank(sqlParameters.table, connector, idList)

    checkDifferentDelayB1 = True
    checkDifferentTimeSliceB1 = True
    checkDifferentDelayB2 = True
    checkDifferentTimeSliceB2 = True
    delayB1 = dataB1List[0].delay
    delayB2 = dataB2List[0].delay
    TimeSliceB1 = dataB1List[0].timeslice
    TimeSliceB2 = dataB2List[0].timeslice
    for item in dataB1List:
        if item.delay != delayB1:
            checkDifferentDelayB1 = False
            break
    for item in dataB1List:
        if item.timeslice != TimeSliceB1:
            checkDifferentTimeSliceB1 = False
            break
    for item in dataB2List:
        if item.delay != delayB2:
            checkDifferentDelayB2 = False
            break
    for item in dataB2List:
        if item.timeslice != TimeSliceB2:
            checkDifferentTimeSliceB2 = False
            break

    result = list()
    description = 'DateFirst-{0} TimeFirst-{1} Datelast-{2} Timelast-{3} TimeSliceB1={4}(usec) TimeSliceB2={5}(usec) DelayB1={6}(usec) DelayB2={7}(usec) DifferentDelaysB1-{8} DifferentDelaysB2-{9} DifferentTimeSlicesB1-{10} DifferentTimeSlicesB2-{11}'.format(
            dataB1List[0].dateTime.strftime("%Y-%m-%d"),
            dataB1List[0].dateTime.strftime("%H:%M:%S"),
            dataB1List[-1].dateTime.strftime("%Y-%m-%d"),
            dataB1List[-1].dateTime.strftime("%H:%M:%S"),
            dataB1List[0].timeslice,
            dataB2List[0].timeslice,
            dataB1List[0].delay,
            dataB2List[0].delay,
            not checkDifferentDelayB1,
            not checkDifferentDelayB2,
            not checkDifferentTimeSliceB1,
            not checkDifferentTimeSliceB2)
    resultSignature = namedtuple('MultiResult','matrixB1 timeSliceB1 matrixB2 timeSliceB2 delayB1 delayB2')
    for i in range(0,np.size(dataB1List)):  #(dataB1.matrix,dataB1.timeslice,dataB2.matrix,dataB2.timeslice,dataB1,dataB2)
        result.append(resultSignature(dataB1List[i].matrix,dataB1List[i].timeslice,dataB2List[i].matrix,dataB2List[i].timeslice,dataB1List[i].delay,dataB2List[i].delay))
    return (result,description)
    

'''def sumData(dataB1List,dataB2List):
    sumDataB1 = np.zeros(shape=(np.size(dataB1List[0].matrix,0),np.size(dataB1List[0].matrix,1)))
    sumDataB2 = np.zeros(shape=(np.size(dataB2List[0].matrix,0),np.size(dataB2List[0].matrix,1)))
    for i in range(count):
        sumDataB1 += dataB1List[i].matrix
        sumDataB2 += dataB2List[i].matrix
    return (sumDataB1,dataB1List[0].timeslice,sumDataB2,dataB2List[0].timeslice)'''