import pyqtgraph as pg
from pyqtgraph.dockarea import DockArea, Dock
from PyQt6 import QtWidgets,QtGui
import numpy as np

from ticsummary.ui.SettingsColorBarDialog import SettingsColorBarDialog

class ProfileBeamDock(Dock):
    def setData(self,data,scaleX,scaleY,delayX):
        stateAutoScale = (
            self.colorMapPlot.vb.getState(),
            self.intensityMapLinePlot.vb.getState(),
            self.projectionMapHistPlot.vb.getState()
        )

        self.scaleX = scaleX
        self.scaleY = scaleY
        self.imageData = data
        intensity = np.sum(data,axis=1)
        projectionX = np.transpose(data).sum(axis=1)
        self.minProfileY = -(scaleY*np.size(projectionX)/2)+scaleY/2
        self.maxProfileY = +(scaleY*np.size(projectionX)/2)-scaleY/2
        projectionY = np.arange(self.minProfileY,self.maxProfileY,scaleY)
        self.profileSum = np.sum(intensity)
        self.histogramItem.setOpts(y=projectionY,width=projectionX)
        self.image.setImage(data)
        timeX = list()
        for i in range (0,len(data)):
            timeX.append(delayX+i*scaleX)
        self.linePlotIntensityMcpitem.setData(x=timeX,y=intensity.tolist()) #np.arange(0,len(data)*scaleX,scaleX)
        tr = QtGui.QTransform()
        tr.scale(scaleX,scaleY)
        tr.translate(0, -np.size(projectionX)/2)
        self.image.setTransform(tr)
        self.bar._update_items()
        self.setOrientation("horizontal")
        
        self.__setValueCrossHairProfile__(0,0,0)

        self.bar.setMaxMinImage(np.min(data),np.max(data))

        self.colorMapPlot.vb.setState(stateAutoScale[0])
    def autoRangeAll(self):
        self.colorMapPlot.vb.enableAutoRange()
    def updateStyle(self):
        Dock.updateStyle(self)
        self.setOrientation("horizontal")
    def __init__(self,keyEventHandler, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.keyEventHandler = keyEventHandler
        self.__initGraph__()
    def keyPressEvent(self,event):
        self.keyEventHandler(event)

    class __ColorBarItemWithDoubleClick__(pg.ColorBarItem):
        def __init__(self,parent, *args, **kwargs):
            pg.ColorBarItem.__init__(self, *args, **kwargs)
            self.autoscale = True
            self.parent = parent
            # creating a mouse double click event
        def mouseDoubleClickEvent(self, e):
            self.settingsDialog = SettingsColorBarDialog(self.parent,*self.levels(),self.cmap.name,self.autoscale,self.__setNewparameter__)
            self.settingsDialog.show()
        def __setNewparameter__(self,max,min,cmapstr,autoscale):
            if cmapstr[0:3] == "CET":
                cmap = pg.colormap.get(cmapstr)
            else:
                cmap = pg.colormap.getFromMatplotlib(cmapstr)
            self.setCmap(cmap)
            self._update_items()
            self.maxUser = max
            self.minUser = min
            self.autoscale=autoscale
            if autoscale:
                self.setLevels(values=(self.minImage,self.maxImage))
            else:
                self.setLevels(values=(min,max))
        def setMaxMinImage(self,min,max):
            self.minImage = min
            self.maxImage = max
            if self.autoscale:
                self.setLevels(values=(self.minImage,self.maxImage))
            else:
                self.setLevels(values=(self.minUser,self.maxUser))

    def __initGraph__(self):
        labelAxisStyle = {'color': '#FFF', 'font-size': '8pt'}
        titlePlotStyle = {'color': '#FFF', 'font-size': '14pt'}

        #self.hideTitleBar()
        
        ##Init mani layout and add into dock
        self.layoutPlot = pg.GraphicsLayoutWidget(show=True)
        #self.layoutPlot.scene().sigMouseMoved.connect(self.mouseMoved)
        self.addWidget(self.layoutPlot)

        self.colorMapPlot:pg.PlotItem = self.layoutPlot.addPlot(row=1,col=1,rowspan=1,colspan=1)
        self.intensityMapLinePlot = self.layoutPlot.addPlot(row=2,col=1,rowspan=1,colspan=1)
        self.projectionMapHistPlot:pg.PlotItem = self.layoutPlot.addPlot(row=1,col=2,rowspan=1,colspan=1)

        self.colorMapPlot.setMouseEnabled(x=False, y=False)
        self.intensityMapLinePlot.setMouseEnabled(x=False, y=False)
        self.projectionMapHistPlot.setMouseEnabled(x=False, y=False)

        self.colorMapPlot.enableAutoRange(x=True, y=True)
        self.intensityMapLinePlot.enableAutoRange(x=True, y=True)
        self.projectionMapHistPlot.enableAutoRange(x=True, y=True)

        self.layoutPlot.ci.layout.setColumnStretchFactor(0,1)
        self.layoutPlot.ci.layout.setColumnStretchFactor(1,10)
        self.layoutPlot.ci.layout.setColumnStretchFactor(2,2)
        
        self.layoutPlot.ci.layout.setRowStretchFactor(0,1)
        self.layoutPlot.ci.layout.setRowStretchFactor(1,20)
        self.layoutPlot.ci.layout.setRowStretchFactor(2,7)

        self.cmap = pg.colormap.getFromMatplotlib("nipy_spectral")
        self.bar = self.__ColorBarItemWithDoubleClick__(self, interactive=True, colorMap=self.cmap)
        #self.bar.setFixedWidth(40)
        self.image = pg.ImageItem()
        self.bar.setImageItem(self.image)
        self.colorMapPlot.addItem(self.image)
        self.layoutPlot.addItem(self.bar,1,0,2,1)

        #self.vLine = pg.InfiniteLine(angle=90, movable=False)
        #self.hLine = pg.InfiniteLine(angle=0, movable=False)
        #self.colorMapPlot.addItem(self.vLine, ignoreBounds=True)
        #self.colorMapPlot.addItem(self.hLine, ignoreBounds=True)
        self.proxy = pg.SignalProxy(self.colorMapPlot.scene().sigMouseMoved, rateLimit=60, slot=self.__mouseMoved__)
        self.labelDescription = pg.LabelItem(justify='left')
        self.labelDescription.setText("Sum=0 X=0 Y=0 Count=0",size="12pt")
        self.layoutPlot.addItem(self.labelDescription, row=0,col=1,rowspan=1,colspan=3)

        self.intensityMapLinePlot.setXLink(self.colorMapPlot)
        self.colorMapPlot.setYLink(self.projectionMapHistPlot)
        #self.projectionMapHistPlot.setFixedWidth(150)
        self.histogramItem = pg.BarGraphItem(x0 = 0, y = (), height = 0.6, width=(), brush ='g')
        self.projectionMapHistPlot.addItem(self.histogramItem)

        font=QtGui.QFont()
        font.setPixelSize(10)

        self.colorMapPlot.getAxis("bottom").setTickFont(font)
        self.colorMapPlot.getAxis("left").setTickFont(font)
        self.colorMapPlot.getAxis("left").setWidth(70)
        self.bar.getAxis("right").setTickFont(font)


        #self.colorMapPlot.setTitle(self.name(), **titlePlotStyle)
        self.colorMapPlot.setLabel('left', "position", units="mm", **labelAxisStyle)
        self.colorMapPlot.setLabel('bottom', "time", units="sec", **labelAxisStyle)
        #self.projectionMapHistPlot.setTitle("Projection",**titlePlotStyle)
        self.projectionMapHistPlot.setLabel('left',"position",units="mm",**labelAxisStyle)
        self.projectionMapHistPlot.setLabel('bottom',"count",units="qty",**labelAxisStyle)
        #self.intensityMapLinePlot.setTitle("Intensity", **self.titlePlotStyle)
        self.intensityMapLinePlot.setLabel('left',"count",units="qty",**labelAxisStyle)
        self.intensityMapLinePlot.setLabel('bottom',"time",units="sec",**labelAxisStyle)

        self.linePlotIntensityMcpitem:pg.PlotDataItem = self.intensityMapLinePlot.plot(pen=(0,120,120),name="Intensity")
        self.histPlotProjectionMcpItem:pg.PlotDataItem = self.projectionMapHistPlot.plot(pen=(0,120,120),name='Projection')

    def __setValueCrossHairProfile__(self,x,y,count):
        self.labelDescription.setText("Sum={0:.0f} X={1:.0e} Y={2:.0f} Count={3:.0f}".format(self.profileSum,x,y,count),size="10pt")

    def __mouseMoved__(self,evt):
        pos = evt[0]  ## using signal proxy turns original arguments into a tuple
        if self.colorMapPlot.sceneBoundingRect().contains(pos):
            mousePoint = self.colorMapPlot.vb.mapSceneToView(pos)
            indexX = int(mousePoint.x() / self.scaleX)
            indexY = int(mousePoint.y())
            if indexX >= 0 and indexX < np.size(self.imageData,0):
                if indexY >= 0 and indexY < np.size(self.imageData,1):
                    self.__setValueCrossHairProfile__(indexX * self.scaleX,indexY,self.imageData[indexX][indexY])
                    #self.vLine.setPos(indexX * self.scaleX + self.scaleX/2)
                    #self.hLine.setPos(indexY + 0.5)
    
