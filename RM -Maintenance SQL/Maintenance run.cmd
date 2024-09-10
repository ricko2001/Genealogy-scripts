rem @ECHO OFF
REM
REM  File paths must use doubled back slash due to Sqlite3.exe limitation

REM file locations

SET DATABASE=C:\\Users\\me\\Genealogy\\TEST.rmtree

SET RMNOCASE=C:\\Users\\me\\Genealogy\\SW\\unifuzz64.dll
REM see: https://sqlitetoolsforrootsmagic.com/wp-content/uploads/2018/05/unifuzz64.dll
SET REGEXP=C:\\Users\\me\\Genealogy\\SW\\regexp.dll
REM see: https://github.com/nalgeon/sqlean


SET SQL_FILE=.\\Maintenance-auto.sql

SET REPORT_FILE=..\\Report_Maintenance_Run.txt

REM Generate time stamp
FOR /F %%A IN ('WMIC OS GET LocalDateTime ^| FINDSTR \.') DO @SET B=%%A
SET TIMESTAMP=%B:~0,4%-%B:~4,2%-%B:~6,2%-%B:~8,2%%B:~10,2%%B:~12,2%

REM Create TempFile
SET TEMPFILE=%TEMP%\MaintenanceTempFile_%TIMESTAMP%.txt

if exist "%REPORT_FILE%" del  "%REPORT_FILE%"

REM Create the command file for sqlite3

echo .output "%REPORT_FILE%" > "%TEMPFILE%"
echo .changes on             >> "%TEMPFILE%"
echo .bail on                >> "%TEMPFILE%"
echo .open "%DATABASE%"      >> "%TEMPFILE%"
echo .load "%RMNOCASE%"      >> "%TEMPFILE%"
REM echo .load "%REGEXP%"        >> "%TEMPFILE%"
echo .echo on                >> "%TEMPFILE%"
echo .version                >> "%TEMPFILE%"
echo .                       >> "%TEMPFILE%"
echo .                       >> "%TEMPFILE%"
echo .                       >> "%TEMPFILE%"
echo --Database="%DATABASE%" >> "%TEMPFILE%"
echo --Date %TIMESTAMP%      >> "%TEMPFILE%"
echo --File "%SQL_FILE%"     >> "%TEMPFILE%"

copy "%TEMPFILE%" +"%SQL_FILE%" "%TEMPFILE%"

echo .quit                   >> "%TEMPFILE%"


REM echo =======================
REM echo contents of TEMPFILE
REM type "%TEMPFILE%"

SQLite3 < "%TEMPFILE%"


REM delete the temp file
del "%TEMPFILE%"

REM Display the report file in NotePad
REM "%PROGRAMFILES%\notepad++\notepad++.exe" "%REPORT_FILE%"
C:\Windows\system32\notepad.exe "%REPORT_FILE%"
