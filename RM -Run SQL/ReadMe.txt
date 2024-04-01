Run SQL
Utility application for use with RootsMagic databases


RootsMagic (RM) software uses a SQLite relational database as its data storage
file. Having access to that file via third party tools is a major advantage
to using RM.

This utility will run one or two SQL statements on a database and display the
results in a report file.

This utility is meant to help the novice SQL user get the task done.
It attempts to eliminate most of the complications found using more 
sophisticated off the shelf software.


======================================================================
Overview

This program is what is called a "command line utility".

To use it:

1:  Create or find or solicit an SQL statement to run. 

2:  Make a copy of your database file and run the utility on this copy.

3.  Edit the supplied text file named "RM-Python-config.ini". (Hereinafter 
referred to as the "ini file".) The utility needs to know where the RM database 
file is located, the location of the database extension dll file if needed,
what SQL to use for the query. Editing the ini file can be done 
using the Windows NotePad app.

4:  Double click the RunSQL file. This momentarily displays the black 
command console window and then displays the report file using Notepad.

5:  If the database was modified, open the database in RootsMagic and
examine the results.


======================================================================
Compatibility
Tested with 
       RootsMagic v9.   Not tested with RM 7 or 8.
       Operating system Window 11, 64bit  (Windows 10 most probably OK)
       Python for Windows v3.11.4   64bit  (when using the py version)
       unifuzz64.dll (file has no version number defined. see MD5 and file size below)

The py script file could be modified to work on MacOS with Python ver 3 installed.


======================================================================
Backups

IMPORTANT: You should run this script on a copy of your database file until you
have confidence using it and confidence in its results. Or at least have a 
several current known-good backups.
Assume software developers are fallible and make mistakes, but are not 
malevolent.

Similarly, always use a database copy when you are developing your SQL.


======================================================================
Getting Started

To install and use the single .exe file version:

*  Create a working folder on your disk, far away from your research database so that
 there will not be confusion.

*  Make a copy of your RM database and place it in the working folder. 
It is suggested that you name the database copy: "TEST.rmtree"

*  Copy these files from downloaded zip file to the working folder-
      RunSQL.exe
      RM-Python-config.ini

*  OPTIONAL if required: Download the SQLite extension file: unifuzz64.dll   -see below
*  OPTIONAL if required: Move the unifuzz64.dll file to the working folder
   Only some SQL operations require the unifuzz64.dll to provide the RMNOCASE collation.
   You will see an error message if it is necessary but not provided.

*  Edit the RM-Python-config.ini in the working folder to specify the location 
   of the RM file. If it's named TEST.rmtree, you're already done.
   OPTIONAL if required:  Specify the path to the unifuzz64.dll file.
   To edit, Open NotePad and drag the ini file onto the NotePad window.

*  Database modification statements should usually be followed by a
   SELECT changes(); statement to display how many rows were changed.

*  Double click the RunSQL.exe file to run the utility.

*  Examine the Report file that was displayed in NotePad.

*  Open the database in RM and review the changes.

--- OR ---

Use the py script file.  See section below, after the Notes section, entitled-
"Which to use? Standalone .exe file or .py file"


======================================================================
unifuzz64.dll download-

direct download:
https://sqlitetoolsforrootsmagic.com/wp-content/uploads/2018/05/unifuzz64.dll

the link above is found in this context-
https://sqlitetoolsforrootsmagic.com/rmnocase-faking-it-in-sqlite-expert-command-line-shell-et-al/

The SQLiteToolsforRootsMagic website has been around for many years and is run 
by a trusted RM user. Many posts to public RootsMagic user forums mention use 
of unifuzz64.dll from the SQLiteToolsforRootsMagic website.


======================================================================
ini file configuration

First, some nomenclature. An ini file is made up of Sections, Keys, Values and 
Comments. The names in square brackets are Section Names that identify the start
of a section. A Section contains Key = Value pairs. Names on the left of 
the = sign are Keys. Text on the right side of the = is the Value of the Key 
at the left. Comment lines start with # and are only included to help the user 
read and understand the file.

The example values shown below are from the supplied sample RM-Python-config.ini file
The unifuzz64.dll/RMNOCASE is not needed for the example.

