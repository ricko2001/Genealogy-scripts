TestExternalFiles


RootsMagic (RM) uses a database as its main storage. The database 
schema includes a table that points to external files. These file appear
under the RM8 Media tab.

As the number of linked files increases, user errors become more likely. 
* A file on disk may get renamed, or moved, breaking the link 
    from the database. RM has tools to help fix these, but it does not 
    give a log of what was done. There is a report that can be run, but
    with effort.
* A file may be added to the media folder on disk but then not attached to the
    desired database element. Common when working quickly.
* A file may be added to RM, but then detached from all source, facts etc , leaving it
    "un-tagged". No harm in leaving it, but cleanup may be desirable.
* A file may be added to the database more than once.

This utility will help identify these issues.
It is recommended to run this script daily as part of your backup routine.


======================================================================
Command Line Utility

This application is what is called a command line utility. To use it:
1: first edit the supplied text file named "RM-Python-config.ini". This can be done 
   using the Windows NotePad app. The file contains options and required configuration settings.

2: Double click the TestExternalFiles file. This momentarily displays the
   black command console window and at the same time, generates the report text file.
   (7,000 media files requires about 3 seconds run time for 4 features turned on)

3  Open the Report text file in Notepad. The file will contain the report results.


======================================================================
Features

The utility performs several functions, as specified in the ini file Options section:

CHECK_FILES
   Checks that each file referenced in the RM database actually 
   exists on disk at the specified location. Any database file link not
   found on disk is listed.

UNREF_FILES
   Lists all files found in the folder specified by SEARCH_ROOT_FLDR_PATH 
   (see below) that are NOT referenced in the RM database.
   Perhaps the file was added to the folder, but was mistakenly never
   added to the database.
   This feature is designed for use when media files referenced by RM are all
   in a single folder hierarchy. 

FOLDER_LIST
   Lists all folders referenced in the RM database. A file in an unexpected location
   may have been accidentally added to the database. This list will make it obvious.

NO_TAG_FILES
   Lists all files found in RM's Media tab that have zero tags.

DUP_FILES
    Lists files that have been added more than one time to the database. These will
    appear more than once in RM's Media tab.


======================================================================
Compatibility
Tested with RootsMagic v7.6.5 and v8.2.0.0 (RM ver 7.6, 8.0 OK)
       Python for Windows v3.10.5   64bit  (ver 3.9 OK)
       unifuzz64.dll (file has no version number defined. see MD5 and file size in accompanying file Hash.txt)
       Operating system Window 11, 64bit  (Windows 10 OK)
The exe file is Windows only, probably Windows 10 and later.
The py file could probably be modified to work on MacOS with Python ver 3+ is installed.


======================================================================
Which to use? Standalone .exe file or .py file

Decide whether you wish to use the script file (.py) or the executable file (.exe) version. 
They produce exactly the same output at the same speed.

* Executable file Version
Pro:
The single exe file is all you need. No need to install Python.
Con:
The exe file is not human readable. 
A certain amount of trust is required to run a program not from a major software house.
Unknown software from an unknown software author could contain mal-ware.

or

* Script File Version
Pro: 
The script file is easily readable and one can confirm what it does
You may want to learn Python and make your own changes to the script.
Con:
The script version requires an installation of the Python environment to run.
This is a 100 MB investment in disk space. (Small for modern day hard disks)


======================================================================
Backups 

IMPORTANT: This utility ONLY reads the RM database file. This utility cannot change your RM file.
However, until you trust that the above statement is true, you should run this script on a copy
of your database file or at least have a known-good backup.


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
*  If no report file is generated, look at the black command console window for
    error messages that will help you fix the problem.

*  RM-Python-config.ini
   If there are any non-ASCII characters in the RM-Python-config.ini file, 
   perhaps in a database path, or in ignored objects, then the file 
   must be saved in UTF-8 format, with no byte order mark (BOM). This is a simple 
   save option in NotePad.

*  UNREF_FILES
   If there is a difference in capitalization of file name or directory path in the
   database vs. the file system, the file will be listed as un-referenced. 
   (Unix-like file system case sensitivity)

*  General information: File paths pointing to external files
   in RM7: all paths are absolute starting with a drive letter
   in RM8: absolute file path starting with a drive letter
           or
           a path relative to another location.
   RM8 Relative path symbols 
   (these are expanded when found in the first position of the stored path)
	~	home directory  (%USERPROFILE%)
	?	media folder as set in RM preferences
	*	RM main database file location

*   CHECK_FILES feature: file path case in the database or in the file system path name is not significant.

