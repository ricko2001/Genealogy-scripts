import sqlite3
import os
from pathlib  import Path
from datetime import datetime
import configparser

import xml.etree.ElementTree as ET


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
def getSchema(conn):

    SqlStmt="""\
      SELECT  DataRec
      FROM    ConfigTable
      WHERE   RecType = 1
"""
    cur = conn.cursor()
    cur.execute(SqlStmt)
    cur.arraysize=5
    rows = cur.fetchmany()

    if len(rows) != 1:
       print ( "ConfigTable has more than 1 RecType=1 record. Bad database structure.")
       return

    xmlBytes = (rows[0][0])
    # RM saves a UTF-8byte order mark at start of BLOB.
    # It is automatically removed when converting to a UTF-8 string
    xmlText = str(xmlBytes, encoding="utf-8")

    root = ET.fromstring(xmlText)
    print ( root.tag )

    for child in root:
      print(child.tag, child.text)
    
    Version = root.find('Version').text
    STVersion = root.find('STVersion').text
    
    print( "\n\n\n\n\n\n" )
    print( Version )
    print( STVersion )

# ================================================================


# ================================================================


# ================================================================

     
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
    
    print ("Database processed  = " + database_Path + "\n\n\n")
   # Process the database
   
    with create_connection(database_Path) as conn:
      conn.enable_load_extension(True)
      conn.load_extension(RMNOCASE_Path)
      getSchema(conn)


       

if __name__ == '__main__':
    main()
    