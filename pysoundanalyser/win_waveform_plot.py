# -*- coding: utf-8 -*- 
#   Copyright (C) 2010-2023 Samuele Carcagno <sam.carcagno@gmail.com>
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

import matplotlib
matplotlib.rcParams['path.simplify'] = False

from .pyqtver import*
if pyqtversion == 5:
    from PyQt5 import QtGui, QtCore
    from PyQt5.QtWidgets import QAction, QInputDialog
    from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
    from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
    matplotlib.rcParams['backend'] = "Qt5Agg"
elif pyqtversion == 6:
    from PyQt6 import QtGui, QtCore
    from PyQt6.QtGui import QAction
    from PyQt6.QtWidgets import QInputDialog
    from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
    from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
    matplotlib.rcParams['backend'] = "Qt5Agg"

# Matplotlib Figure object
from matplotlib.figure import Figure

from matplotlib.widgets import Cursor
from matplotlib import font_manager
from .dialog_get_font import*
from .win_generic_plot import*
import numpy as np

class waveformPlot(genericPlot):
    def __init__(self, parent, sound, prm):
        genericPlot.__init__(self, parent, prm)
        self.currLocale = self.parent().prm['appData']['currentLocale']
        self.currLocale.setNumberOptions(self.currLocale.NumberOption.OmitGroupSeparator | self.currLocale.NumberOption.RejectGroupSeparator)
        self.sound = sound
        self.lineCol = scaleRGBTo01(self.prm['pref']['lineColor1'])
        self.lineWidth = self.prm['pref']['line_width']
        self.xAxisLabel = self.prm['pref']['waveform_x_axis_label']
        self.yAxisLabel = self.prm['pref']['waveform_y_axis_label']
        self.getData()
        self.plotData()
        self.setAxesLabels()
        self.canvas.draw()
        self.setWindowTitle(self.sound['label'] + ' [' + self.sound['chan'] +']')
    def getData(self):
        self.x = np.arange(len(self.sound['wave']))/self.sound['fs'] #self.sound['timeArray']
        self.y = self.sound['wave']
    def setAxesLabels(self):
        self.axes.set_xlabel(self.xAxisLabel, color=self.axesLabelColor, fontproperties = self.labelFont)
        self.axes.set_ylabel(self.yAxisLabel, color=self.axesLabelColor, fontproperties = self.labelFont)
    def plotData(self):
        self.line, = self.axes.plot(self.x, self.y, color=self.lineCol)
        self.xminWidget.setText(self.currLocale.toString(self.axes.get_xlim()[0])) 
        self.xmaxWidget.setText(self.currLocale.toString(self.axes.get_xlim()[1])) 
        self.yminWidget.setText(self.currLocale.toString(self.axes.get_ylim()[0])) 
        self.ymaxWidget.setText(self.currLocale.toString(self.axes.get_ylim()[1])) 
    def createAdditionalMenus(self):
        self.editLineWidthAction = QAction(self.tr('Line Width'), self)
        self.editLineWidthAction.triggered.connect(self.onChangeLineWidth)

        self.editLineColorAction = QAction(self.tr('Line Color'), self)
        self.editLineColorAction.triggered.connect(self.onChangeLineColor)
        
    def defineMenusLayout(self):
        self.linePropertiesMenu.addAction(self.editLineWidthAction)
        self.linePropertiesMenu.addAction(self.editMajorTickLengthAction)
        self.linePropertiesMenu.addAction(self.editMajorTickWidthAction)
        self.linePropertiesMenu.addAction(self.editMinorTickLengthAction)
        self.linePropertiesMenu.addAction(self.editMinorTickWidthAction)
        self.linePropertiesMenu.addAction(self.editGridLineWidthAction)
        self.linePropertiesMenu.addAction(self.editSpinesLineWidthAction)
        self.colorPropertiesMenu.addAction(self.editLineColorAction)
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
    def onChangeLineColor(self):
        col = QColorDialog.getColor()
        if col.isValid():
            self.lineCol = pltColorFromQColor(col)
            self.line.set_color(self.lineCol)
            self.canvas.draw()
    def onChangeLineWidth(self):
        msg = self.tr('Line Width:')
        value, ok = QInputDialog.getDouble(self, self.tr('Input Dialog'), msg, self.lineWidth, 0)
        if ok:
            self.lineWidth = value
            self.line.set_linewidth(self.lineWidth)
            self.canvas.draw()