*   UNREF_FILES feature: The folder specified in RM's preferences as the Media folder is not necessarily
    the same as the folder specified by the SEARCH_ROOT_FLDR_PATH variable in the 
    RM-Python-config.ini file, but it is recommended that they be the same.

    To shorten the list of unreferenced items, the IGNORED_OBJECTS section can be edited to list items 
    to be ignored. The goal would be to produce a report file with no unreferenced filed found. This is
    an easy result to interpret. If a file is to be added to the folder that won't be referenced by
    RM, add it to the IGNORED_OBEJECTS section

*   DUP_FILES feature:  Files may be duplicated in the media tab intentionally as they might 
    have different captions etc.

*   SHOW_ORIG_PATH feature: (RM8 only) 
    A display option is available for files found by either the CHECK_FILES or NO_TAG_FILES or DUP_FILES
    The option is turned on with the option SHOW_ORIG_PATH in the ini file.
    With this option on, the path for each file is shown twice,
    - the path on disk, that is, after any RM8 token in the path has been expanded.
    - the path as saved in the database with the token not expanded.

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
Sample report output-

++++++++++
++++++++++
Report generated at      = 2022-07-07 13:48:50
Database processed       = C:\Users\me\Genealogy\MyFile.rmtree
Database last changed on = 2022-06-30 15:36:12


===============================================================DIV70==
=== Start of "Files Not Found" listing

File path not found: 
"C:\Users\me\Documents\Genealogy\GeneDB\Exhibits\Dummy Birth File.txt"
File path not found: 
"C:\Users\me\Documents\Genealogy\GeneDB\Exhibits\Misc\Morita, Tama #4516.rtf"


=== End of "Files Not Found" listing

===============================================================DIV70==
=== Start of "Unreferenced Files" listing

.\Sources\Birth\Hauer, Theadore Joseph b1912 -Birth Certificate.jpg
.\Sources\Birth\Scamihorn, Samuel Jay b1942 -Birth Certificate.jpg


Folder processed: "C:\Users\me\Documents\Genealogy\GeneDB\Exhibits"
Files in processed folder not referenced by the database: 2
Processed folder contains 4859 files (not counting ignored items)
Database file links: 4972

=== End of "Unreferenced Files" listing

===============================================================DIV70==
=== Start of "Referenced Folders" listing

C:\Users\me\Genealogy\GeneDB\Exhibits
C:\Users\me\Genealogy\GeneDB\Exhibits\Audio\Otter
C:\Users\me\Genealogy\GeneDB\Exhibits\Images\Faces
C:\Users\me\Genealogy\GeneDB\Exhibits\Images\Misc
C:\Users\me\Genealogy\GeneDB\Exhibits\Images\Newspaper-  Waldzell firefighters
C:\Users\me\Genealogy\GeneDB\Exhibits\Images\Photos
C:\Users\me\Genealogy\GeneDB\Exhibits\Images\Photos\Imai, Ethel

  Folders referenced in database  7

=== End of "Referenced Folders" listing

===============================================================DIV70==
=== Start of "Files with no Tags" listing

"C:\Users\me\Genealogy\GeneDB\Exhibits\Dummy Birth File.txt"
"C:\Users\me\Genealogy\GeneDB\Exhibits\Images\Photos\Imai Family 1945-1948.jpg"

=== End of "Files with no Tags" listing

===============================================================DIV70==
=== Start of "Duplicated Files" listing

"C:\Users\me\Genealogy\GeneDB\Exhibits\Sources\Passenger List\Och, Dorothea & Margareta -Passenger List 1929 -2of2 -ANCimg50.jpg"
"C:\Users\me\Genealogy\GeneDB\Exhibits\Sources\Passenger List\Och, Dorothea & Margareta -Passenger List 1929 -2of2 -ANCimg50.jpg"
"C:\Users\me\Genealogy\GeneDB\Exhibits\Images\Places\USA-New York\Otter Paint shop in 2021 (393 Linden St.).PNG"
"C:\Users\me\Genealogy\GeneDB\Exhibits\Images\Places\USA-New York\Otter Paint shop in 2021 (393 Linden St.).PNG"

=== End of "Duplicated Files" listing

===============================================================DIV70==
=== End of Report

++++++++++
++++++++++

======================================================================
TODO
*  Add code to find duplicate files with different paths saved in database.


======================================================================
Feedback
The author appreciates comments and suggestions regarding this software.
Richard.J.Otter@gmail.com

Public comments may be made at-
https://github.com/ricko2001/Genealogy-scripts/discussions

See my Linked-In profile at-
https://www.linkedin.com/in/richardotter/
