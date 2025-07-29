"""
This class handles the creation of a DSpace simple archive suitable for import into a dspace repository. 

See: http://www.dspace.org/1_6_2Documentation/ch08.html#N15B5D for more information about the DSpace 
Simple Archive format. 
"""

import os, csv
from itemfactory import ItemFactory
from shutil import copy
import unicodedata

class DspaceArchive:

    """
    Constructor:

    The constructor takes a path to a csv file. 
    It then parses the file, creates items, and adds the items to the archive.  
    """
    def __init__(self, input_path):
        self.items = []
        self.input_path = input_path.encode('utf-8')
        self.input_base_path = os.path.dirname(input_path).encode('utf-8')

        with open(self.input_path, 'r', encoding="utf-8-sig") as f:
            reader = csv.reader(f)

            header = next(reader)

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
            name = b"item_%03d" % (int(index) + 1)
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
        contents_file = open(os.path.join(item_path, b'contents'), "wb")

        files = item.getFiles()
        for index, file_name in enumerate(files):
            contents_file.write(self.normalizeUnicode(file_name))
            if index < len(files):
                contents_file.write(b"\n")

        contents_file.close()


    def copyFiles(self, item, item_path):
        """
        Copy the files that are referenced by an item to the item directory in the DSPace simple archive. 
        """

        files = item.getFilePaths()
        for index, file_name in enumerate(files):
            source_path = os.path.join(self.input_base_path, file_name)
            dest_path = os.path.join(item_path, file_name)
            copy(source_path.decode(), self.normalizeUnicode(dest_path).decode())

    def getMetadataSchemas(self): 
        """
        Get a list of the metadata prefixes used in the CSV file.
        """

        keys = self.items[0].getAttributes().keys()
        
        results = []
        for key in keys:
            s = key.split(b'.')[0]
            if s and s not in results:
                results.append(s)

        return results

    def writeMetadata(self, item, item_path):
        """ 
        Write the metadata for an item to an XML file in the item directory.
        This has to happen once for each metadata schema that's used in the file.
        See: https://wiki.lyrasis.org/pages/viewpage.action?pageId=104566653
        """

        self.getMetadataSchemas()
        schemas = self.getMetadataSchemas()

        # For each schema, we create a separate metadata file.
        for schema in schemas:
            xml = item.toXML(schema)

            # Default filename for Dublin Core is dublin_core.xml
            # For other schemas, we use metadata_<schema>.xml
            filename = b"dublin_core.xml"
            if schema != b'dc':
                filename = b"metadata_" + schema + b".xml"

            metadata_file = open(os.path.join(item_path, filename), "wb")
            metadata_file.write(xml)
            metadata_file.close()

    def normalizeUnicode(self, str):
        """
        Normalizes a Unicode string by replacing unicode characters with ascii equivalents.

        Args:
            str (str): The Unicode string to be normalized.

        Returns:
            str: The normalized string encoded as UTF-8.

        """
        cleaned = unicodedata.normalize(u'NFD', str.decode()).encode('ascii', 'ignore')
        return cleaned.decode().encode('utf-8')
