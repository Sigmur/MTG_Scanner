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
import tempfile
import pygame
import pygame.camera

FILE_OUTPUT_NAME = 'capture.jpg'
CAMERA_W = 1600
CAMERA_H = 1200
camera = None
screen = None
dummy_screen = pygame.Surface((CAMERA_W, CAMERA_H))
begin_time = int(time.time() * 100)
update_diff = 0

def init():
	global camera
	
	pygame.init()
	pygame.camera.init()
	cam_list = pygame.camera.list_cameras()
	if len(cam_list) < 1:
		raise ValueError('No camera detected !')
	camera = pygame.camera.Camera(cam_list[0],(CAMERA_W,CAMERA_H), "RGB")
	camera.start()
	
def cleanup():
	global camera
	
	del(camera)
	
def updateImage():
	global update_diff
	global begin_time
	
	now = int(time.time() * 100)
	diff = int(now - begin_time)
	begin_time = now
	
	if (update_diff >= 20):
		camera.get_image()
		update_diff = 0
	else:
		update_diff += diff

def capture(output_file_path = ''):
	global camera
	
	if output_file_path == '':
		output_file_path = tempfile.gettempdir() + '/' + FILE_OUTPUT_NAME
	snapshot = camera.get_image()
	pygame.image.save(snapshot, output_file_path)
	return output_file_path

def initOuput():
	global screen
	
	screen = pygame.display.set_mode((CAMERA_W,CAMERA_H),0)
	
def updateOutput():
	image1 = camera.get_image()
	screen.blit(image1,(0,0))
	pygame.display.update()
