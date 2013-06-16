#!/usr/bin/env bash
pyrcc4 -py3 -o ../pysoundanalyser_pack/qrc_resources.py ../resources.qrc 
pylupdate4 -verbose pysoundanalyser.pro
lrelease -verbose pysoundanalyser.pro

mv *.qm ../translations/
