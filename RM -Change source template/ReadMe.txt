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
not provide a mechanism to propagate changes made to a source template back to
sources and citations already created from it. That's where this utility comes
in.

A common use case is to add to or rename the fields of a source template that's
already in use. The work flow using this utility, involves :
* Be sure that you have a known-good backup of your database.
* Copy the in-use source template (using the "Copy" button in the RM source
  templates list window)
* Rename and edit the Source Template copy to have the desired fields 
* Make a copy of your database and place it in a working folder.
* Uses this utility on the database copy in the working folder to switch the 
  sources that used the old template to instead use the newly created template.

See "All possible Source Template changes" in the Notes section before
proceeding.

This utility does not modify any source template. It modifies sources and
citations.
This utility does not move data BETWEEN source and citation fields. Other
utilities can do that.


=========================================================================DIV80==
Backups

VERY IMPORTANT
This utility makes changes to the RM database file. It can change a large number 
of data items in a single run.
You will likely not be satisfied with your first run of the utility and you will
want to try again, perhaps several times, each time making changes to your
configuration file. You must run this script on a copy of your database file
and have at least several known-good backups.

Once you are satisfied, don't hurry to use the resulting file. Wait a week or so
and to allow further consideration. Then run the utility with your perfected
config file on a copy of your now-current database and then use the modified
database as your normal work file. The week delay will give you time to think
about it. If you start using the newly modified database immediately, you'll
lose work if you miss a problem and have to revert to a backup.


=========================================================================DIV80==
Compatibility

Tested with RootsMagic version 10

.exe file version
       Windows 64bit only. Tested with Window 11.

.py file version
       Tested with Python for Windows v3.12   64bit
       The py file has not been tested on MacOS but could probably be easily
       modified to work on MacOS with Python version 3 installed.

=========================================================================DIV80==
Overview

This program is what is called a "command line utility". To install and use
the exe single file version:

*  Create a working folder on your disk.

*  With RM closed, make a cop of your main database, rename it, and put the copy
   into the working folder. Never run the utility directly on you main database file.

*  Copy these files from the downloaded zip file to the working folder-
      ChangeSourceTemplate.exe
      RM-Python-config.ini

*  Edit the supplied text file named "RM-Python-config.ini". (Hereinafter
   referred to, simply, as the "config file".) The utility needs to know where
   the RM database file is located, the output report file name and location,
   and the various configuration parameters needed to tell the utility what to do.
   Editing the config file can be done using the Windows NotePad app.

*  Double click the ChangeSourceTemplate.exe file to run the utility and
   generate the report file.

*  Examine the report output file and then, based on the output, go to the
   next step by editing the config file and re-running the utility. Repeat.
   A series of validation runs is completed first and then a final run is
   initiated with "MAKE_CHANGES = on" to actually change the database.

   Details follow below.

--- OR ---

Use the py script file.

See section below, after the Notes section, entitled-
   "Which to use? Standalone .exe file or .py file"


=========================================================================DIV80==
Running the utility in detail

=============DIV20==
Create a folder on your computer that you will not confuse with other
folders. It will be referred to as the "working folder".

=============DIV20==
Copy these two required files from the downloaded zip file to the working folder-
      ChangeSourceTemplate.exe
      RM-Python-config.ini

=============DIV20==
Close RM if it's open (did you make a backup?) and make a copy of your main
database file using file manager.
Rename the database copy file so that there will not be any chance of confusion.
Suggestion: name it "TEST.rmtree"

=============DIV20==
Move the copy into the working folder that you created above.

=============DIV20==
Edit the RM-Python-config.ini file in the working folder by opening NotePad and then
dragging the RM-Python-config.ini file onto the opened NotePad application window.

Look for the section at the top-
[FILE_PATHS]
DB_PATH                  = TEST.rmtree
REPORT_FILE_PATH         = Report_ChangeSourceTemplate.txt

Change the name of the roots magic database file in the line starting with
DB_PATH to that of the file you placed in the working folder.
If you named it TEST, you're done.
The other line should be OK as is.

Look at the section of the config file containing options:
[OPTIONS]
CHECK_TEMPLATE_NAMES   = off
LIST_SOURCES           = off
LIST_TEMPLATE_DETAILS  = off
CHECK_MAPPING_DETAILS  = off
MAKE_CHANGES           = off

Confirm all 5 options are set to off.
The first four options tell the utility to execute validation runs. Only the last
option, when "on" will make changes to your database. Either 0 or 1 of the five
options may be "on" at one time in a run of the utility.
Save the config file, and leave the file open in the editor.
NOTE: only the first "on" action will be performed when the utility is run, the 
remaining options are ignored. So always check that only one action is set to on.

