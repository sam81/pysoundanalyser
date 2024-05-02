#!/usr/bin/env python
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

import argparse, sys, platform, os, copy, logging, pickle, platform, signal, scipy, time, traceback
from pysoundanalyser.pyqtver import*
if pyqtversion == 5:
    from PyQt5 import QtGui, QtCore
    from PyQt5.QtGui import QIcon
    from PyQt5.QtWidgets import QAbstractItemView, QAction, QApplication, QDialog, QDialogButtonBox, QGridLayout, QFileDialog, QInputDialog, QLabel, QMainWindow, QMessageBox, QPushButton, QScrollArea, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget
elif pyqtversion == 6:
    from PyQt6 import QtGui, QtCore
    from PyQt6.QtGui import QAction, QIcon
    from PyQt6.QtWidgets import QAbstractItemView, QApplication, QDialog, QDialogButtonBox, QGridLayout, QFileDialog, QInputDialog, QLabel, QMainWindow, QMessageBox, QPushButton, QScrollArea, QTableWidget, QTableWidgetItem, QVBoxLayout, QWidget


from numpy import sin, cos, pi, sqrt, abs, arange, zeros, mean, concatenate, convolve, angle, real, log2, log10, int_, linspace, repeat, ceil, unique, hamming, hanning, blackman, bartlett, round, transpose
from numpy.fft import rfft, irfft, fft, ifft
from tempfile import mkstemp

from pysoundanalyser import qrc_resources
from pysoundanalyser.global_parameters import*
from pysoundanalyser._version_info import*
from pysoundanalyser.utilities_open_manual import*
from pysoundanalyser.threaded_plotters import*
from pysoundanalyser.audio_manager import*

__version__ = pysoundanalyser_version
signal.signal(signal.SIGINT, signal.SIG_DFL)

local_dir = os.path.expanduser("~") +'/.local/share/data/pysoundanalyser/'
if os.path.exists(local_dir) == False:
    os.makedirs(local_dir)
stderrFile = os.path.expanduser("~") +'/.local/share/data/pysoundanalyser/pysoundanalyser_stderr_log.txt'

logging.basicConfig(filename=stderrFile,level=logging.DEBUG,)


# def excepthook(except_type, except_val, tbck):
#     """ Show errors in message box"""
#     # recover traceback
#     tb = traceback.format_exception(except_type, except_val, tbck)
#     ret = QMessageBox.critical(None, "Critical Error! Something went wrong, the following info may help you troubleshooting",
#                                     ''.join(tb),
#                                     QMessageBox.StandardButton.Ok)
#     timeStamp = ''+ time.strftime("%d/%m/%y %H:%M:%S", time.localtime()) + ' ' + '\n'
#     logMsg = timeStamp + ''.join(tb)
#     logging.debug(logMsg)

def excepthook(except_type, except_val, tbck):
    """ Show errors in message box"""
    # recover traceback
    tb = traceback.format_exception(except_type, except_val, tbck)
    def onClickSaveTbButton():
        ftow = QFileDialog.getSaveFileName(None, 'Choose where to save the traceback', "traceback.txt", 'All Files (*)')[0]
        if len(ftow) > 0:
            if fnmatch.fnmatch(ftow, '*.txt') == False:
                ftow = ftow + '.txt'
            fName = open(ftow, 'w')
            fName.write("".join(tb))
            fName.close()
    
    diag = QDialog(None, Qt.WindowType.CustomizeWindowHint | Qt.WindowType.WindowCloseButtonHint)
    diag.window().setWindowTitle("Critical Error!")
    siz = QVBoxLayout()
    lay = QVBoxLayout()
    saveTbButton = QPushButton("Save Traceback", diag)
    saveTbButton.clicked.connect(onClickSaveTbButton)
    lab = QLabel("Sorry, something went wrong. The attached traceback can help you troubleshoot the problem: \n\n" + "".join(tb))
    lab.setMargin(10)
    lab.setWordWrap(True)
    lab.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
    lab.setStyleSheet("QLabel { background-color: white }");
    lay.addWidget(lab)

    sc = QScrollArea()
    sc.setWidget(lab)
    siz.addWidget(sc) #SCROLLAREA IS A WIDGET SO IT NEEDS TO BE ADDED TO A LAYOUT

    buttonBox = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok|QDialogButtonBox.StandardButton.Cancel)

    buttonBox.accepted.connect(diag.accept)
    buttonBox.rejected.connect(diag.reject)
    siz.addWidget(saveTbButton)
    siz.addWidget(buttonBox)
    diag.setLayout(siz)
    diag.exec()

    timeStamp = ''+ time.strftime("%d/%m/%y %H:%M:%S", time.localtime()) + ' ' + '\n'
    logMsg = timeStamp + ''.join(tb)
    logging.debug(logMsg)

if platform.system() == 'Windows':
    import winsound

from pysoundanalyser import sndlib
from pysoundanalyser.utility_functions import*
import pysoundanalyser.random_id as random_id
from pysoundanalyser.win_waveform_plot import*
from pysoundanalyser.win_spectrum_plot import*
from pysoundanalyser.win_spectrogram_plot import*
from pysoundanalyser.win_acf_plot import*
from pysoundanalyser.win_autocorrelogram_plot import*
from pysoundanalyser.dialog_edit_preferences import*
from pysoundanalyser.dialog_resample import*
from pysoundanalyser.dialog_save_sound import*
from pysoundanalyser.dialog_change_channel import*
from pysoundanalyser.dialog_concatenate import*
from pysoundanalyser.dialog_cut import*
from pysoundanalyser.dialog_apply_filter import*
from pysoundanalyser.dialog_generate_sound import*
from pysoundanalyser.dialog_generate_noise import*
from pysoundanalyser.dialog_generate_sinusoid import*

tmpprm = {}; tmpprm['appData'] = {}
tmpprm = set_global_parameters(tmpprm)
tmpprm = get_prefs(tmpprm)
if tmpprm['pref']['sound']['wavmanager'] == 'soundfile':
    from pysoundanalyser.wavpy_sndf import wavread, wavwrite
elif tmpprm['pref']['sound']['wavmanager'] == 'scipy':
    #from pysoundanalyser.scipy_wav import scipy_wavwrite, scipy_wavread
    from pysoundanalyser.wavpy import wavread, wavwrite

