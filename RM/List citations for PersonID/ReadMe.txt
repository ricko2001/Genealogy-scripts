=========================================================================DIV80==
List all Citations for a Person given the PersonID/RIN
ListCitationsForPersonID

Utility application for use with RootsMagic databases

RootsMagic (RM) software uses a SQLite relational database as its data storage
file. Having access to that file via third part tools is a major advantage
to using RM.

=========================================================================DIV80==
Purpose

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


=========================================================================DIV80==
Backups

IMPORTANT: You should run this script on a copy of your database file until you
have confidence using it and confidence in its results. Or at least have a
current known-good backup.

This script only reads the database file and makes no changes.


=========================================================================DIV80==
Compatibility

Tested with RootsMagic v 10
Not compatible with RM v7
Tested with Python for Windows v3.13   64bit

The py file has not been tested on MacOS but could probably be easily
modified to work on MacOS with Python version 3 installed.


======================================================================
Overview

This program is what is called a "command line utility". 
To install and use the script:

*  Install Python for Windows x64  -see immediately below

*  Create a new folder on your disk.
   This will be called the "working folder".

*  Make a copy of your database, move the copy into the working folder.
   Rename the copy to TEST.rmtree

*  Copy these files and the folder from the downloaded zip file to the working folder-
        ListCitationsForPersonID.py
        RM-Python-config.ini
        RMpy

   The utility needs to know where the RM database file is located, the output
   report file name and its location.
   
   The config file also tells the utility what actions to perform.
    If you followed the above instructions, no edits are needed.

*  Double click the ListCitationsForPersonID.py file. This displays the
    black command console window.

*  Enter the RIN for the desired report and hit the Enter key. The command 
    window is closed.

*  Examine the generated report text file that is now opened in Notepad.



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

=========-
RM-Python-config.ini  (the config file)
If there are any non-ASCII characters in the config file then the file must be
saved in UTF-8 format, with no byte order mark (BOM).
The included sample ini file has an accented ä in the first line comment to
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
*   consider alternate output formats


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
