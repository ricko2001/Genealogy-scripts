Group from SQL
Utility application for use with RootsMagic databases

SEARCH FOR TODO **********************

RootsMagic (RM) software uses a SQLite relational database as its main storage.
This utility uses SQL to query the database file and create a RM group in the 
RM database independently of RM. Groups may be created with RootsMagic software,
of course, but the types of queries are limited.

This utility will create and/or update a RM group from any SQL query that returns 
a list of PersonIDs (RINs).

Also remember, that groups in RM, are always groups of Persons. So if you want 
to find all facts with a certain characteristic, you need to create a group of 
the people that have that fact attached. Once the group is created, you will 
need to search each person's edit window for the fact you are interested in.


======================================================================
Overview

This program is what is called a "command line utility".

To use it:

1:  Create or find a SQL statement that returns the RINs of the people you are 
interested in putting in a group.

2:  Edit the supplied text file named "RM-Python-config.ini". (Hereinafter 
referred to as the "ini file".) The utility needs to know where the RM database 
file is located, the location of the database extension dll file, what SQL to 
use for the query, and the name for the group. Editing the ini file can be done 
using the Windows NotePad app.

2:  Double click the GroupFromSQL file. This momentarily displays the black 
command console window and at the same time, generates the group within the database.
The console window displays:
      * full path of the database operated on,
      * number of people selected by the SQL
      * status of the group
and then prompts the user to hit the enter key to close the console window. It 
will also display any warning/error messages. Read the console window messages
carefully before closing it.

3:  Return to the RootsMagic window and examine the group membership.


======================================================================
Compatibility
Tested with 
       RootsMagic v9.   Not tested with RM 7 or 8.
       unifuzz64.dll (file has no version number defined. see MD5 and file size below)
       Operating system Window 11, 64bit  (Windows 10 most probably OK)
       Python for Windows v3.11.4   64bit  (when using the py version)

The py script file could be modified to work on MacOS with Python ver 3 installed.


======================================================================
Backups

IMPORTANT: You should run this script on a copy of your database file until you
have confidence using it and confidence in its results. Or at least have a 
current known-good backup.
Assume software developers are fallible and make mistakes, but are not 
malevolent.

Similarly, always use a database copy when you are developing your SQL. It's
easy to make unintended database changes in GUI based database manager apps.


======================================================================
Getting Started

To install and use the single .exe file version:

*  Create a working folder on your disk, perhaps in the same folder
   that contains your RM database.

*  Copy these files from downloaded zip file to the working folder-
      GroupFromSQL.exe
      RM-Python-config.ini

*  Download the SQLite extension file: unifuzz64.dll   -see below

*  Move the unifuzz64.dll file to the working folder

*  Edit the RM-Python-config.ini in the working folder to specify the location 
   of the RM file and the unifuzz64.dll file. 
   To edit, Open NotePad and drag the ini file onto the NotePad window.

*  Double click the GroupFromSQL.exe file to run the utility.

*  Examine the console window text and press the enter key to close it.

*  Open the database in RM, open the People view window and select the created
   group as filter to see the results.

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

For example-

#-----------------------------------------------
[OptSet_Sm]
RM_GROUP_NAME = GroupSmith
UPDATE_GROUP  = yes
#-----------------------------------------------


The lines starting with #----- are comments and are only seen by the human 
reader. This is section OptSet_Sm there are 2 keys-RM_GROUP_NAME and UPDATE_GROUP.
key RM_GROUP_NAME has value GroupSmith, key UPDATE_GROUP has value yes.

The example values shown below are from the supplied sample RM-Python-config.ini file
The Section Names and Values with mixed case characters are all examples. Use 
names that make sense to you.  

[OPTIONS]
GROUP_FROM_SQL_OPTION_SET = OptSet_Jones

    The name of the INI file section that contains Key/Values that will be used 
    by this utility to generate the group.


[OptSet_Sm]
RM_GROUP_NAME = OptSet_Jones

    The name of the RM group to store the results.


UPDATE_GROUP = yes

    The group name may be new or preexisting. If it is new, it will be created.
    If it is preexisting, the group will be updated only if UPDATE_GROUP is set
    to yes. If UPDATE_GROUP is set to no, the utility does not make any changes.


SQL_QUERY =
   -- selects person whose married name starts with 'sm'
   select pt.personid
   from persontable as pt
   inner join nametable as nt on pt.personid = nt.ownerid
   where nt.nametype = 5 -- married name
   and nt.surname like 'sm%'


