=========================================================================DIV80==
Run SQL
RunSQL

Utility application for use with RootsMagic databases

RootsMagic (RM) software uses a SQLite relational database as its data storage
file. Having access to that file via third party tools is a major advantage
to using RM.


=========================================================================DIV80==
Purpose

This utility will run SQL statements and script files on a database 
and display the results in a text file.

This utility is meant to help the novice SQL user get the task done.
It attempts to eliminate most of the complications found using more
sophisticated off the shelf SQLite manager software.

The ability to run SQL script files can be used by even advanced users to
run database maintenance scripts which give predictable results and
don't need to show output.


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
to allow further consideration. Then run the utility with your perfected
config file on a copy of your now-current database and then use the modified
database as your normal work file. The week delay will give you time to think
about it. If you start using the newly modified database immediately, you'll
lose work if you miss a problem and have to revert to a backup.


=========================================================================DIV80==
Compatibility

Tested with RootsMagic v 10
Tested with Python for Windows v3.13   64bit

The py file has not been tested on MacOS but could probably be easily
modified to work on MacOS with Python version 3 installed.


=========================================================================DIV80==
Overview

This program is what is called a "command line utility". 
To install and use the script:

*  Install Python for Windows x64  -see immediately below

*  Create a new folder on your disk.
   This will be called the "working folder".

*  Make a copy of your database, move the copy into the working folder.
   Rename the copy to TEST.rmtree

*  Copy these files and the folder from the downloaded zip file to the working folder-
      RunSQL.py
      RM-Python-config.ini
      RMpy

*  Download the SQLite extension file: unifuzz64.dll   -see below
   (This dll provides a RMNOCASE collation used by RM.)
   Move the unifuzz64.dll file to the working folder.

*  Edit the file, RM-Python-config.ini (hereinafter referred to as the 
   "config file") in the working folder.

   The utility needs to know where the RM database file is located, the output
   report file name and location, the location of the unifuzz64.dll, and the SQL to be executed.

   If you followed the above instructions, all you need to edit is the values of the key
   SQL_STATEMENT_1
   See Notes section, below, for details.

*  Double click the RunSQL.py ile to run the utility and
   generate the report text file. 
   The results of the SQL run will be displayed in NotePad.


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

Direct link to recent (as of 2024-12) version installer-
https://www.python.org/ftp/python/3.13.1/python-3.13.1-amd64.exe

The Python installation requires about 100 Mbytes.
It is easily and cleanly removed using the standard method found in
Windows=>Settings

Run the Python installer selecting all default options.


=========================================================================DIV80==
unifuzz64.dll download-

direct download:
https://sqlitetoolsforrootsmagic.com/wp-content/uploads/2018/05/unifuzz64.dll

the link above is found in this context-
https://sqlitetoolsforrootsmagic.com/rmnocase-faking-it-in-sqlite-expert-command-line-shell-et-al/

The SQLiteToolsforRootsMagic website has been around for many years and is run
by a trusted RM user. Many posts to public RootsMagic user forums mention use
of unifuzz64.dll from the SQLiteToolsforRootsMagic website.


=========================================================================DIV80==
Config file contents and editing

First, some nomenclature. The config file is made up of Sections, Keys, Values and
Comments. The names in square brackets are Section Names that identify the start
of a section. A Section contains Key = Value pairs. Names on the left of
the = sign are Keys. Text on the right side of the = is the Value of the Key.
Comment lines start with # and are only included to help the user read and
understand the file.

For example-

[FILE_PATHS]
DB_PATH         = TEST.rmtree
[SQL]
SQL_STATEMENT_1 = SELECT PersonID FROM PersonTable

Shown are two sections: "FILE_PATHS" and "SQL".

Section "OPTIONS" has one key :"DB_PATH" which has the value "TEST.rmtree".

Section "SQL" has one key: "SQL_STATEMENT_1" which has the
value "SELECT PersonID FROM PersonTable".

This example, if run with the utility, will run the very simple SQL statement
and print out all of the RINs in the database.
The example SQL text is very simple and fits on the same line as the key name.
Real SQL will be more complex and require multiple lines.
Each line of a multi line Value must be indented at least one space.

for example:

[SQL]
SQL_STATEMENT_1 =
    -- simple example sql
    SELECT Given
    FROM NameTable
    WHERE Surname LIKE 'smith';

The SQL_STATEMENT_1  key specifies the SQL statement that will be run.
The statement may begin on the next line, as above, as long as the SQL lines are all
indented with white space. Blank lines are not allowed.
Use indented SQL comments (--) to add spacing for readability.
# style comments are not allowed within multi line values.

Note that the SQL_STATEMENT_1 key is required, while additional SQL_STATEMENTs are optional.

The the app will accept up to 99 SQL statements.-
   SQL_STATEMENT_1
   SQL_STATEMENT_2
   ...
   SQL_STATEMENT_99

This app will also run SQL script files. In this case, the file path is
specified, not the contents.
For example:

[SQL]
SQL_SCRIPT_1 = Maintenance-auto.sql

For this key, always place the file path on the same line as the key name,
as shown in the example.
To specify a second script file to run, add in another key name as:

SQL_SCRIPT_2 =  C:\my script folder\SecondScriptFile.sql

Up to 99 scripts can be run.

