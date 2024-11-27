TestExternalFiles

Utility application for use with RootsMagic databases

RootsMagic (RM) software uses a SQLite relational database as its data storage
file. Having access to that file via third part tools is a major advantage
to using RM.


=========================================================================DIV80==
Purpose

The database includes links to external files which RM calls "media files".
These files appear in the RM Media tab.

As the number of linked files increases, user errors become more likely.
* A file on disk may get renamed or moved, breaking the link from the database.
    RM has tools to fix these, but it does not give a log of what it has done.
    There is a report that can be run, but with effort.
* A file may be added to the media folder on disk but then not added to the
    database. A common oversight when working quickly.
* A file may be added to RM, but then detached from all source, facts etc,
    leaving it "un-tagged". No harm in leaving it, but de-cluttering may be
    desirable.
* A file may be added to the database more than once.
* A file from a far-flung folder may be added and it's location forgotten.
* A file may be renamed, or misplaced or its contents altered. One will not be
  able to verify the original file's contents are the same as in the current file.

This utility will identify these issues.
It is recommended to run this script daily as part of your backup routine.

A Hash file might be generated annually and archived with the full dataset.


=========================================================================DIV80==
Backups

IMPORTANT: This utility ONLY reads the RM database file. This utility cannot
change your RM file. However, until you trust that this statement is true,
you should run this script on a copy of your database file or at least
have several known-good backups.


=========================================================================DIV80==
Compatibility

Works with RootsMagic v7 through v10

.exe file version
       Windows 64bit only. Tested with Window 11.

.py file version
       Tested with Python for Windows v3.12 & 3.13   64bit
       The py file has not been tested on MacOS but could probably be easily
       modified to work on MacOS with Python version 3 installed.


=========================================================================DIV80==
Performance

A database with 7,000 media files requires about 3 seconds run time for 5
features turned on without hash file.
Generating a hash file for 7,000 image files takes roughly a minute.


=========================================================================DIV80==
Overview

This program is what is called a "command line utility". To install and use
the exe single file version:

*  Create a new folder on your disk.
   This will be called the "working folder".

*  Copy these files from the downloaded zip file to the working folder-
      TestExternalFiles.exe
      RM-Python-config.ini

*  Make a copy of your database, move the copy into the working folder.
   Rename the copy to TEST.rmtree

*  Edit the supplied text file named "RM-Python-config.ini". (Hereinafter
   referred to, as the "config file".)
   The utility needs to know where the RM database file is located, the output
   report file name and location, and the various configuration parameters
   needed to tell the utility what to do

*  Double click the TestExternalFiles file to run the utility and
   generate the report text file.

3:  Examine the generated report text file that was opened in Notepad.
    The file will contain the analysis results.

--- OR ---

Use the py script file.

See section below, after the Notes section, entitled-
   "Which to use? Standalone .exe file or .py file"


=========================================================================DIV80==
Capabilities

The utility can perform several functions, as configured in the config file's
OPTIONS section, either separately or in combination:

CHECK_FILES
    Checks that each file referenced in the RM database actually
    exists on disk at the specified location. Any file path link found in
    the database but not found on disk is listed.

UNREF_FILES
    Lists all files found in the folder specified by SEARCH_ROOT_FLDR_PATH in
    the config file (see below) that are NOT referenced in the RM database.
    This will find files that were perhaps added to the folder but were
    mistakenly never added to the database.
    This feature is designed for use when media files referenced by RM are all
    under a single folder hierarchy.

NO_TAG_FILES
    Lists all files found in RM's Media tab that have zero tags.

FOLDER_LIST
    Lists all folders referenced in the RM database.
    A file in an unexpected location may have been accidentally added to the
    database. This list will make it obvious.

NOT_MEDIA_FLDR
    Lists all files that are not in the RM "Media folder" as specified in the 
    RM preferences settings. Best practice is to set the "Media Folder" in 
    preferences and use that folder as the location for all media.

DUP_FILEPATHS
    Lists files that have been added more than one time to the database. These
    will appear more than once in RM's Media tab.

DUP_FILENAMES
    Lists files that have the same filename. This is not usually a problem, but
    being aware of the duplicate names may help your organizing efforts.

HASH_FILE
    Generates a text file containing a listing of each media file's name,
    location and HASH value, currently set to use MD5.
    https://en.wikipedia.org/wiki/MD5
    The HASH text file, when requested, is generated at the location
    specified in the config file.
    While MD5 is no longer considered secure for cryptography, it serves well
    for this purpose.


=========================================================================DIV80==
=========================================================================DIV80==
NOTES

