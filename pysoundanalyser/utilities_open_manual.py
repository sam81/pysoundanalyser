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
    from PyQt5.QtGui import QDesktopServices
elif pyqtversion == 6:
    from PyQt6 import QtGui, QtCore
    from PyQt6.QtGui import QDesktopServices
    
import os

def onShowManualPdf():
    fileToOpen = os.path.abspath(os.path.dirname(__file__)) + '/doc/_build/latex/pysoundanalyser.pdf'
    QDesktopServices.openUrl(QtCore.QUrl.fromLocalFile(fileToOpen))

def onShowManualHTML():
    fileToOpen = os.path.abspath(os.path.dirname(__file__)) + '/doc/_build/html/index.html'
    QDesktopServices.openUrl(QtCore.QUrl.fromLocalFile(fileToOpen))


