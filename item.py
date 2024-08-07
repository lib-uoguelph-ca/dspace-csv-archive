"""
A representation of an item in DSpace.

An item has a collection of files (aka Bitstreams) and a number of metadata name value pairs. 
"""

import os
import re


class Item:
    delimiter = '||'

    def __init__(self, delimiter = b'||'):
        self.delimiter = delimiter
        self._attributes = {}
        self.files = b""

    """
    Get a dict of all attributes.
    """
    def getAttributes(self):
        return self._attributes

    """
    Set an attribute value.
    """
    def setAttribute(self, attribute, value):
        if attribute == b"files":
            self.files = value.encode('utf-8')
        else:
            self._attributes[attribute] = value.encode('utf-8')

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
        files = self.files.split(self.delimiter)
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
        files = self.files.split(self.delimiter)
        for index, file_name in enumerate(files):
            file = file_name.strip()
            values.append(file)
        return values

    """
    Returns an XML represenatation of the item.
    """
    def toXML(self):
        output = b""
        output += b"<dublin_core>" + os.linesep.encode('utf-8')
        for index, value in self.getAttributes().items():
            tag_open = self.getOpenAttributeTag(index)
            tag_close = b"</dcvalue>" + os.linesep.encode('utf-8')

            values = value.split(self.delimiter)

            for val in values:
                if not val:
                    continue

                output += tag_open
                output += self.escape(val.strip())
                output += tag_close
        output += b"</dublin_core>" + os.linesep.encode('utf-8')

        return output

    """
    Get the opening XML tag for a metadata attribute.
    """
    def getOpenAttributeTag(self, attribute):
        lang = self.getAttributeLangString(attribute)
        element = self.getAttributeElementString(attribute)
        qualifier = self.getAttributeQualifierString(attribute)

        tag_open = b'<dcvalue%s%s%s>' % (element, qualifier, lang)

        return tag_open

    """
    Get a string for the key value pair for the lang attribute.
    eg 'language="en"'
    """
    def getAttributeLangString(self, attribute):
        match = re.search(b'_(\\w+)', attribute)

        if match != None:
            return b' language="' + self.escape(match.group(1)) + b'" '
        else:
            return b''

    """
    Strip the language bit off of a metadata attribute.
    """
    def stripAttributeLang(self, attribute):
        attribs = attribute.split(b'_')
        return attribs[0]

    """
    Get a string of the key value pair for the element attribute.
    eg 'element="contributor"'
    """
    def getAttributeElementString(self, attribute):
        attribute = self.stripAttributeLang(attribute)
        attribs = attribute.split(b'.')

        if len(attribs) >= 2:
            return b' element="' + self.escape(attribs[1]) + b'" '
        else:
            return b''

    """
    Get a string the key value pair for the qualifier attribute.
    eg 'qualifier="author"'
    """
    def getAttributeQualifierString(self, attribute):
        attribute = self.stripAttributeLang(attribute)
        attribs = attribute.split(b'.')

        if len(attribs) >= 3:
            return b' qualifier="' + self.escape(attribs[2]) + b'" '
        else:
            return b''
        
    """
    The html.escape function doesn't support unicode strings, so I've just stolen it, 
    made some slight tweaks, and included it here.
    """
    def escape(self, s, quote=False):
        """
        Replace special characters "&", "<" and ">" to HTML-safe sequences.
        If the optional flag quote is true (the default), the quotation mark
        characters, both double quote (") and single quote (') characters are also
        translated.
        """
        s = s.replace(b"&", b"&amp;") # Must be done first!
        s = s.replace(b"<", b"&lt;")
        s = s.replace(b">", b"&gt;")
        if quote:
            s = s.replace(b'"', b"&qubot;")
            s = s.replace(b'\'', b"&#x27;")
        return s