*   CHECK_FILES feature: By default, folder path and file name capitalization in
    the database and in the  file system path name must match for the file to be
    found by this utility. They do not need to match for RM to find the file. 
    The author's opinion is that case miss-matches should be fixed.
    This behavior can be reversed by the setting the  
    option CASE_INSENSITIVE to "on".

*   UNREF_FILES
    This option is designed so that your goal should be to produce a report
    with no unreferenced files found. That result is easy to interpret.
    If a file is added to the media folder but not added to the RM database,
    it will show up om this list.

    However, there may be files and folders of files that you want to store
    near your media files, but are not actually referenced by the database.

    To shorten the list of unreferenced items, a specified set of files and folders
    within the SEARCH_ROOT_FLDR_PATH folder can be ignored and not displayed in the
    Unreferenced Files report. There are two methods of specifying the objects to ignore:
    1: the IGNORED_OBJECTS section can be used to tell the utility to not include 
    certain files in the list of unreferenced files. See below.
    2: The option IGNORED_ITEMS_FILE can be set to on of off. When the option is
    set to on, the specification of the files/folders to ignore is done by the
    file TestExternalFiles_ignore.txt which should be found in the
    SEARCH_ROOT_FLDR_PATH folder. The TestExternalFiles_ignore.txt file contains
    a set of exclusion patterns. A pattern may contain wildcard characters.
    The format of the patterns can be found in many on-line sources, for example-
      https://www.atlassian.com/git/tutorials/saving-changes/gitignore#git-ignore-patterns
      https://git-scm.com/docs/gitignore
    A sample file is included in the zip file.
    
    To use these kind of match patterns containing wild cards, one must turn on the
    option IGNORED_ITEMS_FILE, create a text file named TestExternalFiles_ignore.txt, 
    in the root of the SEARCH_ROOT_FLDR_PATH folder, and then edit that file to
    contain the patterns for the files to ignore.

    The TestExternalFiles_ignore.txt must be stored in utf-8 format if it contains non-ASCII 
    characters. (Same as for the config file)


*   IGNORED_OBJECTS

    FILES
    Add file names that should not be reported as being unreferenced.
    One name per line. Indented with at least one space character.
    No paths, just file names.
    All files with this name are ignored no matter where they are within
    the SEARCH_ROOT_FLDR_PATH folder

    FOLDERS
    Add folder names whose entire contents should not be reported as being
    unreferenced.
    One name per line. Indented with at least one space character.
    No paths, just folder names. (e.g. Folder1   and not  C:\Users\me\Folder1 )
    All folders with this name have their contents ignored no matter where they
    are within the SEARCH_ROOT_FLDR_PATH folder

    I suggest that you organize your file and folders so that ignored folders
    all have the same name, even though there may be many of them in different
    locations in the media folder.


*   SEARCH_ROOT_FLDR_PATH
    The folder specified in RM's preferences as the Media folder is not 
    necessarily the same as the folder specified by the SEARCH_ROOT_FLDR_PATH
    variable in the config file  (but I recommended that they be the same).


*   UNREF_FILES
    The value of- "# DB links minus # non-ignored files" should, in a
    sense, be zero. However, if a folder is ignored, but there are linked files
    within, then the value will be positive.


*   DUP_FILEPATHS
    Files with the same path and name may be duplicated in the media tab
    intentionally as they might have different captions etc.


*   DUP_FILENAMES
    Files listed have the same file names, ignoring case.
    Duplicate file names are not a error. This function is provided as a
    organizational tool. This feature does not check the file contents,
    only the names. Use the HASH_File feature to distinguish file contents.


*   SHOW_ORIG_PATH (RM v8 through v10 only)
    A display option is available for files found by either the CHECK_FILES or
    NO_TAG_FILES or DUP_FILES
    The option is turned on with the option SHOW_ORIG_PATH in the config file.
    With this option on, the path for each file is shown twice,
    - the path on disk, that is, after any RM8-9 token in the path has been expanded.
    - the path as saved in the database with the relative path anchor token not expanded.
    See the note below "Background information" regarding relative paths in RM.


*   REPORT_FILE_DISPLAY_APP
    Option to automatically open the report file in a display application.
    The included config file sample has this option activated and set to use Windows
    NotePad as the display app. It can be deactivated by inserting a # character
    at the start of the line. Your favorite editor may be substituted.


*   RM-Python-config.ini  (the config file)
    If there are any non-ASCII characters in the config file then the file must be
    saved in UTF-8 format, with no byte order mark (BOM).
    The included sample config file has an accented ä in the first line comment to
    force it to be in the correct format.
    File format is an option in the "Save file" dialog box in NotePad.
    The [END] section is entirely optional.


