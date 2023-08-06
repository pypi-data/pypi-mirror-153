from ticsummary.ui import ConnectionConfigurationDialog
from ticsummary.ui.OpenSqlDataDialog import OpenSQLData
from ticsummary.ui.ViewGraphicsDialog import ViewGraphicsDialog
from ticsummary.ui.ProfileBeamDock import ProfileBeamDock
from ticsummary.ui.DescriptionDataDock import DescriptionDataDock

from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import Qt
import pyqtgraph as pg
import numpy as np
from enum import Enum
import time

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 672)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.comboBoxType = QtWidgets.QComboBox(self.centralwidget)
        font = QtGui.QFont()
        font.setPointSize(14)
        self.comboBoxType.setFont(font)
        self.comboBoxType.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.comboBoxType.setObjectName("comboBoxType")
        self.horizontalLayout.addWidget(self.comboBoxType)
        self.labelId = QtWidgets.QLabel(self.centralwidget)
        self.labelId.setObjectName("labelId")
        self.horizontalLayout.addWidget(self.labelId)
        self.spinBoxId = QtWidgets.QSpinBox(self.centralwidget)
        self.spinBoxId.setFocusPolicy(QtCore.Qt.FocusPolicy.ClickFocus)
        self.spinBoxId.setButtonSymbols(QtWidgets.QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.spinBoxId.setKeyboardTracking(True)
        self.spinBoxId.setObjectName("spinBoxId")
        self.horizontalLayout.addWidget(self.spinBoxId)
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)
        self.spinBoxCountSum = QtWidgets.QSpinBox(self.centralwidget)
        self.spinBoxCountSum.setFocusPolicy(QtCore.Qt.FocusPolicy.ClickFocus)
        self.spinBoxCountSum.setButtonSymbols(QtWidgets.QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.spinBoxCountSum.setMinimum(2)
        self.spinBoxCountSum.setMaximum(1000)
        self.spinBoxCountSum.setObjectName("spinBoxCountSum")
        self.horizontalLayout.addWidget(self.spinBoxCountSum)
        self.pushButtonPrev = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonPrev.setAutoRepeat(True)
        self.pushButtonPrev.setAutoRepeatDelay(300)
        self.pushButtonPrev.setAutoRepeatInterval(100)
        self.pushButtonPrev.setObjectName("pushButtonPrev")
        self.horizontalLayout.addWidget(self.pushButtonPrev)
        self.pushButtonNext = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonNext.setAutoRepeat(True)
        self.pushButtonNext.setAutoRepeatDelay(300)
        self.pushButtonNext.setAutoRepeatInterval(100)
        self.pushButtonNext.setObjectName("pushButtonNext")
        self.horizontalLayout.addWidget(self.pushButtonNext)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout.addLayout(self.horizontalLayout)
        self.horizontalLayoutGraphics = QtWidgets.QHBoxLayout()
        self.horizontalLayoutGraphics.setObjectName("horizontalLayoutGraphics")
        self.verticalLayout.addLayout(self.horizontalLayoutGraphics)
        self.progressBarTask = QtWidgets.QProgressBar(self.centralwidget)
        self.progressBarTask.setProperty("value", 24)
        self.progressBarTask.setObjectName("progressBarTask")
        self.verticalLayout.addWidget(self.progressBarTask)
        self.horizontalLayout_Information = QtWidgets.QHBoxLayout()
        self.horizontalLayout_Information.setObjectName("horizontalLayout_Information")
        self.verticalLayout.addLayout(self.horizontalLayout_Information)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 800, 31))
        font = QtGui.QFont()
        font.setPointSize(16)
        self.menubar.setFont(font)
        self.menubar.setObjectName("menubar")
        self.menuFile = QtWidgets.QMenu(self.menubar)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.menuFile.setFont(font)
        self.menuFile.setObjectName("menuFile")
        self.menuEdit = QtWidgets.QMenu(self.menubar)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.menuEdit.setFont(font)
        self.menuEdit.setObjectName("menuEdit")
        self.menuView = QtWidgets.QMenu(self.menubar)
        self.menuView.setObjectName("menuView")
        MainWindow.setMenuBar(self.menubar)
        self.actionFrom_sql_database = QtGui.QAction(MainWindow)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.actionFrom_sql_database.setFont(font)
        self.actionFrom_sql_database.setObjectName("actionFrom_sql_database")
        self.actionmeasured_data_to_csv = QtGui.QAction(MainWindow)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.actionmeasured_data_to_csv.setFont(font)
        self.actionmeasured_data_to_csv.setObjectName("actionmeasured_data_to_csv")
        self.actionConnectionSqlDatabase = QtGui.QAction(MainWindow)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.actionConnectionSqlDatabase.setFont(font)
        self.actionConnectionSqlDatabase.setObjectName("actionConnectionSqlDatabase")
        self.actionPlots = QtGui.QAction(MainWindow)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.actionPlots.setFont(font)
        self.actionPlots.setObjectName("actionPlots")
        self.actionReset_position = QtGui.QAction(MainWindow)
        font = QtGui.QFont()
        font.setPointSize(16)
        self.actionReset_position.setFont(font)
        self.actionReset_position.setObjectName("actionReset_position")
        self.actionMeasuredDataToCSV = QtGui.QAction(MainWindow)
        self.actionMeasuredDataToCSV.setObjectName("actionMeasuredDataToCSV")
        self.actionSave_state_program = QtGui.QAction(MainWindow)
        self.actionSave_state_program.setEnabled(False)
        self.actionSave_state_program.setObjectName("actionSave_state_program")
        self.menuFile.addSeparator()
        self.menuFile.addAction(self.actionMeasuredDataToCSV)
        self.menuEdit.addAction(self.actionConnectionSqlDatabase)
        self.menuView.addAction(self.actionPlots)
        self.menuView.addAction(self.actionReset_position)
        self.menubar.addAction(self.menuEdit.menuAction())
        self.menubar.addAction(self.menuView.menuAction())
        self.menubar.addAction(self.menuFile.menuAction())

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "TICSummary"))
        self.labelId.setText(_translate("MainWindow", "Id:"))
        self.label.setText(_translate("MainWindow", "Count:"))
        self.pushButtonPrev.setToolTip(_translate("MainWindow", "Key Left"))
        self.pushButtonPrev.setText(_translate("MainWindow", "Prev"))
        self.pushButtonPrev.setShortcut(_translate("MainWindow", "Left"))
        self.pushButtonNext.setToolTip(_translate("MainWindow", "Key Right"))
        self.pushButtonNext.setText(_translate("MainWindow", "Next"))
        self.pushButtonNext.setShortcut(_translate("MainWindow", "Right"))
        self.menuFile.setTitle(_translate("MainWindow", "Export"))
        self.menuEdit.setTitle(_translate("MainWindow", "Connection"))
        self.menuView.setTitle(_translate("MainWindow", "View"))
        self.actionFrom_sql_database.setText(_translate("MainWindow", "from sql database"))
        self.actionmeasured_data_to_csv.setText(_translate("MainWindow", "measured data to csv"))
        self.actionConnectionSqlDatabase.setText(_translate("MainWindow", "Edit"))
        self.actionPlots.setText(_translate("MainWindow", "Plots"))
        self.actionReset_position.setText(_translate("MainWindow", "Reset position"))
        self.actionMeasuredDataToCSV.setText(_translate("MainWindow", "Measured data to csv"))
        self.actionSave_state_program.setText(_translate("MainWindow", "Save state program"))



