#!/usr/bin/env python3
# Date Written : 30-Dec-2019
# Written By: Terry Tse

import RPi.GPIO as GPIO
import time
import datetime
import sys
import os

#Ultrasonic PINs
TRIG1 = 11
ECHO1 = 12
TRIG2 = 16
ECHO2 = 18

#Relay Pin
RelayPin1 = 13    # pin13
RelayPin2 = 15    # pin15
dist01 = 10    # 180cm / 70inches
dist02 = 10    # 180cm / 70inches

# File Buffer Size
bufsize = 0

T1_engaged = 0
T2_engaged = 0

# The following parameters is used to check the object, if it is stay in front of the ultrasonic sensor.
# Them, the system will trigger the relay switch.
chk_T1_again = 0
chk_T2_again = 0
# How many seconds will trigger the relay.
num_of_secs = 3

# Setup GPIO.
def setup():
	GPIO.setmode(GPIO.BOARD)
	# Ultrasonic Sensor #1

	GPIO.setup(TRIG1, GPIO.OUT)
	GPIO.setup(ECHO1, GPIO.IN)
	# Ultrasonic Sensor #2
	GPIO.setup(TRIG2, GPIO.OUT)
	GPIO.setup(ECHO2, GPIO.IN)

	# Relay #1
	GPIO.setup(RelayPin1, GPIO.OUT)
        GPIO.output(RelayPin1, GPIO.HIGH)
        # Relay #2
        GPIO.setup(RelayPin2, GPIO.OUT)
        GPIO.output(RelayPin2, GPIO.HIGH)

        GPIO.setwarnings(False)

# Ultrasonic Sensor Checking Distance
# Ultrasonic Sensor #1
def distance_s1():
	GPIO.output(TRIG1, True)
	time.sleep(0.0001)
	GPIO.output(TRIG1, False)
	time.sleep(0.0001)
	start = time.time()
	
	while GPIO.input(ECHO1) == 0:
	     start = time.time()
	while GPIO.input(ECHO1) == 1:
	     stop = time.time()

	elapsed = stop - start
	#distance = (elapsed * 34300)/2
	distance = elapsed
	return distance

# Ultrasonic Sensor #2
def distance_s2():
	GPIO.output(TRIG2, True)
	time.sleep(0.00001)
	GPIO.output(TRIG2, False)
	time.sleep(0.00001)
	start = time.time()
	
	while GPIO.input(ECHO1) == 0:
	     start = time.time()
	while GPIO.input(ECHO1) == 1:
	     stop = time.time()

	elapsed = stop - start
	#distance = (elapsed * 34300)/2
	distance = elapsed
	return distance

# Trigger the relay switch in order to lock the door.
def press_lock1_button():
	#'relay off...'
	GPIO.output(RelayPin1, GPIO.HIGH)
	time.sleep(0.5)
	#'...relayd on'
	GPIO.output(RelayPin1, GPIO.LOW)

def press_lock2_button():
	#'relay off...'
	GPIO.output(RelayPin2, GPIO.HIGH)
	time.sleep(0.5)
	#'...relayd on'
	GPIO.output(RelayPin2, GPIO.LOW)

def reset_relay():
	#'...relayd on'
	GPIO.output(RelayPin1, GPIO.LOW)
	GPIO.output(RelayPin2, GPIO.LOW)

# Check Toilet #1 was engaged or not.
def check_T1():
        global T1_engaged 
	global chk_T1_again
 	dis_1 = 0
	dis_1 = int(distance_s1())
        print ("Toilet #1", T1_engaged, num_of_secs, chk_T1_again, dis_1, dist01)
	time.sleep(0.5)
        if dis_1 < dist01 and T1_engaged == 0: 
           T1_engaged = 1
        if dis_1 < dist01 and T1_engaged == 1:
	   chk_T1_again += 1
	   # If the object has been detected and not move for few seconds, then trigger the relay.
           if chk_T1_again == num_of_secs:
	      press_lock1_button()
              T1_engaged = 2
	      logFile.write("Toilet #1 was engaged when ")
	      logFile.write(str(time.strftime('%Y-%m-%d %H:%M%p / ')))
	      logFile.write("object was detected at ")
	      logFile.write(str(round(dis_1, 2)))
	      logFile.write("cm\n")
	      return T1_engaged
        if dis_1 > dist01:
 	   if T1_engaged == 2:
              T1_engaged = 0 
              chk_T1_again = 0 

# Check Toilet #2 was engaged or not.
def check_T2():
        global T2_engaged 
	global chk_T2_again
 	dis_2 = 0
	dis_2 = int(distance_s2())
        print ("Toilet #2", T2_engaged, num_of_secs, chk_T2_again, dis_2, dist02)
	time.sleep(0.5)
        if dis_2 < dist02 and T2_engaged == 0: 
           T2_engaged = 1
        if dis_2 < dist02 and T2_engaged == 1:
           print (chk_T2_again)
	   chk_T2_again += 1
	   # If the object has been detected and not move for FOUR seconds, then trigger the relay.
           if chk_T2_again == num_of_secs:
           	press_lock2_button()
           	T2_engaged = 2
 	   	logFile.write("Toilet #2 was engaged when ")
 	   	logFile.write(str(time.strftime('%Y-%m-%d %H:%M%p / ')))
 	   	logFile.write("object was detected at ")
           	logFile.write(str(round(dis_2, 2)))
           	logFile.write("cm\n")
           	return T2_engaged
        if dis_2 > dist02 and T2_engaged == 2:
           T2_engaged = 0
           chk_T2_again = 0 

def loop():
        global T1_engaged 
        global T2_engaged 
        # Endless loop for sending signal to ultrasonic sensor.
        while True:
		# Check Toilet #1
       		check_T1()
		# Check Toilet #2
		# Only the toilet #1 is testing, ultrasonic sensor disabled.
		# check_T2()
	
def destroy():
	GPIO.cleanup()

if __name__ == "__main__":
	setup()
        filename = ('/home/pi/ADP/log/'+time.strftime('%Y%m%d-%H%M%p')+'_tls.log')
	global logFile
        logFile = open(filename, 'w+', buffering=bufsize)
	reset_relay()
	try:
                reset_relay()
		loop()
	except KeyboardInterrupt:
		pass
	finally:
		logFile.close()
		GPIO.cleanup()
