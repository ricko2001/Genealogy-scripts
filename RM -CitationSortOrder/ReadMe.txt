CitationSortOrder
Utility application for use with RootsMagic databases


RootsMagic (RM) software uses a SQLite relational database as its main storage.
This utility uses SQL to modify the database so as to reorder how citations are 
displayed in the Rootsmagic application.


CAUTION
This utility is using an undocumented feature of the RootsMagic application. 
It is possible that a future release of RootsMagic may ignore the changes made
by this utility. It may also be possible, but highly unlikely, that a future  RM
release may not work with a database whose citation sort order has been changed 
with this utility. Luckily, all changes made by this utility can be reverted by
a single, simple SQL update statement. See Notes.

======================================================================
Overview

This program is what is called a "command line utility".

To use it:

1:  Edit the supplied text file named "RM-Python-config.ini". (Hereinafter 
referred to as the "ini file".) The utility needs to know where the RM database 
file is located.) Editing the ini file can be done using the Windows NotePad app.

2:  Double click the CitationSortOrder file. This displays the black 
command console window. 

3:  The console window displays a prompt asking for the RIN 
(PersonID) of the person that has the attached citation list.
The utility will continue with prompts until the desired list of citations is
displayed. The user then responds to prompts until the list is ordered in the 
desired way. The utility will then close.

4:  Return to the RootsMagic application window. Navigate away from the changed
citation listing and the return to it. Examine the modified sort order.


======================================================================
Compatibility
Tested with 
       RootsMagic v9.   Not tested with RM 7 or 8.
       Operating system Window 11, 64bit  (Windows 10 most probably OK)
       Python for Windows v3.11.4   64bit  (when using the py version)

The py script file could be modified to work on MacOS with Python ver 3 installed.


======================================================================
Backups

IMPORTANT: You should run this script on a copy of your database file until you
have confidence using it and confidence in its results. Or at least have a 
current known-good backup.
Assume software developers are fallible and make mistakes, but are not 
malevolent. :)


======================================================================
Getting Started

To install and use the single .exe file version:

*  Create a working folder on your disk, perhaps in the same folder
   that contains your RM database.

*  Copy these files from downloaded zip file to the working folder-
      CitationSortOrder.exe
      RM-Python-config.ini

*  Edit the RM-Python-config.ini in the working folder to specify the location 
   of the RM file. 
   To edit, Open NotePad and drag the ini file onto the NotePad window.

*  Double click the CitationSortOrder.exe file to run the utility.

*  Respond to the utility's prompts to navigate to the desired citation listing.

*  Respond to the utility's prompts to change the citation list order.

*  Examine the console window text and press the enter key to close it.

*  Open the database in RM, navigate to the modified citation list and confirm the change.

--- OR ---

Use the py script file.  See section below, after the Notes section, entitled-
"Which to use? Standalone .exe file or .py file"


======================================================================
NOTES

*    As tested with RootsMagic v9.1.3 x64 on Windows-
CitationSortOrder will change the sort order for citations attached to Person, 
Names, and Facts.
Currently, this utility will not change the sort order of citations attached to
Tasks, Marriages & Associations.
Those capabilities could be added.

*     Use of this utility may be productively combined with the use of a global
re-ordering SQL script developed by Tom Holden and Jerry Bryan.
https://sqlitetoolsforrootsmagic.com/forum/topic/sorting-the-order-of-rm9-citations/

Due to lack of support in the RM app, the modified sort order is not utilized
in the "slide in" workflow for facts.

*    Updating the sort order of a set of citations while the database is open in 
RM works OK. However, the citation lists do not have a refresh button, so, 
you'll need to navigate away from the modified sort order citation list and then
return to it to see the new sort order.

*    RM-Python-config.ini, the ini file.
If there are any non-ASCII characters in the RM-Python-config.ini file,
perhaps in a database path, then the file must be saved in UTF-8 format, with no
byte order mark (BOM). This is an option in the save dialog box in NotePad.

*    This utility only changes the database table: CitationLinkTable and within
it, only the SortOrder column..

*    To revert all citation sort order modifications made by this utility, simply
change the sort order column to all zeros.
UPDATE CitationLinkTable SET SortOrder = 0;
This will change the sort order in RM 9.1.3 to "order entered", which is 
the default.


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
      CitationSortOrder.py
      RMDates.py
      RM-Python-config.ini
*  Edit the RM-Python-config.ini in the working folder to specify the location 
   of the RM file. 
   To edit, Open NotePad and drag the ini file onto the NotePad window.
*  Double click the CitationSortOrder.py file to run the utility.
*  Respond to the utility's prompts to navigate to the desired citation listing.
*  Respond to the utility's prompts to change the citation list order.
*  Examine the console window text and press the enter key to close it.
*  Open the database in RM, navigate to the modified citation list and confirm the change.


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
