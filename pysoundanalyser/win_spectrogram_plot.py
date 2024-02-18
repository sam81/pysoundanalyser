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

import matplotlib
matplotlib.rcParams['path.simplify'] = False

from .pyqtver import*
if pyqtversion == 5:
    from PyQt5 import QtGui, QtCore
    from PyQt5.QtGui import QDoubleValidator
    from PyQt5.QtWidgets import QAction, QCheckBox, QComboBox, QLabel, QInputDialog
    from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
    from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
    matplotlib.rcParams['backend'] = "Qt5Agg"
elif pyqtversion == 6:
    from PyQt6 import QtGui, QtCore
    from PyQt6.QtGui import QAction, QDoubleValidator
    from PyQt6.QtWidgets import QCheckBox, QComboBox, QLabel, QInputDialog
    from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
    from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
    matplotlib.rcParams['backend'] = "Qt5Agg"

# Matplotlib Figure object
from matplotlib.figure import Figure
from matplotlib.widgets import Cursor


from numpy import log, sin, cos, pi, sqrt, abs, arange, zeros, mean, concatenate, convolve, angle, real, log2, log10, int_, linspace, meshgrid, repeat, ceil, unique, hamming, hanning, blackman, bartlett, round, transpose, where
from numpy.fft import rfft, irfft, fft, ifft
from .utility_functions import*
from .win_generic_plot import*

