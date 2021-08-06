#sliderpython3 sensor fusion code
#!/usr/bin/env python

from threading import Thread
import os.path
import serial
import time
import collections
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import struct
import copy
import pandas as pd
import numpy as np
import csv as csv_
from collections import deque

#Need to change:
#(1) where to save EMG calibration data
cal_dir = os.path.join('C:/Users/amber/OneDrive/Documents/VSCode/basic/calibration','EMGcalibration.txt')
#(2) COM port
COM_PORT = 'COM4'
#(3) slider min and max value (raw data)
SLIDER_MIN = 0.
SLIDER_MAX = 672. #4096.

numPlots = 3 #number of inputs

class slider:
    def __init__(self, port=COM_PORT, serialBaud = 115200, plotLength = 100, dataNumBytes = 4):
        self.port = port
        self.baud = serialBaud
        self.plotMaxLength = plotLength
        self.dataNumBytes = dataNumBytes
        self.numPlots = numPlots
        self.rawData = bytearray(numPlots * dataNumBytes)
        self.dataType = None
        if dataNumBytes == 2:
            self.dataType = 'h'     # 2 byte integer
        elif dataNumBytes == 4:
            self.dataType = 'f'     # 4 byte float
        self.data = []
        self.datafused = np.array([]) #fused data
        for i in range(numPlots):   # give an array for each type of data and store them in a list
            self.data.append(collections.deque([0] * plotLength, maxlen=plotLength))
        self.isRun = True
        self.isReceiving = False
        self.thread = None
        self.plotTimer = 0
        self.previousTimer = 0
        # self.csvData = []

        print('Trying to connect to: ' + str(port) + ' at ' + str(serialBaud) + ' BAUD.')
        try:
            self.serialConnection = serial.Serial(port, serialBaud, timeout=4)
            print('Connected to ' + str(port) + ' at ' + str(serialBaud) + ' BAUD.')
        except:
            print("Failed to connect with " + str(port) + ' at ' + str(serialBaud) + ' BAUD.')

    def startArduino(self): #read serial start
        if self.thread == None:
            self.thread = Thread(target=self.backgroundThread)
            self.thread.start()
            # Block till we start receiving values
            while self.isReceiving != True:
                time.sleep(0.1)
    
    def receiveArduinoData(self): 
        currentTimer = time.perf_counter()
        self.plotTimer = int((currentTimer - self.previousTimer) * 1000)     # the first reading will be erroneous
        self.previousTimer = currentTimer
        #for 1 data only:
        # value,  = struct.unpack('f', self.rawData)    # use 'h' for a 2 byte integer
        # self.data = value*100 # for slider
        # self.data = round(value) +78     # for EMG2, 25 is relax data, for EMG1 - 16
        # if ((self.data < 2) and (self.data > -2)):
        #     self.data = 0
        # print(self.data)

        #try slider only:
        # data = self.rawData[(2*self.dataNumBytes):(self.dataNumBytes + 2*self.dataNumBytes)]
        # value,  = struct.unpack(self.dataType, data)
        # self.data[i] = value

        #3 data:
        # privateData = copy.deepcopy(self.rawData[:])    # so that the 3 values in our plots will be synchronized to the same sample time
        for i in range(self.numPlots):
            data = self.rawData[(i*self.dataNumBytes):(self.dataNumBytes + i*self.dataNumBytes)]
            value,  = struct.unpack(self.dataType, data)
            self.data[i] = value
            # self.data[i].append(value)    # we get the latest data point and append it to our array

        # print(self.data[0],self.data[1],self.data[2]) #Debug

        return self.data

    def grabData(self):

        #(1) receive 3 data from Arduino
        self.receiveArduinoData()

        #(2) scale slider data
        slider_scaled = self.rescale_inp()

        #(3) scale EMG data
        EMG_scaled = self.rescale_inp_EMG()

        #(4) fuse 3 data
        self.datafused = 0.5*(slider_scaled + EMG_scaled) #senor fusion
        # self.datafused = EMG_scaled #EMG only
        # self.datafused = slider_scaled #slider only

        # print(self.datafused) #Debug

        return self.datafused
    
    def rescale_inp(self,MIN=SLIDER_MIN,MAX=SLIDER_MAX): 
        inp = self.data[2]
        return 255*((float(inp) - MIN) / (MAX - MIN)) - 127.5 #-127.5~127.5
        # return 2 * ( (inp - MIN) / (MAX - MIN) - .5) * trial['scale'] * (3./2.)

    def rescale_inp_EMG(self): 
        thresh = 0.025 # threshold is 2% of MVIC
        
        EMG_calibration = np.loadtxt(cal_dir)
        MIN_1 = EMG_calibration[0,0]
        MIN_2 = EMG_calibration[1,0]
        MAX_1 = EMG_calibration[0,1]
        MAX_2 = EMG_calibration[1,1]

        inp1 = self.data[0] #A0, EMG 1 
        inp2 = self.data[1] #A1, EMG 2
        scaled_1 = 127*(float(inp1) - MIN_1) / (MAX_1 - MIN_1)
        scaled_2 = 127*(float(inp2) - MIN_2) / (MAX_2 - MIN_2)
        # scaled_1 = inp1/MAX_1 * 4 #(inp1 - MIN_1) / (MAX_1 - MIN_1)
        # scaled_2 = inp2/MAX_2 * 4 #(inp2 - MIN_2) / (MAX_2 - MIN_2)

        if (inp1 < thresh*MAX_1) & (inp2 < thresh*MAX_2):
            return 0
        elif scaled_1 > scaled_2:
            scaled = scaled_1
        elif scaled_2 > scaled_1:
            scaled = -scaled_2
        else:
            print('error')

        return scaled #-127.5~127.5
        #return   2 * scaled * trial['scale'] * (3./2.) #(scaled) * trial['scale'] #* 1/2 #2

    def backgroundThread(self):    # retrieve data
        time.sleep(1.0)  # give some buffer time for retrieving data
        self.serialConnection.reset_input_buffer()
        while (self.isRun):
            self.serialConnection.readinto(self.rawData)
            self.isReceiving = True
            #print(self.rawData)

    def close(self):
        self.isRun = False
        self.thread.join()
        self.serialConnection.close()
        print('Disconnected...')
        # df = pd.DataFrame(self.csvData)
        # df.to_csv('/home/rikisenia/Desktop/data.csv')

