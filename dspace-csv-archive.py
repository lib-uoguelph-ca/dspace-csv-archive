#!/usr/bin/python

import os, sys

from dspacearchive import DspaceArchive

if len(sys.argv) != 2:
	print("Usage: ./dspace-csv-archive /path/to/input/file.csv")
	sys.exit()

input_file = sys.argv[1]
input_base_path = os.path.dirname(input_file)

archive = DspaceArchive(input_file)
archive.write("./output")

