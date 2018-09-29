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
#OpenCV (cv2) Install
#http://www.life2coding.com/install-opencv-3-4-0-python-3-raspberry-pi-3/
#sudo apt-get install libhdf5-dev
#sudo apt-get update
#sudo apt-get install libhdf5-serial-dev
#sudo apt install libqtgui4

import numpy as np
import cv2
import math
import os

index = 0

def process(file_name, threshold=150):
	global index
	
	#1) Open file
	img = cv2.imread(file_name)

	height, width, channels = img.shape
	#2) Generate blank file to be filled with found text
	blank_image = np.zeros((height, width, 3), np.uint8)
	
	#3) Generate temp images & process image
	img2gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
	ret, mask = cv2.threshold(img2gray, threshold, 255, cv2.THRESH_BINARY)
	image_final = cv2.bitwise_and(img2gray, img2gray, mask=mask)
	ret, new_img = cv2.threshold(image_final, threshold, 255, cv2.THRESH_BINARY)  # for black text , cv.THRESH_BINARY_INV
	kernel = cv2.getStructuringElement(cv2.MORPH_CROSS, (3, 3))  # to manipulate the orientation of dilution , large x means horizonatally dilating  more, large y means vertically dilating more
	dilated = cv2.dilate(new_img, kernel, iterations=6)  # dilate , more the iteration more the dilation

	#4) Detect contours
	image, contours, hierarchy = cv2.findContours(dilated,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_NONE)
	
	for contour in contours:
		[x, y, w, h] = cv2.boundingRect(contour)		# get rectangle bounding contour
		# Don't plot small false positives that aren't text
		if (w < 45 and h < 60) or h < 60 or w > 200 or h > 200:
			continue
		# y begin: width, x begin : height
		region = img[y:y+h, x:x+w]
		# Put found text piece on blank image
		blank_image[y:y+h, x:x+w] = region
	
	#5) Grayscale result to ease Tessaract pain
	blank_image = cv2.cvtColor(blank_image, cv2.COLOR_BGR2GRAY)
	_, result_image = cv2.threshold(blank_image, threshold, 255, cv2.THRESH_BINARY)
	
	#6) Erode to make font bigger
	erode_kernel = np.ones((5,5), np.uint8) 
	result_image = cv2.dilate(result_image, erode_kernel, iterations=1)

	#7) Resize & rotate result
	result_image = cv2.resize(result_image, (int(width * 0.6), int(height * 0.6))) 
	rows, cols = result_image.shape
	M = cv2.getRotationMatrix2D((cols/2,rows/2),-6,1)
	result_image = cv2.warpAffine(result_image,M,(cols,rows))

	#8) Reverse result color
	result_image = cv2.bitwise_not(result_image)
	
	#9) Write temp tesseract input file
	result_name = os.getcwd() + '/out/card' + str(index) +'_out.jpg'
	index += 1
	cv2.imwrite(result_name, result_image)
	return result_name

	#cv2.imshow('result', result_image)
	#cv2.waitKey()
