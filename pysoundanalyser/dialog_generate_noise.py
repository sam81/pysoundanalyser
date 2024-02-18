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
if pyqtversion == 5:
    from PyQt5 import QtGui, QtCore
    from PyQt5.QtGui import QDoubleValidator, QIntValidator
    from PyQt5.QtWidgets import QComboBox, QDialog, QDialogButtonBox, QGridLayout, QLabel, QLineEdit, QVBoxLayout
elif pyqtversion == 6:
    from PyQt6 import QtGui, QtCore
    from PyQt6.QtGui import QDoubleValidator, QIntValidator
    from PyQt6.QtWidgets import QComboBox, QDialog, QDialogButtonBox, QGridLayout, QLabel, QLineEdit, QVBoxLayout

class generateNoiseDialog(QDialog):
    def __init__(self, parent):
        QDialog.__init__(self, parent)
        self.prm = parent.prm
        self.currLocale = self.parent().prm['appData']['currentLocale']
        self.currLocale.setNumberOptions(self.currLocale.NumberOption.OmitGroupSeparator | self.currLocale.NumberOption.RejectGroupSeparator)
        vbl = QVBoxLayout()
        self.grid = QGridLayout()

        # Noise Type
        noiseTypeLabel = QLabel(self.tr('Noise Type: '))
        self.noiseTypeChooser = QComboBox()
        self.noiseTypeChooser.addItems([self.tr('White'), self.tr('Pink'), self.tr("Red"), self.tr("Blue"), self.tr("Violet")])
        self.noiseTypeChooser.setCurrentIndex(0)
        self.grid.addWidget(noiseTypeLabel, 0, 0)
        self.grid.addWidget(self.noiseTypeChooser, 0, 1)
        self.noiseTypeChooser.currentIndexChanged[int].connect(self.onChangeNoiseType)
        #Noise Label
        noiseLabelLabel = QLabel(self.tr('Sound Label: '))
        self.noiseLabelWidget = QLineEdit(self.tr('Noise'))
        self.grid.addWidget(noiseLabelLabel, 0, 2)
        self.grid.addWidget(self.noiseLabelWidget, 0, 3)
        # Noise Duration
        noiseDurationLabel = QLabel(self.tr('Duration (ms):'))
        defaultDuration = 980
        self.noiseDurationWidget = QLineEdit(self.currLocale.toString(defaultDuration)) 
        self.noiseDurationWidget.setValidator(QDoubleValidator(self))
        self.grid.addWidget(noiseDurationLabel, 1, 0)
        self.grid.addWidget(self.noiseDurationWidget, 1, 1)
        #Noise Ramps
        noiseRampsLabel = QLabel(self.tr('Ramps (ms):'))
        defaultRamps = 10
        self.noiseRampsWidget = QLineEdit(self.currLocale.toString(defaultRamps)) 
        self.noiseRampsWidget.setValidator(QDoubleValidator(self))
        self.grid.addWidget(noiseRampsLabel, 1, 2)
        self.grid.addWidget(self.noiseRampsWidget, 1, 3)
        #Noise Spectrum Level
        noiseLevelLabel = QLabel(self.tr('Spectrum Level (dB):'))
        defaultSpectrumLevel = 40
        self.noiseLevelWidget = QLineEdit(self.currLocale.toString(defaultSpectrumLevel)) 
        self.noiseLevelWidget.setValidator(QIntValidator(self))
        self.grid.addWidget(noiseLevelLabel, 2, 0)
        self.grid.addWidget(self.noiseLevelWidget, 2, 1)
        #Noise Sampling Rate
        sampRateLabel = QLabel(self.tr('Sampling Rate'))
        defaultSampRate = 48000
        self.sampRateWidget = QLineEdit(self.currLocale.toString(defaultSampRate)) 
        self.sampRateWidget.setValidator(QIntValidator(self))
        self.grid.addWidget(sampRateLabel, 3, 0)
        self.grid.addWidget(self.sampRateWidget, 3, 1)
        #Ear
        noiseEarLabel = QLabel(self.tr('Ear: '))
        self.noiseEarChooser = QComboBox()
        self.noiseEarChooser.addItems([self.tr('Right'), self.tr('Left'), self.tr('Both')])
        self.noiseEarChooser.setCurrentIndex(0)
        self.grid.addWidget(noiseEarLabel, 3, 2)
        self.grid.addWidget(self.noiseEarChooser, 3, 3)
        self.currNoiseType = self.tr('White')
       
        buttonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok|
                                     QDialogButtonBox.StandardButton.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

        vbl.addLayout(self.grid)
        vbl.addWidget(buttonBox)
        self.setLayout(vbl)
        self.setWindowTitle(self.tr("Generate Noise"))

   
    def onChangeNoiseType(self):
        prevNoiseType = self.currNoiseType
        self.currNoiseType = self.noiseTypeChooser.currentText()
        if self.currNoiseType != prevNoiseType:
            if prevNoiseType == self.tr('White'):
                pass
            elif prevNoiseType in [self.tr('Pink'), self.tr("Red"), self.tr("Blue"), self.tr("Violet")]:
                self.grid.removeWidget(self.reLabel)
                #self.reLabel.setParent(None)
                self.reLabel.deleteLater()
                self.grid.removeWidget(self.reWidget)
                #self.reWidget.setParent(None)
                self.reWidget.deleteLater()

                
            if self.currNoiseType in [self.tr('Pink'), self.tr("Red"), self.tr("Blue"), self.tr("Violet")]:
                self.reLabel = QLabel(self.tr('re. (Hz): '))
                defaultRe = 1000
                self.reWidget = QLineEdit(self.currLocale.toString(defaultRe)) 
                self.reWidget.setValidator(QDoubleValidator(self))
                self.grid.addWidget(self.reLabel, 2, 2)
                self.grid.addWidget(self.reWidget, 2, 3)
               
              
