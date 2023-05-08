#! /usr/bin/env python
# -*- coding: utf-8 -*- 

import copy, os

thisDir = os.getcwd()
#read the current pyqt version
f = open('../pysoundanalyser/pyqtver.py', 'r')
pyqtverLines = f.readlines()
pyqtverLinesPyQt6 = copy.copy(pyqtverLines)
f.close()
for i in range(len(pyqtverLinesPyQt6)):
    if pyqtverLinesPyQt6[i].strip().split('=')[0].strip() == "pyqtversion":
           pyqtverLinesPyQt6[i] = "pyqtversion = 6\n"

#Change pyqtver to PyQt6
f = open('../pysoundanalyser/pyqtver.py', 'w')
f.writelines(pyqtverLinesPyQt6)
f.close()

os.system('/usr/bin/sh mkupdate_pyqt6.sh')

os.chdir('../')
os.system('python3 setup-pyqt6.py sdist --formats=gztar,zip')
#os.system('python3 setup-pyqt4.py bdist_wininst')

#revert to pyqt5
for i in range(len(pyqtverLines)):
    if pyqtverLines[i].strip().split('=')[0].strip() == "pyqtversion":
           pyqtverLines[i] = "pyqtversion = 5\n"
os.chdir('prep-release')
f = open('../pysoundanalyser/pyqtver.py', 'w')
f.writelines(pyqtverLines)
f.close()

os.system('/usr/bin/sh mkupdate_pyqt5.sh')
