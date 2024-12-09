=========================================================================DIV80==
Convert Fact
ConvertFact

Utility application for use with RootsMagic databases

RootsMagic (RM) software uses a SQLite relational database as its data storage
file. Having access to that file via third party tools is a major advantage
to using RM.


=========================================================================DIV80==
Purpose

This utility can convert facts of one fact type to facts of a different fact type.
e.g. "Residence (fam)" to "Residence", or "Census" to "Census 1950".

Simply changing the fact type for an existing fact is trivial using SQL.
Complications arise when a family fact is converted to a Individual fact or when
the fact to be changed has witnesses.
ConvertFact will test all of these cases and guide you.

ConvertFact will not create new fact types or roles. That can't be helpfully
automated and remains a task to be done by the user with RM.

ConvertFact can be configured to convert only a subset of the facts of a certain
fact type based on the date of the fact and/or the description of the fact.

See Notes section for further details.


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

Tested with RootsMagic v10
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
      ConvertFact.py
      RM-Python-config.ini
      RMpy

*  Edit the file, RM-Python-config.ini (hereinafter referred to as the 
   "config file") in the working folder.

   The utility needs to know where the RM database file is located, the output
   report file name and its location.
   
   The config file also tells the utility what actions to perform.


*  Double click the ConvertFact.py file to run the utility and
   generate the report text file. 

*  Examine the report output file and confirm the changes using the RootsMagic app.

   Details follow below.


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
NOTES

===========-
The config file must be edited to indicate the conversion that should be done.

The task is specified by the key value pairs. or example-

[MAPPING]
FACTTYPE_CURRENT  = Census (family)
FACTTYPE_NEW      = Census
ROLE              = Spouse

Note that the value can have embedded spaces.
Space characters between the = and the value are ignored.


===========-
Fact Type name lists

Fact Type full names are listed in RM by the "Fact types" window found in
several places in the RM user interface-
  In the Edit Person window upon clicking the + button (Add fact button or Alt+A)
  In the three dot menu in the Person tab.
  In the command pallet. (type in "fact")

This window also displays, in the right side panel -
* Whether the fact type is Individual or Family.
* The full fact type name and its assigned abbreviation.
The specification of fact types in the config file uses the full fact type name,
not the abbreviation.


===========-
Fact Type fields used

It is best to check the fields used in both fact types before making the change.
If the fields used by the current and new fact types differ (date, place,
description), no data is lost in the conversion.


===========-
Fact types in RM come in two categories: Individual and Family.

Facts of the Individual type are linked to a single person while facts of the
family type are linked to a database family.
An RM database family consists either 2 or 1 persons, labeled internally as
Father and Mother. Either the father or mother may be "unknown"
(and thus set to 0 in the database). Database families, by design, do not
include any offspring.


===========-
Supported fact type conversions:

Individual => Individual
Family => Individual
Family => Family

Not allowed:
Individual => Family


Configuration items in config file required for each type conversion:

* Individual => Individual
FACTTYPE_CURRENT (full name of the fact type of the facts that that should be converted)
FACTTYPE_NEW (full name of the fact type that existing facts should be converted to)
(ROLE is ignored)

* Family => Individual
FACTTYPE_CURRENT
FACTTYPE_NEW
ROLE (name of an existing role associated with the FACTTYPE_NEW)

* Family => Family
FACTTYPE_CURRENT
FACTTYPE_NEW
(ROLE is ignored)


===========-
Limiting which Facts are changed

There maybe situations in which only a subset of Facts should be changed to a new fact type.
One can limit the facts by fields that describe them- the Date and the Description.

Some examples-

[SOURCE_FILTER]
DESC              = %New York%
DATE              = 1930

if you want to convert only facts whose descriptions start with the
words "New York", then enter-

[SOURCE_FILTER]
DESC              = New York%
DATE              =

notice the trailing percent sign.
If the fact descriptions should only contain "New York" somewhere in the text,
enter-

[SOURCE_FILTER]
DESC              = %New York%
DATE              =

The percent sign % wildcard matches any sequence of zero or more characters.
The underscore _ wildcard matches any single character.

To limit the facts converted by their Date, use the DATE value.
The DATE value is always a four digit year.
For example-

[SOURCE_FILTER]
DESC              = 
DATE              = 1930

The values for DESC and DATE are optional. If all facts of a certain type are to be converted,
leave these fields blank-

[SOURCE_FILTER]
DESC              = 
DATE              = 


===========-
Complications handled by this utility

The first complication comes with converting a Family fact to a Individual fact.

A family fact is linked to a father-mother couple. If the father is know, then
the new Individual fact will be linked to the father. If the mother is also known,
the mother will be added as a witness to the new Individual fact. Her role is
specified in the config file as "ROLE =".

If the father is not known then the new Individual fact will be linked to the
mother. There is no new witness added, so the ROLE config file item is ignored.


The second complication arises when the facts of FACTTYPE_CURRENT have witnesses.

Background: Every witness is assigned a role in RM when the fact is shared.
Each fact type has its own set of roles. Many of the roles have the same name,
for instance "Witness" however they are still separate and the sentence assigned
to each of the roles are probably different.

If the original fact type, say Census (fam) had a role named "Spouse", and that
fact type is to be converted to "Census", then the fact of type census will
have the former witness transferred to it maintaining the former role, in this
case "Spouse". If "Census" does not have already have a role named Spouse,
the utility will complain and request that you create such a role for "Census"
before the conversion can be completed.
You don't have to recreate all of the roles that exist for the FACTTYPE_CURRENT,
only the ones that are in use. ConvertFact will tell you which ones.


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


=========================================================================DIV80==
TODO
*  ?? what would you find useful?


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
