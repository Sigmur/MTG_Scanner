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

#Requied libs
#sudo apt-get install libjpeg8-dev
#sudo pip3 install Pillow
#sudo apt-get install tesseract-ocr
#sudo pip3 install pytesseract

import sys
import time
import RPi.GPIO as GPIO
import json
import io
import os
import pygame
import timing
#Driver for main stepper motor
from motor import stepper
#Sensor to correct position for card reading
import photo_resistor
#Camera driver to read card
import camera
#Resize, process & prepare image for Tesseract
import image_processing
#Tesseract OCR image to string
import ocr_processing
#Parse result Tesseract string
from mtg import parsing
#MTG api call, disabld for now
#import mtg_card_api
from  motor import filters

#Pinout					BOARD CORNER HERE
# 3.3V  1 #  # 2  5V
# BCM2  3 #  # 4  5V
# BCM3  5 #  # 6  GND
# BCM4  7 #  # 8  BCM14
# GND   9 #  #10  BCM15
# BCM17 11#  #12  BCM18
# BCM27 13#  #14  GND
# BCM22 15#  #16  BCM23
# 3.3V  17#  #18  BCM24
# BCM10 19#  #20  GND
# BCM9  21#  #22  BCM25
# BCM11 23#  #24  BCM8
# GND   25#  #26  BCM7
# BCM0  27#  #28  BCM1
# BCM5  29#  #30  GND
# BCM6  31#  #32  BCM12
# BCM13 33#  #34  GND
# BCM19 35#  #36  BCM16
# BCM26 37#  #38  BCM20
# GND   39#  #40  BCM21

#Stepper pinout
#A_PLUS  = BCM17
#A_MINUS = BCM22
#B_PLUS  = BCM27
#B_MINUS = BCM23
#Photoresitor
#SIGNAL  = BCM4

# INIT
stepper.init()
stepper.setDirection(-1) #Counter clockwise
photo_resistor.init()
camera.init()
filters.init()

#time.sleep(0.0007) - maximum speed

#State 1) Roll a card, wait for photo sensor to trigger
#State 2) take a picture, do stuff with it
#State 3) Move filter into position
#State 4) Roll gently to drop a card, wait for second sensor to trigger 
STATE_ROLL = 1
STATE_IMAGE_PROCESSING = 2
STATE_FILTER = 3
STATE_DROP = 4
#Calibration states
STATE_CALIBRATE_SENSOR_ON =		1 #Check if light sensor detection is ok
STATE_CALIBRATE_SENSOR_OFF =	2 #Roll a card over the light sensor, stop when trigger light sensor, ask user to press enter for ok and escape for retry
STATE_CALIBRATE_CAMERA =		3 #Roll a card and activate camera to allow user to calibrate focus
STATE_CALIBRATE_ANGLE =			4 #Take a picture, detect angle, show result image, ask to user if result is ok or not, after ~5 successful tests, save angle

current_state = STATE_ROLL
camera_update_timer = 0
last_processed_data = {}
processed_count = 0
log = []

#Check wich program to launch, scanner by default
PROGRAM_SCANNER			= 0	#Scan card and store result in a json file
PROGRAM_CAMERA			= 1	#Roll a card, show camera output to allow user to adjust focus
PROGRAM_FILTERS			= 2 #Open/close filters one after another
PROGRAM_CALIBRATION		= 3 #Calibration process
#Arguments :
# camera = roll a card & display camera output setup focus
program = PROGRAM_SCANNER
if len(sys.argv) > 1:
	if sys.argv[1] == 'camera':
		print('Entering camera focus mode')
		camera.camera_handler.toggleShowOutput(True)
		program = PROGRAM_CAMERA
	elif sys.argv[1] == 'filters':
		print('Entering filters test mode')
		program = PROGRAM_FILTERS
	elif sys.argv[1] == 'calibrate':
		print('Entering calibration mode')
		program = PROGRAM_CALIBRATION
		current_state = STATE_CALIBRATE_SENSOR_ON
else:
	camera_handler.toggleShowOutput(True)
		
def saveLog():
	if os.path.exists('./log') == False:
		os.makedirs('./log')
	log_name = 'log/log_card_' + str(int(time.time())) + '.json'
	# Write JSON file
	with io.open(log_name, 'w', encoding='utf8') as outfile:
		str_ = json.dumps(log, indent=4, separators=(',', ': '), ensure_ascii=False)
		outfile.write(str(str_))

def scanner():
	global current_state
	global processed_count
	global log
	global camera_update_timer
	global last_processed_data
	
	if current_state == STATE_ROLL:
		stepper.turn(6)
		if photo_resistor.isActive() == True:
			current_state = STATE_IMAGE_PROCESSING
			camera_update_timer = time.time() + 2
			stepper.stop()
			print('------------------------')
	elif current_state == STATE_IMAGE_PROCESSING:
		if (time.time() < camera_update_timer): #Wait for card to stop moving & camera to be correctly init
			time.sleep(0.1)
			return
		#1) Take a picture
		#debug path '/home/pi/projets/MTGScanner/card' + str(processed_count) + '.jpg'
		#captured = camera.capture('/home/pi/projets/MTGScanner/out/card' + str(processed_count) + '.jpg')
		#TODO - REWORK WITH NEW SYSTEMS
		captured = None
		#2) Pre-process image for Tesseract
		processed_path = image_processing.process(captured)
		#3) Pass image threw Tesseract
		ocr_string = ocr_processing.processImage(processed_path)
		#4) Parse result string
		card_data = mtg_parsing.parse(ocr_string)
		last_processed_data = card_data
		print(card_data, ocr_string)
		log.append(card_data)
		processed_count += 1
		current_state = STATE_FILTER
	elif current_state == STATE_FILTER:
		#TODO - Cleanup this
		if (last_processed_data['extention'] == 'AKH'):
			filters.open(1)
		elif (last_processed_data['extention'] == 'BFZ'):
			filters.open(2)
		elif (last_processed_data['extention'] == 'KLD'):
			filters.open(3)
		elif (last_processed_data['extention'] == 'ORI'):
			filters.open(4)
		else:
			filters.close()
		current_state = STATE_DROP
	elif current_state == STATE_DROP:
		#Slight static movment to trigger drop
		for i in range(0, 5):
			stepper.step()
			time.sleep(0.05)
		if photo_resistor.isActive() == False:
			time.sleep(0.5)
			#print("Dropped !")
			current_state = STATE_ROLL
		else:
			stepper.turn(30)
			
