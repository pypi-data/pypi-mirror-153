from typing import List
from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtWidgets import QMessageBox

from ticsummary import databaseMYSQL


class Ui_OpenSQLDataDialog(object):
    def setupUi(self, OpenSQLDataDialog):
        OpenSQLDataDialog.setObjectName("OpenSQLDataDialog")
        OpenSQLDataDialog.resize(701, 600)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(OpenSQLDataDialog)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.radioButtonSeveral = QtWidgets.QRadioButton(OpenSQLDataDialog)
        self.radioButtonSeveral.setChecked(True)
        self.radioButtonSeveral.setObjectName("radioButtonSeveral")
        self.verticalLayout.addWidget(self.radioButtonSeveral)
        self.radioButtonFromFirst = QtWidgets.QRadioButton(OpenSQLDataDialog)
        self.radioButtonFromFirst.setObjectName("radioButtonFromFirst")
        self.verticalLayout.addWidget(self.radioButtonFromFirst)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.verticalLayout_2.addLayout(self.horizontalLayout_2)
        self.tableViewData = QtWidgets.QTableWidget(OpenSQLDataDialog)
        self.tableViewData.setObjectName("tableViewData")
        self.verticalLayout_2.addWidget(self.tableViewData)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.pushButtonOpen = QtWidgets.QPushButton(OpenSQLDataDialog)
        self.pushButtonOpen.setObjectName("pushButtonOpen")
        self.horizontalLayout.addWidget(self.pushButtonOpen)
        self.verticalLayout_2.addLayout(self.horizontalLayout)

        self.retranslateUi(OpenSQLDataDialog)
        QtCore.QMetaObject.connectSlotsByName(OpenSQLDataDialog)

    def retranslateUi(self, OpenSQLDataDialog):
        _translate = QtCore.QCoreApplication.translate
        OpenSQLDataDialog.setWindowTitle(_translate("OpenSQLDataDialog", "Open data"))
        self.radioButtonSeveral.setText(_translate("OpenSQLDataDialog", "Selection of several data"))
        self.radioButtonFromFirst.setText(_translate("OpenSQLDataDialog", "Selection of several from the first"))
        self.pushButtonOpen.setText(_translate("OpenSQLDataDialog", "Open"))



