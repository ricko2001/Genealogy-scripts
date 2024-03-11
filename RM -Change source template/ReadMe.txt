ChangeSourceTemplate
Utility application for use with RootsMagic databases

RootsMagic (RM) software uses a SQLite relational database as its data storage 
file. Having access to that file via third party tools is a major advantage
to using RM.

Purpose
This utility works with structured sources and citations as well as the source 
templates that define them. "Structured" meaning having defined data fields 
used to create footnotes using the sentence language, as opposed to free form.

RM users can create their own source templates. Those users often find that an 
initial source template design needs updating after using it for a time and 
gaining more experience. Changes to the source template are desired, but RM does 
not provide a mechanism to propagate changes to a source template back to 
sources and citations already created from it. That's where this utility comes 
in.

A common use case is to add to or rename the fields of a source template that's
already in use. The work flow using this utility, involves :
* copy the in-use source template (using the "Copy" button in the source 
  templates list window)
* Rename and edit the copy to have the desired fields
* Uses this utility to switch the sources that used the old template
  to instead use the newly created template.

See "All possible Source Template changes" in the Notes section before 
proceeding.

This utility does not modify any source template. It modifies sources and
citations.
This utility does not move data BETWEEN source and citation fields.


======================================================================
Backups

VERY IMPORTANT
This utility makes changes to the RM database file. It can change a
large number of data items in a single run.
You will likely not be satisfied with your first run of the utility and will
want to try again, perhaps several times, each time making changes to your
ini configuration file. You must run this script on a copy of your database file
and have at least several known-good backups.

Once you are satisfied, don't hurry to use the resulting file. Wait a week or so 
and to allow further consideration. Then run the utility with your perfected 
ini file on a copy of your now-current database and then use the modified
database as your normal work file. The week delay will give you time to think
about it. If you start using the newly modified database immediately, you'll
lose work if you miss a problem and have to revert to a backup.


======================================================================
Compatibility

Tested with RootsMagic v9

.exe file version
       Windows 64bit only. Tested with Window 11.

.py file version
       Tested with Python for Windows v3.12   64bit
       The py file has not been tested on MacOS could probably be easily
       modified to work on MacOS with Python version 3 installed.

======================================================================
Overview

This program is what is called a "command line utility". To install and use
the exe single file version:

*  Create a working folder on your disk.

*  With RM closed, make a cop of your main database and put it into the 
   working folder. Never run the utility on you main database directly.

*  Copy these files from the downloaded zip file to the working folder-
      ChangeSourceTemplate.exe
      RM-Python-config.ini

*  Make a copy your main RM database file and move it to the working folder-

*  Edit the supplied text file named "RM-Python-config.ini". (Hereinafter
   referred to, simply, as the "ini file".) The utility needs to know where
   the RM database file is located, the output report file name and location,
   and the various configuration parameters needed to tell the utility what to do.
   Editing the ini file can be done using the Windows NotePad app.

*  Double click the ChangeSourceTemplate.exe file to run the utility and
   generate the report file.

*  Examine the report output file and then, based on the output, go to the 
   next step by editing the ini file and re-running the utility. Repeat.
   A series of validation runs is completed first and then a final run in
   initiated with "MAKE_CHANAGES = on" to actually change the database.

   Details follow below.

--- OR ---

Use the py script file.  

See section below, after the Notes section, entitled-
   "Which to use? Standalone .exe file or .py file"


======================================================================
Running the utility in detail

Create a working folder on your computer that you will not confuse with other folders.

Copy these two required files from the downloaded zip file to the working folder-
      ChangeSourceTemplate.exe
      RM-Python-config.ini

Close RM if it's open (did you make a backup?) and make a copy of your main
database file using file manager. 
Rename the database copy file so that there will not be any chance of confusion. 
Suggestion: name it "TEST.rmtree"

Move the copy into the working folder that you created above.

Edit the RM-config.ini file in the working folder by opening NotePad and thrn
dragging the RM-config.ini file onto the opened NotePad application window.

Look for the section at the top-
[FILE_PATHS]
DB_PATH                  = TEST.rmtree
REPORT_FILE_PATH         = Report_ChangeSourceTemplate.txt

Change the name of the roots magic database file in the line starting with
DB_PATH to that of the file you placed in the working folder. 
If you named it TEST, you're done.
The other line should be OK as is.


