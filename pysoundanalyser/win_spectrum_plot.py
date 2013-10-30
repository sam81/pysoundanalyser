#! /usr/bin/env python
# -*- coding: utf-8 -*- 
#   Copyright (C) 2010-2013 Samuele Carcagno <sam.carcagno@gmail.com>
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

from __future__ import nested_scopes, generators, division, absolute_import, with_statement, print_function, unicode_literals
from PyQt4 import QtGui, QtCore
from PyQt4.QtGui import QAction, QCheckBox, QComboBox, QDoubleValidator, QLabel, QInputDialog

# Matplotlib Figure object
from matplotlib.figure import Figure
# import the Qt4Agg FigureCanvas object, that binds Figure to
# Qt4Agg backend. It also inherits from QWidget
from matplotlib.backends.backend_qt4agg import FigureCanvasQTAgg as FigureCanvas
# import the NavigationToolbar Qt4Agg widget
from matplotlib.backends.backend_qt4agg import NavigationToolbar2QTAgg as NavigationToolbar
#from navigation_toolbar_modified import*
from matplotlib.widgets import Cursor
from matplotlib import font_manager
from .dialog_get_font import*

import matplotlib
matplotlib.rcParams['path.simplify'] = False
from .win_generic_plot import*


from numpy import sin, cos, pi, sqrt, abs, arange, zeros, mean, concatenate, convolve, angle, real, log2, log10, int_, linspace, repeat, ceil, unique, hamming, hanning, blackman, bartlett, round, transpose
from numpy.fft import rfft, irfft, fft, ifft
from .utility_functions import*

class spectrumPlot(genericPlot):
    def __init__(self, parent, sound, prm):
        genericPlot.__init__(self, parent, prm)
        self.prm = parent.prm
        self.sound = sound
        self.currLocale = self.parent().prm['data']['currentLocale']
        self.currLocale.setNumberOptions(self.currLocale.OmitGroupSeparator | self.currLocale.RejectGroupSeparator)
        self.win = self.prm['pref']['smoothingWindow']
        self.logXAxis = self.prm['pref']['spectrumLogXAxis']
        self.lineCol = pltColorFromQColor(self.prm['pref']['lineColor1'])
        self.lineWidth = self.prm['pref']['line_width']
        self.poweroftwo = self.prm['pref']['poweroftwo']
        self.xAxisLabel = self.prm['pref']['spectrum_x_axis_label']
        self.yAxisLabel = self.prm['pref']['spectrum_y_axis_label']
        self.firstRun = True
        self.getData()
        self.plotData()
        self.setAxesLabels()
        self.canvas.draw()
        self.setWindowTitle(self.sound['label'] + ' [' + self.sound['chan'] +']')
    def getData(self):
        (freqArr, p) = getSpectrum(self.sound['wave'], self.sound['fs'], self.win, self.poweroftwo)
        self.sound['freqArr'] =  freqArr
        self.sound['spectrum'] = p
    def plotData(self):
        if self.logXAxis == False:
          self.line, = self.axes.plot(self.sound['freqArr'], 10*log10(self.sound['spectrum']), color=self.lineCol, linewidth=self.lineWidth)
        else:
            self.line, = self.axes.plot(self.sound['freqArr'], 10*log10(self.sound['spectrum']), color=self.lineCol, linewidth=self.lineWidth)
            self.axes.set_xscale('log')
            formatter = matplotlib.ticker.FuncFormatter(log_10_product)
            self.axes.xaxis.set_major_formatter(formatter)
        if self.firstRun == True:
            self.xminWidget.setText(self.currLocale.toString(self.axes.get_xlim()[0])) 
            self.xmaxWidget.setText(self.currLocale.toString(self.axes.get_xlim()[1])) 
            self.yminWidget.setText(self.currLocale.toString(self.axes.get_ylim()[0])) 
            self.ymaxWidget.setText(self.currLocale.toString(self.axes.get_ylim()[1])) 
            self.firstRun = False
    def updatePlot(self):
        self.axes.clear()
        self.getData()
        self.plotData()
        self.onAxesChange()
        self.setAxesLabels()
        self.toggleGrid(None)
        self.canvas.draw()

    def createAdditionalControlWidgets(self):
        self.windowChooser = QComboBox()
        self.windowChooser.addItems(self.prm['data']['available_windows'])
        self.windowChooser.setCurrentIndex(self.windowChooser.findText(self.prm['pref']['smoothingWindow']))
        self.windowChooserLabel = QLabel(self.tr('Window:'))
        self.gridBox.addWidget(self.windowChooserLabel, 0, 4)
        self.gridBox.addWidget(self.windowChooser, 0, 5)
        self.windowChooser.currentIndexChanged[int].connect(self.onChangeWindowFunction)

        self.poweroftwoOn = QCheckBox(self.tr('Power of 2'))
        self.poweroftwoOn.setChecked(self.prm['pref']['poweroftwo'])
        self.poweroftwoOn.stateChanged[int].connect(self.togglePoweroftwo)
        self.gridBox.addWidget(self.poweroftwoOn, 0, 6)
        self.logXAxisWidget = QCheckBox(self.tr('Log axis'))
        self.logXAxisWidget.stateChanged[int].connect(self.toggleLogXAxis)
        self.gridBox.addWidget(self.logXAxisWidget, 0, 7)
    def setAxesLabels(self):
        self.axes.set_xlabel(self.xAxisLabel)
        self.axes.set_ylabel(self.yAxisLabel)
    def onChangeWindowFunction(self):
        self.win = self.windowChooser.currentText()
        self.updatePlot()
        
    def togglePoweroftwo(self, state):
        if self.poweroftwoOn.isChecked():
            self.poweroftwo = True
        else:
            self.poweroftwo = False
        self.updatePlot()
    def toggleLogXAxis(self, state):
        if self.logXAxisWidget.isChecked():
            self.logXAxis = True
        else:
            self.logXAxis = False
        self.updatePlot()
  
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


   
