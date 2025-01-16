# Genealogy-scripts and utilities

updated: 2025-01-16

These are scripts I've written to help my work with RootsMagic genealogy software. They directly access the SQLite database used by RootsMagic (RM) to store its data.

Some are simple SQL in txt files, there are several Windows command files, and a number of Python scripts.

The are tested only on Windows 11 x64 OS with Python 3x. Most have been tested only with RM v10 databases.
I don't have a MacOS computer to test with, but I'd guess that most could easily be ported. Let me know if you have any results.


"Released" scripts means that-

* The ReadMe file has enough guidance for even a novice user.
* All configuration is done through an ini file so the python code does not need to be changed.
* All needed files are in a single zip archive for easy download.
* I've done significant amounts of testing.
* The release is version numbered.

The Release zip file is found in the Releases page, here on Github (https://github.com/ricko2001/Genealogy-scripts/releases)

If any of the other scripts are of interest, I may be persuaded to make them release-ready. Let me know.
Always interested in feedback.

## RELEASED:

### RM -Run SQL

This utility is meant to help the novice SQL user get the task done.
It attempts to eliminate most of the complications found using more
sophisticated off the shelf software.

This utility will run one or two SQL statements on a database and display the
results in a report file. It will also run a SQL command script. 

### RM -Test external files

A utility to check status of external files linked to a RootsMagic file.\
This only reads the RM file. No changes are made.\
I find use of this app invaluable as part of my backup routine.

### RM -Group from SQL

A utility to quickly update a RM group by running an SQL query.\
Makes changes only to GroupTable.

### RM -Color from Group

A utility to quickly update a the color coding of people in specified RM groups.\
Makes changes only to PersonTable.

### RM -Change Source for a Citation

A simple utility to fix a particular kind of data entry mistake. It moves a citation from one master source to another. It does lots of error checking to prevent further errors.

The fix that this utility makes is trivial in SQL, but this app takes information that is available in the RootsMagic user interface and does all of the look ups for you.

### RM -Change source template

A utility to switch the source template used by one or a set of sources.\
Preserves all linkages and allows remapping of field data.\
This is the solution for modifying a SourceTemplate in use.

My process is to always run the script on a copy of the main database. Then after iterating through fixes to the configuration file and I'm satisfied with the results, I backup the main database and then move the copy with the changes done by the script to the main database file location.

### RM -Citation Sort Order

A utility to allow the user to re-order the listing of citations attached to Persons, Names, or Facts.\
See [SQLiteTools site](https://sqlitetoolsforrootsmagic.com/forum/topic/sorting-the-order-of-rm9-citations/) for a compatible SQL script that will update a  citations ordering in one step based on selected criteria.

### RM -Convert Fact

Utility to change the fact type for a set of facts. For instance, convert all
"Census (fam)" facts with date 1940 to "Census" facts. Handles witnesses and Fam->Personal conversions.\
Probably most useful for projects imported from TMG, or when introducing a custom fact.

## NOT RELEASED

### RM -Lump misc sources

I started in TMG as splitting all sources. Now in RM, I am lumping the sources for which it makes sense to me. So far, Find_a_Grave, Census and Social Security SSDI, and all Ancestry collections. These scripts do that. They will need modification for your circumstances. These are not released and require Python development to run.

## Non Python

### RM -SQL for creating useful groups

As the name says, contains SQL that can be used by the GroupFromSQL utility.

These are just SQL statements, not python scripts, so they won't be released
as the scripts above. But they have been extensively tested.
They don't modify the database, so little risk involved.

### RM -Maintenance SQL

Consists of a SQL command file containing SQL updates that fix reoccurring problems in my database caused by user errors during data entry.
There are parts of the script that are specific to my data entry practices. Read it before you run it.
The Maintenance SQL has been run on my production database many times.

## NOTE-

I have a Github web site where I have links to these utilities and other RootsMagic related information.\
https://RichardOtter.github.io

# Python Packages used

## Required packages for running the scripts

My later releases use the custom "RMpy" python package located in the "RM -RMpy package" folder. 

Those scripts using the package will find it if the folder structure is preserved. If the main script is moved elsewhere, copy the "RMpy" folder to be in the same directory as the main script.

## Required packages for building frozen executables (exe files)  NO LONGER USED

NOTE: the following lines substitute "me" for your user name, and NNN for the python ver code.

For a new install or each major upgrade of python, do the following:

Adjust path to include-
C:\Users\me\AppData\Local\Programs\Python\PythonNNN

so can start python with "python"
if you don't add it, use full path to invoke-
C:\Users\me\AppData\Local\Programs\Python\PythonNNN\Python


Adjust path to include-
C:\Users\me\AppData\Local\Programs\Python\PythonNNN\Scripts

if you don't add it, use full path to invoke-
C:\Users\me\AppData\Local\Programs\Python\PythonNNN\Scripts\pip


confirm pip is working 
by attempting to run it-

or install pip \
Currently, see:  https://pip.pypa.io/en/stable/installation/

can start pip in several ways:

|   command       |  comment  |
|---|---|
| pip | will work only if it is in the path|
| python -m pip |  will work only if python is in the path |
| py -m pip | only available as optional install using installer from python web site |


Install these packages:

python.exe -m pip install --upgrade pip

pip install --upgrade PyYAML

pip install --upgrade pyinstaller

pip install --upgrade pyinstaller-versionfile

# RM Utilities Release Format Change

News as of 2024-12-10\
A new release format was necessitated by a problem I was not aware of until recently. People who have previously attempted to download the utilities have probably been warned that the zip file contained a virus or malware. I was just told about the problem by a user.

I want to state emphatically that none of the files ever posted on my GitHub site ever posed an actual hazard. A google search for "PyInstaller virus warning" shows the magnitude of the issue. It is clear that malware has been packaged with the same software distribution system I was used (PyInstaller). The anti virus companies then created file signatures that detected these threats. Unfortunately, it seems like every piece of software packaged has the same "signature". The PyInstaller created exe file distribution method was very practical as users did not need to install Python software.

The Internet has gotten to be a dangerous place, and it seems there are fewer and fewer methods for non-corporate software developers to distribute ready-to-run files.

This means that I have removed the "exe" format file from the release zip and the user must now install Python to run the scripts.

## There are advantages to the new format:

All apps are now in the same zip file. Perhaps this will encourage users to try an app they didn't know they needed.

All apps are tested with each other using the same RMPy package (common code).

Less effort maintaining one release than the previous nine.

All of the software is human-readable. Each user can read the code and confirm that nothing bad is happening.

## TODO
I am still in the process of creating a release build script and improving the release folder's structure.
