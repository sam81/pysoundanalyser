#   Copyright (C) 2010-2012 Samuele Carcagno <sam.carcagno@gmail.com>
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

class cutDialog(QtGui.QDialog):
    def __init__(self, parent, snd):
        QtGui.QDialog.__init__(self, parent)
        
        self.currLocale = self.parent().prm['data']['currentLocale']
        self.currLocale.setNumberOptions(self.currLocale.OmitGroupSeparator | self.currLocale.RejectGroupSeparator)
        grid = QtGui.QGridLayout()
        n = 0
       

            
        fromLabel = QtGui.QLabel(self.tr('From: '))
        grid.addWidget(fromLabel, n, 0)
        self.fromWidget = QtGui.QLineEdit('0')
        self.fromWidget.setValidator(QtGui.QDoubleValidator(self))
        grid.addWidget(self.fromWidget, n, 1)
        
        unitLabel = QtGui.QLabel(self.tr('Unit: '))
        grid.addWidget(unitLabel, n, 2)
        self.unitChooser = QtGui.QComboBox()
        self.unitChooser.addItems([self.tr("Seconds"), self.tr("Milliseconds"), self.tr("Samples")])
        self.unitChooser.setCurrentIndex(0)
        grid.addWidget(self.unitChooser, n, 3)
        
        n = n+1
        toLabel = QtGui.QLabel(self.tr('To: '))
        grid.addWidget(toLabel, n, 0)
        self.toWidget = QtGui.QLineEdit('0')
        self.toWidget.setValidator(QtGui.QDoubleValidator(self))
        grid.addWidget(self.toWidget, n, 1)
        n = n+1
        
        
        
        buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok|
                                     QtGui.QDialogButtonBox.Cancel)
        
        self.connect(buttonBox, QtCore.SIGNAL("accepted()"),
                     self, QtCore.SLOT("accept()"))
        self.connect(buttonBox, QtCore.SIGNAL("rejected()"),
                     self, QtCore.SLOT("reject()"))
        grid.addWidget(buttonBox, n, 3)
        self.setLayout(grid)
        self.setWindowTitle(self.tr("Cut"))

  
        
