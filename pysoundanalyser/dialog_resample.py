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
    from PyQt5.QtGui import QIntValidator
    from PyQt5.QtWidgets import QComboBox, QDialog, QDialogButtonBox, QGridLayout, QLabel, QLineEdit, QMessageBox
elif pyqtversion == 6:
    from PyQt6 import QtGui, QtCore
    from PyQt6.QtGui import QIntValidator
    from PyQt6.QtWidgets import QComboBox, QDialog, QDialogButtonBox, QGridLayout, QLabel, QLineEdit, QMessageBox

class resampleDialog(QDialog):
    def __init__(self, parent, multipleSelection, currSampRate):
        QDialog.__init__(self, parent)

        self.currLocale = self.parent().prm['appData']['currentLocale']
        self.currLocale.setNumberOptions(self.currLocale.NumberOption.OmitGroupSeparator | self.currLocale.NumberOption.RejectGroupSeparator)
        grid = QGridLayout()
        n = 0
        if multipleSelection == False:
            currSampRateLabel = QLabel(self.tr("Current sampling rate: ") + self.currLocale.toString(currSampRate)) 
            grid.addWidget(currSampRateLabel, n, 0)
            n = n+1
        newSampRateLabel = QLabel(self.tr('New Sampling Rate: '))
        grid.addWidget(newSampRateLabel, n, 0)
        self.newSampRateWidget = QLineEdit('48000')
        self.newSampRateWidget.setValidator(QIntValidator(self))
        grid.addWidget(self.newSampRateWidget, n, 1)
        self.newSampRateWidget.editingFinished.connect(self.onSampRateChanged)
        n = n+1

        convertorLabel = QLabel(self.tr('Resampling Algorithm: '))
        grid.addWidget(convertorLabel, n, 0)
        self.convertorChooser = QComboBox()
        self.convertorChooser.addItems(['fourier'])
        self.convertorChooser.setCurrentIndex(0)
        grid.addWidget(self.convertorChooser, n, 1)

        n = n+1

        winLabel = QLabel(self.tr('Window Type: '))
        grid.addWidget(winLabel, n, 0)
        self.winChooser = QComboBox()
        self.winChooser.addItems(self.parent().prm['appData']['available_windows'])
        self.winChooser.setCurrentIndex(self.winChooser.findText(self.parent().prm['pref']['smoothingWindow']))
        grid.addWidget(self.winChooser, n, 1)

        n = n+1
        
        buttonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok|
                                     QDialogButtonBox.StandardButton.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
        grid.addWidget(buttonBox, n, 1)
        self.setLayout(grid)
        self.setWindowTitle(self.tr("Resample"))
        self.newSampRate = int(self.newSampRateWidget.text())

    def onSampRateChanged(self):
        newSampRate = int(self.newSampRateWidget.text())
        if newSampRate < 1:
            QMessageBox.warning(self, self.tr('Warning'), self.tr('New sampling rate too small'))
        else:
            self.newSampRate = newSampRate
