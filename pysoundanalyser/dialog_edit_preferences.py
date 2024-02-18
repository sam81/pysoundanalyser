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
    from PyQt5.QtCore import QLocale
    from PyQt5.QtGui import QColor, QDoubleValidator, QIntValidator
    from PyQt5.QtWidgets import QCheckBox, QColorDialog, QComboBox, QDialog, QDialogButtonBox, QGridLayout, QLabel, QLineEdit, QPushButton, QTabWidget, QVBoxLayout, QWidget
elif pyqtversion == 6:
    from PyQt6 import QtGui, QtCore
    from PyQt6.QtCore import QLocale
    from PyQt6.QtGui import QColor, QDoubleValidator, QIntValidator
    from PyQt6.QtWidgets import QCheckBox, QColorDialog, QComboBox, QDialog, QDialogButtonBox, QGridLayout, QLabel, QLineEdit, QPushButton, QTabWidget, QVBoxLayout, QWidget

import copy, pickle, platform

try:
    import soundfile
    sndf_available = True
except:
    sndf_available = False

if platform.system() == "Linux":
    try:
        import alsaaudio
    except ImportError:
        pass
try:
    import pyaudio
except ImportError:
    pass

class preferencesDialog(QDialog):
    def __init__(self, parent):
        QDialog.__init__(self, parent)
        self.tmpPref = {}
        self.tmpPref['pref'] = copy.deepcopy(self.parent().prm['pref'])
        self.currLocale = self.parent().prm['appData']['currentLocale']
        self.currLocale.setNumberOptions(self.currLocale.NumberOption.OmitGroupSeparator | self.currLocale.NumberOption.RejectGroupSeparator)
        self.audioManager = parent.audioManager
        
        self.tabWidget = QTabWidget()
        self.tabWidget.currentChanged.connect(self.tabChanged)
        self.appPrefWidget = QWidget()
        self.plotPrefWidget = QWidget()
        self.signalPrefWidget = QWidget()
        self.soundPrefWidget = QWidget()

        
        #APP PREF
        appPrefGrid = QGridLayout()
        n = 0
        self.languageChooserLabel = QLabel(self.tr('Language (requires restart):'))
        appPrefGrid.addWidget(self.languageChooserLabel, n, 0)
        self.languageChooser = QComboBox()
        self.languageChooser.addItems(self.parent().prm['appData']['available_languages'])
        self.languageChooser.setCurrentIndex(self.languageChooser.findText(self.tmpPref['pref']['language']))
        self.languageChooser.currentIndexChanged[int].connect(self.onLanguageChooserChange)
        appPrefGrid.addWidget(self.languageChooser, n, 1)
        n = n+1
        self.countryChooserLabel = QLabel(self.tr('Country (requires restart):'))
        appPrefGrid.addWidget(self.countryChooserLabel, n, 0)
        self.countryChooser = QComboBox()
        self.countryChooser.addItems(self.parent().prm['appData']['available_countries'][self.tmpPref['pref']['language']])
        self.countryChooser.setCurrentIndex(self.countryChooser.findText(self.tmpPref['pref']['country']))
        appPrefGrid.addWidget(self.countryChooser, n, 1)

        self.appPrefWidget.setLayout(appPrefGrid)
        
        #PLOT PREF
        plotPrefGrid = QGridLayout()
        n = 0

        #LINE COLOUR
        self.lineColor1 = self.tmpPref['pref']['lineColor1']
        self.lineColorButton = QPushButton(self.tr("Line Color"), self)
        self.lineColorButton.clicked.connect(self.onChangeLineColor)
        plotPrefGrid.addWidget(self.lineColorButton, n, 0)

        self.lineColorSquare = QWidget(self)
        self.lineColorSquare.setStyleSheet("QWidget { background-color: %s }" % QColor(*self.lineColor1).name())
        plotPrefGrid.addWidget(self.lineColorSquare, n, 1)
       
        n = n+1
        self.backgroundColor = self.tmpPref['pref']['backgroundColor']
        self.backgroundColorButton = QPushButton(self.tr("Background Color"), self)
        self.backgroundColorButton.clicked.connect(self.onChangeBackgroundColor)
        plotPrefGrid.addWidget(self.backgroundColorButton, n, 0)

        self.backgroundColorSquare = QWidget(self)
        self.backgroundColorSquare.setStyleSheet("QWidget { background-color: %s }" % QColor(*self.backgroundColor).name())
        plotPrefGrid.addWidget(self.backgroundColorSquare, n, 1)

        n = n+1
        self.canvasColor = self.tmpPref['pref']['canvasColor']
        self.canvasColorButton = QPushButton(self.tr("Canvas Color"), self)
        self.canvasColorButton.clicked.connect(self.onChangeCanvasColor)
        plotPrefGrid.addWidget(self.canvasColorButton, n, 0)

        self.canvasColorSquare = QWidget(self)
        self.canvasColorSquare.setStyleSheet("QWidget { background-color: %s }" % QColor(*self.canvasColor).name())
        plotPrefGrid.addWidget(self.canvasColorSquare, n, 1)
        
        n = n+1
        self.dpiLabel = QLabel(self.tr('DPI - Resolution:'))
        plotPrefGrid.addWidget(self.dpiLabel, n, 0)
        self.dpiWidget = QLineEdit(str(self.tmpPref['pref']['dpi']))
        plotPrefGrid.addWidget(self.dpiWidget, n, 1)
        self.dpiWidget.setValidator(QIntValidator(self))
        self.dpiWidget.editingFinished.connect(self.ondpiChange)
        
        n = n+1
        self.cmapChooserLabel = QLabel(self.tr('Color Map:'))
        plotPrefGrid.addWidget(self.cmapChooserLabel, n, 0)
        self.cmapChooser = QComboBox()
        self.cmapChooser.addItems(self.parent().prm['appData']['available_colormaps'])
        self.cmapChooser.setCurrentIndex(self.cmapChooser.findText(self.tmpPref['pref']['colormap']))
        plotPrefGrid.addWidget(self.cmapChooser, n, 1)
        n = n+1
        
        self.gridOn = QCheckBox(self.tr('Grid'))
        self.gridOn.setChecked(self.tmpPref['pref']['grid'])
        plotPrefGrid.addWidget(self.gridOn, n, 1)

        self.plotPrefWidget.setLayout(plotPrefGrid)
        
        #SIGNAL PREF
        signalPrefGrid = QGridLayout()
        n = 0
        self.windowChooser = QComboBox()
        self.windowChooser.addItems(self.parent().prm['appData']['available_windows'])
        self.windowChooser.setCurrentIndex(self.windowChooser.findText(self.tmpPref['pref']['smoothingWindow']))
        self.windowChooserLabel = QLabel(self.tr('Window:'))
        signalPrefGrid.addWidget(self.windowChooserLabel, 0, 0)
        signalPrefGrid.addWidget(self.windowChooser, 0, 1)

        n = n+1
        self.signalPrefWidget.setLayout(signalPrefGrid)
        
        #SOUND PREF
        soundPrefGrid = QGridLayout()
        n = 0
        self.wavmanagerLabel = QLabel(self.tr('Wav Manager:'))
        self.wavmanagerChooser = QComboBox()
        if sndf_available == True:
            self.wavmanagerChooser.addItems(["soundfile", "scipy"])
        else:
            self.wavmanagerChooser.addItems(["scipy"])
        self.wavmanagerChooser.setCurrentIndex(self.wavmanagerChooser.findText(self.tmpPref['pref']['sound']['wavmanager']))
        soundPrefGrid.addWidget(self.wavmanagerLabel, n, 0)
        soundPrefGrid.addWidget(self.wavmanagerChooser, n, 1)

        n = n+1
        self.playChooser = QComboBox()
        self.playChooser.addItems(self.parent().prm['appData']['available_play_commands'])
        self.playChooser.setCurrentIndex(self.playChooser.findText(self.tmpPref['pref']['sound']['playCommandType']))
        self.playChooser.currentIndexChanged[int].connect(self.onPlayChooserChange)
        self.playChooserLabel = QLabel(self.tr('Play Command:'))
        soundPrefGrid.addWidget(self.playChooserLabel, n, 0)
        soundPrefGrid.addWidget(self.playChooser, n, 1)
        n = n+1

        self.playCommandLabel = QLabel(self.tr('Command:'))
        soundPrefGrid.addWidget(self.playCommandLabel, n, 0)
        self.playCommandWidget = QLineEdit(self.tmpPref['pref']['sound']['playCommand'])
        if self.playChooser.currentText() != self.tr('custom'):
            self.playCommandWidget.setReadOnly(True)
        soundPrefGrid.addWidget(self.playCommandWidget, n, 1)
        n = n+1
        foo = self.playChooser.currentText()
        if foo != self.tr('custom'):
            self.playCommandLabel.hide()
            self.playCommandWidget.hide()

        #if alsaaudio is selected, provide device list chooser
        if self.parent().prm["appData"]["alsaaudioAvailable"] == True:
            self.alsaaudioPlaybackCardList = self.listAlsaaudioPlaybackCards()
            self.alsaaudioDeviceLabel = QLabel(self.tr('Device:'))
            soundPrefGrid.addWidget(self.alsaaudioDeviceLabel, n, 0)
            self.alsaaudioDeviceChooser = QComboBox()
            self.alsaaudioDeviceChooser.addItems(self.alsaaudioPlaybackCardList)
            self.alsaaudioDeviceChooser.setCurrentIndex(self.alsaaudioDeviceChooser.findText(self.tmpPref["pref"]["sound"]["alsaaudioDevice"]))
            soundPrefGrid.addWidget(self.alsaaudioDeviceChooser, n, 1)
            n = n+1
            if self.tmpPref['pref']['sound']['playCommandType'] != "alsaaudio":
                self.alsaaudioDeviceLabel.hide()
                self.alsaaudioDeviceChooser.hide()

        #if pyaudio is selected, provide device list chooser
        if self.parent().prm["appData"]["pyaudioAvailable"] == True:
            self.listPyaudioPlaybackDevices()
            self.pyaudioDeviceLabel = QLabel(self.tr('Device:'))
            soundPrefGrid.addWidget(self.pyaudioDeviceLabel, n, 0)
            self.pyaudioDeviceChooser = QComboBox()
            self.pyaudioDeviceChooser.addItems(self.pyaudioDeviceListName)
            try:
                self.pyaudioDeviceChooser.setCurrentIndex(self.pyaudioDeviceListIdx.index(self.tmpPref["pref"]["sound"]["pyaudioDevice"]))
            except:
                self.tmpPref["pref"]["sound"]["pyaudioDevice"] = self.pyaudioDeviceListIdx[0]
                self.parent().prm["pref"]["sound"]["pyaudioDevice"] = self.pyaudioDeviceListIdx[0]
                self.pyaudioDeviceChooser.setCurrentIndex(self.pyaudioDeviceListIdx.index(self.tmpPref["pref"]["sound"]["pyaudioDevice"]))
            soundPrefGrid.addWidget(self.pyaudioDeviceChooser, n, 1)
            n = n+1
            if self.tmpPref['pref']['sound']['playCommandType'] != "pyaudio":
                self.pyaudioDeviceLabel.hide()
                self.pyaudioDeviceChooser.hide()

        if self.parent().prm["appData"]["alsaaudioAvailable"] == True or self.parent().prm["appData"]["pyaudioAvailable"] == True:
            self.bufferSizeLabel = QLabel(self.tr('Buffer Size (samples):'))
            soundPrefGrid.addWidget(self.bufferSizeLabel, n, 0)
            self.bufferSizeWidget =  QLineEdit(self.currLocale.toString(self.tmpPref["pref"]["sound"]["bufferSize"]))
            self.bufferSizeWidget.setValidator(QIntValidator(self))
            soundPrefGrid.addWidget(self.bufferSizeWidget, n, 1)
            n = n+1
            if self.tmpPref['pref']['sound']['playCommandType'] not in ["alsaaudio", "pyaudio"]:
                self.bufferSizeLabel.hide()
                self.bufferSizeWidget.hide()

        # self.samplerateLabel = QLabel(self.tr('Default Sampling Rate:'))
        # soundPrefGrid.addWidget(self.samplerateLabel, n, 0)
        # self.samplerateWidget = QLineEdit(self.tmpPref["pref"]["sound"]["defaultSampleRate"])
        # #self.samplerateWidget.setValidator(QIntValidator(self))
        # soundPrefGrid.addWidget(self.samplerateWidget, n, 1)
        # n = n+1

        self.nbitsLabel = QLabel(self.tr('Bits:'))
        self.nbitsChooser = QComboBox()
        self.nbitsChooser.addItems(self.parent().prm['appData']['nBitsChoices'])
        self.nbitsChooser.setCurrentIndex(self.parent().prm['appData']['nBitsChoices'].index(self.tmpPref['pref']['sound']['nBits'])) 
        soundPrefGrid.addWidget(self.nbitsLabel, n, 0)
        soundPrefGrid.addWidget(self.nbitsChooser, n, 1)
        n = n+1


        # n = n+1
        # self.playChooser = QComboBox()
        # self.playChooser.addItems(self.parent().prm['appData']['available_play_commands'])
        # self.playChooser.setCurrentIndex(self.playChooser.findText(self.tmpPref['pref']['sound']['playCommandType']))
        # self.playChooser.currentIndexChanged[int].connect(self.onPlayChooserChange)
        # self.playChooserLabel = QLabel(self.tr('Play Command:'))
        # soundPrefGrid.addWidget(self.playChooserLabel, n, 0)
        # soundPrefGrid.addWidget(self.playChooser, n, 1)

        # n = n+1
        # self.playCommandLabel = QLabel(self.tr('Command:'))
        # soundPrefGrid.addWidget(self.playCommandLabel, n, 0)
        # self.playCommandWidget = QLineEdit(str(self.tmpPref['pref']['sound']['playCommand']))
        # self.playCommandWidget.setReadOnly(True)
        # soundPrefGrid.addWidget(self.playCommandWidget, n, 1)

        n = n+1
        self.maxLevelLabel = QLabel(self.tr('Max Level:'))
        soundPrefGrid.addWidget(self.maxLevelLabel, n, 0)
        self.maxLevelWidget = QLineEdit(self.currLocale.toString(self.tmpPref['pref']['sound']['maxLevel']))
        self.maxLevelWidget.setValidator(QDoubleValidator(self))
        soundPrefGrid.addWidget(self.maxLevelWidget, n, 1)

        
        self.soundPrefWidget.setLayout(soundPrefGrid)

        self.tabWidget.addTab(self.appPrefWidget, self.tr("Applicatio&n"))
        self.tabWidget.addTab(self.plotPrefWidget, self.tr("Plot&s"))
        self.tabWidget.addTab(self.signalPrefWidget, self.tr("Signa&l"))
        self.tabWidget.addTab(self.soundPrefWidget, self.tr("Soun&d"))

        buttonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Apply|QDialogButtonBox.StandardButton.Ok|QDialogButtonBox.StandardButton.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        buttonBox.button(QDialogButtonBox.StandardButton.Apply).clicked.connect(self.permanentApply)
        
        layout = QVBoxLayout()
        layout.addWidget(self.tabWidget)
        layout.addWidget(buttonBox)
        self.setLayout(layout)
      

    def ondpiChange(self):
        try:
            val = int(self.dpiWidget.text())
        except ValueError:
            QMessageBox.warning(self, self.tr('Warning'), self.tr('dpi value not valid'))
            self.dpiWidget.setText(str(self.tmpPref['pref']['dpi']))

        val = int(self.dpiWidget.text())
        if val < 10:
            QMessageBox.warning(self, self.tr('Warning'), self.tr('dpi value too small'))
            self.dpiWidget.setText(str(10))

    def onChangeLineColor(self):
        col = QColorDialog.getColor()
        if col.isValid():
            self.lineColor1 = (col.red(), col.green(), col.blue())
        self.lineColorSquare.setStyleSheet("QWidget { background-color: %s }" % QColor(*self.lineColor1).name())
    def onChangeCanvasColor(self):
        col = QColorDialog.getColor()
        if col.isValid():
            self.canvasColor = (col.red(), col.green(), col.blue())
        self.canvasColorSquare.setStyleSheet("QWidget { background-color: %s }" % QColor(*self.canvasColor).name())
    def onChangeBackgroundColor(self):
        col = QColorDialog.getColor()
        if col.isValid():
            self.backgroundColor = (col.red(), col.green(), col.blue())
        self.backgroundColorSquare.setStyleSheet("QWidget { background-color: %s }" % QColor(*self.backgroundColor).name())
    def onLanguageChooserChange(self):
        for i in range(self.countryChooser.count()):
            self.countryChooser.removeItem(0)
        self.countryChooser.addItems(self.parent().prm['appData']['available_countries'][self.languageChooser.currentText()])
    def onPlayChooserChange(self):
        foo = self.playChooser.currentText()
        if foo != self.tr('custom'):
            self.playCommandLabel.hide()
            self.playCommandWidget.hide()
            self.playCommandWidget.setText(foo)
            self.playCommandWidget.setReadOnly(True)
        else:
            self.playCommandWidget.show()
            self.playCommandLabel.show()
            self.playCommandWidget.setReadOnly(False)

        if self.parent().prm["appData"]["alsaaudioAvailable"] == True:
            if foo == "alsaaudio":
                self.alsaaudioDeviceLabel.show()
                self.alsaaudioDeviceChooser.show()
               
            else:
                self.alsaaudioDeviceLabel.hide()
                self.alsaaudioDeviceChooser.hide()
             

        if self.parent().prm["appData"]["pyaudioAvailable"] == True:
            if foo == "pyaudio":
                self.pyaudioDeviceLabel.show()
                self.pyaudioDeviceChooser.show()
            else:
                self.pyaudioDeviceLabel.hide()
                self.pyaudioDeviceChooser.hide()

        if self.parent().prm["appData"]["alsaaudioAvailable"] == True or self.parent().prm["appData"]["pyaudioAvailable"] == True:
            if foo in ["alsaaudio", "pyaudio"]:
                self.bufferSizeLabel.show()
                self.bufferSizeWidget.show()
            else:
                self.bufferSizeLabel.hide()
                self.bufferSizeWidget.hide()
                
        # foo = self.playChooser.currentText()
        # if foo != self.tr('custom'):
        #     self.playCommandWidget.setText(foo)
        #     self.playCommandWidget.setReadOnly(True)
        # else:
        #     self.playCommandWidget.setReadOnly(False)

            

    def tryApply(self):
        self.tmpPref['pref']['colormap'] = str(self.cmapChooser.currentText())
        self.tmpPref['pref']['dpi'] = int(self.dpiWidget.text())
        self.tmpPref['pref']['lineColor1'] = self.lineColor1
        self.tmpPref['pref']['canvasColor'] = self.canvasColor
        self.tmpPref['pref']['backgroundColor'] = self.backgroundColor
        self.tmpPref['pref']['language'] = self.languageChooser.currentText()
        self.tmpPref['pref']['country'] = self.countryChooser.currentText()
        self.tmpPref['pref']['sound']['wavmanager'] = str(self.wavmanagerChooser.currentText())
        self.tmpPref['pref']['sound']['playCommand'] = self.playCommandWidget.text()
        self.tmpPref['pref']['sound']['playCommandType'] = self.playChooser.currentText()
        if self.parent().prm["appData"]["alsaaudioAvailable"] == True:
            self.tmpPref['pref']['sound']['alsaaudioDevice'] = self.alsaaudioDeviceChooser.currentText()
        if self.parent().prm["appData"]["pyaudioAvailable"] == True:
            self.tmpPref['pref']['sound']['pyaudioDevice'] =  self.pyaudioDeviceListIdx[self.pyaudioDeviceChooser.currentIndex()]
        self.tmpPref['pref']['sound']['maxLevel'] = self.currLocale.toDouble(self.maxLevelWidget.text())[0]
        self.tmpPref['pref']['sound']['nBits'] = self.nbitsChooser.currentText()
        if self.parent().prm["appData"]["alsaaudioAvailable"] == True or self.parent().prm["appData"]["pyaudioAvailable"] == True:
            self.tmpPref['pref']['sound']['bufferSize'] = self.currLocale.toInt(self.bufferSizeWidget.text())[0]
        if self.gridOn.isChecked():
            self.tmpPref['pref']['grid'] = True
        else:
            self.tmpPref['pref']['grid'] = False
        self.tmpPref['pref']['smoothingWindow'] = str(self.windowChooser.currentText())

    def revertChanges(self):
        self.cmapChooser.setCurrentIndex(self.cmapChooser.findText(self.tmpPref['pref']['colormap']))
        self.dpiWidget.setText(str(self.tmpPref['pref']['dpi']))
        self.languageChooser.setCurrentIndex(self.languageChooser.findText(self.tmpPref['pref']['language']))
        self.countryChooser.setCurrentIndex(self.countryChooser.findText(self.tmpPref['pref']['country']))
        self.wavmanagerChooser.setCurrentIndex(self.wavmanagerChooser.findText(self.tmpPref['pref']['sound']['wavmanager']))
        self.playChooser.setCurrentIndex(self.playChooser.findText(self.tmpPref['pref']['sound']['playCommandType']))
        if self.parent().prm["appData"]["alsaaudioAvailable"] == True:
            self.alsaaudioDeviceChooser.setCurrentIndex(self.alsaaudioDeviceChooser.findText(self.tmpPref['pref']['sound']['alsaaudioDevice']))
        if self.parent().prm["appData"]["pyaudioAvailable"] == True:
            self.pyaudioDeviceChooser.setCurrentIndex(self.pyaudioDeviceListIdx.index(self.tmpPref['pref']['sound']['pyaudioDevice']))
        self.playCommandWidget.setText(self.tmpPref['pref']['sound']['playCommand'])
        if self.playChooser.currentText() != self.tr('custom'):
            self.playCommandWidget.setReadOnly(True)
        self.maxLevelWidget.setText(str(self.tmpPref['pref']['sound']['maxLevel']))
        self.nbitsChooser.setCurrentIndex(self.nbitsChooser.findText(self.tmpPref['pref']['sound']['nBits']))
        if self.parent().prm["appData"]["alsaaudioAvailable"] == True or self.parent().prm["appData"]["pyaudioAvailable"] == True:
            self.bufferSizeWidget.setText(self.currLocale.toString(self.tmpPref['pref']['sound']['bufferSize']))
        self.gridOn.setChecked(self.tmpPref['pref']['grid'])
        self.windowChooser.setCurrentIndex(self.windowChooser.findText(self.tmpPref['pref']['smoothingWindow']))
        self.lineColor1 = self.tmpPref['pref']['lineColor1']
        self.lineColorSquare.setStyleSheet("QWidget { background-color: %s }" % QColor(*self.lineColor1).name())
        self.canvasColor = self.tmpPref['pref']['canvasColor']
        self.backgroundColor = self.tmpPref['pref']['backgroundColor']
        self.backgroundColorSquare.setStyleSheet("QWidget { background-color: %s }" % QColor(*self.backgroundColor).name())
        self.canvasColorSquare.setStyleSheet("QWidget { background-color: %s }" % QColor(*self.canvasColor).name())
       
        
       
    def permanentApply(self):
        self.tryApply()
        self.parent().prm['pref'] = copy.deepcopy(self.tmpPref['pref'])
        f = open(self.parent().prm['prefFile'], 'wb')
        pickle.dump(self.parent().prm['pref'], f)
        f.close()

    def tabChanged(self):
        self.tryApply()
        if self.tmpPref['pref'] != self.parent().prm['pref']:
            conf = applyChanges(self)
            if conf.exec():
                self.permanentApply()
            else:
                self.tmpPref['pref'] = copy.deepcopy(self.parent().prm['pref'])
                self.revertChanges()

    def listAlsaaudioPlaybackCards(self):
        playbackCardList = alsaaudio.pcms(alsaaudio.PCM_PLAYBACK)
        return playbackCardList
    
    def listPyaudioPlaybackDevices(self):
        self.pyaudioHostApiListName = []
        self.pyaudioHostApiListIdx = []
        self.pyaudioDeviceListName = []
        self.pyaudioDeviceListIdx = []
        paManager = pyaudio.PyAudio()
        nDevices = paManager.get_device_count()
        nApi = paManager.get_host_api_count()
        for i in range(nApi):
            self.pyaudioHostApiListName.append(paManager.get_host_api_info_by_index(i)['name'])
            self.pyaudioHostApiListIdx.append(paManager.get_host_api_info_by_index(i)['index'])
        for i in range(nDevices):
            thisDevInfo = paManager.get_device_info_by_index(i)
            if thisDevInfo["maxOutputChannels"] > 0:
                self.pyaudioDeviceListName.append(thisDevInfo["name"] + ' - ' + self.pyaudioHostApiListName[thisDevInfo["hostApi"]])
                self.pyaudioDeviceListIdx.append(thisDevInfo["index"])
        return 
                

class applyChanges(QDialog):
    def __init__(self, parent):
        QDialog.__init__(self, parent)
        grid = QGridLayout()
        n = 0
        label = QLabel(self.tr('There are unsaved changes. Apply Changes?'))
        grid.addWidget(label, n, 1)
        n = n+1
        buttonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok|
                                     QDialogButtonBox.StandardButton.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        grid.addWidget(buttonBox, n, 1)
        self.setLayout(grid)
        self.setWindowTitle(self.tr("Apply Changes"))
