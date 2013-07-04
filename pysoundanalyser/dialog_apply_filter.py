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

class applyFIR2PresetsDialog(QtGui.QDialog):
    def __init__(self, parent):
        QtGui.QDialog.__init__(self, parent)
        self.prm = parent.prm
        self.currLocale = self.parent().prm['data']['currentLocale']
        self.currLocale.setNumberOptions(self.currLocale.OmitGroupSeparator | self.currLocale.RejectGroupSeparator)
        vbl = QtGui.QVBoxLayout()
        self.grid = QtGui.QGridLayout()

        
        filterTypeLabel = QtGui.QLabel(self.tr('Filter Type: '))
        self.filterChooser = QtGui.QComboBox()
        self.filterChooser.addItems([self.tr('lowpass'), self.tr('highpass'), self.tr('bandpass'), self.tr('bandstop')])
        self.filterChooser.setCurrentIndex(0)
        self.grid.addWidget(self.filterChooser, 0, 1)
        self.connect(self.filterChooser,  QtCore.SIGNAL("currentIndexChanged(int)"), self.onChangeFilterType)
        self.filterOrderLabel = QtGui.QLabel(self.tr('Filter Order: '))
        self.filterOrderWidget = QtGui.QLineEdit('256')
        self.filterOrderWidget.setValidator(QtGui.QIntValidator(self))
        self.grid.addWidget(self.filterOrderLabel, 0, 2)
        self.grid.addWidget(self.filterOrderWidget, 0, 3)

        self.currFilterType = self.tr('lowpass')
        self.cutoffLabel = QtGui.QLabel(self.tr('Cutoff: '))
        self.endCutoffLabel = QtGui.QLabel(self.tr('End Transition Band = Cutoff *'))
        self.cutoffWidget = QtGui.QLineEdit('')
        self.cutoffWidget.setValidator(QtGui.QDoubleValidator(self))
        endCutoff = 1.2
        self.endCutoffWidget = QtGui.QLineEdit(self.currLocale.toString(endCutoff))
        self.endCutoffWidget.setValidator(QtGui.QDoubleValidator(self))
        self.grid.addWidget(self.cutoffLabel, 2, 1)
        self.grid.addWidget(self.cutoffWidget, 2, 2)
        self.grid.addWidget(self.endCutoffLabel, 2, 3)
        self.grid.addWidget(self.endCutoffWidget, 2, 4)

       
        buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok|
                                     QtGui.QDialogButtonBox.Cancel)
        
        self.connect(buttonBox, QtCore.SIGNAL("accepted()"),
                     self, QtCore.SLOT("accept()"))
        self.connect(buttonBox, QtCore.SIGNAL("rejected()"),
                     self, QtCore.SLOT("reject()"))

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
                self.cutoffLabel.setParent(None)
                self.grid.removeWidget(self.endCutoffLabel)
                self.endCutoffLabel.setParent(None)
                self.grid.removeWidget(self.cutoffWidget)
                self.cutoffWidget.setParent(None)
                self.grid.removeWidget(self.endCutoffWidget)
                self.endCutoffWidget.setParent(None)

            elif prevFilterType == self.tr('highpass'):
                self.grid.removeWidget(self.cutoffLabel)
                self.cutoffLabel.setParent(None)
                self.grid.removeWidget(self.startCutoffLabel)
                self.startCutoffLabel.setParent(None)
                self.grid.removeWidget(self.cutoffWidget)
                self.cutoffWidget.setParent(None)
                self.grid.removeWidget(self.startCutoffWidget)
                self.startCutoffWidget.setParent(None)
            elif prevFilterType == self.tr('bandpass') or prevFilterType == self.tr('bandstop'):
                self.grid.removeWidget(self.lowerCutoffLabel)
                self.lowerCutoffLabel.setParent(None)
                self.grid.removeWidget(self.startCutoffLabel)
                self.startCutoffLabel.setParent(None)
                self.grid.removeWidget(self.lowerCutoffWidget)
                self.lowerCutoffWidget.setParent(None)
                self.grid.removeWidget(self.startCutoffWidget)
                self.startCutoffWidget.setParent(None)
                
                self.grid.removeWidget(self.higherCutoffLabel)
                self.higherCutoffLabel.setParent(None)
                self.grid.removeWidget(self.endCutoffLabel)
                self.endCutoffLabel.setParent(None)
                self.grid.removeWidget(self.higherCutoffWidget)
                self.higherCutoffWidget.setParent(None)
                self.grid.removeWidget(self.endCutoffWidget)
                self.endCutoffWidget.setParent(None)
                
            if self.currFilterType == self.tr('lowpass'):
                self.cutoffLabel = QtGui.QLabel(self.tr('Cutoff: '))
                self.endCutoffLabel = QtGui.QLabel(self.tr('End Transition Band = Cutoff *'))
                self.cutoffWidget = QtGui.QLineEdit('')
                self.cutoffWidget.setValidator(QtGui.QDoubleValidator(self))
                endCutoff = 1.2
                self.endCutoffWidget = QtGui.QLineEdit(self.currLocale.toString(endCutoff))
                self.endCutoffWidget.setValidator(QtGui.QDoubleValidator(self))
                self.grid.addWidget(self.cutoffLabel, 2, 1)
                self.grid.addWidget(self.cutoffWidget, 2, 2)
                self.grid.addWidget(self.endCutoffLabel, 2, 3)
                self.grid.addWidget(self.endCutoffWidget, 2, 4)
            elif self.currFilterType == self.tr('highpass'):
                self.cutoffLabel = QtGui.QLabel(self.tr('Cutoff: '))
                self.startCutoffLabel = QtGui.QLabel(self.tr('Start Transition Band = Cutoff *'))
                self.cutoffWidget = QtGui.QLineEdit('')
                self.cutoffWidget.setValidator(QtGui.QDoubleValidator(self))
                startCutoff = 0.8
                self.startCutoffWidget = QtGui.QLineEdit(self.currLocale.toString(startCutoff)) 
                self.startCutoffWidget.setValidator(QtGui.QDoubleValidator(self))
                self.grid.addWidget(self.cutoffLabel, 2, 1)
                self.grid.addWidget(self.cutoffWidget, 2, 2)
                self.grid.addWidget(self.startCutoffLabel, 2, 3)
                self.grid.addWidget(self.startCutoffWidget, 2, 4)
            elif self.currFilterType == self.tr('bandpass'):
                self.lowerCutoffLabel = QtGui.QLabel(self.tr('Lower Cutoff: '))
                self.startCutoffLabel = QtGui.QLabel(self.tr('Start Transition Band = Cutoff *'))
                self.lowerCutoffWidget = QtGui.QLineEdit('')
                self.lowerCutoffWidget.setValidator(QtGui.QDoubleValidator(self))
                startCutoff = 0.8
                self.startCutoffWidget = QtGui.QLineEdit(self.currLocale.toString(startCutoff)) 
                self.startCutoffWidget.setValidator(QtGui.QDoubleValidator(self))
                self.grid.addWidget(self.lowerCutoffLabel, 2, 1)
                self.grid.addWidget(self.lowerCutoffWidget, 2, 2)
                self.grid.addWidget(self.startCutoffLabel, 2, 3)
                self.grid.addWidget(self.startCutoffWidget, 2, 4)
                
                self.higherCutoffLabel = QtGui.QLabel(self.tr('Higher Cutoff: '))
                self.endCutoffLabel = QtGui.QLabel(self.tr('End Transition Band = Cutoff *'))
                self.higherCutoffWidget = QtGui.QLineEdit('')
                self.higherCutoffWidget.setValidator(QtGui.QDoubleValidator(self))
                endCutoff = 1.2
                self.endCutoffWidget = QtGui.QLineEdit(self.currLocale.toString(endCutoff)) 
                self.endCutoffWidget.setValidator(QtGui.QDoubleValidator(self))
                self.grid.addWidget(self.higherCutoffLabel, 3, 1)
                self.grid.addWidget(self.higherCutoffWidget, 3, 2)
                self.grid.addWidget(self.endCutoffLabel, 3, 3)
                self.grid.addWidget(self.endCutoffWidget, 3, 4)
            elif self.currFilterType == self.tr('bandstop'):
                self.lowerCutoffLabel = QtGui.QLabel(self.tr('Lower Cutoff: '))
                self.endCutoffLabel = QtGui.QLabel(self.tr('End Transition Band = Cutoff *'))
                self.lowerCutoffWidget = QtGui.QLineEdit('')
                self.lowerCutoffWidget.setValidator(QtGui.QDoubleValidator(self))
                endCutoff = 1.2
                self.endCutoffWidget = QtGui.QLineEdit(self.currLocale.toString(endCutoff)) 
                self.endCutoffWidget.setValidator(QtGui.QDoubleValidator(self))
                self.grid.addWidget(self.lowerCutoffLabel, 2, 1)
                self.grid.addWidget(self.lowerCutoffWidget, 2, 2)
                self.grid.addWidget(self.endCutoffLabel, 2, 3)
                self.grid.addWidget(self.endCutoffWidget, 2, 4)
                
                self.higherCutoffLabel = QtGui.QLabel(self.tr('Higher Cutoff: '))
                self.startCutoffLabel = QtGui.QLabel(self.tr('Start Transition Band = Cutoff *'))
                self.higherCutoffWidget = QtGui.QLineEdit('')
                self.higherCutoffWidget.setValidator(QtGui.QDoubleValidator(self))
                startCutoff = 0.8
                self.startCutoffWidget = QtGui.QLineEdit(self.currLocale.toString(startCutoff)) 
                self.startCutoffWidget.setValidator(QtGui.QDoubleValidator(self))
                self.grid.addWidget(self.higherCutoffLabel, 3, 1)
                self.grid.addWidget(self.higherCutoffWidget, 3, 2)
                self.grid.addWidget(self.startCutoffLabel, 3, 3)
                self.grid.addWidget(self.startCutoffWidget, 3, 4)
