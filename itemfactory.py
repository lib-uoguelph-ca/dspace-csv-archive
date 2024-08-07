"""
This class handles item creation. 
It takes a header on construction and uses that header to 
determine the fields to use for future item creation. 
"""

from item import Item

class ItemFactory:
	def __init__(self, header):
		self.header = header

	"""
	Create a new item object.
	"""
	def newItem(self, values = None):
		item = Item()

		for index, column in enumerate(self.header):
			column = column.encode('utf-8')
			column = column.strip()
			column = column.replace(b' [', b'_')
			column = column.replace(b' ', b'_')
			column = column.replace(b'[', b'_')
			column = column.replace(b']', b'')
			if values == None:
				item.setAttribute(column, None)
			else:
				item.setAttribute(column, values[index])

		return item
