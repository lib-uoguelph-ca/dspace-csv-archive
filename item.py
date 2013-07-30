import os

class Item:
	_attributes = {}

	def	__setattr__(self, name, value):
		self._attributes[name] = value

	def __getattr__(self, attribute):
		if attribute in self._attributes:
			return self._attributes[attribute]
		else:
			raise AttributeError("Attribute " + attribute + " does not exist.")

	def getAttributes(self):
		return self._attributes

	def __str__(self):
		return str(self._attributes)

	def getFiles(self):
		values = []
		files = self.files.split(',')
		for index, file_name in enumerate(files):
			file = os.path.basename(file_name).strip()
			values.append(file)
		return values

	def getFilePaths(self):
		values = []
		files = self.files.split(',')
		for index, file_name in enumerate(files):
			file = file_name.strip()
			values.append(file)
		return values
