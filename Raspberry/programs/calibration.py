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

import time
import json
import io

from programs import program
import camera
import photo_resistor
import image_processing
from motor import stepper

#1) Calibrate unblocked photo sensor light reception
#2) Roll a card over photo sensor to calibrate light block
#3) Calibrate camera focus, roll a card if removed
#4) Calibrate angle, test a card ,ask if angle is ok, roll another card. If ok 3 times in a row, save angle.

STATE_CALIBRATE_SENSOR_ON =		1 #Check if light sensor detection is ok
STATE_CALIBRATE_SENSOR_OFF =	2 #Roll a card over the light sensor, stop when trigger light sensor, ask user to press enter for ok and escape for retry
STATE_CALIBRATE_CAMERA =		3 #Roll a card and activate camera to allow user to calibrate focus
STATE_CALIBRATE_ANGLE =			4 #Take a picture, detect angle, show result image, ask to user if result is ok or not, after ~5 successful tests, save angle

class Handler(program.Program):
	def __init__(self):
		print('Entering calibration mode')
		self.state = STATE_CALIBRATE_SENSOR_ON
		self.angles = []
		
		#1) Init camera
		camera.init()
		camera.camera_handler.toggleShowOutput(True)
		#2) Init stepper
		stepper.init()
		stepper.setDirection(-1) #Counter clockwise
		#3) Init sensor
		photo_resistor.init()
		
	def getName(self):
		return 'Calibration'

	def update(self):
		if self.state == STATE_CALIBRATE_SENSOR_ON:
			#1) Calibrate unblocked photo sensor light reception
			ok = '\033[92m' + 'DETECT LIGHT' + '\033[0m'
			not_ok = '\033[91m' + 'IN THE DARK ' + '\033[0m'
			
			#photo resistor active = in the dark
			sensor_state = not_ok if photo_resistor.isActive() == True else ok
			if photo_resistor.isActive() != True: #It was good at one point, check over time
				sensor_state = ok 
				for i in range(0, 100): #Check a 100 times over a second, must stay inactive
					if photo_resistor.isActive() == True:
						sensor_state = not_ok
						break
					time.sleep(0.01)
				
			print('Photosensor calibration mode, sensor state is ' + sensor_state, end='\r')
			if sensor_state == ok:
				print('Photosensor light calibration ok, test with a card over it')
				self.state = STATE_CALIBRATE_SENSOR_OFF
			time.sleep(0.1)
		elif self.state == STATE_CALIBRATE_SENSOR_OFF:
			#2) Roll a card over photo sensor to calibrate light block
			if photo_resistor.isActive() != True: #While there is nothing over it ,roll a card
				stepper.turn(6)
				print('Wait for a card ...', end='\r')
				time.sleep(0.001)
			else:
				print('Detected a card, is the calibration ok ? type y/n and press enter', end='\n')
				while True:
					choice = input("> ")
					if choice == 'y':
						print('Sensor off clibration is ok')
						self.state = STATE_CALIBRATE_CAMERA
						break
					elif choice == 'n':
						print('Ok, manually remove card and move sensor, will resume operation in 10 seconds')
						time.sleep(10)
						print('Resume')
						break
		elif self.state == STATE_CALIBRATE_CAMERA:
			#3) Calibrate camera focus, roll a card if removed
			print('Manually calibrate camera focus')
			print("Press CTRL-C to exit this mode, manually remove a card to roll a new one")
			try:
				while True:
					while photo_resistor.isActive() != True: #While there is nothing over it ,roll a card
						stepper.turn(6)
						time.sleep(0.01)
			except KeyboardInterrupt:
				self.state = STATE_CALIBRATE_ANGLE
				print("\nCamera calibration is ok, check angle")
				camera.camera_handler.toggleShowOutput(False)
				pass
		elif self.state == STATE_CALIBRATE_ANGLE:
			#4) Calibrate angle, test a card ,ask if angle is ok, roll another card. If ok 3 times in a row, save angle.
			#4.1) Roll card if needed
			while photo_resistor.isActive() != True: #While there is nothing over it ,roll a card
				stepper.turn(6)
				time.sleep(0.01)
			#4.2) Display angled image
			for i in range(0, 25):
				time.sleep(0.1)
			image = camera.read().copy()
			if image is None:
				return
			print('Detect angle ...')
			angle = image_processing.detectAngle(image)
			image = image_processing.rotate(image, angle)
			camera.to_display = image
			print('Detected angle of', angle, ' enter \'y\' if image is displayed correctly and \'n\' if not')
			while True:
				choice = input("> ")
				if choice == 'y':
					self.angles.append(angle)
					if len(self.angles) >= 3:
						with io.open('angle.json', 'w', encoding='utf8') as outfile:
							str_ = json.dumps({"angle": (sum(self.angles) / len(self.angles))}, indent=4, separators=(',', ': '), ensure_ascii=False)
							outfile.write(str(str_))
						print('Calibration is over !')
						return True
					else:
						print(len(self.angles), '/ 3', 'Angle added to pile, go to next card')
						while photo_resistor.isActive():
							stepper.turn(6)
						break
				elif choice == 'n':
					print('Try with another card')
					while photo_resistor.isActive():
						stepper.turn(6)
					break
		else:
			return False
			
	def stop(self):
		camera.cleanup()
