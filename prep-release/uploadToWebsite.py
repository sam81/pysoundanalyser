import ftplib, os, platform

passwd = input('FTP password: ')
session = ftplib.FTP('ftp.samcarcagno.altervista.org', 'samcarcagno', passwd)
session.cwd('pysoundanalyser/builds')


f = open('../setup.py', 'r')
ln = f.readlines()
f.close()
for i in range(len(ln)):
    if ln[i].strip().split('=')[0].strip() == "version":
           ver = ln[i].strip().split('=')[1].strip()
           ver = ver[1:len(ver)-2]
fPaths = ["../dist/pysoundanalyser-" + ver + ".tar.gz",
          "../dist/pysoundanalyser-" + ver + ".zip"]#,
          # "../dist/pysoundanalyser-pyqt4-" + ver + ".tar.gz",
          # "../dist/pysoundanalyser-pyqt4-" + ver + ".zip",
          # "../dist/pysoundanalyser-pyside-" + ver + ".tar.gz",
          # "../dist/pysoundanalyser-pyside-" + ver + ".zip"]
#fPaths = []

for fPath in fPaths:
    print("Uploading: " + fPath)
    fHandle = open(fPath, 'rb')
    session.storbinary("STOR " + fPath.split('/')[2], fHandle)

htmlPagePath = "/media/ntfsShared/lin_home/dc/devel/websites/xoom-website/altervista/pysoundanalyser/pysoundanalyser.html"
fIn = open(htmlPagePath, "r")
lns = fIn.readlines()
fIn.close()


for i in range(len(lns)):
    if lns[i][0:21] == '<li> <a href="builds/':
        if lns[i].split("</a>")[1].strip() == 'Linux/UNIX source package (PyQt5)</li>':
            lns[i] = '<li> <a href="builds/pysoundanalyser-'+ver+'.tar.gz">pysoundanalyser-'+ver+'.tar.gz</a> Linux/UNIX source package (PyQt5)</li>\n'
        elif lns[i].split("</a>")[1].strip() == 'Windows source package (PyQt5)</li>':
            lns[i] = '<li> <a href="builds/pysoundanalyser-'+ver+'.zip">pysoundanalyser-'+ver+'.zip</a> Windows source package (PyQt5)</li>\n'
        # elif lns[i].split("</a>")[1].strip() == 'Linux/UNIX source package (PyQt4)</li>':
        #     lns[i] = '<li> <a href="builds/pysoundanalyser-pyqt4-'+ver+'.tar.gz">pysoundanalyser-pyqt4-'+ver+'.tar.gz</a> Linux/UNIX source package (PyQt4)</li>\n'
        # elif lns[i].split("</a>")[1].strip() == 'Windows source package (PyQt4)</li>':
        #     lns[i] = '<li> <a href="builds/pysoundanalyser-pyqt4-'+ver+'.zip">pysoundanalyser-pyqt4-'+ver+'.zip</a> Windows source package (PyQt4)</li>\n'
        # elif lns[i].split("</a>")[1].strip() == 'Linux/UNIX source package (PySide)</li>':
        #     lns[i] = '<li> <a href="builds/pysoundanalyser-pyside-'+ver+'.tar.gz">pysoundanalyser-pyside-'+ver+'.tar.gz</a> Linux/UNIX source package (PySide)</li>\n'
        # elif lns[i].split("</a>")[1].strip() == 'Windows source package (PySide)</li>':
        #     lns[i] = '<li> <a href="builds/pysoundanalyser-pyside-'+ver+'.zip">pysoundanalyser-pyside-'+ver+'.zip</a> Windows source package (PySide)</li>\n'
        
fOut = open(htmlPagePath, 'w')
fOut.writelines(lns)
fOut.close()

session.cwd('../')
fHandle = open(htmlPagePath, 'rb')
session.storbinary("STOR " + "pysoundanalyser.html", fHandle)