def main():
    cmd_initial = input('Press 1 to start calibration process;Press enter to start data collection: ')
    if cmd_initial != "":
        sliderJoystick = slider(port = COM_PORT)   # initializes all required variables
        sliderJoystick.startArduino()              # starts background thread
        cmd = input('Press enter to start max_1 calibration (2-sec): ')
        if cmd != "":
            EMG_MAX_1 = float(cmd)
        else:
            calibration_num = 3
            save_calibration = np.zeros((calibration_num,))
            for num in range(calibration_num):
                cmd = input('Press enter to start max_1 calibration (2-sec): ')
                calibration = []
                t_end = time.time() + 2 # in 2 seconds
                while time.time() < t_end:
                    EMG1Data = sliderJoystick.receiveArduinoData() #A0, EMG 1
                    calibration.append(EMG1Data[0]) 
                save_calibration[num] = np.percentile(calibration,95)# calculate 95th percentile 
                
            EMG_MAX_1 = np.mean(save_calibration)
            print(EMG_MAX_1)
            # np.savetxt('calibration_max_1.csv',calibration,delimiter=',')

        cmd = input('Press enter to start max_2 calibration (2-sec): ')
        if cmd != '':
            EMG_MAX_2 = float(cmd)
        else:
            calibration_num = 3
            save_calibration = np.zeros((calibration_num,))
            for num in range(calibration_num):
                cmd = input('Press enter to start max_2 calibration (2-sec): ')
                calibration = []
                t_end = time.time() + 2 # in 2 seconds
                while time.time() < t_end:
                    EMG2Data = sliderJoystick.receiveArduinoData() #A1, EMG 2
                    calibration.append(EMG2Data[1])            
                save_calibration[num] = np.percentile(calibration,95) # calculate 95th percentile 

            EMG_MAX_2 = np.mean(save_calibration)
            print(EMG_MAX_2)
            # np.savetxt('calibration_max_2.csv',calibration,delimiter=',')

        cmd = input('Press enter to start relaxing (5-sec): ')
        if cmd != '':
            EMG_MIN_1 = float(cmd)
            EMG_MIN_2 = float(cmd)
        else:
            relax1 = []
            relax2 = []
            t_end = time.time() + 5 # in 5 seconds
            while time.time() < t_end:
                EMG1relax = sliderJoystick.receiveArduinoData()[0] #A0, EMG 1
                EMG2relax = sliderJoystick.receiveArduinoData()[1] #A1, EMG 2
                relax1.append(EMG1relax)    
                relax2.append(EMG2relax)        
            EMG_MIN_1 = np.mean(relax1)
            EMG_MIN_2 = np.mean(relax2)
            print(EMG_MIN_1,EMG_MIN_2)
            # np.savetxt('calibration_max_2.csv',calibration,delimiter=',')

        EMG_calibration = (np.asarray([[EMG_MIN_1,EMG_MAX_1],[EMG_MIN_2,EMG_MAX_2]]))
        
        np.savetxt(cal_dir, EMG_calibration)
    
        sliderJoystick.close()
    
    else:
        sliderJoystick = slider(port = COM_PORT)   # initializes all required variables
        sliderJoystick.startArduino()              # starts background thread

        t_end = time.time() + 10 # in 10 seconds
        while time.time() < t_end:
            sliderJoystick.grabData()
            # sliderJoystick.receiveArduinoData()
            
        sliderJoystick.close()
        
    # sliderJoystick = slider(port = COM_PORT)   # initializes all required variables
    # sliderJoystick.startArduino()              # starts background thread
    
    # for n in range(0,200): #200, so 4 seconds
    #     sliderJoystick.grabData()     #or append it to your other data or whatever
    #     time.sleep(1./50.) #20ms

    # sliderJoystick.close()


