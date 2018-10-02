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
import filter
import config
from programs import program
from motor import servo
from mtg import parsing

#Setup filters
#Static filters :
#Filter 0 = land
#Filter 1 = tokens
#Filter 2 = Unreadable
#End of line = Extention read but no matching filter found or missing data

#Check filter max size
#For each avaliable filter, ask filtration methods
#		type=(C|U|R|M|L|T|S|E)	- filter by card type
#		ext=(MM2|MM3....)		- filter by card extention
#		keep					- keep old data or keep blank
#		clear					- set blank

class Handler(program.Program):
	def __init__(self):
		print('Entering filter setup mode')
		self.current_filter = 0
		self.filter_datas = config.get('filters', {})
		for i in range(0, servo.SERVO_TRANSMISSION_SIZE)
			if i not in self.filter_datas
				self.filter_datas[i] = None
		
	def getName(self):
		return 'Filter setup'

	def update(self):
		if self.current_filter >= servo.SERVO_TRANSMISSION_SIZE
			config.set('filters', self.filter_datas)
			print('Filter configuration is over !', end='\n')
			return True
		if self.current_filter == 0:
			print('[Filter 0] Reserved for basic lands.', end='\n')
			self.current_filter += 1
		elif self.current_filter == 1:
			print('[Filter 1] Reserved for tokens.', end='\n')
			self.current_filter += 1
		elif self.current_filter == 2:
			print('[Filter 2] Reserved for unreadable or partially unread cards.', end='\n')
			print('-------------------------------------------------------------', end='\n')
			print('Availiable filtration methods :\ntype=(C|U|R|M|L|T|S|E)\t- filter by card type', end='\n')
			print('type=(C|U|R|M|L|T|S|E)\t- filter by card type', end='\n')
			print('ext=(MM2|MM3....)\t\t- filter by card extention', end='\n')
			print('keep\t\t\t\t\t- keep old data or keep blank', end='\n')
			print('clear\t\t\t\t\t- set blank', end='\n')
			print('You can chain filters ex: "type=C ext=AKH"', end='\n')
			print('-------------------------------------------------------------', end='\n')
			self.current_filter += 1
		else:
			if self.filter_datas[self.current_filter] is not None:
				print('[Filter ' + str(self.current_filter) + '] Current filter data : ' + filter_data)
			else:
				print('[Filter ' + str(self.current_filter) + '] Has no configuration')
			while True:
				print('[Filter ' + str(self.current_filter) + '] Choose your filtration method :', end='\n')
				choice = input("> ")
				if choice == 'keep':
					#Nothing to do
					self.current_filter += 1
					break
				elif choice == 'clear':
					#Set to nothing
					self.filter_datas[self.current_filter] = None
					self.current_filter += 1
					break
				else: #Check if type or extention specified
					filter_infos = {}
					type_result = re.search(r'type=(\w{1})')
					extention_result = re.search(r'ext=(\w{3})')
					
					if (type_result is None and extention_result is None):
						continue
						
					if (type_result is not None):
						type = type_result.group(0).upper()
						if parsing.isValidCardType(type):
							filter_infos['type'] = type
						else:
							print('[Filter ' + str(self.current_filter) + '] Invalid type : ' + type, end='\n')

					if (extention_result is not None):
						extention = extention_result.group(0).upper()
						if parsing.isValidExtention(type):
							filter_infos['extention'] = extention
						else:
							print('[Filter ' + str(self.current_filter) + '] Invalid extention : ' + extention, end='\n')
							
					if len(filter_infos) <= 0:
						continue
					#new filter is ok, save it
					self.filter_datas[self.current_filter] = filter_infos
					self.current_filter += 1
					break
		return False
			
	def stop(self):
		filter.closeAll()
		config.set('filters', self.filter_datas)

