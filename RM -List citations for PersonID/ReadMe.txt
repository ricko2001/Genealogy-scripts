
List all Citations for a Person given the PersonID/RIN
ListCitationsForPersonID

RootsMagic (RM) uses SQLite as its main storage. 
This script queries the database directly.
It only reads the database and makes no changes. 
Make a backup of your database before using this script
until you have confidence that your data is OK.

Input is a single RIN number (also called a PersonID).
The RIN can be entered at the console window as the script runs, or it can be 
specified in the RM-Python-config.ini file.

Output is an alphabetically sorted list of source names and citation names attached -
    to the specified person
    to facts attached to the person
    to facts shared to the person
    to names attached to the person
    to "family" objects that the person is in
    to facts attached to "family" objects that the person is in
    to associations that the person is a member of

the output also includes the number of citations found.

The results are saved to a report file which is automatically displayed.


======================================================================
Overview

This program is what is called a "command line utility".

To use it:

1:  Edit the supplied text file named "RM-Python-config.ini". (Hereinafter
    referred to as the "config file".)

2:  Double click the ListCitationsForPersonID file. This displays the
    black command console window.

3:  Enter the RIN for the desired report and hit the Enter key. The command 
    window is closed.

3:  Examine the generated report text file that is now opened in Notepad.


======================================================================
Tested with:
       RootsMagic database file v10		(RM v7 no longer supported)
       Python for Windows v3.12.3   64bit 
       Operating system= Window 11, 64bit


======================================================================
Backups

IMPORTANT: This utility ONLY reads the RM database file. This utility cannot
change your RM file. However, until you trust that this statement is true,
you should run this script on a copy of your database file or at least
have several known-good backups.


======================================================================
Getting Started

To install and use the exe single file version:

*  Create a new folder on your disk.
   This will be called the "working folder".

*  Copy these files from the downloaded zip file to the working folder-
      ListCitationsForPersonID.exe
      RM-Python-config.ini

*  Make a copy of your database, move the copy into the working folder.
   Rename the copy to TEST.rmtree

*  Edit the config file in the working folder to specify the location of the RM
   database file. If you've followed the above suggestions, no editing is required.
   Editing the config file can be done using the Windows NotePad app.
   Open Notepad and drag the config file into the open NotePad window.

*   Double click the ListCitationsForPersonID.exe file. This displays the
    black command console window.

*  Enter the RIN for the desired report and hit the Enter key. The command 
    window is closed.

*  Examine the generated report text file that is now opened in Notepad.


--- OR ---

Use the py script file.  See section below, after the Notes section, entitled-
   "Which to use? Standalone .exe file or .py file"


======================================================================
NOTES

*   RM-Python-config.ini  (the config file)
If there are any non-ASCII characters in the config file then the file must be
saved in UTF-8 format, with no byte order mark (BOM).
The included sample ini file has an accented ä in the first line comment to
force it to be in the correct format.
File format is an option in the "Save file" dialog box in NotePad.


*   Troubleshooting:
=========-
No Report File

If no report file is generated, look at the black command
console window for error messages that will help you fix the problem.
If no report file is generated and the black command console window closes
before you can read it, try first opening a command line console and then
running the exe or py file from the command line. The window will not close
and you'll be able to read any error messages.


=========-
Error message- ... RM-Python-config.ini file contains a format error ...
The problem is as stated, the solution may be harder to determine.
You may want to look at- https://en.wikipedia.org/wiki/INI_file

=========-
If no report file is generated and the black command console window closes
before you can read it, try first opening a command line console and then
running the exe or py file from the command line. The window will not close
and you'll be able to read any error messages.

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

*  Create a new folder on your disk.
   This will be called the "working folder".

*  Copy these files and the folder from the downloaded zip file to the working folder-
      ListCitationsForPersonID.y
      RM-Python-config.ini
      RMpy

*  Make a copy of your database, move the copy into the working folder.
   Rename the copy to TEST.rmtree

*  Edit the config file in the working folder to specify the location of the RM
   database file. If you've followed the above suggestions, no editing is required.
   Editing the config file can be done using the Windows NotePad app.
   Open Notepad and drag the config file into the open NotePad window.

*   Double click the ListCitationsForPersonID.py file. This displays the
    black command console window.

*  Enter the RIN for the desired report and hit the Enter key. The command 
    window is closed.

*  Examine the generated report text file that is now opened in Notepad.


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
*   consider alternate output formats


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

