@ECHO OFF

ECHO Update all files in local git - make sure main branch is correct.
ECHO Test script.py, version.py, readme.txt
ECHO push code to github main

ECHO This script is to be run from the "RM -Test external files" folder
ECHO It will create a subfolder -  Release TestExternalFiles vn.n.n.n where all building is done.
ECHO That subfolder should be moved to the upper level Releases folder when ready.

REM ECHO Enter version number n.n.n.n
SET /P  VERSION_NUMBER="Enter version number n.n.n.n   "

SET APPNAME=TestExternalFiles

SET DIST_FLDR_NAME=%APPNAME% v%VERSION_NUMBER%

SET REL_FLDR=Release %APPNAME% v%VERSION_NUMBER%

ECHO Is the Version.py updated ?
pause

MKDIR ".\%REL_FLDR%"
MKDIR ".\%REL_FLDR%\%DIST_FLDR_NAME%"
xcopy ReadMe.txt             ".\%REL_FLDR%\%DIST_FLDR_NAME%"
xcopy RM-Python-config.ini   ".\%REL_FLDR%\%DIST_FLDR_NAME%"
xcopy TestExternalFiles.py   ".\%REL_FLDR%\%DIST_FLDR_NAME%"
xcopy Version.py             ".\%REL_FLDR%\%DIST_FLDR_NAME%"


cd ".\%REL_FLDR%\%DIST_FLDR_NAME%"

REM create the exe file
pyinstaller --onefile  --version-file Version.py  TestExternalFiles.py


del Version.py
move *.spec  .\build
copy dist\*.exe .
move build ..
move dist ..

cd ..

7za a -tzip "%DIST_FLDR_NAME%.zip" "%DIST_FLDR_NAME%"

pause

ECHO for RELEASE on GitHub- 
ECHO  Tag the local repo with an annotated tag  - no spaces allowed in tag name
ECHO  use git tag name = %APPNAME%_v%VERSION_NUMBER%
ECHO  push the local tag to github main
ECHO  tags can be deleted and or renamed-  see   https://phoenixnap.com/kb/git-rename-tag

ECHO  Draft a release
ECHO  Check previous title for patter (use spaces in title, not in tag)
ECHO  use release title  = %APPNAME% v%VERSION_NUMBER%

ECHO  Add release info, refer to previous descriptions for what to write.
ECHO  Add the zip file
ECHO  Save as draft and let it sit and age for a while
ECHO  Publish the release
ECHO  Write an announcement post to groups.
ECHO  


ECHO use git tag name = %APPNAME%_v%VERSION_NUMBER%

ECHO  ============================================
ECHO  END OF SCRIPT
ECHO  ============================================
pause

