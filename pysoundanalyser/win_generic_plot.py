# -*- coding: utf-8 -*- 
#   Copyright (C) 2010-2024 Samuele Carcagno <sam.carcagno@gmail.com>
#   This file is part of pysoundanalyser

#    pysoundanalyser is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.

#    pysoundanalyser is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.

#    You should have received a copy of the GNU General Public License
#    along with pysoundanalyser.  If not, see <http://www.gnu.org/licenses/>.

from .pyqtver import*

import matplotlib
matplotlib.rcParams['path.simplify'] = False

if pyqtversion == 5:
    from PyQt5 import QtGui, QtCore
    from PyQt5.QtGui import QDoubleValidator, QIcon
    from PyQt5.QtWidgets import QAction, QCheckBox, QColorDialog, QComboBox, QGridLayout, QHBoxLayout, QInputDialog, QLabel, QLineEdit, QMainWindow, QVBoxLayout, QWidget
    from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
    from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
    matplotlib.rcParams['backend'] = "Qt5Agg"
elif pyqtversion == 6:
    from PyQt6 import QtGui, QtCore
    from PyQt6.QtGui import QAction, QDoubleValidator, QIcon
    from PyQt6.QtWidgets import QCheckBox, QColorDialog, QComboBox, QGridLayout, QHBoxLayout, QInputDialog, QLabel, QLineEdit, QMainWindow, QVBoxLayout, QWidget
    from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
    from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
    matplotlib.rcParams['backend'] = "Qt5Agg"
    
# Matplotlib Figure object
from matplotlib.figure import Figure

from matplotlib.widgets import Cursor
from matplotlib import font_manager
from .dialog_get_font import*
from .utility_functions import*
import numpy as np

