#!/bin/sh

. /home/sam/bin/ppyenv/bin/activate
read -p 'pyqtver: ' pyqtver
./mkupdate_pyqt$pyqtver.sh
cd ../pysoundanalyser/doc
./mkdoc.sh
cd ../../prep-release
cd ..
python3 -m build

