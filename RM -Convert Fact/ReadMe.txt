ConvertFact
Utility application for use with RootsMagic databases

RootsMagic (RM) software uses a SQLite relational database as its data storage
file. Having access to that file via third party tools is a major advantage
to using RM.

This utility can convert all facts(also called events) of a certain type to 
facts of a different type. 
Facts in RM come in two styles: Personal and Family. Personal Facts are
attached to a single person while Family Facts are attached to a database
family.
A database family consists either 1 or 2 people, labeled internally as
Father and Mother. Either the father or mother may be "unknown"
and thus set to 0 in the database. Database families do not include any
offspring.
The utility will not create a new personal fact for a father ID=0 or add a 
mother ID=0 as a witness.

Allowed conversions:
Personal => Personal
Family => Personal
Family => Family

Not allowed:
Personal => Family

Simply changing the fact type for an existing fact is trivial. Complications arise
when the fact has witnesses or when a family fact is converted to a personal fact.

Any conversion of a fact that already has a witness involves assigning a new role to that witness. 
That's because each fact type has a different, independent set of possible roles. The role's main task, besides naming the role itsef, is to control which sentence is used for the witness in a narrative report

Family => Personal  fact conversion requires that the first person in the family (database name: Father) be assigned a new personal fact and the second person in the family (database name: Mother) be added as a witness with a particular role. That role is specified in the ini file as an input parameter.


FactTypes are listed in the "Fact type list" feature found in several places in the user interface- In the Edit Person windows upon clicking the + add fact button, in the three dot menu or in th command pallet. 
The input of fact types in the ini files uses the full fact type name, not the abbreviation. The full name is shown in the Edit Person window.




## Tested with RootsMagic v9.1.3
##             Python for Windows v3.11.0
##             unifuzz64.dll (ver not set, MD5=06a1f485b0fae62caa80850a8c7fd7c2)

    # Facts to convert				 new fact to create
    #  FTID	name				FTID	name			2nd person		RoleID
    #  311	Census fam			18		Census			spouse			420 
    #  310	Residence fam		29		Residence		spouse			417 
    # 1071	Psgr List fam 		1001	Psgr List		Principal2		421
    # 1066	Note fam			1026	Note			Principal2		416 


# consider whether the util should be more general say convert any fact tinto any other?

# the first person in fam fact will retain the new indiv fact, the second person will be shared fact.

# All of the roles used in the old fact must also appear in the new fact





======================================================================
Overview

This program is what is called a "command line utility".

To use it:

1:  Edit the supplied text file named "RM-Python-config.ini". (Hereinafter
    referred to, simply, as the "ini file".)
    The utility needs to know where the RM database file is located, which
    fact type to change, and where to create the report file.
    Editing the ini file can be done using the Windows NotePad app.

2:  Double click the ConvertFact file. This momentarily displays the
    black command console window and at the same time, generates the report
    text file.

3:  Examine the generated report text file that was opened in Notepad.
    The file will contain a summary of the changes made.


======================================================================
Capabilities

Sole function is to change all facts of a certain fact typ to a different fact tye.
Current limitation- the current fact must be a family type, the 
fact type to chnage to must be Personal fact type.


======================================================================
Compatibility

Tested with RootsMagic v9

.exe file version
       Windows 64bit only. Tested with Window 11.

.py file version
       Tested with Python for Windows v3.12   64bit
       The py file has not been tested on MacOS.
       The script could probably be modified to work on MacOS with Python
       version 3 installed.


======================================================================
Backups

IMPORTANT: This utility makes changes to the RM database file.
You must run this script on a copy of your database file or at least
have several known-good backups.
You will likely not be satisfied with the first run of the utility and will
want to try again.
Once you are satisfied, wait a week and the run it on a copy of your current database and
then use the modified database as your normal work file.


======================================================================
Getting Started

To install and use the exe single file version:

*  Create a working folder on your disk, perhaps in the same folder
   that contains your RM database.

*  Copy these files from the downloaded zip file to the working folder-
      ConvertFact.exe
      RM-Python-config.ini

*  Download the SQLite extension: unifuzz64.dll   -see below

*  Move the unifuzz64.dll file to the working folder

