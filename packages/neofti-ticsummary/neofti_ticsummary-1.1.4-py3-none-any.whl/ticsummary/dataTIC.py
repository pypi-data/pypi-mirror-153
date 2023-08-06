from dataclasses import dataclass
from datetime import datetime as dt
from enum import Enum
from numpy import ndarray


#import array
@dataclass
class DescriptionTICData:
    dateTime: dt
    timeSlice: float
    delay: float
    countChannel: int
    countSlice: int
    threshold: ndarray

@dataclass
class DescriptionDevice:
    name: str
    channelFrom: int
    channelTo: int
    

@dataclass
class RawTICData:
    descriptionTICData: DescriptionTICData
    matrix: ndarray