Look at the section of the ini file containing options:
[OPTIONS]
CHECK_TEMPLATE_NAMES   = off
LIST_SOURCES           = off
LIST_TEMPLATE_DETAILS  = off
CHECK_MAPPING_DETAILS  = off
MAKE_CHANGES           = off

Confirm all 5 options are set to off.
The first four options tell the utility to execute validation runs. Only the last
option, when "on" will make changes to your database. Either 0 or 1 of the 5 
options may be "on" at a time.
Save the ini file, and leave the file open in the editor.

===========================================DIV50==
Option All = off

Double click the SwitchSourceTemplate.exe file to run it. A black console window
should momentarily open and then close.
A new file, Report_ChangeSourceTemplate.txt, should appear in the working folder
and then automatically open in NotePad. 
Check that there are no error messages listed in the Report file.
If the database file couldn't be found, fix the ini file, save it and re-run
the utility until you get it right.

If the report file did not open in NotePad, read the troubleshooting
section in the NOTES below.

===========================================DIV50==
Option CHECK_TEMPLATE_NAMES = on

Now you know what to expect when running the utility and how to configure the
ini file. You're ready to start, but first, you need to figure out what needs
to be accomplished and tell the utility.

There is a source template in the RM file that is not quite right. You've used
it to create sources, and, because of the template, they're not quite right either.
Check your database and determine the exact name of the not-quite-right template. 

Look at the ini file, still open in NotePad and find the section :

[SOURCE_TEMPLATES]
TEMPLATE_OLD    = Sample_OldTemplateName
TEMPLATE_NEW    = Sample_NewTemplateName

You need to edit the ini file so that Sample_OldTemplateName is replaced with
the exact name of the not-quite-right template The easiest way is to do this is
to find the template in the Source Template List in RM, click the edit button,
and copy the name into the clipboard, then paste into the ini file.

There should also be another source template, that is similar to the not-quite-right
template, but that has the corrections that you want. Find its exact name, as
above, and paste the name into the ini file.
Your ini file in NotePad should now have the new names.

[SOURCE_TEMPLATES]
TEMPLATE_OLD    = not-quite-right template name
TEMPLATE_NEW    = new and improved template name

Now look back at the OPTIONS section of the ini file, and change the line-
CHECK_TEMPLATE_NAMES   = off
to 
CHECK_TEMPLATE_NAMES   = on

Save the file, leave it open in Notepad, double click the utility exe file to
run it. A black console window should momentarily open and then close.
The Report_ChangeSourceTemplate.txt file should automatically open in NotePad. 

Check that there are no error messages listed in the Report file.
If a source template name couldn't be found, fix the ini file, save it and re-run
the utility until you get it right.
A common issue is that template names may an embedded space, a leading or
trailing space.  See NOTES section for details on how to use quote characters to fix.

===========================================DIV50==
Option LIST_SOURCES = on

Now comes the question of which sources should have their SourceTemplate switched.
The usual case will require that all of the sources using the old template should
be switched over to use the new template. Other situations are also possible in
which only a subset of all sources using the old template should be switched over
to the new template.

In the ini files, look for the line:
SOURCE_NAME_LIKE = %

This line specifies the matching pattern that determines the sources to be
switched. Leave it alone for now.

RM does not make it easy to get a list of sources that use a specific template,
so the next utility run will generate that list.

Look at the OPTIONS section of the ini file still open in NotePad, edit these
two lines so they are as shown:
CHECK_TEMPLATE_NAMES   = off
LIST_SOURCES           = on

Save the file, leave it open in Notepad, double click the utility exe file to
run it, etc. The Report_ChangeSourceTemplate.txt file should automatically
open in NotePad. 

Check that there are no error messages listed in the Report file. Yous should
see a list of all sources that were created using the Old Template.
Any or all of these listed sources may be converted to the new template.

If you want to convert all of them, you can go to the next step. If only some
are to be converted, you will need to edit the line SOURCE_NAME_LIKE = % and
rerun the utility to confirm that the correct sources are listed..