*   IGNORED_OBJECTS section of the config file
    Due to how the config file is parsed by the python library, files and folders
    whose names start with the # character cannot be added to the FILES or FOLDERS.
    Instead, they are considered comments. There is a way to overcome this
    limitation but the explanation of how is not worth the confusion it would
    create. Bottom line- if you really want to add the file or folder, change
    its name so it doesn't start with a # - or use the new ignore file method to
    exclude files.

*   A listing of "DB entires with blank filename or path found" is displayed when a
    media item in the database has a blank file path or file name. These items
    should be fixed first.


*   Background information: File paths pointing to external files
    in RM 7:   all paths are absolute starting with a drive letter
    in RM 8&9: absolute file path starting with a drive letter
            or
            a path relative to another location.
    RM 8&9 Relative path symbols
    (these are expanded when found in the first position of the stored path)
    ?    media folder as set in RM preferences
    ~    home directory  (%USERPROFILE%)
    *    RM main database file location


*   Switching between RM 8, RM 9 and RM 10
    This section probably applies to no-one. Please don't read it and get confused !
    If the machine running the script has had multiple versions of RootsMagic
    installed, over the years, there may be slightly unexpected behavior in some
    cases. RootsMagic saves some of its settings in an .xml file located in the
    user's home folder/AppData/Roaming/RootsMagic. A separate sub folder is
    created for each RM major version. The script will read the Media Folder
    location setting found in the highest installed RM version .xml file.
    This is fine if you are not using ver 8 after having installed ver 9, or
    when the same media folder location has been used for ver 8 and later.

    When run on a RM7 database, the Media Folder location is not needed so the
    XML file is not referenced, so switching  between ver 7 and ver 10 will not
    be an issue.


*  Files attached to RM Tasks are not analyzed by this utility and they do not 
   appear in the RM Media tab.


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

Probably the trickiest part of the config file is the IGNORED_OBJECTS section.
The FOLDERS and FILENAMES keys are multi-line values.
Each line of the value should be on a separate line indented with at least 
one blank. An empty line generates an error.
Multi-line values may not contain comment lines (lines starting with a #).

examples-

correct format-

[IGNORED_OBJECTS]
FOLDERS =
  Folder1
  Folder2
  Folder3


incorrect format- (empty line not allowed)

[IGNORED_OBJECTS]
FOLDERS =
  Folder1

  Folder2
  Folder3


incorrect format (not indented)

[IGNORED_OBJECTS]
FOLDERS =
  Folder1
Folder2
  Folder3


incorrect format- (no comments allowed)

[IGNORED_OBJECTS]
FOLDERS =
  Folder1
# Folder2
  Folder3

incorrect format- (# comment indicator only allowed at start of line)

[IGNORED_OBJECTS]
FOLDERS =    # a comment
  Folder1
  Folder2
  Folder3

incorrect format (no empty lines)

[IGNORED_OBJECTS]
FOLDERS =

  Folder1
  Folder2
  Folder3


=========================================================================DIV80==
=========================================================================DIV80==
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
   Only use the exe file that you downloaded from GitHub.com yourself.

--- OR ---

*   The .py Script File Version
  Pro:
   The script file is easily readable and one can confirm what it does.
   You may want to learn Python and make your own changes to the script
   and be able to use other scripts.
  Con:
   The script version requires an installation of the Python environment to run.
   This is a 100 MB investment in disk space. (Not big for modern day hard disks)


=========================================================================DIV80==
To use the py script version of the app

To install and use the script file version:

*  Install Python for Windows x64  -see immediately below

*  Create a new folder on your disk.
   This will be called the "working folder".

*  Make a copy of your database, move the copy into the working folder.
   Rename the copy to TEST.rmtree

*  Copy these files and the folder from the downloaded zip file to the working folder-
      TestExternalFiles.py
      RM-Python-config.ini
      RMpy

See the Overview section for the subsequent tasks.


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

Direct link to recent (2024-02) version installer-
https://www.python.org/ftp/python/3.12.2/python-3.12.2-amd64.exe

The Python installation requires about 100 Mbytes.
It is easily and cleanly removed using the standard method found in
Windows=>Settings

Run the Python installer selecting all default options.


=========================================================================DIV80==
TODO
*  Add code to find duplicate files represented by different relative paths
   in database.
*  ?? what would you find useful?


=========================================================================DIV80==
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


=========================================================================DIV80==
Distribution
Everyone is free to use this utility. However, instead of
distributing it yourself, please instead distribute the URL
of my website where I describe it- https://RichardOtter.github.io

=========================================================================DIV80==
