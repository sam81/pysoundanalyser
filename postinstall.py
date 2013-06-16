#!/usr/bin/env python
# -*- coding: utf-8 -*-
import os
import sys

if sys.argv[1] == '-install':
    #find python installation directory
    python_dir = sys.prefix
    # Path to pythonw.exe the executable for GUI applications (no console)
    pyw_path = os.path.abspath(os.path.join(python_dir, 'pythonw.exe'))
    # 
    script_dir = os.path.abspath(os.path.join(python_dir, 'Scripts'))

    ico_path = os.path.join(python_dir, 'Lib/site-packages/pysoundanalyser_pack/icons/johnny_automatic_crashing_wave.ico')
    script_path = os.path.join(script_dir, 'pysoundanalyser.pyw')
    
    try:
        desktop_path = get_special_folder_path("CSIDL_COMMON_DESKTOPDIRECTORY")
    except OSError:
        desktop_path = get_special_folder_path("CSIDL_DESKTOPDIRECTORY")
    

    create_shortcut(pyw_path, # programme à lancer
                    "psychoacoustics experiments platform", # Description
                    os.path.join(desktop_path, 'pysoundanalyser.lnk'), 
                    script_path, 
                    desktop_path,
                    ico_path)
  
    file_created(os.path.join(desktop_path, 'pysoundanalyser.lnk'))
    
    try:
        start_path = get_special_folder_path("CSIDL_COMMON_PROGRAMS")
    except OSError:
        start_path = get_special_folder_path("CSIDL_PROGRAMS")
    

    programs_path = os.path.join(start_path, "pysoundanalyser")
    try :
        os.mkdir(programs_path)
        directory_created(programs_path)
    except OSError:
        pass
    
    
    
    create_shortcut(pyw_path, # 
                    "psychoacoustics experiments platform", #Description
                    os.path.join(programs_path, 'pysoundanalyser.lnk'),  
                    script_path, # Argument
                    desktop_path,
                    ico_path) # Working directory
                    
    file_created(os.path.join(programs_path, 'pysoundanalyser.lnk'))
    
 
    #sys.stdout.write("Shortcuts created.")
    sys.exit()
