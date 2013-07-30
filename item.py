"""
A representation of an item in DSpace.

An item has a collection of files (aka Bitstreams) and a number of metadata name value pairs. 
"""

import os

class Item:
	def __init__(self):
		self._attributes = {}

	"""
	Get a dict of all attributes.
	"""
	def getAttributes(self):
		return self._attributes

	"""
	Set an attribute value.
	"""
	def setAttribute(self, attribute, value):
		self._attributes[attribute] = value

	"""
	Get an attribute value. 
	"""
	def getAttribute(self, attribute):
		return self._attributes[attribute]

	"""
	Convert the item to a string
	"""
	def __str__(self):
		return str(self._attributes)

	"""
	Get the files (bitstreams) associated with this item.
	This function just returns the file name, with no path.
	"""
	def getFiles(self):
		values = []
		files = self.getAttribute('files').split(',')
		for index, file_name in enumerate(files):
			file = os.path.basename(file_name).strip()
			values.append(file)
		return values

	"""
	Get the files (bitstreams) associated with this item.
	This function returns the file with the full import path.
	"""
	def getFilePaths(self):
		values = []
		files = self.getAttribute('files').split(',')
		for index, file_name in enumerate(files):
			file = file_name.strip()
			values.append(file)
		return values
