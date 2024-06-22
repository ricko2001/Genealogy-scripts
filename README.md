# Genealogy-scripts and utilities

updated: 2024-06-22

These are scripts I've written to help my work with RootsMagic genealogy software. They directly access the SQLite database used by RootsMagic (RM) to store its data.

Some are simple SQL in txt files, there are several Windows command files, and a number of Python
scripts.

The are tested only on Windows 11 x64 OS with Python 3x. Most have been tested only with RM v10 databases.
I don't have a MacOS computer to test with, but I'd guess that most could easily be ported. Let me know if you have any results.


"Released" scripts means that-
* I've included an .exe file version of the Python script so Python installation is not required.
* The release is version numbered.
* The ReadMe file has enough guidance for even a novice user.
* All configuration is done through an ini file so the python code does not need to be changed.
* All needed files are in a single zip archive for easy download.
* I've done significant amounts of testing.

The Release zip file packages are found in the Releases page, here on Github (https://github.com/ricko2001/Genealogy-scripts/releases)

If any of the other scripts are of interest, I may be persuaded to make them release-ready. Let me know.
Always interested in feedback.

## RELEASED:

### RM -Run SQL

This utility is meant to help the novice SQL user get the task done.
It attempts to eliminate most of the complications found using more
sophisticated off the shelf software.

This utility will run one or two SQL statements on a database and display the
results in a report file.

### RM -Test external files

A utility to check status of external files linked to a RootsMagic file.\
This only reads the RM file. No changes are made.\
I find use of this app invaluable as part of my backup routine.

### RM -Group from SQL

A utility to quickly update a RM group by running an SQL query.
Makes changes to GroupTable and TagTable.

### RM -Change Source for a Citation

A simple utility to fix a particular kind of data entry mistake. It moves a citation from one master source to another. It does lots of error checking to prevent further errors.

The fix that this utility makes is trivial in SQL, but this app takes information that is available in the RootsMagic user interface and does all of the look ups for you.

### RM -Change source template

A utility to switch the source template used by one or a set of sources.\
Preserves all linkages and allows remapping of field data.\
This is the solution for modifying a SourceTemplate in use.

My process is to always run the script on a copy of the main database. Then after iterating through fixes to the configuration file and I'm satisfied with the results, I backup the main database and then move the copy with the changes done by the script to the main database file location.

### RM -Citation Sort Order

A utility to allow the user to re-order the listing of citations attached to Persons, Names, or Facts.

### RM -Convert Fact

Utility to change the fact type for a set of facts. For instance, convert all
"Census (fam)" facts with date 1940 to "Census" facts. Handles witnesses and Fam->Personal conversions.\
Probably most useful for projects imported from TMG, or when introducing a custom fact.

### Non Python

### RM -SQL for creating useful groups

As the name says, contains SQL that can be used by the GroupFromSQL utility.

These are just SQL statements, not python scripts, so they won't be released
as the scripts above. But they have been extensively tested.
They don't modify the database, so little risk involved.

### RM -Maintenance SQL

Consists of a Windows cmd script that runs a SQL file containing SQL updates
that fix reoccurring problems in my database caused by user errors during
data entry. The cmd script generates a report file which is then
automatically displayed in NotePad.\
The Maintenance sql has been run on my production database many times.

## NOT RELEASED

### RM -Lump misc sources

I started in TMG as splitting all sources. Now in RM, I am lumping the sources for which it makes sense to me. So far, Find_a_Grave, Census and Social Security SSDI, and all Ancestry collections. These scripts do that. They will most likely need modification for your circumstances.


## NOTE-

I have a Github web site where I have links to these utilities and other RootsMagic related information.\
https://RichardOtter.github.io

# Python Packages used

## Required packages for running the scripts

Currently, 2 scripts use the custom "RMpy" python package located in the "RM -RMpy package" folder.
The exe files have it already included.
Those scripts using the package will find it if the folder structure is preserved. If the main script is 
moved elsewhere, copy the RMpy folder to be in the same directory as the main script.

## Required packages for building frozen executables (exe files)

For a new install or each upgrade of python, do the following:

Add to path-
C:\Users\rotter\AppData\Local\Programs\Python\PythonNNN\Scripts
(or update existing path to new ver number)

confirm pip is working or install pip 
Currently, see:  https://pip.pypa.io/en/stable/installation/

Install these packages:

pip install PyYAML

pip install pyinstaller

pip install pyinstaller-versionfile

