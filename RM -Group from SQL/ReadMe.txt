=========================================================================DIV80==
Group from SQL
GroupFromSQL

Utility application for use with RootsMagic databases

RootsMagic (RM) software uses a SQLite relational database as its data storage
file. Having access to that file via third part tools is a major advantage
to using RM.


=========================================================================DIV80==
Purpose

This utility uses SQL to query the database file and create a RM group in the
RM database independently of RM. Groups may be created with RootsMagic software,
of course, but the types of queries are more limited.

This utility will update one or more RM groups from any SQL query that returns
a list of PersonIDs (RINs).

Also remember, that groups in RM, are always groups of Persons. So if you want
to find all RM facts with a certain characteristic, you need to create a group of
the people that have that fact attached. Once the group is created, you will
need to search each person's edit window for the fact you are interested in.


=========================================================================DIV80==
Backups

IMPORTANT: You should run this script on a copy of your database file until you
have confidence using it and confidence in its results. Or at least have a
current known-good backup.
Assume software developers are fallible and make mistakes, but are not
malevolent.

Similarly, always use a database copy when you are developing your SQL. It's
easy to make unintended database changes in GUI based database manager apps.


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

*  Copy these files and folder from downloaded zip file to the working folder-
      GroupFromSQL.py
      RM-Python-config.ini
      RMpy

*  Create or find a SQL statement that returns the RINs of the people you want
   to put into a group.

*  Edit the file, RM-Python-config.ini (hereinafter referred to as the 
   "config file") in the working folder.

   The utility needs to know where the RM database file is located, the output
   report file name and its location.
   
   The config file also tells the utility what actions to perform.

*  Double click the GroupFromSQL.py file. This displays the black
   command console window and then displays a report file in Notepad.
   At the same time, the group within the database is updated.

*  Return to RootsMagic and examine the group membership.


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
Config file contents and editing

First, some nomenclature. The config file is made up of Sections, Keys, Values and
Comments. The names in square brackets are Section Names that identify the start
of a section. A Section contains Key = Value pairs. Names on the left of
the = sign are Keys. Text on the right side of the = is the Value of the Key.
Comment lines start with # and are only included to help the user read and
understand the file.

For example-

[OPTIONS]
GROUP_NANE = GroupEveryone

#-----------------------------------------------
[GroupEveryone]
SQL_QUERY = SELECT PersonID FROM PersonTable

#-----------------------------------------------

Shown are two sections: "OPTIONS" and "GroupEveryone".

Section "OPTIONS" has one key :"GROUP_NAME" which has the value "GroupEveryone".

Section "GroupEveryone" has one key: "SQL_QUERY" which has the
value "SELECT PersonID FROM PersonTable".

This example, if run with the utility, will update the group GroupEveryone, already 
existing in the database, using the SQL statement show.
The example SQL_QUERY is very simple and fits on the same line as the key name.
Real SQL will be much more complex and require multiple lines.
Each line of a multi line Value must be indented at least one space.

for example:

SQL_QUERY =
   --
   -- selects person whose married name starts with 'sm'
   SELECT pt.personid
   FROM persontable AS pt
   INNER JOIN nametable AS nt ON pt.personid = nt.ownerid
   WHERE nt.nametype = 5    -- married name
   AND nt.surname LIKE 'sm%'

The SQL_QUERY key specifies the SQL statement that will be run.
It must return a set of PersonID's. The statement may begin on the next line,
as above, as long as the SQL lines are all
indented with white space. Blank lines are not allowed.
Use indented SQL comments (--) to add spacing for readability.
# style comments are not allowed in multi line values.


The Group_name value in OPTIONS may also have multiple lines, that is
multiple group names. Each of those group will be updated in the same run
of the utility.

Your config file can contain multiple Sections each with SQL statements.
Only the Sections specified by [OPTIONS] GROUP_NANE will be used. The others
are ignored.


=========================================================================DIV80==
=========================================================================DIV80==
NOTES

*    This utility will not help you write the SQL statement and is not a good
working environment in which to create your SQL statement.
Confirm you query works before running it in this utility. (Or get the SQL from
a source that has confirmed its results. This app is written so that incorrect
SQL will not damage your database, only give groups with unwanted members.)
It is suggested that you write and debug your SQL in a GUI SQLite manager app,
such as "SQLite Expert Personal", the 64bit version, a free app. Several others
are also available.

Note that the SQL statement is run in an environment that does not have the
RMNOCASE collation used by RM for most name type columns. Use "COLLATE NOCASE"
to avoid errors.

*    Due to technical issue regarding RMNOCASE, this utility will not create a
new group. Instead use RM to create the group name before using this utility.
The process is simple-
Open the database in RM,
Click the Command palette icon in the top right corner of the RM window.
Type "Group" and select the "Groups" command.
In the Add New Group window, type the name of the new group and hit Save.
Be sure the name is unique among group names.
Leave the Type set to "Simple" as is the default.

The same Add New Group window can be accessed by clicking the large plus icon in
the groups tab in the "Side View" which by default is on the left.

*    Updating the contents of a group while the database is open in RM works OK.
However, RM lists using group (simple style) filters do not have a refresh button,
so, for example, if you displaying People view filtered by the group that has been
updated, you'll need to switch to another group and then back again to see the
effect of the group having been updated.

*    On some occasions, the utility report file will display a "Database
Locked" message. In that case, close RM and re-run the utility, then re-open 
RM. It's not clear why this sometimes happens, but it is rare. 
For some reason, RM keeps an open transaction which prevents other processes
from making updates.
No database damage has ever been seem after many hundreds of uses. 
"Database locked" is a normal message encountered from SQLite.


Less important notes.

*   RM-Python-config.ini  (the config file)
If there are any non-ASCII characters in the config file then the file must be
saved in UTF-8 format, with no byte order mark (BOM).
The included sample ini file has an accented ä in the first line comment to
force it to be in the correct format.
File format is an option in the "Save file" dialog box in NotePad.

*    I have not tested all SQL statements :)
The utility takes the input SQL and creates a temporary view based on it. If that
fails, an appropriate error is returned. That should protect against SQL that
modifies/deletes data. (This is not tested beyond simple cases.)

*    This utility only changes the GroupsTable in the database

*    This utility creates a temporary view named: PersonIdList_RJO_utils and
deletes it when done.

*    This utility will, if so configured, modify a pre-existing group that may be
important to you. Take care when assigning the group name: [OPTIONS] GROUP_NAME.

*     (For testing) To create a "database locked" situation, start a transaction
in an external SQLite tool, try to run this utility. Will get locked message 
until transaction in SQLite Expert is either committed or RolledBack.



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

Probably the trickiest part of the config file is the GROUP_NAME key.
It may be assigned either a single or multi line value.
Each line of the value should be on a separate line indented with at least 
one blank. An empty line generates an error.
Multi-line values may not contain comment lines (lines starting with a #).

examples-

correct formats-

GROUP_NAME = GroupName1

GROUP_NAME =
  GroupName1

GROUP_NAME = GroupName1
  GroupName2
  GroupName3

GROUP_NAME =
  GroupName1
  GroupName2
  GroupName3


incorrect format- (empty line not allowed)

GROUP_NAME =
  GroupName1

  GroupName2
  GroupName3


incorrect format (not indented)

GROUP_NAME =
GroupName1
GroupName2
GroupName3

incorrect format (no commented lines in the multi line value)

GROUP_NAME =
  GroupName1
 #  GroupName2
  GroupName3


=========================================================================DIV80==
TODO
COLOR:  Consider adding color coding functions.


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