class OpenSQLData():
    '''def __init__(self, parameters, funcCallback):
        self.dialog = QtWidgets.QDialog()
        self.ui = Ui_OpenSQLDataDialog()
        self.ui.setupUi(self.dialog)
        self.ui.tableViewData.setColumnCount(7)
        self.ui.tableViewData.setHorizontalHeaderLabels(('ID_Run','ACSN','Date&Time','TimeSlice B1','Delay B1','TimeSlice B2','Delay B2'))
        self.ui.tableViewData.setSelectionBehavior(QtWidgets.QTableWidget.SelectionBehavior.SelectRows)
        with databaseMYSQL.openConnection(parameters) as connector:
            self.ui.tableViewData.setRowCount(databaseMYSQL.getCountRecords(parameters.table, connector))
            rowTableIter = iter(range(0, self.ui.tableViewData.rowCount()))
            setItem = lambda tableViewData,str,row,column: tableViewData.setItem(
                row,
                column,
                QtWidgets.QTableWidgetItem(str)
            )
            with databaseMYSQL.getCursorWODataByConnector(parameters, connector) as cursor:
                for (id_RUN,ACSN,Date_Time,TimeSlice_B1, Delay_B1, TimeSlice_B2, Delay_B2) in cursor:
                    id = next(rowTableIter)
                    setItem(self.ui.tableViewData,str(id_RUN),id,0)
                    setItem(self.ui.tableViewData,str(ACSN),id,1)
                    setItem(self.ui.tableViewData,str(Date_Time),id,2)
                    setItem(self.ui.tableViewData,str(TimeSlice_B1),id,3)
                    setItem(self.ui.tableViewData,str(Delay_B1),id,4)
                    setItem(self.ui.tableViewData,str(TimeSlice_B2),id,5)
                    setItem(self.ui.tableViewData,str(Delay_B2),id,6)
        self.ui.radioButtonSeveral.toggled.connect(self.radioButtonSeveralToggled)
        self.ui.radioButtonFromFirst.toggled.connect(self.radioButtonFromFirstToggled)
        self.ui.pushButtonOpen.clicked.connect(self.pushButtonOpenClicked)
        self.funcCallBack = funcCallback'''
    
    def __init__(self, funcCallback, listData):
        self.dialog = QtWidgets.QDialog()
        self.ui = Ui_OpenSQLDataDialog()
        self.ui.setupUi(self.dialog)
        self.ui.tableViewData.setColumnCount(7)
        self.ui.tableViewData.setHorizontalHeaderLabels(('ID_Run','ACSN','Date&Time','TimeSlice B1','Delay B1','TimeSlice B2','Delay B2'))
        self.ui.tableViewData.setSelectionBehavior(QtWidgets.QTableWidget.SelectionBehavior.SelectRows)
        with databaseMYSQL.openConnection(parameters) as connector:
            self.ui.tableViewData.setRowCount(databaseMYSQL.getCountRecords(parameters.table, connector))
            rowTableIter = iter(range(0, self.ui.tableViewData.rowCount()))
            setItem = lambda tableViewData,str,row,column: tableViewData.setItem(
                row,
                column,
                QtWidgets.QTableWidgetItem(str)
            )
            with databaseMYSQL.getCursorWODataByConnector(parameters, connector) as cursor:
                for (id_RUN,ACSN,Date_Time,TimeSlice_B1, Delay_B1, TimeSlice_B2, Delay_B2) in cursor:
                    id = next(rowTableIter)
                    setItem(self.ui.tableViewData,str(id_RUN),id,0)
                    setItem(self.ui.tableViewData,str(ACSN),id,1)
                    setItem(self.ui.tableViewData,str(Date_Time),id,2)
                    setItem(self.ui.tableViewData,str(TimeSlice_B1),id,3)
                    setItem(self.ui.tableViewData,str(Delay_B1),id,4)
                    setItem(self.ui.tableViewData,str(TimeSlice_B2),id,5)
                    setItem(self.ui.tableViewData,str(Delay_B2),id,6)
        self.ui.radioButtonSeveral.toggled.connect(self.radioButtonSeveralToggled)
        self.ui.radioButtonFromFirst.toggled.connect(self.radioButtonFromFirstToggled)
        self.ui.pushButtonOpen.clicked.connect(self.pushButtonOpenClicked)
        self.funcCallBack = funcCallback 
    
    def show(self):
        self.dialog.exec()
    
    def radioButtonSeveralToggled(self, checked:bool):
        if checked:
            self.ui.tableViewData.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.ContiguousSelection)
            self.ui.tableViewData.clearSelection()
    def radioButtonFromFirstToggled(self, checked:bool):
        if checked:
            self.ui.tableViewData.setSelectionMode(QtWidgets.QAbstractItemView.SelectionMode.SingleSelection)
            self.ui.tableViewData.clearSelection()
    def pushButtonOpenClicked(self):
        selectedList = self.ui.tableViewData.selectionModel().selectedRows()
        selectedList[0].column
        if len(selectedList) <= 0:
            msqBox = QMessageBox()
            msqBox.setText("No data selected. \nPlease select data")
            msqBox.exec()
            return
        if self.ui.radioButtonSeveral.isChecked():
            #self.selectedRow = list
            resultData = list()
            for item in selectedList:
                resultData.append(int(self.ui.tableViewData.item(item.row(),0).data(0)))
            self.funcCallBack(resultData)
            self.dialog.close()
        if self.ui.radioButtonFromFirst.isChecked():
            for i in range(selectedList[0]+1, self.ui.tableViewData.model().rowCount()):
                selectedList.append(i)
            #self.selectedRow = list
            self.funcCallBack(selectedList)
            self.dialog.close()
    #def close(self):
