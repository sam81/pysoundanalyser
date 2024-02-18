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
    from PyQt5.QtCore import pyqtSignal, Qt, QEvent, QSize
    from PyQt5.QtGui import QDoubleValidator, QIntValidator, QFontMetrics
    from PyQt5.QtWidgets import  QApplication, QCheckBox, QFrame, QGridLayout, QDialog, QDialogButtonBox, QHBoxLayout, QLabel, QLayout, QLineEdit, QComboBox, QScrollArea, QSizePolicy, QVBoxLayout, QWidget, QDesktopWidget
elif pyqtversion == 6:
    from PyQt6 import QtGui, QtCore
    from PyQt6.QtCore import pyqtSignal, Qt, QEvent, QSize
    from PyQt6.QtGui import QDoubleValidator, QIntValidator, QFontMetrics
    from PyQt6.QtWidgets import  QApplication, QCheckBox, QFrame, QGridLayout, QDialog, QDialogButtonBox, QHBoxLayout, QLabel, QLayout, QLineEdit, QComboBox, QScrollArea, QSizePolicy, QVBoxLayout, QWidget#, QDesktopWidget
    
class generateSoundDialog(QDialog):
    def __init__(self, parent, sndType):
        QDialog.__init__(self, parent)

        self.prm = parent.prm
        self.currLocale = self.parent().prm['appData']['currentLocale']
        self.currLocale.setNumberOptions(self.currLocale.NumberOption.OmitGroupSeparator | self.currLocale.NumberOption.RejectGroupSeparator)
        self.vbl = QVBoxLayout()
        self.hbl = QHBoxLayout()
        self.grid_0 = QGridLayout()
        self.grid_1 = QGridLayout()

        if sndType == "Harmonic Complex":
            self.execString = "harm_compl"
        elif sndType == "Silence":
            self.execString = "silence"
        elif sndType == "FM Tone":
            self.execString = "fm_tone"
        elif sndType == "AM Tone":
            self.execString = "am_tone"

        self.nrows = 0
        #SOUND LABEL
        soundLabelLabel = QLabel(self.tr('Sound Label: '))
        self.soundLabelWidget = QLineEdit(self.tr(sndType))
        self.grid_0.addWidget(soundLabelLabel, self.nrows, 0)
        self.grid_0.addWidget(self.soundLabelWidget, self.nrows, 1)
        self.nrows = self.nrows + 1
        #SAMPLING RATE
        sampRateLabel = QLabel(self.tr('Sampling Rate'))
        defaultSampRate = 48000
        self.sampRateWidget = QLineEdit(self.currLocale.toString(defaultSampRate)) 
        self.sampRateWidget.setValidator(QIntValidator(self))
        self.grid_0.addWidget(sampRateLabel, self.nrows, 0)
        self.grid_0.addWidget(self.sampRateWidget, self.nrows, 1)
        self.nrows = self.nrows + 1
        
        methodToCall = getattr(self, "select_default_parameters_" + self.execString)
        self.sndPrm = methodToCall()
        self.setDefaultParameters()
        buttonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok|
                                           QDialogButtonBox.StandardButton.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

        self.grid_0.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.grid_1.setAlignment(Qt.AlignmentFlag.AlignTop)
        self.hbl.addLayout(self.grid_0)
        self.hbl.addLayout(self.grid_1)

        self.scrollAreaWidgetContents = QWidget()#QFrame()
        #self.scrollAreaWidgetContents.setFrameStyle(QFrame.StyledPanel|QFrame.Sunken)
        self.scrollAreaWidgetContents.setLayout(self.hbl)
        
        self.scrollArea = QScrollArea()
        #self.scrollArea.setWidgetResizable(True)
        self.scrollArea.setWidget(self.scrollAreaWidgetContents)
        self.scrollAreaWidgetContents.layout().setSizeConstraint(QLayout.SizeConstraint.SetFixedSize)

        self.vbl.addWidget(self.scrollArea)
        self.vbl.addWidget(buttonBox)
        self.setLayout(self.vbl)
        if pyqtversion == 5:
            screen = QDesktopWidget().screenGeometry()
        elif pyqtversion == 6:
            screen = self.screen().geometry()
        self.resize(int(0.3*screen.width()), int(0.5*screen.height()))
        self.setWindowTitle(self.tr("Generate Sound"))

    
    ## def minimumSizeHint(self):
    ##     size = self.sizeHint()
    ##     fm = QFontMetrics(self.font())
    ##     size.setHeight(fm.height() * 3)
    ##     return size


    ## def sizeHint(self):
    ##     fm = QFontMetrics(self.font())
    ##     size = fm.height()
    ##     return QSize(size*50, size * 60)
        

    def setDefaultParameters(self):
    
        self.field = list(range(self.sndPrm['nFields']))
        self.fieldLabel = list(range(self.sndPrm['nFields']))
        fieldLabelColumn = 0
        fieldColumn = 1
        chooserLabelColumn = 2
        chooserColumn = 3
        fshift = self.nrows
        for f in range(self.sndPrm['nFields']):
            self.fieldLabel[f] = QLabel(self.tr(self.sndPrm['fieldLabel'][f]))
            self.grid_0.addWidget(self.fieldLabel[f], f+fshift, fieldLabelColumn)
            self.field[f] = QLineEdit()
            self.field[f].setText(str(self.sndPrm['field'][f]))
            self.field[f].setValidator(QDoubleValidator(self))
            self.grid_0.addWidget(self.field[f], f+fshift, fieldColumn)
         
        self.chooser = list(range(self.sndPrm['nChoosers']))
        self.chooserLabel = list(range(self.sndPrm['nChoosers']))
        self.chooserOptions = list(range(self.sndPrm['nChoosers']))
        for c in range(self.sndPrm['nChoosers']):
            self.chooserLabel[c] = QLabel(self.tr(self.sndPrm['chooserLabel'][c]))
            self.grid_1.addWidget(self.chooserLabel[c], c, chooserLabelColumn)
            self.chooserOptions[c] = self.sndPrm['chooserOptions'][c]
            self.chooser[c] = QComboBox()  
            self.chooser[c].addItems(self.chooserOptions[c])
            self.chooser[c].setCurrentIndex(self.chooserOptions[c].index(self.sndPrm['chooser'][c]))
            self.grid_1.addWidget(self.chooser[c], c, chooserColumn)
        for c in range(len(self.chooser)):
            #self.chooser[c].activated[str].connect(self.onChooserChange)
            self.chooser[c].textActivated[str].connect(self.onChooserChange)
            self.onChooserChange()
        self.sndPrm['nFields'] = len(self.field)
        self.sndPrm['nChoosers'] = len(self.chooser)

  
    def onChooserChange(self):
        self.fieldsToHide = []; self.fieldsToShow = []
        self.choosersToHide = []; self.choosersToShow = [];
        methodToCall = getattr(self, "get_fields_to_hide_" + self.execString)
        tmp = methodToCall()

        for i in range(len(self.fieldsToHide)):
            self.field[self.fieldsToHide[i]].hide()
            self.fieldLabel[self.fieldsToHide[i]].hide()
        for i in range(len(self.fieldsToShow)):
            self.field[self.fieldsToShow[i]].show()
            self.fieldLabel[self.fieldsToShow[i]].show()
        for i in range(len(self.choosersToHide)):
            self.chooser[self.choosersToHide[i]].hide()
            self.chooserLabel[self.choosersToHide[i]].hide()
        for i in range(len(self.choosersToShow)):
            self.chooser[self.choosersToShow[i]].show()
            self.chooserLabel[self.choosersToShow[i]].show()
            
    def select_default_parameters_harm_compl(self):
   
        field = []
        fieldLabel = []
        chooser = []
        chooserLabel = []
        chooserOptions = []
    
        fieldLabel.append( self.tr("F0 (Hz)"))
        field.append(440)
    
        fieldLabel.append(self.tr("Bandwidth (Hz)"))
        field.append(10)
    
        fieldLabel.append(self.tr("Bandwidth (Cents)"))
        field.append(150)
    
        fieldLabel.append(self.tr("Spacing (Cents)"))
        field.append(10)
    
        fieldLabel.append(self.tr("ITD (micro s)"))
        field.append(320)
    
        fieldLabel.append(self.tr("IPD (radians)"))
        field.append(3.14159)#265)
    
        fieldLabel.append(self.tr("Narrow Band Component Level (dB SPL)"))
        field.append(65)
    
        fieldLabel.append(self.tr("Iterations"))
        field.append(16)
    
        fieldLabel.append(self.tr("Gain"))
        field.append(1)
    
        fieldLabel.append( self.tr("Low Harmonic"))
        field.append(1)
    
        fieldLabel.append(self.tr("High Harmonic"))
        field.append(20)
    
        fieldLabel.append(self.tr("Low Freq. (Hz)"))
        field.append(0)
    
        fieldLabel.append( self.tr("High Freq. (Hz)"))
        field.append(2000)
    
        fieldLabel.append( self.tr("Low Stop"))
        field.append(0.8)
    
        fieldLabel.append( self.tr("High Stop"))
        field.append(1.2)
    
        fieldLabel.append(self.tr("Harmonic Level (dB SPL)"))
        field.append(50)
    
        fieldLabel.append(self.tr("Spectrum Level (dB SPL)"))
        field.append(50)
    
        fieldLabel.append(self.tr("Component Level (dB SPL)"))
        field.append(50)
    
        fieldLabel.append(self.tr("Duration (ms)"))
        field.append(980)
    
        fieldLabel.append(self.tr("Ramp (ms)"))
        field.append(10)
    
        fieldLabel.append(self.tr("No. 1 Low Freq. (Hz)"))
        field.append(0)
    
        fieldLabel.append( self.tr("No. 1 High Freq. (Hz)"))
        field.append(1000)
    
        fieldLabel.append(self.tr("No. 1 S. Level (dB SPL)"))
        field.append(-200)
    
        fieldLabel.append(self.tr("No. 2 Low Freq. (Hz)"))
        field.append(2000)
    
        fieldLabel.append(self.tr("No. 2 High Freq. (Hz)"))
        field.append(3000)
    
        fieldLabel.append(self.tr("No. 2 S. Level (dB SPL)"))
        field.append(-200)
    
        fieldLabel.append(self.tr("Stretch (%)"))
        field.append(0)
    
        fieldLabel.append(self.tr("Harmonic Spacing (Cents)"))
        field.append(500)
    

       
        chooserOptions.append([self.tr("Right"), self.tr("Left"), self.tr("Both"), self.tr("Odd Left"), self.tr("Odd Right")])
        chooserLabel.append(self.tr("Ear:"))
        chooser.append(self.tr("Both"))
        chooserOptions.append([self.tr("Sinusoid"), self.tr("Narrowband Noise"), self.tr("IRN"), self.tr("Huggins Pitch")])
        chooserLabel.append(self.tr("Type:"))
        chooser.append(self.tr("Sinusoid"))
        chooserOptions.append([self.tr("Sine"), self.tr("Cosine"), self.tr("Alternating"), self.tr("Schroeder"), self.tr("Random")])
        chooserLabel.append(self.tr("Phase:"))
        chooser.append(self.tr("Sine"))
        chooserOptions.append([self.tr("White"), self.tr("Pink"), self.tr("None")])
        chooserLabel.append(self.tr("Noise Type:"))
        chooser.append(self.tr("White"))

        chooserOptions.append([self.tr("White"), self.tr("Pink")])
        chooserLabel.append(self.tr("Dichotic Noise Type:"))
        chooser.append(self.tr("White"))
        chooserOptions.append([self.tr("Add Same"), self.tr("Add Original")])
        chooserLabel.append(self.tr("IRN Type:"))
        chooser.append(self.tr("Add Same"))
        chooserOptions.append([self.tr("NoSpi"), self.tr("NpiSo")])
        chooserLabel.append(self.tr("Phase relationship:"))
        chooser.append(self.tr("NoSpi"))
        chooserOptions.append([self.tr("IPD Linear"), self.tr("IPD Stepped"), self.tr("ITD")])
        chooserLabel.append(self.tr("Dichotic Difference:"))
        chooser.append( self.tr("IPD Stepped"))
        chooserOptions.append([self.tr("Harmonic"), self.tr("Harmonic Stretched")])
        chooserLabel.append(self.tr("Harmonicity:"))
        chooser.append(self.tr("Harmonic"))
        chooserOptions.append([self.tr("Hz"), self.tr("Cent"), self.tr("ERB")])
        chooserLabel.append(self.tr("Bandwidth Unit:"))
        chooser.append(self.tr("Hz"))
   
        x = {}
        x['nFields'] = len(fieldLabel)
        x['nChoosers'] = len(chooserLabel)
        x['field'] = field
        x['fieldLabel'] = fieldLabel
        x['chooser'] = chooser
        x['chooserLabel'] = chooserLabel
        x['chooserOptions'] =  chooserOptions

        return x
    def get_fields_to_hide_harm_compl(self):
        if self.chooser[self.sndPrm['chooserLabel'].index(QApplication.translate("","Type:",""))].currentText() == QApplication.translate("","Sinusoid",""):
            self.fieldsToHide = [self.sndPrm['fieldLabel'].index(self.tr("Bandwidth (Hz)")),
                                   self.sndPrm['fieldLabel'].index(self.tr("Bandwidth (Cents)")),
                                   self.sndPrm['fieldLabel'].index(self.tr("Spacing (Cents)")),
                                   self.sndPrm['fieldLabel'].index(self.tr("ITD (micro s)")),
                                   self.sndPrm['fieldLabel'].index(self.tr("IPD (radians)")),
                                   self.sndPrm['fieldLabel'].index(self.tr("Narrow Band Component Level (dB SPL)")),
                                   self.sndPrm['fieldLabel'].index(self.tr("Iterations")),
                                   self.sndPrm['fieldLabel'].index(self.tr("Gain")),
                                   self.sndPrm['fieldLabel'].index(self.tr("Spectrum Level (dB SPL)")),
                                   self.sndPrm['fieldLabel'].index(self.tr("Component Level (dB SPL)"))]
            self.fieldsToShow = [self.sndPrm['fieldLabel'].index(self.tr("Harmonic Level (dB SPL)"))]
            self.choosersToHide = [self.sndPrm['chooserLabel'].index(self.tr("IRN Type:")),
                                     self.sndPrm['chooserLabel'].index(self.tr("Phase relationship:")),
                                     self.sndPrm['chooserLabel'].index(self.tr("Bandwidth Unit:")),
                                     self.sndPrm['chooserLabel'].index(self.tr("Dichotic Noise Type:")), #white, pink
                                     self.sndPrm['chooserLabel'].index(self.tr("Dichotic Difference:"))]
            self.choosersToShow = [self.sndPrm['chooserLabel'].index(self.tr("Ear:")),
                                     self.sndPrm['chooserLabel'].index(self.tr("Phase:")), #sine cos schroeder, etc
                                     self.sndPrm['chooserLabel'].index(self.tr("Noise Type:")), #white, pink
                                     self.sndPrm['chooserLabel'].index(self.tr("Harmonicity:"))] #Harmonic, equal cents spacing
          
        elif self.chooser[self.sndPrm['chooserLabel'].index(QApplication.translate("","Type:",""))].currentText() == QApplication.translate("","Narrowband Noise",""): 
            self.fieldsToHide = [self.sndPrm['fieldLabel'].index(self.tr("Bandwidth (Cents)")),
                                   self.sndPrm['fieldLabel'].index(self.tr("Spacing (Cents)")),
                                   self.sndPrm['fieldLabel'].index(self.tr("ITD (micro s)")),
                                   self.sndPrm['fieldLabel'].index(self.tr("IPD (radians)")),
                                   self.sndPrm['fieldLabel'].index(self.tr("Narrow Band Component Level (dB SPL)")),
                                   self.sndPrm['fieldLabel'].index(self.tr("Iterations")),
                                   self.sndPrm['fieldLabel'].index(self.tr("Gain")),
                                   self.sndPrm['fieldLabel'].index(self.tr("Harmonic Level (dB SPL)")),
                                   self.sndPrm['fieldLabel'].index(self.tr("Component Level (dB SPL)"))]
            self.fieldsToShow = [self.sndPrm['fieldLabel'].index(self.tr("Bandwidth (Hz)")),
                                self.sndPrm['fieldLabel'].index(self.tr("Spectrum Level (dB SPL)"))]
            self.choosersToHide = [self.sndPrm['chooserLabel'].index(self.tr("Phase:")), #sine cos schroeder, etc
                                     self.sndPrm['chooserLabel'].index(self.tr("IRN Type:")),
                                     self.sndPrm['chooserLabel'].index(self.tr("Phase relationship:")), #NoSpi, NpiSo
                                     self.sndPrm['chooserLabel'].index(self.tr("Dichotic Difference:"))] #IPD, ITD
            self.choosersToShow = [self.sndPrm['chooserLabel'].index(self.tr("Ear:")),
                                    self.sndPrm['chooserLabel'].index(self.tr("Noise Type:")), #white, pink
                                    self.sndPrm['chooserLabel'].index(self.tr("Dichotic Noise Type:")), #white, pink
                                    self.sndPrm['chooserLabel'].index(self.tr("Bandwidth Unit:")),
                                    self.sndPrm['chooserLabel'].index(self.tr("Harmonicity:"))] #Harmonic, equal cents spacing

        elif self.chooser[self.sndPrm['chooserLabel'].index(QApplication.translate("","Type:",""))].currentText() == QApplication.translate("","IRN",""):
            self.fieldsToHide = [self.sndPrm['fieldLabel'].index(self.tr("Low Harmonic")),
                                   self.sndPrm['fieldLabel'].index(self.tr("High Harmonic")),
                                   self.sndPrm['fieldLabel'].index(self.tr("Bandwidth (Hz)")),
                                   self.sndPrm['fieldLabel'].index(self.tr("Bandwidth (Cents)")),
                                   self.sndPrm['fieldLabel'].index(self.tr("Spacing (Cents)")),
                                   self.sndPrm['fieldLabel'].index(self.tr("ITD (micro s)")),
                                   self.sndPrm['fieldLabel'].index(self.tr("IPD (radians)")),
                                   self.sndPrm['fieldLabel'].index(self.tr("Narrow Band Component Level (dB SPL)")),
                                   self.sndPrm['fieldLabel'].index(self.tr("Harmonic Level (dB SPL)")),
                                   self.sndPrm['fieldLabel'].index(self.tr("Component Level (dB SPL)")),
                                   self.sndPrm['fieldLabel'].index(self.tr("Stretch (%)")),
                                   self.sndPrm['fieldLabel'].index(self.tr("Harmonic Spacing (Cents)"))]
            self.fieldsToShow = [self.sndPrm['fieldLabel'].index(self.tr("Iterations")),
                                   self.sndPrm['fieldLabel'].index(self.tr("Gain")),
                                   self.sndPrm['fieldLabel'].index(self.tr("Spectrum Level (dB SPL)"))]
            self.choosersToShow = [self.sndPrm['chooserLabel'].index(self.tr("Ear:")), #left, right, both, odd left, odd right
                                     self.sndPrm['chooserLabel'].index(self.tr("Noise Type:")), #white, pink
                                     self.sndPrm['chooserLabel'].index(self.tr("IRN Type:"))]
            self.choosersToHide = [self.sndPrm['chooserLabel'].index(self.tr("Phase:")), #sine cos schroeder, etc
                                    self.sndPrm['chooserLabel'].index(self.tr("Phase relationship:")), #NoSpi, NpiSo
                                    self.sndPrm['chooserLabel'].index(self.tr("Dichotic Difference:")), #IPD, ITD
                                    self.sndPrm['chooserLabel'].index(self.tr("Bandwidth Unit:")),
                                    self.sndPrm['chooserLabel'].index(self.tr("Dichotic Noise Type:")), #white, pink
                                    self.sndPrm['chooserLabel'].index(self.tr("Harmonicity:"))] #Harmonic, equal cents spacing
                          
                          
        elif self.chooser[self.sndPrm['chooserLabel'].index(QApplication.translate("","Type:",""))].currentText() == QApplication.translate("","Huggins Pitch",""):
            self.fieldsToHide = [self.sndPrm['fieldLabel'].index(self.tr("Bandwidth (Cents)")),
                                   self.sndPrm['fieldLabel'].index(self.tr("Spacing (Cents)")),
                                   self.sndPrm['fieldLabel'].index(self.tr("ITD (micro s)")),
                                   self.sndPrm['fieldLabel'].index(self.tr("IPD (radians)")),
                                   self.sndPrm['fieldLabel'].index(self.tr("Narrow Band Component Level (dB SPL)")),
                                   self.sndPrm['fieldLabel'].index(self.tr("Iterations")),
                                   self.sndPrm['fieldLabel'].index(self.tr("Gain")),
                                   self.sndPrm['fieldLabel'].index(self.tr("Harmonic Level (dB SPL)")),
                                   self.sndPrm['fieldLabel'].index(self.tr("Component Level (dB SPL)"))]
            self.fieldsToShow = [self.sndPrm['fieldLabel'].index(self.tr("Bandwidth (Hz)")),
                                   self.sndPrm['fieldLabel'].index(self.tr("Spectrum Level (dB SPL)"))]
            self.choosersToShow = [self.sndPrm['chooserLabel'].index(self.tr("Phase relationship:")), #NoSpi, NpiSo
                                    self.sndPrm['chooserLabel'].index(self.tr("Bandwidth Unit:")),
                                    self.sndPrm['chooserLabel'].index(self.tr("Dichotic Difference:")), 
                                    self.sndPrm['chooserLabel'].index(self.tr("Dichotic Noise Type:")), #white, pink
                                    self.sndPrm['chooserLabel'].index(self.tr("Harmonicity:"))] #Harmonic, equal cents spacing
            self.choosersToHide = [self.sndPrm['chooserLabel'].index(self.tr("Ear:")), #left, right, both, odd left, odd right
                                     self.sndPrm['chooserLabel'].index(self.tr("Phase:")), #sine cos schroeder, etc
                                     self.sndPrm['chooserLabel'].index(self.tr("IRN Type:")),
                                     self.sndPrm['chooserLabel'].index(self.tr("Dichotic Difference:"))] #IPD, ITD
            if self.chooser[self.sndPrm['chooserLabel'].index(QApplication.translate("","Dichotic Difference:",""))].currentText() in [QApplication.translate("","IPD Linear",""), QApplication.translate("","IPD Stepped","")]:
                 self.fieldsToHide.extend([self.sndPrm['fieldLabel'].index(self.tr("ITD (micro s)"))])
                 self.fieldsToShow.extend([self.sndPrm['fieldLabel'].index(self.tr("IPD (radians)"))])
            elif self.chooser[self.sndPrm['chooserLabel'].index(QApplication.translate("","Dichotic Difference:",""))].currentText() == QApplication.translate("","ITD",""):
                 self.fieldsToHide.extend([self.sndPrm['fieldLabel'].index(self.tr("IPD (radians)"))])
                 self.fieldsToShow.extend([self.sndPrm['fieldLabel'].index(self.tr("ITD (micro s)"))])

            
        ## elif self.chooser[self.sndPrm['chooserLabel'].index(QApplication.translate("","Type:",""))].currentText() == QApplication.translate("","Simple Dichotic",""):
        ##     self.fieldsToHide = [self.sndPrm['fieldLabel'].index(self.tr("Bandwidth (Hz)")),
        ##                            self.sndPrm['fieldLabel'].index(self.tr("Iterations")),
        ##                            self.sndPrm['fieldLabel'].index(self.tr("Gain")),
        ##                            self.sndPrm['fieldLabel'].index(self.tr("Harmonic Level (dB SPL)")),
        ##                            self.sndPrm['fieldLabel'].index(self.tr("Spectrum Level (dB SPL)")),
        ##                            self.sndPrm['fieldLabel'].index(self.tr("Narrow Band Component Level (dB SPL)"))]
        ##     self.fieldsToShow = [self.sndPrm['fieldLabel'].index(self.tr("Bandwidth (Cents)")),
        ##                            self.sndPrm['fieldLabel'].index(self.tr("Spacing (Cents)")),
        ##                            self.sndPrm['fieldLabel'].index(self.tr("Component Level (dB SPL)"))]
        ##     if self.chooser[self.sndPrm['chooserLabel'].index(QApplication.translate("","Dichotic Difference:",""))].currentText() == QApplication.translate("","IPD",""):
        ##         self.fieldsToHide.extend([self.sndPrm['fieldLabel'].index(self.tr("ITD (micro s)"))])
        ##         self.fieldsToShow.extend([self.sndPrm['fieldLabel'].index(self.tr("IPD (radians)"))])
        ##     elif self.chooser[self.sndPrm['chooserLabel'].index(QApplication.translate("","Dichotic Difference:",""))].currentText() == QApplication.translate("","ITD",""):
        ##         self.fieldsToHide.extend([self.sndPrm['fieldLabel'].index(self.tr("IPD (radians)"))])
        ##         self.fieldsToShow.extend([self.sndPrm['fieldLabel'].index(self.tr("ITD (micro s)"))])
        ##         self.choosersToShow = [self.sndPrm['chooserLabel'].index(self.tr("Phase relationship:")), #NoSpi, NpiSo
        ##                                  self.sndPrm['chooserLabel'].index(self.tr("Dichotic Difference:")), #IPD, ITD
        ##                                  self.sndPrm['chooserLabel'].index(self.tr("Bandwidth Unit:")),
        ##                                  self.sndPrm['chooserLabel'].index(self.tr("Harmonicity:"))]
        ##         self.choosersToHide = [self.sndPrm['chooserLabel'].index(self.tr("Ear:")), #left, right, both, odd left, odd right
        ##                                  self.sndPrm['chooserLabel'].index(self.tr("Phase:")), #sine cos schroeder, etc
        ##                                  self.sndPrm['chooserLabel'].index(self.tr("Noise Type:")), #white, pink
        ##                                  self.sndPrm['chooserLabel'].index(self.tr("Dichotic Noise Type:")), #white, pink
        ##                                  self.sndPrm['chooserLabel'].index(self.tr("IRN Type:"))]
        ## elif self.chooser[self.sndPrm['chooserLabel'].index(QApplication.translate("","Type:",""))].currentText() == QApplication.translate("","Narrowband Noise 2",""):
        ##     self.fieldsToHide = [self.sndPrm['fieldLabel'].index(self.tr("Bandwidth (Hz)")),
        ##                          self.sndPrm['fieldLabel'].index(self.tr("Iterations")),
        ##                          self.sndPrm['fieldLabel'].index(self.tr("Gain")),
        ##                          self.sndPrm['fieldLabel'].index(self.tr("Harmonic Level (dB SPL)")),
        ##                          self.sndPrm['fieldLabel'].index(self.tr("Spectrum Level (dB SPL)")),
        ##                          self.sndPrm['fieldLabel'].index(self.tr("IPD (radians)")),
        ##                          self.sndPrm['fieldLabel'].index(self.tr("ITD (micro s)"))]
        ##     self.fieldsToShow = [self.sndPrm['fieldLabel'].index(self.tr("Bandwidth (Cents)")),
        ##                          self.sndPrm['fieldLabel'].index(self.tr("Spacing (Cents)")),
        ##                          self.sndPrm['fieldLabel'].index(self.tr("Narrow Band Component Level (dB SPL)")),
        ##                          self.sndPrm['fieldLabel'].index(self.tr("Component Level (dB SPL)"))]
                           
        ##     self.choosersToShow = [self.sndPrm['chooserLabel'].index(self.tr("Phase relationship:")), #NoSpi, NpiSo
        ##                            self.sndPrm['chooserLabel'].index(self.tr("Harmonicity:"))]
        ##     self.choosersToHide = [self.sndPrm['chooserLabel'].index(self.tr("Ear:")), #left, right, both, odd left, odd right
        ##                            self.sndPrm['chooserLabel'].index(self.tr("Dichotic Difference:")),
        ##                            self.sndPrm['chooserLabel'].index(self.tr("Phase:")), #sine cos schroeder, etc
        ##                            self.sndPrm['chooserLabel'].index(self.tr("Noise Type:")), #white, pink
        ##                            self.sndPrm['chooserLabel'].index(self.tr("IRN Type:"))]
                
        if self.chooser[self.sndPrm['chooserLabel'].index(QApplication.translate("","Harmonicity:",""))].currentText() == QApplication.translate("","Harmonic",""):
            self.fieldsToHide.extend([self.sndPrm['fieldLabel'].index(self.tr("Harmonic Spacing (Cents)")),
                                      self.sndPrm['fieldLabel'].index(self.tr("Stretch (%)"))])
        elif self.chooser[self.sndPrm['chooserLabel'].index(QApplication.translate("","Harmonicity:",""))].currentText() == QApplication.translate("","Harmonic Stretched",""):
            self.fieldsToHide.extend([self.sndPrm['fieldLabel'].index(self.tr("Harmonic Spacing (Cents)"))])
            self.fieldsToShow.extend([self.sndPrm['fieldLabel'].index(self.tr("Stretch (%)"))])
        elif self.chooser[self.sndPrm['chooserLabel'].index(QApplication.translate("","Harmonicity:",""))].currentText() == QApplication.translate("","Equal Cents Spacing",""):
            self.fieldsToShow.extend([self.sndPrm['fieldLabel'].index(self.tr("Harmonic Spacing (Cents)"))])


    #Noise Type
        if self.chooser[self.sndPrm['chooserLabel'].index(QApplication.translate("","Noise Type:",""))].currentText() == QApplication.translate("","None",""):
            self.fieldsToHide.extend([self.sndPrm['fieldLabel'].index(self.tr("No. 1 Low Freq. (Hz)")),
                                      self.sndPrm['fieldLabel'].index(self.tr("No. 1 High Freq. (Hz)")),
                                      self.sndPrm['fieldLabel'].index(self.tr("No. 1 S. Level (dB SPL)")),
                                      self.sndPrm['fieldLabel'].index(self.tr("No. 2 Low Freq. (Hz)")),
                                      self.sndPrm['fieldLabel'].index(self.tr("No. 2 High Freq. (Hz)")),
                                      self.sndPrm['fieldLabel'].index(self.tr("No. 2 S. Level (dB SPL)"))])
        else:
            self.fieldsToShow.extend([self.sndPrm['fieldLabel'].index(self.tr("No. 1 Low Freq. (Hz)")),
                                      self.sndPrm['fieldLabel'].index(self.tr("No. 1 High Freq. (Hz)")),
                                      self.sndPrm['fieldLabel'].index(self.tr("No. 1 S. Level (dB SPL)")),
                                      self.sndPrm['fieldLabel'].index(self.tr("No. 2 Low Freq. (Hz)")),
                                      self.sndPrm['fieldLabel'].index(self.tr("No. 2 High Freq. (Hz)")),
                                      self.sndPrm['fieldLabel'].index(self.tr("No. 2 S. Level (dB SPL)"))])

        
        ## if (self.chooser[self.sndPrm['chooserLabel'].index(QApplication.translate("","Type:",""))].currentText() == QApplication.translate("","Simple Dichotic","") or QApplication.translate("","Narrowband Noise 2","")):
        ##     self.fieldsToHide.extend([self.sndPrm['fieldLabel'].index(self.tr("Low Stop")), self.sndPrm['fieldLabel'].index(self.tr("High Stop"))])
            
        ## else:
        ##     self.fieldsToShow.extend([self.sndPrm['fieldLabel'].index(self.tr("Low Stop")), self.sndPrm['fieldLabel'].index(self.tr("High Stop"))])
    def select_default_parameters_fm_tone(self):

        field = []
        fieldLabel = []
        chooser = []
        chooserLabel = []
        chooserOptions = []

        fieldLabel.append(self.tr("Carrier Frequency (Hz)"))
        field.append(1000)    

        fieldLabel.append(self.tr("Modulation Frequency (Hz)"))
        field.append(40)

        fieldLabel.append(self.tr("Modulation Index"))
        field.append(1)

        fieldLabel.append(self.tr("Carrier Phase (radians)"))
        field.append(0)    

        fieldLabel.append(self.tr("Duration (ms)"))
        field.append(980)    

        fieldLabel.append(self.tr("Ramp (ms)"))
        field.append(10)    

        fieldLabel.append(self.tr("Level (dB SPL)"))
        field.append(65)    


        chooserOptions.append([self.tr("Right"), self.tr("Left"), self.tr("Both")])
        chooserLabel.append(self.tr("Ear:"))
        chooser.append(self.tr("Both"))

        x = {}
        x['nFields'] = len(fieldLabel)
        x['nChoosers'] = len(chooserLabel)
        x['field'] = field
        x['fieldLabel'] = fieldLabel
        x['chooser'] = chooser
        x['chooserLabel'] = chooserLabel
        x['chooserOptions'] =  chooserOptions

        return x
    
    def get_fields_to_hide_fm_tone(self):
        pass

    def select_default_parameters_am_tone(self):

        field = []
        fieldLabel = []
        chooser = []
        chooserLabel = []
        chooserOptions = []

        fieldLabel.append(self.tr("Frequency (Hz)"))
        field.append(1000)    

        fieldLabel.append(self.tr("AM Frequency (Hz)"))
        field.append(10)

        fieldLabel.append(self.tr("AM Depth"))
        field.append(1)

        fieldLabel.append(self.tr("Carrier Phase (radians)"))
        field.append(0)    

        fieldLabel.append(self.tr("Modulation Phase (radians)"))
        field.append(0)    

        fieldLabel.append(self.tr("Duration (ms)"))
        field.append(980)    

        fieldLabel.append(self.tr("Ramp (ms)"))
        field.append(10)    

        fieldLabel.append(self.tr("Level (dB SPL)"))
        field.append(65)    


        chooserOptions.append([self.tr("Right"), self.tr("Left"), self.tr("Both")])
        chooserLabel.append(self.tr("Ear:"))
        chooser.append(self.tr("Both"))

        x = {}
        x['nFields'] = len(fieldLabel)
        x['nChoosers'] = len(chooserLabel)
        x['field'] = field
        x['fieldLabel'] = fieldLabel
        x['chooser'] = chooser
        x['chooserLabel'] = chooserLabel
        x['chooserOptions'] =  chooserOptions

        return x
    
    def get_fields_to_hide_am_tone(self):
        pass

        
    def select_default_parameters_silence(self):
   
        field = []
        fieldLabel = []
        chooser = []
        chooserLabel = []
        chooserOptions = []
    
        fieldLabel.append( self.tr("Duration (ms)"))
        field.append(1000)    

       
        chooserOptions.append([self.tr("Right"), self.tr("Left"), self.tr("Both")])
        chooserLabel.append(self.tr("Ear:"))
        chooser.append(self.tr("Both"))

        x = {}
        x['nFields'] = len(fieldLabel)
        x['nChoosers'] = len(chooserLabel)
        x['field'] = field
        x['fieldLabel'] = fieldLabel
        x['chooser'] = chooser
        x['chooserLabel'] = chooserLabel
        x['chooserOptions'] =  chooserOptions

        return x
    
    def get_fields_to_hide_silence(self):
        pass
