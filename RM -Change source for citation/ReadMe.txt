ChangeSrcForCitation
Utility application for use with RootsMagic databases


RootsMagic (RM) software has Sources and Citations.
Sources are also called "Master Sources".
Citations are also called "Source Details".

Sources are created using a Source Template. If 2 sources are created 
from the same source template, they will have the same fundamental structure

Citations are created as a child of a Source. Citations of different sources
created using the same source template will also have the same fundamental
structure.

This simple utility will move a citation from one source to another source,
but only if the 2 sources were created using the same source template.

For example, if you lump census source by US state and year, you will have a
number of sources all based on the same source template.
When entering a citation, you may accidentally cite a source set up for the 
wrong year or state. Instead of deleting and recreating the citation, use this
utility to move it to the correct source.

======================================================================
Compatibility
Works with RootsMagic v8 and v9

.exe file version
       Windows 64bit only. Tested with Window 11.

.py file version
       Python for Windows v3.11.4   64bit
       The py file has not been tested on MacOS.
       The script could probably be modified to work on MacOS with Python
       version 3 installed.


======================================================================
Backups

IMPORTANT: This utility modifies the RM database file. 
You should run this script on a copy of your database file or at least
have a known-good backup until you are confident that the changes made 
are the ones desired.


======================================================================
Overview

This program is what is called a "command line utility".

To use it:

*  Create a working folder on your disk, perhaps in the same folder
   that contains your RM database.

*  Copy these files from the downloaded zip file to the working folder-
      ChangeSrcForCitation.exe
      RM-Python-config.ini

*  Edit the ini file in the working folder to specify the location
   of the RM file. (To edit, Open NotePad and drag the ini file onto the
   NotePad window.)

*  Double click the ChangeSrcForCitation.exe file to run the utility.
   Enter the requested information in the black command console window
   that is displayed. 

*  Confirm that the desired change was made in RM.


--- OR ---

Use the py script file.  See section below, after the Notes section, entitled-
   "Which to use? Standalone .exe file or .py file"


======================================================================
NOTES

*   All interactions with the utility are through the RM-Python-config.ini file
    and the command line console window.
    The RM-Python-config.ini file just give the location of the database to
    modify. The same RM-Python-config.ini file can be shared with other utility
    applications such as TestExternalFiles and GroupFromSQL.

*   Information that the user enters in the command window is checked before
    it is used. It is unlikely that random data would be accepted by 
    the utility.

*   Checks made by the utility:
    1- User is asked for the citation name of the citation to modify.
        a) the name must be found. 
        b) the name must be unique among all citations for all sources.
       The entire citation name does not need to be entered, as long as enough 
       is entered to make it unique. 
       You will be made aware of problems.
    2- User is asked for the source that is to be used as the new parent of
       the citation.
        a) the source name must be found. 
        b) the source name must be unique.
        c) the existing source used by the citation and the new source
           specified must both use the same source template.
       The entire source name does not need to be entered, as long as enough 
       is entered to make it unique. 
       You will be made aware of problems.

*   RM-Python-config.ini  (the ini file)
    If there are any non-ASCII characters in the ini file, perhaps in a database
    path, then the file must be saved in UTF-8 format, with no byte order 
    mark (BOM). The included sample ini file has an umlauted ä in a comment at 
    the end to force it to be in the correct format.
    File format is an option in the save dialog box in NotePad.


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
*  Copy these files from downloaded zip file to the working folder-
      ChangeSrcForCitation.py
      RM-Python-config.ini
*  Edit the ini file in the working folder to specify the location
   of the RM file.
   (To edit, Open NotePad and drag the ini file onto the NotePad window.)
   The same ini file may be used with either the .exe or .py version of the utility.
*  Double click the ChangeSrcForCitation.py file to run the utility.
   Enter the requested information in the black command console window
   that is displayed. 
*  Confirm that the desired change was made in RM.


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

Direct link to recent (2023-07) version installer-
https://www.python.org/ftp/python/3.11.4/python-3.11.4-amd64.exe

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
This is especially true of the exe file version.

======================================================================
