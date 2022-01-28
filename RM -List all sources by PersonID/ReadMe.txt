
List all sources for a Person given the PersonID/RIN

RootsMagic (RM) uses SQLite as its main storage. 
This script queries the database directly.
It only reads the database and makes no changes. 
Make a backup of your database before using this script
until you have confidence that your data is OK.

Input is a single RIN number. Also called a PersonID
The RIN can be entered at the console window as the script runs, or it can be specified in the RM-Python-config.ini file.

Output is a alphabetically sorted list of source names and citation names attached -
	to the specified person
	to facts attached to the person
	to names attached to the person
	to "family" objects that the person is in
	to facts attached to "family" objects that the person is in
the output also includes the number of citations found.

The last line of output prompts the user to hit Enter to close the window.

Sample output at end of this file.


To install:
*  Download and install Python for Windows x64 (use default options)  -see below
*  Download unifuzz64.dll   -see below
*  Create a folder on disk and copy these files to it-
      ListSourceNamesForPersonID.py
      RM-Python-config.ini
      unifuzz64.dll
*  Edit the RM-Python-config.ini to specify the location of the RM file,  
   the unifuzz64.dll file.

To use:
*  Double click the ListSourceNamesForPersonID.py file and enter the RIN at the prompt in the console window.
*  Examine the output either in the console window - and/or copy it to the clipboard
*  Press Enter to close the console window.



Tested with RootsMagic v8.1.5.0		RM v7 no longer supported)
       Python for Windows v3.10.2   64bit  (most likely any ver 3 Python will work)
       unifuzz64.dll (version number not set, MD5=06a1f485b0fae62caa80850a8c7fd7c2)
       Operating system= Window 10, 64bit


Python download- direct link
https://www.python.org/ftp/python/3.10.2/python-3.10.2-amd64.exe
about 25 MBytes, uses about 100 MB after install
Default install location is %USERPROFILE%\AppData\Local\Programs
Un-installation works well, if you decide to not keep it

This link is found on the page-
https://www.python.org/downloads/windows/
Use the current version of Python, version 3.10.2 or later
Click on the link near the top of page. It is named "Latest Python 3 Release ...." 
Then ...
Find the link at the bottom of page, in "Files" section, labeled "Windows installer (64-bit)"
Click it and save the installer, and then run it. Use default options if unsure.


unifuzz64.dll download-
https://sqlitetoolsforrootsmagic.com/wp-content/uploads/2018/05/unifuzz64.dll
above link found on this page-
https://sqlitetoolsforrootsmagic.com/rmnocase-faking-it-in-sqlite-expert-command-line-shell-et-al/
This script does not need the application "SQLite Expert" described on the page. We need just the single file "unifuzz64.dll"

Notes:
*  If there are any non-ASCII characters in the RM-Python-config.ini file, 
   perhaps in a database path, then the file 
   must be saved in UTF-8 format, with no byte order mark (BOM).


TODO
*  Output report file not yet implemented. If the output is needed, copy it from the console window. Right click 



=====================
Sample output   (abridged)
=====================

PersonID= 3


BRC Otter,Alban Josef b1927 -1  -ORIG       Listed as "Alban Josef Otter", son of "Ferdinand Otter" and "Agnes Schürger", born on "22.April 1927 in Waldzell".
BRC Otter,Alban Josef b1927 -1  -ORIG       Listed as "Alban Josef Otter", son of "Ferdinand Otter" and "Agnes Schürger".
BRC Otter,Richard b1955  -ORIG        Listed as son of 'Alban Otter' & 'Rose Maier'.
CIT Otter,Alban       Certificate issued Dec 9, 1958, from Brooklyn Court, NY.
DIRdb ANC US  1950-1993     PublicRecords Vol-1       Rose Otter b1929
DIRdb ANC US  1950-1993     PublicRecords Vol-2       Alban J Otter; 1927; ; ;
DIRdb ANC US  1950-1993     PublicRecords Vol-2       Alban Otter b1927
DIRdb ANC US  1950-1993     PublicRecords Vol-2       Rosa Otter b1929
I Otter,Alban J b1927       Given as born 22/Apr/1927.
I Otter,MaryAnn       States that parents sold house between Thanksgiving and Christmas of 1977.
I Otter,MaryAnn       States that parents sold house between Thanksgiving and Christmas of 1977. Then moved to 3rd floor above Green Tree.
I Otter,Richard J b1955       Given as born 22/Apr/1927 in Waldzell.
I Otter,Roman       2010-02-28: Stayed with brother Alban in upstairs apartment from immigration in 1962 for 9 years.
I Otter,Rose       2010-02-28: Visit, found escrow papers, closed on 9 Nov 1995. Moved into house in Jan 1996.
I Otter,Rose       Rose Otter said he died night of Sunday June 18, 2006 at home in Santa Maria, CA.
INTV Otter,Alban 1998-02-27       Given as Waldzell.
MR Otter & Maier m1954  -A  -ORIG       Listed as Alban Otter married Rose Maier
MR Otter & Maier m1954  -FS
OBIT Maier,Dorothea  -DE       Listed as 'Rosa Otter, geb. Maier und Familie'.
SSACIdb ANC US       SSACI Otter,Alban Josef b1927
SSDIdb ANC US       SSDI Otter,Alban b1927

 52  source citations found


Hit Enter to exit
=====================


