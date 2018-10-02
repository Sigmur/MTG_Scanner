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
import os
import io
import json
import config
from programs import program
import camera
import image_processing
import photo_resistor
import ocr_processing
import mtg.parsing
from motor import stepper
import filters

#State 1) Roll a card, wait for photo sensor to trigger
#State 2) take a picture, do stuff with it
#State 3) Move filter into position
#State 4) Roll gently to drop a card
STATE_ROLL = 1
STATE_IMAGE_PROCESSING = 2
STATE_FILTER = 3
STATE_DROP = 4

#TODO - Write/read config file for filters

class Handler(program.Program):
	def __init__(self):
		print('Scanner engaged')
		#1) Init camera
		camera.init()
		camera.camera_handler.toggleShowOutput(True)
		#2) Init stepper
		stepper.init()
		stepper.setDirection(-1) #Counter clockwise
		#3) Init sensor
		photo_resistor.init()
		#4) Init filters
		filters.init()
		
		#Init vars
		self.current_state = STATE_ROLL
		self.processed_count = 0
		self.log = []
		self.last_processed_data = []
		
	def getName(self):
		return 'Scanner'

	def update(self):
		if self.current_state == STATE_ROLL:
			#State 1) Roll a card, wait for photo sensor to trigger
			stepper.turn(6)
			if photo_resistor.isActive() == True:
				self.current_state = STATE_IMAGE_PROCESSING
				stepper.stop()
				print('------------------------')
		elif self.current_state == STATE_IMAGE_PROCESSING:
			#State 2) take a picture, do stuff with it
			time.sleep(0.9) #We need to wait for the camera to update properly
			#1) Take a picture
			camera.camera_handler.toggleShowOutput(False)
			captured = camera.read().copy()
			if captured is None:
				return
			#2) Pre-process image for Tesseract
			camera.to_display = captured.copy()
			processed_path = image_processing.process(captured)
			if processed_path is None:
				return
			#3) Pass image threw Tesseract
			ocr_string = ocr_processing.processImage(processed_path)
			#4) Parse result string
			card_data = mtg.parsing.parse(ocr_string)
			self.last_processed_data = card_data
			print(card_data, ocr_string)
			self.log.append(card_data)
			self.processed_count += 1
			self.current_state = STATE_FILTER
		elif self.current_state == STATE_FILTER:
			#State 3) Move filter into position
			#TODO - Cleanup this
			#if (self.last_processed_data['extention'] == 'AKH'):
			#	filters.open(1)
			#elif (self.last_processed_data['extention'] == 'BFZ'):
			#	filters.open(2)
			#elif (self.last_processed_data['extention'] == 'KLD'):
			#	filters.open(3)
			#elif (self.last_processed_data['extention'] == 'ORI'):
			#	filters.open(4)
			#else:
			#	filters.close()
			self.current_state = STATE_DROP
		elif self.current_state == STATE_DROP:
			#State 4) Roll gently to drop a card, wait for second sensor to trigger
			#Slight static movEment to trigger drop
			for i in range(0, 5):
				stepper.step() #A few stepsis all it takes
				time.sleep(0.05)
			if photo_resistor.isActive() == False:
				time.sleep(0.5)
				self.current_state = STATE_ROLL
			else:
				stepper.turn(30)
		return False
			
	def stop(self):
		self.saveLog()
		camera.cleanup()
		
	def saveLog(self):
		if os.path.exists('./log') == False:
			os.makedirs('./log')
		log_name = 'log/log_card_' + str(int(time.time())) + '.json'
		# Write JSON file
		with io.open(log_name, 'w', encoding='utf8') as outfile:
			str_ = json.dumps(self.log, indent=4, separators=(',', ': '), ensure_ascii=False)
			outfile.write(str(str_))
