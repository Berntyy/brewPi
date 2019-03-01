# REading temp
from subprocess import check_output
from re import findall
from time import sleep, strftime, time
import matplotlib.pyplot as plt
import RPi.GPIO as GPIO
import signal
import sys
import os


plt.ion()
x = []
y = []
pin = 12 # GPIO to activate fan
maxTMP = 50

def setup():
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(pin, GPIO.OUT)
    p = GPIO.PWM(pin, 60)
    p.start(100)
    return()

def get_temp():
    temp = check_output(["vcgencmd","measure_temp"]).decode("UTF-8")
    temp = float(findall("\d+\.\d+",temp)[0])
    return(temp)
def fanON():
    p = setPWM(50)
    p.start(0)
    sleep(0.1)
    return()
def fanOFF():
    p = setPWM(0)
    sleep(0.1)
    p.stop()
    return()
def controlFan():
    temp = get_temp()
    print(temp)
    if temp > maxTMP:
        fanON()
        print("Fan oN")
    else:
        fanOFF()
    return()
def setPWM(freq):
    p = GPIO.PWM(pin,freq)
    return p
def write_temp(temp):
    with open("cpu_temp.csv","a") as log:
        log.write("{0},{1}\n".format(strftime("%Y-%m-%d %H:%M:%S"),str(temp)))

def graph(temp):
    y.append(temp)
    x.append(time())
    plt.clf()
    plt.scatter(x,y)
    plt.plot(x,y)
    plt.draw()
try:
    setup()
    #while True:
       # temp = get_temp()
        #write_temp(temp)
        #graph(temp)
    #while True:
        #controlFan()
        #sleep(2)
        #temp = get_temp()
        #write_temp(temp)
        #graph(temp)
        #sleep(1)
    
except KeyboardInterrupt:
    fanOFF()
    GPIO.cleanup()

