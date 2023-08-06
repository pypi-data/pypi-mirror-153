from PyQt6 import QtCore, QtGui, QtWidgets
from PyQt6.QtCore import QObject, pyqtSignal, pyqtSlot 
from PyQt6.QtWidgets import QFileDialog, QMessageBox
from ticsummary import databaseMYSQL
import json
import os
from pathlib import Path


class Ui_ConnectionConfigurationDialog(object):
    def setupUi(self, ConnectionConfigurationDialog):
        ConnectionConfigurationDialog.setObjectName("ConnectionConfigurationDialog")
        ConnectionConfigurationDialog.setWindowModality(QtCore.Qt.WindowModality.ApplicationModal)
        ConnectionConfigurationDialog.resize(488, 300)
        ConnectionConfigurationDialog.setModal(True)
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(ConnectionConfigurationDialog)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label = QtWidgets.QLabel(ConnectionConfigurationDialog)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.label_2 = QtWidgets.QLabel(ConnectionConfigurationDialog)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.label_3 = QtWidgets.QLabel(ConnectionConfigurationDialog)
        self.label_3.setObjectName("label_3")
        self.verticalLayout_2.addWidget(self.label_3)
        self.label_4 = QtWidgets.QLabel(ConnectionConfigurationDialog)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_2.addWidget(self.label_4)
        self.label_5 = QtWidgets.QLabel(ConnectionConfigurationDialog)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_2.addWidget(self.label_5)
        self.label_6 = QtWidgets.QLabel(ConnectionConfigurationDialog)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_2.addWidget(self.label_6)
        self.horizontalLayout_3.addLayout(self.verticalLayout_2)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.lineEditHost = QtWidgets.QLineEdit(ConnectionConfigurationDialog)
        self.lineEditHost.setObjectName("lineEditHost")
        self.verticalLayout.addWidget(self.lineEditHost)
        self.lineEditDB = QtWidgets.QLineEdit(ConnectionConfigurationDialog)
        self.lineEditDB.setObjectName("lineEditDB")
        self.verticalLayout.addWidget(self.lineEditDB)
        self.spinBoxPort = QtWidgets.QSpinBox(ConnectionConfigurationDialog)
        self.spinBoxPort.setButtonSymbols(QtWidgets.QAbstractSpinBox.ButtonSymbols.NoButtons)
        self.spinBoxPort.setMaximum(9999)
        self.spinBoxPort.setObjectName("spinBoxPort")
        self.verticalLayout.addWidget(self.spinBoxPort)
        self.lineEditUser = QtWidgets.QLineEdit(ConnectionConfigurationDialog)
        self.lineEditUser.setObjectName("lineEditUser")
        self.verticalLayout.addWidget(self.lineEditUser)
        self.lineEditPassword = QtWidgets.QLineEdit(ConnectionConfigurationDialog)
        self.lineEditPassword.setObjectName("lineEditPassword")
        self.verticalLayout.addWidget(self.lineEditPassword)
        self.lineEditTable = QtWidgets.QLineEdit(ConnectionConfigurationDialog)
        self.lineEditTable.setObjectName("lineEditTable")
        self.verticalLayout.addWidget(self.lineEditTable)
        self.horizontalLayout_3.addLayout(self.verticalLayout)
        self.verticalLayout_3.addLayout(self.horizontalLayout_3)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButtonWriteConf = QtWidgets.QPushButton(ConnectionConfigurationDialog)
        self.pushButtonWriteConf.setObjectName("pushButtonWriteConf")
        self.horizontalLayout.addWidget(self.pushButtonWriteConf)
        self.pushButtonReadConf = QtWidgets.QPushButton(ConnectionConfigurationDialog)
        self.pushButtonReadConf.setObjectName("pushButtonReadConf")
        self.horizontalLayout.addWidget(self.pushButtonReadConf)
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.verticalLayout_3.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.pushButtonSave = QtWidgets.QPushButton(ConnectionConfigurationDialog)
        self.pushButtonSave.setObjectName("pushButtonSave")
        self.horizontalLayout_2.addWidget(self.pushButtonSave)
        self.pushButtonCancel = QtWidgets.QPushButton(ConnectionConfigurationDialog)
        self.pushButtonCancel.setObjectName("pushButtonCancel")
        self.horizontalLayout_2.addWidget(self.pushButtonCancel)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)

        self.retranslateUi(ConnectionConfigurationDialog)
        QtCore.QMetaObject.connectSlotsByName(ConnectionConfigurationDialog)

    def retranslateUi(self, ConnectionConfigurationDialog):
        _translate = QtCore.QCoreApplication.translate
        ConnectionConfigurationDialog.setWindowTitle(_translate("ConnectionConfigurationDialog", "Connection configuration"))
        self.label.setText(_translate("ConnectionConfigurationDialog", "Host"))
        self.label_2.setText(_translate("ConnectionConfigurationDialog", "Database"))
        self.label_3.setText(_translate("ConnectionConfigurationDialog", "Port"))
        self.label_4.setText(_translate("ConnectionConfigurationDialog", "User"))
        self.label_5.setText(_translate("ConnectionConfigurationDialog", "Password"))
        self.label_6.setText(_translate("ConnectionConfigurationDialog", "Table"))
        self.pushButtonWriteConf.setText(_translate("ConnectionConfigurationDialog", "Write configuration"))
        self.pushButtonReadConf.setText(_translate("ConnectionConfigurationDialog", "Read configuration"))
        self.pushButtonSave.setText(_translate("ConnectionConfigurationDialog", "Save"))
        self.pushButtonCancel.setText(_translate("ConnectionConfigurationDialog", "Cancel"))


        
