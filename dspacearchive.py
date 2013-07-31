"""
This class handles the creation of a DSpace simple archive suitable for import into a dspace repository. 

See: http://www.dspace.org/1_6_2Documentation/ch08.html#N15B5D for more information about the DSpace 
Simple Archive format. 
"""

import os, csv
from itemfactory import ItemFactory
from shutil import copy

class DspaceArchive:

	"""
	Constructor:

	The constructor takes a path to a csv file. 
	It then parses the file, creates items, and adds the items to the archive.  
	"""
	def __init__(self, input_path):
		self.items = []
		self.input_path = input_path
		self.input_base_path = os.path.dirname(input_path)

		with open(self.input_path, 'rb') as f:
			reader = csv.reader(f)

			header = reader.next()

			item_factory = ItemFactory(header)

			for row in reader:
				item = item_factory.newItem(row)
				self.addItem(item)

	"""
	Add an item to the archive. 
	"""
	def addItem(self, item):
		self.items.append(item)

	"""
	Get an item from the archive.
	"""
	def getItem(self, index):
		return self.items[index]

	"""
	Write the archie to disk in the format specified by the DSpace Simple Archive format.
	See: http://www.dspace.org/1_6_2Documentation/ch08.html#N15B5D
	"""
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
			self.copyFiles(item, item_path)

			#Metadata file
			self.writeMetadata(item, item_path)

	"""
	Create a zip file of the archive. 
	"""
	def zip(self, dir = None):
		pass

	"""
	Create a directory if it doesn't already exist.
	"""
	def create_directory(self, path):
		if not os.path.isdir(path):
			os.mkdir(path)

	"""
	Create a contents file that contains a lits of bitstreams, one per line. 
	"""
	def writeContentsFile(self, item, item_path):
		contents_file = open(os.path.join(item_path, 'contents'), "w")

		files = item.getFiles()
		for index, file_name in enumerate(files):
			contents_file.write(file_name)
			if index < len(files):
				contents_file.write("\n")

		contents_file.close()

	"""
	Copy the files that are referenced by an item to the item directory in the DSPace simple archive. 
	"""
	def copyFiles(self, item, item_path):
		files = item.getFilePaths()
		for index, file_name in enumerate(files):
			copy(os.path.join(self.input_base_path, file_name), item_path)

	def writeMetadata(self, item, item_path):
		xml = item.toXML()

		metadata_file = open(os.path.join(item_path, 'dublin_core.xml'), "w")
		metadata_file.write(xml)
		metadata_file.close()
