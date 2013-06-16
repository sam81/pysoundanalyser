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

class resampleDialog(QtGui.QDialog):
    def __init__(self, parent, multipleSelection, currSampRate):
        QtGui.QDialog.__init__(self, parent)

        self.currLocale = self.parent().prm['data']['currentLocale']
        self.currLocale.setNumberOptions(self.currLocale.OmitGroupSeparator | self.currLocale.RejectGroupSeparator)
        grid = QtGui.QGridLayout()
        n = 0
        if multipleSelection == False:
            currSampRateLabel = QtGui.QLabel(self.currLocale.toString(currSampRate)) 
            grid.addWidget(currSampRateLabel, n, 0)
            n = n+1

            
        newSampRateLabel = QtGui.QLabel(self.tr('New Sampling Rate: '))
        grid.addWidget(newSampRateLabel, n, 0)
        self.newSampRateWidget = QtGui.QLineEdit('48000')
        self.newSampRateWidget.setValidator(QtGui.QIntValidator(self))
        grid.addWidget(self.newSampRateWidget, n, 1)
        self.connect(self.newSampRateWidget, QtCore.SIGNAL('editingFinished()'), self.onSampRateChanged)
        n = n+1

        convertorLabel = QtGui.QLabel(self.tr('Resampling Algorithm: '))
        grid.addWidget(convertorLabel, n, 0)
        self.convertorChooser = QtGui.QComboBox()
        self.convertorChooser.addItems(['fourier'])
        self.convertorChooser.setCurrentIndex(0)
        grid.addWidget(self.convertorChooser, n, 1)

        n = n+1

        winLabel = QtGui.QLabel(self.tr('Window Type: '))
        grid.addWidget(winLabel, n, 0)
        self.winChooser = QtGui.QComboBox()
        self.winChooser.addItems(self.parent().prm['data']['available_windows'])
        self.winChooser.setCurrentIndex(self.winChooser.findText(self.parent().prm['pref']['smoothingWindow']))
        grid.addWidget(self.winChooser, n, 1)

        n = n+1
        
        buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok|
                                     QtGui.QDialogButtonBox.Cancel)
        
        self.connect(buttonBox, QtCore.SIGNAL("accepted()"),
                     self, QtCore.SLOT("accept()"))
        self.connect(buttonBox, QtCore.SIGNAL("rejected()"),
                     self, QtCore.SLOT("reject()"))
        grid.addWidget(buttonBox, n, 1)
        self.setLayout(grid)
        self.setWindowTitle(self.tr("Resample"))

    def onSampRateChanged(self):
        newSampRate = int(self.newSampRateWidget.text())
        if newSampRate < 1:
            QtGui.QMessageBox.warning(self, self.tr('Warning'), self.tr('New sampling rate too small'))
        else:
            self.newSampRate = newSampRate
