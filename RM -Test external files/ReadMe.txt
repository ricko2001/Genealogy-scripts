TestExternalFiles
Utility for RootsMagic databases


RootsMagic (RM) software uses a database as its main storage. The database
includes a table that points to external files. These file appear
under the RM Media tab.

As the number of linked files increases, user errors become more likely.
* A file on disk may get renamed, or moved, breaking the link
    from the database. RM has tools to help fix these, but it does not
    give a log of what was done. There is a report that can be run, but
    with effort.
* A file may be added to the media folder on disk but then not attached to the
    desired database element. Common when working quickly.
* A file may be added to RM, but then detached from all source, facts etc,
    leaving it "un-tagged". No harm in leaving it, but de-cluttering may be
    desirable.
* A file may be added to the database more than once.
* A file may be renamed, or misplaced and the original file contents cannot
    be verified.

This utility will help identify these issues.
It is recommended to run this script daily as part of your backup routine.


======================================================================
Command Line Utility

This application is what is called a command line utility. To use it:
1: first edit the supplied text file named "RM-Python-config.ini". This
   can be done using the Windows NotePad app. The file contains options
   and required configuration settings.

2: Double click the TestExternalFiles file. This momentarily displays the
   black command console window and at the same time, generates the report
   text file. (7,000 media files requires about 3 seconds run time for 5
   features turned on without hash file. Generating a hash file for 7,000
   files takes about a minute.)

3  Open the Report text file in Notepad. The file will contain the report
   results. A HASH text file, when requested, is generated at the user
   configured location.


======================================================================
Features

The utility performs several functions, as configured in the RM-Python-config.ini
file's Options section, either separately or in combination:

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

NO_TAG_FILES
   Lists all files found in RM's Media tab that have zero tags.

DUP_FILEPATHS
    Lists files that have been added more than one time to the database. These will
    appear more than once in RM's Media tab.

DUP_FILENAMES
    Lists files that have the same filename. This is not usually a problem, but being
    aware of the duplicate names may help your organizing efforts.

FOLDER_LIST
   Lists all folders referenced in the RM database. A file in an unexpected location
   may have been accidentally added to the database. This list will make it obvious.

HASH_FILE
    Generates a text file containing a listing of each media file's name, location
    and HASH value, currently set to use MD5. (MD5 is no longer considered secure
    for cryptography, but serves well for this application.)


======================================================================
Compatibility
Tested with RootsMagic v7.6.5, v8 and v9
       Python for Windows v3.11.4   64bit
       unifuzz64.dll (file has no version number defined. see MD5 and file size below)
       Operating system Window 11, 64bit  (Windows 10 OK)
The exe file is Windows only, probably Windows 10 and later.
The py file could probably be modified to work on MacOS with Python ver 3+ installed.


======================================================================
Which to use? Standalone .exe file or .py file

Decide whether you wish to use the script file (.py) or the executable file (.exe) version.
They produce exactly the same output at the same speed.

* Executable file Version
Pro:
The single exe file is all you need. No need to install Python.
Con:
The exe file is not human readable.
A certain amount of trust is required to run a program not published by a major software house.
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

IMPORTANT: This utility ONLY reads the RM database file. This utility cannot
change your RM file. However, until you trust that the above statement is true,
you should run this script on a copy of your database file or at least
have a known-good backup.


======================================================================
Getting Started

To install and use the single file version:
*  Create a working folder on your disk, perhaps in your Documents folder.
*  Copy these files from downloaded zip file to the working folder-
      TestExternalFiles.exe
      RM-Python-config.ini
*  Download the SQLite extension: unifuzz64.dll   -see below
*  Move the unifuzz64.dll file to the working folder
*  Edit the RM-Python-config.ini in the working folder to specify the location
   of the RM file, the unifuzz64.dll file and the output report file.
   Some script functions may be turned on or off. The required edits should
   be obvious. (To edit, Open NotePad and drag the ini file onto the NotePad window.)
