#!/bin/sh

pyrcc5 -o ../pysoundanalyser/qrc_resources.py ../resources.qrc
pylupdate5 -verbose pysoundanalyser.pro
lrelease -verbose pysoundanalyser.pro

mv *.qm ../translations/
