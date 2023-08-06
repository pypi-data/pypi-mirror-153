from PyQt6 import QtCore, QtGui, QtWidgets
from pkg_resources import resource_listdir,resource_filename
import ticsummary.ui.images as resImages
import pyqtgraph as pg

class Ui_DialogSettingsColorBar(object):
    def setupUi(self, DialogSettingsColorBar):
        DialogSettingsColorBar.setObjectName("DialogSettingsColorBar")
        DialogSettingsColorBar.resize(182, 132)
        DialogSettingsColorBar.setMaximumSize(QtCore.QSize(182, 132))
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(DialogSettingsColorBar)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.label_4 = QtWidgets.QLabel(DialogSettingsColorBar)
        self.label_4.setObjectName("label_4")
        self.verticalLayout_2.addWidget(self.label_4)
        self.label = QtWidgets.QLabel(DialogSettingsColorBar)
        self.label.setObjectName("label")
        self.verticalLayout_2.addWidget(self.label)
        self.label_2 = QtWidgets.QLabel(DialogSettingsColorBar)
        self.label_2.setObjectName("label_2")
        self.verticalLayout_2.addWidget(self.label_2)
        self.horizontalLayout_2.addLayout(self.verticalLayout_2)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.checkBoxAutoscale = QtWidgets.QCheckBox(DialogSettingsColorBar)
        self.checkBoxAutoscale.setText("")
        self.checkBoxAutoscale.setObjectName("checkBoxAutoscale")
        self.verticalLayout.addWidget(self.checkBoxAutoscale)
        self.spinBoxMax = pg.SpinBox(value=0, int=True, dec=True, minStep=1, step=1)

        self.verticalLayout.addWidget(self.spinBoxMax)
        self.spinBoxMin = pg.SpinBox(value=0, int=True, dec=True, minStep=1, step=1)

        self.verticalLayout.addWidget(self.spinBoxMin)
        self.horizontalLayout_2.addLayout(self.verticalLayout)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.horizontalLayout_5 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_5.setObjectName("horizontalLayout_5")
        self.label_3 = QtWidgets.QLabel(DialogSettingsColorBar)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout_5.addWidget(self.label_3)
        self.comboBoxColor = QtWidgets.QComboBox(DialogSettingsColorBar)
        self.comboBoxColor.setObjectName("comboBoxColor")
        self.horizontalLayout_5.addWidget(self.comboBoxColor)
        self.verticalLayout_3.addLayout(self.horizontalLayout_5)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        spacerItem = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Policy.Expanding, QtWidgets.QSizePolicy.Policy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.pushButtonApply = QtWidgets.QPushButton(DialogSettingsColorBar)
        self.pushButtonApply.setObjectName("pushButtonApply")
        self.horizontalLayout.addWidget(self.pushButtonApply)
        self.pushButtonSave = QtWidgets.QPushButton(DialogSettingsColorBar)
        self.pushButtonSave.setObjectName("pushButtonSave")
        self.horizontalLayout.addWidget(self.pushButtonSave)
        self.pushButtonCancel = QtWidgets.QPushButton(DialogSettingsColorBar)
        self.pushButtonCancel.setObjectName("pushButtonCancel")
        self.horizontalLayout.addWidget(self.pushButtonCancel)
        self.verticalLayout_3.addLayout(self.horizontalLayout)

        self.retranslateUi(DialogSettingsColorBar)
        QtCore.QMetaObject.connectSlotsByName(DialogSettingsColorBar)

    def retranslateUi(self, DialogSettingsColorBar):
        _translate = QtCore.QCoreApplication.translate
        DialogSettingsColorBar.setWindowTitle(_translate("DialogSettingsColorBar", "Settings color bar"))
        self.label_4.setText(_translate("DialogSettingsColorBar", "Autoscale"))
        self.label.setText(_translate("DialogSettingsColorBar", "Max"))
        self.label_2.setText(_translate("DialogSettingsColorBar", "Min"))
        self.label_3.setText(_translate("DialogSettingsColorBar", "Color"))
        self.pushButtonApply.setText(_translate("DialogSettingsColorBar", "Apply"))
        self.pushButtonSave.setText(_translate("DialogSettingsColorBar", "Save"))
        self.pushButtonCancel.setText(_translate("DialogSettingsColorBar", "Cancel"))

class SettingsColorBarDialog(QtWidgets.QDialog):
    def __init__(self,parent,minValue,maxValue,cmap,autoscale,funcSetNewParameters):
        super().__init__(parent)
        self.ui = Ui_DialogSettingsColorBar()
        self.ui.setupUi(self)
        
        self.ui.pushButtonApply.clicked.connect(self.apply)
        self.ui.pushButtonSave.clicked.connect(self.save)
        self.ui.pushButtonCancel.clicked.connect(self.cancel)
        self.ui.checkBoxAutoscale.stateChanged.connect(self.setAutoscale)
        
        self.oldCmap = cmap
        self.oldMaxvalue = maxValue
        self.oldMinValue = minValue
        self.oldAutoscale = autoscale
        
        self.ui.checkBoxAutoscale.setChecked(autoscale)
        
        self.ui.comboBoxColor.setIconSize(QtCore.QSize(65,20))
        listImageRaw = resource_listdir(resImages.__name__, "")
        listImage = list()
        for file in listImageRaw:
            if 'jpg' in file:
                listImage.append(file)
        
        for image in listImage:
            self.ui.comboBoxColor.addItem(QtGui.QIcon(resource_filename(resImages.__name__,image)), image.replace('.jpg',''))
        
        self.ui.comboBoxColor.setCurrentIndex(listImage.index('{0}.jpg'.format(cmap)))
        self.funcSetNewParameters = funcSetNewParameters
        self.ui.spinBoxMax.setValue(maxValue)
        self.ui.spinBoxMin.setValue(minValue)
    def apply(self):
        self.funcSetNewParameters(self.ui.spinBoxMax.value(),self.ui.spinBoxMin.value(),self.ui.comboBoxColor.currentText(),self.ui.checkBoxAutoscale.isChecked())
    def save(self):
        self.funcSetNewParameters(self.ui.spinBoxMax.value(),self.ui.spinBoxMin.value(),self.ui.comboBoxColor.currentText(),self.ui.checkBoxAutoscale.isChecked())
        self.accept()
    def cancel(self):
        self.funcSetNewParameters(self.oldMaxvalue,self.oldMinValue,self.oldCmap,self.oldAutoscale)
        self.reject()
    def setAutoscale(self,value):
        self.ui.spinBoxMax.setEnabled(0==value)
        self.ui.spinBoxMin.setEnabled(0==value)
        
if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    set = SettingsColorBarDialog(0,100,100)
    set.show()
    sys.exit(app.exec())