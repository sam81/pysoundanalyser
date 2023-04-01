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

from __future__ import nested_scopes, generators, division, absolute_import, with_statement, print_function, unicode_literals
from .pyqtver import*
if pyqtversion == 5:
    from PyQt5 import QtGui, QtCore
    from PyQt5.QtCore import QLocale
    from PyQt5.QtGui import QDoubleValidator, QIntValidator
    from PyQt5.QtWidgets import QCheckBox, QColorDialog, QComboBox, QDialog, QDialogButtonBox, QGridLayout, QLabel, QLineEdit, QPushButton, QTabWidget, QVBoxLayout, QWidget
elif pyqtversion == 6:
    from PyQt6 import QtGui, QtCore
    from PyQt6.QtCore import QLocale
    from PyQt6.QtGui import QDoubleValidator, QIntValidator
    from PyQt6.QtWidgets import QCheckBox, QColorDialog, QComboBox, QDialog, QDialogButtonBox, QGridLayout, QLabel, QLineEdit, QPushButton, QTabWidget, QVBoxLayout, QWidget

import copy, pickle


class preferencesDialog(QDialog):
    def __init__(self, parent):
        QDialog.__init__(self, parent)
        self.tmpPref = {}
        self.tmpPref['pref'] = copy.deepcopy(self.parent().prm['pref'])
        self.currLocale = self.parent().prm['data']['currentLocale']
        self.currLocale.setNumberOptions(self.currLocale.NumberOption.OmitGroupSeparator | self.currLocale.NumberOption.RejectGroupSeparator)
        
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
        self.languageChooser.addItems(self.parent().prm['data']['available_languages'])
        self.languageChooser.setCurrentIndex(self.languageChooser.findText(self.tmpPref['pref']['language']))
        self.languageChooser.currentIndexChanged[int].connect(self.onLanguageChooserChange)
        appPrefGrid.addWidget(self.languageChooser, n, 1)
        n = n+1
        self.countryChooserLabel = QLabel(self.tr('Country (requires restart):'))
        appPrefGrid.addWidget(self.countryChooserLabel, n, 0)
        self.countryChooser = QComboBox()
        self.countryChooser.addItems(self.parent().prm['data']['available_countries'][self.tmpPref['pref']['language']])
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
        self.lineColorSquare.setStyleSheet("QWidget { background-color: %s }" % self.lineColor1.name())
        plotPrefGrid.addWidget(self.lineColorSquare, n, 1)
       
        n = n+1
        
        self.backgroundColor = self.tmpPref['pref']['backgroundColor']
        self.backgroundColorButton = QPushButton(self.tr("Background Color"), self)
        self.backgroundColorButton.clicked.connect(self.onChangeBackgroundColor)
        plotPrefGrid.addWidget(self.backgroundColorButton, n, 0)

        self.backgroundColorSquare = QWidget(self)
        self.backgroundColorSquare.setStyleSheet("QWidget { background-color: %s }" % self.backgroundColor.name())
        plotPrefGrid.addWidget(self.backgroundColorSquare, n, 1)

        n = n+1
        self.canvasColor = self.tmpPref['pref']['canvasColor']
        self.canvasColorButton = QPushButton(self.tr("Canvas Color"), self)
        self.canvasColorButton.clicked.connect(self.onChangeCanvasColor)
        plotPrefGrid.addWidget(self.canvasColorButton, n, 0)

        self.canvasColorSquare = QWidget(self)
        self.canvasColorSquare.setStyleSheet("QWidget { background-color: %s }" % self.canvasColor.name())
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
        self.cmapChooser.addItems(self.parent().prm['data']['available_colormaps'])
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
        self.windowChooser.addItems(self.parent().prm['data']['available_windows'])
        self.windowChooser.setCurrentIndex(self.windowChooser.findText(self.tmpPref['pref']['smoothingWindow']))
        self.windowChooserLabel = QLabel(self.tr('Window:'))
        signalPrefGrid.addWidget(self.windowChooserLabel, 0, 0)
        signalPrefGrid.addWidget(self.windowChooser, 0, 1)

        n = n+1
        self.signalPrefWidget.setLayout(signalPrefGrid)
        
        #SOUND PREF
        soundPrefGrid = QGridLayout()
        n = 0
        self.wavmanagerLabel = QLabel(self.tr('Wav Manager (requires restart):'))
        self.wavmanagerChooser = QComboBox()
        self.wavmanagerChooser.addItems(["scipy"])
        self.wavmanagerChooser.setCurrentIndex(self.wavmanagerChooser.findText(self.tmpPref['pref']['wavmanager']))
        soundPrefGrid.addWidget(self.wavmanagerLabel, n, 0)
        soundPrefGrid.addWidget(self.wavmanagerChooser, n, 1)

        n = n+1
        
        self.playChooser = QComboBox()
        self.playChooser.addItems(self.parent().prm['data']['available_play_commands'])
        self.playChooser.setCurrentIndex(self.playChooser.findText(self.tmpPref['pref']['playCommandType']))
        self.playChooser.currentIndexChanged[int].connect(self.onPlayChooserChange)
        self.playChooserLabel = QLabel(self.tr('Play Command:'))
        soundPrefGrid.addWidget(self.playChooserLabel, n, 0)
        soundPrefGrid.addWidget(self.playChooser, n, 1)

        n = n+1
        self.playCommandLabel = QLabel(self.tr('Command:'))
        soundPrefGrid.addWidget(self.playCommandLabel, n, 0)
        self.playCommandWidget = QLineEdit(str(self.tmpPref['pref']['playCommand']))
        self.playCommandWidget.setReadOnly(True)
        soundPrefGrid.addWidget(self.playCommandWidget, n, 1)

        n = n+1
        self.maxLevelLabel = QLabel(self.tr('Max Level:'))
        soundPrefGrid.addWidget(self.maxLevelLabel, n, 0)
        self.maxLevelWidget = QLineEdit(self.currLocale.toString(self.tmpPref['pref']['maxLevel']))
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
            self.lineColor1 = col
        self.lineColorSquare.setStyleSheet("QWidget { background-color: %s }" % self.lineColor1.name())
    def onChangeCanvasColor(self):
        col = QColorDialog.getColor()
        if col.isValid():
            self.canvasColor = col
        self.canvasColorSquare.setStyleSheet("QWidget { background-color: %s }" % self.canvasColor.name())
    def onChangeBackgroundColor(self):
        col = QColorDialog.getColor()
        if col.isValid():
            self.backgroundColor = col
        self.backgroundColorSquare.setStyleSheet("QWidget { background-color: %s }" % self.backgroundColor.name())
    def onLanguageChooserChange(self):
        for i in range(self.countryChooser.count()):
            self.countryChooser.removeItem(0)
        self.countryChooser.addItems(self.parent().prm['data']['available_countries'][self.languageChooser.currentText()])
    def onPlayChooserChange(self):
        foo = self.playChooser.currentText()
        if foo != self.tr('custom'):
            self.playCommandWidget.setText(foo)
            self.playCommandWidget.setReadOnly(True)
        else:
            self.playCommandWidget.setReadOnly(False)

            

    def tryApply(self):
        self.tmpPref['pref']['colormap'] = str(self.cmapChooser.currentText())
        self.tmpPref['pref']['dpi'] = int(self.dpiWidget.text())
        self.tmpPref['pref']['lineColor1'] = self.lineColor1
        self.tmpPref['pref']['canvasColor'] = self.canvasColor
        self.tmpPref['pref']['backgroundColor'] = self.backgroundColor
        self.tmpPref['pref']['language'] = self.languageChooser.currentText()
        self.tmpPref['pref']['country'] = self.countryChooser.currentText()
        self.tmpPref['pref']['wavmanager'] = str(self.wavmanagerChooser.currentText())
        self.tmpPref['pref']['playCommand'] = self.playCommandWidget.text()
        self.tmpPref['pref']['playCommandType'] = self.playChooser.currentText()
        self.tmpPref['pref']['maxLevel'] = self.currLocale.toDouble(self.maxLevelWidget.text())[0]
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
        self.playChooser.setCurrentIndex(self.playChooser.findText(self.tmpPref['pref']['playCommandType']))
        self.playCommandWidget.setText(self.tmpPref['pref']['playCommand'])
        if self.playChooser.currentText() != self.tr('custom'):
            self.playCommandWidget.setReadOnly(True)
        self.maxLevelWidget.setText(str(self.tmpPref['pref']['maxLevel']))
        self.gridOn.setChecked(self.tmpPref['pref']['grid'])
        self.windowChooser.setCurrentIndex(self.windowChooser.findText(self.tmpPref['pref']['smoothingWindow']))
        self.lineColor1 = self.tmpPref['pref']['lineColor1']
        self.lineColorSquare.setStyleSheet("QWidget { background-color: %s }" % self.lineColor1.name())
        self.canvasColor = self.tmpPref['pref']['canvasColor']
        self.backgroundColor = self.tmpPref['pref']['backgroundColor']
        self.backgroundColorSquare.setStyleSheet("QWidget { background-color: %s }" % self.backgroundColor.name())
        self.canvasColorSquare.setStyleSheet("QWidget { background-color: %s }" % self.canvasColor.name())
       
        
       
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
