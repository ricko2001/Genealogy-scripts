# Genealogy-scripts and utilities

These are scripts I've written to help with my work with RootsMagic genealogy software. They directly access the SQLite database created by RootsMagic (RM) to store its data.

These are currently all Python, tested only on Windows 11 OS with Python 3x.

Probably the most useful for others will be:

## RELEASED:
### RM -Test external files
A utility to check status of external files linked to a RootsMagic file.
This only reads the RM file. No changes are made.
Release are available as zip files.


### RM -Group from SQL
A utility to quickly update a RM group by running an SQL query.
Makes changes to GroupTable and TagTable.
Release are available as zip files.

### RM -Citation Sort Order
A utility to allow the user to re-order the listing of citations attached to Persons, Names, or Facts. Uses python module RMDate.py in RM -Dates and Sort Dates


## NOT RELEASED
### RM -SQL for creating useful groups
As the name says, contains SQL that can be used by the GroupFromSQL utility.

### RM -Maintenance SQL
Consists of a Windows cmd script that runs a SQL file containing SQL updates 
that fix reoccurring problems in my database caused by user errors during 
data entry. The cmd script generates a report file which is then 
automatically displayed in NotePad++.


### RM -Switch source template
A utility to switch the source template used by one or a set of sources.
Preserves all linkages and allows remapping of field data.
This is the solution for modifying a SourceTemplate in use.

This makes changes to the RM file when run with the "MAKE_CHANGES" option. Be absolutely sure that a working backup is available. The script works, but you will likely want to re-run it several times to get the exact results that you desire.

My process is to always run the script on a copy of the main database. Then after iterating through fixes to the ini file and I'm satisfied with the results, I backup the main database and then move the copy with the changes done by the script to the main database file location.

This is close to release.


### RM -Lump misc sources
I started in TMG as splitting all sources. Now in RM, I am lumping the sources that make sense to me. So far, Find_a_Grave, Census and Social Security SSDI and SSACI. These scripts do that. They will most likely  need modification for your circumstances.
 

 ---

Released utilities are available as zip archives which include single file exe versions. No Python installation needed.
The others are saved in GitHub code as the simple .py text files.


If any of the other scripts are of interest, I may be persuaded to make them release-ready. Let me know.
