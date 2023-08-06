from PyQt6 import QtCore, QtGui, QtWidgets   
from ticsummary.model import Model

class EntryPoint:    
    def run(self):
        import sys
        app = QtWidgets.QApplication(sys.argv)
        model = Model()
        sys.exit(app.exec())

def startup():
    entryPoint = EntryPoint()
    entryPoint.run()
    
if __name__ == "__main__":
    startup()