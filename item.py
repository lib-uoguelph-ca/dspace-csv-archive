"""
A representation of an item in DSpace.

An item has a collection of files (aka Bitstreams) and a number of metadata name value pairs. 
"""

import os, cgi

class Item:
	def __init__(self):
		self._attributes = {}
		self.files = ""

	"""
	Get a dict of all attributes.
	"""
	def getAttributes(self):
		return self._attributes

	"""
	Set an attribute value.
	"""
	def setAttribute(self, attribute, value):
		if attribute == "files":
			self.files = value
		else:
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
		files = self.files.split(',')
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
		files = self.files.split(';')
		for index, file_name in enumerate(files):
			file = file_name.strip()
			values.append(file)
		return values

	def toXML(self):
		output = ""
		output += "<dublin_core>" + os.linesep
		for index, value in self.getAttributes().iteritems():
			tag_open = self.getOpenTag(index)
			tag_close = "</dcvalue>" + os.linesep

			values = value.split(';')

			for val in values:
				output += tag_open
				output += cgi.escape(val.strip(), quote=True)
				output += tag_close
		output += "</dublin_core>" + os.linesep

		return output

	def getOpenTag(self, attribute):
		attribs = attribute.split('.')

		tag_open = ""

		if len(attribs) == 3:
			element = attribs[1]
			qualifier = attribs[2]
			tag_open = '<dcvalue element="%s" qualifier="%s">' % (cgi.escape(element, quote=True), cgi.escape(qualifier, quote=True)) 
			
		elif len(attribs) == 2:
			element = attribs[1]
			tag_open = '<dcvalue element="%s">' % (cgi.escape(element, quote=True)) 

		return tag_open