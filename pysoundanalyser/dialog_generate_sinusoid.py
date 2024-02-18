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

class generateSinusoidDialog(QDialog):
    def __init__(self, parent):
        QDialog.__init__(self, parent)
        self.prm = parent.prm
        self.currLocale = self.parent().prm['appData']['currentLocale']
        self.currLocale.setNumberOptions(self.currLocale.NumberOption.OmitGroupSeparator | self.currLocale.NumberOption.RejectGroupSeparator)
        vbl = QVBoxLayout()
        self.grid = QGridLayout()

        #Sound Label
        soundLabelLabel = QLabel(self.tr('Sound Label: '))
        self.soundLabelWidget = QLineEdit(self.tr('Sinusoid'))
        self.grid.addWidget(soundLabelLabel, 0, 0)
        self.grid.addWidget(self.soundLabelWidget, 0, 1)
        # Sound Frequency
        soundFrequencyLabel = QLabel(self.tr('Frequency (Hz):'))
        defaultFrequency = 1000
        self.soundFrequencyWidget = QLineEdit(self.currLocale.toString(defaultFrequency)) 
        self.soundFrequencyWidget.setValidator(QDoubleValidator(self))
        self.grid.addWidget(soundFrequencyLabel, 1, 0)
        self.grid.addWidget(self.soundFrequencyWidget, 1, 1)
        # Sound Phase
        soundPhaseLabel = QLabel(self.tr('Phase (radians):'))
        defaultPhase = 0
        self.soundPhaseWidget = QLineEdit(self.currLocale.toString(defaultPhase)) 
        self.soundPhaseWidget.setValidator(QDoubleValidator(self))
        self.grid.addWidget(soundPhaseLabel, 2, 0)
        self.grid.addWidget(self.soundPhaseWidget, 2, 1)
        # Sound Duration
        soundDurationLabel = QLabel(self.tr('Duration (ms):'))
        defaultDuration = 980
        self.soundDurationWidget = QLineEdit(self.currLocale.toString(defaultDuration)) 
        self.soundDurationWidget.setValidator(QDoubleValidator(self))
        self.grid.addWidget(soundDurationLabel, 3, 0)
        self.grid.addWidget(self.soundDurationWidget, 3, 1)
        #Sound Ramps
        soundRampsLabel = QLabel(self.tr('Ramps (ms):'))
        defaultRamps = 10
        self.soundRampsWidget = QLineEdit(self.currLocale.toString(defaultRamps)) 
        self.soundRampsWidget.setValidator(QDoubleValidator(self))
        self.grid.addWidget(soundRampsLabel, 4, 0)
        self.grid.addWidget(self.soundRampsWidget, 4, 1)
        #Sound Level
        soundLevelLabel = QLabel(self.tr('Level (dB):'))
        defaultLevel = 40
        self.soundLevelWidget = QLineEdit(self.currLocale.toString(defaultLevel)) 
        self.soundLevelWidget.setValidator(QIntValidator(self))
        self.grid.addWidget(soundLevelLabel, 5, 0)
        self.grid.addWidget(self.soundLevelWidget, 5, 1)
        #Sound Sampling Rate
        sampRateLabel = QLabel(self.tr('Sampling Rate'))
        defaultSampRate = 48000
        self.sampRateWidget = QLineEdit(self.currLocale.toString(defaultSampRate)) 
        self.sampRateWidget.setValidator(QIntValidator(self))
        self.grid.addWidget(sampRateLabel, 6, 0)
        self.grid.addWidget(self.sampRateWidget, 6, 1)
        #Ear
        soundEarLabel = QLabel(self.tr('Ear: '))
        self.soundEarChooser = QComboBox()
        self.soundEarChooser.addItems([self.tr('Right'), self.tr('Left'), self.tr('Both')])
        self.soundEarChooser.setCurrentIndex(0)
        self.grid.addWidget(soundEarLabel, 7, 0)
        self.grid.addWidget(self.soundEarChooser, 7, 1)
        self.soundEarChooser.currentIndexChanged[int].connect(self.onChangeChannel)
        self.currChannel = self.tr('Right')
       
        buttonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok|
                                     QDialogButtonBox.StandardButton.Cancel)
        
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

        vbl.addLayout(self.grid)
        vbl.addWidget(buttonBox)
        self.setLayout(vbl)
        self.setWindowTitle(self.tr("Generate Sinusoid"))

   
   
              
    def onChangeChannel(self):
        prevChannel = self.currChannel
        self.currChannel = self.soundEarChooser.currentText()
        if self.currChannel != prevChannel:
            if prevChannel == self.tr('Both'):
                self.grid.removeWidget(self.itdLabel)
                #self.itdLabel.setParent(None)
                self.itdLabel.deleteLater()
                self.grid.removeWidget(self.itdWidget)
                #self.itdWidget.setParent(None)
                self.itdWidget.deleteLater()

                self.grid.removeWidget(self.itdRefLabel)
                #self.itdRefLabel.setParent(None)
                self.itdRefLabel.deleteLater()
                self.grid.removeWidget(self.itdRefChooser)
                #self.itdRefChooser.setParent(None)
                self.itdRefChooser.deleteLater()

                

                self.grid.removeWidget(self.ildLabel)
                #self.ildLabel.setParent(None)
                self.ildLabel.deleteLater()
                self.grid.removeWidget(self.ildWidget)
                #self.ildWidget.setParent(None)
                self.ildWidget.deleteLater()

                self.grid.removeWidget(self.ildRefLabel)
                #self.ildRefLabel.setParent(None)
                self.ildRefLabel.deleteLater()
                self.grid.removeWidget(self.ildRefChooser)
                #self.ildRefChooser.setParent(None)
                self.ildRefChooser.deleteLater()
                
            elif prevChannel in [self.tr('Right'), self.tr('Left')]:
                pass
            if self.currChannel ==  self.tr('Both'):
                self.itdLabel = QLabel(self.tr('ITD (us)'))
                defaultITD = 0
                self.itdWidget = QLineEdit(self.currLocale.toString(defaultITD)) 
                self.itdWidget.setValidator(QIntValidator(self))
                self.grid.addWidget(self.itdLabel, 8, 0)
                self.grid.addWidget(self.itdWidget, 8, 1)

                self.itdRefLabel = QLabel(self.tr('Reference'))
                self.itdRefChooser = QComboBox()
                self.itdRefChooser.addItems([self.tr('Right'), self.tr('Left')])
                self.itdRefChooser.setCurrentIndex(0)
                self.grid.addWidget(self.itdRefLabel, 8, 2)
                self.grid.addWidget(self.itdRefChooser, 8, 3)

                self.ildLabel = QLabel(self.tr('ILD (dB)'))
                defaultILD = 0
                self.ildWidget = QLineEdit(self.currLocale.toString(defaultILD)) 
                self.ildWidget.setValidator(QIntValidator(self))
                self.grid.addWidget(self.ildLabel, 9, 0)
                self.grid.addWidget(self.ildWidget, 9, 1)

                self.ildRefLabel = QLabel(self.tr('Reference'))
                self.ildRefChooser = QComboBox()
                self.ildRefChooser.addItems([self.tr('Right'), self.tr('Left')])
                self.ildRefChooser.setCurrentIndex(0)
                self.grid.addWidget(self.ildRefLabel, 9, 2)
                self.grid.addWidget(self.ildRefChooser, 9, 3)
                
