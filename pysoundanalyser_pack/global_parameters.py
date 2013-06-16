# -*- coding: utf-8 -*-
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
from PyQt4.QtGui import QApplication#.translate

import platform, os, pickle
from pylab import*


def global_parameters(prm):
    prm['data']['available_colormaps'] = [m for m in cm.datad if not m.endswith("_r")]
    prm['data']['available_windows'] = ['none', 'hamming', 'hanning', 'blackman', 'bartlett']
    prm['data']['available_filters'] = ['fir2_presets']
    prm['data']['available_languages'] = [QApplication.translate("Preferences Window","System Settings","", QApplication.UnicodeUTF8),
                                          QApplication.translate("Preferences Window","en","", QApplication.UnicodeUTF8),
                                          QApplication.translate("Preferences Window","it","", QApplication.UnicodeUTF8),
                                          QApplication.translate("Preferences Window","fr","", QApplication.UnicodeUTF8),
                                          QApplication.translate("Preferences Window","es","", QApplication.UnicodeUTF8),
                                          QApplication.translate("Preferences Window","el","", QApplication.UnicodeUTF8)]
    prm['data']['available_countries'] = {}
    prm['data']['available_countries']['System Settings'] = ["System Settings"]
    prm['data']['available_countries']['en'] = [QApplication.translate("Preferences Window","US","", QApplication.UnicodeUTF8),
                                                         QApplication.translate("Preferences Window","GB","", QApplication.UnicodeUTF8)]

    prm['data']['available_countries']['it'] = [QApplication.translate("Preferences Window","IT","", QApplication.UnicodeUTF8),
                                                         QApplication.translate("Preferences Window","CH","", QApplication.UnicodeUTF8)]
    prm['data']['available_countries']['fr'] = [QApplication.translate("Preferences Window","FR","", QApplication.UnicodeUTF8),
                                                         QApplication.translate("Preferences Window","CA","", QApplication.UnicodeUTF8)]

    prm['data']['available_countries']['es'] = [QApplication.translate("Preferences Window","ES","", QApplication.UnicodeUTF8),
                                                         QApplication.translate("Preferences Window","BO","", QApplication.UnicodeUTF8),
                                                         QApplication.translate("Preferences Window","CL","", QApplication.UnicodeUTF8)]

    prm['data']['available_countries']['el'] = [QApplication.translate("Preferences Window","GR","", QApplication.UnicodeUTF8),
                                                         QApplication.translate("Preferences Window","CY","", QApplication.UnicodeUTF8)]

    return prm
  


