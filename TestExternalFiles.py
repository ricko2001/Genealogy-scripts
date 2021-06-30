import sqlite3
import os
from pathlib  import Path
from datetime import datetime
import configparser

## Tested with RootsMagic v7.6.5  (not tested with RM 8)
##             Python for Windows v3.9.0
##             unifuzz64.dll (ver not set, MD5=06a1f485b0fae62caa80850a8c7fd7c2)
##                   from:   https://sqlitetoolsforrootsmagic.com/rmnocase-faking-it-in-sqlite-expert-command-line-shell-et-al/

## Configuration ini file:    RM-Python-config.ini
## exmaple ini file:
#        
#        [File Paths]
#        DB_PATH      = C:\MyDatabae.rmgc
#        REPORT_PATH  = C:\Exhibit File report.txt  
#        RMNOCASE_PATH = C:\RMNOCASE\unifuzz64.dll
#        
##

# TODO
# implement "NotReferencedFile function
# better error handling opening database
# check database schema version


# ================================================================
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


# ================================================================
def ListFolders(conn, reportF):

    SqlStmt="""\
      SELECT  DISTINCT MediaPath
      FROM MultimediaTable
        ORDER BY MediaPath
"""
    cur = conn.cursor()
    cur.execute(SqlStmt)

    rows = cur.fetchall()
    reportF.write ("Folder List:\n\n")
    for row in rows:
        reportF.write(row[0] + "\n")
    reportF.write (str(len(rows)) + "  rows returned \n\n")

    return rows



# ================================================================
def CheckAllFiles(conn, reportF):

    SqlStmt="""\
      SELECT  MediaPath, MediaFile
      FROM MultimediaTable
        ORDER BY MediaPath, MediaFile
"""
    cur = conn.cursor()
    cur.execute(SqlStmt)
    
    reportF.write ("File not found warnings:\n\n")

    for row in cur:
      checkPath (row, reportF)



# ================================================================
def checkPath( row, reportF ):
    dirPath=Path(row[0])
    filePath=Path(row[0] + row[1])

    if not dirPath.exists(): 
       reportF.write ("Directory path not found:" + "\"" + str(dirPath) + "\"" + "\n")
       return
    else:
        if filePath.exists():
            if not filePath.is_file():
                reportF.write ("File path is not a file:" + "\"" + str(filePath) + "\"" + "\n")
                return
        else:
            reportF.write ("File path not found:" + "\"" + str(filePath) + "\"" + "\n")
            return
    #print ("Path OK:", "\"" + str(filePath) + "\"")
    return


# ================================================================
def NonReferencedFiles():
     # TODO
     return


# ================================================================
def TS():
     # datetime object containing current date and time
     now = datetime.now()
     dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
     return dt_string
     
# ================================================================
def main():
    # Configuration
    IniFile="RM-Python-config.ini"
    
    # ini file must be in current directory
    if not os.path.exists(IniFile):
        print("The ini configuration file, " + IniFile + " must be in the current directory." )
        return

    config = configparser.ConfigParser()
    config.read('RM-Python-config.ini')
    
    # Read file paths from ini file
    report_Path = config['File Paths']['REPORT_PATH']
    database_Path = config['File Paths']['DB_PATH']
    RMNOCASE_Path = config['File Paths']['RMNOCASE_PATH']

    if not os.path.exists(database_Path):
        print('Database path not found')
        return
    
   # Process the database
   
    with create_connection(database_Path) as conn:
      conn.enable_load_extension(True)
      conn.load_extension(RMNOCASE_Path)
    
      with open( report_Path, "w") as reportF:
      
        reportF.write ("report generated at = " + TS() + "\n")	
        reportF.write ("Database processed  = " + database_Path + "\n\n\n")
        
        CheckAllFiles(conn, reportF)
        
        reportF.write ("\n\n\n")
        
        ListFolders(conn, reportF)
        
        reportF.write ("\n\n\n")

        NonReferencedFiles()
        
        reportF.write ("\n\n\n")
       
        reportF.write ("End of report \n")
  
       

if __name__ == '__main__':
    main()
    
