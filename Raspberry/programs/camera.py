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
sys.path.append('../')

import Program
import camera
import photo_resistor
from motor import stepper

#1) Show camera output
#2) While no card detected, roll a card

class ProgramCamera(Program):
	def __init__(self):
		print('Entering camera focus mode')

		#1) Init camera
		camera.init()
		camera.camera_handler.toggleShowOutput(True)
		#2) Init stepper
		stepper.init()
		stepper.setDirection(-1) #Counter clockwise
		#3) Init sensor
		photo_resistor.init()
		
	def getName(self):
		return 'Camera'

	def update(self):
		if photo_resistor.isActive() != True: #Sensor not triggered = no card above it
			stepper.turn(6)
			
	def stop(self):
		camera.cleanup()