def def_prefs(prm):
    prm["pref"] = {}
    prm['pref']['colormap'] = 'jet'
    prm['pref']['spectrumLogXAxis'] = False
    #FFT preferences
    prm['pref']['smoothingWindow'] = 'hamming'
    prm['pref']['poweroftwo'] = False
    #Sound preferences
    prm["pref"]["wavmanager"] = "scipy"
    if platform.system() == 'Windows':
        prm["pref"]["playCommand"] = 'winsound'
        prm["pref"]["playCommandType"] = 'winsound'
    else:
        prm["pref"]["playCommand"] = 'aplay'
        prm["pref"]["playCommandType"] = 'aplay'
    if platform.system() == 'Windows':
        prm['data']['available_play_commands'] = ["winsound", "sndfile-play", QApplication.translate("Preferences Window","custom","", QApplication.UnicodeUTF8)]
    else:
        prm['data']['available_play_commands'] = ["aplay", "sndfile-play", QApplication.translate("Preferences Window","custom","", QApplication.UnicodeUTF8)]

    prm["pref"]["nBits"] = 16
    prm["pref"]["maxLevel"] = 100
    #Figure preferences
    prm['pref']['grid'] = True
    prm['pref']['dpi'] = 80
    #range is 0--255
    prm['pref']['lineColor1'] = QtGui.QColor(0,0,0)
    prm['pref']['line_width'] = 1
    prm['pref']['backgroundColor'] = QtGui.QColor(250,250,250)
    prm['pref']['canvasColor'] = QtGui.QColor(200, 200, 200)
    prm['pref']['axes_color'] = QtGui.QColor(0,0,0)
    prm['pref']['grid_color'] = QtGui.QColor(0,0,0)
    prm['pref']['tick_label_color'] = QtGui.QColor(0,0,0)
    prm['pref']['axes_label_color'] = QtGui.QColor(0,0,0)
    prm['pref']['label_font_family'] = 'sans-serif'
    prm['pref']['label_font_weight'] = 'normal'
    prm['pref']['label_font_style'] = 'normal' #italics, oblique
    prm['pref']['label_font_size'] = 12
    prm['pref']['label_font_stretch'] = 'normal'
    prm['pref']['label_font_variant'] = 'normal'
    prm['pref']['major_tick_length'] = 5
    prm['pref']['major_tick_width'] = 1
    prm['pref']['minor_tick_length'] = 3
    prm['pref']['minor_tick_width'] = 0.8

    prm['pref']['grid_line_width'] = 0.5
    prm['pref']['spines_line_width'] = 1


    prm['pref']['tick_label_font_family'] = 'sans-serif'
    prm['pref']['tick_label_font_weight'] = 'normal'
    prm['pref']['tick_label_font_style'] = 'normal' #italics, oblique
    prm['pref']['tick_label_font_size'] = 12
    prm['pref']['tick_label_font_stretch'] = 'normal'
    prm['pref']['tick_label_font_variant'] = 'normal'
    prm['pref']['spectrum_x_axis_label'] = QApplication.translate("Spectrum Plot","Frequency (Hz)","", QApplication.UnicodeUTF8)
    prm['pref']['spectrum_y_axis_label'] = QApplication.translate("Spectrum Plot","Level (dB)","", QApplication.UnicodeUTF8)
    prm['pref']['waveform_x_axis_label'] = QApplication.translate("Waveform Plot","Time (s)","", QApplication.UnicodeUTF8)
    prm['pref']['waveform_y_axis_label'] = QApplication.translate("Waveform Plot","Amplitude","", QApplication.UnicodeUTF8)
    prm['pref']['acf_x_axis_label'] = QApplication.translate("Autocorrelation Plot","Lag (s)","", QApplication.UnicodeUTF8)
    prm['pref']['acf_y_axis_label'] = QApplication.translate("Autocorrelation Plot","Correlation","", QApplication.UnicodeUTF8)
    prm['pref']['spectrogram_x_axis_label'] = QApplication.translate("Spectrogram Plot","Time (s)","", QApplication.UnicodeUTF8)
    prm['pref']['spectrogram_y_axis_label'] = QApplication.translate("Spectrogram Plot","Frequency (Hz)","", QApplication.UnicodeUTF8)
    prm['pref']['autocorrelogram_x_axis_label'] = QApplication.translate("Autocorrelogram Plot","Time (s)","", QApplication.UnicodeUTF8)
    prm['pref']['autocorrelogram_y_axis_label'] = QApplication.translate("Autocorrelogram Plot","Lag (s)","", QApplication.UnicodeUTF8)

    prm['pref']['language'] = 'System Settings'
    prm['pref']['country'] = 'System Settings'

    return prm



def get_prefs(prm):
    prm = def_prefs(prm)
    prm['prefFile'] = os.path.expanduser("~") +'/.config/pysoundanalyser/preferences'

    if os.path.exists(os.path.expanduser("~") +'/.config/') == False:
        os.mkdir(os.path.expanduser("~") +'/.config/')
    if os.path.exists(os.path.expanduser("~") +'/.config/pysoundanalyser/') == False:
        os.mkdir(os.path.expanduser("~") +'/.config/pysoundanalyser/')
    if os.path.exists(prm['prefFile']):
        fIn = open(prm['prefFile'], 'rb')
        prm['tmp'] = pickle.load(fIn)
        fIn.close()
        for k in prm['pref'].keys():
            if k in prm['tmp']:
                prm['pref'][k] = prm['tmp'][k]
    return prm
