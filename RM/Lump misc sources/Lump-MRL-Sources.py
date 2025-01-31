import sqlite3
import os
import time
from pathlib  import Path
from datetime import datetime
import configparser
import xml.etree.ElementTree as ET
import sys




## WARNING make a known-good backup of the rmtree file before use.

##  Requirements: (see ReadMe.txt for details)
##   RootsMagic v9 database file
##   RM-Python-config.ini  ( Configuration ini file to set options and parameters)
##   unifuzz64.dll
##   tested with Python v3.10

# ================================================================
def main():

    # Configuration file
    IniFile="RM-Python-config.ini"

    # ini file must be in "current directory" and encoded as UTF-8 if non-ASCII chars present (no BOM)
    if not os.path.exists(IniFile):
        print("ERROR: The ini configuration file, " + IniFile + " must be in the current directory." )
        return

    config = configparser.ConfigParser(
                      empty_lines_in_values=False, 
                      interpolation=None)
    config.read(IniFile, 'UTF-8')

    # Read file paths from ini file
    database_Path = config['FILE_PATHS']['DB_PATH']
    RMNOCASE_Path = config['FILE_PATHS']['RMNOCASE_PATH']

    if not os.path.exists(database_Path):
        print('Database path not found. Fix configuration file and try again.')
        return

    OldSourceTemplate =  10023   # _Title, Date; Name [etc]
    NewSourceID = 6643           #  MRdb-Lohr, Bayern
    NewSourceTemplateID = 10059  # __MR-Lohr

    # Process the database
    with create_DBconnection(database_Path) as conn:
      conn.enable_load_extension(True)
      conn.load_extension(RMNOCASE_Path)


    # Deal with index and the fact that the RMNOCASE collation is different here than in RM
    SqlStmt= """
     REINDEX RMNOCASE;
     """
    cur = conn.cursor()
    cur.execute(SqlStmt)

# List the sources to be lumped
    SqlStmt="""\
SELECT SourceID
  FROM SourceTable
  WHERE  Name LIKE 'MR-L%'
         AND TemplateID=10023
"""
    # TemplateID = OldSourceTemplateID
    # GetListOfRows too limited with param

    SourcesToLump = GetListOfRows( conn, SqlStmt)
    print ("number of source to process: ", len(SourcesToLump))

    for oldSrc in SourcesToLump:
        print ("=====================================================")
        print (oldSrc)
        ConvertSrcToCit (conn, oldSrc, NewSourceID)

    return 0


# ================================================================
def ConvertSrcToCit ( conn, oldSourceID, newSourceID):
    # move the single "-" citation in old source to the new source

    citationIDsToMove= getCitationsToMove(conn,oldSourceID)

    # right now, only deal with case where # cits == 1
    if len(citationIDsToMove) != 1:  return

    citNum=0
    for citationIDToMove in citationIDsToMove:
        citNum = citNum + 1
        #if citNum > 1: input("cit enter to continue")


    # Copy the Standard and hidden fields from old src to citationToMove
    # should be fixed in cases where existing citations have info in the note fields
        SqlStmt = """
        UPDATE CitationTable
          SET (CitationName, 
               ActualText, 
               Comments, 
               UTCModDate) = 
                (SELECT 
                   Name, 
                   ActualText,
                   Comments,
                   UTCModDate 
                 FROM SourceTable 
                 WHERE SourceID = ?)
          WHERE CitationID = ?
          """
        cur = conn.cursor()
        cur.execute(SqlStmt, (oldSourceID, citationIDToMove))

    # Change owner & type for web tags attached to old source so they follow the citationToMove
    # do web tags already attached to the citationToMove remain attached?

        SqlStmt = """
        UPDATE URLTable
          SET OwnerType = 4,
              OwnerID = ? 
          WHERE OwnerType = 3 AND OwnerID = ?
          """
        cur = conn.cursor()
        cur.execute(SqlStmt, ( citationIDToMove, oldSourceID))

    # Change owner & type for media attached to old source so they follow the citationToMove
    # do media already attached to the citationToMove remain attached?
        SqlStmt = """
        UPDATE MediaLinkTable
          SET OwnerType = 4,
              OwnerID = ? 
          WHERE OwnerType = 3 AND OwnerID = ?
          """
        cur = conn.cursor()
        cur.execute(SqlStmt, ( citationIDToMove, oldSourceID))

    #  move the citation to the new source
        SqlStmt = """
        UPDATE CitationTable
          SET SourceID = ?
          WHERE CitationID = ?
          """
        cur = conn.cursor()
        cur.execute(SqlStmt, (newSourceID, citationIDToMove))

    # Get the SourceTable.Fields BLOB from the oldSource to extract its data
        SqlStmt = """
        SELECT Fields
          FROM SourceTable
          WHERE SourceID = ?
          """
        cur = conn.cursor()
        cur.execute(SqlStmt, (oldSourceID,))
        origSrcField = cur.fetchone()[0].decode()
        srcField = origSrcField

        # test for and fix old style "XML" no longer used in RM8
        xmlStart = "<Root>"
        rootLoc=srcField.find(xmlStart)
        if rootLoc != 0:
          srcField = srcField[rootLoc::]

        # read into DOM and parse for needed values (currently, only Date (of source creation))
        srcRoot = ET.fromstring(srcField)
        srcFields = srcRoot.find("Fields")
        srcFields.iterfind("Field")

        AccessDate  = None
        for item in srcFields:
            if item[0].text == "Date":
                AccessDate= item[1].text

        #print ("date=", AccessDate)


        # create XML text that represents the citation fields of the source template used by the newSource
        # Get the CitationTable.Fields BLOB for the new source (must be pre-existing and named "sample citation")
        SqlStmt = """
        SELECT CT.Fields
          FROM CitationTable CT
          JOIN SourceTable ST ON CT.SourceId = ST.SourceID
          WHERE CT.SourceID = ? AND CT.CitationName = "sample citation"
          """
        cur = conn.cursor()
        cur.execute(SqlStmt, (newSourceID,))
        newFieldTxt = cur.fetchone()[0].decode()

        newRoot = ET.fromstring(newFieldTxt)



        #print ("ET.tostring(newRoot)")
        #print (ET.tostring(newRoot))

        SqlStmt = """
        UPDATE CitationTable
          SET Fields = ?
          WHERE CitationID = ?
          """
        cur = conn.cursor()
        cur.execute(SqlStmt, (ET.tostring(newRoot), citationIDToMove,) )

        conn.commit()
        #print ("after commit")
        #end loop for citations

    # delete the old src
    SqlStmt = """
    DELETE from SourceTable
        WHERE SourceID = ?
        """
    cur = conn.cursor()
    cur.execute(SqlStmt, (oldSourceID,))
    print ("delete-", oldSourceID)
    conn.commit()

    return


# ================================================================
def getCitationsToMove ( conn, oldSourceID):
    # get citations for oldSourceID
    SqlStmt = """
    SELECT CitationID
      FROM CitationTable
      WHERE SourceID = ?
      """
    cur = conn.cursor()
    cur.execute(SqlStmt, (oldSourceID,))
    citationsIDs = cur.fetchall()

    citationIDsToMove= []

    # change the data structure from list of tuples to list of ints
    for each in citationsIDs:
        citationIDsToMove.append(each[0])

    return citationIDsToMove


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
def create_DBconnection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


# ================================================================
# Call the "main" function
if __name__ == '__main__':
    main()