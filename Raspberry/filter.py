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

from motor import servo

filter_default_states = {}
filter_states = {}

#Here our servos have 2 states : Open & closed
#Servos are places like this on the output :
#			filter_0----servo_0
#servo_1----filter_1
#			filter_2----servo_2
# ...
# To close filter_0, servo_0 must be in closed state
# To close filter_1, servo_1 must be in open state
# and so on

def init():
	global filter_default_states
	global filter_states
	
	for i in range(0, servo.SERVO_TRANSMISSION_SIZE):
		filter_default_states[i] = ((i % 2) == 0) # switch between open & closed as default states
		filter_states[i] = False
	
	servo.setServos(filter_default_states)

def open(servo_index):
	global filter_states

	if filter_states[servo_index] == True:
		return
	filter_states[servo_index] = True
	servo.setServos({servo_index: True})

def close(servo_index):
	global filter_states

	if filter_states[servo_index] == False:
		return
	filter_states[servo_index] = False
	servo.setServos({servo_index: False})
	
def toggle(servo_index):
	global filter_states

	filter_states[servo_index] = not filter_states[servo_index]
	servo.setServos({servo_index: filter_states[servo_index]})

def closeAll():
	global filter_states

	servo.setServos(filter_default_states)
	for i in range(0, servo.SERVO_TRANSMISSION_SIZE):
		filter_states[i] = False
		
def openOnly(servo_index):
	global filter_states
	
	states = filter_default_states.copy()
	states[servo_index] = not states[servo_index]
	servo.setServos(states)
	filterstates = states
