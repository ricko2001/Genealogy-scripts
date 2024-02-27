# Genealogy-scripts and utilities

updated: 2024-02-27

These are scripts I've written to help my work with RootsMagic genealogy software. They directly access the SQLite database used by RootsMagic (RM) to store its data.

These are currently all written in Python, tested only on Windows 11 x64 OS with Python 3x. Most have been tested only with RM v9 databases.
I don't have a MacOS computer to test with, but I'd guess that most could easily be ported. Let me know if you have any results.


"Released" means that-
* I've included an .exe file version of the Python script so Python installation is not required. 
* The ReadMe file is user friendly.
* All configuration is done through an ini file so the python code does not need to be changed.
* I've done significant amounts of testing.

The Release zip file packages are found in the Releases page, here on Github (https://github.com/ricko2001/Genealogy-scripts/releases)


If any of the other scripts are of interest, I may be persuaded to make them release-ready. Let me know.


## RELEASED:

### RM -Test external files
A utility to check status of external files linked to a RootsMagic file.
This only reads the RM file. No changes are made.
I find use of this app invaluable as part of my backup routine.


### RM -Group from SQL
A utility to quickly update a RM group by running an SQL query.
Makes changes to GroupTable and TagTable.


### RM -Change Source for a Citation
A simple utility to fix a particular kind of data entry mistake. It moves a citation from one master source to another. It does lots of error checking to prevent further errors.

The fix that this utility makes is trivial in SQL, but this app takes information that is available in the RootsMagic user interface and does all of the look ups for you. 


### RM -Citation Sort Order
A utility to allow the user to re-order the listing of citations attached to Persons, Names, or Facts. Uses python module RMDate.py in RM -Dates and Sort Dates


### RM -Convert Fact
Utility to change the fact type for a set of facts. For instance, convert all 
"Census (fam)" facts with date 1940 to "Census" facts. Handles witnesses and Fam->Personal conversions.
Probably most useful for projects imported from TMG, or when introducing a custom fact.


## NOT RELEASED

### RM -SQL for creating useful groups
As the name says, contains SQL that can be used by the GroupFromSQL utility.


### RM -Maintenance SQL
Consists of a Windows cmd script that runs a SQL file containing SQL updates 
that fix reoccurring problems in my database caused by user errors during 
data entry. The cmd script generates a report file which is then 
automatically displayed in NotePad++.


### RM -Change source template
A utility to switch the source template used by one or a set of sources.
Preserves all linkages and allows remapping of field data.
This is the solution for modifying a SourceTemplate in use.

This makes changes to the RM file when run with the "MAKE_CHANGES" option. Be absolutely sure that a working backup is available. The script works, but you will likely want to re-run it several times to get the exact results that you desire.

My process is to always run the script on a copy of the main database. Then after iterating through fixes to the ini file and I'm satisfied with the results, I backup the main database and then move the copy with the changes done by the script to the main database file location.

This is close to release.


### RM -Lump misc sources
I started in TMG as splitting all sources. Now in RM, I am lumping the sources that make sense to me. So far, Find_a_Grave, Census and Social Security SSDI, and all Ancestry collections. These scripts do that. They will most likely  need modification for your circumstances.


## NOTE-
I have a Github web site where I have links to these utilities and other RootsMagic related information.
https://RichardOtter.github.io
