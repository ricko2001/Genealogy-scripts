@ECHO OFF

REM Update all files in local git
REM Test py, version.py, readme, hash

REM ECHO Enter version number n.n.n.n
SET /P  VERSION_NUMBER=Enter version number n.n.n.n

SET APPNAME=TestExternalFiles

SET ZIP_FILE_NAME= %APPNAME% %VERSION_NUMBER%.zip

SET REL_FLDR=Release %APPNAME% %VERSION_NUMBER%

ECHO Is the Version.py updated ?
pause



MKDIR .\%REL_FLDR%
xcopy ReadMe.txt             .\%REL_FLDR%
xcopy RM-Python-config.ini   .\%REL_FLDR%
xcopy TestExternalFiles.py   .\%REL_FLDR%
xcopy Hash.txt               .\%REL_FLDR%
xcopy Version.py             .\%REL_FLDR%

cd .\%REL_FLDR%

REM create the exe file
pyinstaller --onefile  --version-file Version.py  TestExternalFiles.py

move *.spec  .\build

7za a -tzip * "%ZIP_FILE_NAME%"