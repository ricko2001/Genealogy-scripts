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
##   RootsMagic v8 database file
##   RM-Python-config.ini  ( Configuration ini file to set options and parameters)
##   unifuzz64.dll
##   Python v3.10 or greater


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

    # test number of citatons found
    if len(citationsIDs) > 0 :
        # if 0, i.e. not used, leave it alone to make it stand out for needing further genealogical work

        # change the data structure from list of tuples to list of ints
        for each in citationsIDs:
            citationIDsToMove.append(each[0])
        # debug     print (citationIDsToMove)

    return citationIDsToMove


# ================================================================
def Convert ( conn, oldSourceID, newSourceID):

    citationIDsToMove= getCitationsToMove(conn,oldSourceID)

    for citationIDToMove in citationIDsToMove:

    # Copy the Standard and hidden fields from old src to citationToMove
        SqlStmt = """
        UPDATE CitationTable
          SET (CitationName, ActualText, Comments, UTCModDate) = (SELECT Name, ActualText, Comments, UTCModDate FROM SourceTable WHERE SourceID = ?)
          WHERE CitationID = ?
          """
        cur = conn.cursor()
        cur.execute(SqlStmt, (oldSourceID, citationIDToMove))

    # Change owner & type for relevant web tags so they follow the citationToMove
        SqlStmt = """
        UPDATE URLTable
          SET OwnerType = 4,
              OwnerID = ? 
          WHERE OwnerType = 3 AND OwnerID = ?
          """
        cur = conn.cursor()
        cur.execute(SqlStmt, ( citationIDToMove, oldSourceID))

    # Change owner & type for relevant media so they follow the citationToMove
        SqlStmt = """
        UPDATE MediaLinkTable
          SET OwnerType = 4,
              OwnerID = ? 
          WHERE OwnerType = 3 AND OwnerID = ?
          """
        cur = conn.cursor()
        cur.execute(SqlStmt, ( citationIDToMove, oldSourceID))

    #  move the existing citation to the new source
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

    #   Test for trailing junk (thought I saw a trailing period in some records ???
    #    xmlEnd = "</Root>"
    #    rootEndLoc=srcField.find(xmlEnd)
    #    srcLength = len(srcField)
    #    if rootEndLoc != srcLength -len(xmlEnd):
    #      srcField = srcField[0:rootEndLoc + len(xmlEnd):]

    # debug    if len(srcField) != len(origSrcField):
    # debug        print ("orig srcField")
    # debug        print (origSrcField)
    # debug        print ("fixed srcField")
    # debug        print (srcField)

        # read into DOM and parse for needed values (currently, only AccessDate)
        srcRoot = ET.fromstring(srcField)
        srcFields = srcRoot.find("Fields")
        srcFields.iterfind("Field")

        AccessDate  = None
        for item in srcFields:
            if item[0].text == "AccessDate":
                AccessDate= item[1].text

    # debug         print ("date=", AccessDate)

        # Parse the ActualText field for needed info (unlikely to be used for most runs)

        # get the text data
        SqlStmt = """
        SELECT ActualText
          FROM CitationTable
          WHERE CitationID = ?
          """
        cur = conn.cursor()
        cur.execute(SqlStmt, (citationIDToMove,))
        actualText = cur.fetchone()[0]

      # debug       print(actualText)
        print(actualText)
        LastFoundLoc = 0
        # SSDI   searchStrings = ['Name:\t', 'Social Security Number:\t', 'Birth Date:\t', 'Issue Year:\t' ]
        searchStrings = ['Name:\t', 'Birth Date:\t', 'SSN:\t' ]
        # , 'Father:\t'

        results=[]
        NL = "\n"
        for searchText in searchStrings:
            searchTextLoc = actualText.find(searchText, LastFoundLoc)
            endofLineLoc = actualText.find(NL, searchTextLoc)
            found = actualText[searchTextLoc + len(searchText) : endofLineLoc]
            found = found.replace("\r", "")
    # debug             print (searchTextLoc, endofLineLoc, len(searchText))
    # debug             print ( searchTextLoc + len(searchText), endofLineLoc -searchTextLoc)
    # debug             print (len(found))
    # debug             print (found)
            results.append(found)
            LastFoundLoc = endofLineLoc +1

    # debug         for each in results:
    # debug              print (each, "\n")

    # create an XML chunk that represents the citation fields of the source template used by the newSource
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

        # this shoud be improved. Order of data in list depends on order of search strings.
        newRoot = ET.fromstring(newFieldTxt)
        newFields = newRoot.find("Fields")
        newFields.findall("Field")
        for item in newFields:
            if item[0].text == "Name":
                item[1].text = results[0]
            if item[0].text == "BirthDate":
                item[1].text = results[1]
            if item[0].text == "SSN":
                item[1].text = results[2]
            if item[0].text == "AccessDate":
                item[1].text = AccessDate

    # debug         print ("ET.tostring(newRoot)")
    # debug         print (ET.tostring(newRoot))

        SqlStmt = """
        UPDATE CitationTable
          SET Fields = ?
          WHERE CitationID = ?
          """
        cur = conn.cursor()
        cur.execute(SqlStmt, (ET.tostring(newRoot), citationIDToMove,) )

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

    # specify which source is to get the converted citations
    # for SSDI NewSourceID = 5502
    NewSourceID = 5503

# List the sources to be lumped
#                 SqlStmt="""\
#             SELECT SourceID
#               FROM SourceTable
#               WHERE  Name LIKE 'SSDI%'
#                      AND TemplateID=10008
#             """

    SqlStmt="""\
SELECT SourceID
  FROM SourceTable
  WHERE  Name LIKE 'SSACI%'
         AND TemplateID=10033
"""
    SourcesToLump = GetListOfRows( conn, SqlStmt)
    print ("number of source to process: ", len(SourcesToLump))

    for oldSrc in SourcesToLump:
        print ("=====================================================")
        print (oldSrc)
        Convert (conn, oldSrc, NewSourceID)

    return 0


# ================================================================
# Call the "main" function
if __name__ == '__main__':
    main()