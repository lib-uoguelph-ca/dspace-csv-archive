import os

class Item:
	def __init__(self):
		self._attributes = {}

	def getAttributes(self):
		return self._attributes

	def setAttribute(self, attribute, value):
		self._attributes[attribute] = value

	def getAttribute(self, attribute):
		return self._attributes[attribute]

	def __str__(self):
		return str(self._attributes)

	def getFiles(self):
		values = []
		files = self.getAttribute('files').split(',')
		for index, file_name in enumerate(files):
			file = os.path.basename(file_name).strip()
			values.append(file)
		return values

	def getFilePaths(self):
		values = []
		files = self.getAttribute('files').split(',')
		for index, file_name in enumerate(files):
			file = file_name.strip()
			values.append(file)
		return values