class spectrogramPlot(genericPlot):
    def __init__(self, parent, sound, prm):
        genericPlot.__init__(self, parent, prm)
        self.prm = parent.prm
        self.sound = sound
        self.currLocale = self.parent().prm['appData']['currentLocale']
        self.currLocale.setNumberOptions(self.currLocale.NumberOption.OmitGroupSeparator | self.currLocale.NumberOption.RejectGroupSeparator)
        self.poweroftwo = self.prm['pref']['poweroftwo']
        self.win = self.prm['pref']['smoothingWindow']
        self.xAxisLabel = self.prm['pref']['spectrogram_x_axis_label']
        self.yAxisLabel = self.prm['pref']['spectrogram_y_axis_label']
        self.logXAxis = self.prm['pref']['spectrumLogXAxis']
        self.winLength = 0
        self.winOverlap = 0
        self.firstRun = True
        self.getData()
        self.plotData()
        self.setAxesLabels()
        self.canvas.draw()
        self.setWindowTitle(self.sound['label'] + ' [' + self.sound['chan'] +']')
    def getData(self):
        if self.firstRun == True:
            dur = self.sound['duration']
            nSmp = self.sound['nSamples']
            self.winLength = dur/10
            if nSmp > int(0.025*48000) and nSmp < int(0.25*48000) :
                self.winLength = 0.01
            elif nSmp < int(0.025*48000):
                self.winLength = dur
            self.winOverlap = 0
               

        (powerMatrix, freqArr, timeArr) = getSpectrogram(self.sound['wave'], self.sound['fs'], self.winLength, self.winOverlap, self.win, self.poweroftwo)
        minval = 9e10
        for sl in range(powerMatrix.shape[1]):
            if len(powerMatrix[:,sl][powerMatrix[:,sl] > 0]) < 1:
                pass
            else:
                minval = min(minval, min(powerMatrix[:,sl][powerMatrix[:,sl] > 0])) 
        for sl in range(powerMatrix.shape[1]):
            powerMatrix[:,sl][where(powerMatrix[:,sl] <= 0)[0]] = minval*10**-10 #100 dB less than minval

        self.sound['spectrogram_freqArr'] =  freqArr
        self.sound['spectrogram_timeArr'] =  timeArr
        self.sound['spectrogram_winLength'] =  self.winLength
        self.sound['spectrogram_winOverlap'] =  self.winOverlap
        self.sound['spectrogram'] = powerMatrix
    def plotData(self):
        Z = 10*log10(self.sound['spectrogram'])
        # X,Y = meshgrid(self.sound['spectrogram_timeArr'], self.sound['spectrogram_freqArr'])
        # self.im = self.axes.pcolormesh(X, Y, Z, cmap=self.prm['pref']['colormap'])
        Z = flipud(Z)
        extent = self.sound['spectrogram_timeArr'][0], self.sound['spectrogram_timeArr'][-1], 1, self.sound['spectrogram_freqArr'][-1]
        self.im = self.axes.imshow(Z, cmap=self.prm['pref']['colormap'], extent=extent)
        self.axes.axis('auto')
        if self.logXAxis == True:
            self.axes.set_yscale('log')
            self.axes.set_xlim(0, self.sound['duration'])
            #self.axes.set_xlim(0, self.sound['spectrogram_timeArr'][-1])
            self.axes.set_ylim(1, self.sound['spectrogram_freqArr'][-1])
        else:
            self.axes.set_yscale('linear')
            #self.axes.set_xlim(0, self.sound['spectrogram_timeArr'][-1])
            self.axes.set_xlim(0, self.sound['duration'])
            self.axes.set_ylim(0, self.sound['spectrogram_freqArr'][-1])
            
        self.fig.colorbar(self.im)
        if self.firstRun == True:
            self.xminWidget.setText(self.currLocale.toString(self.axes.get_xlim()[0])) 
            self.xmaxWidget.setText(self.currLocale.toString(self.axes.get_xlim()[1])) 
            self.yminWidget.setText(self.currLocale.toString(self.axes.get_ylim()[0])) 
            self.ymaxWidget.setText(self.currLocale.toString(self.axes.get_ylim()[1])) 
            self.winLengthWidget.setText(self.currLocale.toString(self.winLength)) 
            self.firstRun = False
      
    def createAdditionalControlWidgets(self):
        self.windowChooser = QComboBox()
        self.windowChooser.addItems(self.prm['appData']['available_windows'])
        self.windowChooser.setCurrentIndex(self.windowChooser.findText(self.prm['pref']['smoothingWindow']))
        self.windowChooserLabel = QLabel(self.tr('Window:'))
        self.gridBox.addWidget(self.windowChooserLabel, 0, 4)
        self.gridBox.addWidget(self.windowChooser, 0, 5)
        self.windowChooser.currentIndexChanged[int].connect(self.onChangeWindowFunction)

        self.poweroftwoOn = QCheckBox(self.tr('Power of 2'))
        self.poweroftwoOn.setChecked(self.prm['pref']['poweroftwo'])
        self.poweroftwoOn.stateChanged[int].connect(self.togglePoweroftwo)
        self.gridBox.addWidget(self.poweroftwoOn, 0, 6)

        self.winLengthLabel= QLabel(self.tr('Window Length (s)'))
        self.winLengthWidget = QLineEdit(self.currLocale.toString(0)) 
        self.winLengthWidget.setValidator(QDoubleValidator(self))
        self.gridBox.addWidget(self.winLengthLabel, 2, 0)
        self.gridBox.addWidget(self.winLengthWidget, 2, 1)

        self.winOverlapLabel= QLabel(self.tr('Overlap (%)'))
        self.winOverlapWidget = QLineEdit(self.currLocale.toString(0)) 
        self.winOverlapWidget.setValidator(QDoubleValidator(self))
        self.gridBox.addWidget(self.winOverlapLabel, 2, 2)
        self.gridBox.addWidget(self.winOverlapWidget, 2, 3)

        self.cmapChooserLabel = QLabel(self.tr('Color Map:'))
        self.gridBox.addWidget(self.cmapChooserLabel, 1, 4)
        self.cmapChooser = QComboBox()
        self.cmapChooser.addItems(self.prm['appData']['available_colormaps'])
        self.cmapChooser.setCurrentIndex(self.cmapChooser.findText(self.prm['pref']['colormap']))
        self.gridBox.addWidget(self.cmapChooser, 1, 5)

        self.logXAxisWidget = QCheckBox(self.tr('Log axis'))
        self.logXAxisWidget.stateChanged[int].connect(self.toggleLogXAxis)
        self.gridBox.addWidget(self.logXAxisWidget, 1, 6)

        self.windowChooser.currentIndexChanged[int].connect(self.onChangeWindowFunction)
        self.cmapChooser.currentIndexChanged[int].connect(self.onChangeWindowFunction)
        self.winLengthWidget.editingFinished.connect(self.onChangeWindowFunction)
        self.winOverlapWidget.editingFinished.connect(self.onChangeWindowFunction)
        
    def onChangeWindowFunction(self):
        self.win = self.windowChooser.currentText()
        self.winLength = self.currLocale.toDouble(self.winLengthWidget.text())[0]
        self.winOverlap = self.currLocale.toDouble(self.winOverlapWidget.text())[0]
        self.selectedColormap = self.cmapChooser.currentText()
        self.getData()
        self.updatePlot()
    def togglePoweroftwo(self, state):
        if self.poweroftwoOn.isChecked():
            self.poweroftwo = True
        else:
            self.poweroftwo = False
        self.getData()
        self.updatePlot()
    def toggleLogXAxis(self, state):
        if self.logXAxisWidget.isChecked():
            self.logXAxis = True
        else:
            self.logXAxis = False
        self.updatePlot()
    def setAxesLabels(self):
        self.axes.set_xlabel(self.xAxisLabel)
        self.axes.set_ylabel(self.yAxisLabel)
    def onAxesChange(self):
        xmin = self.currLocale.toDouble(self.xminWidget.text())[0]
        xmax = self.currLocale.toDouble(self.xmaxWidget.text())[0]
        ymin = self.currLocale.toDouble(self.yminWidget.text())[0]
        ymax = self.currLocale.toDouble(self.ymaxWidget.text())[0]
        self.updatePlot()

    def updatePlot(self):

        xmin = self.currLocale.toDouble(self.xminWidget.text())[0]
        xmax = self.currLocale.toDouble(self.xmaxWidget.text())[0]
        ymin = self.currLocale.toDouble(self.yminWidget.text())[0]
        ymax = self.currLocale.toDouble(self.ymaxWidget.text())[0]

        #compute spectrogram only on the selected region, so that the range of colors available is greater
        idx1 = where(self.sound['spectrogram_freqArr'] >= ymin); idx1 = idx1[0]
        idx2 = where(self.sound['spectrogram_freqArr'] <= ymax); idx2 = idx2[0]
        idx1 = set(idx1); idx2 = set(idx2)
        idx12 = idx1.intersection(idx2)
        l = sorted(list(idx12))

        itx1 = where(self.sound['spectrogram_timeArr'] >= xmin); itx1 = itx1[0]
        itx2 = where(self.sound['spectrogram_timeArr'] <= xmax); itx2 = itx2[0]
        itx1 = set(itx1); itx2 = set(itx2)
        itx12 = itx1.intersection(itx2)
        lt = list(itx12)

        self.fig.clear()
        self.selectedColormap = self.cmapChooser.currentText()
        self.axes = self.fig.add_subplot(111, facecolor=self.backgroundColor)
        Z = 10*log10(self.sound['spectrogram'][l[0]:(l[-1]+1),lt[0]:(lt[-1]+1)])
        #X,Y = meshgrid(self.sound['spectrogram_timeArr'][lt[0]:(lt[-1]+1)], self.sound['spectrogram_freqArr'][l[0]:(l[-1]+1)])
       
        #self.im = self.axes.pcolor(X, Y, Z, cmap=str(self.selectedColormap))
        Z = flipud(Z)
        extent = self.sound['spectrogram_timeArr'][lt[0]], self.sound['spectrogram_timeArr'][lt[-1]], self.sound['spectrogram_freqArr'][l[0]], self.sound['spectrogram_freqArr'][l[-1]]
        self.im = self.axes.imshow(Z, cmap=str(self.selectedColormap), extent=extent)
        self.axes.axis('auto')
        if self.logXAxis == True:
            self.axes.set_yscale('log')
            if ymin <= 0:
                ymin = 1
                self.yminWidget.setText(self.currLocale.toString(1)) 
        else:
            self.axes.set_yscale('linear')
        #self.axes.axis('auto')
        self.axes.set_ylim(ymin, ymax)
        self.axes.set_xlim(xmin, xmax)

        
        self.fig.colorbar(self.im)
        self.setAxesLabels()
        self.setBaseFigureProperties()
        self.toggleGrid(None)
        self.canvas.draw()


         
