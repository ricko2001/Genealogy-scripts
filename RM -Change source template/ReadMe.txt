ChangeSourceTemplate
Utility application for use with RootsMagic databases

RootsMagic (RM) software uses a SQLite relational database as its data storage 
file. Having access to that file via third party tools is a major advantage
to using RM.

Purpose
This utility works with structured Sources and Citations as well as the Source 
Templates that define them. "Structured" meaning having defined data fields 
used to create footnotes using the sentence language, as opposed to free form.

Some users create their own source templates. Those users often find that an 
initial SourceTemplate design needs updating after using it for a time and 
gaining experience. Changes to the source template are desired, but RM does 
not provide a mechanism to back-propagate changes to a source template to 
sources and citations already created from it. That's where this utility comes 
in.

A common use case is to add to or rename the fields of a Source Template that's
already in use. Using this utility, instead of editing the in-use template, one instead :
* copies the in-use SourceTemplate using the RM command
* renames and edits the copy to have the desired fields
* then uses this utility to switch the sources that used the old template
  to instead use the newly created template.
* If the old template is no longer in use, it may be deleted (unless it is
 a built-in template type)


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
   working folder. Never work on you main database directly.

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
   A series of test runs is completed and then a final run with 
   "MAKE_CHANAGES = on" actually changes the database.

   Details follow below.


--- OR ---

Use the py script file.  

See section below, after the Notes section, entitled-
   "Which to use? Standalone .exe file or .py file"


======================================================================


* determine witch source or set of sources should have their SourceTemplates switched.
* examine the existing SourceTemplate and create a new SourceTemplate, probably based on the old one, with the desired changes.
* determine the exact names of the SourceTemplate already in use and the SourceTemplate to be used.
* determine how data described by the existing SourceTemplate will be mapped to the new SourceTemplate.
* edit the RM-Config.ini file to include the information determined above.
* test the RM-Config.ini file values by running the test options in the order they appear.
* run the utility with the MAKE_CHANGES option set to on.
* open the database in RootsMagic
* confirm that the desired changes have been made and no others.
* after careful examination, start using the modified database as your production database.

Create the new source template that fixes  problems in the existing template.
That means you'll need to know:
 * the exact name of the source template currently in use. The "old" source template.
 * the exact name of the source template that the sources should be switched to.  The "new" source template.
*  The set of sources that need to have the source template switched. In my experience, this will be all of the sources that use the old template. Use SOURCE_NAME_LIKE = %
If only some of those source should be converted, they must be selected using the SOURCE_NAME_LIKE using wild card characters. Perhaps they all start with
"MR USA" Use SOURCE_NAME_LIKE = MR USA% to get the list of sources that start with that string and that use the old source template.

 * where data in the fields in the "old" source template should be moved to in the "new" source template. The "mapping".

The new source template needs to be created before running the script. The mapping should also be determined before the running the MakeChanges option.. 
Experience says that the first (several) runs of the script will not give exactly what you want. Each run will give results that will hep you refine the new source template and the mapping from old to new fields.





===========================================DIV50==
Running the utility in detail

Create a working folder on your computer that you will not confuse with other folders.

Copy these two required files from the downloaded zip file to the working folder-
      ChangeSourceTemplate.exe
      RM-Python-config.ini

Close RM if it's open and make a copy of your main database file using file manager. 
Rename the database copy file so that there will not be any chance of confusion. 
I'd name it "TEST.rmtree"

Move the copy into the working folder that you created above.

Edit the RM-config.ini file in the working folder by dragging it onto the opened NotePad application windows.
Look for the section at the top-
[FILE_PATHS]
DB_PATH                  = TEST.rmtree
REPORT_FILE_PATH         = Report_ChangeSourceTemplate.txt

Change the name of the roots magic database file in the line starting with
DB_PATH to that of the file you placed in the working folder.
The other line should be OK.


Look at the section of the ini file containing options:
[OPTIONS]
CHECK_TEMPLATE_NAMES   = off
LIST_SOURCES           = off
LIST_TEMPLATE_DETAILS  = off
CHECK_MAPPING_DETAILS  = off
MAKE_CHANGES           = off

