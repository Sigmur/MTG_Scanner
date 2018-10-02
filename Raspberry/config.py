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

import json
import io
import os

datas = None

CONFIG_FILE = 'config.json'

def load():
	global datas
	
	#If no file found, never created, init an empty object
	if not os.path.isfile(CONFIG_FILE):
		datas = {}
		return
		
	with open(CONFIG_FILE) as json_data:
		datas = json.load(json_data)

def save():
	global datas
	
	if datas is None:
		return
		
	with io.open(CONFIG_FILE, 'w', encoding='utf8') as outfile:
		json_data = json.dumps(datas, indent=4, separators=(',', ': '), ensure_ascii=False)
		outfile.write(str(json_data))
	
def set(key, value, autosave=True):
	global datas
	
	if datas is None:
		load()
	datas[key] = value
	
	if autosave:
		save()

def get(key, default=None):
	global datas
	
	if datas is None:
		load()
	if key in datas:
		return datas[key]
	return default
