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

class concatenateDialog(QtGui.QDialog):
    def __init__(self, parent, snd1, snd2):
        QtGui.QDialog.__init__(self, parent)
        
        self.order = 'given'
        self.snd1 = snd1
        self.snd2 = snd2
        self.currLocale = self.parent().prm['data']['currentLocale']
        self.currLocale.setNumberOptions(self.currLocale.OmitGroupSeparator | self.currLocale.RejectGroupSeparator)
        grid = QtGui.QGridLayout()
        n = 0
       

            
        snd1Label = QtGui.QLabel(self.tr('Sound 1: '))
        grid.addWidget(snd1Label, n, 0)
        snd2Label = QtGui.QLabel(self.tr('Sound 2: '))
        grid.addWidget(snd2Label, n, 1)
       

        n = n+1
        self.snd1Widget = QtGui.QLineEdit(snd1['label'])
        self.snd1Widget.setReadOnly(True)
        grid.addWidget(self.snd1Widget, n, 0)
        self.snd2Widget = QtGui.QLineEdit(snd2['label'])
        self.snd2Widget.setReadOnly(True)
        grid.addWidget(self.snd2Widget, n, 1)
        swapButton = QtGui.QPushButton(self.tr("Swap Sounds"), self)
        QtCore.QObject.connect(swapButton,
                               QtCore.SIGNAL('clicked()'), self.onClickSwapButton)
        grid.addWidget(swapButton, n, 2)
        n = n+1
        
        delayTypeLabel = QtGui.QLabel(self.tr('Delay Type: '))
        grid.addWidget(delayTypeLabel, n, 0)
        self.delayTypeChooser = QtGui.QComboBox()
        self.delayTypeChooser.addItems(['offset to onset', 'onset to onset'])
        self.delayTypeChooser.setCurrentIndex(0)
        grid.addWidget(self.delayTypeChooser, n, 1)

        n = n+1
        delayLabel = QtGui.QLabel(self.tr('Delay (ms): '))
        grid.addWidget(delayLabel, n, 0)
        self.delayWidget = QtGui.QLineEdit('0')
        self.delayWidget.setValidator(QtGui.QDoubleValidator(self))
        grid.addWidget(self.delayWidget, n, 1)

        n = n+1
        outNameLabel = QtGui.QLabel(self.tr('Sound Label: '))
        grid.addWidget(outNameLabel, n, 0)
        self.outNameWidget = QtGui.QLineEdit(str(snd1['label']+'-'+snd2['label']))
        grid.addWidget(self.outNameWidget, n, 1)

        n = n+1
        outChanLabel = QtGui.QLabel(self.tr('Output Channel: '))
        grid.addWidget(outChanLabel, n, 0)
        self.outChanChooser = QtGui.QComboBox()
        self.outChanChooser.addItems([self.tr('Right'), self.tr('Left')])
        if snd1['chan'] == snd2['chan']:
            self.outChanChooser.setCurrentIndex(self.outChanChooser.findText(snd1['chan']))
        else:
            self.outChanChooser.setCurrentIndex(0)
        grid.addWidget(self.outChanChooser, n, 1)

        n = n+1

        
        
        
        buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok|
                                     QtGui.QDialogButtonBox.Cancel)
        
        self.connect(buttonBox, QtCore.SIGNAL("accepted()"),
                     self, QtCore.SLOT("accept()"))
        self.connect(buttonBox, QtCore.SIGNAL("rejected()"),
                     self, QtCore.SLOT("reject()"))
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
       
        
