-- UPDATED 2021/5/24 Amber Chou

1. create virtual environment for python 3.5.4, [your path] -m venv venv35, for example:
$ /Users/amber/AppData/Local/Programs/Python/Python35/python.exe -m venv venv35
and then activate the virtual environment
venv35\Scripts\activate.bat

2. install correct versions of packages
$ pip install numpy==1.14.3
$ pip install -U matplotlib 
$ pip install ipython==6.1.0
$ pip install pygame==1.9.2
$ pip install pyserial==3.2.1

3. change to hcps directory, for example: 
$ cd /path/to/hcps/directory

4. start ipython:
$ ipython
alternative: 
$ python
$ python -m IPython
or:
$ import IPython
$ IPython.embed()

5. run experiment
In [1]: run experiment subject protocol port 
for example: run experimentPython3 subject0 su19fo

(Note: if using keyboard, press down to start the game, and then use left and right to control the diamond)


-- UPDATED 2021/7/1 Amber Chou
(Note: comment out lines su18CP in __init__.py)

-  run experiment with sliderino
In [1]: run experiment subject protocol port 
for example: run experimentPython3 subject0 su19fo COM3

-  run experiment with SpikerShields EMG
run experimentPython3 subject0 su19fo COM3

-- UPDATED 2021/7/12 Amber Chou
*** EMG calibration code adapted from expCHI.py
*** python-Arduno communication code adapted from https://thepoorengineer.com/en/arduino-python-plot/#combine

Updated these files to run the SpikerShields EMG via Arduino Uno:
1. sliderPython3.py (original code in the same file for reference) 
2. experimentPython3.py (changes from line 231-245 for the rescale_inp)
3. silderino.ino code saved in sliderino_EMG_only (original code saved in sliderino_original for reference)

Note that these code also works for slider via Arduino Uno, with changes in all three files: 
1. sliderPython3.py line 53; 
2. experimentPython3.py line 235; 
3. silderino code saved in sliderino_slider_only

-- UPDATED 2021/7/22 Amber Chou, sensori-fusion code

Process:
1. change sliderPython3.py line 20 & 22 (COM and where to save EMGcalibration.txt)
2. run sliderPython3.py and do the calibration
3. run pygame

Note: if would like to check EMG value, can uncommon line 113 (scaled data) or line 93 (raw data), and run sliderPython3.py for data collection process.
