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

class changeChannelDialog(QtGui.QDialog):
    def __init__(self, parent, multipleSelection, currChan):
        QtGui.QDialog.__init__(self, parent)

        grid = QtGui.QGridLayout()
        n = 0


        chooserLabel = QtGui.QLabel(self.tr('Channel: '))
        self.chooser = QtGui.QComboBox()
        self.chooser.addItems([self.tr('Right'), self.tr('Left')])
        self.chooser.setCurrentIndex(self.chooser.findText(currChan))
        grid.addWidget(self.chooser, n, 1)
        n = n+1
     
        
        buttonBox = QtGui.QDialogButtonBox(QtGui.QDialogButtonBox.Ok|
                                     QtGui.QDialogButtonBox.Cancel)
        
        self.connect(buttonBox, QtCore.SIGNAL("accepted()"),
                     self, QtCore.SLOT("accept()"))
        self.connect(buttonBox, QtCore.SIGNAL("rejected()"),
                     self, QtCore.SLOT("reject()"))
        grid.addWidget(buttonBox, n, 1)
        self.setLayout(grid)
        self.setWindowTitle(self.tr("Change Channel"))

   
