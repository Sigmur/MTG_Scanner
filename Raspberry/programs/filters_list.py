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
import config
from programs import program
from motor import servo

#List current filter configuration

class Handler(program.Program):
	def __init__(self):
		print('List filters settings')
		self.current_filter = 0
		self.filter_datas = config.get('filters', {})
		
	def getName(self):
		return 'Filter list'

	def update(self):
		print('[Filter 0] - Lands only', end='\n')
		print('[Filter 1] - Tokens only', end='\n')
		print('[Filter 2] - Unreadable - missing extention or totaly empty', end='\n')
		for i in range(3, servo.SERVO_TRANSMISSION_SIZE)
			if i in self.filter_datas
				print('[Filter ' + str(i) + '] - ' str(self.filter_datas[i]), end='\n')
			else
				print('[Filter ' + str(i) + '] - Empty', end='\n')
		print('[End of line] - Extention read, but no filter assigend or missing other data', end='\n')
		return True
		
	def stop(self):
		return