*  Edit the ini file in the working folder to specify the locations of the RM
   database file, the unifuzz64.dll file, and the output report file.

*  Double click the ConvertFact.exe file to run the utility and
   generate the report file.

*  Examine the report output file.


--- OR ---

Use the py script file.  

See section below, after the Notes section, entitled-
   "Which to use? Standalone .exe file or .py file"

======================================================================
NOTES

*   The ini file must be dited to indicate the work that should be done.
    The task is specified by the three values-
        FACT_CURRENT  = Census (family)
        FACT_NEW      = Census
        ROLE          = Spouse

    Note that the name can have embedded spaces.
    Space characters between the = and the name are ignored.


*   REPORT_FILE_DISPLAY_APP
    Option to automatically open the report file in a display application.
    The included ini sample file has this option activated and set to use Windows
    NotePad as the display app. It can be deactivated by inserting a # character
    at the start of the line. Your favorite editor may be substituted.

*   RM-Python-config.ini  (the ini file)
    If there are any non-ASCII characters in the ini file then the file must be
    saved in UTF-8 format, with no byte order mark (BOM).
    The included sample ini file has an accented ä in the first line comment to
    force it to be in the correct format.
    File format is an option in the "Save file" dialog box in NotePad.
    The [END] section is entirely optional.

*   Directory structure (optional)
    My directory structure, which of course, I recommend 🙂, is-

    Genealogy          (top level folder, mine is in my Home folder)
      myRD-DB.rmtree   (my main database file)
      Misc Databases   (folder for other databases I frequently use)
      Exhibits         (folder containing all media files in a folder hierarchy)
      SW               (folder containing various utility apps and the ini file)

*   Troubleshooting:
    If no report file is generated, look at the black command
    console window for error messages that will help you fix the problem.
    If no report file is generated and the black command console window closes
    before you can read it, try first opening a command line console and then
    running the exe or py file from the command line. The window will not close
    and you'll be able to read any error messages.

*   Troubleshooting:
    Error message- ... RM-Python-config.ini file contains a format error ...
    The problem is as stated, the solution may be harder to determine.
    You may want to look at- https://en.wikipedia.org/wiki/INI_file


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


======================================================================
To use the py script version of the app

To install and use the script file version:
*  Install Python for Windows x64  -see immediately below
*  Create a working folder on your disk, perhaps in the same folder
   that contains your RM database.
*  Copy these files from downloaded zip file to the working folder-
      ConvertFact.py
      RM-Python-config.ini
*  Download the SQLite extension: unifuzz64.dll   -see below
*  Move the unifuzz64.dll file to the working folder
*  Edit the ini file in the working folder to specify the location
   of the RM file and the output report file.
   Some utility functions may be turned on or off. The required edits should
   be obvious. The sample ini file is already configured with the most useful
   options turned on. (To edit, Open NotePad and drag the ini file onto the NotePad
   window.)
   The same ini file may be used with either the .exe or .py version of the utility.
*  Double click the TestExternalFiles.py file to run the utility and
   generate the report file.
*  Examine the report output file.

======================================================================
unifuzz64.dll download-

Direct download link-
https://sqlitetoolsforrootsmagic.com/wp-content/uploads/2018/05/unifuzz64.dll

above link found in this context-
https://sqlitetoolsforrootsmagic.com/rmnocase-faking-it-in-sqlite-expert-command-line-shell-et-al/

The SQLiteToolsforRootsMagic website has been around for years and
is run by a trusted RM user. Many posts to public RootsMagic user forums
mention use of unifuzz64.dll from the SQLiteToolsforRootsMagic website.

MD5( unifuzz64.dll ) = 06a1f485b0fae62caa80850a8c7fd7c2
size( unifuzz64.dll ) = 256,406 bytes


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

Direct link to recent (2024-02) version installer-
https://www.python.org/ftp/python/3.12.2/python-3.12.2-amd64.exe

The Python installation requires about 100 Mbytes.
It is easily and cleanly removed using the standard method found in
Windows=>Settings

Run the Python installer selecting all default options.


======================================================================
TODO
*  ?? what would you find useful?


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

======================================================================