=============DIV20==
STEP 0		Option    All options = off

Double click the SwitchSourceTemplate.exe file to run it. A black console window
should momentarily open and then close.
A new file, Report_ChangeSourceTemplate.txt, should appear in the working folder
and then automatically open in NotePad.
Check that there are no error messages listed in the Report file.
If the database file couldn't be found, fix the config file, save it and re-run
the utility until you get it right.

If the report file did not open in NotePad, read the troubleshooting
section in the NOTES below.

=============DIV20==
STEP 1		Option CHECK_TEMPLATE_NAMES = on

Now you know what to expect when running the utility and how to configure the
config file. You're ready to start, but first, you need to figure out what needs
to be accomplished and tell the utility.

There is a source template in the RM file that is not quite right. You've used
it to create sources, and, because of the template, they're not quite right either.
Check your database and determine the exact name of the not-quite-right template.

Look at the config file, still open in NotePad and find the section :

[SOURCE_TEMPLATES]
TEMPLATE_OLD    = Sample_OldTemplateName
TEMPLATE_NEW    = Sample_NewTemplateName

You need to edit the config file so that Sample_OldTemplateName is replaced with
the exact name of the not-quite-right template The easiest way is to do this is
to find the template in the Source Template List in RM, click the edit button,
and copy the name into the clipboard, then paste into the config file.

There should also be another source template, that is similar to the not-quite-right
template, but that has the corrections that you want. Find its exact name, as
above, and paste the name into the config file.
Your config file in NotePad should now have the new names.

[SOURCE_TEMPLATES]
TEMPLATE_OLD    = not-quite-right template name
TEMPLATE_NEW    = new and improved template name

Now look back at the OPTIONS section of the config file, and change the line-
CHECK_TEMPLATE_NAMES   = off
to
CHECK_TEMPLATE_NAMES   = on

Save the file, leave it open in Notepad, double click the utility exe file to
run it. A black console window should momentarily open and then close.
The Report_ChangeSourceTemplate.txt file should automatically open in NotePad.

Check that there are no error messages listed in the Report file.
If a source template name couldn't be found, fix the config file, save it and re-run
the utility until you get it right.
A common issue is that template names may an embedded space, a leading or
trailing space.  See NOTES section for details on how to use quote characters to fix.

=============DIV20==
STEP 2		Option LIST_SOURCES = on

Now comes the question of which sources should have their SourceTemplate switched.
The usual case will require that all of the sources using the old template should
be switched over to use the new template. Other situations are also possible in
which only a subset of all sources using the old template should be switched over
to the new template.

In the config file, look for the line:
SOURCE_NAME_LIKE = %

This line specifies the matching pattern that determines the sources to be
switched. Leave it alone for now.

RM does not make it easy to get a list of sources that use a specific template,
so the next utility run will generate that list.

Look at the OPTIONS section of the config file still open in NotePad, edit these
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


=============DIV20==
STEP 3		Option LIST_TEMPLATE_DETAILS = on

Now the utility has to be told how the old template relates to the new one.
This is done with the MAPPING key in the config file.
Remember, many changes can be made to source templates that do not require this utility.
See the Notes section starting with "All possible Source Template changes".

The mapping will only describe field renaming, field addition and field deletion.

Before the mapping value is edited, it's a good idea to get a clear listing of the fields in both the old and new templates. This can be gotten from the RM Source Template window, but it can be shown very quickly using this utility.

Look at the OPTIONS section of the config file still open in NotePad, edit these
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

source     Text     "Repository"
source     Place    "RepositoryLoc"
citation   Text     "Name"
source     Text     "Jurisdiction"
citation   Text     "Form"
citation   Text     "CertificateNo"
citation   Date     "Date"

I have created a new template that has some field changes. Its info is-

source     Text     "RepositoryName"
source     Place    "RepositoryLoc"
citation   Text     "PersonName"
source     Text     "Jurisdiction"
citation   Text     "Form"
citation   Text     "CertificateNo"
citation   Date     "Date"
citation   Text     "ID-number"

The quotation marks are optional for most names. However names with spaces- either embedded, 
leading or trailing, must be enclosed in double quotes as shown.

First, I'll take the old template and copy it here, eliminating the type column

source        "Repository"
source        "RepositoryLoc"
citation       "Name"
source        "Jurisdiction"
citation      "Form"
citation      "CertificateNo"
citation      "Date"