[SQL]
SQL_STATEMENT_1 =
    UPDATE MediaLinkTable
    SET Include1 = 1, 
        UTCModDate = julianday('now') - 2415018.5
    WHERE OwnerType = 0
    and Include1 <> 1;

SQL_STATEMENT_2 =
    SELECT changes();

The section name is "SQL"
The first Key is "SQL_STATEMENT_1"
Follow the existing format where the Value (statement) begins on the next line.
Each following line of the Value must also be indented with blank characters.
Blank lines within a Value are not allowed. 
Use indented SQL comments (--) to add spacing.

The next Key is "SQL_STATEMENT_2"

Note that the SQL_STATEMENT_1 key is required, while the SQL_STATEMENT_2 key is optional. 


======================================================================
NOTES

*    This utility will not help you write the SQL statement and is not a good 
working environment in which to create your SQL statement. 
Confirm you query works before running it in this utility. (Or get the SQL from
a source that has confirmed its results. 

*    The RMNOCASE collation, provided by the unifuzz64.dll database extension
will be required for many queries. If it is required, but not configured, 
an error message- "no such collation sequence: RMNOCASE" will be displayed in 
the report file. 
To enable it, download the unifuzz64.dll file, place it in the working folder,
remove the "#" character in the ini file at the left of the word RMNOCASE_PATH. 

*    Note that the SQL_STATEMENT_1 key is required, while the SQL_STATEMENT_2 key is optional. If you want to keep a statement in the ini file for future use, but want it inactive, change its key name to SQL_STATEMENT_100  or any number except 1 or 2.
Duplicate key names generate an error.


*    On some occasions, the utility console window will display a "Database 
Locked" message. In that case: Close the console window, Close RM and re-run the
 utility, then re-open RM. It's not clear why this sometimes happens, but it is
 rare. No database damage has ever been seem after many hundreds of uses (as 
expected. "Database locked" is a normal message encountered with SQLite.)


Less important notes included for completeness..

*    RM-Python-config.ini, the ini file.
If there are any non-ASCII characters in the RM-Python-config.ini file,
perhaps in a database path, then the file must be saved in UTF-8 format, with no
byte order mark (BOM). This is an option in the save dialog box in NotePad.

*    MD5 hash values are used to confirm the identity of files.
        MD5 hash							File size		File name
        06a1f485b0fae62caa80850a8c7fd7c2	256,406 bytes	unifuzz64.dll


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

*  Create a working folder on your disk, far away from your research database so that
 there will not be confusion.

*  Make a copy of your RM database and place it in the working folder. 
It is suggested that you name the database copy: "TEST.rmtree"

*  Copy these files from downloaded zip file to the above folder-
      RunSQL.py
      RM-Python-config.ini

*  OPTIONAL if required: Download the SQLite extension file: unifuzz64.dll   -see above
*  OPTIONAL if required: Move the unifuzz64.dll file to the working folder

*  Edit the RM-Python-config.ini in the working folder to specify the location 
   of the RM file and the unifuzz64.dll file. 
   To edit, Open NotePad and drag the ini file onto the NotePad window.

*  Double click the RunSQL.py file to run the utility.

*  Examine the Report file that was displayed in NotePad.

*  Open the database in RM and review the changes.


======================================================================
Python install-
Install Python from the Microsoft Store
or download and install from Python.org web site

From Microsoft Store
Run a command in Windows by pressing the keyboard key combination "Windows + R", then in the small window, type Python.
Windows store will open in your browser and you will be be shown the current version of Python.
Click the Get button.

Web site download and install
Download the current version of Python 3, ( or see direct link below for the current as of this date)
https://www.python.org/downloads/windows/

Click on the link near the top of page. Then ...
Find the link near bottom left side of the page, in the "Stable Releases"
section, labeled "Download Windows installer (64-bit)"
Click it and save the installer.

Direct link to recent (2023-07) version installer-
https://www.python.org/ftp/python/3.11.4/python-3.11.4-amd64.exe

The Python installation requires about 100 Mbytes.
It is easily and cleanly removed using the standard method found in Windows=>Settings

Run the Python installer selecting all default options.


======================================================================
TODO
Consider adding execution of SQL scripts.
Consider fancier formatting of output.
Add ability to add additional database extensions besides RMNOCASE.

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
This is especially true of the exe file version.

======================================================================
