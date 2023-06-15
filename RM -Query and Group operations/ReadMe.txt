Query and Group operations

RootsMagic (RM) software uses a database as its main storage.
Groups may be created with Roots Magic software, but the types of queries are limited

======================================================================
Command Line Utility

This application is what is called a command line utility. To use it:
1: first edit the supplied text file named "RM-Python-config.ini". This can be done
   using the Windows NotePad app. The file contains options and required configuration settings.

2: Double click the TestExternalFiles file. This momentarily displays the
   black command console window and at the same time, generates the report text file.
   (7,000 media files requires about 3 seconds run time for 4 features turned on without hash file.
    Generating a hash file for 7,000 files takes about a minute.)

3  Open the Report text file in Notepad. The file will contain the report results.


======================================================================
Features


======================================================================
Compatibility
Tested with RootsMagic v7.6.5, v8 and v9
       Python for Windows v3.10.5   64bit
       unifuzz64.dll (file has no version number defined. see MD5 and file size in accompanying file Hash.txt)
       Operating system Window 11, 64bit  (Windows 10 OK)
The exe file is Windows only, probably Windows 10 and later.
The py file could probably be modified to work on MacOS with Python ver 3+ installed.


======================================================================
Backups

You should run this script on a copy of your database file or at least have a known-good backup.


======================================================================
Getting Started

To install and use the single file version:
*  Create a folder on your disk
*  Copy these files from downloaded zip file to the above folder-
      TestExternalFiles.exe
      RM-Python-config.ini
*  Download unifuzz64.dll   -see below
*  Move the unifuzz64.dll file to the above folder
*  Edit the RM-Python-config.ini in the above folder to specify the location of the RM file,
   the unifuzz64.dll file and the output report file. Some script functions
   may be turned on or off. The required edits should be obvious.
   (To edit, Open NotePad and drag the ini file onto the NotePad window.)
*  Double click the TestExternalFiles.exe file to run the script and generate
   the report file.
*  Examine the report output file.

----
OR
----

To install and use the script file version:
*  Install Python for Windows x64  -see below
*  Create a folder on your disk
*  Copy these files from downloaded zip file to the above folder-
      TestExternalFiles.py
      RM-Python-config.ini
*  Download unifuzz64.dll   -see below
*  Move the unifuzz64.dll file to the above folder
*  Edit the RM-Python-config.ini in the above folder to specify the location of the RM file,
   the unifuzz64.dll file and the output report file. Some script functions
   may be turned on or off. The required edits should be obvious.
   (To edit, Open NotePad and drag the ini file onto the NotePad window.)
*  Double click the TestExternalFiles.py file to run the script and generate
   the report file.
*  Examine the report output file.



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
Find the link near bottom of page, in "Files" section, labeled "Windows installer (64-bit)"
Click it and save the installer.

Direct link to recent version installer-
https://www.python.org/ftp/python/3.10.5/python-3.10.5-amd64.exe


The Python installation requires about 100 Mbytes.
It is easily and cleanly removed using the standard method found in Windows=>Settings

Run the Python installer selecting all default options.


======================================================================
unifuzz64.dll download-

https://sqlitetoolsforrootsmagic.com/wp-content/uploads/2018/05/unifuzz64.dll

above link found in this context-
https://sqlitetoolsforrootsmagic.com/rmnocase-faking-it-in-sqlite-expert-command-line-shell-et-al/

The SQLiteToolsforRootsMagic website has been around for years and is run by a trusted RM user.
Many posts to public RootsMagic user forums mention use of unifuzz64.dll from the SQLiteToolsforRootsMagic website.

======================================================================
NOTES

*  RM-Python-config.ini
   If there are any non-ASCII characters in the RM-Python-config.ini file,
   perhaps in a database path, or in ignored objects, then the file
   must be saved in UTF-8 format, with no byte order mark (BOM). This is a simple
   save option in NotePad.


*   RMNOCASE_fake-SQLiteSpy64.dll
    An alternate for unifuzz64.dll named "RMNOCASE_fake-SQLiteSpy64.dll" has recently been created and
    has been successfully tested. The 2 dlls work equally well for this script.
    https://sqlitetoolsforrootsmagic.com/wp-content/uploads/2017/12/RMNOCASE_fake-SQLiteSpy64.dll.bak
    in the context of this page:
    https://sqlitetoolsforrootsmagic.com/rmnocase-faking-it-in-sqlitespy/rmnocase_fake-sqlitespy64-dll/

    After download, rename the file by removing the final ".bak"


*   MD5 hash values are used to confirm the identity of files.
	MD5 hash							File size		File name
	06a1f485b0fae62caa80850a8c7fd7c2	256,406 bytes	unifuzz64.dll
	43fe353e3e3456dc33f8f60933dbc6ab	74,240 bytes	RMNOCASE_fake-SQLiteSpy64.dll


======================================================================

======================================================================
TODO


======================================================================
Feedback
The author appreciates comments and suggestions regarding this software.
Richard.J.Otter@gmail.com

Public comments may be made at-
https://github.com/ricko2001/Genealogy-scripts/discussions

See my Linked-In profile at-
https://www.linkedin.com/in/richardotter/
