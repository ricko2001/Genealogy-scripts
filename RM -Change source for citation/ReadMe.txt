ChangeSrcForCitation

Utility application for use with RootsMagic databases

RootsMagic (RM) software uses a SQLite relational database as its data storage
file. Having access to that file via third party tools is a major advantage
to using RM.


=========================================================================DIV80==
Purpose

RootsMagic has Sources and Citations. Sources are also called "Master Sources".
Citations are also called "Source Details".

Sources are created using a Source Template. If 2 sources are created
from the same source template, they will have the same fundamental structure.

A Citation is created as a child of a Source. Citations of different sources
created using the same source template will also have the same fundamental
structure.

This simple utility will move a citation from one source to another source,
but only if the 2 sources were created using the same source template.

For example, if you lump census source by US state and year, you will have a
number of sources all based on the same source template.
When entering a citation, you may accidentally cite a source set up for the
wrong year or state. Instead of deleting and recreating the citation, use this
utility to move it to the correct source.


=========================================================================DIV80==
Backups

IMPORTANT: This utility modifies the RM database file.
You should run this script on a copy of your database file or at least
have a known-good backup until you are confident that the changes made
are the ones desired.


=========================================================================DIV80==
Compatibility

Tested with RootsMagic v10

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

*  Create a new folder on your disk.
   This will be called the "working folder".

*  Copy these files from the downloaded zip file to the working folder-
      ChangeSrcForCitation.exe
      RM-Python-config.ini

*  Make a copy of your database, move the copy into the working folder.
   Rename the copy to TEST.rmtree

*  Edit the supplied text file named "RM-Python-config.ini". (Hereinafter
   referred to, as the "config file".)
   The utility needs to know where the RM database file is located, the output
   report file name and location.

*  Double click the ChangeSrcForCitation.exe file to run the utility.
   Enter the requested information in the displayed black command
   console window.

*  When you are finished, a summary report will be displayed in NotePad.
   Confirm that the desired change was made in RM.


--- OR ---

Use the py script file.  See section below, after the Notes section, entitled-
   "Which to use? Standalone .exe file or .py file"


=========================================================================DIV80==
=========================================================================DIV80==
NOTES

*   All interactions with the utility are through the RM-Python-config.ini file
    and the command line console window.
    The RM-Python-config.ini file just give the location of the database to
    modify. The same RM-Python-config.ini file can be shared with other utility
    applications such as TestExternalFiles and GroupFromSQL.

*   Information that the user enters in the command window is checked before
    it is used. It is unlikely that random data would be accepted by
    the utility.

*   The utility asks for the name of the citation to change and the source
    that it should use. In both cases, only enough of the name needs to be
    entered to make it unique among all citations for all sources. 
    It is suggested that you copy and paste from the RM source edit window.
    There is no need to manually type input.
    One may start the name entry with a % char and it will be used as the
    standard  'SQL Like' wild card.
    If the full citation name is not unique, then as a workaround, you
    could add some text to the citation name of the citation you want
    to modify to make the name unique.

*   Checks made by the utility:
    1- User is asked for the citation name of the citation to modify.
        a) the name must be found.
        b) the name must be unique among all citations for all sources.
       You will be made aware of problems.
    2- User is asked for the source that is to be used as the new parent of
       the citation.
        a) the source name must be found.
        b) the source name must be unique.
        c) the existing source used by the citation and the new source
           specified must both use the same source template.
       You will be made aware of problems.

===========================================DIV50==
REPORT_FILE_DISPLAY_APP

Option to automatically open the report file in a display application.
The included ini sample file has this option activated and set to use Windows
NotePad as the display app. It can be deactivated by inserting a # character
at the start of the line. Your favorite editor may be substituted.

===========================================DIV50==
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
There is probably something wrong with the config file line-
REPORT_FILE_PATH

=========-
Error message:
RM-Python-config.ini file contains a format error

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

*  Create a new folder on your disk.
   This will be called the "working folder".

*  Make a copy of your database, move the copy into the working folder.
   Rename the copy to TEST.rmtree

*  Copy these files and the folder from the downloaded zip file to the working folder-
      ChangeSrcForCitation.py
      RM-Python-config.ini
      RMpy

See the Overview section for the subsequent tasks.


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

Direct link to recent (2023-07) version installer-
https://www.python.org/ftp/python/3.11.4/python-3.11.4-amd64.exe

The Python installation requires about 100 Mbytes.
It is easily and cleanly removed using the standard method found in
Windows=>Settings

Run the Python installer selecting all default options.


=========================================================================DIV80==
TODO
*  ?? what would you find useful?

*  Do you have citations in different sources with the same citation name?
That situation will prevent you from using this app.
I could add a workflow where the utility will first ask for the source
and then ask for a citation name that is used by that source, but 
it increases the effort for a situation that may not be common, especially
as there is a workaround: temporarily chnage one of the citation names.


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
This is especially true of the exe file version.

=========================================================================DIV80==