class DockAreaWithUncloseableDocks(pg.dockarea.DockArea):
    def makeContainer(self, typ):
        new = super(DockAreaWithUncloseableDocks, self).makeContainer(typ)
        if hasattr(new, "setChildrenCollapsible"):
            new.setChildrenCollapsible(False)
        return new

class ModeInterface(Enum):
    DEFFAULT  = (False,False,False,False)
    MANUAL    = (True,True,True,False)
    MANUALSUM = (True,True,True,True)
    ONLINE    = (True,True,False,False)  
    def __init__(self,chartEnabled,comboBoxTypeEnabled,controlDataIdEnabled,controlSumDataIdEnabled):
        self.chartEnabled = chartEnabled
        self.comboBoxTypeEnabled = comboBoxTypeEnabled
        self.controlDataIdEnabled = controlDataIdEnabled
        self.controlSumDataIdEnabled = controlSumDataIdEnabled


class MainWindow(QtWidgets.QMainWindow, QtCore.QObject):
    sigIterationValueId = QtCore.pyqtSignal(int)
    sigSetNewId = QtCore.pyqtSignal(int)
    sigSetNewCountSum = QtCore.pyqtSignal(int)
    flagControlKeysOff = False
    #self.sigSetRealTimeMode = QtCore.pyqtSignal()
    #self.sigUnsetRealTimeMode = QtCore.pyqtSignal()

    def __init__(self,parent=None):
        super().__init__(parent)
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.actionPlots.triggered.connect(self.__openViewGraphics__)
        self.ui.actionReset_position.triggered.connect(lambda : self.dockAreaChart.restoreState(self.dockAreaState))
        self.ui.pushButtonNext.clicked.connect(self.__nextId__)
        self.ui.pushButtonPrev.clicked.connect(self.__prevId__)
        self.ui.pushButtonNext.setFocus()

        self.ui.progressBarTask.setHidden(True)

        self.dockAreaChart = DockAreaWithUncloseableDocks()

        self.profileDockX1 = ProfileBeamDock(self.keyPressEvent, name="MCP X B1", size=(5,1))
        self.profileDockX2 = ProfileBeamDock(self.keyPressEvent, name="MCP X B2", size=(5,1))
        self.profileDockY1 = ProfileBeamDock(self.keyPressEvent, name="MCP Y B1", size=(5,1))
        self.profileDockY2 = ProfileBeamDock(self.keyPressEvent, name="MCP Y B2", size=(5,1))
        self.descriptionData = DescriptionDataDock(self.keyPressEvent,name="DATA DESCRIPTION",size=(1,1))

        self.dockAreaChart.addDock(self.descriptionData)
        self.dockAreaChart.addDock(self.profileDockX1,'left',self.descriptionData)
        self.dockAreaChart.addDock(self.profileDockY1,"right",self.profileDockX1)
        self.dockAreaChart.addDock(self.profileDockX2,"bottom",self.profileDockX1)
        self.dockAreaChart.addDock(self.profileDockY2,"bottom",self.profileDockY1)
        self.ui.horizontalLayoutGraphics.addWidget(self.dockAreaChart)
        
        self.dockAreaState = self.dockAreaChart.saveState()
        
        self.ui.comboBoxType.addItem("Manual")
        self.ui.comboBoxType.addItem("Online")
        self.ui.comboBoxType.addItem("Manual sum")
        self.ui.comboBoxType.setCurrentIndex(0)
    
        self.realTimeModeOn = False
        self.savedStateinterface = None

        self.setMode(ModeInterface.DEFFAULT)
    def setInfinityProgress(self, mode:bool):
        self.ui.progressBarTask.setMaximum(0 if mode else 100)
        self.ui.progressBarTask.setMinimum(0)
        self.ui.progressBarTask.setValue(-1 if mode else 0)

    def autoRangeAllProfileDocks(self):
        self.profileDockX1.autoRangeAll()
        self.profileDockX2.autoRangeAll()
        self.profileDockY1.autoRangeAll()
        self.profileDockY2.autoRangeAll()

    def keyPressEvent(self,event):
        #if event.key() == Qt.Key.Key_Right:
        #    self.__nextId__()
        #if event.key() == Qt.Key.Key_Left:
        #    self.__prevId__()
        if event.key() == Qt.Key.Key_Enter or event.key() == Qt.Key.Key_Return:
            if self.ui.spinBoxId.hasFocus():
                self.__setId__()
            if self.ui.spinBoxCountSum.hasFocus():
                self.__setCountSum()


    def __setId__(self):
        self.sigSetNewId.emit(self.ui.spinBoxId.value())
        self.ui.spinBoxId.clearFocus()
    def __setCountSum(self):
        self.sigSetNewCountSum.emit(self.ui.spinBoxCountSum.value())
        self.ui.spinBoxCountSum.clearFocus()

    def __nextId__(self):
        self.sigIterationValueId.emit(+1)

    def __prevId__(self):
        self.sigIterationValueId.emit(-1)
        
    def setMode(self, mode:ModeInterface):
        self.currentMode = mode
        self.dockAreaChart.setEnabled(mode.chartEnabled)
        self.ui.comboBoxType.setEnabled(mode.comboBoxTypeEnabled)
        self.ui.spinBoxId.setEnabled(mode.controlDataIdEnabled)
        self.ui.pushButtonNext.setEnabled(mode.controlDataIdEnabled)
        self.ui.pushButtonPrev.setEnabled(mode.controlDataIdEnabled)
        self.ui.spinBoxCountSum.setEnabled(mode.controlSumDataIdEnabled)

    def setButtonNextEnabled(self,enabled):
        self.ui.pushButtonNext.setEnabled(enabled)
    def setButtonPrevEnabled(self,enabled):
        self.ui.pushButtonPrev.setEnabled(enabled)
        
    def setBusyMode(self,mode):
        if mode:
            self.savedStateinterface = (
                self.dockAreaChart.isEnabled(),
                self.ui.comboBoxType.isEnabled(),
                self.ui.spinBoxId.isEnabled(),
                self.ui.pushButtonNext.isEnabled(),
                self.ui.pushButtonPrev.isEnabled(),
                self.ui.spinBoxCountSum.isEnabled(),
            )
            self.dockAreaChart.setEnabled(not mode)
            self.ui.comboBoxType.setEnabled(not mode)
            self.ui.spinBoxId.setEnabled(not mode)
            self.ui.pushButtonNext.setEnabled(not mode)
            self.ui.pushButtonPrev.setEnabled(not mode)
            self.ui.spinBoxCountSum.setEnabled(not mode)
        else:
            if self.savedStateinterface == None:
                return
            self.dockAreaChart.setEnabled(self.savedStateinterface[0])
            self.ui.comboBoxType.setEnabled(self.savedStateinterface[1])
            self.ui.spinBoxId.setEnabled(self.savedStateinterface[2])
            self.ui.pushButtonNext.setEnabled(self.savedStateinterface[3])
            self.ui.pushButtonPrev.setEnabled(self.savedStateinterface[4])
            self.ui.spinBoxCountSum.setEnabled(self.savedStateinterface[5])
    
    def setIdValue(self,id):
        self.ui.spinBoxId.setValue(id)
    def setRangeId(self,min,max):
        self.ui.spinBoxId.setMaximum(max)
        self.ui.spinBoxId.setMinimum(min)

    #def connectSignalIteration

    def setIndexListData(self,data):
        self.ui.comboBoxListData.addItems(data)
    
    def setData(self,dataX1,scaleTimeX1,delayX1,dataY1,scaleTimeY1,delayY1,dataX2,scaleTimeX2,delayX2,dataY2,scaleTimeY2,delayY2,scaleChannelToMM):
        self.profileDockX1.setData(dataX1, scaleTimeX1,scaleChannelToMM,delayX1)
        self.profileDockY1.setData(dataY1, scaleTimeY1,scaleChannelToMM,delayY1)
        self.profileDockX2.setData(dataX2, scaleTimeX2,scaleChannelToMM,delayX2)
        self.profileDockY2.setData(dataY2, scaleTimeY2,scaleChannelToMM,delayY2)
    def setDataInfo(self,text):
        self.descriptionData.setText(text)
    
    def __openViewGraphics__(self):
        self.viewGraphics = ViewGraphicsDialog(self.ui.centralwidget , not self.profileDockX1.isHidden(), not self.profileDockX2.isHidden(), not self.profileDockY1.isHidden() ,not self.profileDockY2.isHidden(), not self.descriptionData.isHidden())
        self.viewGraphics.getUI().checkBoxMCPX1.stateChanged.connect(lambda :self.__changeHiddenModeDock__(self.profileDockX1))
        self.viewGraphics.getUI().checkBoxMCPX2.stateChanged.connect(lambda :self.__changeHiddenModeDock__(self.profileDockX2))
        self.viewGraphics.getUI().checkBoxMCPY1.stateChanged.connect(lambda :self.__changeHiddenModeDock__(self.profileDockY1))
        self.viewGraphics.getUI().checkBoxMCPY2.stateChanged.connect(lambda :self.__changeHiddenModeDock__(self.profileDockY2))
        self.viewGraphics.getUI().checkBoxDataDescription.stateChanged.connect(lambda :self.__changeHiddenModeDock__(self.descriptionData))
        self.viewGraphics.show()
    
    def __changeHiddenModeDock__(self,dock):
        if dock.isHidden():
            dock.show()
        else:
            dock.hide()
        
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MainWindow()
    MainWindow.show()
    sys.exit(app.exec())
    
    
    
