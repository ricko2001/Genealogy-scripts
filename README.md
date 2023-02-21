# Genealogy-scripts

These are scripts I've written to help with my
work with RootsMagic genealogy software.
They access the SQLite database created by RootsMagic (RM) to store its data.

These are currently all Python, tested only on Windows 11 OS.

Probably the most useful for others will be:

RM -Test external files
  A utility to check status of external files linked to a RootsMagic file.

  This only reads the RM file. No changes are made.


RM -Switch source template
  A utility to switch the source template used by one or a set of sources.
  Preserves all linkages and allows remapping of field data.

  This makes changes to the RM file when run with the "MAKE_CHANGES" option.
  Be absolutely sure that a working backup is available. The script works, but you
  will likely want to re-run it several times to get the exact results that please you.



These scripts are saved in GitHub code as the simple .py text files. 
Single file exe versions are also available in the Releases
part of the repo as zip files, accompanied by their sample ini file 
and ReadMe file.