Note that SOURCE_NAME_LIKE can specify an exact match or a wildcard match.
The wildcard match may use the two SQL LIKE wildcard characters "%" and "_".
Note that the search is not case sensitive and more than one wildcard character
can be used in a search.
( for additional help, see, for instance:  https://www.sqlitetutorial.net/sqlite-like/ )


===========================================DIV50==
Option LIST_TEMPLATE_DETAILS = on

Now the utility has to be told how the old template relates to the new one.
This is done with the MAPPING key in the ini file.
Remember, many changes can be made to source templates that do not require this utility. 
See the Notes section starting with "All possible Source Template changes".

The mapping will only describe field renaming, field addition and field deletion.

Before the mapping value is edited, it's a good idea to get a clear listing of the fields in both the old and new templates. This can be gotten from the RM Source Template window, but it can be shown very quickly using this utility.

Look at the OPTIONS section of the ini file still open in NotePad, edit these
two lines so they are as shown:
LIST_SOURCES           = off
LIST_TEMPLATE_DETAILS  = on

Save the file, leave it open in Notepad, double click the utility exe file to
run it, etc. The Report_ChangeSourceTemplate.txt file should automatically
open in NotePad. 

Check that there are no error messages listed in the Report file. 
You should see a list of all the fields in the old and new templates.


As part of the process of designing a new template that fixes an old one, it's
a good idea to map out how field names correspond. That is what the mapping
value is.
We'll create the mapping from the information in the report file just created.

Using the built-in source template "Birth Registration, state level" as an example-
The report files lists this-

"source"   Text     "Repository"
"source"   Place     "RepositoryLoc"
"citation"   Text     "Name"
"source"   Text     "Jurisdiction"
"citation"   Text     "Form"
"citation"   Text     "CertificateNo"
"citation"   Date     "Date"

I have created a new template that has some field changes. It's info is-

"source"   Text     "RepositoryName"
"source"   Place     "RepositoryLoc"
"citation"   Text     "PersonName"
"citation"   Text     "Form"
"citation"   Text     "CertificateNo"
"citation"   Date     "Date"
"citation"   Text     "ID-number"

First, I'll take the old template and copy it here, eliminating the type column

"source"        "Repository"
"source"        "RepositoryLoc"
"citation"      "Name"
"source"        "Jurisdiction"
"citation"      "Form"
"citation"      "CertificateNo"
"citation"      "Date"

Now, I'll move sort the source fields from the citation fields. (This is optional)

"source"        "Repository"
"source"        "RepositoryLoc"
"source"        "Jurisdiction"
"citation"      "Name"
"citation"      "Form"
"citation"      "CertificateNo"
"citation"      "Date"

Now I'll take the field name column from the New template listing and place it to the right of the old field.


"source"        "Repository"     "RepositoryName"
"source"        "RepositoryLoc"   "RepositoryLoc"
"source"        "Jurisdiction"
"citation"      "Name"             "PersonName"
"citation"      "Form"             "Form"
"citation"      "CertificateNo"     "CertificateNo"
"citation"      "Date"               "Date"
"citation"                          "ID-number"

Notice that 2 fields have been renamed, a new citation field "ID-number" has been added, and 1 source field "Jurisdiction" has been deleted.
Complete the Mapping by adding the word "NULL" to the middle column for  "ID-number" since there was no such column in the old template and add "NULL"
to the right and column for "Jurisdiction" since that field is to be deleted.

"source"        "Repository"     "RepositoryName"
"source"        "RepositoryLoc"  "RepositoryLoc"
"source"        "Jurisdiction"   "NULL"
"citation"      "Name"           "PersonName"
"citation"      "Form"           "Form"
"citation"      "CertificateNo"  "CertificateNo"
"citation"      "Date"           "Date"
"citation"      "NULL"           "ID-number"


Edit the mapping value in the ini file so that is has this value.
The ini file rows must be indented with at least 1 space.

Mapping = 
  "source"        "Repository"     "RepositoryName"
  "source"        "RepositoryLoc"  "RepositoryLoc"
  "source"        "Jurisdiction"   "NULL"
  "citation"      "Name"           "PersonName"
  "citation"      "Form"           "Form"
  "citation"      "CertificateNo"  "CertificateNo"
  "citation"      "Date"           "Date"
  "citation"      "NULL"           "ID-number"

===========================================DIV50==
Option CHECK_MAPPING_DETAILS = on

Look at the OPTIONS section of the ini file still open in NotePad, edit these
two lines so they are as shown:
LIST_TEMPLATE_DETAILS  = off
CHECK_MAPPING_DETAILS  = on

Save the file, leave it open in Notepad, double click the utility exe file to
run it, etc. The Report_ChangeSourceTemplate.txt file should automatically
open in NotePad. 

Check that there are no error messages listed in the Report file. 
If the mapping checks out as valid, you will see the message:
No problems detected in the specified mapping.

You may get a message saying that one of the fields could not be located.
If so, make the fix in the Mapping and rerun.

If everything checks out, you're ready to make the chnages.

===========================================DIV50==
Option MAKE_CHANGES = on

Look at the OPTIONS section of the ini file still open in NotePad, edit these
two lines so they are as shown:
CHECK_MAPPING_DETAILS  = off
MAKE_CHANGES  = on

Save the file, leave it open in Notepad, double click the utility exe file to
run it, etc. The Report_ChangeSourceTemplate.txt file should automatically
open in NotePad. 

Check that there are no error messages listed in the Report file. 

Open the database in RootsMagic and confirm that the desired changes have been made.

If there are changes that you did not want, make another copy of yor main database file and copy it to the working folder and try again.


======================================================================
======================================================================
NOTES

All possible Source Template changes 
for source templates that are in use by Sources and Citations

These alterations:
    change source template name
    change field type
    change display name of a field
    change brief hint for a field
    change long hint for a field
    change footnote template
    change short footnote template
    change bibliography template
    change order of source fields
may be made at anytime. No bad consequence. The changes will be immediately seen
in all new and existing source and citations. This utility is not needed.

This alteration:
    change order of citation fields
may be made at any time, but existing citations whose citation names were
automatically generated will not be updated with what would be the new
auto generated name using the new order of citation fields.
If this is objectionable, one could open each citation, delete the existing
citation name and let it be auto generated using the new template information.
(Possible task for a new utility app?)

These alterations
    change field name
    add new fields
    delete fields

The following change implies movement of data from a source to a citation 
or vice versa. This could be called "Lumoing" or "Spliting" source info. 
Do not use this utility. (See my site for Lumping utilities) 

Checkbox "This is a source detail field"


If custom templates are defined that use fields that are renamed, those custom template must be updated to match the new names.



Converting a field from say, "name" type to "date" would not make much sense if the field's
existing data actually has name data in it.
If the utility is not used and these changes are made-
Additional fields-- New fields will not be correctly initialized, sentence language will not see the new field as empty when.
Deleted fields-- Old data not removed, but is only hidden.


One could work with just one source at a time by giving the full source name and not including a wild card, say
SOURCE_NAME_LIKE = BIRTH Helen Sauer
The list would include only the one source. After that source is successfully converted, a different source could
be converted in a new  MAKE_CHANGES run. The error checking runs can be skipped since the other parameters are already confirmed as accurate.
If all of the desired Sources can't be found with one value of SOURCE_NAME_LIKE, you can run the utility multiple times with different values of SOURCE_NAME_LIKE. Or, you may consider renaming your source so they fit an easy to find pattern.



===========================================DIV50==
Source fields go to source fields and citation fields go to citation fields.  
New fields in the new source template should be initialized in existing source by doing 
a NULL => field map.
Existing fields that are no longer needed can be deleted by doing a Field => Null mapping.

===========================================DIV50==
For better or for worse SourceTemplate, template field and Fact names in RM can start, end or contain  1 or more blank characters.

If you have this, the map line that contains the odd field name should be entered with each of the three words/names in double quotes, like
  "source"   "field1 "    "field4"


spaces- embedded, leading training and quotes
field names, LIKE string

so this also goes for speciying Sourcetemplate Names in the ini file-
need to use quotes to include spaces.

for names-
TEMPLATE_OLD
TEMPLATE_NEW
SOURCE_NAME_LIKE

can use " for leading and trailing spaces

fields are just renamed
what if removal- rename is wrong?

should really create a new XML and copy data
need to test NULL => field
and
field => NULL



===========================================DIV50==
Don't run MAKE_CHHANGES with the same mapping on a source more than once, unless you have given it some thought
????


===========================================DIV50==
RM does not prevent creation of entries with identical names.
Important for this utility, this includes Sources, Citations, Source Templates and Source Template fields.
If your database has duplicate names for items this utility will operate on, the safest course is to change the name so it's no longer an exact duplicate of another item of the same type.

if there are duplicates in the SourceTemplate names, the utility will complain and make you change the name before it will run.
If you have duplicate field names that are of the same type (source vs citation), I don;t know what to say. You will find odd behavior. Good luck.

Field names
RM allows the names and the field names to contain any character at any position.

SourceTemplate names
RM allows the names to contain any character at any position.

One can say this allows great flexibility, but it also cause complication when one want to, say look up a particular name by typing it in.
If the Name desired happens to end with a space, it will generally be invisible when displayed. So when you type Name as a exact match search term, you may really need to type "Name ".

Note that the value can have embedded spaces.
Space characters between the = and the value are ignored.
If a name contains a leading or trailing space, then enclose the value with
double quotes, as in-
    TEMPLATE_OLD = "MyOdd name "

Leading or trailing spaces in a name is a bad practice. Fix them as you fix
other aspects of your source templates.


===========================================DIV50==

The ini file must be edited to indicate the conversion that should be done.

The task is specified by key value pairs. Here are three Keys-
    TEMPLATE_OLD      =
    TEMPLATE_NEW      =
    SOURCENAME_LIKE   =

Here are examples of three Key-Value pairs-
    TEMPLATE_OLD      = MyOldSorceTemplateName
    TEMPLATE_NEW      = NewTemplate Name
    SOURCENAME_LIKE   = DeathRecord US,NY %




===========================================DIV50==
The default citation name is the concatenation of the contents of the citation fields, separated by semicolons. The order is set by the order of the fields in the Source template.
If field contents are reordered by the mapping in the utility, the default Citation Name will also change, but existing names in existing citations will not be updated. 


===========================================DIV50==
mapping rules
processed in order of the mapping value.

all fields in old and new src templates must be listed, all old on left, all new on right
old source fields can go to new source fields
NULL on left side means that the field on right side will be empty but correctly initialized. Must be used when adding a new field but without moving old data to it.

NULL on right side means the data on left side field will not be used and the old data is deleted.

not all old src fields have to be used. Can map to NULL, in which case data is not carried over.


Check if source names need to be unique	    dups are not prevented, even with same src template
Check if source template names need to be unique	dups are not prevented
Check if field names in Source template need to be unique.	dups are not prevented

check why the first column of mapping is needed.
could determine at runtime that a field is a citation (Source details) field.

The xml for sources is updated
Existing xml read into DOM and manipulated, then saved back

In mapping- can a s-field in old template be mapped to a c-field in new? NO
In mapping- can a c-field in old template be mapped to a s-field in new? NO

in processing, for each source selected in set,
its template is changed and data from previous fields is copied to the new template as mapped. 
Don't have access to any citation fields at this point. Even if had access, which copy of the citation field would be used? 
So cannot "map a c-field in old template to a s-field in new"


!!!!!!!!!!!!!
no need to liste the unchanged fields unless the order is changed-
wait cant't reorder firlds only names that would screw up data


RULE each line describes how a field in the old template will be renamed in the new template
RULE data in a source field can't be renamed so as to make it a citation field (and vice versa)
RULE if the exact same name appears on the 2nd and 3rd column of a row, that row will have no effect.
RULE if the 2nd colum
The kind of template changes that are handled by this utility are covered in the Notes section below.
You are presumably using this utility becase the old and new template differ in their fields.

The template currently in use and the one that will be used will presumably have different fields
If one only changes a source's template in the database, the source will have the fields and data corresponding to the template it was created with the MAPPING key. Note that the MAPPING key is set to a multi line value. The format is three items per line, 
the first being either source or citation. The second is a field name in the Old template and the third is a feild name in the new template

MAPPING = 
  source       Title           NULL
  source       Date            EventDate
  citation     Person          CoupleNames
  citation     BDate           CD
  citation     CD              SrcInfo
  citation     CitationDate    AccessDate
  citation     NULL            NewField

This works as long as the second and remaining lines are indented at least 1 space
and there are no empty lines

What it means

We assume that we want to rename fields to those used in the new template.
We may want to add new empty fields if they exist in the new template
We may want to delete old fields if there is no point to rename them to a field used in new template.

Fields may be in either source or citation. In RM UI, citation fields have a y in column.
All fields are saved as plain text. Their type info is used for display and input.



old is the existing SourceTemplateID specified by the source
SourceNamesLike is the search criteria fed to the SQL LIKE function.
Looks like leading or trailing spaces won't work in search.

The selection by SourceTemplateID is easy, the name Like selection may be an issue.
The script prints out the selected sources (ID and name) to the console.
Confirm that the list is what is desired.

Now double check that a new source template exists and has the properties desired.
run the script with



to list fields of old and new template.
Copy from window and paste into the RM-Python-config.ini.

Organize into a table with whitespace separating columns (tabs, or blanks)
Important- "mapping" is at left margin, subsequent lines are indented all the same amount.



first column specified whether the mapping is for source (no) or citation (y)
second col specifies the field name as it currently exists.
third is the name to use in renaming the first column. 
NULL is a special name. 
in first column, it means add a field with the name specified in the third column.
in the third column, it means delete the field specified in the second column.

This mapping should correspond to the templates being used.
Don't add fields that aren't specified in the new template,
add a fields for all templates specified in the new template.

all three tables have XML data-
SourceTemplateTable		FieldDefs
SourceTable				Fields
CitationTable			Fields

===========================================DIV50==
REPORT_FILE_DISPLAY_APP
Option to automatically open the report file in a display application.
The included ini sample file has this option activated and set to use Windows
NotePad as the display app. Your favorite editor may be substituted.
It can be deactivated by inserting a # character
at the start of the line.

===========================================DIV50==
RM-Python-config.ini  (the ini file)
If there are any non-ASCII characters in the ini file then the file must be
saved in UTF-8 format, with no byte order mark (BOM).
The included sample ini file has an accented ä in the first line comment to
force it to be in the correct format.
File format is an option in the "Save file" dialog box in NotePad.
The [END] section is entirely optional.

ini file path names may be absolute or relative to the current directory.

===========================================DIV50==
Directory structure (optional)
My directory structure, which of course, I recommend 🙂, is-

Genealogy          (top level folder, mine is in my Home folder)
  myRD-DB.rmtree   (my main database file)
  Misc Databases   (folder for other databases I frequently use)
  Exhibits         (folder containing all media files in a folder hierarchy)
  SW               (folder containing various utility apps and the ini file)

===========================================DIV50==
Troubleshooting:
If no report file is generated, look at the black command
console window for error messages that will help you fix the problem.

Error message- ... RM-Python-config.ini file contains a format error ...
The problem is as stated, the solution may be harder to determine.
Start over with the supplied ini file and make sure that works, Then make your
edits one by one to identify the problem.
You may want to look at- https://en.wikipedia.org/wiki/INI_file

A reason that report file cannot be generated is if the specified REPORT_FILE_PATH
cannot be created.
The default value in the supplied ini file should always work.

If no report file is generated and the black command console window closes
before you can read it, try first opening a command line console and then
running the exe or py file from the command line. The window will not close
and you'll be able to read any error messages.


======================================================================
Development Notes   (not needed to use utility)
======================================================================
======================================================================

The XML fields in the source and citation record are just a collection of fieldName-value pairs. 
The order of these pairs in the XML is not significant.
The Template determines the order of the values in the default citation name.
There is no point to reordering the data in the source and citation XML.

===========================================DIV50==

XML tag info
SourceTemplate XML has Field Name, Display Name, Type, Hint, LongHint, and boolean for field is in source or citation.
Sources and Citations have XML that contain only Field Name/Field Value pairs.

===========================================DIV50==
XML format has changed format from v7 to v8

Old style XML  (possibly only remains in built-in SourceTemplate records ?)
...<?xml version="1.0" encoding="UTF-8"?>x0A<root> text </root>c0A
NOTE- when copying from SQLite expert BLOB editor, the leading 3 BOM bytes and line feed 0A byes are copied as periods.

New style
<root> text </root>
No characters outside of root element. (no XML processing statement, no BOM, no line feed chars.

This app-
  Ignores the extraneous info and looks only at the root element.
  Modifies XML in Source and citation records only.
  Can rename a field, can add an empty field, can delete a field.

===========================================DIV50==
Odd cases of XML format found in my database:

Found an odd Fields value in CitationTable.
CitationID 101294 had just <root />
<Root> <Fields> </Fields> </Root>

for citations, found one that had no Fields tag.
So when finding them, got None.
If changed <Root /> to one with fields, works.
Do this happen in other places?
maybe do a search for just <Root > in citations.

Fixed by adding a Fields empty element within Root, then continuing.

Caused by same fields value of <Root />
When looking to remove processing instruction element found in old data, was
looking for start of XML by searching for <Root>, but it wasn't found in this case. So look for "<Root"

===========================================DIV50==
LIKE note from SQLite doc-
The LIKE operator does a pattern matching comparison. The operand to the right of the LIKE operator contains the pattern and the left hand operand contains the string to match against the pattern. A percent symbol ("%") in the LIKE pattern matches any sequence of zero or more characters in the string. An underscore ("_") in the LIKE pattern matches any single character in the string. Any other character matches itself or its lower/upper case equivalent (i.e. case-insensitive matching). Important Note: SQLite only understands upper/lower case for ASCII characters by default. The LIKE operator is case sensitive by default for unicode characters that are beyond the ASCII range. For example, the expression 'a' LIKE 'A' is TRUE but 'æ' LIKE 'Æ' is FALSE. The ICU extension to SQLite includes an enhanced version of the LIKE operator that does case folding across all unicode characters.

If the optional ESCAPE clause is present, then the expression following the ESCAPE keyword must evaluate to a string consisting of a single character. This character may be used in the LIKE pattern to include literal percent or underscore characters. The escape character followed by a percent symbol (%), underscore (_), or a second instance of the escape character itself matches a literal percent symbol, underscore, or a single escape character, respectively.


======================================================================
======================================================================
======================================================================
Which to use? Standalone .exe file or .py file

Decide whether you wish to use the script file (.py) or the executable
file (.exe) version. They produce exactly the same output at the same speed.
Using one does not preclude using the other.

Pro's and Con's

*   The .exe Executable File Version
  Pro:
   The single exe file is all you need. No need to install Python.
  Con:
   The exe file is not human readable.
   A certain amount of trust is required to run a program not distributed
   by a major software publisher. Unknown software from an untrusted source
   could contain mal-ware. Rely on reviews by other users to establish trust.
   Only use the exe file that you downloaded from GitHub.com yourself.

--- OR ---

*   The .py Script File Version
  Pro:
   The script file is easily readable and one can confirm what it does.
   You may want to learn Python and make your own changes to the script
   and be able to use other scripts.
  Con:
   The script version requires an installation of the Python environment to run.
   This is a 100 MB investment in disk space. (Not big for modern day hard disks)


======================================================================
To use the py script version of the app

To install and use the script file version:
*  Install Python for Windows x64  -see immediately below
*  Create a working folder on your disk, perhaps in the same folder
   that contains your RM database.
*  Copy these files from downloaded zip file to the working folder-
      ChangeSourceTemplate.py
      RM-Python-config.ini
*  Edit the ini file in the working folder to specify the locations of the RM
   database file and the output report file. The ini file also specifies the
   input parameters for the fact conversion. See Notes section below.
   The same ini file may be used with either the .exe or .py version of the utility.
*  Double click the ChangeSourceTemplate.py file to run the utility and generate the 
   report file.
*  Examine the report output file.


======================================================================
Python install-
Install Python from the Microsoft Store
or download and install from Python.org web site

From Microsoft Store
Run a command in Windows by pressing the keyboard key combination
"Windows + R", then in the small window, type Python.
Windows store will open in your browser and you will be be shown
the various versions of Python.
Click the Get button for the latest version.

Web site download and install
Download the current version of Python 3, ( or see direct link below
for the current as of this date)
https://www.python.org/downloads/windows/

Click on the link near the top of page. Then ...
Find the link near bottom left side of the page, in the "Stable Releases"
section, labeled "Download Windows installer (64-bit)"
Click it and save the installer.

Direct link to recent (2024-02) version installer-
https://www.python.org/ftp/python/3.12.2/python-3.12.2-amd64.exe

The Python installation requires about 100 Mbytes.
It is easily and cleanly removed using the standard method found in
Windows=>Settings

Run the Python installer selecting all default options.


======================================================================
TODO
*  ?? what would you find useful?


======================================================================
Feedback
The author appreciates comments and suggestions regarding this software.
Richard.J.Otter@gmail.com

Public comments may be made at-
https://github.com/ricko2001/Genealogy-scripts/discussions


Also see:
My website containing other RootsMagic relevant information:
https://RichardOtter.github.io

My Linked-In profile at-
https://www.linkedin.com/in/richardotter/


======================================================================
Distribution
Everyone is free to use this utility. However, instead of
distributing it yourself, please instead distribute the URL
of my website where I describe it- https://RichardOtter.github.io

======================================================================
