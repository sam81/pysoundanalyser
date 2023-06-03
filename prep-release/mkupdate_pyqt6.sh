#!/usr/bin/env bash


pylupdate6 --verbose --ts pysoundanalyser_de.ts --ts pysoundanalyser_el.ts --ts pysoundanalyser_en_GB.ts --ts pysoundanalyser_es.ts --ts pysoundanalyser_fr.ts --ts pysoundanalyser_it.ts --ts pysoundanalyser_ru.ts ../pysoundanalyser/__main__.py ../pysoundanalyser/dialog_apply_filter.py ../pysoundanalyser/dialog_change_channel.py ../pysoundanalyser/dialog_concatenate.py ../pysoundanalyser/dialog_edit_preferences.py ../pysoundanalyser/dialog_generate_noise.py ../pysoundanalyser/dialog_generate_sound.py ../pysoundanalyser/dialog_generate_sinusoid.py ../pysoundanalyser/dialog_resample.py ../pysoundanalyser/dialog_save_sound.py ../pysoundanalyser/random_id.py ../pysoundanalyser/utility_functions.py ../pysoundanalyser/win_acf_plot.py ../pysoundanalyser/win_autocorrelogram_plot.py ../pysoundanalyser/win_spectrogram_plot.py ../pysoundanalyser/win_spectrum_plot.py ../pysoundanalyser/win_waveform_plot.py ../pysoundanalyser/sndlib.py

lrelease -verbose pysoundanalyser.pro

mv *.qm ../translations/

rcc -g python ../resources.qrc | sed '0,/PySide2/s//PyQt6/' > ../pysoundanalyser/qrc_resources.py
