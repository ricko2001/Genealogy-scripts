@ECHO OFF
REM
REM
REM  File paths must use either doubled back slash or
REM     forward slash due to Sqlite3.exe limitation

REM requires SQLite3.exe from
REM https://sqlite.org/download.html
REM see download labeled: sqlite-tools-win-x64-3440200.zip
REM   A bundle of command-line tools for managing SQLite database files ...

REM file locations
SET DATABASE=DB/TEST.rmtree
REM SET DATABASE=../Otter-Saito.rmtree

SET RMNOCASE=C:/Users/rotter/Genealogy/GeneDB/SW/unifuzz64.dll
SET SQL_FILE=./Maintenance-auto.txt
REM SET REPORT_FILE=Report_Maintenance_Run.txt
SET REPORT_FILE=../Report_Maintenance_Run.txt

REM Generate time stamp
FOR /F %%A IN ('WMIC OS GET LocalDateTime ^| FINDSTR \.') DO @SET B=%%A
SET TIMESTAMP=%B:~0,4%-%B:~4,2%-%B:~6,2%-%B:~8,2%%B:~10,2%%B:~12,2%

REM Create TempFile
SET TEMPFILE=%TEMP%\MaintenanceTempFile_%TIMESTAMP%.txt

echo "%TEMPFILE%"

echo --Command file for Mainetance SQL run > "%TEMPFILE%"
echo .echo on                >> "%TEMPFILE%"
echo .output "%REPORT_FILE%" >> "%TEMPFILE%"
echo .version                >> "%TEMPFILE%"
echo .changes on             >> "%TEMPFILE%"
echo .bail on                >> "%TEMPFILE%"
echo .open "%DATABASE%"      >> "%TEMPFILE%"
echo .databases              >> "%TEMPFILE%"
echo .load "%RMNOCASE%"      >> "%TEMPFILE%"
echo -- File "%SQL_FILE%"    >> "%TEMPFILE%"
copy "%TEMPFILE%" +"%SQL_FILE%" "%TEMPFILE%"
echo .quit                   >> "%TEMPFILE%"


echo =======================
REM echo contents of TEMPFILE
REM type "%TEMPFILE%"

SQLite3 < "%TEMPFILE%"


REM delete the temp file
del "%TEMPFILE%"

REM Display the report file in NotePad++
"%PROGRAMFILES%\notepad++\notepad++.exe" "%REPORT_FILE%"