Confirm all 5 options are set to off
Save the ini file, and leave the file open in the editor.

===========================================DIV50==
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
Now you know what to expect when running the utility and how to configure the
ini file. You're ready to start, but first, you need to figure out what needs
to be accomplished and tell the utility.

There is a source template in the RM file that is not quite right. You've used it to create sources, 
and, because of the template, they're not quite right either.
Check your database and determine the exact name of the not-quite-right template. 

Look at the ini file, still open in NotePad and find the section :

[SOURCE_TEMPLATES]
TEMPLATE_OLD    = Sample_OldTemplateName
TEMPLATE_NEW    = Sample_NewTemplateName

You need to edit the ini file so that Sample_OldTemplateName is replaced with the exact name of the not-quite-right template
The easiest way is to do this is to find the template in the Source Template List in RM, click the edit button, and copy the name into the clipboard, then paste into NotePad.

There should also be another source template, that is similar to the not-quite-right template, but has the corrections that you want. Find its exact name, as above, and paste the name into the ini file.
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

===========================================DIV50==

Now comes the question of which sources should have their SourceTemplate switched.
The usual case will require that all of the sources using the old template should be switched over to use the new template.
Other situations are also possible in which only a subset of all sources using the old template should be switched over to the new template.

In the ini files, look for the line:
SOURCE_NAME_LIKE = %

This line specifies the matching pattern that determines the sources to be switched. Leave it alone for now.

RM does not make it easy to get a list of sources that use a specific template, so the
next utility run will generate that list.

Look at the OPTIONS section of the ini file still open in NotePad, edit theses
two lines so they are as shown:
CHECK_TEMPLATE_NAMES   = off
LIST_SOURCES           = on

Save the file, leave it open in Notepad, double click the utility exe file to
run it, etc. The Report_ChangeSourceTemplate.txt file should automatically
open in NotePad. 

Check that there are no error messages listed in the Report file. Yous should
also see a list of all sources that were created using the Old Template.
Any or all of these listed sources may be converted to the new template.

If you want to convert all of them, you can go to the next step. If only some are to be converted, you will
need to edit the line SOURCE_NAME_LIKE = % and rerun the utility to confirm your change.

