
TestExternalFiles.py

RootsMagic (RM) uses SQLite as its main storage. The database 
schema includes a table that links to external files using an 
absolute path starting with a drive letter. (UNC names have not 
been tested by me.)

As the number of linked files increases, it becomes more likely 
that user mistakes will happen. 
* A file on disk may get renamed, or moved, breaking the link 
    from the database. RM has tools to help fix these, but it does not 
    give a log of what was done.
* A file may be added to the media folder but then not linked in the
    database. Common when working quickly.

This utility will help identify both issues.

The utility can perform 3 functions, as indicated in the 
ini file Options section:

CHECK_FILES
   Checks that each file referenced in the RM database actually 
   exists on disk in the specified location.
   If all OK, the report section will be empty.

FOLDER_LIST
   Lists all folders referenced in the RM database.

UNREF_FILES
   Lists all files found in the folder SEARCH_ROOT_FLDR_PATH 
   that are NOT referenced in the RM database.
   Perhaps the file was add to the folder, but was not linked 
   to a fact or source in the database. 


To install and use:
*  Download and install Python for Windows x64 (use default options)  -see below
*  Download unifuzz64.dll   -see below
*  Create a folder on disk and copy these files to it-
      TestExternalFiles.py
      RM-Python-config.ini
      unifuzz64.dll
*  Edit the RM-Python-config.ini to specify the location of the RM file,  
   the unifuzz64.dll file and the output report file. Some script functions
   may be turned on or off. The required edits should be obvious.
*  Double click the TestExternalFiles.py file.
*  Examine the report output file.


Tested with RootsMagic v7.6.5  (will not work with RM 8 created database)
       Python for Windows v3.9.0   64bit  
       unifuzz64.dll (version number not set, MD5=06a1f485b0fae62caa80850a8c7fd7c2)
       Operating system= Window 10, 64bit


Python download-
https://www.python.org/ftp/python/3.9.6/python-3.9.6-amd64.exe
This link is in the context of-
https://www.python.org/downloads/windows/
Use the current version of Python, version > 3.9.0. 
Click on the link near the top of page. Then ...
Find the link near bottom of page, in "Files" section, labeled "Windows installer (64-bit)"
Click it and save the installer.

unifuzz64.dll download-
https://sqlitetoolsforrootsmagic.com/wp-content/uploads/2018/05/unifuzz64.dll
above link found in this context-
https://sqlitetoolsforrootsmagic.com/rmnocase-faking-it-in-sqlite-expert-command-line-shell-et-al/


Notes:
*  If there are any non-ASCII characters in the RM-Python-config.ini file, 
   perhaps in a database path, or in ignored objects, then the file 
   must be saved in UTF-8 format, with no byte order mark (BOM).

*  If there is a difference in capitalization of file name or directory path in the
   database vs. the file system, the file will be listed as un-referenced. 
   (Unix-like file system case sensitivity)

TODO
*  for files mentioned in the RM database, but not found 
at their specified location, include the database items 
that the file is tagged with.

