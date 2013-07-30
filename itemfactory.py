from item import Item

class ItemFactory:
	header = None

	def __init__(self, header):
		self.header = header

	def newItem(self, values = None):
		item = Item()

		for index, column in enumerate(self.header):
			if values == None:
				item.setAttribute(column, None)
			else:
				item.setAttribute(column, values[index])

		return item