Now, I'll move the source fields to the top and the citation fields to the bottom.

source         "Repository"
source         "RepositoryLoc"
source         "Jurisdiction"
citation       "Name"
citation       "Form"
citation       "CertificateNo"
citation       "Date"

Now I'll take the field names from the New template listing and place them
on the corresponding line to the right of the old field.


source        "Repository"     "RepositoryName"
source        "RepositoryLoc"   "RepositoryLoc"
source        "Jurisdiction"
citation      "Name"             "PersonName"
citation      "Form"             "Form"
citation      "CertificateNo"    "CertificateNo"
citation      "Date"              "Date"
citation                          "ID-number"

Notice that 2 fields have been renamed, a new citation field "ID-number" has been added, and 1 source field "Jurisdiction" has been deleted.
Complete the Mapping by adding the word NULL to the middle column for  "ID-number" since there was no such column in the old template and add NULL
to the right and column for "Jurisdiction" since that field is to be deleted.

source        "Repository"     "RepositoryName"
source        "RepositoryLoc"  "RepositoryLoc"
source        "Jurisdiction"   NULL
citation      "Name"           "PersonName"
citation      "Form"           "Form"
citation      "CertificateNo"  "CertificateNo"
citation      "Date"           "Date"
citation      NULL           "ID-number"


Add the KEY names above each category of field names

MAPPING_SOURCE =
source        "Repository"     "RepositoryName"
source        "RepositoryLoc"  "RepositoryLoc"
source        "Jurisdiction"   NULL

MAPPING_CITATION =
citation      "Name"           "PersonName"
citation      "Form"           "Form"
citation      "CertificateNo"  "CertificateNo"
citation      "Date"           "Date"
citation      NULL             "ID-number"

Remove the words source at citation at the start of each line.
Insert a ">" character between the columns.
The rows with the field names must be indented with at least 1 space.
All the rows in a value must have the same indentation.
The space between the columns and the ">" is flexible.
There is one or more blank lines at the end of a value (MAPPING_SOURCE
and MAPPING_CITATION) separating it from the next item.

This is the text that has to go into the config file:

MAPPING_SOURCE =
  "Repository"    > "RepositoryName"
  "RepositoryLoc" > "RepositoryLoc"
  "Jurisdiction"  >  NULL


MAPPING_CITATION =
  "Name"          >  "PersonName"
  "Form"          >  "Form"
  "CertificateNo" >  "CertificateNo"
  "Date"          >  "Date"
  NULL            >  "ID-number"


=============DIV20==
STEP 4		Option CHECK_MAPPING_DETAILS = on

Look at the OPTIONS section of the config file still open in NotePad, edit these
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

If everything checks out, you're ready to make the changes.

=============DIV20==
STEP 5		Option MAKE_CHANGES = on

Look at the OPTIONS section of the config file still open in NotePad, edit these
two lines so they are as shown:
CHECK_MAPPING_DETAILS  = off
MAKE_CHANGES  = on

Save the file, leave it open in Notepad, double click the utility exe file to
run it, etc. The Report_ChangeSourceTemplate.txt file should automatically
open in NotePad.

Check that there are no error messages listed in the Report file.

Open the database in RootsMagic and confirm that the desired changes have been made.

If there are changes that you did not want, make another copy of your main
database file and copy it to the working folder and try again.


=========================================================================DIV80==
=========================================================================DIV80==
NOTES

===========================================DIV50==
All possible Source Template changes for source templates
that are already in use by Sources and Citations

These alterations:
*    change source template name
*    change field type
*    change display name of a field
*    change brief hint for a field
*    change long hint for a field
*    change footnote template
*    change short footnote template
*    change bibliography template
*    change order of source fields

May be made at anytime. No negative consequence. The changes will be immediately
seen in all new and existing source and citations. This utility is not needed.
Converting a field type from say, "name" type to "date" would not make much
sense if the field's existing data actually has name data in it. But it can be
done at any time.


This alteration:
*    change order of citation fields

May be made at any time, but existing citations whose citation names were
automatically generated will not be updated with what would be the new
auto generated name using the new order of citation fields.
If this is objectionable, one could open each citation, delete the existing
citation name and let it be auto generated using the new template information.
(Possible task for a new utility app?)


This alteration:
*    change state of check-box ("This is a source detail field")

This change implies movement of data from a source to a citation
or vice versa. This could be called "Lumping" or "Splitting" source info.
Do not use this utility. (See my site for Lumping utilities.)


These alterations:
*    change field name
*    add new fields
*    delete fields

