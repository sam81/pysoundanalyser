.. _sec-user_interface:

****************
User Interface
****************

- **Load Sound** The ``Load Sound`` button allows you to load a wav file into the program. Currently only 16, 24, and 32 bit wav files with one or two channels are supported. Note that the entire wav file is loaded in memory, this is fine and fast for wav files of short duration (tens of seconds), but longer sound files are going to consume huge amounts of RAM and may even halt your computer. If you need to work on long sound files, please use other software, like audacity.  

  - **Save As** The ``Save As`` button allows you to save PSA sound objects as wav files. Currently it is only possible to save sounds as 16, 24, or 32 bit wav files with one or two channels. If you choose a mono (1-channel) format, and multiple PSA sound objects have been selected for saving, they will be summed together before saving. If you choose a stereo (2-channels) format, "right" and "left" PSA sound objects will be saved to their respective channels in the wav file; if multiple "right" or "left" PSA sound objects have been selected, they will be summed before saving.

- **Clone Sound**
      
- **Concatenate**
  
- **Cut** The ``Cut`` button allows you to remove segments of a sound waveform. The starting and ending points of the segments to be cut off can be specified in seconds, milliseconds, or sample numbers. When working with sample numbers, note that PSA indexing works exactly like numpy indexing. Examples:


  .. code-block:: python
		
     >>> import numpy as np #import numpy
     >>> sig = np.arange(10) #generate a 10-elements array
     >>> x[0:5] #Select the first five samples, indexing starts from 0
     array([0, 1, 2, 3, 4])
     >>> sig[7:10] #select last 3 samples
     array([7, 8, 9])
     >>> sig[1:3] #select the second and third sample
     array([1, 2])
     >>> sig[1:2] #select the second sample
     array([1])
     >>> sig[1:1] #note that if the start and end point are the same nothing is selected
     array([], dtype=int64)
 
- **Play** The ``Play`` button allows playback of the currently selected sound.

- **Plot Waveform** The ``Plot Wavform`` button allows you to plot the waveform of the currently selected sound.
    
- **Spectrum** Plot the spectrum of the currently selected sound.
    
- **Spectrogram** Plot the spectrogram of the currently selected sound.

- **Autocorrelation** Plot the autocorrelation function of the currently selected sound.

- **Autocorrelogram** Plot the autocorrelogram of the currently selected sound.

- **Level Difference** Show the difference in level between two selected sounds.

- **Scale** Change the level of the currently selected sound.

- **Resample** Resample the currently selected sound.

- **Rename** Rename the currently selected sound.

- **Remove** Remove the currently selected sound from the workspace.

- **Remove All** Remove all sounds from the workspace.