*  Double click the TestExternalFiles.exe file to run the utility and
   generate the report file.
*  Examine the report output file.

----
OR
----

To install and use the script file version:
*  Install Python for Windows x64  -see below
*  Create a working folder on your disk, perhaps in your Documents folder.
*  Copy these files from downloaded zip file to the working folder-
      TestExternalFiles.py
      RM-Python-config.ini
*  Download the SQLite extension: unifuzz64.dll   -see below
*  Move the unifuzz64.dll file to the working folder
*  Edit the RM-Python-config.ini in the working folder to specify the
   location of the RM file, the unifuzz64.dll file and the output report file.
   Some script functions may be turned on or off. The required edits should
   be obvious. (To edit, Open NotePad and drag the ini file onto the
   NotePad window.)
*  Double click the TestExternalFiles.py file to run the utility and
   generate the report file.
*  Examine the report output file.


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

Direct download link-
https://www.python.org/ftp/python/3.11.4/python-3.11.4-amd64.exe


The Python installation requires about 100 Mbytes.
It is easily and cleanly removed using the standard method found in Windows=>Settings

Run the Python installer selecting all default options.


======================================================================
unifuzz64.dll download-

Direct download link-
https://sqlitetoolsforrootsmagic.com/wp-content/uploads/2018/05/unifuzz64.dll

above link found in this context-
https://sqlitetoolsforrootsmagic.com/rmnocase-faking-it-in-sqlite-expert-command-line-shell-et-al/

The SQLiteToolsforRootsMagic website has been around for years and
is run by a trusted RM user. Many posts to public RootsMagic user forums
mention use of unifuzz64.dll from the SQLiteToolsforRootsMagic website.

======================================================================
NOTES

*  If no report file is generated, look at the black command console window for
    error messages that will help you fix the problem.

*  RM-Python-config.ini
   If there are any non-ASCII characters in the RM-Python-config.ini file,
   perhaps in a database path, or in ignored objects, then the file
   must be saved in UTF-8 format, with no byte order mark (BOM). This is
   a save option in NotePad.

*  UNREF_FILES
   If there is a difference in capitalization of file name or directory
   path in the database vs. the file system, the file will be listed as
   un-referenced.  (Unix-like file system case sensitivity)

*  General information: File paths pointing to external files
   in RM 7:   all paths are absolute starting with a drive letter
   in RM 8&9: absolute file path starting with a drive letter
           or
           a path relative to another location.
   RM 8&9 Relative path symbols
   (these are expanded when found in the first position of the stored path)
	~	home directory  (%USERPROFILE%)
	?	media folder as set in RM preferences
	*	RM main database file location

*   CHECK_FILES feature: file path case in the database or in the file system
    path name is not significant.

*   UNREF_FILES feature: The folder specified in RM's preferences as the Media
    folder is not necessarily the same as the folder specified by the
    SEARCH_ROOT_FLDR_PATH variable in the RM-Python-config.ini file, but it is
    recommended that they be the same.

    To shorten the list of unreferenced items, the IGNORED_OBJECTS section can
    be edited to list items to be ignored. The goal would be to produce a report
    file with no unreferenced filed found. This is an easy result to interpret.
    If a file is to be added to the folder that won't be referenced by
    RM, add it to the IGNORED_OBEJECTS section. The goal is to have this test
    produce no output under normal circumstances. If a file is added to the media
    folder and inadvertent not added to the RM database, it will show up here.

*   DUP_FILEPATHS feature:  Files may be duplicated in the media tab intentionally
    as they might have different captions etc.

*   DUP_FILENAMES feature:  Files listed have the same file names, ignoring case.
    Duplicate file names are not a problem. This function is provided as a
    troubleshooting tool

