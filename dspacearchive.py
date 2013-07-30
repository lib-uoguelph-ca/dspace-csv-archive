import os, csv
from itemfactory import ItemFactory
from shutil import copy

class DspaceArchive:
	items = []
	input_path = None
	input_base_path = "."

	def __init__(self, input_path):
		self.input_path = input_path
		self.input_base_path = os.path.dirname(input_path)

		with open(self.input_path, 'rb') as f:
			reader = csv.reader(f)

			header = reader.next()

			item_factory = ItemFactory(header)

			for row in reader:
				item = item_factory.newItem(row)
				self.addItem(item)

	def addItem(self, item):
		self.items.append(item)

	def getItem(self, index):
		return self.items[index]

	def write(self, dir = "."):
		self.create_directory(dir)

		for index, item in enumerate(self.items):

			#item directory
			name = "item_%03d" % (int(index) + 1)
			item_path = os.path.join(dir, name)
			self.create_directory(item_path)

			#contents file
			self.writeContentsFile(item, item_path)

			#content files (aka bitstreams)
			self.copyFiles(item, item_path);

	def zip(self, dir = None):
		pass

	def create_directory(self, path):
		if not os.path.isdir(path):
			os.mkdir(path)

	def writeContentsFile(self, item, item_path):
		contents_file = open(os.path.join(item_path, 'contents'), "w")

		files = item.getFiles()
		for index, file_name in enumerate(files):
			contents_file.write(file_name)
			if index < len(files):
				contents_file.write("\n")

		contents_file.close()

	def copyFiles(self, item, item_path):
		files = item.getFilePaths()
		for index, file_name in enumerate(files):
			copy(os.path.join(self.input_base_path, file_name), item_path)