The SQL statement that will be run. It must return a set of PersonID's. The 
statement may begin on the next line, as above, as long as the SQL lines are all
indented with white space. Either blanks or tabs. Blank lines are not allowed. 
Use indented SQL comments (--) to add spacing.

Your ini file can contain multiple Sections each with group names and SQL 
statements. Only the option set specified by GROUP_FROM_SQL_OPTION_SET will be used.


======================================================================
NOTES

*    This utility will not help you write the SQL statement and is not a good 
working environment in which to create your SQL statement. 
Confirm you query works before running it in this utility. (Or get the SQL from
a source that has confirmed its results. This app is written so that incorrect 
SQL will not damage your database, only give groups with unwanted members.)
It is suggested that you write and debug your SQL in a GUI SQLite manager app,
such as "SQLite Expert Personal", the 64bit version, a free app. Several others 
are also available. 

When opening a RM database in a SQL manager app, many of your queries will
require loading the same database extension used by this utility. Use the 64 bit
 version of the extension and the 64 bit version of the SQL manager app. This 
utility is also 64 bit.

*    Not all RM windows will not automatically recognize a new group created by
this utility while the database is loaded. So if you are creating a new group, 
the most straight forward approach is to restart RM or run the utility while the
database is not loaded.
In practice, it is the People list that does not recognize the new group. 
Workaround: open the "Group" tab (in the same panel as the main "Index"), and click
the "Pencil" icon to display the New, Edit, Delete window. Close the window.
This nudges the People list window into seeing the new group.
No issues have been see with updating an existing group. The group always shows 
the current members (unless it is already in use for filtering a list. In that 
case, switch to a different group, and then back.)

*    Updating the contents of a group while the database is open in RM works OK. 
However, RM lists using group filters do not have a refresh button, so, for 
example, if you displaying People view filtered by the group that has been 
updated, you'll need to switch to another group and then back again to see the 
effect of the group having been updated.

*    On some occasions, the utility console window will display a "Database 
Locked" message. In that case. close the console window, close RM and re-run the
 utility, then re-open RM. It's not clear why this sometimes happens, but it is
 rare. No database damage has ever been seem after many hundreds of uses (as 
expected. "Database locked" is a normal message encountered with SQLite.)


Less important notes included for completeness..

*    RM-Python-config.ini, the ini file.
If there are any non-ASCII characters in the RM-Python-config.ini file,
perhaps in a database path, then the file must be saved in UTF-8 format, with no
byte order mark (BOM). This is an option in the save dialog box in NotePad.

*    I have not tested all SQL statements :)
The utility takes the input SQL and creates a temporary view based on it. If that
fails, an appropriate error is returned. That should protect against SQL that
modifies/deletes data. (This is not tested beyond simple cases.)

*    This utility only changes the database tables: TagTable and GroupsTable.

*    This utility creates a temporary view named: PersonIdList_RJO_utils and
deletes it when done.

*    This utility could, if configured to, modify a pre-existing group that is
important to you. Take care when assigning the group name: QUERY_GROUP_NAME.

*     (For testing) To create a "database locked" situation, in SQLite Expert, start a 
transaction, try to run this utility. Will get locked message until transaction
in SQLite Expert is either committed or RolledBack.

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
*  Create a working folder on your disk, perhaps in the same folder
   that contains your RM database.
*  Copy these files from downloaded zip file to the above folder-
      GroupFromSQL.py
      RM-Python-config.ini
*  Download the SQLite extension file: unifuzz64.dll   -see above
*  Move the unifuzz64.dll file to the working folder
*  Edit the RM-Python-config.ini in the working folder to specify the location 
   of the RM file and the unifuzz64.dll file. 
   To edit, Open NotePad and drag the ini file onto the NotePad window.
*  Double click the GroupFromSQL.exe file to run the utility.
*  Examine the console window text and press the enter key to close it.
*  Open the database in RM, open the People view window and select the created
   group as filter to see the results.


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
COLOR:  Consider adding color coding functions.

COLLATION: Do some comparison testing on running queries using unifuzz64.dll's version of
RMNOCASE on a database indexed using RM's version of RMNOCASE. 

COLLATION: Due to RMNOCASE issue, should queries include COLLATE NOCASE override as in-
SELECT Surname FROM NameTable  
WHERE Surname = 'Öhring'  COLLATE NOCASE

COLLATION: Look at possibility of fully populating the new SurnameMP, GivenMP & NicknameMP 
columns and using them in queries to eliminate RMNOCASE.

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
