# Written By: Terry Tse
#!/usr/bin/env python3


import RPi.GPIO as GPIO
import time
import datetime

#Relay Pin
RelayPin1 = 22
RelayPin2 = 27    

# Setup GPIO.
def setup():
	GPIO.setmode(GPIO.BCM)

	# Relay #1
	GPIO.setup(RelayPin1, GPIO.OUT)
        GPIO.output(RelayPin1, GPIO.HIGH)
	# Relay #2
        GPIO.setup(RelayPin2, GPIO.OUT)
        GPIO.output(RelayPin2, GPIO.HIGH)

        GPIO.setwarnings(False)

def reset_relay():
        GPIO.output(RelayPin1, GPIO.LOW)
        GPIO.output(RelayPin2, GPIO.LOW)
	
def destroy():
	GPIO.cleanup()

if __name__ == "__main__":
	setup()
	reset_relay()
	#destroy()
