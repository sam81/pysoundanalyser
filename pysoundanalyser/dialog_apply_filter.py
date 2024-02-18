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

class applyFIR2PresetsDialog(QDialog):
    def __init__(self, parent):
        QDialog.__init__(self, parent)
        self.prm = parent.prm
        self.currLocale = self.parent().prm['appData']['currentLocale']
        self.currLocale.setNumberOptions(self.currLocale.NumberOption.OmitGroupSeparator | self.currLocale.NumberOption.RejectGroupSeparator)
        vbl = QVBoxLayout()
        self.grid = QGridLayout()

        
        filterTypeLabel = QLabel(self.tr('Filter Type: '))
        self.filterChooser = QComboBox()
        self.filterChooser.addItems([self.tr('lowpass'), self.tr('highpass'), self.tr('bandpass'), self.tr('bandstop')])
        self.filterChooser.setCurrentIndex(0)
        self.grid.addWidget(self.filterChooser, 0, 1)
        self.filterChooser.currentIndexChanged[int].connect(self.onChangeFilterType)
        self.filterOrderLabel = QLabel(self.tr('Filter Order: '))
        self.filterOrderWidget = QLineEdit('256')
        self.filterOrderWidget.setValidator(QIntValidator(self))
        self.grid.addWidget(self.filterOrderLabel, 0, 2)
        self.grid.addWidget(self.filterOrderWidget, 0, 3)

        self.currFilterType = self.tr('lowpass')
        self.cutoffLabel = QLabel(self.tr('Cutoff: '))
        self.endCutoffLabel = QLabel(self.tr('End Transition Band = Cutoff *'))
        self.cutoffWidget = QLineEdit('')
        self.cutoffWidget.setValidator(QDoubleValidator(self))
        endCutoff = 1.2
        self.endCutoffWidget = QLineEdit(self.currLocale.toString(endCutoff))
        self.endCutoffWidget.setValidator(QDoubleValidator(self))
        self.grid.addWidget(self.cutoffLabel, 2, 1)
        self.grid.addWidget(self.cutoffWidget, 2, 2)
        self.grid.addWidget(self.endCutoffLabel, 2, 3)
        self.grid.addWidget(self.endCutoffWidget, 2, 4)

       
        buttonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok|
                                     QDialogButtonBox.StandardButton.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)

        vbl.addLayout(self.grid)
        vbl.addWidget(buttonBox)
        self.setLayout(vbl)
        self.setWindowTitle(self.tr("Apply Filter"))

   
    def onChangeFilterType(self):
        prevFilterType = self.currFilterType
        self.currFilterType = str(self.filterChooser.currentText())
        if self.currFilterType != prevFilterType:
            if prevFilterType == self.tr('lowpass'):
                self.grid.removeWidget(self.cutoffLabel)
                #self.cutoffLabel.setParent(None)
                self.cutoffLabel.deleteLater()
                self.grid.removeWidget(self.endCutoffLabel)
                #self.endCutoffLabel.setParent(None)
                self.endCutoffLabel.deleteLater()
                self.grid.removeWidget(self.cutoffWidget)
                #self.cutoffWidget.setParent(None)
                self.cutoffWidget.deleteLater()
                self.grid.removeWidget(self.endCutoffWidget)
                #self.endCutoffWidget.setParent(None)
                self.endCutoffWidget.deleteLater()

            elif prevFilterType == self.tr('highpass'):
                self.grid.removeWidget(self.cutoffLabel)
                #self.cutoffLabel.setParent(None)
                self.cutoffLabel.deleteLater()
                self.grid.removeWidget(self.startCutoffLabel)
                #self.startCutoffLabel.setParent(None)
                self.startCutoffLabel.deleteLater()
                self.grid.removeWidget(self.cutoffWidget)
                #self.cutoffWidget.setParent(None)
                self.cutoffWidget.deleteLater()
                self.grid.removeWidget(self.startCutoffWidget)
                #self.startCutoffWidget.setParent(None)
                self.startCutoffWidget.deleteLater()
            elif prevFilterType == self.tr('bandpass') or prevFilterType == self.tr('bandstop'):
                self.grid.removeWidget(self.lowerCutoffLabel)
                #self.lowerCutoffLabel.setParent(None)
                self.lowerCutoffLabel.deleteLater()
                self.grid.removeWidget(self.startCutoffLabel)
                #self.startCutoffLabel.setParent(None)
                self.startCutoffLabel.deleteLater()
                self.grid.removeWidget(self.lowerCutoffWidget)
                #self.lowerCutoffWidget.setParent(None)
                self.lowerCutoffWidget.deleteLater()
                self.grid.removeWidget(self.startCutoffWidget)
                #self.startCutoffWidget.setParent(None)
                self.startCutoffWidget.deleteLater()
                
                self.grid.removeWidget(self.higherCutoffLabel)
                #self.higherCutoffLabel.setParent(None)
                self.higherCutoffLabel.deleteLater()
                self.grid.removeWidget(self.endCutoffLabel)
                #self.endCutoffLabel.setParent(None)
                self.endCutoffLabel.deleteLater()
                self.grid.removeWidget(self.higherCutoffWidget)
                #self.higherCutoffWidget.setParent(None)
                self.higherCutoffWidget.deleteLater()
                self.grid.removeWidget(self.endCutoffWidget)
                #self.endCutoffWidget.setParent(None)
                self.endCutoffWidget.deleteLater()
                
            if self.currFilterType == self.tr('lowpass'):
                self.cutoffLabel = QLabel(self.tr('Cutoff: '))
                self.endCutoffLabel = QLabel(self.tr('End Transition Band = Cutoff *'))
                self.cutoffWidget = QLineEdit('')
                self.cutoffWidget.setValidator(QDoubleValidator(self))
                endCutoff = 1.2
                self.endCutoffWidget = QLineEdit(self.currLocale.toString(endCutoff))
                self.endCutoffWidget.setValidator(QDoubleValidator(self))
                self.grid.addWidget(self.cutoffLabel, 2, 1)
                self.grid.addWidget(self.cutoffWidget, 2, 2)
                self.grid.addWidget(self.endCutoffLabel, 2, 3)
                self.grid.addWidget(self.endCutoffWidget, 2, 4)
            elif self.currFilterType == self.tr('highpass'):
                self.cutoffLabel = QLabel(self.tr('Cutoff: '))
                self.startCutoffLabel = QLabel(self.tr('Start Transition Band = Cutoff *'))
                self.cutoffWidget = QLineEdit('')
                self.cutoffWidget.setValidator(QDoubleValidator(self))
                startCutoff = 0.8
                self.startCutoffWidget = QLineEdit(self.currLocale.toString(startCutoff)) 
                self.startCutoffWidget.setValidator(QDoubleValidator(self))
                self.grid.addWidget(self.cutoffLabel, 2, 1)
                self.grid.addWidget(self.cutoffWidget, 2, 2)
                self.grid.addWidget(self.startCutoffLabel, 2, 3)
                self.grid.addWidget(self.startCutoffWidget, 2, 4)
            elif self.currFilterType == self.tr('bandpass'):
                self.lowerCutoffLabel = QLabel(self.tr('Lower Cutoff: '))
                self.startCutoffLabel = QLabel(self.tr('Start Transition Band = Cutoff *'))
                self.lowerCutoffWidget = QLineEdit('')
                self.lowerCutoffWidget.setValidator(QDoubleValidator(self))
                startCutoff = 0.8
                self.startCutoffWidget = QLineEdit(self.currLocale.toString(startCutoff)) 
                self.startCutoffWidget.setValidator(QDoubleValidator(self))
                self.grid.addWidget(self.lowerCutoffLabel, 2, 1)
                self.grid.addWidget(self.lowerCutoffWidget, 2, 2)
                self.grid.addWidget(self.startCutoffLabel, 2, 3)
                self.grid.addWidget(self.startCutoffWidget, 2, 4)
                
                self.higherCutoffLabel = QLabel(self.tr('Higher Cutoff: '))
                self.endCutoffLabel = QLabel(self.tr('End Transition Band = Cutoff *'))
                self.higherCutoffWidget = QLineEdit('')
                self.higherCutoffWidget.setValidator(QDoubleValidator(self))
                endCutoff = 1.2
                self.endCutoffWidget = QLineEdit(self.currLocale.toString(endCutoff)) 
                self.endCutoffWidget.setValidator(QDoubleValidator(self))
                self.grid.addWidget(self.higherCutoffLabel, 3, 1)
                self.grid.addWidget(self.higherCutoffWidget, 3, 2)
                self.grid.addWidget(self.endCutoffLabel, 3, 3)
                self.grid.addWidget(self.endCutoffWidget, 3, 4)
            elif self.currFilterType == self.tr('bandstop'):
                self.lowerCutoffLabel = QLabel(self.tr('Lower Cutoff: '))
                self.endCutoffLabel = QLabel(self.tr('End Transition Band = Cutoff *'))
                self.lowerCutoffWidget = QLineEdit('')
                self.lowerCutoffWidget.setValidator(QDoubleValidator(self))
                endCutoff = 1.2
                self.endCutoffWidget = QLineEdit(self.currLocale.toString(endCutoff)) 
                self.endCutoffWidget.setValidator(QDoubleValidator(self))
                self.grid.addWidget(self.lowerCutoffLabel, 2, 1)
                self.grid.addWidget(self.lowerCutoffWidget, 2, 2)
                self.grid.addWidget(self.endCutoffLabel, 2, 3)
                self.grid.addWidget(self.endCutoffWidget, 2, 4)
                
                self.higherCutoffLabel = QLabel(self.tr('Higher Cutoff: '))
                self.startCutoffLabel = QLabel(self.tr('Start Transition Band = Cutoff *'))
                self.higherCutoffWidget = QLineEdit('')
                self.higherCutoffWidget.setValidator(QDoubleValidator(self))
                startCutoff = 0.8
                self.startCutoffWidget = QLineEdit(self.currLocale.toString(startCutoff)) 
                self.startCutoffWidget.setValidator(QDoubleValidator(self))
                self.grid.addWidget(self.higherCutoffLabel, 3, 1)
                self.grid.addWidget(self.higherCutoffWidget, 3, 2)
                self.grid.addWidget(self.startCutoffLabel, 3, 3)
                self.grid.addWidget(self.startCutoffWidget, 3, 4)