Use this utility to update existing source and citations to the new template
structure.

If the utility is not used and these changes are made:
*    change field name
Data is be invisible when accessed with the new name. The old date remains, but
is hidden.
*    add new fields
New fields will not be correctly initialized, sentence language will not see the
new field as empty when tested by <> in the sentence language.
*    delete fields
Old data not removed, but is only hidden.This is not really a problem, but
it's not tidy.


===========================================DIV50==
Selecting sources to be changed

If the SOURCE_NAME_LIKE variable does not give you the set you need, you can
run the utility multiple times with different values of SOURCE_NAME_LIKE.
Once a source has been updated, it won't show up in future lists because it now
uses a new template and the list only shows sources using the old template.

Or, one could work with just one source at a time by giving the full source name
and not including a wild card, say
SOURCE_NAME_LIKE = BIRTH Helen Sauer
The list would include only the one source. After that source is successfully
converted, a different source could be converted in a new  MAKE_CHANGES run.
The error checking runs can be skipped since the other parameters are already
confirmed as accurate.

Or, you may consider renaming your sources (temporarily ?) so they fit an easy to find pattern.


===========================================DIV50==
Source Template Names and Field Names

For better or for worse source names, source template names, template field names
in RM are not required to be unique and can start with, end with or contain space characters.

If you specify a name in the config file that is not unique, the report file will show the problem. Simply rename the item to make the name unique.
If you have duplicate field names that are of the same type (source vs citation), I don't know what to say. You will find odd behavior. Good luck.

If the template name, field name or SOURCE_NAME_LIKE variable contains a space character at the start or the end it will generally be invisible when displayed. In any case you can quotation marks e.g. "Name ", or " Name" or "My Name".


===========================================DIV50==
Running the utility with MAKE_CHHANGES = off does not make any changes to your
database. You can run it as many times as you need.

===========================================DIV50==
Mapping rules processing

* The mappings are processed in the order that they are listed.

* Each line describes how a field in the old template will be renamed in the new template

* Data in a source field can't be renamed so as to make it a citation field (and vice versa)

* NULL on the left side (old source template) means that the field on right
side will be empty but correctly initialized. Must be used when adding a new
field but without moving old data to it.
In RM v9.1.3, an uninitialized Name-Value pair will not behave as expected in
the footnote sentence language. This may get fixed.

Do not name an existing field as the field for the new source template.
This would create a duplicated name. The app will prevent this but it will stop
the run and a new copy of the database should be used after that.

* NULL on right side means the data on left side field will not be used and the
old name-Value pair is deleted.

* The exact same name on the left and right side means that the mapping will
have no effect.

* If you want to switch names of fields that already exist, be careful
not create a duplicate field in an intermediate step.
The app will prevent this but it will stop the run and a new copy of the
database should be used after that.
Best to make the names slightly different but still distinguishable.
Can accomplish exact name switch, but with two runs of the app with 2 new
templates.

===========================================DIV50==
To help understand how the system works- think of each source and citation
record as having a set of Key-Value pairs.These are the fields.
The source fields are in the source record and vice versa.
When you enter a source/citation, using the template, RM displays the key names
and the user adds the values.
When a footnote needs to be created, RM uses the template to construct it from
the Key-Value pairs.
This app operates on source and citation records. It can-
Rename a Key
Delete a Key-Value pair
Add a new, Key-Value pair with a particular Key and an empty value.-

===========================================DIV50==
RM-Python-config.ini  (the config file)
If there are any non-ASCII characters in the config file then the file must be
saved in UTF-8 format, with no byte order mark (BOM).
The included sample config file has an accented ä in the first line comment to
force it to be in the correct format.
File format is an option in the "Save file" dialog box in NotePad.
The [END] section is entirely optional.

config file path names may be absolute or relative to the current directory.

The MAPPING key takes a multi-line value.
Each line must be indented with at least one space character.
All the rows in a value must have the same indentation.
Each line must have 2 entries- old field, new field
The space between the columns is flexible.
There is one or more blank lines at the end of a value separating it
from the next item.


===========================================DIV50==
REPORT_FILE_DISPLAY_APP
Option to automatically open the report file in a display application.
The included ini sample file has this option activated and set to use Windows
NotePad as the display app. Your favorite editor may be substituted.
It can be deactivated by inserting a # character
at the start of the line.

===========================================DIV50==
Directory structure (optional)
My directory structure, which of course, I recommend 🙂, is-

