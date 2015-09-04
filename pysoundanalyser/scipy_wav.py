# -*- coding: utf-8 -*-
from __future__ import nested_scopes, generators, division, absolute_import, with_statement, print_function, unicode_literals
from scipy.io import wavfile
from numpy import float32, int16, int32

def scipy_wavwrite(fname, fs, nbits, data):
    if nbits == 16:
        data = data*(2.**15)
        data = data.astype(int16)
    elif nbits == 24:
        print('error, cannot save 24 bits at the moment')
    elif nbits == 32:
        data = data*(2.**31)
        data = data.astype(int32)

    if nbits != 24:
        wavfile.write(fname, fs, data)

def scipy_wavread(fname):
    fs, snd = wavfile.read(fname)
    if snd.dtype == int16:
        snd = snd/(2.**15)
        nbits = 16
    elif snd.dtype == int32:
        snd = snd/(2.**31)
        nbits = 32
    elif snd.dtype == float32:
        nbits = 32
    #if snd.ndim == 1:
    #    snd = snd.reshape(snd.shape[0], 1) # if there is only 1 chan, for consistency put it in column format
    return fs, snd, nbits
    
