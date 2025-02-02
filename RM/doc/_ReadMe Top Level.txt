This zip file contains the current versions of all the released
RootsMagic utility programs.

The collection of utilities, RM Utilities Suite, has a version number
and each of the individual utilities also has a separate version
number (displayed in the report file header.)

If a utility is updated or a new one is created, a new collection (or suite)
with a new version number will be created and released on GitHub.

These utilities are written in the Python scripting language. To run them,
the Python language must be installed on the computer. See below for instructions.


Code common to all of the utilities is contained in the Python package RMpy.
This is the folder named RMpy in each of the utility folders.
The RMpy folder and its contents are exactly the same in each utility folder.
The folder has been copied to each utility folder solely as a convenience.

If you use multiple utilities, place the corresponding utility py 
files, one copy of the RMpy folder, and a single RM-Python-config.ini file
into a folder. The various utility apps share the RM-Python-config.ini file 
and the RMpy folder.


Some utilities, such as TestExternalFile, GroupFromSQL, ColorFromGroup, 
ListCitationsForPersonID, CitationSortOrder and ConvertFact are most convenient
when used directly on the production database. Others, like ChangeSourceTemplate,
usually require several attempts, due to their more complicated setup requirements.
So these should always be run on a database copy.
As mentioned in the individual ReadMe files, always run the utility on a database
copy until you are confident of the results and affect on the database.



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

