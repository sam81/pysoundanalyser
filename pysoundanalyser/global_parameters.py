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

import matplotlib, platform
matplotlib.rcParams['path.simplify'] = False

if platform.system() == "Linux":
    try:
        import alsaaudio
        alsaaudioAvailable = True
    except ImportError:
        alsaaudioAvailable = False
        pass
else:
    alsaaudioAvailable = False
    

try:
    import pyaudio
    pyaudioAvailable = True
except ImportError:
    pyaudioAvailable = False
    pass

try:
    import soundfile
    sndf_available = True
except:
    sndf_available = False

from .pyqtver import*
if pyqtversion == 5:
    from PyQt5 import QtGui, QtCore
    #from PyQt5.QtGui import QColor
    from PyQt5.QtWidgets import QApplication
    matplotlib.rcParams['backend'] = "Qt5Agg"
    prefFileSuffix = ""
elif pyqtversion == 6:
    from PyQt6 import QtGui, QtCore
    #from PyQt6.QtGui import QColor
    from PyQt6.QtWidgets import QApplication
    matplotlib.rcParams['backend'] = "Qt5Agg"
    prefFileSuffix = ""

import platform, os, pickle


def set_global_parameters(prm):
    prm['appData']['available_colormaps'] = [m for m in matplotlib.cm.datad if not m.endswith("_r")]
    prm['appData']['available_windows'] = ['none', 'hamming', 'hanning', 'blackman', 'bartlett']
    prm['appData']['available_filters'] = ['fir2_presets']
    prm['appData']['available_languages'] = ["System Settings",
                                             "en",
                                             "it",
                                             "fr",
                                             "es",
                                             "el"]
    prm['appData']['available_countries'] = {}
    prm['appData']['available_countries']['System Settings'] = ["System Settings"]
    prm['appData']['available_countries']['en'] = ["US",
                                                   "GB"]

    prm['appData']['available_countries']['it'] = ["IT",
                                                   "CH"]
    prm['appData']['available_countries']['fr'] = ["FR",
                                                   "CA"]

    prm['appData']['available_countries']['es'] = ["ES",
                                                   "BO",
                                                   "CL"]

    prm['appData']['available_countries']['el'] = ["GR",
                                                   "CY"]

    prm['appData']['alsaaudioAvailable'] = alsaaudioAvailable
    prm['appData']['pyaudioAvailable'] = pyaudioAvailable

    if platform.system() == 'Linux':
        prm['appData']['available_play_commands'] = []
        if os.system("which aplay") == 0:
            prm['appData']['available_play_commands'].append("aplay")
        if os.system("which play") == 0:
            prm['appData']['available_play_commands'].append("play")
        if os.system("which sndfile-play") == 0:
            prm['appData']['available_play_commands'].append("sndfile-play")
    elif platform.system() == 'Windows':
        prm['appData']['available_play_commands'] = ["winsound"]
        if os.system("where sndfile-play") == 0:
            prm['appData']['available_play_commands'].append("sndfile-play")  
    elif platform.system() == 'Darwin': #that should be the MAC
        prm['appData']['available_play_commands'] = ["afplay"]
    elif platform.system() == 'FreeBSD':
        prm['appData']['available_play_commands'] = ["wavplay"]
    else:
        prm['appData']['available_play_commands'] = [QApplication.translate("","custom","")]

    if pyaudioAvailable == True:
        prm['appData']['available_play_commands'].append("pyaudio")
    if alsaaudioAvailable == True:
        prm['appData']['available_play_commands'].append("alsaaudio")
    prm['appData']['available_play_commands'].append(QApplication.translate("","custom",""))

    prm['appData']['nBitsChoices'] = ["16", "24", "32"]

    return prm
  


