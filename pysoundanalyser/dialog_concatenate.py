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
    from PyQt5.QtGui import QDoubleValidator
    from PyQt5.QtWidgets import QComboBox, QDialog, QDialogButtonBox, QGridLayout, QLabel, QLineEdit, QPushButton
elif pyqtversion == 6:
    from PyQt6 import QtGui, QtCore
    from PyQt6.QtGui import QDoubleValidator
    from PyQt6.QtWidgets import QComboBox, QDialog, QDialogButtonBox, QGridLayout, QLabel, QLineEdit, QPushButton

class concatenateDialog(QDialog):
    def __init__(self, parent, snd1, snd2):
        QDialog.__init__(self, parent)
        
        self.order = 'given'
        self.snd1 = snd1
        self.snd2 = snd2
        self.currLocale = self.parent().prm['appData']['currentLocale']
        self.currLocale.setNumberOptions(self.currLocale.NumberOption.OmitGroupSeparator | self.currLocale.NumberOption.RejectGroupSeparator)
        grid = QGridLayout()
        n = 0
       
            
        snd1Label = QLabel(self.tr('Sound 1: '))
        grid.addWidget(snd1Label, n, 0)
        snd2Label = QLabel(self.tr('Sound 2: '))
        grid.addWidget(snd2Label, n, 1)
       

        n = n+1
        self.snd1Widget = QLineEdit(snd1['label'])
        self.snd1Widget.setReadOnly(True)
        grid.addWidget(self.snd1Widget, n, 0)
        self.snd2Widget = QLineEdit(snd2['label'])
        self.snd2Widget.setReadOnly(True)
        grid.addWidget(self.snd2Widget, n, 1)
        swapButton = QPushButton(self.tr("Swap Sounds"), self)
        swapButton.clicked.connect(self.onClickSwapButton)
        grid.addWidget(swapButton, n, 2)
        n = n+1
        
        delayTypeLabel = QLabel(self.tr('Delay Type: '))
        grid.addWidget(delayTypeLabel, n, 0)
        self.delayTypeChooser = QComboBox()
        self.delayTypeChooser.addItems(['offset to onset', 'onset to onset'])
        self.delayTypeChooser.setCurrentIndex(0)
        grid.addWidget(self.delayTypeChooser, n, 1)

        n = n+1
        delayLabel = QLabel(self.tr('Delay (ms): '))
        grid.addWidget(delayLabel, n, 0)
        self.delayWidget = QLineEdit('0')
        self.delayWidget.setValidator(QDoubleValidator(self))
        grid.addWidget(self.delayWidget, n, 1)

        n = n+1
        outNameLabel = QLabel(self.tr('Sound Label: '))
        grid.addWidget(outNameLabel, n, 0)
        self.outNameWidget = QLineEdit(str(snd1['label']+'-'+snd2['label']))
        grid.addWidget(self.outNameWidget, n, 1)

        n = n+1
        outChanLabel = QLabel(self.tr('Output Channel: '))
        grid.addWidget(outChanLabel, n, 0)
        self.outChanChooser = QComboBox()
        self.outChanChooser.addItems([self.tr('Right'), self.tr('Left')])
        if snd1['chan'] == snd2['chan']:
            self.outChanChooser.setCurrentIndex(self.outChanChooser.findText(snd1['chan']))
        else:
            self.outChanChooser.setCurrentIndex(0)
        grid.addWidget(self.outChanChooser, n, 1)

        n = n+1

        
        
        
        buttonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok|
                                     QDialogButtonBox.StandardButton.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        grid.addWidget(buttonBox, n, 2)
        self.setLayout(grid)
        self.setWindowTitle(self.tr("Concatenate"))

    def onClickSwapButton(self):
        if self.order == 'given':
            self.order = 'swapped'
            self.snd1Widget.setText(self.snd2['label'])
            self.snd2Widget.setText(self.snd1['label'])
        elif self.order == 'swapped':
            self.order = 'given'
            self.snd1Widget.setText(self.snd1['label'])
            self.snd2Widget.setText(self.snd2['label'])
       
        