If you want none of the SQL Statements to run, just change the name of 
SQL_STATEMENT_1  to anything else, such as:
INACTIVE_SQL_STATEMENT_1 
Since the SQL_STATEMENT_1  won't be found, noen of the other SQL_STATEMENTs 
will run.

Same for SQL script file keys. Renaming SQL_SCRIPT_1 will stop any scripts 
from running.


=========================================================================DIV80==
NOTES

===========-
*  IMPORTANT
   If your SQL makes any **changes** to an RMONCASE collated column, you must
   run the SQL:
   REINDEX RMNOCASE;
   as SQL_STATEMENT_1 or at the start of your script file. 
   Put your updating SQL in following statements. After running the SQL,
   IMPORTANT- run the RM "Rebuild Indexes" tool immediately after opening
   the modified database in RM.

   For fully reliable results, any queries using RMONCASE collated columns
   should be coded to use the SQLite built-in NOCASE collation, as above,
   Start with REINDEX RMNOCASE; do the query and then run the RM "Rebuild 
   Indexes" tool immediately after opening the modified database in RM.


*  Database modification statements should usually be followed by a
   SELECT changes(); statement to display how many rows were changed.


*    This utility will not help you write the SQL statement and is not a good
working environment in which to create your SQL statement.
Confirm you query works before running it in this utility. (Or get the SQL from
a source that has confirmed its results.)



Less important notes included for completeness..

===========-
REPORT_FILE_DISPLAY_APP

Option to automatically open the report file in a display application.
The included ini sample file has this option activated and set to use Windows
NotePad as the display app. It can be deactivated by inserting a # character
at the start of the line. Your favorite editor may be substituted.

===========-
RM-Python-config.ini  (the config file)

If there are any non-ASCII characters in the config file then the file must be
saved in UTF-8 format, with no byte order mark (BOM).
The included sample config file has an accented ä in the first line comment to
force it to be in the correct format.
File format is an option in the "Save file" dialog box in NotePad.

===========-
MD5 authentication of unifuzz64.dll

 MD5 hash values are used to confirm the identity of files.
 MD5 hash                            File size         File name
 06a1f485b0fae62caa80850a8c7fd7c2    256,406 bytes    unifuzz64.dll


=========================================================================DIV80==
=========================================================================DIV80==
=========================================================================DIV80==
Troubleshooting:

=========-
No Report File displayed

If the report is created, but not displayed, check the config
file line- REPORT_FILE_DISPLAY_APP

If no report file is generated, look at the black command
console window for error messages that will help you fix the problem.
There may be something wrong with the config file line- REPORT_FILE_PATH

If the black console windows displays the message-
RM-Python-config.ini file contains a format error
See the section below.

If no report file is generated and the black command console window closes
before you can read it, try first opening a command line console and then
running the exe or py file from the command line. The window will not close
and you'll be able to read any error messages.

=========-
Error message:
RM-Python-config.ini file contains a format error

Start over with the supplied config file and make sure that works, Then make your
edits one by one to identify the problem.
You may want to look at- https://en.wikipedia.org/wiki/INI_file

Probably the trickiest part of the config file is the SQL section.
The SQL_STATEMENT_1 and SQL_STATEMENT_2 keys are multi-line values.
Each line of the value should be on a separate line indented with at least
one blank. An empty line generates an error.
Multi-line values may not contain comment lines (lines starting with a #).

examples-

correct format-

[SQL]
SQL_STATEMENT_1 =
   SELECT pt.personid
   FROM persontable AS pt
   INNER JOIN nametable AS nt ON pt.personid = nt.ownerid
   WHERE nt.nametype = 5    -- married name
   AND nt.surname LIKE 'sm%'



incorrect format- (empty line not allowed)

[SQL]
SQL_STATEMENT_1 =
   SELECT pt.personid
   FROM persontable AS pt

   INNER JOIN nametable AS nt ON pt.personid = nt.ownerid
   WHERE nt.nametype = 5    -- married name
   AND nt.surname LIKE 'sm%'


incorrect format (not indented)

[SQL]
SQL_STATEMENT_1 =
SELECT pt.personid
FROM persontable AS pt
INNER JOIN nametable AS nt ON pt.personid = nt.ownerid
WHERE nt.nametype = 5    -- married name
AND nt.surname LIKE 'sm%'


incorrect format- (no comments allowed)

[SQL]
SQL_STATEMENT_1 =
   SELECT pt.personid
   # this is an non-allowed comment line
   FROM persontable AS pt
   INNER JOIN nametable AS nt ON pt.personid = nt.ownerid
   WHERE nt.nametype = 5    -- married name
   AND nt.surname LIKE 'sm%'


incorrect format- (empty line not allowed)

[SQL]
SQL_STATEMENT_1 =

   SELECT pt.personid
   FROM persontable AS pt
   INNER JOIN nametable AS nt ON pt.personid = nt.ownerid
   WHERE nt.nametype = 5    -- married name
   AND nt.surname LIKE 'sm%'


*    On some occasions, the utility console window will display a "Database
Locked" message. In that case: Close the console window, Close RM and re-run the
 utility, then re-open RM. "Database locked" is a normal message encountered with SQLite.)


=========================================================================DIV80==
TODO
Consider adding execution of SQL scripts.
Consider fancier formatting of output.
Add ability to add additional database extensions besides RMNOCASE.


=========================================================================DIV80==
Feedback
The author appreciates comments and suggestions regarding this software.
RichardJOtter@gmail.com

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
