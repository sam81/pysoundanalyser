from cx_Freeze import setup, Executable

# Dependencies are automatically detected, but it might need
# fine tuning.
build_options = {'packages': ['pysoundanalyser'],
                 'excludes': ['tkinter',
                              'PyQt5.QtQml',
                              'PyQt5.QtBluetooth',
                              'PyQt5.QtQuickWidgets',
                              'PyQt5.QtSensors',
                              'PyQt5.QtSerialPort',
                              'PyQt5.QtSql'
                              ]}


import sys
base = 'Win32GUI' if sys.platform=='win32' else None

executables = [
    Executable('pysoundanalyser\\__main__.py',
               base=base,
               target_name = 'pysoundanalyser',
               icon='icons/johnny_automatic_crashing_wave.ico')
]

setup(name='pysoundanalyser',
    version="0.3.4",
      description = '',
      options = {'build_exe': build_options},
      executables = executables)
