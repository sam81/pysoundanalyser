#!/bin/sh

cd ../doc
#./mkdoc.sh
cp manual/pysoundanalyser_manual.pdf ../pysoundanalyser_pack/doc/


cd ../prep-release
./mkupdate.sh
./distbuild.sh 
