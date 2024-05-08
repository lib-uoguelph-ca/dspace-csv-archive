DSpace CSV Archive
====================
Takes a simple CSV spreadsheet, and a bunch of files and magically turns them into the DSpace Simple Archive format. Supports unicode characters in metadata. The tool will automatically strip unicode characters out of filenames. 

## Requirements
Requires [Python](https://www.python.org/) version 3.8 or greater

## Some simple rules for the CSV spreadsheet
* The first row should be your header, which defines the values you're going to provide. 
* Only one column is mandatory: 'files'. Files can be organized in any way you want, just provide the proper path relative to the CSV file's location.
* Add one column for each metadata element (eg: dc.title)
* The order of the columns does not matter.
* Only dublin core metadata elements are supported (for now).
* Use the fully qualified dublin core name for each element (eg dc.contributor.author).
* Languages can be specified by leaving a space after the element name and then listing the language.
* Separate multiple values for an element by double-pipes (||).
* If your metadata value has a comma in it, put some quotes around it. Eg: "Roses are red, violets are blue".

## Example CSV structure 
<table>
	<tr>
		<th>files</th>
		<th>dc.title en</th>
		<th>dc.contributor.author en</th>
		<th>dc.subject</th>
		<th>dc.type</th>
	</tr>
	<tr>
		<td>something1.pdf||something_else1.pdf</td>
		<td>title 1</td>
		<td>author 1</td>
		<td>subject 1</td>
		<td>Report</td>
	</tr>
	<tr>
		<td>directory/something2.pdf</td>
		<td>"title 2, with comma"</td>
		<td>author 2a||author 2b</td>
		<td>subject 2</td>
		<td>Article</td>
	</tr>
</table>

## Usage 
	./dspace-csv-archive /path/to/input/file.csv

or

	python3 ./dspace-csv-archive /path/to/input/file.csv

If successful, the script will place the processed files into a directory called `output` in whatever directory you were in when you ran your command. 

<div style="border: 1px solid #333; padding: 1em; background-color: #CCC; color: black;">
<strong>Note: </strong>The tool will overwrite any exisitng content in the <code>output</code> directory when it is run. If you want to save the results, copy them somewhere safe before you run the tool a second time. 
</div>

## Importing into DSpace
If it is not already, the directory should be placed in a location that the `dspace` user can access it *and write to the directory*. I recommend putting the directory into `/home/dspace/imported-data/` and leaving it there so the mapfile can be easily found if it is needed later, e.g. to remove or modify imported data. One way to do this is: 

    sudo cp -r [directory-name] /home/dspace/imported-data/
    sudo chown -R dspace:dspace /home/dspace/imported-data/[directory-name]

Now we are ready to use the `import` command that comes with DSpace. Be sure to run this command as the `dspace` user. Something like: 

    [dspace]/bin/dspace import --add --eperson=[importer's email address] --collection=[collection handle] --source=[directory-name] --mapfile=[directory-name]/mapfile

Before running the import, you can validate your import by running the same command above along with the validate argument. This will test the import without actually importing anything and report any issues:

    [dspace]/bin/dspace import --add --valideate --eperson=[importer's email address] --collection=[collection handle] --source=[directory-name] --mapfile=[directory-name]/mapfile

Running the import command without the validate argument will add the items in the directory to the specified collection, and document the operations that were completed in the mapfile. If the import didn't work as you planned, you can use the mapfile to reverse the operations. 

The `mapfile` that's generated as part of this import command is particularly important, and the file that gets generated should be kept along with the rest of the input files. You can use the mapfile to reverse or modify the import using the command-line tools. Please refer to the [DSpace documentation](https://wiki.lyrasis.org/pages/viewpage.action?pageId=104566653) for more information about the DSpace Simple Archive Format or the import/export commands.