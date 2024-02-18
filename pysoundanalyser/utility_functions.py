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
elif pyqtversion == 6:
    from PyQt6 import QtGui, QtCore
    
from numpy import sin, cos, pi, sqrt, abs, arange, floor, zeros, mean, concatenate, convolve, correlate, angle, real, log2, log10, int_, linspace, repeat, ceil, unique, hamming, hanning, blackman, bartlett, round, transpose, flipud, amax
from numpy.fft import rfft, irfft, fft, ifft
from scipy.signal import firwin2
import copy
#import pysoundanalyser.pysndlib as sndlib
from pysoundanalyser import sndlib

def pltColorFromQColor(qcolor):
    col = (qcolor.red()/255., qcolor.green()/255., qcolor.blue()/255.)
    return col

def scaleRGBTo01(col):
    col = tuple(el/255 for el in col)
    return col

def getSpectrum(sig, sampFreq, window, poweroftwo):
    n = len(sig)
    if poweroftwo == True:
        nfft = 2**sndlib.nextpow2(n)
    else:
        nfft = n
    if window != 'none':
        if window == 'hamming':
             w = hamming(n)
        elif window == 'hanning':
             w = hanning(n)
        elif window == 'blackman':
             w = blackman(n)
        elif window == 'bartlett':
             w = bartlett(n)
        sig = sig*w
        
         
    p = fft(sig, nfft) # take the fourier transform 
    nUniquePts = int(ceil((nfft+1)/2.0))
    p = p[0:nUniquePts]
    p = abs(p)
    p = p / float(n) #float(n) # scale by the number of points so that
    # the magnitude does not depend on the length 
    # of the signal or on its sampling frequency  
    p = p**2  # square it to get the power 

    # multiply by two (see technical document for details)
    # odd nfft excludes Nyquist point
    if nfft % 2 > 0: # we've got odd number of points fft
         p[1:len(p)] = p[1:len(p)] * 2
    else:
         p[1:len(p) -1] = p[1:len(p) - 1] * 2 # we've got even number of points fft

    freqArray = arange(0, nUniquePts, 1.0) * (sampFreq / float(nfft));
    return freqArray, p

def getSpectrogram(sig, sampFreq, winLength, overlap, winType, poweroftwo):
    #winLength in seconds
    #overlap in percent
    #if the signal length is not a multiple of the window length it is truncated
    winLengthPnt = floor(winLength * sampFreq).astype("int")
    step = winLengthPnt - round(winLengthPnt * overlap / 100.).astype("int")
    ind = arange(0, len(sig) - winLengthPnt, step)
    n = len(ind)

    freqArray, p = getSpectrum(sig[ind[0]:ind[0]+winLengthPnt], sampFreq, winType, poweroftwo)

    powerMatrix = zeros((len(freqArray), n))
    powerMatrix[:,0] = p
    for i in range(1, n):
        freqArray, p = getSpectrum(sig[ind[i]:ind[i]+winLengthPnt], sampFreq, winType, poweroftwo)
        powerMatrix[:,i] = p

    timeInd = arange(0, len(sig), step)
    timeArray = 1/sampFreq * (timeInd)
    return powerMatrix, freqArray, timeArray


def getAcf(sig, sampRate, maxLag, normalised, window):
    n = len(sig)
    if window != 'none':
        if window == 'hamming':
             w = hamming(n)
        elif window == 'hanning':
             w = hanning(n)
        elif window == 'blackman':
             w = blackman(n)
        elif window == 'bartlett':
             w = bartlett(n)
        sig = sig*w
    sampRate = float(sampRate) 
    acf = correlate(sig, sig, mode=str('full'))
    acf = acf[int(acf.size/2):]
    maxLagPnt = int(round(maxLag*sampRate))
    if maxLagPnt > len(acf):
         maxLagPnt = int(len(acf))
    acf = acf[0:maxLagPnt]
    lags = arange(maxLagPnt)/sampRate
    if normalised == True:
        acf = acf/max(acf)
    return lags, acf

def getAutocorrelogram(sig, sampFreq, winLength, overlap, winType, maxLag, normalised):
    #winLength in seconds
    #overlap in percent
    winLengthPnt = floor(winLength * sampFreq).astype("int")
    step = winLengthPnt - round(winLengthPnt * overlap / 100.).astype("int")
    ind = arange(0, len(sig) - winLengthPnt, step)
    n = len(ind)

    lags, acf = getAcf(sig[ind[0]:ind[0]+winLengthPnt], sampFreq, maxLag, normalised, winType)

    acfMatrix = zeros((len(acf), n))
    acfMatrix[:,0] = acf
    for i in range(1, n):
        lags, acf = getAcf(sig[ind[i]:ind[i]+winLengthPnt], sampFreq, maxLag, normalised, winType)
        acfMatrix[:,i] = acf

    timeInd = arange(0, len(sig), step)
    timeArray = 1/sampFreq * (timeInd)
    return acfMatrix, lags, timeArray
            

def log_10_product(x, pos):
    """The two args are the value and tick position.
    Label ticks with the product of the exponentiation"""
    return '%1i' % (x)

