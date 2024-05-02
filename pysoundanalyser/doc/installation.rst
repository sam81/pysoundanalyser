.. _sec-installation:

************
Installation
************

pysoundanalyser is written in Python and requires the installation of a Python interpreter. Once the Python interpreter has been installed, pysoundanalyser can be installed via pip:

::

   pip install pysoundanalyser


once pysoundanalyser is installed you can launch it from a bash/DOS terminal with the command

::
   
   pysoundanalyser

Note that the program needs to be launched in the same Python environment in which it has been installed. The program has been tested on Linux and Windows. It should work also on Mac computers but this has not been tested. Depending on your Python distribution you may want to install the python modules pysoundanalyser depends on before installing pysoundanalyser (e.g. via the conda package manager if you're using the Anaconda Python distribution). The dependencies are:

- PyQt6 
- numpy 
- scipy 
- pandas 
- matplotlib 
- PyAudio 

if you're using Linux you can also install `pyalsaaudio` to have an addition sound output option. If you're using conda on Windows I'd recommend installing PyAudio via pip because the PyAudio version available on conda is not built with support for the WASAPI output interface (at least that was the case the last time I checked). 


