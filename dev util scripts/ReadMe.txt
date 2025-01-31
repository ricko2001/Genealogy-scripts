===========================================DIV50==
Build script

Used as-is for most previous releases that built an exe file.
This is being changed so as to produce one release zip file containing all py scripts and docs.

The script will use the local _util_info.yaml file to determine which files
to package and will use the version info in the yaml to update the py source files before
being copied to release zip.




BuildRelease.py

along with the required _util_info.yaml file.

All copies in the util folders are hardlinks of BuildRelease.py
The local copies of the yaml file are not links.


===========================================DIV50==
DB  local copy maintenance

DB reset test db.cmd
DB get fresh copy.cmd

2 Windows command scripts to allow easy replacement of the local copy of the
 master database with a fresh copy or from the local backup.

The local copies have the name of the 2 higher folder name, 
usually the script folder name to distinguish the file names


===========================================DIV50==