def def_prefs(prm):
    prm['pref'] = {}
    prm['pref']['sound'] = {}
    prm['pref']['colormap'] = 'jet'
    prm['pref']['spectrumLogXAxis'] = False
    #FFT preferences
    prm['pref']['smoothingWindow'] = 'hamming'
    prm['pref']['poweroftwo'] = False

    ########################
    #Sound preferences
    if sndf_available == True:
        prm["pref"]["sound"]["wavmanager"] = "soundfile"
    else:
        prm["pref"]["sound"]["wavmanager"] = "scipy"

    if platform.system() == 'Windows':
        prm["pref"]["sound"]["playCommand"] = "winsound"
        prm["pref"]["sound"]["playCommandType"] = "winsound"
    elif platform.system() == 'Darwin':
        prm["pref"]["sound"]["playCommand"] = "afplay"
        prm["pref"]["sound"]["playCommandType"] = QApplication.translate("","custom","")
    else:
        prm["pref"]["sound"]["playCommand"] = "aplay"
        prm["pref"]["sound"]["playCommandType"] = QApplication.translate("","custom","")
    if alsaaudioAvailable == True:
        prm["pref"]["sound"]["alsaaudioDevice"] = "default"
    if pyaudioAvailable == True:
        prm["pref"]["sound"]["pyaudioDevice"] = 0



    # if platform.system() == 'Windows':
    #     prm["pref"]["sound"]["playCommand"] = 'winsound'
    #     prm["pref"]["sound"]["playCommandType"] = 'winsound'
    # elif platform.system() == "Darwin":
    #     prm["pref"]["sound"]["playCommand"] = 'afplay'
    #     prm["pref"]["sound"]["playCommandType"] = QApplication.translate("Preferences Window","custom","")
    # elif platform.system() == 'FreeBSD':
    #     prm['appData']['available_play_commands'] = ["wavplay"]
    #     prm['appData']['available_play_commands'].append(QApplication.translate("Preferences Window","custom",""))
    # else:
    #     prm["pref"]["sound"]["playCommand"] = 'aplay'
    #     prm["pref"]["sound"]["playCommandType"] = 'aplay'
    # if platform.system() == 'Windows':
    #     prm['appData']['available_play_commands'] = ["winsound", "sndfile-play", QApplication.translate("Preferences Window","custom","")]
    # else:
    #     prm['appData']['available_play_commands'] = ["aplay", "sndfile-play", QApplication.translate("Preferences Window","custom","")]

    prm["pref"]["sound"]["nBits"] = "32"
    prm["pref"]["sound"]["maxLevel"] = 100
    prm["pref"]["sound"]["appendSilence"] = 0
    prm["pref"]["sound"]["bufferSize"] = 1024

    ######################################
    #Figure preferences
    prm['pref']['grid'] = True
    prm['pref']['dpi'] = 80
    #range is 0--255
    prm['pref']['lineColor1'] = (0,0,0)
    prm['pref']['line_width'] = 1
    prm['pref']['backgroundColor'] = (250,250,250)
    prm['pref']['canvasColor'] = (200, 200, 200)
    prm['pref']['axes_color'] = (0,0,0)
    prm['pref']['grid_color'] = (0,0,0)
    prm['pref']['tick_label_color'] = (0,0,0)
    prm['pref']['axes_label_color'] = (0,0,0)
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
    prm['pref']['spectrum_x_axis_label'] = QApplication.translate("Spectrum Plot","Frequency (Hz)","")
    prm['pref']['spectrum_y_axis_label'] = QApplication.translate("Spectrum Plot","Level (dB)","")
    prm['pref']['waveform_x_axis_label'] = QApplication.translate("Waveform Plot","Time (s)","")
    prm['pref']['waveform_y_axis_label'] = QApplication.translate("Waveform Plot","Amplitude","")
    prm['pref']['acf_x_axis_label'] = QApplication.translate("Autocorrelation Plot","Lag (s)","")
    prm['pref']['acf_y_axis_label'] = QApplication.translate("Autocorrelation Plot","Correlation","")
    prm['pref']['spectrogram_x_axis_label'] = QApplication.translate("Spectrogram Plot","Time (s)","")
    prm['pref']['spectrogram_y_axis_label'] = QApplication.translate("Spectrogram Plot","Frequency (Hz)","")
    prm['pref']['autocorrelogram_x_axis_label'] = QApplication.translate("Autocorrelogram Plot","Time (s)","")
    prm['pref']['autocorrelogram_y_axis_label'] = QApplication.translate("Autocorrelogram Plot","Lag (s)","")

    prm['pref']['language'] = 'System Settings'
    prm['pref']['country'] = 'System Settings'

    return prm



def get_prefs(prm):
    prm = def_prefs(prm)
    prm['prefFile'] = os.path.expanduser("~") +'/.config/pysoundanalyser/preferences'+prefFileSuffix

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
