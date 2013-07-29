from item import Item

class ItemFactory:
	header = None

	def __init__(self, header):
		self.header = header

	def newItem(self, values = None):
		item = Item()

		for index, column in enumerate(self.header):
			if values == None:
				setattr(item, column, None)
			else:
				setattr(item, column, values[index])

		return item