Note that SOURCE_NAME_LIKE can specify an exact match or a wildcard match.
The wildcard match may use the SQL LIKE wild card characters "%" and "_". Note that the search is not case sensitive.
(for additional help, see:  https://www.sqlitetutorial.net/sqlite-like/  )




The template currently in use and the one that will be used will presumably have differiert fields, type sentences etc.
If one only changes a source's template in the database, the source will have the fields and data corresponding to the template it was created with.

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
===========================================DIV50==
NOTES

Possible Source Template changes for Templates that are in use

The following may be changed at anytime. This utility not needed:
Template Name
Field type
The Display Name of a field
Brief Hint of a field
Long Hint of a field
The order of the Fields
Footnote Template
Short Footnote template
Bibliography templates

The following changes will not be shown in existing sources and citations.
Use this utility:
Field Name
Checkbox "This is a source detail field"
Additional fields
Deleted fields


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


ini file path names may be relative or absolute

===========================================DIV50==
Source fields go to source fields and citation fields go to citation fields.  
New fields in the new source template should be initialized in existing source by doing 
a NULL => field map.
Existing fields that are no longer needed can be deleted by doing a Field => Null mapping.

===========================================DIV50==
For better or for worse SourceTemplate, template field and Fact names in RM can start, end or contain  1 or more blank characters.

If you have this, the map line that contains the odd field name should be entered with each of the three words/names in double quotes, like
  "source"   "field1 "    "field4"


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



Note:
RM does not prevent creation of entries with identical names.
Important for this utility, this includes Sources, Citations, Source Templates and Source Template fields.
If your database has duplicate names for items this utility will operate on, the safest course is to change the name so it's no longer an exact duplicate of another item of the same type.

NOTE
===========================================DIV50==
LIKE note from SQLite doc-
The LIKE operator does a pattern matching comparison. The operand to the right of the LIKE operator contains the pattern and the left hand operand contains the string to match against the pattern. A percent symbol ("%") in the LIKE pattern matches any sequence of zero or more characters in the string. An underscore ("_") in the LIKE pattern matches any single character in the string. Any other character matches itself or its lower/upper case equivalent (i.e. case-insensitive matching). Important Note: SQLite only understands upper/lower case for ASCII characters by default. The LIKE operator is case sensitive by default for unicode characters that are beyond the ASCII range. For example, the expression 'a' LIKE 'A' is TRUE but 'æ' LIKE 'Æ' is FALSE. The ICU extension to SQLite includes an enhanced version of the LIKE operator that does case folding across all unicode characters.

If the optional ESCAPE clause is present, then the expression following the ESCAPE keyword must evaluate to a string consisting of a single character. This character may be used in the LIKE pattern to include literal percent or underscore characters. The escape character followed by a percent symbol (%), underscore (_), or a second instance of the escape character itself matches a literal percent symbol, underscore, or a single escape character, respectively.

===========================================DIV50==
Don't run the same mapping on a source more than once, unless you have given it some thought

===========================================DIV50==

RM does not prevent creation of entries with identical names.
Important for this utility, this includes Sources, Citations, Source Templates and Source Template fields.
If your database has duplicate names for items this utility will operate on, the safest course is to change the name so it's no longer an exact duplicate of another item of the same type.


if there are duplicates in the SourceTemplate names, the utility will complain and make you change the name before it will run.
If you have duplicate field names that are of the same type (source vs citation), I don;t know what to say. You will find odd behavior. Good luck.

===========================================DIV50==
===========================================DIV50==
RootsMagic XML format
XML in fields BLOB has changed format from v7 to v8

Old style XML
...<?xml version="1.0" encoding="UTF-8"?>.
and an 0A at end of BLOB

NOTE- when copying from SQLite expert BLOB editor, the leading 3 BOM bytes and line feed 0A byes are copied as periods.

New style
<root>
text
</root>
no XML processing statement, no BOM, no line feed chars.

NOTE- when copying from SQLite expert BLOB editor, the leading 3 BOM bytes and line feed 0A byes are copied as periods.

This app ignores the extraneous info and looks only at the root element.





======================================================================
NOTES

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

Note that the value can have embedded spaces.
Space characters between the = and the value are ignored.
If a name contains a leading or trailing space, then enclose the value with
double quotes, as in-
    TEMPLATE_OLD = "MyOdd name "

Leading or trailing spaces in a name is a bad practice. Fix them as you fix
other aspects of your source templates.

===========================================DIV50==
SourceTemplate names
RM allows the names and the field names to contain any character at any position.

One can say this allows great flexibility, but it also cause complication when one want to, say look up a particular name by typing it in.
If the Name desired happens to end with a space, it will generally be invisible when displayed. So when you type Name as a exact match search term, you may really need to type "Name ".




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

Similar logic says a c-field in old template cannot be mapped to a s-field in new



===========================================DIV50==
REPORT_FILE_DISPLAY_APP
Option to automatically open the report file in a display application.
The included ini sample file has this option activated and set to use Windows
NotePad as the display app. It can be deactivated by inserting a # character
at the start of the line. Your favorite editor may be substituted.

===========================================DIV50==
RM-Python-config.ini  (the ini file)
If there are any non-ASCII characters in the ini file then the file must be
saved in UTF-8 format, with no byte order mark (BOM).
The included sample ini file has an accented ä in the first line comment to
force it to be in the correct format.
File format is an option in the "Save file" dialog box in NotePad.
The [END] section is entirely optional.

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
If no report file is generated and the black command console window closes
before you can read it, try first opening a command line console and then
running the exe or py file from the command line. The window will not close
and you'll be able to read any error messages.

===========================================DIV50==
Troubleshooting:
Error message- ... RM-Python-config.ini file contains a format error ...
The problem is as stated, the solution may be harder to determine.
You may want to look at- https://en.wikipedia.org/wiki/INI_file

===========================================DIV50==
Development Notes   (not needed to use utility)
===========================================DIV50==

===========================================DIV50==
Odd cases of XML format found:

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