class ConnectionConfiguration(QtWidgets.QDialog):
    def __init__(self,parent=None, parameters = None):
        self.ui = Ui_ConnectionConfigurationDialog()
        super().__init__(parent)
        self.ui.setupUi(self)
        self.__initSignal__()

        if not parameters is None:
            self.__setParametersInUI__(
                parameters.host,
                parameters.database,
                parameters.port,
                parameters.user,
                parameters.password,
                parameters.table)
    
    def __initSignal__(self):
        self.ui.pushButtonReadConf.clicked.connect(self.__readConfiguration__)
        self.ui.pushButtonWriteConf.clicked.connect(self.__writeConfiguration__)
        self.ui.pushButtonCancel.clicked.connect(self.__cancel__)
        self.ui.pushButtonSave.clicked.connect(self.__save__)

    def __readConfiguration__(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', os.path.expanduser("~"), "Json files (*.json)")[0]
        try:
            with open(fname, "r") as file:
                data = json.load(file)
            
            self.__setParametersInUI__(
                data['Settings']['SQL']['Host'],
                data['Settings']['SQL']['Database'],
                int(data['Settings']['SQL']['Port']),
                data['Settings']['SQL']['Username'],
                data['Settings']['SQL']['Password'],
                data['Settings']['SQL']['Table'])
        except Exception as e:
            print("Error while write configuration:", e)
            
    def __setParametersInUI__(self, host, db, port, username, password, table):
        self.ui.lineEditHost.setText(host)
        self.ui.lineEditDB.setText(db)
        self.ui.spinBoxPort.setValue(port)
        self.ui.lineEditUser.setText(username)
        self.ui.lineEditPassword.setText(password)
        self.ui.lineEditTable.setText(table)

    def __getParametersFromUI__(self):
        return databaseMYSQL.ParametersConnection(
            user = self.ui.lineEditUser.text(),
            password = self.ui.lineEditPassword.text(),
            host = self.ui.lineEditHost.text(),
            database = self.ui.lineEditDB.text(),
            table = self.ui.lineEditTable.text(),
            port = self.ui.spinBoxPort.value())
        
    def __writeConfiguration__(self):
        try:
            fname = QFileDialog.getSaveFileName(self, 'Save file', os.path.dirname(os.path.realpath(__file__)), "Json files (*.json)")[0]
            toJson = {'Host':self.ui.lineEditHost.text(), 'Database':self.ui.lineEditDB.text(), 'Port':str(self.ui.spinBoxPort.value()), 'User':self.ui.lineEditUser.text(), 'Password':self.ui.lineEditPassword.text(), 'Table':self.ui.lineEditTable.text()}
            with open(fname, "w") as file:
                json.dump(toJson, file)
        except Exception as e:
            print("Error while write configuration:", e)
            
    def __checkConnection__(self):
        return databaseMYSQL.parametersIsValid(self.__getParametersFromUI__())
    
    def getNewParameters(self):
        return self.__getParametersFromUI__()

    def __save__(self):
        try:
            if not (self.__checkConnection__()): raise Exception('Parameters is not valid')
            self.accept()
        except TimeoutError as e:
            msgBox = QMessageBox(parent=self)
            msgBox.setText("Connection is unvalid: Timeout error")
            msgBox.setWindowTitle("Status connection")
            msgBox.exec()
        except Exception as e:
            msgBox = QMessageBox(parent=self)
            msgBox.setText("Connection is unvalid: {0}".format(e))
            msgBox.setWindowTitle("Status connection")
            msgBox.exec()

    def __cancel__(self):
        self.reject()


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    connectionConfiguration = ConnectionConfiguration()
    connectionConfiguration.show()
    sys.exit(app.exec())
    
    


