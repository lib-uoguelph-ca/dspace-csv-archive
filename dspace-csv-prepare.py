import sys, csv
from itemfactory import ItemFactory

if len(sys.argv) != 2:
	print "Usage: ./dspcae-csv-prepare input-file.csv"
	sys.exit()

with open('test.csv', 'rb') as f:
    reader = csv.reader(f)

    header = reader.next()
    print "Header Row: "
    print header

    item_factory = ItemFactory(header)


    print "Body: "
    for row in reader:
        item = item_factory.newItem(row)
        print item