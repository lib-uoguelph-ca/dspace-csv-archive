class Item:
	_attributes = {}

	def	__setattr__(self, name, value):
		self._attributes[name] = value

	def __getattr__(self, attribute):
		ret = None

		if hasattr(self, attribute):
			ret = getattr(self, attribute)
		else:
			if attribute in self._attributes:
				ret = self._attributes[attribute]
			else:
				raise AttributeError("Attribute " + attribute + " does not exist.")
			return ret

	def getAttributes(self):
		return self._attributes

	def __str__(self):
		return str(self._attributes)