def concatenateSounds(sound1, sound2, delay, delayType, fs):
    #snd1 and snd2 have only one channel
    #delay in ms
    delay = delay/1000
    delayPnts = int(round(delay*fs))
    nSampSound1 = len(sound1)
    nSampSound2 = len(sound2)
    if delayType == "onset to onset":
        delayPnts = delayPnts - nSampSound1
    elif delayType == "offset to onset":
        pass

    if delayPnts < 0 and abs(delayPnts) > nSampSound1:
        # in this case sound2 leads sound1 with a delay of abs(delayPnts) - nSampSnd1 - nSampSnd2
        delayPnts = abs(delayPnts) - nSampSound1 - nSampSound2
        snd1 = sound2
        snd2 = sound1
    else:
        snd1 = sound1
        snd2 = sound2


    nSampSnd1 = len(snd1)
    nSampSnd2 = len(snd2)
    if delayPnts == 0:
        #case 1
        # s1 ---------
        # s2          ------------
        cn = concatenate((snd1, snd2), axis=0)
    elif delayPnts > 0:
        #case 2
        # s1 ------------
        # s2                  -----------
        sil = zeros(delayPnts)
        cn1 = concatenate((snd1, sil), axis=0)
        cn  = concatenate((cn1, snd2), axis=0)
    elif delayPnts < 0 and abs(delayPnts) < nSampSnd1:
        seg1 = snd1[0:len(snd1) - abs(delayPnts)]
        if nSampSnd2 > abs(delayPnts):
            #case 3a
            # s1 -----------
            # s2        ----------
            seg2 = snd1[len(snd1) - abs(delayPnts):nSampSnd1] + snd2[0:abs(delayPnts)]
            seg3 = snd2[abs(delayPnts):nSampSnd2]
            cn1 = concatenate((seg1, seg2), axis=0)
            cn = concatenate((cn1, seg3), axis=0)
        elif nSampSnd2 == abs(delayPnts):
            #case 3b
            # s1 ------------
            # s2       ------
            seg2 = snd1[len(snd1) - abs(delayPnts):nSampSnd1] + snd2
            cn = concatenate((seg1, seg2), axis=0)
        elif nSampSnd2 < abs(delayPnts):
            # case 3c
            # s1 -------------
            # s2      ----
            seg2 = snd1[len(snd1) - abs(delayPnts):len(snd1) - abs(delayPnts) + nSampSnd2] + snd2
            seg3 = snd1[len(snd1) - abs(delayPnts) + nSampSnd2: nSampSnd1]
            cn1 = concatenate((seg1, seg2), axis=0)
            cn = concatenate((cn1, seg3), axis=0)
    elif delayPnts < 0 and abs(delayPnts) == nSampSnd1:
        if nSampSnd1 > nSampSnd2:
            #case 4a
            # s1 ------------------
            # s2 -----------
            seg1 = snd1[0:nSampSnd2] + snd2
            seg2 = snd1[nSampSnd2:nSampSnd1]
            cn = concatenate((seg1, seg2), axis=0)
        elif nSampSnd1 == nSampSnd2:
            #case 4b
            # s1 ------------------
            # s2 ------------------
            cn = snd1 + snd2
        elif nSampSnd1 < nSampSnd2:
            #case 4c
            # s1 -----------
            # s2 ----------------
            seg1 = snd2[0:nSampSnd1] + snd1
            seg2 = snd2[nSampSnd1:nSampSnd2]
            cn = concatenate((seg1, seg2), axis=0)

    return cn
    



#def scale_rms(sig, desiredRms)
def fir2FiltAlt(f1, f2, f3, f4, filterType, snd, fs, filterOrder):
    fs = float(fs)
    f1 = (f1 * 2) / fs
    f2 = (f2 * 2) / fs
    f3 = (f3 * 2) / fs
    f4 = (f4 * 2) / fs

    n = filterOrder

    if filterType == 'lowpass':
        f = [0, f3, f4, 1]
        m = [1, 1, 0.00003, 0]
    elif filterType == 'highpass':
        f = [0, f1, f2, 0.999999, 1] #high pass
        m = [0, 0.00003, 1, 1, 0]
    elif filterType == 'bandpass':
        f = [0, f1, f2, ((f2+f3)/2), f3, f4, 1]
        m = [0, 0.00003, 1, 1, 1, 0.00003, 0]
    elif filterType == 'bandstop':
        f = [0, f1, f2, ((f2+f3)/2), f3, f4, 0.999999, 1] #band stop
        m = [1, 1, 0.00003, 0, 0.00003, 1, 1, 0] 
   

    b = firwin2 (n,f,m);
    x = copy.copy(snd)
    x = convolve(snd, b, 1)
    #x[:, 1] = convolve(snd[:,1], b, 1)
    
    return x


def cutSampleRegion(snd, startCut, endCut):
    print(startCut)
    print(endCut)
    nSamples = snd.shape[0]
    if startCut < 0 or endCut > nSamples:
        print("out of boundaries")
        return
    else:
        if startCut == 0:
            if snd.ndim == 1:
                snd = snd[endCut:nSamples]
            elif snd.ndim == 2:
                snd = snd[endCut:nSamples,:]
        elif endCut == nSamples:
             if snd.ndim == 1:
                 snd = snd[0:startCut]
             elif snd.ndim == 2:
                 snd = snd[0:startCut,:]
        else:
            snd = concatenate((snd[0:startCut], snd[endCut:nSamples]), axis=0)
    return snd
                
## def cutTimeRegion(snd, startCut, endCut, cutUnit, fs):
##     if cutUnit == "msec":
##         startCut = startCut / 1000
##         endCut = endCut / 1000
##     nSamples = snd.shape[0]
##     startCutSamples = int(round(startCut * fs))
##     endCutSamples = int(round(endCut * fs))
##     if startCutSamples < 0 or endCutSamples > nSamples:
##         print("out of boundaries")
##         return
##     snd = cutSampleRegion(snd, startCutSamples, endCutSamples)
##     return snd
