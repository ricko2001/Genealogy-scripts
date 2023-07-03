Group from SQL

RootsMagic (RM) software uses a SQLite database as its main storage. This utility uses SQL
to modify the database file independently of RM.
Groups may be created with Roots Magic software, but the types of queries are limited.
Some group search criteria can be saved and refreshed, but again, the search criteria are limited.

This utility will create and/or update a RM group from any SQL query that returns
a list of PersonIDs (RINs).


======================================================================
Command Line Utility

This application is what is called a command line utility. To use it:

1: Edit the supplied text file named "RM-Python-config.ini".
   The file contains the SQL statement and required configuration settings.

2: Double click the GroupFromSQL.py file. This displays the black command
   console window and at the same time, generates the group.
   The console window displays:
      the full path of the database operated on
      the number of people selected by the SQL
   and then prompts the user to hit the enter key to close the console.
   It will also display and error messages.


======================================================================
Option specification
The example values shown are from the supplied example RM-Python-config.ini file

[OPTIONS]
   RUN_SQL     = yes
   Required to be yes for utility to run.
   ( I'm still considering how to use the same ini file for multiple script files.)

[OPTIONS]
    OPTION_SET_ID = OptGroup_SMITH
    The name of the INI file group of options that will be used
    by the utility to create the group.

[OptGroup_SMITH]
QUERY_GROUP_NAME = GroupSmith
    The name of the RM group to store the results.

[OptGroup_SMITH]
QUERY_GROUP_UPDATE = yes
    The group name may be new or existing.
    If it is new, it will be created.
    If it is existing, the group will be updated only if QUERY_GROUP_UPDATE is set to yes.
    If QUERY_GROUP_UPDATE is set to no, the utility exits without making any changes.

[OptGroup_SMITH]
SQL_QUERY =
    SELECT pt.PersonID
    FROM PersonTable AS pt
    INNER JOIN NameTable AS nt ON pt.PersonID = nt.OwnerID
    WHERE nt.NameType = 5 -- married name
    AND nt.Surname = 'Smith'


     The SQL statement that will be run. It must return a set of PersonID's.
     The statement may begin on the next line, as above, as long as the SQL lines are
     all indented with white space. Either blanks or tabs.
     Blank lines are not allowed. Use indented blank SQL comments (--) to add spacing.

     Your ini file can contain multiple SQL statements and group names. Each is called an option set.
     Only the option set specified by OPTION_SET_ID will be used.


======================================================================
Compatibility
Tested with RootsMagic v9. Should be OK with previous version at least to v7
       Python for Windows v3.11.4   64bit
       unifuzz64.dll (file has no version number defined. see MD5 and file size below)
       Operating system Window 11, 64bit  (Windows 10 OK)
The py file could probably be modified to work on MacOS with Python ver 3+ installed.


======================================================================
Which to use? Standalone .exe file or .py file

Decide whether you wish to use the script file (.py) or the executable file (.exe) version.
They produce exactly the same output at the same speed.

* Executable file Version
Pro:
The single exe file is all you need. No need to install Python.
Con:
The exe file is not human readable.
A certain amount of trust is required to run a program not published by a major software house.
Unknown software from an unknown software author could contain mal-ware.

or

* Script File Version
Pro:
The script file is easily readable and one can confirm what it does
You may want to learn Python and make your own changes to the script.
Con:
The script version requires an installation of the Python environment to run.
This is a 100 MB investment in disk space. (Small for modern day hard disks)


======================================================================
Backups

IMPORTANT: You should run this script on a copy of your database file until you
have some confidence with it. Or at least have a very recent known-good backup.

This script only changes the TagTable and the GroupsTable.
It could, if asked to, update a group that is important to you. Be careful
when assigning QUERY_GROUP_NAME.
A light-weight temporary view is created, but temp views are always removed after disconnect.


======================================================================
Getting Started

To install and use the single file version:
*  Create a working folder on your disk, perhaps in your Documents folder.
*  Copy these files from downloaded zip file to the working folder-
      GroupFromSQL.exe
      RM-Python-config.ini
*  Download the SQLite extension: unifuzz64.dll   -see below
*  Move the unifuzz64.dll file to the working folder
*  Edit the RM-Python-config.ini in the above folder to specify the location of the RM file and
   the unifuzz64.dll file. For the initial setup, you may want to set RUN_SQL  = no
   so that only the database and dll path values are checked. Continue as below.
   This avoids dealing with more than one issue at once. After you solve any path issues, if any,
   set RUN_SQL  = yes and continue onward.
   (To edit, Open NotePad and drag the ini file onto the NotePad window.)
*  Double click the GroupFromSQL.exe file to run the utility.
*  Examine the console window and press enter to dismiss it.
*  Open the database in RM, open the People view window and select the created group as filter.

----
OR
----

To install and use the script file version:
*  Install Python for Windows x64  -see below
*  Create a folder on your disk
*  Copy these files from downloaded zip file to the above folder-
      GroupFromSQL.py
      RM-Python-config.ini
*  Download unifuzz64.dll   -see below
*  Move the unifuzz64.dll file to the above folder
*  Edit the RM-Python-config.ini in the above folder to specify the location of the RM file and
   the unifuzz64.dll file. For the initial setup, you may want to set RUN_SQL  = no
   so that only the database and dll path values are checked. Continue as below.
   This avoids dealing with more than one issue at once. After you solve any path issues, if any,
   set RUN_SQL  = yes and continue onward.
   (To edit, Open NotePad and drag the ini file onto the NotePad window.)
*  Double click the GroupFromSQL.py file to run the script.
*  Examine the console window and press enter to dismiss it.
*  Open the database in RM, open the People view window and select the created group as filter.



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
Find the link near bottom of page, in "Files" section, labeled "Windows installer (64-bit)"
Click it and save the installer.

Direct link to recent (2023-07) version installer-
https://www.python.org/ftp/python/3.11.4/python-3.11.4-amd64.exe

The Python installation requires about 100 Mbytes.
It is easily and cleanly removed using the standard method found in Windows=>Settings

Run the Python installer selecting all default options.


======================================================================
unifuzz64.dll download-

https://sqlitetoolsforrootsmagic.com/wp-content/uploads/2018/05/unifuzz64.dll

above link found in this context-
https://sqlitetoolsforrootsmagic.com/rmnocase-faking-it-in-sqlite-expert-command-line-shell-et-al/

The SQLiteToolsforRootsMagic website has been around for years and is run by a
trusted RM user. Many posts to public RootsMagic user forums mention use of unifuzz64.dll from
the SQLiteToolsforRootsMagic website.

======================================================================
NOTES

*  This utility will not help you write the SQL statement. Confirm you query works before
   running it in this utility. You'll probably want to do that in your favorite SQLite manager app.

*  RM will not recognize a new group created externally after it has loaded the database.
   So if you are creating a new group, you'll have to restart RM or run the
   utility while the database is not loaded.

*  Updating the contents of a group while the database is open in RM works OK. However,
   RM lists using group filters do not have a refresh button, so, for example, if you
   displaying People view filtered by the group that has been updated, you'll need to
   switch to another group and then back again to see the effect of the group having been updated.

*  I have not tested all SQL statements :)
   The utility takes the input SQL and creates a temporary view based on it. If that
   fails, an appropriate error is returned. That should protect against SQL that
   modifies/deletes data. (This is not confirmed beyond simple cases.)

