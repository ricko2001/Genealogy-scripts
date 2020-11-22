import sqlite3
import sys
import os
from pathlib import Path


## Tested with RootsMagic v7.6.5
##             Python for Windows v3.9.0
##             unifuzz64.dll (ver not set, MD5=06a1f485b0fae62caa80850a8c7fd7c2)
##                   from:   https://sqlitetoolsforrootsmagic.com/rmnocase-faking-it-in-sqlite-expert-command-line-shell-et-al/

def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn



def ListFolders(conn):

    SqlStmt="""\
      SELECT  DISTINCT MediaPath
      FROM MultimediaTable
        ORDER BY MediaPath
"""
    cur = conn.cursor()
    cur.execute(SqlStmt)

    rows = cur.fetchall()
    print ("MultimediaTable has each of these folders mentioned at least once:\n\n")
    for row in rows:
        print(row[0])
    print (len(rows), "rows returned \n\n")

    return rows



def CheckAllFiles(conn):

    SqlStmt="""\
      SELECT  MediaPath, MediaFile
      FROM MultimediaTable
        ORDER BY MediaPath, MediaFile
"""
    cur = conn.cursor()
    cur.execute(SqlStmt)

    for row in cur:
      checkPath (row)



def checkPath( row ):
    dirPath=Path(row[0])
    filePath=Path(row[0] + row[1])

    #print (dirPath)
    #print (filePath)

    if not dirPath.exists(): 
       print ("Directory path not found:", "\"" + str(dirPath) + "\"")
       return
    else:
        if filePath.exists():
            if not filePath.is_file():
                print ("File path is not a file:", "\"" + str(filePath) + "\"")
                return
        else:
            print ("File path not found:", "\"" + str(filePath) + "\"")
            return
    #print ("Path OK:", "\"" + str(filePath) + "\"")
    return



def main():
    databasePath=os.getenv("DB_PATH")
    if databasePath == None:
    # test database
        databasePath = r"C:\Users\rotter\Documents\Genealogy\Genealogy SW\RootsMagic\SQL access\test DB\test copy Otter-Saito.rmgc"
    # production
        #databasePath = r"C:\Users\rotter\Documents\Genealogy\GeneDB\Otter-Saito.rmgc"

    RMNOCASE_extPath=os.getenv("RMNOCASEPATH")
    if RMNOCASE_extPath == None:
        RMNOCASE_extPath=r"C:\Users\rotter\Documents\Genealogy\Genealogy SW\RootsMagic\SQL access\RMNOCASE\unifuzz64.dll"


    # create a database connection
    
    conn = create_connection(databasePath)
    conn.enable_load_extension(True)
    conn.load_extension(RMNOCASE_extPath)

    print("Database in use:", databasePath)
    input("Press the <Enter> key to continue...")

    with conn:
       ListFolders(conn)
       input("Press the <Enter> key to continue...")
       CheckAllFiles(conn)

   # testData=[ r"C:\Users\rotter\source\Python\TestExternalFiles\ "[:-1] , "test.py"]
   # checkPath(testData)



if __name__ == '__main__':
    main()
    
