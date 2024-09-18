Group from SQL
Utility application for use with RootsMagic databases


RootsMagic (RM) software uses a SQLite relational database as its main storage.
This utility uses SQL to query the database file and create a RM group in the
RM database independently of RM. Groups may be created with RootsMagic software,
of course, but the types of queries are more limited.

This utility will create and/or update a RM group from any SQL query that returns
a list of PersonIDs (RINs).

Also remember, that groups in RM, are always groups of Persons. So if you want
to find all RM facts with a certain characteristic, you need to create a group of
the people that have that fact attached. Once the group is created, you will
need to search each person's edit window for the fact you are interested in.


======================================================================
Overview

This program is what is called a "command line utility".

To use it:

1:  Create or find a SQL statement that returns the RINs of the people you are
interested in putting in a group.

2:  Edit the supplied text file named "RM-Python-config.ini". (Hereinafter
referred to as the "config file".) The utility needs to know where the RM database
file is located, what SQL to use for the query, and the name for the group.
Editing the config file can be done using the Windows NotePad app.

2:  Double click the GroupFromSQL file. This momentarily displays the black
command console window and then displays a report file in Notepad.
At the same time, the group within the database is updated.

3:  Return to RootsMagic and examine the group membership.


======================================================================
Compatibility
Tested with
       RootsMagic v10
       Operating system Window 11, 64bit  (Windows 10 most probably OK)
       Python for Windows v3.12    64bit  (when using the py version)

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

*  Create a new folder on your disk.
   This will be called the working folder.

*  Copy these files from downloaded zip file to the working folder-
      GroupFromSQL.exe
      RM-Python-config.ini

*  Make a copy of your database, move it into the working folder.
   Rename it TEST.rmtree

*  Open the TEST database and create an empty group with the name of your choice
   of Type=Simple. Its contents are not important and as they will be cleared and
   re-populated by the utility.

*  Edit the config file in the working folder to specify the location
   of the RM file, the name of the group and the SQL statement to run.
   See section "config file structure" below for more details.
   To edit, Open NotePad and drag the config file onto the NotePad window.

*  Double click the GroupFromSQL.exe file to run the utility.

*  Examine the report file to confirm success.

*  Open the database in RM, open the People view window and select the created
   group as filter to see the results.

--- OR ---

Use the py script file.  See section below, after the Notes section, entitled-
"Which to use? Standalone .exe file or .py file"


======================================================================
config file structure

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

Section "GroupEveryone" has one key: SQL_QUERY which has the
value "SELECT PersonID FROM PersonTable".

This example, if run with the utility, will update the group GroupEveryone, already existing
in the database, using the SQL statement show.
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

Your config file can contain multiple Sections each with SQL statements.
Only the Section specified by [OPTIONS] GROUP_NANE will be used.


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

Note that the SQL statement is run in an environment that does not have the
RMNOCASE collation used by RM for most name type columns. Use "COLLATE NOCASE"
to avoid errors.

*    Due to technical issue regarding RMNOCASE, this utility will not create a new group.
Instead use RM to create the group name before using this utility.
The process is simple-
Open the database in RM,
Click the Command palette icon in the top right corner of the RM window.
Type "Group" and select the "Groups" command.
In the Add New Group window, type the name of the new group and hit Save.
Be sure the name is unique among group names.
Leave the Type set to "Simple" as is the default.

The same Add New Group window can be accessed by clicking the large plus icon in the groups tab
in the "Side View" which by default is on the left.

*    Updating the contents of a group while the database is open in RM works OK.
However, RM lists using group filters do not have a refresh button, so, for
example, if you displaying People view filtered by the group that has been
updated, you'll need to switch to another group and then back again to see the
effect of the group having been updated.

*    On some occasions, the utility report file will display a "Database
Locked" message. In that case, close RM and re-run the  utility, then re-open 
RM. It's not clear why this sometimes happens, but it is  rare. No database
damage has ever been seem after many hundreds of uses as expected. 
"Database locked" is a normal message encountered from SQLite.


Less important notes.

*    RM-Python-config.ini, the config file.
If there are any non-ASCII characters in the RM-Python-config.ini file,
perhaps in a database path, then the file must be saved in UTF-8 format, with no
byte order mark (BOM). This is an option in the save dialog box in NotePad.

*    I have not tested all SQL statements :)
The utility takes the input SQL and creates a temporary view based on it. If that
fails, an appropriate error is returned. That should protect against SQL that
modifies/deletes data. (This is not tested beyond simple cases.)

*    This utility only changes the GroupsTable in the database

*    This utility creates a temporary view named: PersonIdList_RJO_utils and
deletes it when done.

*    This utility will, if so configured, modify a pre-existing group that is
important to you. Take care when assigning the group name: [OPTIONS] GROUP_NAME.

*     (For testing) To create a "database locked" situation, in SQLite Expert, start a
transaction, try to run this utility. Will get locked message until transaction
in SQLite Expert is either committed or RolledBack.


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
*  Copy these files and folder from downloaded zip file to the above folder-
      GroupFromSQL.py
      RM-Python-config.ini
      RMpy
*  Edit the RM-Python-config.ini in the working folder to specify the location
   of the RM file
   To edit, Open NotePad and drag the config file onto the NotePad window.
*  Double click the GroupFromSQL.exe file to run the utility.
*  Examine the report file text to confirm the successful run.
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
