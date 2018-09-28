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

import sys
import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)
DEFAULT_A_PLUS = 17
DEFAULT_A_MINUS = 22
DEFAULT_B_PLUS = 27
DEFAULT_B_MINUS = 23

stepper_sequence = 	[
					[1,0,0,0],
					[1,1,0,0],
					[0,1,0,0],
					[0,1,1,0],
 				    [0,0,1,0],
				    [0,0,1,1],
				    [0,0,0,1],
					[1,0,0,1]]
					
					  
step_count = len(stepper_sequence)
step_direction = 1 #1 & 2 clockwise, -1 & -2 counterclockwise
step_pins = [DEFAULT_A_PLUS,DEFAULT_A_MINUS,DEFAULT_B_PLUS,DEFAULT_B_MINUS]
current_step_index = 0

def init():
	global step_pins
	print("Setup stepper pins", step_pins)
	for pin in step_pins:
		GPIO.setup(pin,GPIO.OUT)
		GPIO.output(pin, False)
    
def stop():
  for pin in step_pins:
    GPIO.output(pin, False)

def setPins(a_plus = DEFAULT_A_PLUS, a_minus = DEFAULT_A_MINUS, b_plus = DEFAULT_B_PLUS, b_minus = DEFAULT_B_MINUS):
	global step_pins
	step_pins[0] = a_plus
	step_pins[1] = a_minus
	step_pins[2] = b_plus
	step_pins[3] = b_minus

def setDirection(direction):
  global step_direction
  
  if direction > 0 and direction > 2:
    direction = 2
  if direction < 0 and direction < -2:
    direction = -2
  if direction == 0:
    direction = 0
  step_direction = direction

def step():
	global step_pins
	global stepper_sequence
	global current_step_index
	global step_direction

	for pin in range(0, 4):
		GPIO.output(step_pins[pin], stepper_sequence[current_step_index][pin])

	current_step_index += step_direction

	if (current_step_index >= step_count):
		current_step_index = 0
	if (current_step_index < 0):
		current_step_index = step_count + step_direction

turn_delay = -1
turn_time = 0
turn_diff = 0
#delay is in ms
def turn(delay):
	global turn_delay
	global turn_time
	global turn_diff
	
	current_time = time.time() * 1000;

	if (turn_delay != delay or turn_delay == -1) and delay > 0:
		turn_delay = delay
		turn_diff = 0
		
	if (delay <= 0):
		return

	turn_diff += current_time - turn_time
	
	if (turn_diff >= turn_delay):
		step()
		turn_diff = 0
		
	turn_time = current_time
