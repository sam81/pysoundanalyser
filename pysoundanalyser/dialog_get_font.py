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
#    along with pysoundanalyser. If not, see <http://www.gnu.org/licenses/>.

import matplotlib
from .pyqtver import*
if pyqtversion == 5:
    from PyQt5 import QtGui, QtCore
    from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QGridLayout, QLabel, QListWidget, QPushButton
    matplotlib.rcParams['backend'] = "Qt5Agg"
elif pyqtversion == 6:
    from PyQt6 import QtGui, QtCore
    from PyQt6.QtWidgets import QDialog, QDialogButtonBox, QGridLayout, QLabel, QListWidget, QPushButton
    matplotlib.rcParams['backend'] = "Qt5Agg"
import matplotlib.font_manager as fm
from numpy import unique

import os, pickle
 
class getFontDialog(QDialog):
    def __init__(self, parent, currFont):
        QDialog.__init__(self, parent)
        #---------------------
        self.currFont = currFont
        if self.currFont.get_file() == None:
            self.currFontFile = fm.findfont(self.currFont)
            self.currFontSize = self.currFont.get_size()
            self.currFontStyle = self.currFont.get_style()
            self.currFontWeight = self.currFont.get_weight()
            self.currFont = fm.FontProperties(fname=self.currFontFile, style=self.currFontStyle, weight=self.currFontWeight, size=self.currFontSize)
            self.currFontFamily = self.currFont.get_name()
        else:
            self.currFontFile = self.currFont.get_file()
            self.currFontSize = self.currFont.get_size()
            self.currFontStyle = self.currFont.get_style()
            self.currFontWeight = self.currFont.get_weight()
            self.currFontFamily = self.currFont.get_name()
            
        self.fontsCacheFile = os.path.expanduser("~") +'/.config/pysoundanalyser/fontsCache'
        if os.path.exists(self.fontsCacheFile):
            fIn = open(self.fontsCacheFile, 'rb')
            self.fontsDic = pickle.load(fIn)
            fIn.close()
        else:
            self.refreshFontsCache()
        
        self.currLocale = self.parent().prm['appData']['currentLocale']
        self.currLocale.setNumberOptions(self.currLocale.NumberOption.OmitGroupSeparator | self.currLocale.NumberOption.RejectGroupSeparator)
        grid = QGridLayout()
      
        fontNameLabel = QLabel(self.tr('Font Name'))
        grid.addWidget(fontNameLabel, 0, 0)
        
        fontStyleLabel = QLabel(self.tr('Font Style'))
        grid.addWidget(fontStyleLabel, 0, 1)
        
        fontSizeLabel = QLabel(self.tr('Font Size'))
        grid.addWidget(fontSizeLabel, 0, 2)
        ind = sorted(self.fontsDic.keys()).index(self.currFontFamily)
        self.fontListWidget = QListWidget(self)
        self.fontListWidget.insertItems(0, sorted(self.fontsDic.keys()))
        self.fontListWidget.setCurrentRow(ind)
        self.fontListWidget.itemClicked.connect(self.onChangeFontName)
        grid.addWidget(self.fontListWidget, 1, 0)

        self.fontStylesWidget = QListWidget(self)
        self.fontStylesWidget.insertItems(0, self.fontsDic[sorted(self.fontsDic.keys())[ind]]['styleAbb'])
        indStyle = self.fontsDic[sorted(self.fontsDic.keys())[ind]]['styleAbb'].index(self.currFontStyle + ' ' + self.currFontWeight)
        self.fontStylesWidget.setCurrentRow(indStyle)
        grid.addWidget(self.fontStylesWidget, 1, 1)

        self.fontSizeWidget = QListWidget(self)
        self.pointSizeList = ['4', '5', '6', '7', '8', '9', '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '22', '24', '26', '28', '32', '48', '64', '72', '80', '96', '128']
        self.fontSizeWidget.insertItems(0, self.pointSizeList)
        self.fontSizeWidget.setCurrentRow(self.pointSizeList.index(str(int(self.currFontSize))))
        grid.addWidget(self.fontSizeWidget, 1, 2)
       
        buttonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok|
                                     QDialogButtonBox.StandardButton.Cancel)
        buttonBox.accepted.connect(self.accept)
        buttonBox.rejected.connect(self.reject)
       
        grid.addWidget(buttonBox, 3, 2)

        refreshFontsCacheButton = QPushButton(self.tr("Refresh fonts cache"), self)
        refreshFontsCacheButton.clicked.connect(self.onClickRefreshFontsCacheButton)
        grid.addWidget(refreshFontsCacheButton, 3, 0)
        
        self.setLayout(grid)
        self.setWindowTitle(self.tr("Choose Font"))

    def onChangeFontName(self):
        currFontName = str(self.fontListWidget.currentItem().text())
        self.fontStylesWidget.clear()
        self.fontStylesWidget.insertItems(0, self.fontsDic[currFontName]['styleAbb'])
        self.fontStylesWidget.setCurrentRow(0)

    def onClickRefreshFontsCacheButton(self):
        #ind = sorted(self.fontsDic.keys()).index(self.currFontFamily)
        #indStyle = self.fontsDic[sorted(self.fontsDic.keys())[ind]]['styleAbb'].index(self.currFontStyle + ' ' + self.currFontWeight)
        ind = self.fontListWidget.currentRow() #sorted(self.fontsDic.keys()).index(self.currFontFamily)
        indStyle = self.fontStylesWidget.currentRow() #self.fontsDic[sorted(self.fontsDic.keys())[ind]]['styleAbb'].index(self.currFontStyle + ' ' + self.currFontWeight)
        self.refreshFontsCache()
        self.fontListWidget.clear()
        self.fontStylesWidget.clear()
        self.fontListWidget.insertItems(0, sorted(self.fontsDic.keys()))
        self.fontListWidget.setCurrentRow(ind)
        self.fontStylesWidget.insertItems(0, self.fontsDic[sorted(self.fontsDic.keys())[ind]]['styleAbb'])
        self.fontStylesWidget.setCurrentRow(indStyle)
        
    def refreshFontsCache(self):
        x = fm.FontManager()
        weight_lookup = {
            '100': 'ultralight',
            '200': 'light',
            '400': 'normal',    
            '500': 'medium',     
            '600': 'demibold',   
            '700': 'bold',       
            '800': 'extra bold', 
            '900': 'black'}

        fontList = x.ttflist
        fontNamesAll = []
        for i in range(len(x.ttflist)):
            fontNamesAll.append(x.ttflist[i].name)
        fontNames = unique(fontNamesAll)

        self.fontsDic = {}
        for i in range(len(fontNames)):
            self.fontsDic[fontNames[i]] = {}
            self.fontsDic[fontNames[i]]['style'] = []
            self.fontsDic[fontNames[i]]['styleAbb'] = []

        for font in fontList:
            style = font.style
            weight = font.weight
            self.fontsDic[font.name]['style'].append(style + ':' + str(weight) + ':' + font.fname)
            try:
                weightName = weight_lookup[str(weight)]
            except:
                if weight <= 100:
                    weightName = 'ultralight'
                elif weight <= 200:
                    weightName = 'light'
                elif weight <= 400:
                    weightName = 'normal'
                elif weight <= 500:
                    weightName = 'medium'
                elif weight <= 600:
                    weightName = 'demibold'
                elif weight <= 700:
                    weightName = 'bold'
                elif weight <= 800:
                    weightName = 'extra bold'
                elif weight <= 900:
                    weightName = 'black'
                    # print(font.name)
                    # print(weightName)
                    # print(weight)

            styleName = style + ' ' + weightName #+ ' (weight' + str(weight) + ')'
            self.fontsDic[font.name]['styleAbb'].append(styleName)

        f = open(self.fontsCacheFile, 'wb')
        pickle.dump(self.fontsDic, f)
        f.close()
        #---------------------
