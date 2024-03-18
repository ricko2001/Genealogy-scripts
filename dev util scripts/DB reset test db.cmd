REM reset the TEST database from the local backup copy

SET DB_EXTEN=rmtree
SET DEV_DB_PATH=.

SET DEV_DB_NAME=TEST
SET DEV_DB_BACKUP=TEST_dev_backup

REM delete existing dev test database and local backup
del "%DEV_DB_PATH%\%DEV_DB_NAME%.%DB_EXTEN%" 

REM create a local backup copy of the test DB
copy "%DEV_DB_PATH%\%DEV_DB_BACKUP%.%DB_EXTEN%" "%DEV_DB_PATH%\%DEV_DB_NAME%.%DB_EXTEN%"

REM pause and request input to close window - optional
pause