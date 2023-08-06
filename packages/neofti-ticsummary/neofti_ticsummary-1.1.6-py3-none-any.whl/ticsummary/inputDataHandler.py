from ticsummary import dataTIC
from dataclasses import dataclass
from collections import namedtuple
import numpy as np

def getMatrixByFromToFilter(array,fromIndex,toIndex):
    if fromIndex != toIndex:
        result = np.zeros(shape=(np.size(array,0),toIndex-fromIndex + 1),dtype=int)
        for i in range(0,np.size(array,0)):
            for j in range(fromIndex,toIndex + 1):
                result[i][j-fromIndex] = array[i][j]
    else:
        result = np.zeros(shape=np.size(array,0),dtype=int)
        for i in range(0,np.size(array,0)):
                result[i] = array[i][fromIndex]
    return result

def getSumDataByLoadMultiData(dataList): #(dataB1.matrix,dataB1.timeslice,dataB2.matrix,dataB2.timeslice,dataB1,dataB2)
    sumDataB1 = np.zeros(shape=(np.size(dataList[0][0][0],0),np.size(dataList[0][0][0],1)))
    sumDataB2 = np.zeros(shape=(np.size(dataList[0][0][2],0),np.size(dataList[0][0][2],1)))
    for i in range(len(dataList[0])):
        sumDataB1 += dataList[0][i][0]
        sumDataB2 += dataList[0][i][2]
    resultSignature = namedtuple('SumResult','matrixB1 timeSliceB1 delayB1 matrixB2 timeSliceB2 delayB2 description')
    return resultSignature(sumDataB1,dataList[0][0].timeSliceB1,dataList[0][0].delayB1 ,sumDataB2,dataList[0][0].timeSliceB2,dataList[0][0].delayB2,dataList[1])
            
'''def getMeasuredProfileTICDataByRawTICData(rawBlockData):
    npRawData = ndarray(rawBlockData.matrix)
    
    measureBlock = __measureProfile__(npRawData, rawBlockData.descriptionTICData.timeSlice)
    
    return MeasureProfileTICData(rawBlockData.descriptionTICData, 
                                         measureBlock.countPerSlice, 
                                         measureBlock.meanPerSlice, 
                                         measureBlock.sigmaPerSlice, 
                                         measureBlock.errorSigmaPerSlice, 
                                         measureBlock.timePerSlice, 
                                         measureBlock.numberPerChannel, 
                                         measureBlock.countPerChannel, 
                                         measureBlock.matrix)

def getMeasuredCounterTICDataByRawTICData(rawBlockData):
    npRawData = ndarray(rawBlockData.matrix)
    
    measureBlock = __measureCounter__(npRawData, rawBlockData.descriptionTICData.timeSlice)
    
    return MeasureCounterTICData(rawBlockData.descriptionTICData, 
                                         measureBlock.countPerSlice, 
                                         measureBlock.meanPerSlice, 
                                         measureBlock.sigmaPerSlice, 
                                         measureBlock.errorSigmaPerSlice, 
                                         measureBlock.timePerSlice, 
                                         measureBlock.numberPerChannel, 
                                         measureBlock.countPerChannel, 
                                         measureBlock.matrix)

def __measureProfile__(rawArray, timeSlice):
    countChannel = rawArray[0].size
    countSlice = len(rawArray)
    
    countPerSlice = numpy.zeros(countSlice)
    meanPerSlice = numpy.zeros(countSlice, float)
    sigmaPerSlice = numpy.zeros(countSlice, float)
    errorSigmaPerSlice = numpy.zeros(countSlice, float)
    timePerSlice = numpy.zeros(countSlice, float)
    
    numberPerChannel = numpy.arange(countChannel)
    countPerChannel = numpy.zeros(countChannel)
    
    for i in range(0,countSlice):
        countPerSlice[i] = numpy.sum(rawArray[i])
        meanPerSlice[i] = numpy.median(rawArray[i])
        sigmaPerSlice[i] = numpy.std(rawArray[i])
        errorSigmaPerSlice[i] = sigmaPerSlice[-1]/sqrt(countPerSlice[-1])
        timePerSlice[i] = 0 + timeSlice*i

        countPerChannel = countPerChannel + rawArray[i]
    
    for i in range (0, countChannel):
        numberPerChannel[i] = i + 1
    return __BlockMeasuredProfile__(countPerSlice, meanPerSlice, sigmaPerSlice, errorSigmaPerSlice, timePerSlice)

def getMeasuredCounterTICDataByRawTICData(rawBlockData):
    measureBlock = __measureCounter__(rawBlockData)
    
    return MeasureCounterTICData(rawBlockData.descriptionTICData,
                                         measureBlock.sum)
    
def __measureCounter__(rawArray):
    return __BlockMeasuredCounter__(rawArray.sum())
    
@dataclass
class __BlockMeasuredCounter__():
    sum:int
    
@dataclass
class __BlockMeasuredProfile__():
    countPerSlice:ndarray
    meanPerSlice:ndarray
    sigmaPerSlice:ndarray
    errorSigmaPerSlice:ndarray
    timePerSlice:ndarray

@dataclass
class MeasureProfileTICData:
    descriptionTICData: dataTIC.DescriptionTICData
    countPerSlice: ndarray
    meanPerSlice: ndarray
    sigmaPerSlice: ndarray
    errorSigmaPerSlice: ndarray
    timePerSlice: ndarray
    numberPerChannel: ndarray
    countPerChannel: ndarray
    matrix: ndarray

@dataclass
class MeasureCounterTICData:
    descriptionTICData: dataTIC.DescriptionTICData
    sum: int
    countPerSlice: ndarray
    timePerSlice: ndarray'''
    
if __name__ == '__main__':
    i=5