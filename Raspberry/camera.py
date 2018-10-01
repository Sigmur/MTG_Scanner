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

from threading import Thread
import cv2
import queue
import time

CAMERA_W	= 1600
CAMERA_H	= 1200
CAMERA_FPS	= 60
 
images = queue.Queue(3)
 
class WebcamVideoStream:
	def __init__(self, src=0):
		#1) Init stream
		self.stream = cv2.VideoCapture(src)
		if (self.stream.isOpened() == False): 
			raise Exception('Could not init camera')
		
		self.stream.set(cv2.CAP_PROP_FRAME_WIDTH, CAMERA_W)
		self.stream.set(cv2.CAP_PROP_FRAME_HEIGHT, CAMERA_H)
		self.stream.set(cv2.CAP_PROP_FPS, CAMERA_FPS)

		''' Possible camera parameters
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
		'''
		
		#2) Init frame queue & get first frame
		self.show_output = False
		self.has_new_frame = False
		self.updateFrame()
 
		#3) Setup stop
		self.stopped = False
		
	def start(self):
		# start the thread to read frames from the video stream
		Thread(target=self.update, args=()).start()
		return self
 
	def update(self):
		# keep looping infinitely until the thread is stopped
		while True:
			# if the thread indicator variable is set, stop the thread
			if self.stopped:
				return
 
			# otherwise, read the next frame from the stream
			self.updateFrame()

	def updateFrame(self):
		global images

		begin = time.time()
		(self.grabbed, self.last_image) = self.stream.read()
		if images.full():
			images.get_nowait()
		images.put_nowait(self.last_image)
		self.has_new_frame = True
		if self.show_output == True:
			self.displayImage(self.last_image)

		sleep_time = (1.0 / CAMERA_FPS) - (time.time() - begin)
		if (sleep_time < 0):
			sleep_time = 0
		time.sleep(sleep_time)
		
	def toggleShowOutput(self, active=None):
		if active is None:
			active = not self.show_output
		self.show_output = active
	
	def displayImage(self, image=None, window_title='Camera output'):
		if image is None and self.has_new_frame == True:
			(self.grabbed, self.last_image) = self.stream.read()
			image = self.last_image
		if image is None:
			return
		cv2.imshow(window_title, image)
		self.has_new_frame == False
		image = cv2.waitKey(1) & 0xFF
 
	def stop(self):
		# indicate that the thread should be stopped
		cv2.destroyAllWindows()
		self.stream.release()
		self.stopped = True

camera_handler = None

def init():
	global camera_handler
	
	camera_handler = WebcamVideoStream()
	camera_handler.start()

def cleanup():
	global camera_handler

	if camera_handler is None:
		return
	camera_handler.stop()
		
def read():
	global images
	
	return images.get()
