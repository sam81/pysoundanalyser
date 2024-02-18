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

from pysoundanalyser.pyqtver import*
if pyqtversion == 5:
    from PyQt5.QtCore import QThread
elif pyqtversion == 6:
    from PyQt6.QtCore import QThread
    

from pysoundanalyser.win_waveform_plot import*
from pysoundanalyser.win_spectrum_plot import*
from pysoundanalyser.win_spectrogram_plot import*
from pysoundanalyser.win_acf_plot import*
from pysoundanalyser.win_autocorrelogram_plot import*

class threadedWaveformPlot(QThread):
    def __init__(self, parent):
        QThread.__init__(self, parent)
    def plotWaveformThreaded(self, sound, prm):
        self.sound = sound
        self.prm = prm
        self.start()
    def run(self):
        
        waveformPlot(self, self.sound, self.prm)
        #print("THREAD RUNNING")
        #print(self.sound)
 