if __name__ == '__main__':
    main()

## Original code from Momona

# #!/usr/bin/python
# # -*- coding: utf-8 -*-

# import serial
# from time import sleep
# import numpy as np
# import struct
# import serial.tools.list_ports

# COM_PORT = 'COM3'
# # COM_PORT = '/dev/tty.usbmodem141121'

# encoding = 'ascii'

# class slider():

#     def __init__(self, port=COM_PORT, debugMode = True, dataNumBytes = 4):

#         self.arduinoSerial = serial.Serial(port = port, baudrate = 115200,
#         timeout=0.1)
#         # bytesize=serial.EIGHTBITS)
#         self.dataNumBytes = dataNumBytes
#         self.rawData = bytearray(dataNumBytes)
#         self.data = np.array([])
#         self.debugMode = debugMode


#     def __del__(self):
#         self.clearUSBRecBuffer()

#     def clearUSBRecBuffer(self):
#         while (self.arduinoSerial.inWaiting()):
#             self.arduinoSerial.read()
#         if self.debugMode:
#             print ('USB received buffer cleared\n')

#     def startArduino(self):
#         self.stopArduino()
#         self.clearUSBRecBuffer()
#         self.arduinoSerial.write(bytearray('a',encoding))
#         if self.debugMode:
#             print ('Arduino started.\n')

#     def stopArduino(self):
#         self.arduinoSerial.write(bytearray('A',encoding))
#         if self.debugMode:
#             print ('Arduino stopped.\n')
    
    

#     def grabData(self):
#         self.arduinoSerial.write(bytearray('g',encoding))

#         while(self.arduinoSerial.inWaiting()<8):
#             pass

#         # self.data, = struct.unpack('h', self.rawData) #usse 'f' as 4 byte float; 'h' as 2 byte int
#         self.data = struct.unpack('<fI', self.arduinoSerial.read(8))
#         return self.data


# if __name__ == '__main__':
#     #arduinoPorts = [p.device
#     #for p in serial.tools.list_ports.comports()
#     #if 'Arduino' in p.description
#     #]

#     sliderJoystick = slider(port=COM_PORT)

#     sliderJoystick.startArduino()
#     print ('phase 1')
#     for n in range(0,10): #200
#         print (sliderJoystick.grabData())     #or append it to your other data or whatever
#         sleep(1./50.)
#     # print(sliderJoystick.grabData())

#     # sliderJoystick.grabData()

#     # print((sliderJoystick.grabData()[1]))
#     # sliderJoystick.rescale_inp(sliderJoystick.grabData()[1])

#     #sleep(3)
#     #print('Slept Some')

#     #for n in range(0,20):
#     #    print sliderJoystick.grabData()

#     sliderJoystick.stopArduino()


#     # sleep(5)
#     # # sleep(2.5)
#     # # print sliderJoystick.grabData()
#     # # sleep(2.5)
#     # print 'phase2'
#     # sliderJoystick.startArduino()
#     # for n in range(0,1000):
#     #     print sliderJoystick.grabData()     #or append it to your other data or whatever
#     # sliderJoystick.stopArduino()