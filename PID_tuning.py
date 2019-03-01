################
## PID TUNING ##
################

import MCP3008 # For reading the temperature
import RPi.GPI as GPIO
import pid

# Define the variables for the PID class in pid.py
float Ki

# Define the agressive and conservative Tuning parameters
float aggKp = 10, aggKi = 0.1, aggKd = 1
float consKp = 1, consKi = 0.01, consKd = 0.25

# Specify the links for pid
pid.pid()

def setup():
	temp = readADC() # Read the temperature
	SetPoint = 100

	##### TURN ON PID

def main():
	setup()
	temp = readADC()

	float gap = abs(SetPoint - temp) # Distance
	if(gap<10):
		pid.SetTuning(consKp, consKi, consKd)
	else:
		pid.SetTuning(aggKp, aggKi, aggKd)
