#!/usr/bin/python
'''
MIT License

Copyright (c) 2018 Sigmur

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
'''

import RPi.GPIO as GPIO
import time

SERVO_TRANSMISSION_CLOCK_PIN =	20
SERVO_TRANSMISSION_PIN =		21
SERVO_TRANSMISSION_DELAY =		0.005 # 5ms
SERVO_TRANSMISSION_SIZE =		16 

current_servo_states = []

def init():
	global current_servo_states
	
	#Init input/output
	GPIO.setup(SERVO_TRANSMISSION_CLOCK_PIN, GPIO.OUT)
	GPIO.setup(SERVO_TRANSMISSION_PIN, GPIO.OUT)
	GPIO.output(SERVO_TRANSMISSION_CLOCK_PIN, False)
	GPIO.output(SERVO_TRANSMISSION_PIN, False)
	#Init servo states
	for i in range(0, SERVO_TRANSMISSION_SIZE):
		current_servo_states.append(False)
	
def setServos(servo_list):
	global current_servo_states
	
	for index, state in servo_list.items():
		if index > 0 and index < SERVO_TRANSMISSION_SIZE:
			current_servo_states[index] = True if state <= 0 else False
			
def sendServoStates():
	for i in range(0, SERVO_TRANSMISSION_SIZE):
		#1) Write current bit to transmission pin
		GPIO.output(SERVO_TRANSMISSION_PIN, current_servo_states[i])
		#2) Rise pin to tell receiver that it need to read
		GPIO.output(SERVO_TRANSMISSION_CLOCK_PIN, True)
		#3) Wait a little for receiver to read
		time.sleep(SERVO_TRANSMISSION_DELAY)
		#4) Drop pin, end of transmission for this bit
		GPIO.output(SERVO_TRANSMISSION_CLOCK_PIN, False)
		time.sleep(0.001)
	GPIO.output(SERVO_TRANSMISSION_PIN, False)
	