*   SHOW_ORIG_PATH feature: (RM 8&9 only)
    A display option is available for files found by either the CHECK_FILES or
    NO_TAG_FILES or DUP_FILES
    The option is turned on with the option SHOW_ORIG_PATH in the ini file.
    With this option on, the path for each file is shown twice,
    - the path on disk, that is, after any RM8 token in the path has been expanded.
    - the path as saved in the database with the token not expanded.

*   RMNOCASE_fake-SQLiteSpy64.dll
    An alternate for unifuzz64.dll named "RMNOCASE_fake-SQLiteSpy64.dll" has recently
    been created and has been successfully tested. The 2 dlls work equally well for this script.
    https://sqlitetoolsforrootsmagic.com/wp-content/uploads/2017/12/RMNOCASE_fake-SQLiteSpy64.dll.bak
    in the context of this page:
    https://sqlitetoolsforrootsmagic.com/rmnocase-faking-it-in-sqlitespy/rmnocase_fake-sqlitespy64-dll/

    After download, rename the file by removing the final ".bak"

*   Switching between RM 8 and RM 9
    If the machine running the script has had multiple versions of RootsMagic
    installed, over the years, there may be slightly unexpected behavior in some cases.
    RootsMagic saves some of its settings in an xml file located in the user's home
    folder/AppData/Roaming/RootsMagic. A separate sub folder is created for each RM major
    version. The script will read the Media Folder location setting found in the highest
    installed RM version xml file. This is fine if you are not using ver 8 after having
    installed ver 9, or when the same media folder location has been used for ver 8 and later.
    When run on a RM7 database, the Media Folder location is not needed so the xml file is
    not referenced, so switching  between ver 7 and ver 9 will not be an issue.



*   MD5 hash values are used to confirm the identity of files.
	MD5 hash							File size		File name
	06a1f485b0fae62caa80850a8c7fd7c2	256,406 bytes	unifuzz64.dll
	43fe353e3e3456dc33f8f60933dbc6ab	74,240 bytes	RMNOCASE_fake-SQLiteSpy64.dll


======================================================================
======================================================================
Sample report output-

++++++++++
++++++++++
Report generated at      = 2023-06-19 13:18:16
Database processed       = C:\Users\me\Genealogy\MyFile.rmtree
Database last changed on = 2023-06-18 13:29:41
SQLite library version   = 3.42.0

===============================================================DIV70==
=== Start of "Files Not Found" listing

File path not found:
"C:\Users\me\Documents\Genealogy\GeneDB\Exhibits\Dummy Birth File.txt"
File path not found:
"C:\Users\me\Documents\Genealogy\GeneDB\Exhibits\Misc\Morita, Tama b-1920jpg"


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

=== Start of "Duplicated File Paths" listing


    No Duplicate File Paths in Media Gallery were found.

=== End of "Duplicated File Paths" listing

===============================================================DIV70==

=== Start of "Duplicated File Names" listing

"Adkinson, Charles Alton b1948.jpg"
"Bales & Rose -e1960.jpg"
"Gastwirtschaft Eduard Otter.jpg"
"Marker-Plot cross reference.txt"

=== End of "Duplicated File Names" listing

===============================================================DIV70==
=== End of Report

++++++++++
++++++++++

======================================================================
TODO
*  Add code to find duplicate files represented by different relative paths in database.
*  Determine whether using the RMNOCASE collation in unifuzz64.dll will cause erroneous
   output in this utility. Ideally, one would first run reindex RMNOCARE using the
   collation in unifuzz64.dll, do the queries, and then rebuild index within RootsMagic
   using the RM's version of RMNOCASE. However, this utility DOES NOT MODIFY the database.
   No problems have bee detected so far.


======================================================================
Feedback
The author appreciates comments and suggestions regarding this software.
Richard.J.Otter@gmail.com

Public comments may be made at-
https://github.com/ricko2001/Genealogy-scripts/discussions

See my Linked-In profile at-
https://www.linkedin.com/in/richardotter/
