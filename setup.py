#! /usr/bin/env python
from distutils.core import setup
setup(
    version="0.2.46",
      author="Samuele Carcagno",
      author_email="sam.carcagno@google.com;",
      description="Alpha version of pysoundanalyser, a program for visualizing sounds ",
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
    url="https://samcarcagno.altervista.org/pysoundanalyser/pysoundanalyser.html",
    requires=['PyQt (>=4.8.4)', 'matplotlib (>=1.0.1)', 'numpy (>=1.6.1)', 'scipy (>=0.10.1)'],
    packages=["pysoundanalyser"],
    #py_modules = ['pysndlib'],
    scripts = ["pysoundanalyser.pyw"],
    package_dir={'pysoundanalyser': 'pysoundanalyser'},
    package_data={'pysoundanalyser': ["qrc_resources.py",
                                     "doc/_build/latex/*.pdf",
                                     "doc/_build/html/*.*",
                                     "doc/_build/html/_images/*",
                                     "doc/_build/html/_modules/*",
                                     "doc/_build/html/_sources/*.*",
                                     "doc/_build/html/_sources/_templates/autosummary/*.*",
                                     "doc/_build/html/_sources/_themes/*.*",
                                     "doc/_build/html/_static/*.*",
                                     "doc/_build/html/_static/css/*.*",
                                     "doc/_build/html/_static/font/*.*",
                                     "doc/_build/html/_static/js/*.*",
                                     "doc/_build/html/_templates/autosummary/*.*",
                                     "doc/_build/html/_themes/*.*"],},
    
    data_files = [('share/applications', ['pysoundanalyser.desktop']),
                  ('share/icons', ['icons/johnny_automatic_crashing_wave.svg'])]
    )