class applicationWindow(QMainWindow):
    """main window"""
    def __init__(self, prm):
        QMainWindow.__init__(self)
        self.setAcceptDrops(True)
        self.prm = prm
        self.prm['version'] = __version__
        self.prm['builddate'] = pysoundanalyser_builddate
        self.currLocale = prm['appData']['currentLocale']
        self.currLocale.setNumberOptions(self.currLocale.NumberOption.OmitGroupSeparator | self.currLocale.NumberOption.RejectGroupSeparator)
        self.setWindowTitle(self.tr("Python Sound Analyser"))
        self.audioManager = audioManager(self)
        # main widget
        self.main_widget = QWidget(self)
        #MENU-----------------------------------
        self.waveformPlotter = threadedWaveformPlot(self)
        self.menubar = self.menuBar()
        #FILE MENU
        self.fileMenu = self.menubar.addMenu(self.tr('&File'))

        exitButton = QAction(QIcon(':/exit.svg'), self.tr('Exit'), self)
        exitButton.setShortcut('Ctrl+Q')
        exitButton.setStatusTip(self.tr('Exit application'))
        exitButton.triggered.connect(self.close)
        self.statusBar()
        self.fileMenu.addAction(exitButton)


        #EDIT MENU
        self.editMenu = self.menubar.addMenu(self.tr('&Edit'))
        self.editPrefAction = QAction(self.tr('Preferences'), self)
        self.editMenu.addAction(self.editPrefAction)
        self.editPrefAction.triggered.connect(self.onEditPref)

        self.selectAllAction = QAction(self.tr('Select All'), self)
        self.editMenu.addAction(self.selectAllAction)
        self.selectAllAction.triggered.connect(self.onSelectAll)

        #GET MENU
        self.getMenu = self.menubar.addMenu(self.tr('&Get'))
        self.getRMSAction = QAction(self.tr('Root Mean Square'), self)
        self.getMenu.addAction(self.getRMSAction)
        self.getRMSAction.triggered.connect(self.onClickGetRMSButton)

        #GET MENU
        self.processMenu = self.menubar.addMenu(self.tr('&Process'))
        self.applyFilterMenu = self.processMenu.addMenu(self.tr('&Apply Filter'))
        self.fir2PresetsAction = QAction(self.tr('FIR2 Presets'), self)
        self.applyFilterMenu.addAction(self.fir2PresetsAction)
        self.fir2PresetsAction.triggered.connect(self.onClickApplyFIR2PresetsButton)
        

        #GENERATE MENU
        self.generateMenu = self.menubar.addMenu(self.tr('&Generate'))
        self.generateHarmComplAction = QAction(self.tr('Harmonic Complex'), self)
        self.generateMenu.addAction(self.generateHarmComplAction)
        self.generateHarmComplAction.triggered.connect(self.onClickGenerateHarmCompl)
        self.generateAMToneAction = QAction(self.tr('AM Tone'), self)
        self.generateMenu.addAction(self.generateAMToneAction)
        self.generateAMToneAction.triggered.connect(self.onClickGenerateAMTone)
        self.generateFMToneAction = QAction(self.tr('FM Tone'), self)
        self.generateMenu.addAction(self.generateFMToneAction)
        self.generateFMToneAction.triggered.connect(self.onClickGenerateFMTone)
        self.generateNoiseAction = QAction(self.tr('Noise'), self)
        self.generateMenu.addAction(self.generateNoiseAction)
        self.generateNoiseAction.triggered.connect(self.onClickGenerateNoise)
        self.generateSilenceAction = QAction(self.tr('Silence'), self)
        self.generateMenu.addAction(self.generateSilenceAction)
        self.generateSilenceAction.triggered.connect(self.onClickGenerateSilence)
        self.generateSinusoidAction = QAction(self.tr('Sinusoid'), self)
        self.generateMenu.addAction(self.generateSinusoidAction)
        self.generateSinusoidAction.triggered.connect(self.onClickGenerateSinusoid)

        #PLOT MENU
        self.plotMenu = self.menubar.addMenu(self.tr('&Plot'))
        self.plotWaveformAction = QAction(self.tr('Waveform'), self)
        self.plotMenu.addAction(self.plotWaveformAction)
        self.plotWaveformAction.triggered.connect(self.onClickPlotButton)
        #
        self.plotSpectrumAction = QAction(self.tr('Spectrum'), self)
        self.plotMenu.addAction(self.plotSpectrumAction)
        self.plotSpectrumAction.triggered.connect(self.onClickSpectrumButton)
        #
        self.plotSpectrogramAction = QAction(self.tr('Spectrogram'), self)
        self.plotMenu.addAction(self.plotSpectrogramAction)
        self.plotSpectrogramAction.triggered.connect(self.onClickSpectrogramButton)
        #
        self.plotAutocorrelationAction = QAction(self.tr('Autocorrelation'), self)
        self.plotMenu.addAction(self.plotAutocorrelationAction)
        self.plotAutocorrelationAction.triggered.connect(self.onClickAutocorrelationButton)
        #
        self.plotAutocorrelogramAction = QAction(self.tr('Autocorrelogram'), self)
        self.plotMenu.addAction(self.plotAutocorrelogramAction)
        self.plotAutocorrelogramAction.triggered.connect(self.onClickAutocorrelogramButton)

        #HELP MENU
        self.helpMenu = self.menubar.addMenu(self.tr('&Help'))

        self.onShowManualHTMLAction = QAction(self.tr('Manual (html)'), self)
        self.helpMenu.addAction(self.onShowManualHTMLAction)
        self.onShowManualHTMLAction.triggered.connect(onShowManualHTML)

        self.onShowManualPdfAction = QAction(self.tr('Manual (pdf)'), self)
        self.helpMenu.addAction(self.onShowManualPdfAction)
        self.onShowManualPdfAction.triggered.connect(onShowManualPdf)
        
        self.onAboutAction = QAction(self.tr('About pysoundanalyser'), self)
        self.helpMenu.addAction(self.onAboutAction)
        self.onAboutAction.triggered.connect(self.onAbout)

        # create a vertical box layout widget
        vbl = QVBoxLayout()
        self.sndList = {}
     
        #LOAD BUTTON
        loadButton = QPushButton(self.tr("Load Sound"), self)
        loadButton.clicked.connect(self.onClickLoadButton)
        #SAVE BUTTON
        saveButton = QPushButton(self.tr("Save As"), self)
        saveButton.clicked.connect(self.onClickSaveButton)

        #CLONE BUTTON
        cloneButton = QPushButton(self.tr("Clone Sound"), self)
        cloneButton.clicked.connect(self.onClickCloneButton)
        
        #RENAME BUTTON
        renameButton = QPushButton(self.tr("Rename"), self)
        renameButton.clicked.connect(self.onClickRenameButton)
        #REMOVE BUTTON
        removeButton = QPushButton(self.tr("Remove"), self)
        removeButton.clicked.connect(self.onClickRemoveButton)
        #REMOVE ALL
        removeAllButton = QPushButton(self.tr("Remove All"), self)
        removeAllButton.clicked.connect(self.onClickRemoveAllButton)
        #PLAY BUTTON
        playButton = QPushButton(self.tr("Play"), self)
        playButton.clicked.connect(self.onClickPlayButton)
        #SPECTRUM BUTTON
        spectrumButton = QPushButton(self.tr("Spectrum"), self)
        spectrumButton.clicked.connect(self.onClickSpectrumButton)
        #SPECTROGRAM BUTTON
        spectrogramButton = QPushButton(self.tr("Spectrogram"), self)
        spectrogramButton.clicked.connect(self.onClickSpectrogramButton)

        #AUTOCORRELATION BUTTON
        autocorrelationButton = QPushButton(self.tr("Autocorrelation"), self)
        autocorrelationButton.clicked.connect(self.onClickAutocorrelationButton)
        #AUTOCORRELOGRAM BUTTON
        autocorrelogramButton = QPushButton(self.tr("Autocorrelogram"), self)
        autocorrelogramButton.clicked.connect(self.onClickAutocorrelogramButton)
        
        #PLOT BUTTON
        plotButton = QPushButton(self.tr("Plot Waveform"), self)
        plotButton.clicked.connect(self.onClickPlotButton)
        #RESAMPLE BUTTON
        resampleButton = QPushButton(self.tr("Resample"), self)
        resampleButton.clicked.connect(self.onClickResampleButton)

        #SCALE BUTTON
        scaleButton = QPushButton(self.tr("Scale"), self)
        scaleButton.clicked.connect(self.onClickScaleButton)

        #LEVEL DIFF BUTTON
        levelDiffButton = QPushButton(self.tr("Level Difference"), self)
        levelDiffButton.clicked.connect(self.onClickLevelDiffButton)

        #CONCATENATE BUTTON
        concatenateButton = QPushButton(self.tr("Concatenate"), self)
        concatenateButton.clicked.connect(self.onClickConcatenateButton)
        #CUT BUTTON
        cutButton = QPushButton(self.tr("Cut"), self)
        cutButton.clicked.connect(self.onClickCutButton)
        
        #MOVE DOWN BUTTON
        moveDownButton = QPushButton(self.tr("Move Down"), self)
        moveDownButton.clicked.connect(self.onClickMoveDownButton)
        #MOVE UP BUTTON
        moveUpButton = QPushButton(self.tr("Move Up"), self)
        moveUpButton.clicked.connect(self.onClickMoveUpButton)

        self.sndTableWidget = QTableWidget()
        #self.sndTableWidget.setSortingEnabled(True)
        self.sndTableWidget.setColumnCount(3)
        self.sndTableWidget.setSelectionBehavior(QAbstractItemView.SelectionBehavior.SelectRows)
        self.sndTableWidget.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        
        self.sndTableWidget.setHorizontalHeaderLabels([self.tr('Label'), self.tr('Channel'), 'id'])
        self.sndTableWidget.hideColumn(2)
        #self.connect(self.sndTableWidget, QtCore.SIGNAL("itemChanged(QTableWidgetItem*)"), self.tableItemChanged)
        #self.connect(self.sndTableWidget, QtCore.SIGNAL("cellDoubleClicked(int,int)"), self.onCellDoubleClicked)
        self.sndTableWidget.itemChanged.connect(self.tableItemChanged)
        self.sndTableWidget.cellDoubleClicked[int,int].connect(self.onCellDoubleClicked)
        vbl.addWidget(loadButton)
        vbl.addWidget(saveButton)
        vbl.addWidget(cloneButton)
        vbl.addWidget(concatenateButton)
        vbl.addWidget(cutButton)
        vbl.addWidget(playButton)
        vbl.addWidget(plotButton)
        vbl.addWidget(spectrumButton)
        vbl.addWidget(spectrogramButton)
        vbl.addWidget(autocorrelationButton)
        vbl.addWidget(autocorrelogramButton)
        vbl.addWidget(levelDiffButton)
        vbl.addWidget(scaleButton)
        vbl.addWidget(resampleButton)
        vbl.addWidget(renameButton)
        vbl.addWidget(removeButton)
        vbl.addWidget(removeAllButton)
        
        vbl.addStretch(1)

        vbl3 = QVBoxLayout()
        vbl3.addWidget(moveUpButton)
        vbl3.addWidget(moveDownButton)
        self.infoPane = QLabel(self.tr('No Selection                                           '))
        vbl3.addWidget(self.infoPane)
        vbl3.addStretch(1)
        grid = QGridLayout(self.main_widget)
        grid.addLayout(vbl, 1, 1)
        grid.addWidget(self.sndTableWidget,1,2)
        grid.addLayout(vbl3,1,3)
        self.sndTableWidget.itemSelectionChanged.connect(self.onSelectionChanged)
        # set the focus on the main widget
        self.main_widget.setFocus()
        # set the central widget of MainWindow to main_widget
        self.setCentralWidget(self.main_widget)

        if self.prm['calledWithWAVFiles'] == True:
            self.loadFiles(self.prm['WAVFilesToLoad'])
            
    def tableItemChanged(self, item):
        pass
        
    def onEditPref(self):
        dialog = preferencesDialog(self)
        if dialog.exec():
            dialog.permanentApply()
            self.audioManager.initializeAudio()
    def onSelectAll(self):
        for i in range(self.sndTableWidget.rowCount()):
            for j in range(self.sndTableWidget.columnCount()):
                self.sndTableWidget.item(i,j).setSelected(True)
    def swapRow(self, row1, row2):

        lab1 = self.sndTableWidget.takeItem(row1,0)
        lab2 = self.sndTableWidget.takeItem(row2,0)
        chan1 = self.sndTableWidget.takeItem(row1,1)
        chan2 = self.sndTableWidget.takeItem(row2,1)
        id1 = self.sndTableWidget.takeItem(row1,2)
        id2 = self.sndTableWidget.takeItem(row2,2)

        self.sndTableWidget.setItem(row1, 0, lab2)
        self.sndTableWidget.setItem(row2, 0, lab1)
        self.sndTableWidget.setItem(row1, 1, chan2)
        self.sndTableWidget.setItem(row2, 1, chan1)
        self.sndTableWidget.setItem(row1, 2, id2)
        self.sndTableWidget.setItem(row2, 2, id1)

        for j in range(self.sndTableWidget.columnCount()):
            self.sndTableWidget.item(row1, j).setSelected(False)
            self.sndTableWidget.item(row2, j).setSelected(True)

    def onClickMoveDownButton(self):
        lastRow = self.sndTableWidget.rowCount() - 1
        rows = self.findSelectedItemRows()
        if len(rows) > 1:
            QMessageBox.warning(self, self.tr('Warning'), self.tr('Only one sound can be moved at a time'))
        elif len(rows) < 1:
            pass
        else:
            row = rows[0]
            if row == lastRow:
                pass
            else:
                self.swapRow(row, row+1)
                
    def onClickMoveUpButton(self):
        rows = self.findSelectedItemRows()
        if len(rows) > 1:
            QMessageBox.warning(self, self.tr('Warning'), self.tr('Only one sound can be moved at a time'))
        elif len(rows) < 1:
            pass
        else:
            row = rows[0]
            if row == 0:
                pass
            else:
                self.swapRow(row, row-1)        
        
    def onClickLoadButton(self):
        #self.sndTableWidget.setSortingEnabled(False)
        files = QFileDialog.getOpenFileNames(self, self.tr("pysoundanalyser - Choose file to load"), '',self.tr("Supported Sound Files (*.wav);;All Files (*)"))[0]
        self.loadFiles(files)
        
    def loadFiles(self, files):
        for f in range(len(files)):
            sndFile = files[f]
            #xxxxxxxxxxxxxxx
            #Should check here if it is a valid wav file
            foo = True 
            if foo == True:
                
                x,fs,nb = self.loadWav(sndFile)
                thisSnd = {}
                if len(x.shape) > 1:
                    thisSnd['wave'] = x[:,0]
                else:
                    thisSnd['wave'] = x
                thisSnd['fs'] = int(fs)
                thisSnd['nBits'] = nb
                thisSnd['chan'] = self.tr('Left')
                thisSnd['nSamples'] = len(thisSnd['wave'])
                thisSnd['duration'] = thisSnd['nSamples'] / thisSnd['fs']
                tmpName = sndFile
                tmpName = sndFile.split('/')[len(sndFile.split('/'))-1]
                tmpName = tmpName.split('.')[0]
                tmpNameR =  tmpName #+ '-R'#'snd-0-R'
                tmpNameL =  tmpName #+ '-L'#'snd-0-L'
        
                thisSnd['label'] = tmpNameR
                condSat = 0
                while condSat == 0:
                    tmp_id = random_id.random_id(5, 'alphanumeric')
                    if tmp_id in self.sndList:
                        condSat = 0
                    else:
                        condSat = 1
                self.sndList[tmp_id] = copy.copy(thisSnd)
                currCount = len(self.sndList)
                self.sndTableWidget.setRowCount(currCount)
                newItem = QTableWidgetItem(thisSnd['label'])
                newItem.setFlags(QtCore.Qt.ItemFlag.ItemIsSelectable | QtCore.Qt.ItemFlag.ItemIsEnabled)
                self.sndTableWidget.setItem(currCount-1, 0, newItem)
                newItem = QTableWidgetItem(thisSnd['chan'])
                newItem.setFlags(QtCore.Qt.ItemFlag.ItemIsSelectable | QtCore.Qt.ItemFlag.ItemIsEnabled)
                self.sndTableWidget.setItem(currCount-1, 1, newItem)
                self.sndList[tmp_id]['qid'] = QTableWidgetItem(tmp_id)
                self.sndTableWidget.setItem(currCount-1, 2, self.sndList[tmp_id]['qid'])
                
        
                if len(x.shape) > 1:
                    nChans = x.shape[1]
                    for nsnd in range(1, nChans):
                        thisSnd = {}
                        thisSnd['wave'] = x[:,nsnd]
                        thisSnd['fs'] = int(fs)
                        thisSnd['nBits'] = nb
                        thisSnd['chan'] = self.tr('Right')
                        thisSnd['nSamples'] = len(thisSnd['wave'])
                        thisSnd['duration'] = thisSnd['nSamples'] / thisSnd['fs']
                        thisSnd['label'] = tmpNameL
                        condSat = 0
                        while condSat == 0:
                            tmp_id = random_id.random_id(5, 'alphanumeric')
                            if tmp_id in self.sndList:
                                condSat = 0
                            else:
                                condSat = 1
                        self.sndList[tmp_id] = copy.copy(thisSnd)
                        currCount = len(self.sndList)
                        self.sndTableWidget.setRowCount(currCount)
                        newItem = QTableWidgetItem(thisSnd['label'])
                        newItem.setFlags(QtCore.Qt.ItemFlag.ItemIsSelectable | QtCore.Qt.ItemFlag.ItemIsEnabled)
                        self.sndTableWidget.setItem(currCount-1, 0, newItem)
                        newItem = QTableWidgetItem(thisSnd['chan'])
                        newItem.setFlags(QtCore.Qt.ItemFlag.ItemIsSelectable | QtCore.Qt.ItemFlag.ItemIsEnabled)
                        self.sndTableWidget.setItem(currCount-1, 1, newItem)
                        self.sndList[tmp_id]['qid'] = QTableWidgetItem(tmp_id)
                        self.sndTableWidget.setItem(currCount-1, 2, self.sndList[tmp_id]['qid'])

       
                
            else:
                pass
        selItems = self.sndTableWidget.selectedItems()
        #self.sndTableWidget.setSortingEnabled(True)
        
    def loadFileValid(self, sndFile):
        #xxxxxxxxxxxxxxx
        # need to update this function
        if len(sndFile) == 0:
            fileValid = False
            msg = None
        else:
            try:
                fileToRead = Sndfile(str(sndFile), 'r')
                fileValid = True
                fileToRead.close()
            except IOError:
                msg = self.tr("Cannot open %1 IOError").arg(sndFile) #'Cannot open' + sndFile + '\n IOError'
                fileValid = False
        #else:
        #    fileValid = False
        #    msg = 'cannot open' + sndFile + ' only wav supported at the moment'
        if fileValid == False and msg != None:
            QMessageBox.warning(self, self.tr('Warning'), msg)

        return fileValid
    
    def loadWav(self,fName):
        snd, fs, nbits = wavread(fName)

        return snd, fs, nbits
    
    def onSelectionChanged(self):
        ids = self.findSelectedItemIds()
        if len(ids) == 0:
            self.infoPane.setText(self.tr('No Selection'))
        elif len(ids) == 2:
            snd1 = self.sndList[ids[0]]
            snd2 = self.sndList[ids[1]]
            rms1 = sndlib.getRMS(snd1['wave'], channel=0)
            rms2 = sndlib.getRMS(snd2['wave'], channel=0)
            dbDiff = 20*log10(rms1/rms2)
            if dbDiff >= 0:
                w = '+'
            elif dbDiff < 0:
                w = ''
            self.infoPane.setText(self.tr("{0} is \n {1} {2} dB than \n {3}").format(snd1['label'], w, self.currLocale.toString(dbDiff), snd2['label']))
        elif len(ids) > 2:
            self.infoPane.setText(self.tr('Multiple Selection'))
        else:
            selectedSound = ids[0]
            dur = round(self.sndList[selectedSound]['duration'], 3)
            chan = self.sndList[selectedSound]['chan']
            fs = int(self.sndList[selectedSound]['fs'])
            if 'nBits' in self.sndList[selectedSound]:
                nb = self.currLocale.toString(int(self.sndList[selectedSound]['nBits']))
            else:
                nb = 'Undefined'
            nSamp = self.sndList[selectedSound]['nSamples']

            allInfo = self.tr("Duration: {0} sec.\n\nChannel: {1} \n\nSamp. Freq.: {2} \n\nBits: {3}" ).format(dur, chan, self.currLocale.toString(fs), nb) 
            self.infoPane.setText(allInfo)
            
    def findSelectedItemIds(self):
        selItems = self.sndTableWidget.selectedItems()
        selItemsRows = []
        for i in range(len(selItems)):
            selItemsRows.append(selItems[i].row())
        selItemsRows = unique(selItemsRows)
        selItemsIds = []
        for i in range(len(selItemsRows)):
            selItemsIds.append(str(self.sndTableWidget.item(selItemsRows[i], 2).text()))
        return selItemsIds
    
    def findSelectedItemRows(self):
        selItems = self.sndTableWidget.selectedItems()
        selItemsRows = []
        for i in range(len(selItems)):
            selItemsRows.append(selItems[i].row())
        selItemsRows = unique(selItemsRows)
        return selItemsRows
    
    def onCellDoubleClicked(self, row, col):
        if col == 0:
            self.onClickRenameButton()
        elif col == 1:
            self.onDoubleClickChannelCell()

    def onClickSaveButton(self):
        ids = self.findSelectedItemIds()
        if len(ids)<1:
            QMessageBox.warning(self, self.tr('Warning'), self.tr('No sound selected.'))
            return
        sampRate = self.sndList[ids[0]]['fs']
        condition = True
        nSampList = []
        for i in range(len(ids)):
            selectedSound = ids[i]
            if self.sndList[selectedSound]['fs'] != sampRate:
                QMessageBox.warning(self, self.tr('Warning'), self.tr('Cannot write sounds with different sample rates'))
                condition = False
                break
         
            nSampList.append(self.sndList[selectedSound]['nSamples'])
        if condition == True:
            snd = zeros((max(nSampList), 2))
            for i in range(len(ids)):
                selectedSound = ids[i]
                nSampDiff = max(nSampList) - len(self.sndList[selectedSound]['wave'])
                if self.sndList[selectedSound]['chan'] == self.tr('Right'):
                    snd[:,1] =  snd[:,1] + concatenate((self.sndList[selectedSound]['wave'], zeros(nSampDiff)), axis=0)
                elif self.sndList[selectedSound]['chan'] == self.tr('Left'):
                    snd[:,0] =  snd[:,0] + concatenate((self.sndList[selectedSound]['wave'], zeros(nSampDiff)), axis=0)
       
        dialog = saveSoundDialog(self)
        if dialog.exec():
            fs = sampRate
            if dialog.channelChooser.currentText() == self.tr('Mono'):
                wave = snd[:,0] + snd[:,1]
                nChannels = 1
            else:
                wave = snd
                nChannels = 2
            ftow = QFileDialog.getSaveFileName(self, self.tr('Choose file to write'), self.tr('.{0}').format(dialog.suggestedExtension), self.tr('All Files (*)'))[0]
            if len(ftow) > 0:

                wavwrite(wave, fs, int(dialog.encodingChooser.currentText()), ftow)              
    
    def onClickCloneButton(self):
        #self.sndTableWidget.setSortingEnabled(False)
        ids = self.findSelectedItemIds()
        if len(ids)<1:
            QMessageBox.warning(self, self.tr('Warning'), self.tr('No sound selected.'))
            return
        for i in range(len(ids)):
            selectedSound = ids[i]
            thisSnd = copy.copy(self.sndList[selectedSound])
            thisSnd['label'] = self.sndList[selectedSound]['label'] + ' (copy)'
            condSat = 0
            while condSat == 0:
                tmp_id = random_id.random_id(5, 'alphanumeric')
                if tmp_id in self.sndList:
                    condSat = 0
                else:
                    condSat = 1
            self.sndList[tmp_id] = thisSnd
            currCount = len(self.sndList)
            self.sndTableWidget.setRowCount(currCount)
            newItem = QTableWidgetItem(thisSnd['label'])
            #newItem.setFlags(QtCore.Qt.ItemFlag.ItemIsSelectable | QtCore.Qt.ItemFlag.ItemIsEnabled)
            self.sndTableWidget.setItem(currCount-1, 0, newItem)
            newItem = QTableWidgetItem(thisSnd['chan'])
            #newItem.setFlags(QtCore.Qt.ItemFlag.ItemIsSelectable | QtCore.Qt.ItemFlag.ItemIsEnabled)
            self.sndTableWidget.setItem(currCount-1, 1, newItem)
            self.sndList[tmp_id]['qid'] = QTableWidgetItem(tmp_id)
            self.sndTableWidget.setItem(currCount-1, 2, self.sndList[tmp_id]['qid'])
            #self.sndTableWidget.setSortingEnabled(True)
            
    def onClickPlotButton(self):
        ids = self.findSelectedItemIds()
        if len(ids)<1:
            QMessageBox.warning(self, self.tr('Warning'), self.tr('No sound selected.'))
            return
        for i in range(len(ids)):
           selectedSound = ids[i]
           waveformPlot(self, self.sndList[selectedSound], self.prm)
           #self.waveformPlotter.plotWaveformThreaded(self.sndList[selectedSound], self.prm)
           
    def onClickSpectrumButton(self):
       ids = self.findSelectedItemIds()
       if len(ids)<1:
           QMessageBox.warning(self, self.tr('Warning'), self.tr('No sound selected.'))
           return
       for i in range(len(ids)):
           selectedSound = ids[i]
           spectrumPlot(self, self.sndList[selectedSound], self.prm)
           
    def onClickAutocorrelationButton(self):
       ids = self.findSelectedItemIds()
       if len(ids)<1:
           QMessageBox.warning(self, self.tr('Warning'), self.tr('No sound selected.'))
           return
       for i in range(len(ids)):
           selectedSound = ids[i]
           acfPlot(self, self.sndList[selectedSound], self.prm)
           
    def onClickAutocorrelogramButton(self):
       ids = self.findSelectedItemIds()
       if len(ids)<1:
           QMessageBox.warning(self, self.tr('Warning'), self.tr('No sound selected.'))
           return
       for i in range(len(ids)):
           selectedSound = ids[i]
           autocorrelogramPlot(self, self.sndList[selectedSound], self.prm)
           
    def onClickSpectrogramButton(self):
       ids = self.findSelectedItemIds()
       if len(ids)<1:
           QMessageBox.warning(self, self.tr('Warning'), self.tr('No sound selected.'))
           return
       for i in range(len(ids)):
           selectedSound = ids[i]
           spectrogramPlot(self, self.sndList[selectedSound], self.prm)
           
    def onClickRenameButton(self):
        ids = self.findSelectedItemIds()
        if len(ids) > 1:
            QMessageBox.warning(self, self.tr('Warning'), self.tr('Only one sound can be renamed at a time'))
        elif len(ids) < 1:
            QMessageBox.warning(self, self.tr('Warning'), self.tr('No sound selected.'))
            return
        else:
            selectedSound = ids[0]
            msg = self.tr('New name:')
            text, ok = QInputDialog.getText(self, self.tr('Input Dialog'), msg)
            if ok:
                    self.sndTableWidget.item(self.sndList[selectedSound]['qid'].row(), 0).setText(text)
                    self.sndList[selectedSound]['label'] = text

    def onDoubleClickChannelCell(self):
        ids = self.findSelectedItemIds()
        if len(ids) > 1:
            QMessageBox.warning(self, self.tr('Warning'), self.tr('Only sound can be changed at a time'))
        else:
            selectedSound = ids[0]
            multipleSelection = False
            currChan = self.sndList[selectedSound]['chan']
            dialog = changeChannelDialog(self, multipleSelection, currChan)
            if dialog.exec():
                newChan = dialog.chooser.currentText()
                self.sndTableWidget.item(self.sndList[selectedSound]['qid'].row(), 1).setText(newChan)
                self.sndList[selectedSound]['chan'] = newChan
          
    def onClickLevelDiffButton(self):
        ids = self.findSelectedItemIds()
        if len(ids)<2:
            QMessageBox.warning(self, self.tr('Warning'), self.tr('No sound selected.'))
            return
        if len(ids) > 2:
            QMessageBox.warning(self, self.tr('Level Difference'), self.tr('Only two sounds can be compared at a time'))
        else:
            snd1 = self.sndList[ids[0]]
            snd2 = self.sndList[ids[1]]
            rms1 = sndlib.getRMS(snd1['wave'], channel=0)
            rms2 = sndlib.getRMS(snd2['wave'], channel=0)
            dbDiff = 20*log10(rms1/rms2)
            if dbDiff >= 0:
                w = '+'
            elif dbDiff < 0:
                w = ''

            QMessageBox.information(self, self.tr('Level Difference'), self.tr('{0} is {1} {2} dB than {3}').format(snd1['label'], w, self.currLocale.toString(dbDiff), snd2['label']))

    def onClickScaleButton(self):
        ids = self.findSelectedItemIds()
        if len(ids)<1:
            QMessageBox.warning(self, self.tr('Warning'), self.tr('No sound selected.'))
            return
        val, ok = QInputDialog.getDouble(self, self.tr('Scale Level'), self.tr('Add or subtract decibels'))
        if ok:
            for i in range(len(ids)):
                selectedSound = ids[i]
                self.sndList[selectedSound]['wave'] = sndlib.scale(val, self.sndList[selectedSound]['wave'])
       
    def onClickRemoveButton(self):
        ids = self.findSelectedItemIds()
        if len(ids)<1:
            QMessageBox.warning(self, self.tr('Warning'), self.tr('No sound selected.'))
            return
        for i in range(len(ids)):
            selectedSound = ids[i]
            self.sndTableWidget.removeRow(self.sndList[selectedSound]['qid'].row())
            del self.sndList[selectedSound]

    def onClickRemoveAllButton(self):
        ks = list(self.sndList.keys())
        for i in range(len(ks)):
            self.sndTableWidget.removeRow(self.sndList[ks[i]]['qid'].row())
            del self.sndList[ks[i]]
 

    def onClickGetRMSButton(self):
        ids = self.findSelectedItemIds()
        if len(ids)<1:
            QMessageBox.warning(self, self.tr('Warning'), self.tr('No sound selected.'))
            return
        rmsVals = []
        msg = self.tr('')
        for i in range(len(ids)):
            selectedSound = ids[i]
            rmsVals.append(sndlib.getRMS(self.sndList[selectedSound]['wave'], channel=0))
            msg = self.tr('{0} {1} : {2} \n').format(msg, self.sndList[selectedSound]['label'], self.currLocale.toString(rmsVals[i])) 
        QMessageBox.information(self, self.tr('Root Mean Square'), msg)
                     
    def onClickPlayButton(self):
        ids = self.findSelectedItemIds()
        if len(ids)<1:
            QMessageBox.warning(self, self.tr('Warning'), self.tr('No sound selected.'))
            return
        sampRate = self.sndList[ids[0]]['fs']
        condition = True
        nSampList = []
        for i in range(len(ids)):
            selectedSound = ids[i]
            if self.sndList[selectedSound]['fs'] != sampRate:
                QMessageBox.warning(self, self.tr('Warning'), self.tr('Cannot play sounds with different sample rates'))
                condition = False
                break
            nSampList.append(self.sndList[selectedSound]['nSamples'])
        if condition == True:
            snd = zeros((max(nSampList), 2))
            for i in range(len(ids)):
                selectedSound = ids[i]
                nSampDiff = max(nSampList) - len(self.sndList[selectedSound]['wave'])
                if self.sndList[selectedSound]['chan'] == self.tr('Right'):
                    snd[:,1] =  snd[:,1] + concatenate((self.sndList[selectedSound]['wave'], zeros(nSampDiff)), axis=0)
                elif self.sndList[selectedSound]['chan'] == self.tr('Left'):
                    snd[:,0] =  snd[:,0] + concatenate((self.sndList[selectedSound]['wave'], zeros(nSampDiff)), axis=0)

        
        wave = snd
        #fs = sampRate
        #playCmd = str(self.prm['pref']['sound']['playCommand'])
        #self.playSound(wave, fs, nbits, playCmd, False, 'temp')
        nbits = int(self.prm['pref']['sound']['nBits'])
        self.audioManager.playSound(wave, sampRate, nbits, False, 'temp.wav')

    # def playSound(self, snd, fs, nbits, playCmd, writewav, fname):
    #     playCmd = str(playCmd)
    #     enc = 'pcm'+ str(nbits)
    #     if writewav == True:
    #         fname = fname
    #     else:
    #         if platform.system() == 'Windows':
    #             fname = 'tmp_snd.wav'
    #         else:
    #             (hnl, fname) = mkstemp('tmp_snd.wav')

    #     wavwrite(snd, fs, nbits, fname)
    #     if playCmd == 'winsound':
    #         winsound.PlaySound(fname, winsound.SND_FILENAME)
    #     else:
    #         cmd = playCmd + ' ' + fname
    #         os.system(cmd)
    #     if writewav == False:
    #         os.remove(fname)
    
    #     return
            
    def onClickResampleButton(self):
        ids = self.findSelectedItemIds()
        if len(ids)<1:
            QMessageBox.warning(self, self.tr('Warning'), self.tr('No sound selected.'))
            return
        else:
            if len(ids) == 1:
                multipleSelection = False
                currSampRate = self.sndList[ids[0]]['fs']
            elif len(ids) > 1:
                multipleSelection = True
                currSampRate = None

            dialog = resampleDialog(self, multipleSelection, currSampRate)
            if dialog.exec():
                newSampRate = dialog.newSampRate
                resampMethod = str(dialog.convertorChooser.currentText())
                smoothWindow = str(dialog.winChooser.currentText())
                if smoothWindow == self.tr('none'):
                    smoothWindow = None
                for i in range(len(ids)):
                    selectedSound = ids[i]
                    if smoothWindow == "hanning":
                        smoothWindow = "hann"
                    self.sndList[selectedSound]['wave'] = scipy.signal.resample(self.sndList[selectedSound]['wave'],
                                                                                int(round(len(self.sndList[selectedSound]['wave'])*newSampRate/self.sndList[selectedSound]['fs'])),
                                                                                window=smoothWindow) 
                    self.sndList[selectedSound]['fs'] = newSampRate
                    self.sndList[selectedSound]['nSamples'] = len(self.sndList[selectedSound]['wave'])
                    self.onSelectionChanged()

    def onClickConcatenateButton(self):
        ids = self.findSelectedItemIds()
        if len(ids)<2:
            QMessageBox.warning(self, self.tr('Warning'), self.tr('No sounds selected.'))
            return
        elif len(ids) > 2:
            QMessageBox.warning(self, self.tr('Concatenate Sounds'), self.tr('Only two sounds can be concatenated at a time'))
        else:
            snd1 = self.sndList[ids[0]]
            snd2 = self.sndList[ids[1]]

            if snd1['fs'] != snd2['fs']:
                QMessageBox.warning(self, self.tr('Concatenate Sounds'), self.tr('Cannot concatenate sounds with different sampling rates'))
            else:
                sampRate = snd1['fs']
                dialog = concatenateDialog(self, snd1, snd2)
                if dialog.exec():
                     delay = self.currLocale.toDouble(dialog.delayWidget.text())[0]
                     delayType = str(dialog.delayTypeChooser.currentText())
                     thisSnd = {}
                     if dialog.order == 'given':
                         thisSnd['wave'] = concatenateSounds(snd1['wave'], snd2['wave'], delay, delayType, sampRate)
                     else:
                         thisSnd['wave'] = concatenateSounds(snd2['wave'], snd1['wave'], delay, delayType, sampRate)

                     thisSnd['label'] = str(dialog.outNameWidget.text())#snd1['label'] + '-' + snd2['label']
                     thisSnd['chan'] = str(dialog.outChanChooser.currentText())
                     thisSnd['nSamples'] = len(thisSnd['wave'])
                     thisSnd['fs'] = sampRate
                     thisSnd['duration'] = thisSnd['nSamples'] / thisSnd['fs']
                     thisSnd['nBits'] = 0
                     thisSnd['format'] = ''
                     condSat = 0
                     while condSat == 0:
                         tmp_id = random_id.random_id(5, 'alphanumeric')
                         if tmp_id in self.sndList:
                             condSat = 0
                         else:
                             condSat = 1
                     self.sndList[tmp_id] = thisSnd
                     currCount = len(self.sndList)
                     self.sndTableWidget.setRowCount(currCount)
                     newItem = QTableWidgetItem(thisSnd['label'])
                     
                     self.sndTableWidget.setItem(currCount-1, 0, newItem)
                     newItem = QTableWidgetItem(thisSnd['chan'])
                     
                     self.sndTableWidget.setItem(currCount-1, 1, newItem)
                     self.sndList[tmp_id]['qid'] = QTableWidgetItem(tmp_id)
                     self.sndTableWidget.setItem(currCount-1, 2, self.sndList[tmp_id]['qid'])
                     
    def onClickCutButton(self):
        ids = self.findSelectedItemIds()
        if len(ids)<1:
            QMessageBox.warning(self, self.tr('Warning'), self.tr('No sound selected.'))
            return
        for i in range(len(ids)):
            snd = self.sndList[ids[i]]
            fs = snd["fs"]
            nSamples = snd["wave"].shape[0]
            dialog = cutDialog(self, snd)
            if dialog.exec():
                startCut = self.currLocale.toDouble(dialog.fromWidget.text())[0]
                endCut = self.currLocale.toDouble(dialog.toWidget.text())[0]
                cutUnit = str(dialog.unitChooser.currentText())
                if cutUnit == "Seconds":
                    startCut = int(round(startCut*fs))
                    endCut = int(round(endCut*fs))
                elif cutUnit == "Milliseconds":
                    startCut = int(round(startCut/1000*fs))
                    endCut = int(round(endCut/1000*fs))

                if startCut < 0 or endCut > nSamples:
                    QMessageBox.warning(self, self.tr('Cut Sound'), self.tr('Values out of range'))
                elif startCut == 0 and endCut == nSamples:
                    QMessageBox.warning(self, self.tr('Cut Sound'), self.tr('Cannot cut entire sound, please use remove button'))
                else:
                    snd["wave"] = cutSampleRegion(snd["wave"], startCut, endCut)
                    snd['nSamples'] = len(snd['wave'])
                    snd['duration'] = snd['nSamples'] / snd['fs']
                    self.onSelectionChanged()

    def onClickApplyFIR2PresetsButton(self):
        ids = self.findSelectedItemIds()
        if len(ids) < 1:
            QMessageBox.warning(self, self.tr('Warning'), self.tr('No sound selected.'))
            return
        else:
            dialog = applyFIR2PresetsDialog(self)
            if dialog.exec():
                if dialog.currFilterType == self.tr('lowpass'):
                    cutoff = self.currLocale.toDouble(dialog.cutoffWidget.text())[0]
                    highStop = self.currLocale.toDouble(dialog.endCutoffWidget.text())[0]
                    for i in range(len(ids)):
                        selectedSound = ids[i]
                        filterOrder = self.currLocale.toInt(dialog.filterOrderWidget.text())[0]
                        self.sndList[selectedSound]['wave'] = fir2FiltAlt(0, 0, cutoff, cutoff*highStop, 'lowpass', self.sndList[selectedSound]['wave'], self.sndList[selectedSound]['fs'], filterOrder)
                elif dialog.currFilterType == self.tr('highpass'):
                    cutoff = self.currLocale.toDouble(dialog.cutoffWidget.text())[0]
                    lowStop = self.currLocale.toDouble(dialog.startCutoffWidget.text())[0]
                    for i in range(len(ids)):
                        selectedSound = ids[i]
                        filterOrder = self.currLocale.toInt(dialog.filterOrderWidget.text())[0]
                        self.sndList[selectedSound]['wave'] = fir2FiltAlt(cutoff*lowStop, cutoff, 0, 0, 'highpass', self.sndList[selectedSound]['wave'], self.sndList[selectedSound]['fs'], filterOrder)
                elif dialog.currFilterType == self.tr('bandpass'):
                    lowerCutoff = self.currLocale.toDouble(dialog.lowerCutoffWidget.text())[0]
                    lowStop = self.currLocale.toDouble(dialog.startCutoffWidget.text())[0]
                    higherCutoff = self.currLocale.toDouble(dialog.higherCutoffWidget.text())[0]
                    highStop = self.currLocale.toDouble(dialog.endCutoffWidget.text())[0]
                    for i in range(len(ids)):
                        selectedSound = ids[i]
                        filterOrder = self.currLocale.toInt(dialog.filterOrderWidget.text())[0]
                        self.sndList[selectedSound]['wave'] = fir2FiltAlt(lowerCutoff*lowStop, lowerCutoff, higherCutoff, higherCutoff*highStop, 'bandpass', self.sndList[selectedSound]['wave'], self.sndList[selectedSound]['fs'], filterOrder)
                elif dialog.currFilterType == self.tr('bandstop'):
                    lowerCutoff = self.currLocale.toDouble(dialog.lowerCutoffWidget.text())[0]
                    highStop = self.currLocale.toDouble(dialog.endCutoffWidget.text())[0]
                    higherCutoff = self.currLocale.toDouble(dialog.higherCutoffWidget.text())[0]
                    lowStop = self.currLocale.toDouble(dialog.startCutoffWidget.text())[0]
                    for i in range(len(ids)):
                        selectedSound = ids[i]
                        filterOrder = self.currLocale.toInt(dialog.filterOrderWidget.text())[0]
                        self.sndList[selectedSound]['wave'] = fir2FiltAlt(lowerCutoff, lowerCutoff*highStop, higherCutoff*lowStop, higherCutoff, 'bandstop', self.sndList[selectedSound]['wave'], self.sndList[selectedSound]['fs'], filterOrder)

    def onClickGenerateNoise(self):
        dialog = generateNoiseDialog(self)
        if dialog.exec():
            label = dialog.noiseLabelWidget.text()
            duration = self.currLocale.toDouble(dialog.noiseDurationWidget.text())[0]
            ramps = self.currLocale.toDouble(dialog.noiseRampsWidget.text())[0]
            spectrumLevel = self.currLocale.toDouble(dialog.noiseLevelWidget.text())[0]
            fs = self.currLocale.toInt(dialog.sampRateWidget.text())[0]
            ear = dialog.noiseEarChooser.currentText()
            if ear == self.tr('Right'):
                ear = 'Right'
            elif ear == self.tr('Left'):
                ear = 'Left'
            elif ear == self.tr('Both'):
                ear = 'Both'
            if dialog.currNoiseType == self.tr('White'):
                thisNoise = sndlib.broadbandNoise(spectrumLevel, duration, ramps, ear, fs, self.prm['pref']['sound']['maxLevel'])
            elif dialog.currNoiseType == self.tr('Pink'):
                refHz = self.currLocale.toDouble(dialog.reWidget.text())[0]
                thisNoise = sndlib.broadbandNoise(spectrumLevel, duration, ramps, ear, fs, self.prm['pref']['sound']['maxLevel'])
                thisNoise = sndlib.makePinkRef(thisNoise, fs, refHz)
            elif dialog.currNoiseType == self.tr('Red'):
                refHz = self.currLocale.toDouble(dialog.reWidget.text())[0]
                thisNoise = sndlib.broadbandNoise(spectrumLevel, duration, ramps, ear, fs, self.prm['pref']['sound']['maxLevel'])
                thisNoise = sndlib.makeRedRef(thisNoise, fs, refHz)
            elif dialog.currNoiseType == self.tr('Blue'):
                refHz = self.currLocale.toDouble(dialog.reWidget.text())[0]
                thisNoise = sndlib.broadbandNoise(spectrumLevel, duration, ramps, ear, fs, self.prm['pref']['sound']['maxLevel'])
                thisNoise = sndlib.makeBlueRef(thisNoise, fs, refHz)
            elif dialog.currNoiseType == self.tr('Violet'):
                refHz = self.currLocale.toDouble(dialog.reWidget.text())[0]
                thisNoise = sndlib.broadbandNoise(spectrumLevel, duration, ramps, ear, fs, self.prm['pref']['sound']['maxLevel'])
                thisNoise = sndlib.makeVioletRef(thisNoise, fs, refHz)



            if ear == 'Right' or ear == 'Left':
                thisSnd = {}
                if ear == 'Right':
                    thisSnd['wave'] = thisNoise[:,1]
                elif ear == 'Left':
                    thisSnd['wave'] = thisNoise[:,0]
                thisSnd['fs'] = fs
                thisSnd['nBits'] = 0
                thisSnd['chan'] = dialog.noiseEarChooser.currentText()
                thisSnd['nSamples'] = len(thisSnd['wave'])
                thisSnd['duration'] = thisSnd['nSamples'] / float(thisSnd['fs'])
                thisSnd['label'] = label
                condSat = 0
                while condSat == 0:
                    tmp_id = random_id.random_id(5, 'alphanumeric')
                    if tmp_id in self.sndList:
                        condSat = 0
                    else:
                        condSat = 1
                self.sndList[tmp_id] = copy.copy(thisSnd)
                currCount = len(self.sndList)
                self.sndTableWidget.setRowCount(currCount)
                newItem = QTableWidgetItem(thisSnd['label'])
                newItem.setFlags(QtCore.Qt.ItemFlag.ItemIsSelectable | QtCore.Qt.ItemFlag.ItemIsEnabled)
                self.sndTableWidget.setItem(currCount-1, 0, newItem)
                newItem = QTableWidgetItem(thisSnd['chan'])
                newItem.setFlags(QtCore.Qt.ItemFlag.ItemIsSelectable | QtCore.Qt.ItemFlag.ItemIsEnabled)
                self.sndTableWidget.setItem(currCount-1, 1, newItem)
                self.sndList[tmp_id]['qid'] = QTableWidgetItem(tmp_id)
                self.sndTableWidget.setItem(currCount-1, 2, self.sndList[tmp_id]['qid'])

            if ear == 'Both':
                for i in range(2):
                    thisSnd = {}
                    if i == 1:
                        thisSnd['wave'] = thisNoise[:,1]
                        thisSnd['chan'] = self.tr('Right')
                    else:
                        thisSnd['wave'] = thisNoise[:,0]
                        thisSnd['chan'] = self.tr('Left')
                    thisSnd['fs'] = fs
                    thisSnd['nBits'] = 0
                    thisSnd['nSamples'] = len(thisSnd['wave'])
                    thisSnd['duration'] = thisSnd['nSamples'] / float(thisSnd['fs'])
                    thisSnd['label'] = label
                    condSat = 0
                    while condSat == 0:
                        tmp_id = random_id.random_id(5, 'alphanumeric')
                        if tmp_id in self.sndList:
                            condSat = 0
                        else:
                            condSat = 1
                    self.sndList[tmp_id] = copy.copy(thisSnd)
                    currCount = len(self.sndList)
                    self.sndTableWidget.setRowCount(currCount)
                    newItem = QTableWidgetItem(thisSnd['label'])
                    newItem.setFlags(QtCore.Qt.ItemFlag.ItemIsSelectable | QtCore.Qt.ItemFlag.ItemIsEnabled)
                    self.sndTableWidget.setItem(currCount-1, 0, newItem)
                    newItem = QTableWidgetItem(thisSnd['chan'])
                    newItem.setFlags(QtCore.Qt.ItemFlag.ItemIsSelectable | QtCore.Qt.ItemFlag.ItemIsEnabled)
                    self.sndTableWidget.setItem(currCount-1, 1, newItem)
                    self.sndList[tmp_id]['qid'] = QTableWidgetItem(tmp_id)
                    self.sndTableWidget.setItem(currCount-1, 2, self.sndList[tmp_id]['qid'])
           
    def onClickGenerateSinusoid(self):
        dialog = generateSinusoidDialog(self)
        if dialog.exec():
            label = dialog.soundLabelWidget.text()
            freq = self.currLocale.toDouble(dialog.soundFrequencyWidget.text())[0]
            phase = self.currLocale.toDouble(dialog.soundPhaseWidget.text())[0]
            duration = self.currLocale.toDouble(dialog.soundDurationWidget.text())[0]
            ramps = self.currLocale.toDouble(dialog.soundRampsWidget.text())[0]
            level = self.currLocale.toDouble(dialog.soundLevelWidget.text())[0]
            fs = self.currLocale.toInt(dialog.sampRateWidget.text())[0]
            ear = dialog.soundEarChooser.currentText()
            if ear == self.tr('Right'):
                ear = 'Right'
            elif ear == self.tr('Left'):
                ear = 'Left'
            elif ear == self.tr('Both'):
                ear = 'Both'

            if ear == 'Both':
                itd = self.currLocale.toDouble(dialog.itdWidget.text())[0]
                itdRef = dialog.itdRefChooser.currentText()
                ild = self.currLocale.toDouble(dialog.ildWidget.text())[0]
                ildRef = dialog.ildRefChooser.currentText()
            else:
                itd = 0
                itdRef = None
                ild = 0
                ildRef = None
          
            thisSound = sndlib.binauralPureTone(freq, phase, level, duration, ramps, ear, itd, itdRef, ild, ildRef, fs, self.prm['pref']['sound']['maxLevel'])
          

            if ear == 'Right' or ear == 'Left':
                thisSnd = {}
                if ear == 'Right':
                    thisSnd['wave'] = thisSound[:,1]
                elif ear == 'Left':
                    thisSnd['wave'] = thisSound[:,0]
                thisSnd['fs'] = fs
                #thisSnd['nBits'] = 0
                thisSnd['chan'] = dialog.soundEarChooser.currentText()
                thisSnd['nSamples'] = len(thisSnd['wave'])
                thisSnd['duration'] = thisSnd['nSamples'] / thisSnd['fs']
                thisSnd['label'] = label
                condSat = 0
                while condSat == 0:
                    tmp_id = random_id.random_id(5, 'alphanumeric')
                    if tmp_id in self.sndList:
                        condSat = 0
                    else:
                        condSat = 1
                self.sndList[tmp_id] = copy.copy(thisSnd)
                currCount = len(self.sndList)
                self.sndTableWidget.setRowCount(currCount)
                newItem = QTableWidgetItem(thisSnd['label'])
                newItem.setFlags(QtCore.Qt.ItemFlag.ItemIsSelectable | QtCore.Qt.ItemFlag.ItemIsEnabled)
                self.sndTableWidget.setItem(currCount-1, 0, newItem)
                newItem = QTableWidgetItem(thisSnd['chan'])
                newItem.setFlags(QtCore.Qt.ItemFlag.ItemIsSelectable | QtCore.Qt.ItemFlag.ItemIsEnabled)
                self.sndTableWidget.setItem(currCount-1, 1, newItem)
                self.sndList[tmp_id]['qid'] = QTableWidgetItem(tmp_id)
                self.sndTableWidget.setItem(currCount-1, 2, self.sndList[tmp_id]['qid'])

            if ear == 'Both':
                for i in range(2):
                    thisSnd = {}
                    if i == 0:
                        thisSnd['wave'] = thisSound[:,1]
                        thisSnd['chan'] = self.tr('Right')
                    else:
                        thisSnd['wave'] = thisSound[:,0]
                        thisSnd['chan'] = self.tr('Left')
                    thisSnd['fs'] = fs
                    thisSnd['nSamples'] = len(thisSnd['wave'])
                    thisSnd['duration'] = thisSnd['nSamples'] / thisSnd['fs']
                    thisSnd['label'] = label
                    condSat = 0
                    while condSat == 0:
                        tmp_id = random_id.random_id(5, 'alphanumeric')
                        if tmp_id in self.sndList:
                            condSat = 0
                        else:
                            condSat = 1
                    self.sndList[tmp_id] = copy.copy(thisSnd)
                    currCount = len(self.sndList)
                    self.sndTableWidget.setRowCount(currCount)
                    newItem = QTableWidgetItem(thisSnd['label'])
                    newItem.setFlags(QtCore.Qt.ItemFlag.ItemIsSelectable | QtCore.Qt.ItemFlag.ItemIsEnabled)
                    self.sndTableWidget.setItem(currCount-1, 0, newItem)
                    newItem = QTableWidgetItem(thisSnd['chan'])
                    newItem.setFlags(QtCore.Qt.ItemFlag.ItemIsSelectable | QtCore.Qt.ItemFlag.ItemIsEnabled)
                    self.sndTableWidget.setItem(currCount-1, 1, newItem)
                    self.sndList[tmp_id]['qid'] = QTableWidgetItem(tmp_id)
                    self.sndTableWidget.setItem(currCount-1, 2, self.sndList[tmp_id]['qid'])

    def onClickGenerateHarmCompl(self):
        dialog = generateSoundDialog(self, "Harmonic Complex")
        if dialog.exec():

            for i in range(dialog.sndPrm['nFields']):
                dialog.sndPrm['field'][i] = self.currLocale.toDouble(dialog.field[i].text())[0]
            for i in range(dialog.sndPrm['nChoosers']):
                dialog.sndPrm['chooser'][i] = dialog.chooser[i].currentText()
            
            label = dialog.soundLabelWidget.text()
            fs = self.currLocale.toInt(dialog.sampRateWidget.text())[0]
            F0                  = dialog.sndPrm['field'][dialog.sndPrm['fieldLabel'].index(dialog.tr("F0 (Hz)"))]
            bandwidth           = dialog.sndPrm['field'][dialog.sndPrm['fieldLabel'].index(dialog.tr("Bandwidth (Hz)"))]
            bandwidthCents      = dialog.sndPrm['field'][dialog.sndPrm['fieldLabel'].index(dialog.tr("Bandwidth (Cents)"))]
            spacingCents        = dialog.sndPrm['field'][dialog.sndPrm['fieldLabel'].index(dialog.tr("Spacing (Cents)"))]
            itd                 = dialog.sndPrm['field'][dialog.sndPrm['fieldLabel'].index(dialog.tr("ITD (micro s)"))]
            ipd                 = dialog.sndPrm['field'][dialog.sndPrm['fieldLabel'].index(dialog.tr("IPD (radians)"))]
            narrowbandCmpLevel  = dialog.sndPrm['field'][dialog.sndPrm['fieldLabel'].index(dialog.tr("Narrow Band Component Level (dB SPL)"))]
            iterations          = int(dialog.sndPrm['field'][dialog.sndPrm['fieldLabel'].index(dialog.tr("Iterations"))])
            gain                = dialog.sndPrm['field'][dialog.sndPrm['fieldLabel'].index(dialog.tr("Gain"))]
            lowHarm             = int(dialog.sndPrm['field'][dialog.sndPrm['fieldLabel'].index(dialog.tr("Low Harmonic"))])
            highHarm            = int(dialog.sndPrm['field'][dialog.sndPrm['fieldLabel'].index(dialog.tr("High Harmonic"))])
            lowFreq             = dialog.sndPrm['field'][dialog.sndPrm['fieldLabel'].index(dialog.tr("Low Freq. (Hz)"))]
            highFreq            = dialog.sndPrm['field'][dialog.sndPrm['fieldLabel'].index(dialog.tr("High Freq. (Hz)"))]
            lowStopComplex      = dialog.sndPrm['field'][dialog.sndPrm['fieldLabel'].index(dialog.tr("Low Stop"))]
            highStopComplex     = dialog.sndPrm['field'][dialog.sndPrm['fieldLabel'].index(dialog.tr("High Stop"))]
            harmonicLevel       = dialog.sndPrm['field'][dialog.sndPrm['fieldLabel'].index(dialog.tr("Harmonic Level (dB SPL)"))]
            spectrumLevel       = dialog.sndPrm['field'][dialog.sndPrm['fieldLabel'].index(dialog.tr("Spectrum Level (dB SPL)"))]
            componentLevel      = dialog.sndPrm['field'][dialog.sndPrm['fieldLabel'].index(dialog.tr("Component Level (dB SPL)"))]
            duration            = dialog.sndPrm['field'][dialog.sndPrm['fieldLabel'].index(dialog.tr("Duration (ms)"))]
            ramp                = dialog.sndPrm['field'][dialog.sndPrm['fieldLabel'].index(dialog.tr("Ramp (ms)"))]
            noise1LowFreq       = dialog.sndPrm['field'][dialog.sndPrm['fieldLabel'].index(dialog.tr("No. 1 Low Freq. (Hz)"))]
            noise1HighFreq      = dialog.sndPrm['field'][dialog.sndPrm['fieldLabel'].index(dialog.tr("No. 1 High Freq. (Hz)"))]
            noise1SpectrumLevel = dialog.sndPrm['field'][dialog.sndPrm['fieldLabel'].index(dialog.tr("No. 1 S. Level (dB SPL)"))]
            noise2LowFreq       = dialog.sndPrm['field'][dialog.sndPrm['fieldLabel'].index(dialog.tr("No. 2 Low Freq. (Hz)"))]
            noise2HighFreq      = dialog.sndPrm['field'][dialog.sndPrm['fieldLabel'].index(dialog.tr("No. 2 High Freq. (Hz)"))]
            noise2SpectrumLevel = dialog.sndPrm['field'][dialog.sndPrm['fieldLabel'].index(dialog.tr("No. 2 S. Level (dB SPL)"))]
            stretch             = dialog.sndPrm['field'][dialog.sndPrm['fieldLabel'].index(dialog.tr("Stretch (%)"))]
            harmSpacing         = dialog.sndPrm['field'][dialog.sndPrm['fieldLabel'].index(dialog.tr("Harmonic Spacing (Cents)"))]
            
            channel           = dialog.sndPrm['chooser'][dialog.sndPrm['chooserLabel'].index(dialog.tr("Ear:"))]
            harmType          = dialog.sndPrm['chooser'][dialog.sndPrm['chooserLabel'].index(dialog.tr("Type:"))]
            harmPhase         = dialog.sndPrm['chooser'][dialog.sndPrm['chooserLabel'].index(dialog.tr("Phase:"))]
            noiseType         = dialog.sndPrm['chooser'][dialog.sndPrm['chooserLabel'].index(dialog.tr("Noise Type:"))]
            dichoticNoiseType = dialog.sndPrm['chooser'][dialog.sndPrm['chooserLabel'].index(dialog.tr("Dichotic Noise Type:"))]
            irnConfiguration  = dialog.sndPrm['chooser'][dialog.sndPrm['chooserLabel'].index(dialog.tr("IRN Type:"))]
            hugginsPhaseRel   = dialog.sndPrm['chooser'][dialog.sndPrm['chooserLabel'].index(dialog.tr("Phase relationship:"))]
            dichoticDifference= dialog.sndPrm['chooser'][dialog.sndPrm['chooserLabel'].index(dialog.tr("Dichotic Difference:"))]
            harmonicity       = dialog.sndPrm['chooser'][dialog.sndPrm['chooserLabel'].index(dialog.tr("Harmonicity:"))]
            bandwidthUnit     = dialog.sndPrm['chooser'][dialog.sndPrm['chooserLabel'].index(dialog.tr("Bandwidth Unit:"))]

            lowStop = 0.8
            highStop = 1.2

            if harmType == self.tr("Sinusoid"):
                self.stimulusCorrect = sndlib.complexTone(F0=F0, harmPhase=harmPhase, lowHarm=lowHarm, highHarm=highHarm, stretch=stretch, level=harmonicLevel, duration=duration, ramp=ramp, channel=channel, fs=fs, maxLevel=self.prm['pref']['sound']['maxLevel'])
            elif harmType == self.tr("Narrowband Noise"):
                self.stimulusCorrect = sndlib.harmComplFromNarrowbandNoise(F0=F0, lowHarm=lowHarm, highHarm=highHarm, level=spectrumLevel, bandwidth=bandwidth, bandwidthUnit=bandwidthUnit, duration=duration, ramp=ramp, channel=channel, fs=fs, maxLevel=self.prm['pref']['sound']['maxLevel'])
            elif harmType == self.tr("IRN"):
                delay = 1/float(F0)
                self.stimulusCorrect = sndlib.makeIRN(delay=delay, gain=gain, iterations=iterations, configuration=irnConfiguration, spectrumLevel=spectrumLevel, duration=duration, ramp=ramp, channel=channel, fs=fs, maxLevel=self.prm['pref']['sound']['maxLevel'])
            elif harmType == self.tr("Huggins Pitch"):
                if dichoticDifference in [self.tr("IPD Linear"), self.tr("IPD Stepped")]:
                    dichoticDifferenceValue = ipd
                elif dichoticDifference == self.tr("ITD"):
                    dichoticDifferenceValue = itd
                self.stimulusCorrect = sndlib.makeHugginsPitch(F0=F0, lowHarm=lowHarm, highHarm=highHarm, spectrumLevel=spectrumLevel, bandwidth=bandwidth, bandwidthUnit=bandwidthUnit, dichoticDifference=dichoticDifference, dichoticDifferenceValue=dichoticDifferenceValue, phaseRelationship=hugginsPhaseRel, noiseType=dichoticNoiseType, duration=duration, ramp=ramp, fs=fs, maxLevel=self.prm['pref']['sound']['maxLevel'])
                channel = self.tr("Both")
        
            if noiseType != self.tr("None"):
                if channel == self.tr("Odd Left") or channel == self.tr("Odd Right"): #alternating harmonics, different noise to the two ears
                    noiseR = sndlib.broadbandNoise(noise1SpectrumLevel, duration + ramp*6, 0, self.tr("Right"), fs, self.prm['pref']['sound']['maxLevel'])
                    noiseL = sndlib.broadbandNoise(noise1SpectrumLevel, duration + ramp*6, 0, self.tr("Left"), fs, self.prm['pref']['sound']['maxLevel'])
                    noise = noiseR + noiseL
                else:
                    noise = sndlib.broadbandNoise(noise1SpectrumLevel, duration + ramp*6, 0, channel, fs, self.prm['pref']['sound']['maxLevel'])
                if noiseType == self.tr("Pink"):
                    noise = sndlib.makePink(noise, fs)
                noise1 = sndlib.fir2Filt(noise1LowFreq*lowStop, noise1LowFreq, noise1HighFreq, noise1HighFreq*highStop, noise, fs)
                noise2 = sndlib.scale(noise2SpectrumLevel - noise1SpectrumLevel, noise)
                noise2 = sndlib.fir2Filt(noise2LowFreq*lowStop, noise2LowFreq, noise2HighFreq, noise2HighFreq*highStop, noise2, fs)
                noise = noise1 + noise2
                noise = noise[0:self.stimulusCorrect.shape[0],]
                noise = sndlib.gate(ramp, noise, fs)
                self.stimulusCorrect = self.stimulusCorrect + noise 
          
            thisSound = self.stimulusCorrect
            self.setupNewSound(sndData=thisSound, label=label, channel=channel, fs=fs)

    def onClickGenerateAMTone(self):
        dialog = generateSoundDialog(self, "AM Tone")
        if dialog.exec():

            for i in range(dialog.sndPrm['nFields']):
                dialog.sndPrm['field'][i] = self.currLocale.toDouble(dialog.field[i].text())[0]
            for i in range(dialog.sndPrm['nChoosers']):
                dialog.sndPrm['chooser'][i] = dialog.chooser[i].currentText()
            
            label = dialog.soundLabelWidget.text()
            fs = self.currLocale.toInt(dialog.sampRateWidget.text())[0]
            freq            = dialog.sndPrm['field'][dialog.sndPrm['fieldLabel'].index(dialog.tr("Frequency (Hz)"))]
            AMFreq            = dialog.sndPrm['field'][dialog.sndPrm['fieldLabel'].index(dialog.tr("AM Frequency (Hz)"))]
            AMDepth            = dialog.sndPrm['field'][dialog.sndPrm['fieldLabel'].index(dialog.tr("AM Depth"))]
            carrPhase            = dialog.sndPrm['field'][dialog.sndPrm['fieldLabel'].index(dialog.tr("Carrier Phase (radians)"))]
            modPhase            = dialog.sndPrm['field'][dialog.sndPrm['fieldLabel'].index(dialog.tr("Modulation Phase (radians)"))]
            duration            = dialog.sndPrm['field'][dialog.sndPrm['fieldLabel'].index(dialog.tr("Duration (ms)"))]
            ramp            = dialog.sndPrm['field'][dialog.sndPrm['fieldLabel'].index(dialog.tr("Ramp (ms)"))]
            level            = dialog.sndPrm['field'][dialog.sndPrm['fieldLabel'].index(dialog.tr("Level (dB SPL)"))]            
            channel           = dialog.sndPrm['chooser'][dialog.sndPrm['chooserLabel'].index(dialog.tr("Ear:"))]
            if channel == self.tr('Right'):
                channel = 'Right'
            elif channel == self.tr('Left'):
                channel = 'Left'
            elif channel == self.tr('Both'):
                channel = 'Both'
            
            thisSound = sndlib.AMTone(frequency=freq, AMFreq=AMFreq, AMDepth=AMDepth, phase=carrPhase, AMPhase=modPhase, level=level,
            duration=duration, ramp=ramp, channel=channel, fs=fs, maxLevel=self.prm['pref']['sound']['maxLevel'])
            #thisSound = self.stimulusCorrect
            self.setupNewSound(sndData=thisSound, label=label, channel=channel, fs=fs)

                        
    def onClickGenerateFMTone(self):
        dialog = generateSoundDialog(self, "FM Tone")
        if dialog.exec():

            for i in range(dialog.sndPrm['nFields']):
                dialog.sndPrm['field'][i] = self.currLocale.toDouble(dialog.field[i].text())[0]
            for i in range(dialog.sndPrm['nChoosers']):
                dialog.sndPrm['chooser'][i] = dialog.chooser[i].currentText()
            
            label = dialog.soundLabelWidget.text()
            fs = self.currLocale.toInt(dialog.sampRateWidget.text())[0]
            carrFreq            = dialog.sndPrm['field'][dialog.sndPrm['fieldLabel'].index(dialog.tr("Carrier Frequency (Hz)"))]
            modFreq            = dialog.sndPrm['field'][dialog.sndPrm['fieldLabel'].index(dialog.tr("Modulation Frequency (Hz)"))]
            modInd            = dialog.sndPrm['field'][dialog.sndPrm['fieldLabel'].index(dialog.tr("Modulation Index"))]
            carrPhase            = dialog.sndPrm['field'][dialog.sndPrm['fieldLabel'].index(dialog.tr("Carrier Phase (radians)"))]
            duration            = dialog.sndPrm['field'][dialog.sndPrm['fieldLabel'].index(dialog.tr("Duration (ms)"))]
            ramp            = dialog.sndPrm['field'][dialog.sndPrm['fieldLabel'].index(dialog.tr("Ramp (ms)"))]
            level            = dialog.sndPrm['field'][dialog.sndPrm['fieldLabel'].index(dialog.tr("Level (dB SPL)"))]            
            channel           = dialog.sndPrm['chooser'][dialog.sndPrm['chooserLabel'].index(dialog.tr("Ear:"))]

            if channel == self.tr('Right'):
                channel = 'Right'
            elif channel == self.tr('Left'):
                channel = 'Left'
            elif channel == self.tr('Both'):
                channel = 'Both'
            
            thisSound = sndlib.FMTone(fc=carrFreq, fm=modFreq, mi=modInd, phase=carrPhase, level=level, duration=duration, ramp=ramp, channel=channel, fs=fs, maxLevel=self.prm['pref']['sound']['maxLevel'])
            self.setupNewSound(sndData=thisSound, label=label, channel=channel, fs=fs)

    def onClickGenerateSilence(self):
        dialog = generateSoundDialog(self, "Silence")
        if dialog.exec():

            for i in range(dialog.sndPrm['nFields']):
                dialog.sndPrm['field'][i] = self.currLocale.toDouble(dialog.field[i].text())[0]
            for i in range(dialog.sndPrm['nChoosers']):
                dialog.sndPrm['chooser'][i] = dialog.chooser[i].currentText()
            
            label = dialog.soundLabelWidget.text()
            fs = self.currLocale.toInt(dialog.sampRateWidget.text())[0]
            duration            = dialog.sndPrm['field'][dialog.sndPrm['fieldLabel'].index(dialog.tr("Duration (ms)"))]            
            channel           = dialog.sndPrm['chooser'][dialog.sndPrm['chooserLabel'].index(dialog.tr("Ear:"))]
            if channel == self.tr('Right'):
                channel = 'Right'
            elif channel == self.tr('Left'):
                channel = 'Left'
            elif channel == self.tr('Both'):
                channel = 'Both'
            
            thisSound = sndlib.makeSilence(duration=duration, fs=fs)
            self.setupNewSound(sndData=thisSound, label=label, channel=channel, fs=fs)
           
    def setupNewSound(self, sndData, label, channel, fs):
        if channel in ['Right', 'Left']:
                thisSnd = {}
                if channel == 'Right':
                    thisSnd['wave'] = sndData[:,1]
                elif channel == 'Left':
                    thisSnd['wave'] = sndData[:,0]
                thisSnd['fs'] = fs
                #thisSnd['nBits'] = 0
                thisSnd['chan'] = channel
                thisSnd['nSamples'] = len(thisSnd['wave'])
                thisSnd['duration'] = thisSnd['nSamples'] / thisSnd['fs']
                thisSnd['label'] = label
                condSat = 0
                while condSat == 0:
                    tmp_id = random_id.random_id(5, 'alphanumeric')
                    if tmp_id in self.sndList:
                        condSat = 0
                    else:
                        condSat = 1
                self.sndList[tmp_id] = copy.copy(thisSnd)
                currCount = len(self.sndList)
                self.sndTableWidget.setRowCount(currCount)
                newItem = QTableWidgetItem(thisSnd['label'])
                newItem.setFlags(QtCore.Qt.ItemFlag.ItemIsSelectable | QtCore.Qt.ItemFlag.ItemIsEnabled)
                self.sndTableWidget.setItem(currCount-1, 0, newItem)
                newItem = QTableWidgetItem(thisSnd['chan'])
                newItem.setFlags(QtCore.Qt.ItemFlag.ItemIsSelectable | QtCore.Qt.ItemFlag.ItemIsEnabled)
                self.sndTableWidget.setItem(currCount-1, 1, newItem)
                self.sndList[tmp_id]['qid'] = QTableWidgetItem(tmp_id)
                self.sndTableWidget.setItem(currCount-1, 2, self.sndList[tmp_id]['qid'])

        if channel in ["Both", "Odd Right", "Odd Left"]:
            for i in range(2):
                thisSnd = {}
                if i == 0:
                    thisSnd['wave'] = sndData[:,1]
                    thisSnd['chan'] = self.tr('Right')
                else:
                    thisSnd['wave'] = sndData[:,0]
                    thisSnd['chan'] = self.tr('Left')
                thisSnd['fs'] = fs
                thisSnd['nSamples'] = len(thisSnd['wave'])
                thisSnd['duration'] = thisSnd['nSamples'] / thisSnd['fs']
                thisSnd['label'] = label
                condSat = 0
                while condSat == 0:
                    tmp_id = random_id.random_id(5, 'alphanumeric')
                    if tmp_id in self.sndList:
                        condSat = 0
                    else:
                        condSat = 1
                self.sndList[tmp_id] = copy.copy(thisSnd)
                currCount = len(self.sndList)
                self.sndTableWidget.setRowCount(currCount)
                newItem = QTableWidgetItem(thisSnd['label'])
                newItem.setFlags(QtCore.Qt.ItemFlag.ItemIsSelectable | QtCore.Qt.ItemFlag.ItemIsEnabled)
                self.sndTableWidget.setItem(currCount-1, 0, newItem)
                newItem = QTableWidgetItem(thisSnd['chan'])
                newItem.setFlags(QtCore.Qt.ItemFlag.ItemIsSelectable | QtCore.Qt.ItemFlag.ItemIsEnabled)
                self.sndTableWidget.setItem(currCount-1, 1, newItem)
                self.sndList[tmp_id]['qid'] = QTableWidgetItem(tmp_id)
                self.sndTableWidget.setItem(currCount-1, 2, self.sndList[tmp_id]['qid'])

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()
            
    def dropEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(Qt.CopyAction)
            event.accept()
            l = []
            for url in event.mimeData().urls():
                l.append(str(url.toLocalFile()))
            self.loadFiles(l)
        else:
            event.ignore()

    def onAbout(self):
        if pyqtversion in [4,5,6]:
            qt_compiled_ver = QtCore.QT_VERSION_STR
            qt_runtime_ver = QtCore.qVersion()
            qt_pybackend_ver = QtCore.PYQT_VERSION_STR
            qt_pybackend = "PyQt"
        elif pyqtversion == -4:
            qt_compiled_ver = QtCore.__version__
            qt_runtime_ver = QtCore.qVersion()
            qt_pybackend_ver = PySide.__version__
            qt_pybackend = "PySide"
        QMessageBox.about(self, self.tr("About pysoundanalyser"),
                                self.tr("""<b>pysoundanalyser - Python Sound Analyser</b> <br>
                                - version: {0}; <br>
                                - build date: {1} <br>
                                <p> Copyright &copy; 2010-2023 Samuele Carcagno. <a href="mailto:sam.carcagno@gmail.com">sam.carcagno@gmail.com</a> 
                                All rights reserved. <p>
                This program is free software: you can redistribute it and/or modify
                it under the terms of the GNU General Public License as published by
                the Free Software Foundation, either version 3 of the License, or
                (at your option) any later version.
                <p>
                This program is distributed in the hope that it will be useful,
                but WITHOUT ANY WARRANTY; without even the implied warranty of
                MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
                GNU General Public License for more details.
                <p>
                You should have received a copy of the GNU General Public License
                along with this program.  If not, see <a href="http://www.gnu.org/licenses/">http://www.gnu.org/licenses/</a>
                <p>Python {2} - {3} {4} compiled against Qt {5}, and running with Qt {6} on {7}""").format(__version__, self.prm['builddate'], platform.python_version(), qt_pybackend, qt_pybackend_ver, qt_compiled_ver, qt_runtime_ver, platform.system()))

