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

#pip install pytesseract
import pytesseract
import PIL
from PIL import Image, ImageFilter

#https://github.com/tesseract-ocr/tesseract/wiki/Command-Line-Usage
TESSERACT_DETECTION_CONFIG = '--psm 3 -l eng+fra'
# Page segmentation modes:
# 0     Orientation and script detection (OSD) only.
# 1     Automatic page segmentation with OSD.
# 2     Automatic page segmentation, but no OSD, or OCR.
# 3     Fully automatic page segmentation, but no OSD. (Default)
# 4     Assume a single column of text of variable sizes.
# 5     Assume a single uniform block of vertically aligned text.
# 6     Assume a single uniform block of text.
# 7     Treat the image as a single text line.
# 8     Treat the image as a single word.
# 9     Treat the image as a single word in a circle.
# 10    Treat the image as a single character.
# 11    Sparse text. Find as much text as possible in no particular order.
# 12    Sparse text with OSD.
# 13    Raw line. Treat the image as a single text line,
# 		bypassing hacks that are Tesseract-specific.

def processImage(path):
	text = pytesseract.image_to_string(Image.open(path), lang=None, config=TESSERACT_DETECTION_CONFIG)
	return text