Genealogy          (top level folder, mine is in my Home folder)
  myRM-DB.rmtree   (my main database file)
  Misc Databases   (folder for other databases I frequently use)
  Exhibits         (folder containing all media files in a folder hierarchy)
  SW               (folder containing various utility apps and the config file)


===========================================DIV50==
Troubleshooting:
If no report file is generated, look at the black command
console window for error messages that will help you fix the problem.

Error message- ... RM-Python-config.ini file contains a format error ...
The problem is as stated, the solution may be harder to determine.
Start over with the supplied config file and make sure that works, Then make your
edits one by one to identify the problem.
You may want to look at- https://en.wikipedia.org/wiki/INI_file

A reason that report file cannot be generated is if the specified REPORT_FILE_PATH
cannot be created.
The default value in the supplied config file should always work.

If no report file is generated and the black command console window closes
before you can read it, try first opening a command line console and then
running the exe or py file from the command line. The window will not close
and you'll be able to read any error messages.


=========================================================================DIV80==
Development Notes   (not needed to use utility)
=========================================================================DIV80==
=========================================================================DIV80==
The XML fields in the source and citation record are just a collection of
FieldName-Value pairs.
The order of these pairs in the XML is not significant.
The Template determines the order of the values in the default citation name.
There is no point to reordering the data in the source and citation XML.

the three tables having source type XML data-
SourceTemplateTable		FieldDefs
SourceTable				Fields
CitationTable			Fields

===========================================DIV50==
XML tag info
SourceTemplate XML has Field Name, Display Name, Type, Hint, LongHint, and boolean for field is in source or citation.
Sources and Citations have XML that contain only Field Name/Field Value pairs.

===========================================DIV50==
details of the XML format has changed format from v7 to v8

Old style XML  (possibly only remains in built-in SourceTemplate records ?)
...<?xml version="1.0" encoding="UTF-8"?>x0A<root> text </root>c0A
NOTE- when copying from SQLite expert BLOB editor, the leading 3 BOM bytes and line feed 0A byes are copied as periods.

New style
<root> text </root>
No characters outside of root element. (no XML processing statement, no BOM, no line feed chars. Much cleaner.

This app-
  Ignores the extraneous info and looks only at the root element.
  Modifies XML in Source and citation records only.
  Can rename a field, can add an empty field, can delete a field.

===========================================DIV50==
Odd cases of XML format found in my database:

Found an odd Fields value in CitationTable.
One Citation had just <root />
Fixed by adding a Fields empty element within Root, then continuing.

To do text search for start of root element, can't look for <Root> because at
least one entry had an empty Root element encoded by: <Root />
So look for "<Root"

===========================================DIV50==
LIKE note from SQLite doc-
The LIKE operator does a pattern matching comparison. The operand to the right of the LIKE operator contains the pattern and the left hand operand contains the string to match against the pattern. A percent symbol ("%") in the LIKE pattern matches any sequence of zero or more characters in the string. An underscore ("_") in the LIKE pattern matches any single character in the string. Any other character matches itself or its lower/upper case equivalent (i.e. case-insensitive matching). Important Note: SQLite only understands upper/lower case for ASCII characters by default. The LIKE operator is case sensitive by default for unicode characters that are beyond the ASCII range. For example, the expression 'a' LIKE 'A' is TRUE but 'æ' LIKE 'Æ' is FALSE. The ICU extension to SQLite includes an enhanced version of the LIKE operator that does case folding across all unicode characters.

If the optional ESCAPE clause is present, then the expression following the ESCAPE keyword must evaluate to a string consisting of a single character. This character may be used in the LIKE pattern to include literal percent or underscore characters. The escape character followed by a percent symbol (%), underscore (_), or a second instance of the escape character itself matches a literal percent symbol, underscore, or a single escape character, respectively.


=========================================================================DIV80==
=========================================================================DIV80==
=========================================================================DIV80==
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


=========================================================================DIV80==
To use the py script version of the app

To install and use the script file version:
*  Install Python for Windows x64  -see immediately below
*  Create a working folder on your disk, perhaps in the same folder
   that contains your RM database.
*  Copy these files from downloaded zip file to the working folder-
      ChangeSourceTemplate.py
      RM-Python-config.ini
*  continue as above, in the section "Running the utility in detail"

=========================================================================DIV80==
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


=========================================================================DIV80==
TODO
*  ?? what would you find useful?


=========================================================================DIV80==
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


=========================================================================DIV80==
Distribution
Everyone is free to use this utility. However, instead of
distributing it yourself, please instead distribute the URL
of my website where I describe it- https://RichardOtter.github.io

=========================================================================DIV80==
