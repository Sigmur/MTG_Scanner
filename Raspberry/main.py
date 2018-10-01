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

#sudo apt-get install libjpeg8-dev
#sudo apt-get install tesseract-ocr

import sys
import time
import RPi.GPIO as GPIO
import json
import io
import os
import timing
from programs import *
#Driver for main stepper motor
#from motor import stepper
#Sensor to correct position for card reading
#import photo_resistor
#Camera driver to read card
#import camera
#Resize, process & prepare image for Tesseract
#import image_processing
#Tesseract OCR image to string
#import ocr_processing
#Parse result Tesseract string
#from mtg import parsing
#MTG api call, disabld for now
#import mtg_card_api
#from  motor import filters

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
#Filters
#CLOCK			= BCM20
#TRANSMISSION	= BCM21

program = None

#1) Load program
if len(sys.argv) > 1:
	if sys.argv[1] == 'camera':
		program = ProgramCamera()
	elif sys.argv[1] == 'filters':
		program = ProgramFilters()
	elif sys.argv[1] == 'calibrate':
		program = ProgramCalibration()
else:
	program = ProgramScanner()

#2) Run program
try:
	while True:
		program.update();

except KeyboardInterrupt:
	print("\n Keyboard stopping")

#3) Cleanup before stop
finally:
	program.stop()
	GPIO.cleanup()
