#! /usr/bin/env python
# -*- coding: utf-8 -*-

import ftplib, os, platform, requests, time
publish = input("publish ('y'/'n')?: ")

winpythonpath = "pysoundanalyser_for_win/"

f = open('../setup.py', 'r')
ln = f.readlines()
f.close()
for i in range(len(ln)):
    if ln[i].strip().split('=')[0].strip() == "version":
           ver = ln[i].strip().split('=')[1].strip()
           ver = ver[1:len(ver)-2]

zippath = "../dist/pysoundanalyser-"+ver+".zip"
           
#remove previous version
cmd = "rm -r " + winpythonpath + "pysoundanalyser/"
os.system(cmd)
#unzip new version
cmd = "unzip -d " + winpythonpath + " -x " + zippath
os.system(cmd)
#rename to pysoundanalyser
cmd = "mv " + winpythonpath+"pysoundanalyser-"+ver + " " + winpythonpath+"pysoundanalyser"
os.system(cmd)

#change iss version name
fIn = open("pysoundanalyser.iss", "r")
lns = fIn.readlines()
fIn.close()

for i in range(len(lns)):
    if lns[i][0:20] == "#define MyAppVersion":
        tmp = lns[4].split(" ")
        tmp.pop()
        tmp.append('"'+ver+'"\n')
        lns[i] = " ".join(tmp)

fIn = open("pysoundanalyser.iss", "w")
lns = fIn.writelines(lns)
fIn.close()

cmd = "./compile_win.sh"
os.system(cmd)


#####################
# Publish on Bintray
#####################

package = "pysoundanalyser"
exeName = "pysoundanalyser_"+ver+"-setup.exe"
exePath = "Output/"+exeName


if publish == 1 or publish == "y":
    print("###############################")
    print("Publishing")
    print("###############################")
    API_KEY = os.environ["BINTRAY_API_KEY"]

    USERNAME = "sam81"

    #URL = "https://api.bintray.com/content/sam81/hearinglab-win/"+ package + "/" + ver + "/pysoundanalyser_" + ver + "/" + exeName + "?publish=1"
    URL = "https://api.bintray.com/content/sam81/hearinglab-win/"+ "/pysoundanalyser_" + ver + "/" + exeName + "?publish=1"
    parameters = {"publish": "1"}
    headers = {
        "X-Bintray-Package": "pysoundanalyser",
        "X-Bintray-Version": ver
    }

    with open(exePath, "rb") as package_fp:
        response = requests.put(
            URL, auth=(USERNAME, API_KEY), params=parameters,
            headers=headers, data=package_fp) 

    print("status code: " + str(response.status_code))
    if response.status_code == 201:
        print("#####################\n Upload successful!")
    else:
        print("#####################\n Upload Unsuccessful.")

    htmlPagePath = "/media/ntfsShared/lin_home/dc/devel/websites/xoom-website/xoom/pysoundanalyser/pysoundanalyser.html"
    fIn = open(htmlPagePath, "r")
    lns = fIn.readlines()
    fIn.close()

    for i in range(len(lns)):
        if lns[i][0:73] == '<li> <a href="https://bintray.com/artifact/download/sam81/hearinglab-win/':
            lns[i] = '<li> <a href="https://bintray.com/artifact/download/sam81/hearinglab-win/pysoundanalyser_'+ver+'/pysoundanalyser_'+ver+'-setup.exe">pysoundanalyser_'+ver+'-setup.exe</a> Windows installer (experimental) </li>'

    fOut = open(htmlPagePath, 'w')
    fOut.writelines(lns)
    fOut.close()

    passwd = input('FTP password: ')
    session = ftplib.FTP('ftp.samcarcagno.altervista.org', 'samcarcagno', passwd)
    session.cwd('pysoundanalyser/')

    fHandle = open(htmlPagePath, 'rb')
    session.storbinary("STOR " + "pysoundanalyser.html", fHandle)
            

else:
    print("###############################")
    print("Not Publishing")
    print("###############################")
     