def camera_focus():
	global current_state
	
	if current_state == STATE_ROLL:
		stepper.turn(10)
		if photo_resistor.isActive() == True:
			current_state = STATE_IMAGE_PROCESSING
	elif current_state == STATE_IMAGE_PROCESSING:
		if photo_resistor.isActive() != True:
			current_state = STATE_ROLL

	time.sleep(0.1)
			
def test_filters():
	for i in range(0, 5):
		print('Toggle filter ', i)
		filters.open(i)
		time.sleep(2)

def calibration():
	global current_state
	global processed_count
	global log
	
	if current_state == STATE_CALIBRATE_SENSOR_ON:
		ok = '\033[92m' + 'DETECT LIGHT' + '\033[0m'
		not_ok = '\033[91m' + 'IN THE DARK ' + '\033[0m'
		STATE_CALIBRATE_SENSOR_OFF
		
		#photo resistor active = in the dark
		state = not_ok if photo_resistor.isActive() == True else ok
		if photo_resistor.isActive() != True: #It was good at one point, check over time
			state = ok 
			for i in range(0, 100):
				if photo_resistor.isActive() == True:
					state = not_ok
					break
				time.sleep(0.01)
			
		print('Photosensor calibration mode, sensor state is ' + state, end='\r')
		if state == ok:
			print('Photosensor light calibration ok, test with a card over it')
			current_state = STATE_CALIBRATE_SENSOR_OFF
		time.sleep(0.1)
	elif current_state == STATE_CALIBRATE_SENSOR_OFF:
		if photo_resistor.isActive() != True: #While there is nothing over it ,roll a card
			stepper.turn(6)
			print('Wait for a card ...', end='\r')
			time.sleep(0.01)
		else:
			print('Detected a card, is the calibration ok ? type y/n and press enter', end='\n')
			while True:
				choice = input("> ")
				if choice == 'y':
					print('Sensor off clibration is ok')
					current_state = STATE_CALIBRATE_CAMERA
					break
				elif choice == 'n':
					print('Ok, manually remove card and move sensor, will resume operation in 10 seconds')
					time.sleep(10)
					print('Resume')
					break
	elif current_state == STATE_CALIBRATE_CAMERA:
		print('Manually calibrate camera focus', current_state)
		print("Press CTRL-C to this mode, manually remove a card to roll a new one")
		try:
			while True:
				while photo_resistor.isActive() != True: #While there is nothing over it ,roll a card
					stepper.turn(6)
		except KeyboardInterrupt:
			current_state = STATE_CALIBRATE_ANGLE
			print("\nCamera calibration is ok, check angle")
			pass
	elif current_state == STATE_CALIBRATE_ANGLE:
		#1) Roll card if needed
		while photo_resistor.isActive() != True: #While there is nothing over it ,roll a card
			stepper.turn(6)
		#2) Display angled image
		for i in range(0, 25):
			time.sleep(0.1)
		image = camera_handler.read()
		angle = image_processing.detectAngle(image)
		image = image_processing.rotate(image, angle)
		camera_handler.displayImage(image)
		print('Detected angle of', angle, ' enter \'y\' if image is displayed correctly and \'n\' if not')
		while True:
			choice = input("> ")
			if choice == 'y':
				log.append(angle)
				processed_count += 1
				if processed_count >= 3:
					with io.open('angle.json', 'w', encoding='utf8') as outfile:
						str_ = json.dumps({"angle": (sum(log) / len(log))}, indent=4, separators=(',', ': '), ensure_ascii=False)
						outfile.write(str(str_))
					print('Calibration is over !')
					sys.exit(0)
					return True
				else:
					print(processed_count, '/ 3', 'Angle added to pile, go to next card')
					while photo_resistor.isActive():
						stepper.turn(6)
					break
			elif choice == 'n':
				print('Try with another card')
				while photo_resistor.isActive():
					stepper.turn(6)
				break
	else:
		return True

try:
	while True:
		if program == PROGRAM_SCANNER:
			scanner()
		elif program == PROGRAM_CAMERA:
			camera_focus()
		elif program == PROGRAM_FILTERS:
			test_filters()
		elif program == PROGRAM_CALIBRATION:
			calibration()
		
#		time.sleep(0.001) # Update every 1ms

except KeyboardInterrupt:
	print("\n Keyboard stopping")

finally:
	if program == PROGRAM_SCANNER:
		saveLog()
	GPIO.cleanup()
	camera.cleanup()
