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
    from PyQt5.QtWidgets import QComboBox, QDialog, QDialogButtonBox, QGridLayout, QLabel, QLineEdit
elif pyqtversion == 6:
    from PyQt6 import QtGui, QtCore
    from PyQt6.QtGui import QDoubleValidator
    from PyQt6.QtWidgets import QComboBox, QDialog, QDialogButtonBox, QGridLayout, QLabel, QLineEdit

class cutDialog(QDialog):
    def __init__(self, parent, snd):
        QDialog.__init__(self, parent)
        
        self.currLocale = self.parent().prm['appData']['currentLocale']
        self.currLocale.setNumberOptions(self.currLocale.NumberOption.OmitGroupSeparator | self.currLocale.NumberOption.RejectGroupSeparator)
        grid = QGridLayout()
        n = 0
       
            
        fromLabel = QLabel(self.tr('From: '))
        grid.addWidget(fromLabel, n, 0)
        self.fromWidget = QLineEdit('0')
        self.fromWidget.setValidator(QDoubleValidator(self))
        grid.addWidget(self.fromWidget, n, 1)
        
        unitLabel = QLabel(self.tr('Unit: '))
        grid.addWidget(unitLabel, n, 2)
        self.unitChooser = QComboBox()
        self.unitChooser.addItems([self.tr("Seconds"), self.tr("Milliseconds"), self.tr("Samples")])
        self.unitChooser.setCurrentIndex(0)
        grid.addWidget(self.unitChooser, n, 3)
        
        n = n+1
        toLabel = QLabel(self.tr('To: '))
        grid.addWidget(toLabel, n, 0)
        self.toWidget = QLineEdit('0')
        self.toWidget.setValidator(QDoubleValidator(self))
        grid.addWidget(self.toWidget, n, 1)
        n = n+1
        
        buttonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok|
                                     QDialogButtonBox.StandardButton.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        grid.addWidget(buttonBox, n, 3)
        self.setLayout(grid)
        self.setWindowTitle(self.tr("Cut"))

  
        
