#!/usr/bin/env bash
#pyrcc4 -py3 -o ../pysoundanalyser/qrc_resources.py ../resources.qrc
rcc -g python ../resources.qrc | sed '0,/PySide2/s//PyQt6/' > ../pysoundanalyser/qrc_resources.py
pylupdate6 -verbose pysoundanalyser.pro
lrelease -verbose pysoundanalyser.pro

mv *.qm ../translations/
