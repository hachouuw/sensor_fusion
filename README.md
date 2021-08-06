# sensor_fusion

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