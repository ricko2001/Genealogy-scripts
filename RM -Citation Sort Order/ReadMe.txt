=========================================================================DIV80==
Citation Sort Order
CitationSortOrder

Utility application for use with RootsMagic databases

RootsMagic (RM) software uses a SQLite relational database as its data storage
file. Having access to that file via third party tools is a major advantage
to using RM.


=========================================================================DIV80==
Purpose

This utility will charge the order that citations are listed in the Edit Person
window for citations attached to Facts, Names and/or Persons. This may be helpful
while doing research in bringing the most important citations to the top of the list.
The new ordering of citations is not used in reports.


=========================================================================DIV80==
Backups

IMPORTANT: You should run this script on a copy of your database file until you
have confidence using it and confidence in its results. Or at least have a
current known-good backup.

CAUTION
This utility is using an undocumented feature of the RootsMagic (RM) application.
It is possible that a future release of RootsMagic may ignore the changes made
by this utility. It may also be possible, but highly unlikely, that a future RM
release may not work with a database whose citation sort order has been changed
with this utility. Fortunately, all changes made by this utility can be reverted by
a single, simple SQL update statement. See Notes.


=========================================================================DIV80==
Compatibility

Tested with RootsMagic version 10
Not compatible with RM ver 7.
Tested with Python for Windows v3.13.1   64bit

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
      CitationSortOrder.py
      RM-Python-config.ini
      RMpy

*  Edit the file, RM-Python-config.ini (hereinafter referred to as the 
   "config file") in the working folder.

   The utility needs to know where the RM database file is located, the output
   report file name and its location.

   If you followed the above instructions, no edits are needed.

*  Double click the CitationSortOrder.py file. This displays the black command
   console window.

*  The console window displays a prompt asking for the RIN
(PersonID) of the person that has the attached citation list.
The utility will continue with prompts until the desired list of citations is
displayed. The user then responds to prompts until the list is ordered in the
desired way. The utility will then close.

*  Return to the RootsMagic application window. Navigate away from the changed
citation listing and the return to it. Examine the modified sort order.


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
CitationSortOrder can change the sort order for citations attached to Person,
Names, and Facts.
Currently, this utility will not change the sort order of citations attached to
Tasks, Marriages & Associations.
Those capabilities could be added.
This utility only changes the database table: CitationLinkTable and within
it, only the SortOrder column..


=========-
Due to lack of support in the RM app, the modified sort order is not utilized
in the "slide in workflow" for facts or in reports generated by RM.


=========-
Use of this utility may be productively combined with the use of a global
re-ordering SQL script developed by Tom Holden and Jerry Bryan.
https://sqlitetoolsforrootsmagic.com/forum/topic/sorting-the-order-of-rm9-citations/


=========-
Note that after reordering, newly added citations will appear at the top
of the list as they will have a SortOrder number of 0.
This contrasts with behavior seen before reordering where the citations are shown
in "order entered" sequence because all records are added with a SortOrder number of 0.
Use this app to make desired changes.


=========-
Updating the sort order of a set of citations while the database is open in
RM works OK. However, the citation lists do not have a refresh button, so,
you'll need to navigate away from the modified sort order citation list and then
return to it to see the new sort order.


=========-
To revert all citation sort order modifications made by this utility, simply
change the sort order column to all zeros.
UPDATE CitationLinkTable SET SortOrder = 0;
This will change the sort order in RM v10 to "order entered", which is
the default.


=========-
RM-Python-config.ini  (the config file)
If there are any non-ASCII characters in the config file then the file must be
saved in UTF-8 format, with no byte order mark (BOM).
The included sample config file has an accented ä in the first line comment to
force it to be in the correct format.

File format is an option in the "Save file" dialog box in NotePad.

config file path names may be absolute or relative to the current directory.


=========-
REPORT_FILE_DISPLAY_APP
Option to automatically open the report file in a display application.
The included ini sample file has this option activated and set to use Windows
NotePad as the display app. Your favorite editor may be substituted.
Automatic display can be deactivated by inserting a # character
at the start of the line.


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
*  add an option subset of the global re-ordering code mentioned above by Tom Holden.

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
