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
##   tested with Python v3.10
## Using RM, determine-
##   * the set of sources to be lumped - here all starting with GSFG
##   * an existing source that the old sources will be made citations of
##   * an existing citation named "sample citation" in the new source. (Others will not interfere)
##  NOTE
##  Find a Grave citations changed over the years, see line 135
##  This script is simply run 4 times, once for each combination of search terms.
##  be sure to do the 2 runs with the citing" search commented out LAST

G_count = 0

# ================================================================
def main():
  global _G_count

  # Configuration file
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
      print('Database path not found. Fix configuration file and try again.')
      return

  # Process the database
  with create_DBconnection(database_Path) as conn:
    conn.enable_load_extension(True)
    conn.load_extension(RMNOCASE_Path)

  # Deal with index and the fact that the collation sequence is different here than in RM
  SqlStmt_IndexD= """
   DROP INDEX idxSourceName;
   """
  SqlStmt_IndexC= """
   CREATE INDEX idxSourceName ON SourceTable (Name COLLATE RMNOCASE) ;
   """
  cur = conn.cursor()
  cur.execute(SqlStmt_IndexD)
  cur = conn.cursor()
  cur.execute(SqlStmt_IndexC)

  # specify which source is to get the converted citations
  NewSourceID = 6276

  # List the sources to be lumped
  SqlStmt_FaG="""
  SELECT SourceID
    FROM SourceTable
    WHERE  Name LIKE 'GSFG %'
           AND TemplateID=0
  """

  SourcesToLump = GetListOfRows( conn, SqlStmt_FaG)

  print ("number of source to process: ", len(SourcesToLump))

  #iterate through each of the old sources, converting each one separately
  for oldSrc in SourcesToLump:
      print ("=====================================================")
      print (oldSrc)
      ConvertSource (conn, oldSrc, NewSourceID)

  print ("total not found",G_count)
  input( "\n\nPress Enter to continue...")
  return 0


# ================================================================
def ConvertSource ( conn, oldSourceID, newSourceID):

  global G_count

  citationIDsToMove= getCitationsToMove(conn,oldSourceID)
  if len(citationIDsToMove) == 0:  return
  print ( "Try to convert " +  str(len(citationIDsToMove)) + " citations")

  # For the given old source, iterate through its citations 
  # and convert each
  for citationIDToMove in citationIDsToMove:
    if ConvertCitation( conn, oldSourceID, newSourceID, citationIDToMove) == False:
       return

  # delete the old src
  SqlStmt = """
  DELETE from SourceTable
      WHERE SourceID = ?
  """
  RunSqlNoResult( conn, SqlStmt, tuple([oldSourceID, ]) )
  conn.commit()
  return

# ================================================================
def ConvertCitation( conn, oldSourceID, newSourceID, citationIDToMove ):
  global G_count
  # Get the SourceTable.Fields BLOB from the oldSource to extract its data
  SqlStmt = """
  SELECT Fields
    FROM SourceTable
    WHERE SourceID = ?
  """

  srcRoot = getFieldsXmlDataAsDOM ( conn, SqlStmt, oldSourceID )
  srcFields = srcRoot.find("Fields")
  FootnoteRaw = None
  for item in srcFields:
    if item[0].text == "Footnote":
      FootnoteRaw= item[1].text
  Footnote = FootnoteRaw.strip()


  # Parse the Footnote field for needed info
  # due to small changes in footnote format for FaG, need to do minimum of 4 runs to get max # of conversions
  # 1 using Memorial ID  (step 1 and 2 order not significant)
  # 2 using Memorial no.
  # 3 using Memorial ID and commenting out the citing search (when no burial place listed)
  # 4 using Memorial no. and commenting out the citing search (when no burial place listed)
  #                            (step 3 and 4 order not significant)

  searchStrings = [
    [': accessed '           , '),'     , 'DateCitation'],
    ['memorial page for '    , ' ('     , 'Name'], 
    [' ('                    , '–'      , 'DateBirth'],   #this is a long dash char
    ['Memorial ID '          , ','      , 'EntryNumber'], 
#    ['Memorial no. '         , ','      , 'EntryNumber'], 
    [', citing '             , ';'      , 'PlaceBurial']
    ]

  parse_results = ParseFootnote( Footnote, searchStrings)
  if parse_results == None: 
    return False


