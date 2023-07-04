# Genealogy-scripts

These are scripts I've written to help with my
work with RootsMagic genealogy software.
They directly access the SQLite database created by RootsMagic (RM) to store its data.

These are currently all Python, tested only on Windows 11 OS.

Probably the most useful for others will be:

RM -Test external files
  A utility to check status of external files linked to a RootsMagic file.
  This only reads the RM file. No changes are made.

RM -Group from SQL
  A utility to quickly update a RM group by running an SQL query.

RM -Switch source template
  A utility to switch the source template used by one or a set of sources.
  Preserves all linkages and allows remapping of field data.

  This makes changes to the RM file when run with the "MAKE_CHANGES" option.
  Be absolutely sure that a working backup is available. The script works, but you
  will likely want to re-run it several times to get the exact results that you desire.

  My process is to always run the script on a copy of the main database.
  Then after iterating thru fixes to the ini file and I'm satisfies with the results,
  I backup the main database and then move the copy with the changes 
  done by the script to the main database file location.


These scripts are saved in GitHub code as the simple .py text files. 
Single file exe versions are also available in the Releases
part of the repo as zip files, accompanied by their sample ini file 
and ReadMe file.

If any of the other scripts are of interest, I may be persuaded to make them
release-ready. Let me know.
