##############
## GUI MESH ##
##############

import PID
import time
import matplotlib.pyplot as plt
import numpy as np
import signal
import sys
import os
from measuretemp import get_temp
import RPi.GPIO as GPIO
import random # Random temp input
from time import strftime

class mesh(object):
    ''' Requires PID file'''

    def __init__(self, P, I, D, relayPin, WindowSize, temp):
        self.P = P
        self.I = I
        self.D = D
        self.relayPin = relayPin
        self.WindowSize = WindowSize
        self.temp = temp
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(relayPin, GPIO.OUT)

    def regulator(self):
        self.pid = PID.PID(self.P, self.I, self.D) # Start PID funksjon

        # Config pid
        self.pid.setPoint = 23
        self.pid.setSampleTime(0.1)
        self.pid.setOutputLim(0.01,10)
        self.pid.setWindup(20)

        self.winStartTime = time.time()

        # Update PID and calculate output
        self.pid.pid_update(self.temp)
        self.output = self.pid.output
        if(time.time() - self.winStartTime > self.WindowSize):
            self.winStartTime += self.WindowSize
        if(self.output < time.time() - self.winStartTime):
            self.logic = 1
            GPIO(self.relayPin, True)
        else:
            self.logic = 0
            GPIO(self.relayPin, False)
        # Write to .csv file with time, temp and logic relay
        with open("mesh_temp.csv", "a") as log:
            log.write("{0},{1},{2}\n".format(strftime("%Y-%m-%d %H:%M:%S"),str(self.temp),str(self.logic)))
        return self.logic,self.output
