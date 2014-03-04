

pyside-rcc -py3 -o ../pysoundanalyser/qrc_resources.py ../resources.qrc
pyside-lupdate -verbose pysoundanalyser.pro
lrelease -verbose pysoundanalyser.pro

mv *.qm ../translations/