from pyqtgraph.dockarea import DockArea, Dock
from PyQt6 import QtWidgets,QtGui
import numpy as np

class DescriptionDataDock(Dock):
    def __init__(self,keyEventHandler, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.keyEventHandler = keyEventHandler
        self.textArea = QtWidgets.QPlainTextEdit('')
        self.addWidget(self.textArea)
    def setText(self,text:str):
        self.textArea.setPlainText(text)
    def clearText(self):
        self.textArea.setPlainText(0)
    def updateStyle(self):
        Dock.updateStyle(self)
        self.setOrientation("horizontal")
    def keyPressEvent(self,event):
        self.keyEventHandler(event)