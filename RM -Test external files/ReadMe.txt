
TestExternalFiles.py

RootsMagic (RM) uses SQLite as its main storage. The database 
schema includes a table that points to external files.


As the number of linked files increases, it becomes more likely 
that user errors will happen. 
* A file on disk may get renamed, or moved, breaking the link 
    from the database. RM has tools to help fix these, but it does not 
    give a log of what was done. There is a report that can be run, but
    with effort.
* A file may be added to the media folder but then not attached to the
    desired database element. Common when working quickly.

This utility will help identify both issues.

The utility can perform 3 functions, as specified in the 
ini file Options section:

CHECK_FILES
   Checks that each file referenced in the RM database actually 
   exists on disk in the specified location.

UNREF_FILES
   Lists all files found in the folder SEARCH_ROOT_FLDR_PATH 
   that are NOT referenced in the RM database.
   Perhaps the file was added to the folder, but was mistakenly never 
   linked to an item in the database.
   This is designed for use when media files referenced by RM are all 
   in a single folder hierarchy.
   NOTE: the RM specified Media folder is not considered, only the 
   SEARCH_ROOT_FLDR_PATH specified in the RM-Python-config.ini file.
   You can set SEARCH_ROOT_FLDR_PATH in the ini file to the RM media folder, 
   if that is where the media files are.

FOLDER_LIST
   Lists all folders referenced in the RM database. A file in an unexpected location
   may have been accidentally added to the database. This list will make it obvious.
   For RM8 files, folder paths may be prefixed 
   with either ~ (home directory) or ? (RM specified media folder)


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
*  Double click the TestExternalFiles.py file to run the 
   script and generate the report file. 
   (5,000 media files requires about 3 seconds tun time)
*  Examine the report output file.

The Python installation requires about 100 Mbytes. 
It is easily and cleanly removed using the standard method found in Windows=>Settings  
All other components are very small.


Tested with RootsMagic v7.6.5 and v8.1.8.0
       Python for Windows v3.10.2   64bit  
       unifuzz64.dll (version number not set, MD5=06a1f485b0fae62caa80850a8c7fd7c2)
       Operating system Window 11, 64bit


Python download-
https://www.python.org/ftp/python/3.9.6/python-3.9.6-amd64.exe
This link is in the context of-
https://www.python.org/downloads/windows/
Use the current version of Python, version > 3.10.0. 
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

*  File paths pointing to external files
   in RM7: absolute file path starting with a drive letter
   in RM8: absolute file path starting with a drive letter
           or
           a path relative to another location.
   RM8 Relative path symbols 
   (these are expanded when found in the first position of the stored path)
	~	home directory  (%USERPROFILE%)
	?	media folder as set in RM preferences
	*	RM main database file location
	.	???


TODO
*  improve display of unreferenced files output when there are none to display. 
   Make it look more like the missing files display.



