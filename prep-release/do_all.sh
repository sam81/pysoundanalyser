#!/bin/sh

python3 do_pyside.py
python3 do_pyqt4.py
./mkupdate_pyqt5.sh
./distbuild.sh 
