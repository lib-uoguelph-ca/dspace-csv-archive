DSpace CSV Archive
====================
Takes a simple CSV spreadsheet, and a bunch of files and magically turns them into the DSpace Simple Archive format. 

Some simple rules: 
-------------------
* The first row should be your header, which defines the values you're going to provide. 
* Only one column is manditory: 'files'. Files can be organized in any way you want, just provide the proper path!
* Add one column for each metadata element (eg: dc.title)
* Only dublin core is supported (for now).
* Languages can be specified by leaving a space after the element name and then listing the language.
* Separate multiple values for an element by semi-colons (;)
* If your metadata value has a comma in it, throw some quotes around it! Eg: "This title, which I made up, has commas"

An Example: 
-----------
<table>
	<tr>
		<th>files</th>
		<th>dc.title en</th>
		<th>dc.contributor.author en</th>
		<th>dc.subject</th>
		<th>dc.type</th>
	</tr>
	<tr>
		<td>something1.pdf; something_else1.pdf</td>
		<td>title 1</td>
		<td>author 1</td>
		<td>subject 1</td>
		<td>Report</td>
	</tr>
	<tr>
		<td>directory/something2.pdf</td>
		<td>"title 2, with comma"</td>
		<td>author 2a; author 2b</td>
		<td>subject 2</td>
		<td>Article</td>
	</tr>
</table>

Usage 
-----
	./dspace-csv-archive.py /path/to/input/file.csv