class DropMainWindow(QMainWindow):
    drpd = QtCore.Signal(str) 
    def __init__(self, parent):
        QMainWindow.__init__(self, parent)
        self.setAcceptDrops(True)
        
    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls:
            event.accept()
        else:
            event.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls:
            event.setDropAction(Qt.CopyAction)
            event.accept()
            l = []
            for url in event.mimeData().urls():
                l.append(str(url.toLocalFile()))
                self.drpd.emit(l[len(l)-1])
        else:
            event.ignore()

def main():
    
    prm = {}
    prm['appData'] = {}
    #prm['appData'] = {}; prm['prefs'] = {}
    # create the GUI application
    qApp = QApplication(sys.argv)
    sys.excepthook = excepthook

    prm['calledWithWAVFiles'] = False
    parser = argparse.ArgumentParser()
    
    parser.add_argument("-f", "--file", help="Load WAV file", nargs='*', default='')
    args = parser.parse_args()
    if len(args.file) > 0:
        prm['calledWithWAVFiles'] = True
        prm['WAVFilesToLoad'] = args.file
    
    #first read the locale settings
    locale = QtCore.QLocale().system().name() #returns a string such as en_US
    qtTranslator = QtCore.QTranslator()
    if qtTranslator.load("qt_" + locale, ":/translations/"):
        qApp.installTranslator(qtTranslator)
    appTranslator = QtCore.QTranslator()
    if appTranslator.load("pysoundanalyser_" + locale, ":/translations/"):
        qApp.installTranslator(appTranslator)
    prm['appData']['currentLocale'] = QtCore.QLocale(locale)
    QtCore.QLocale.setDefault(prm['appData']['currentLocale'])
    
    rootDirectory = os.path.abspath(os.path.dirname(sys.argv[0]))
    prm['rootDirectory'] = rootDirectory
    
    prm = get_prefs(prm)
    prm = set_global_parameters(prm)
    
    #then load the preferred language
    if prm['pref']['country'] != "System Settings":
        locale =  prm['pref']['language']  + '_' + prm['pref']['country']#returns a string such as en_US
        qtTranslator = QtCore.QTranslator()
        if qtTranslator.load("qt_" + locale, ":/translations/"):
            qApp.installTranslator(qtTranslator)
        appTranslator = QtCore.QTranslator()
        if appTranslator.load("pysoundanalyser_" + locale, ":/translations/") or locale == "en_US":
            qApp.installTranslator(appTranslator)
            prm['appData']['currentLocale'] = QtCore.QLocale(locale)
            QtCore.QLocale.setDefault(prm['appData']['currentLocale'])
            prm['appData']['currentLocale'].setNumberOptions(prm['appData']['currentLocale'].NumberOption.OmitGroupSeparator | prm['appData']['currentLocale'].NumberOption.RejectGroupSeparator)

    
    qApp.setWindowIcon(QIcon(":/johnny_automatic_crashing_wave.svg"))
    ## Look and feel changed to CleanLooks
    #QApplication.setStyle(QStyleFactory.create("QtCurve"))
    #QApplication.setPalette(QApplication.style().standardPalette())
    #qApp.currentLocale = locale
    # instantiate the ApplicationWindow widget
    qApp.setApplicationName('pysoundanalyser')
    if platform.system() == "Windows":
        qApp.setStyle('Fusion')
    aw = applicationWindow(prm)


    # show the widget
    aw.show()
    # start the Qt main loop execution, exiting from this script
    # with the same return code of Qt application
    sys.exit(qApp.exec())
if __name__ == "__main__":
    main()
   