class genericPlot(QMainWindow):
    def __init__(self, parent, prm):
        QMainWindow.__init__(self, parent)
        self.setAttribute(QtCore.Qt.WidgetAttribute.WA_DeleteOnClose)
        self.prm = prm
        self.currLocale = self.parent().prm['appData']['currentLocale']
        self.currLocale.setNumberOptions(self.currLocale.NumberOption.OmitGroupSeparator | self.currLocale.NumberOption.RejectGroupSeparator)

        #define some parameters before axes creation
        self.canvasColor = scaleRGBTo01(self.prm['pref']['canvasColor'])
        self.backgroundColor = scaleRGBTo01(self.prm['pref']['backgroundColor'])
        self.axesColor = scaleRGBTo01(self.prm['pref']['axes_color'])
        self.tickLabelColor = scaleRGBTo01(self.prm['pref']['tick_label_color'])
        self.gridColor = scaleRGBTo01(self.prm['pref']['grid_color'])
        self.axesLabelColor = scaleRGBTo01(self.prm['pref']['axes_label_color'])
        self.labelFontFamily = self.prm['pref']['label_font_family']
        self.labelFontWeight = self.prm['pref']['label_font_weight']
        self.labelFontStyle = self.prm['pref']['label_font_style']
        self.labelFontSize = self.prm['pref']['label_font_size']
        self.labelFont = font_manager.FontProperties(family=self.labelFontFamily,
                                                     weight=self.labelFontWeight,
                                                     style= self.labelFontStyle,
                                                     size=self.labelFontSize)
        
        self.majorTickLength = self.prm['pref']['major_tick_length']
        self.majorTickWidth = self.prm['pref']['major_tick_width']
        self.minorTickLength = self.prm['pref']['minor_tick_length']
        self.minorTickWidth = self.prm['pref']['minor_tick_width']
        self.tickLabelFontFamily = self.prm['pref']['tick_label_font_family']
        self.tickLabelFontWeight = self.prm['pref']['tick_label_font_weight']
        self.tickLabelFontStyle = self.prm['pref']['tick_label_font_style']
        self.tickLabelFontSize = self.prm['pref']['tick_label_font_size']
        self.tickLabelFont = font_manager.FontProperties(family=self.tickLabelFontFamily,
                                                         weight=self.tickLabelFontWeight,
                                                         style= self.tickLabelFontStyle,
                                                         size=self.tickLabelFontSize)
        self.xAxisLabel = ''
        self.yAxisLabel = ''
        self.dpi = self.prm['pref']['dpi']
        self.spinesLineWidth = self.prm['pref']['spines_line_width']
        self.gridLineWidth = self.prm['pref']['grid_line_width']

        self.mw = QWidget(self)
        self.vbl = QVBoxLayout(self.mw)
        self.fig = Figure(facecolor=self.canvasColor, dpi=self.dpi)
        self.axes = self.fig.add_subplot(111, facecolor=self.backgroundColor)
       
        self.createBaseMenus()
        self.createAdditionalMenus()
        self.defineMenusLayout()
        self.canvas = FigureCanvas(self.fig)
        self.canvas.setParent(self.mw)
       
        self.ntb = NavigationToolbar(self.canvas, self.mw)
        self.gridOn = QCheckBox(self.tr('Grid'))
        self.gridOn.setChecked(self.prm['pref']['grid'])
        self.gridOn.stateChanged[int].connect(self.toggleGrid)
        self.setBaseFigureProperties()
        self.gridBox = QGridLayout()
        self.createBaseControlWidgets()

        self.createAdditionalControlWidgets()
        self.defineGridBoxLayout()

        self.ntbBox = QHBoxLayout()
        self.ntbBox.addWidget(self.ntb)
        self.ntbBox.addWidget(self.gridOn)
        
        self.vbl.addWidget(self.canvas)
        self.vbl.addLayout(self.ntbBox)
        self.vbl.addLayout(self.gridBox)
        self.mw.setFocus()
        self.setCentralWidget(self.mw)
        self.show()
        self.canvas.draw()


    def createBaseControlWidgets(self):
        self.xminLabel = QLabel(self.tr('xmin'))
        self.xminWidget = QLineEdit(self.currLocale.toString(self.axes.get_xlim()[0]))               
        self.xminWidget.setValidator(QDoubleValidator(self))
        self.xmaxLabel = QLabel(self.tr('xmax'))
        self.xmaxWidget = QLineEdit(self.currLocale.toString(self.axes.get_xlim()[1]))
        self.xmaxWidget.setValidator(QDoubleValidator(self))
        self.yminLabel = QLabel(self.tr('ymin'))
        self.yminWidget = QLineEdit(self.currLocale.toString(self.axes.get_ylim()[0])) 
        self.yminWidget.setValidator(QDoubleValidator(self))
        self.ymaxLabel = QLabel(self.tr('ymax'))
        self.ymaxWidget = QLineEdit(self.currLocale.toString(self.axes.get_ylim()[1])) 
        self.ymaxWidget.setValidator(QDoubleValidator(self))
        self.xminWidget.editingFinished.connect(self.onAxesChange)
        self.xmaxWidget.editingFinished.connect(self.onAxesChange)
        self.yminWidget.editingFinished.connect(self.onAxesChange)
        self.ymaxWidget.editingFinished.connect(self.onAxesChange)

    def createAdditionalControlWidgets(self):
        pass
  
    def defineGridBoxLayout(self):
        self.gridBox.addWidget(self.xminLabel, 0, 0)
        self.gridBox.addWidget(self.xminWidget, 0, 1)
        self.gridBox.addWidget(self.xmaxLabel, 0, 2)
        self.gridBox.addWidget(self.xmaxWidget, 0, 3)
        self.gridBox.addWidget(self.yminLabel, 1, 0)
        self.gridBox.addWidget(self.yminWidget, 1, 1)
        self.gridBox.addWidget(self.ymaxLabel, 1, 2)
        self.gridBox.addWidget(self.ymaxWidget, 1, 3)
    def createBaseMenus(self):
        self.menubar = self.menuBar()
        exitAction = QAction(QIcon('icons/exit.png'), self.tr('Exit'), self)
        exitAction.setShortcut('Ctrl+Q')
        exitAction.setStatusTip(self.tr('Exit application'))
        exitAction.triggered.connect(self.close)
        self.statusBar()
        #FILE MENU
        self.fileMenu = self.menubar.addMenu(self.tr('&File'))
        self.fileMenu.addAction(exitAction)

        #EDIT MENU
        self.editMenu = self.menubar.addMenu(self.tr('&Edit'))
        #LINE Properties sub-menu
        self.linePropertiesMenu = self.editMenu.addMenu(self.tr('&Line Properties'))

        self.editMajorTickLengthAction = QAction(self.tr('Major Tick Length'), self)
        self.editMajorTickLengthAction.triggered.connect(self.onChangeMajorTickLength)

        self.editMajorTickWidthAction = QAction(self.tr('Major Tick Width'), self)
        self.editMajorTickWidthAction.triggered.connect(self.onChangeMajorTickWidth)

        self.editMinorTickLengthAction = QAction(self.tr('Minor Tick Length'), self)
        self.editMinorTickLengthAction.triggered.connect(self.onChangeMinorTickLength)

        self.editMinorTickWidthAction = QAction(self.tr('Minor Tick Width'), self)
        self.editMinorTickWidthAction.triggered.connect(self.onChangeMinorTickWidth)

        self.editGridLineWidthAction = QAction(self.tr('Grid Line Width'), self)
        self.editGridLineWidthAction.triggered.connect(self.onChangeGridLineWidth)

        self.editSpinesLineWidthAction = QAction(self.tr('Spines Line Width'), self)
        self.editSpinesLineWidthAction.triggered.connect(self.onChangeSpinesLineWidth)

        #COLOR Properties sub-menu
        self.colorPropertiesMenu = self.editMenu.addMenu(self.tr('&Color Properties'))

        self.editBackgroundColorAction = QAction(self.tr('Background Color'), self)
        self.editBackgroundColorAction.triggered.connect(self.onChangeBackgroundColor)

        self.editCanvasColorAction = QAction(self.tr('Canvas Color'), self)
        self.editCanvasColorAction.triggered.connect(self.onChangeCanvasColor)

        self.editAxesColorAction = QAction(self.tr('Axes Color'), self)
        self.editAxesColorAction.triggered.connect(self.onChangeAxesColor)

        self.editGridColorAction = QAction(self.tr('Grid Color'), self)
        self.editGridColorAction.triggered.connect(self.onChangeGridColor)

        self.editTickLabelColorAction = QAction(self.tr('Tick Labels Color'), self)
        self.editTickLabelColorAction.triggered.connect(self.onChangeTickLabelColor)

        self.editAxesLabelColorAction = QAction(self.tr('Axes Labels Color'), self)
        self.editAxesLabelColorAction.triggered.connect(self.onChangeAxesLabelColor)

        #LABEL Properties sub-menu
        self.labelPropertiesMenu = self.editMenu.addMenu(self.tr('&Label Properties'))

        self.editXLabelAction = QAction(self.tr('X Axis Label'), self)
        self.editXLabelAction.triggered.connect(self.onChangeXLabel)

        self.editYLabelAction = QAction(self.tr('Y Axis Label'), self)
        self.editYLabelAction.triggered.connect(self.onChangeYLabel)

        self.editLabelFontAction = QAction(self.tr('Labels Font'), self)
        self.editLabelFontAction.triggered.connect(self.onChangeLabelFont)

        self.editTickLabelFontAction = QAction(self.tr('Tick Labels Font'), self)
        self.editTickLabelFontAction.triggered.connect(self.onChangeTickLabelFont)

       
    def createAdditionalMenus(self):
        pass
    def defineMenusLayout(self):
        self.linePropertiesMenu.addAction(self.editMajorTickLengthAction)
        self.linePropertiesMenu.addAction(self.editMajorTickWidthAction)
        self.linePropertiesMenu.addAction(self.editMinorTickLengthAction)
        self.linePropertiesMenu.addAction(self.editMinorTickWidthAction)
        self.linePropertiesMenu.addAction(self.editGridLineWidthAction)
        self.linePropertiesMenu.addAction(self.editSpinesLineWidthAction)
        self.colorPropertiesMenu.addAction(self.editBackgroundColorAction)
        self.colorPropertiesMenu.addAction(self.editCanvasColorAction)
        self.colorPropertiesMenu.addAction(self.editAxesColorAction)
        self.colorPropertiesMenu.addAction(self.editGridColorAction)
        self.colorPropertiesMenu.addAction(self.editTickLabelColorAction)
        self.colorPropertiesMenu.addAction(self.editAxesLabelColorAction)
        self.labelPropertiesMenu.addAction(self.editXLabelAction)
        self.labelPropertiesMenu.addAction(self.editYLabelAction)
        self.labelPropertiesMenu.addAction(self.editLabelFontAction)
        self.labelPropertiesMenu.addAction(self.editTickLabelFontAction)
    def toggleGrid(self, state):
        self.axes.grid(True)
        if self.gridOn.isChecked():
            self.axes.grid(True, color=self.gridColor, linewidth=self.gridLineWidth)
        else:
            self.axes.grid(False)
        self.canvas.draw()
    def onAxesChange(self):
        xmin = self.currLocale.toDouble(self.xminWidget.text())[0]
        xmax = self.currLocale.toDouble(self.xmaxWidget.text())[0]
        ymin = self.currLocale.toDouble(self.yminWidget.text())[0]
        ymax = self.currLocale.toDouble(self.ymaxWidget.text())[0]
        self.axes.set_xlim((xmin, xmax))
        self.axes.set_ylim((ymin, ymax))
        self.canvas.draw()

    def plotData(self):
        pass
      
    def setBaseFigureProperties(self):
        self.fig.set_facecolor(self.canvasColor)
        self.axes.set_facecolor(self.backgroundColor)
        self.toggleGrid(None)
        self.axes.spines['bottom'].set_color(self.axesColor)
        self.axes.spines['left'].set_color(self.axesColor)
        self.axes.spines['top'].set_color(self.axesColor)
        self.axes.spines['right'].set_color(self.axesColor)
        self.axes.spines['bottom'].set_linewidth(self.spinesLineWidth)
        self.axes.spines['left'].set_linewidth(self.spinesLineWidth)
        self.axes.spines['top'].set_linewidth(self.spinesLineWidth)
        self.axes.spines['right'].set_linewidth(self.spinesLineWidth)
        for line in self.axes.yaxis.get_ticklines():
            line.set_color(self.axesColor)
            line.set_markersize(self.majorTickLength)
            line.set_markeredgewidth(self.majorTickWidth)
        for line in self.axes.xaxis.get_ticklines():
            line.set_color(self.axesColor)
            line.set_markersize(self.majorTickLength)
            line.set_markeredgewidth(self.majorTickWidth)
        for line in self.axes.yaxis.get_ticklines(minor=True):
            line.set_color(self.axesColor)
            line.set_markersize(self.minorTickLength)
            line.set_markeredgewidth(self.minorTickWidth)
        for line in self.axes.xaxis.get_ticklines(minor=True):
            line.set_color(self.axesColor)
            line.set_markersize(self.minorTickLength)
            line.set_markeredgewidth(self.minorTickWidth)
        for tick in self.axes.xaxis.get_major_ticks():
            tick.label1.set_color(self.tickLabelColor)
        for tick in self.axes.yaxis.get_major_ticks():
            tick.label1.set_color(self.tickLabelColor)
       

        for tick in self.axes.xaxis.get_major_ticks():
            tick.label1.set_family(self.tickLabelFont.get_family())
            tick.label1.set_size(self.tickLabelFont.get_size())
            tick.label1.set_weight(self.tickLabelFont.get_weight())
            tick.label1.set_style(self.tickLabelFont.get_style())
        for tick in self.axes.yaxis.get_major_ticks():
            tick.label1.set_family(self.tickLabelFont.get_family())
            tick.label1.set_size(self.tickLabelFont.get_size())
            tick.label1.set_weight(self.tickLabelFont.get_weight())
            tick.label1.set_style(self.tickLabelFont.get_style())

        self.axes.set_xlabel(self.xAxisLabel, color=self.axesLabelColor, fontproperties = self.labelFont)
        self.axes.set_ylabel(self.yAxisLabel, color=self.axesLabelColor, fontproperties = self.labelFont)
        self.canvas.draw()
  
    def onChangeMajorTickLength(self):
        msg = self.tr('Tick Length:')
        value, ok = QInputDialog.getDouble(self, self.tr('Input Dialog'), msg, self.majorTickLength, 0)
        if ok:
            self.majorTickLength = value
            self.setBaseFigureProperties()
    def onChangeMajorTickWidth(self):
        msg = self.tr('Tick Width:')
        value, ok = QInputDialog.getDouble(self, self.tr('Input Dialog'), msg, self.majorTickWidth, 0)
        if ok:
            self.majorTickWidth = value
            self.setBaseFigureProperties()
    def onChangeMinorTickLength(self):
        msg = self.tr('Tick Length:')
        value, ok = QInputDialog.getDouble(self, self.tr('Input Dialog'), msg, self.minorTickLength, 0)
        if ok:
            self.minorTickLength = value
            self.setBaseFigureProperties()
    def onChangeMinorTickWidth(self):
        msg = self.tr('Tick Width:')
        value, ok = QInputDialog.getDouble(self, self.tr('Input Dialog'), msg, self.minorTickWidth, 0)
        if ok:
            self.minorTickWidth = value
            self.setBaseFigureProperties()
    def onChangeGridLineWidth(self):
        msg = self.tr('Grid Line Width:')
        value, ok = QInputDialog.getDouble(self, self.tr('Input Dialog'), msg, self.gridLineWidth, 0)
        if ok:
            self.gridLineWidth = value
            self.setBaseFigureProperties()
    def onChangeSpinesLineWidth(self):
        msg = self.tr('Spines Line Width:')
        value, ok = QInputDialog.getDouble(self, self.tr('Input Dialog'), msg, self.spinesLineWidth, 0)
        if ok:
            self.spinesLineWidth = value
            self.setBaseFigureProperties()

    def onChangeBackgroundColor(self):
        col = QColorDialog.getColor()
        if col.isValid():
            self.backgroundColor = pltColorFromQColor(col)
            self.setBaseFigureProperties()
    def onChangeCanvasColor(self):
        col = QColorDialog.getColor()
        if col.isValid():
            self.canvasColor = pltColorFromQColor(col)
            self.setBaseFigureProperties()

    def onChangeAxesColor(self):
        col = QColorDialog.getColor()
        if col.isValid():
            self.axesColor = pltColorFromQColor(col)
            self.setBaseFigureProperties()

    def onChangeGridColor(self):
        col = QColorDialog.getColor()
        if col.isValid():
            self.gridColor = pltColorFromQColor(col)
            self.setBaseFigureProperties()
    def onChangeTickLabelColor(self):
        col = QColorDialog.getColor()
        if col.isValid():
            self.tickLabelColor = pltColorFromQColor(col)
            self.setBaseFigureProperties()

    def onChangeAxesLabelColor(self):
        col = QColorDialog.getColor()
        if col.isValid():
            self.axesLabelColor = pltColorFromQColor(col)
            self.setBaseFigureProperties()

    def onChangeLabelFont(self):
        dialog = getFontDialog(self, self.labelFont)
        if dialog.exec_():
            idx = dialog.fontStylesWidget.currentRow()
            family = str(dialog.fontListWidget.currentItem().text())
            fontFileName = dialog.fontsDic[family]['style'][idx].split(':')[2]
            fontSize = int(dialog.fontSizeWidget.currentItem().text())
            fontStyle = dialog.fontsDic[family]['styleAbb'][idx].split(' ')[0]
            fontWeight = dialog.fontsDic[family]['styleAbb'][idx].split(' ')[1]
            self.labelFont = font_manager.FontProperties(fname = fontFileName, family=family, style=fontStyle, weight=fontWeight, size=fontSize)
            self.setBaseFigureProperties()
    def onChangeTickLabelFont(self):
        dialog = getFontDialog(self, self.tickLabelFont)
        if dialog.exec_():
            idx = dialog.fontStylesWidget.currentRow()
            family = str(dialog.fontListWidget.currentItem().text())
            fontFileName = dialog.fontsDic[family]['style'][idx].split(':')[2]
            fontSize = int(dialog.fontSizeWidget.currentItem().text())
            fontStyle = dialog.fontsDic[family]['styleAbb'][idx].split(' ')[0]
            fontWeight = dialog.fontsDic[family]['styleAbb'][idx].split(' ')[1]
            self.tickLabelFont = font_manager.FontProperties(fname = fontFileName, style=fontStyle, weight=fontWeight, size=fontSize)
            self.setBaseFigureProperties()
    def onChangeXLabel(self):
        msg = self.tr('X Axis label:')
        text, ok = QInputDialog.getText(self, self.tr('Input Dialog'), msg)
        if ok:
            self.xAxisLabel = str(text)
            self.setBaseFigureProperties()
    def onChangeYLabel(self):
        msg = self.tr('Y Axis label:')
        text, ok = QInputDialog.getText(self, self.tr('Input Dialog'), msg)
        if ok:
            self.yAxisLabel = str(text)
            self.setBaseFigureProperties()
       
      

