REM Copy the production database to the local dev database folder

SET DB_EXTEN=rmtree

SET PRODUCTION_DB_PATH=C:\Users\rotter\Genealogy\GeneDB
SET PRODUCTION_DB_NAME=Otter-Saito

SET DEV_DB_PATH=.

REM Get the script folder name
SET DB_DIR=%cd%
cd ..
REM get current folder name
for %%I in (.) do set CurrDirName=%%~nxI
cd "%DB_DIR%"

SET DEV_DB_NAME=TEST-%CurrDirName%
SET DEV_DB_BACKUP=BACKUP_TEST_-%CurrDirName%

REM delete existing dev test database and local backup
del "%DEV_DB_PATH%\%DEV_DB_NAME%.%DB_EXTEN%"
del "%DEV_DB_PATH%\%DEV_DB_BACKUP%.%DB_EXTEN%"

REM This is the only reference to the production database environment
copy "%PRODUCTION_DB_PATH%\%PRODUCTION_DB_NAME%.%DB_EXTEN%" "%DEV_DB_PATH%\%DEV_DB_NAME%.%DB_EXTEN%"

REM create a local backup copy of the test DB
copy "%DEV_DB_PATH%\%DEV_DB_NAME%.%DB_EXTEN%" "%DEV_DB_PATH%\%DEV_DB_BACKUP%.%DB_EXTEN%"

REM pause and request input to close window - optional
REM pause

