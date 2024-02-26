ConvertFact
Utility application for use with RootsMagic databases

RootsMagic (RM) software uses a SQLite relational database as its data storage
file. Having access to that file via third party tools is a major advantage
to using RM.

This utility can convert facts of one fact type to facts of a different fact type. 
e.g.  "Residence (fam)" to "Residence", or "Census" to "Census 1950". 

Simply changing the fact type for an existing fact is trivial using SQL.
Complications arise when a family fact is converted to a personal fact or when
the fact to be changed has witnesses.
ConvertFact will test all of these cases and guide you.

ConvertFact will not create new fact types or roles. That can't be helpfully 
automated and remains a task to be done by the user.

ConvertFact can be configured to convert only a subset of the facts of a certain
fact type based on the date of the fact and/or the description of the fact.

See Notes section for further details.

======================================================================
Overview

This program is what is called a "command line utility".

To use it:

1:  Edit the supplied text file named "RM-Python-config.ini". (Hereinafter
    referred to, simply, as the "ini file".)
    The utility needs to know where the RM database file is located, which
    fact type to change, and where to create the report file etc..
    Editing the ini file can be done using the Windows NotePad app.

2:  Double click the ConvertFact program file. This momentarily displays the
    black command console window and at the same time, generates the report
    text file.

3:  Examine the generated report text file that was opened in Notepad.
    The file will contain a summary of the changes made.


======================================================================
Backups

VERY IMPORTANT
This utility makes changes to the RM database file. It can change a
large number of data items in a single run.
You must run this script on a copy of your database file or at least
have several known-good backups.
You will likely not be satisfied with your first run of the utility and will
want to try again, perhaps several times.
Once you are satisfied, don't hurry to use the resulting file. Wait a week and
then run the utility on a copy of your then-current database and then use the
modified database as your normal work file. The week delay will give you time
to think about the process.


======================================================================
Compatibility

Tested with RootsMagic v9

.exe file version
       Windows 64bit only. Tested with Window 11.

.py file version
       Tested with Python for Windows v3.12   64bit
       The py file has not been tested on MacOS.
       The script could probably be modified to work on MacOS with Python
       version 3 installed.

======================================================================
Getting Started

To install and use the exe single file version:

*  Create a working folder on your disk, perhaps in the same folder
   that contains your RM database.

*  Copy these files from the downloaded zip file to the working folder-
      ConvertFact.exe
      RM-Python-config.ini

*  Edit the ini file in the working folder to specify the locations of the RM
   database file and the output report file. The ini file also specifies the
   input parameters for the fact conversion. See Notes section below.

*  Double click the ConvertFact.exe file to run the utility and
   generate the report file.

*  Examine the report output file and confirm the changes using the RootsMagic app.


--- OR ---

Use the py script file.  

See section below, after the Notes section, entitled-
   "Which to use? Standalone .exe file or .py file"


======================================================================
NOTES

===========================================DIV50==
The ini file must be edited to indicate the conversion that should be done.
The task is specified by the key value pairs-
    FACTTYEP_CURRENT  =
    FACTTYPE_NEW      =
    ROLE              =
    DESC              =
    DATE              =

for example-
    FACTTYEP_CURRENT  = Census (family)
    FACTTYPE_NEW      = Census
    ROLE              = Spouse
    DESC              = %Federal%
    DATE              = 1930

Note that the value can have embedded spaces.
Space characters between the = and the value are ignored.

===========================================DIV50==
Fact Type name lists

Fact Type full names are listed in RM by the "Fact types" list feature found in 
several places in the RM user interface-
  In the Edit Person window upon clicking the + button (Add fact button or Alt+A)
  In the three dot menu in the Person tab.
  In the command pallet. (type in "fact")

This window also displays, in the right side panel -
* Whether the fact type is Personal or Family.
* The full fact type name and its assigned abbreviation.
The specification of fact types in the ini file uses the full fact type name, not the abbreviation.

===========================================DIV50==
Fact types in RM come in two styles: Personal and Family. 

Facts of the personal type are linked to a single person while facts of the 
family type are linked to a database family.
An RM database family consists either 2 or 1 persons, labeled internally as
Father and Mother. Either the father or mother may be "unknown"
(and thus set to 0 in the database). Database families, by design, never include
any offspring.

===========================================DIV50==
Supported fact type conversions:
Personal => Personal
Family => Personal
Family => Family

Not allowed:
Personal => Family


Configuration items in ini file required for each type conversion:

* Personal => Personal
FACTTYPE_CURRENT (full name of the fact type of the facts that that should be converted)
FACTTYPE_NEW (full name of the fact type that existing facts should be converted to)
(ROLE is ignored)
DESC and DATE are optionally used to limit which facts are to be converted

* Family => Personal
FACTTYPE_CURRENT
FACTTYPE_NEW
ROLE (name of an existing role for the FACTTYPE_NEW)
DESC and DATE are optionally used to limit which facts are to be converted

* Family => Family
FACTTYPE_CURRENT
FACTTYPE_NEW
(ROLE is ignored)
DESC and DATE are optionally used to limit which facts are to be converted


===========================================DIV50==
The first complication comes with converting a Family fact to a personal fact.

A family fact is linked to a father-mother couple. If the father is know, then 
the new personal fact will be linked to the father. If the mother is also known,
the mother will be added as a witness to the new personal fact. Her role is
specified in the ini file as "ROLE =".

If the father is not known then the new personal fact will be linked to the
mother. There is no new witness added, so the ROLE ini file item is ignored.


The second complication arises when the facts of FACTTYPE_CURRENT have witnesses.

Background: Every witness is assigned a role in RM when the fact is shared.
Each fact type has its own set of roles. Many of the roles have the same name, 
for instance "Witness" however they are still separate and the sentence assigned
to each of the roles are probably different.

If the original fact type, say Census (fam) had a role named "Spouse", and that
fact type is to be converted to "Census", then the fact of type census will
have the former witness transfered to it maintaining the former role, in this
case "Spouse". If "Census" does not have already have a role named Spouse,
the utility will complain and request that you create such a role for "Census"
before the conversion can be completed.
You don't have to recreate all of the roles that exist for the FACTTYPE_CURRENT,
only the ones that are in use. ConvertFact will tell you which ones.

===========================================DIV50==
The ini file values for DESC and DATE are optionally used to limit which 
facts are to be converted.

Some examples-
if you want to convert only facts whose descriptions start with the 
words "New York", then enter-
DESC = New York%
notice the trailing percent sign.
If the fact descriptions should only contain "New York" somewhere in the text, 
enter-
DESC = %New York%

The percent sign % wildcard matches any sequence of zero or more characters.
The underscore _ wildcard matches any single character.

To limit the facts converted by their Date, use the DATE value.
The DATE value is always a four digit year.
For example-
DATE = 1930

If DESC or DATE is not used, just remove the text on the right of the = sign, 
or comment out the line.
The DESC and DATE may be used in any combination.

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
      ConvertFact.py
      RM-Python-config.ini
*  Edit the ini file in the working folder to specify the locations of the RM
   database file and the output report file. The ini file also specifies the
   input parameters for the fact conversion. See Notes section below.
   The same ini file may be used with either the .exe or .py version of the utility.
*  Double click the ConvertFact.py file to run the utility and generate the 
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
