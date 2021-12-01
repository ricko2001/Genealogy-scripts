import sqlite3
import os
import time
from pathlib  import Path
from datetime import datetime
import configparser
import xml.etree.ElementTree as ET

## WARNING make a known-good backup of the rmtree file before use.

##  Requirements: (see ReadMe.txt for details)
##   RootsMagic v8 database file
##   RM-Python-config.ini  ( Configuration ini file to set options and parameters)
##   unifuzz64.dll
##   Python v3.10 or greater

# TODO
# better error handling when opening database




G_Divider = "==========================================================="
G_QT = "\""


# ================================================================
def create_DBconnection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


# ================================================================
def GetListOfRows ( conn, SqlStmt):
    # SqlStmt should return a set of single values
    cur = conn.cursor()
    cur.execute(SqlStmt)

    result = []
    for t in cur:
      for x in t:
        result.append(x)
    return result


# ================================================================
def runSQL ( conn, SqlStmt):
    # SqlStmt should return nothing
    cur = conn.cursor()
    cur.execute(SqlStmt)
    return



# ================================================================
def GetOldSrc ( conn, SourceID):
    return

# ================================================================
def MoveCitation ( conn, oldSourceID, newSourceID):
    # get citations for oldSourceID
    SqlStmt = """
    SELECT CitationID
      FROM CitationTable
      WHERE SourceID = ?
      """

    cur = conn.cursor()
    cur.execute(SqlStmt, (oldSourceID,))
    citationsIDs = cur.fetchall()

    # test number of citatons found
    if len(citationsIDs) == 0 :
        return
    if len(citationsIDs) > 1 :
        print( "an old source has more than one citation /n", oldSourceID )
        return

    citationIDToMove = citationsIDs[0][0]


# Copy the SourceTable.Name => CitationTable.CitationName
# Copy the SourceTable.UTCModDate => CitationTable.UTCModDate
    SqlStmtXX = """
    UPDATE CitationTable
      SET CitationName = (SELECT Name       FROM SourceTable WHERE SourceID = ?),
      SET UTCModDate   = (SELECT UTCModDate FROM SourceTable WHERE SourceID = ?),
      SET ActualText   = (SELECT ActualText FROM SourceTable WHERE SourceID = ?),
      SET Comments     = (SELECT Comments   FROM SourceTable WHERE SourceID = ?)
      WHERE CitationID = ?
      """

    SqlStmt = """
    UPDATE CitationTable
      SET (CitationName, ActualText, Comments, UTCModDate) = (SELECT Name, ActualText, Comments, UTCModDate FROM SourceTable WHERE SourceID = ?)
      WHERE CitationID = ?
      """
    cur = conn.cursor()
    cur.execute(SqlStmt, (oldSourceID, citationIDToMove))

    # Get the SourceTable.Fields BLOB
    SqlStmt = """
    SELECT Fields
      FROM SourceTable
      WHERE SourceID = ?
      """
    cur = conn.cursor()
    cur.execute(SqlStmt, (oldSourceID,))
    srcFieldsStr = cur.fetchone()[0]

    root = ET.fromstring(srcFieldsStr)

    MediaFolderPathEle = root.find( "./Folders/Media")



#  move the existing citation to the new source
    SqlStmt = """
    UPDATE CitationTable
      SET SourceID = ?
      WHERE CitationID = ?
      """

    cur = conn.cursor()
    cur.execute(SqlStmt, (newSourceID, citationIDToMove))

# don't delete untill data copied to new citation

    SqlStmt = """
    DELETE from SourceTable
      WHERE SourceID = ?
      """
    cur.execute(SqlStmt, (oldSourceID,))

    conn.commit()

    return


# ================================================================
def Convert (conn, oldSrc, NewSourceID):
    MoveCitation ( conn, oldSrc, NewSourceID)

    return



# ================================================================
def TimeStamp():
     # return a TimeStamp string
     now = datetime.now()
     dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
     return dt_string


# ================================================================
def main():

    # Configuration file
    #  IniFile="C:/Users/rotter/Development/Genealogy/Genealogy-scripts/RM -LumpSources/" + "RM-Python-config.ini"
    IniFile="RM-Python-config.ini"

    # ini file must be in "current directory" and encoded as UTF-8 if non-ASCII chars present (no BOM)
    if not os.path.exists(IniFile):
        print("ERROR: The ini configuration file, " + IniFile + " must be in the current directory." )
        return

    config = configparser.ConfigParser()
    config.read(IniFile, 'UTF-8')

    # Read file paths from ini file
    database_Path = config['File Paths']['DB_PATH']
    RMNOCASE_Path = config['File Paths']['RMNOCASE_PATH']

    if not os.path.exists(database_Path):
        print('Database path not found')
        return


    # Process the database
    with create_DBconnection(database_Path) as conn:
      conn.enable_load_extension(True)
      conn.load_extension(RMNOCASE_Path)

    # specific to each run
    # specify which source is to get the converted citations
    NewSourceID = 5502

    # specific to each run
    # List the sources to be lumped
    SqlStmt="""\
SELECT SourceID
  FROM SourceTable
  WHERE  Name LIKE 'SSDI%'
         AND TemplateID=10008
"""


    SourcesToLump = GetListOfRows( conn, SqlStmt)

    for oldSrc in SourcesToLump:
    # let's just do one
   # oldSrc = 66
        print (oldSrc)
        Convert (conn, oldSrc, NewSourceID)

    return 0


# ================================================================
# Call the "main" function
if __name__ == '__main__':
    main()