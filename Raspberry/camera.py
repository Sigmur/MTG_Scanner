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
import time

import cv2

CAMERA_W = 1600
CAMERA_H = 1200
camera = None
begin_time = 0
update_diff = 0

def init():
	global camera
	
	#pygame.init()
	#pygame.camera.init()
	#cam_list = pygame.camera.list_cameras()
	#if len(cam_list) < 1:
	#	raise ValueError('No camera detected !')
	#camera = pygame.camera.Camera(cam_list[0],(CAMERA_W,CAMERA_H), "RGB")
	#camera.start()
	camera = cv2.VideoCapture(0)
	if (camera.isOpened() == False): 
		raise Exception('Could not init camera')
	
	camera.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_W)
	camera.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_H)
	camera.set(cv2.CAP_PROP_FPS, 20)
	camera.set(cv2.CAP_PROP_GAIN, 0)

	test = camera.get(cv2.CAP_PROP_POS_MSEC)
	ratio = camera.get(cv2.CAP_PROP_POS_AVI_RATIO)
	frame_rate = camera.get(cv2.CAP_PROP_FPS)
	width = camera.get(cv2.CAP_PROP_FRAME_WIDTH)
	height = camera.get(cv2.CAP_PROP_FRAME_HEIGHT)
	brightness = camera.get(cv2.CAP_PROP_BRIGHTNESS)
	contrast = camera.get(cv2.CAP_PROP_CONTRAST)
	saturation = camera.get(cv2.CAP_PROP_SATURATION)
	hue = camera.get(cv2.CAP_PROP_HUE)
	gain = camera.get(cv2.CAP_PROP_GAIN)
	exposure = camera.get(cv2.CAP_PROP_EXPOSURE)
	print("Test: ", test)
	print("Ratio: ", ratio)
	print("Frame Rate: ", frame_rate)
	print("Height: ", height)
	print("Width: ", width)
	print("Brightness: ", brightness)
	print("Contrast: ", contrast)
	print("Saturation: ", saturation)
	print("Hue: ", hue)
	print("Gain: ", gain)
	print("Exposure: ", exposure)
	
def cleanup():
	global camera
	
	cv2.destroyAllWindows() 
	camera.release()
	
def updateImage(show=False):
	global update_diff
	global begin_time

	ret, image = camera.read()
	if ret != True: 
		return None
		
	if show:
		cv2.imshow('image', image)
		image = cv2.waitKey(1) & 0xFF
	
	return image

def autoUpdate(show=False):
	global begin_time
	global update_diff

	now = int(time.time() * 100)
	diff = int(now - begin_time)
	begin_time = now
	
	if (update_diff >= 60):
		updateImage(show)
		update_diff = 0
	else:
		update_diff += diff

