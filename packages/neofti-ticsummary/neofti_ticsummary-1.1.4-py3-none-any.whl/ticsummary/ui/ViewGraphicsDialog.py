from PyQt6 import QtCore, QtGui, QtWidgets

class Ui_ViewGraphicsDialog(object):
    def setupUi(self, ViewGraphicsDialog):
        ViewGraphicsDialog.setObjectName("ViewGraphicsDialog")
        ViewGraphicsDialog.resize(158, 200)
        ViewGraphicsDialog.setMinimumSize(QtCore.QSize(140, 200))
        self.verticalLayout = QtWidgets.QVBoxLayout(ViewGraphicsDialog)
        self.verticalLayout.setObjectName("verticalLayout")
        self.checkBoxMCPX1 = QtWidgets.QCheckBox(ViewGraphicsDialog)
        self.checkBoxMCPX1.setObjectName("checkBoxMCPX1")
        self.verticalLayout.addWidget(self.checkBoxMCPX1)
        self.checkBoxMCPX2 = QtWidgets.QCheckBox(ViewGraphicsDialog)
        self.checkBoxMCPX2.setObjectName("checkBoxMCPX2")
        self.verticalLayout.addWidget(self.checkBoxMCPX2)
        self.checkBoxMCPY1 = QtWidgets.QCheckBox(ViewGraphicsDialog)
        self.checkBoxMCPY1.setObjectName("checkBoxMCPY1")
        self.verticalLayout.addWidget(self.checkBoxMCPY1)
        self.checkBoxMCPY2 = QtWidgets.QCheckBox(ViewGraphicsDialog)
        self.checkBoxMCPY2.setObjectName("checkBoxMCPY2")
        self.verticalLayout.addWidget(self.checkBoxMCPY2)
        self.checkBoxDataDescription = QtWidgets.QCheckBox(ViewGraphicsDialog)
        self.checkBoxDataDescription.setObjectName("checkBoxDataDescription")
        self.verticalLayout.addWidget(self.checkBoxDataDescription)
        self.pushButtonClose = QtWidgets.QPushButton(ViewGraphicsDialog)
        self.pushButtonClose.setObjectName("pushButtonClose")
        self.verticalLayout.addWidget(self.pushButtonClose)

        self.retranslateUi(ViewGraphicsDialog)
        QtCore.QMetaObject.connectSlotsByName(ViewGraphicsDialog)

    def retranslateUi(self, ViewGraphicsDialog):
        _translate = QtCore.QCoreApplication.translate
        ViewGraphicsDialog.setWindowTitle(_translate("ViewGraphicsDialog", "Edit plots"))
        self.checkBoxMCPX1.setText(_translate("ViewGraphicsDialog", "MCP X B1"))
        self.checkBoxMCPX2.setText(_translate("ViewGraphicsDialog", "MCP X B2"))
        self.checkBoxMCPY1.setText(_translate("ViewGraphicsDialog", "MCP Y B1"))
        self.checkBoxMCPY2.setText(_translate("ViewGraphicsDialog", "MCP Y B2"))
        self.checkBoxDataDescription.setText(_translate("ViewGraphicsDialog", "DATA DESCRIPTION"))
        self.pushButtonClose.setText(_translate("ViewGraphicsDialog", "Close"))


class ViewGraphicsDialog(QtWidgets.QDialog):
    ui: Ui_ViewGraphicsDialog
    def __init__(self, parent, checkBoxMCPX1Checked, checkBoxMCPX2Checked, checkBoxMCPY1Checked, checkBoxMCPY2Checked,checkBoxDataDescriptionChecked):
        super().__init__(parent)
        self.ui = Ui_ViewGraphicsDialog()
        self.ui.setupUi(self)
        self.ui.checkBoxMCPX1.setChecked(checkBoxMCPX1Checked)
        self.ui.checkBoxMCPX2.setChecked(checkBoxMCPX2Checked)
        self.ui.checkBoxMCPY1.setChecked(checkBoxMCPY1Checked)
        self.ui.checkBoxMCPY2.setChecked(checkBoxMCPY2Checked)
        self.ui.checkBoxDataDescription.setChecked(checkBoxDataDescriptionChecked)
        self.ui.pushButtonClose.clicked.connect(self.close)
    def close(self):
        self.accept()
    def getUI(self):
        return self.ui

if __name__ == "__main__":
    import sys
    
