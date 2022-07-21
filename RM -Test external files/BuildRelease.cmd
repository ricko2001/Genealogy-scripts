@ECHO OFF

REM Update all files in local git
REM Test script.py, version.py, readme, hash

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

ECHO for release- use git tag name = %APPNAME%_v%VERSION_NUMBER%

pause