# Copy fields from old src record to the citationToMove
  SqlStmt = """
  UPDATE CitationTable
    SET (CitationName, ActualText, Comments, UTCModDate)
      = (SELECT Name, ActualText, Comments, UTCModDate FROM SourceTable WHERE SourceID = ?)
    WHERE CitationID = ?
  """
  RunSqlNoResult( conn, SqlStmt, tuple([oldSourceID, citationIDToMove]) )

  # Change owner & type columns for relevant web tags so they follow the citationToMove
  SqlStmt = """
  UPDATE URLTable
    SET OwnerType = 4,
        OwnerID = ? 
    WHERE OwnerType = 3 AND OwnerID = ?
  """
  RunSqlNoResult( conn, SqlStmt, tuple([citationIDToMove, oldSourceID]) )

  # Change owner & type for relevant media so they follow the citationToMove
  SqlStmt = """
  UPDATE MediaLinkTable
    SET OwnerType = 4,
        OwnerID = ? 
    WHERE OwnerType = 3 AND OwnerID = ?
  """
  RunSqlNoResult( conn, SqlStmt, tuple([citationIDToMove, oldSourceID]) )

  #  move the existing citation to the new source
  SqlStmt = """
  UPDATE CitationTable
    SET SourceID = ?
    WHERE CitationID = ?
  """
  RunSqlNoResult( conn, SqlStmt, tuple([newSourceID, citationIDToMove]) )

  # retrieve the XML DOM that has the citation fields of the citations as it exists
  SqlStmt = """
  SELECT CT.Fields
    FROM CitationTable CT
    WHERE CitationID = ?
  """
  citRoot = getFieldsXmlDataAsDOM ( conn, SqlStmt, citationIDToMove)
  citFields = citRoot.find("Fields")
  Page = None
  if citFields != None:
    citFields.iterfind("Field")
    for item in citFields:
      if item[0].text == "Page":
        Page = item[1].text
        break


  # retrieve an empty sample XML chunk that has the citation fields of the source template used by the newSource
  # this means the citation does not retain any old data not explicitly saved.
  # Get the CitationTable.Fields BLOB for the new source (must be pre-existing and named "sample citation")
  SqlStmt = """
  SELECT CT.Fields
    FROM CitationTable CT
    JOIN SourceTable ST ON CT.SourceId = ST.SourceID
    WHERE CT.SourceID = ? AND CT.CitationName = "sample citation"
  """
  newRoot = getFieldsXmlDataAsDOM ( conn, SqlStmt, newSourceID)
  newFields = newRoot.find("Fields")

  # now fill the XML with values
  for item in newFields:
      if item[0].text == "SrcCitation":
       item[1].text = Footnote
      if item[0].text == "CD":
       item[1].text = Page
      if item[0].text == "PlaceCemetery":
       if "PlaceCemetery" in parse_results:
         item[1].text = parse_results["PlaceCemetery"]
      for each in searchStrings:
          if item[0].text == each[2]:
            item[1].text = parse_results.get(each[2], None)

  # Update the citation Fields column with the new XML
  SqlStmt = """
  UPDATE CitationTable
    SET Fields = ?
    WHERE CitationID = ?
  """
  RunSqlNoResult( conn, SqlStmt, tuple([ET.tostring(newRoot), citationIDToMove]) )
  conn.commit()
  return True


# ================================================================
def ParseFootnote( Footnote, searchStrings ):
  global G_count
  # Try parsing the Footnote string. If it fails, don't make any changes to the old source.
  parse_results={}
  searchStart = 0
  for searchText in searchStrings:
    searchTextLocS = Footnote.find(searchText[0], searchStart)
    if searchTextLocS == -1:
      G_count += 1
      # parsing failed, don't change this old source
      # input(str(searchTextLocS) + "  " + str(searchText) + "\n" + Footnote +  "\n\nS Enter to continue...")
      return None
    searchTextLocE = Footnote.find(searchText[1], searchTextLocS)
    if searchTextLocE == -1:
      G_count += 1
      # parsing failed, don't change this old source
      # input(str(searchTextLocS) +"  " + str(searchTextLocE) + "  " + str(searchText) + "\n" + Footnote + "\n\nE Enter to continue...")
      return None
    searchStart = searchTextLocE
    # store away the parse result
    parse_results[searchText[2]] = Footnote[searchTextLocS + len(searchText[0]) : searchTextLocE]
   #end of for searchStrings

  # Deal with PlaceCemetery parsing
  # PlaceBurial has the cemetery name as the first part of the coma delimited location list
  if 'PlaceBurial' in parse_results:
    Place = parse_results['PlaceBurial']
    FirstPartPlace =  Place[ 0 : Place.find(",")]
    if "Cemetery" in FirstPartPlace \
        or "Friedhof" in FirstPartPlace \
        or "Memorial" in FirstPartPlace \
        or "Columbarium" in FirstPartPlace :
      parse_results["PlaceCemetery"] = FirstPartPlace
      parse_results["PlaceBurial"] = Place[Place.find(",") + 2 : ]

  return parse_results


# ================================================================
def RunSqlNoResult ( conn, SqlStmt, myTuple):
    cur = conn.cursor()
    cur.execute(SqlStmt, myTuple)


# ================================================================
def getFieldsXmlDataAsDOM ( conn, SqlStmt, rowID ):
  cur = conn.cursor()
  cur.execute(SqlStmt, (rowID,))
  XmlTxt = cur.fetchone()[0].decode()
  # print (XmlTxt)

  # test for and fix old style "XML" no longer used in RM8
  xmlStart = "<Root"
  rootLoc=XmlTxt.find(xmlStart)
  if rootLoc != 0:
    XmlTxt = XmlTxt[rootLoc::]
  # print (XmlTxt)

  # read into DOM and parse for needed values
  # only Page needed from old cit  XML data
  XmlRoot = ET.fromstring(XmlTxt)

  return XmlRoot


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
# Call the "main" function
if __name__ == '__main__':
    main()

# ================================================================
