import serial
import time
import numpy as np

encoding = 'ascii'
data = np.array([])
# set up the serial line
arduinoSerial = serial.Serial('COM3', baudrate = 9600,timeout=0.1)
time.sleep(2)

arduinoSerial.write(bytearray('g',encoding))

b = arduinoSerial.readline()
string_n = b.decode()
string = string_n.rstrip()
data = float(string)
print(data)

# Read and record the data
# data =[]                       # empty list to store the data
# for i in range(50):

#     b = arduinoSerial.readline()         # read a byte string
#     a = b.decode()  # decode byte string into Unicode  
#     # string = string_n.rstrip() # remove \n and \r
#     flt = float(a[0:4])        # convert string to float
#     print(flt)
#     data.append(flt)           # add to the end of data list
#     time.sleep(0.1)            # wait (sleep) 0.1 seconds

# ser.close()