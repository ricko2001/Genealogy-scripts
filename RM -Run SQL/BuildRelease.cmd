@ECHO OFF

SET APPNAME=RunSQL

SET VERSION_NUMBER=0.9.1


ECHO Update all files in local git - make sure main branch is correct.
ECHO Test script.py, version.py, readme.txt
ECHO push code to github main

ECHO This script is to be run from the "RM -<fldr name>" folder, where the py file is.
ECHO It will create a subfolder -  Release %APPNAME% v%VERSION_NUMBER%   where all building is done.
ECHO That subfolder should be moved to the upper level Releases folder when done.

ECHO Reminders
ECHO Is the Version.py updated in both places ?



SET DIST_FLDR_NAME=%APPNAME% v%VERSION_NUMBER%

SET REL_FLDR=Release %APPNAME% v%VERSION_NUMBER%


MKDIR ".\%REL_FLDR%"

type nul > "%REL_FLDR%\Build_Log.txt"
REM create empty build log file to be filled in by user

IF EXIST ".\%REL_FLDR%\%DIST_FLDR_NAME%" (
  ECHO Folder already exists
  pause
  exit /B )
MKDIR ".\%REL_FLDR%\%DIST_FLDR_NAME%"
REM These are files that will be distributed in the zip

xcopy ReadMe.txt                ".\%REL_FLDR%\%DIST_FLDR_NAME%"
xcopy RM-Python-config.ini      ".\%REL_FLDR%\%DIST_FLDR_NAME%"
xcopy %APPNAME%.py              ".\%REL_FLDR%\%DIST_FLDR_NAME%"
xcopy Version.py                ".\%REL_FLDR%\%DIST_FLDR_NAME%"

cd ".\%REL_FLDR%\%DIST_FLDR_NAME%"

REM create the exe file
pyinstaller --onefile  --version-file Version.py  %APPNAME%.py


del Version.py
move *.spec  .\build
copy dist\*.exe .
move build ..
move dist ..
cd ..

7za a -tzip "%DIST_FLDR_NAME%.zip" "%DIST_FLDR_NAME%"

pause
ECHO  RELEASE PROCEDURE for GitHub
ECHO  
ECHO  use git tag name = %APPNAME%_v%VERSION_NUMBER%
ECHO  
ECHO  see -  https://git-scm.com/docs/git-tag
ECHO  Tag the local repo with an annotated tag  - no spaces allowed in tag name
ECHO  git tag --annotate %APPNAME%_v%VERSION_NUMBER%
ECHO  write text in default text editor, save and close. Perhaps mini release notes?
ECHO  
ECHO  push the local tag to github main
ECHO  git push origin %APPNAME%_v%VERSION_NUMBER%
ECHO  
ECHO  tags can be deleted and or renamed-  see   https://phoenixnap.com/kb/git-rename-tag
ECHO  
ECHO  Draft a release
ECHO  Check previous title for pattern (use spaces in title, not in tag)
ECHO  use release title  = %APPNAME% v%VERSION_NUMBER%
ECHO  
ECHO  Add release info, refer to previous descriptions for what to write.
ECHO  Add the zip file
ECHO  Save as draft and let it sit and age for a while
ECHO  Publish the release
ECHO  Write an announcement post to groups.
ECHO  
ECHO  in Terminal use - Shift-Control-A,  Shift-Control-C  
ECHO  and paste into a new Build_output.txt file, and put it into Release folder/
ECHO  
ECHO  ============================================
ECHO  END OF SCRIPT
ECHO  ============================================
pause

