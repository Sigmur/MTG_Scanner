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

## TO BE REWRITTEN TO WORK WITH NEW ARDUINO SYSTEM
#min 2.5 max 11.5
SERVO_OPEN = 8
SERVO_CLOSE = 11.1

SERVO_COMMUNICATION_PINS = [16, 20, 21]

filters = []

def init():
	global filters
	
	GPIO.setmode(GPIO.BCM)
	for i in range(0, len(SERVO_COMMUNICATION_PINS)):
		GPIO.setup(SERVO_COMMUNICATION_PINS[i], GPIO.OUT)
		GPIO.output(SERVO_COMMUNICATION_PINS[i], False)
		
def setServoOutput(filter_id):
	if (filter_id < 0 or filter_id > 7):
		filter_id = 0
		
	GPIO.output(SERVO_COMMUNICATION_PINS[0], (filter_id & 1))
	GPIO.output(SERVO_COMMUNICATION_PINS[1], (filter_id & 2))
	GPIO.output(SERVO_COMMUNICATION_PINS[2], (filter_id & 4))
		
def open(filter_id):
	setServoOutput(filter_id)

def close():
	setServoOutput(0)
