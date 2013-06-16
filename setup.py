#! /usr/bin/env python
from distutils.core import setup
setup(
    version="0.1.16",
      author="Samuele Carcagno",
      author_email="sam.carcagno@google.com;",
      description="Alpha Version of pysoundanalyser, a program for visualizing sounds ",
      long_description=\
"""
Alpha Version of pysoundanalyser, a program for visualizing sounds
""",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Console',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python :: 3',
        'Topic :: Scientific/Engineering :: Bio-Informatics'
        ],
    license="GPL v3",
    name="pysoundanalyser",
    url="none",
    requires=['PyQt (>=4.8.4)', 'matplotlib (>=1.0.1)', 'numpy (>=1.6.1)', 'scipy (>=0.10.1)'],
    packages=["pysoundanalyser_pack"],
    py_modules = ['pysndlib'],
    scripts = ["pysoundanalyser.pyw", "postinstall.py"],
    package_dir={'pysoundanalyser_pack': 'pysoundanalyser_pack'},
    package_data={'pysoundanalyser_pack': ['doc/*.pdf']},
    data_files = [('share/applications', ['pysoundanalyser.desktop']),
                  ('share/icons', ['icons/johnny_automatic_crashing_wave.svg'])]
    )
