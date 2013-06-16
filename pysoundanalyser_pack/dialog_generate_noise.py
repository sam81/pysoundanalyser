#   Copyright (C) 2010-2011 Samuele Carcagno <sam.carcagno@gmail.com>
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

class generateNoiseDialog(QtGui.QDialog):
    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent)
        self.prm = parent.prm
        self.currLocale = self.parent().prm['data']['currentLocale']
        self.currLocale.setNumberOptions(self.currLocale.OmitGroupSeparator | self.currLocale.RejectGroupSeparator)
        vbl = QtGui.QVBoxLayout()
        self.grid = QtGui.QGridLayout()

        # Noise Type
        noiseTypeLabel = QtGui.QLabel(self.tr('Noise Type: '))
        self.noiseTypeChooser = QtGui.QComboBox()
        self.noiseTypeChooser.addItems([self.tr('white'), self.tr('pink')])
        self.noiseTypeChooser.setCurrentIndex(0)
        self.grid.addWidget(noiseTypeLabel, 0, 0)
        self.grid.addWidget(self.noiseTypeChooser, 0, 1)
        self.connect(self.noiseTypeChooser,  QtCore.SIGNAL("currentIndexChanged(int)"), self.onChangeNoiseType)
        #Noise Label
        noiseLabelLabel = QtGui.QLabel(self.tr('Sound Label: '))
        self.noiseLabelWidget = QtGui.QLineEdit(self.tr('Noise'))
        self.grid.addWidget(noiseLabelLabel, 0, 2)
        self.grid.addWidget(self.noiseLabelWidget, 0, 3)
        # Noise Duration
        noiseDurationLabel = QtGui.QLabel(self.tr('Duration (ms):'))
        defaultDuration = 180
        self.noiseDurationWidget = QtGui.QLineEdit(self.currLocale.toString(defaultDuration)) 
        self.noiseDurationWidget.setValidator(QtGui.QDoubleValidator(self))
        self.grid.addWidget(noiseDurationLabel, 1, 0)
        self.grid.addWidget(self.noiseDurationWidget, 1, 1)
        #Noise Ramps
        noiseRampsLabel = QtGui.QLabel(self.tr('Ramps (ms):'))
        defaultRamps = 10
        self.noiseRampsWidget = QtGui.QLineEdit(self.currLocale.toString(defaultRamps)) 
        self.noiseRampsWidget.setValidator(QtGui.QDoubleValidator(self))
        self.grid.addWidget(noiseRampsLabel, 1, 2)
        self.grid.addWidget(self.noiseRampsWidget, 1, 3)
        #Noise Spectrum Level
        noiseLevelLabel = QtGui.QLabel(self.tr('Spectrum Level (dB):'))
        defaultSpectrumLevel = 40
        self.noiseLevelWidget = QtGui.QLineEdit(self.currLocale.toString(defaultSpectrumLevel)) 
        self.noiseLevelWidget.setValidator(QtGui.QIntValidator(self))
        self.grid.addWidget(noiseLevelLabel, 2, 0)
        self.grid.addWidget(self.noiseLevelWidget, 2, 1)
        #Noise Sampling Rate
        sampRateLabel = QtGui.QLabel(self.tr('Sampling Rate'))
        defaultSampRate = 44100
        self.sampRateWidget = QtGui.QLineEdit(self.currLocale.toString(defaultSampRate)) 
        self.sampRateWidget.setValidator(QtGui.QIntValidator(self))
        self.grid.addWidget(sampRateLabel, 3, 0)
        self.grid.addWidget(self.sampRateWidget, 3, 1)
        #Ear
        noiseEarLabel = QtGui.QLabel(self.tr('Ear: '))
        self.noiseEarChooser = QtGui.QComboBox()
        self.noiseEarChooser.addItems([self.tr('Right'), self.tr('Left'), self.tr('Both')])
        self.noiseEarChooser.setCurrentIndex(0)
        self.grid.addWidget(noiseEarLabel, 3, 2)
        self.grid.addWidget(self.noiseEarChooser, 3, 3)

        

      

        self.currNoiseType = self.tr('white')
       

       
        buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok|
                                     QtGui.QDialogButtonBox.Cancel)
        
        self.connect(buttonBox, QtCore.SIGNAL("accepted()"),
                     self, QtCore.SLOT("accept()"))
        self.connect(buttonBox, QtCore.SIGNAL("rejected()"),
                     self, QtCore.SLOT("reject()"))

        vbl.addLayout(self.grid)
        vbl.addWidget(buttonBox)
        self.setLayout(vbl)
        self.setWindowTitle(self.tr("Generate Noise"))

   
    def onChangeNoiseType(self):
        prevNoiseType = self.currNoiseType
        self.currNoiseType = self.noiseTypeChooser.currentText()
        if self.currNoiseType != prevNoiseType:
            if prevNoiseType == self.tr('white'):
                pass
            elif prevNoiseType == self.tr('pink'):
                self.grid.removeWidget(self.reLabel)
                self.reLabel.setParent(None)
                self.grid.removeWidget(self.reWidget)
                self.reWidget.setParent(None)

                
            if self.currNoiseType == self.tr('pink'):
                self.reLabel = QtGui.QLabel(self.tr('re. (Hz): '))
                defaultRe = 1000
                self.reWidget = QtGui.QLineEdit(self.currLocale.toString(defaultRe)) 
                self.reWidget.setValidator(QtGui.QDoubleValidator(self))
                self.grid.addWidget(self.reLabel, 2, 2)
                self.grid.addWidget(self.reWidget, 2, 3)
               
              
