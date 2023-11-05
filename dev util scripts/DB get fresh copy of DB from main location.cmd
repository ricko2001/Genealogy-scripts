REM DB folder in in script development folder

SET PRODUCTION_FILE_PATH=C:\Users\rotter\Genealogy\GeneDB\Otter-Saito.rmtree

REM delete test database files
del "TEST.rmtree" "TEST-localcopy.rmtree"

copy "%PRODUCTION_FILE_PATH%" "TEST.rmtree"

REM create a local copy of the test DB
copy "TEST.rmtree" "TEST-localcopy.rmtree" 

pause