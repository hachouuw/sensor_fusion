# # ---- EMG raw data collection
# def EMGrawData():
#   ThreeData = joy.receiveArduinoData()
#   return ThreeData

#   # ThreeData = joy.receiveArduinoData()
#   # EMGrealtime = [time.time()]
#   # EMG1Data = [ThreeData[0]]
#   # EMG2Data = [ThreeData[1]]
#   # SliderData = [ThreeData[2]]
# # if COM_PORT is not None:
# #     # print(joy.receiveArduinoData())
# #     EMGrealtime.append(time.time())
# #     ThreeData = joy.receiveArduinoData()
# #     # ThreeData.append(joy.receiveArduinoData())
# #     EMG1Data.append(ThreeData[0])
# #     EMG2Data.append(ThreeData[1])
# #     SliderData.append(ThreeData[2])
   



# from threading import Thread

# def func1():
#     print('Working')

# def func2():
#     print("Working")

# if __name__ == '__main__':
#     Thread(target = func1).start()
#     Thread(target = func2).start()
import sys
print(sys.version)
print(sys.executable)

# # sys.path.append('C:\\Users\\amber\\Documents\\VSCode\\basic\\protocols')

# # pip install numpy
# # pip install -U matplotlib 

import numpy as np
# print(np.__version__)

from scipy.signal import detrend
from collections import deque
import itertools

data = np.linspace(100,110,num = 1000)
window = 10
data1 = detrend(deque(itertools.islice(data,
                    int(len(data)-window*2),
                    int(len(data)-window))),
                    axis=0,type='linear')
data2 = detrend(deque(itertools.islice(data,
                    int(len(data)-(window)),
                    int(len(data)))),
                    axis=0,type='linear')

input1 = np.mean(abs(data1[-window*2:]))
print(data1)


# import numpy as np
# import matplotlib.pyplot as plt

# x = np.linspace(0, 20, 100)  # Create a list of evenly-spaced numbers over the range
# plt.plot(x, np.sin(x))       # Plot the sine of each x point
# plt.show()                   # Display the plot



# import IPython
# IPython.embed()



#!/usr/bin/python


# import numpy as np 

# print("Hello world")