*  RM-Python-config.ini
   If there are any non-ASCII characters in the RM-Python-config.ini file,
   perhaps in a database path, or in ignored objects, then the file must be
   saved in UTF-8 format, with no byte order mark (BOM).
   This is an option in the save dialog box in NotePad.

*   This utility creates a temporary view named: PersonIdList_RJO_utils
    and deletes it when done.

*   MD5 hash values are used to confirm the identity of files.
	MD5 hash							File size		File name
	06a1f485b0fae62caa80850a8c7fd7c2	256,406 bytes	unifuzz64.dll


======================================================================
TODO
Consider possibly operating on existing RM groups and forming intersections, unions etc.

Do some testing on running queries using unifuzz64.dll's version of RMNOCASE on a database
 indexed using RM's version of RMNOCASE. 

Due to RMNOCASE issue, should queries include COLLATE BINARY or COLLATE NOCASE override as in-
SELECT Surname FROM NameTable  
WHERE Surname = 'Öhring'  COLLATE BINARY

Look at possibility of fully populating the new SurnameMP, GivenMP & NicknameMP columns and ...?

======================================================================
Feedback
The author appreciates comments and suggestions regarding this software.
Richard.J.Otter@gmail.com

Public comments may be made at-
https://github.com/ricko2001/Genealogy-scripts/discussions


See my Linked-In profile at-
https://www.linkedin.com/in/richardotter/


======================================================================
