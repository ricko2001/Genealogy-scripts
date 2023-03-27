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
##  Using RM, determine-
##   * the set of sources to be lumped - here all starting with C1940 and having a state abbreviation
##   * an existing source that the old sources will be made citations of
##   * an existing citation named "sample citation" in the new source. (Others will not interfere)


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

#   SourceID	Name
#   6317	CenFedUSdb 1940 California
#   6316	CenFedUSdb 1940 Colorado
#   6333	CenFedUSdb 1940 District of Columbia
#   6304	CenFedUSdb 1940 Hawaii
#   6322	CenFedUSdb 1940 Illinois
#   6323	CenFedUSdb 1940 Indiana
#   6325	CenFedUSdb 1940 Louisiana
#   6321	CenFedUSdb 1940 Michigan
#   6318	CenFedUSdb 1940 Minnesota
#   6324	CenFedUSdb 1940 New Jersey
#   6251	CenFedUSdb 1940 New York
#   6332	CenFedUSdb 1940 Ohio
#   6320	CenFedUSdb 1940 Pennsylvania
#   6315	CenFedUSdb 1940 Texas
#   6319	CenFedUSdb 1940 Virginia



# The list of states to lump in this run
#   new SourceID, state abbrev
  stateList = [
    ( 6317, "CA"),
    ( 6316, "CO"),
    ( 6333, "DC"),
    ( 6304, "HI"),
    ( 6322, "IL"),
    ( 6323, "IN"),
    ( 6325, "LA"),
    ( 6321, "MI"),
    ( 6318, "MN"),
    ( 6324, "NJ"),
    ( 6251, "NY"),
    ( 6332, "OH"),
    ( 6320, "PA"),
    ( 6315, "TX"),
    ( 6319, "VA") ]

  for state in stateList:

    # specify the single source that is to get the new citations
    NewSourceID = state[0]
    StateAbbrev=  state[1]
   
    # List the sources which will be converted to citations of the 'new' source
    Part1 = " SELECT SourceID FROM SourceTable WHERE  Name LIKE 'C1940 "
    Part2 = " %' AND TemplateID=10026"
    # NOTE this sql contains the old SourceTemplateID and depends on format of source names
   
    SqlStmt_OldCensus = Part1 + StateAbbrev + Part2
   
    SourcesToLump = GetListOfRows( conn, SqlStmt_OldCensus)
   
    print ("\n\n\nnumber of source to process: ", len(SourcesToLump))
   
    #iterate through each of the old sources, converting each one separately
    for oldSrc in SourcesToLump:
        print ("old SourceID= " + str(oldSrc) )
        ConvertSource (conn, oldSrc, NewSourceID)
        print ("=====================================================")

  print ("total not found",G_count)
  input( "\n\nPress Enter to continue...")
  return 0


# ================================================================
def ConvertSource ( conn, oldSourceID, newSourceID):

  global G_count

  # For the given old source, count its citations 
  # Code as written only handles sources that have one citation and
  # no info in that citation is preserved.
  # Must make code changes to deal with #cits !=1 or preserve info in the citation.

  # print source name for confirmation
  SqlStmt = """
  SELECT Name
    FROM SourceTable
    WHERE SourceID = ?
  """
  cur = conn.cursor()
  cur.execute(SqlStmt, (newSourceID,))
  print ("source to get cited......" + cur.fetchone()[0]  )

  citationIDsToMove= getCitationsToMove(conn,oldSourceID)
  # print ( "Try to convert " +  str(len(citationIDsToMove)) + " citations")
  if len(citationIDsToMove) != 1:  return

  for citationIDToMove in citationIDsToMove:
    if ConvertCitation( conn, oldSourceID, newSourceID, citationIDToMove) == False:
       return

  # delete the old src (all of its citations have been moved to new source)
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

# Copy fields from old src record to the citationToMove
  SqlStmt = """
  UPDATE CitationTable
    SET (CitationName, ActualText, Comments, UTCModDate)
      = (SELECT Name, ActualText, Comments, UTCModDate FROM SourceTable WHERE SourceID = ?)
    WHERE CitationID = ?
  """
  RunSqlNoResult( conn, SqlStmt, tuple([oldSourceID, citationIDToMove]) )

  # Change owner & type columns for relevant web tags so they follow the citationToMove
  # takes all webtags linked to old source and add them to the citation in process
  # SO ONLY FIRST CITATION MOVED WILL GET THE OLD SOURCE WEB TAGS.

  SqlStmt = """
  UPDATE URLTable
    SET OwnerType = 4,
        OwnerID = ? 
    WHERE OwnerType = 3 AND OwnerID = ?
  """
  RunSqlNoResult( conn, SqlStmt, tuple([citationIDToMove, oldSourceID]) )

  # Change owner & type for relevant media so they follow the citationToMove
  # SO ONLY FIRST CITATION MOVED WILL GET THE OLD SOURCE MEDIA LINKS.

  SqlStmt = """
  UPDATE MediaLinkTable
    SET OwnerType = 4,
        OwnerID = ? 
    WHERE OwnerType = 3 AND OwnerID = ?
  """
  RunSqlNoResult( conn, SqlStmt, tuple([citationIDToMove, oldSourceID]) )

  #  move the existing citation to the new (existing) source
  SqlStmt = """
  UPDATE CitationTable
    SET SourceID = ?
    WHERE CitationID = ?
  """
  RunSqlNoResult( conn, SqlStmt, tuple([newSourceID, citationIDToMove]) )



  # Get the SourceTable.Fields BLOB from the oldSource to extract its data
  SqlStmt = """
  SELECT Fields
    FROM SourceTable
    WHERE SourceID = ?
  """

  oldSrcFields = {}
  srcRoot = getFieldsXmlDataAsDOM ( conn, SqlStmt, oldSourceID )
  srcFields = srcRoot.find("Fields")
  FootnoteRaw = None
  for item in srcFields:
    if   item[0].text == "Household": oldSrcFields["Household"] = item[1].text
    elif item[0].text == "BirthDateHead": oldSrcFields["BirthDateHead"] = item[1].text
    elif item[0].text == "Place": oldSrcFields["Place"] = item[1].text
    elif item[0].text == "Location": oldSrcFields["Location"] = item[1].text
    elif item[0].text == "County": oldSrcFields["County"] = item[1].text
    elif item[0].text == "State": oldSrcFields["State"] = item[1].text
    elif item[0].text == "HouseNumber": oldSrcFields["HouseNumber"] = item[1].text
    elif item[0].text == "Street": oldSrcFields["Street"] = item[1].text
    elif item[0].text == "FilmNumber": oldSrcFields["FilmNumber"] = item[1].text
    elif item[0].text == "DateSheet": oldSrcFields["DateSheet"] = item[1].text
    elif item[0].text == "Page": oldSrcFields["Page"] = item[1].text
    elif item[0].text == "EnumerationDistrict": oldSrcFields["EnumerationDistrict"] = item[1].text
    elif item[0].text == "Dwelling": oldSrcFields["Dwelling"] = item[1].text
    elif item[0].text == "Family": oldSrcFields["Family"] = item[1].text
    elif item[0].text == "FS_ark": oldSrcFields["FS_ark"] = item[1].text
    elif item[0].text == "CD": oldSrcFields["CD"] = item[1].text
    elif item[0].text == "CitationDateUpdated": oldSrcFields["CitationDateUpdated"] = item[1].text
    elif item[0].text == "ANC_RID": oldSrcFields["ANC_RID"] = item[1].text

  print (oldSrcFields)


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
  if newRoot == None:
    print( "cannot find the 'sample citation'")
    return False
  newFields = newRoot.find("Fields")

  # now fill the XML with values
  for item in newFields:
    if   item[0].text == "Household":           item[1].text = oldSrcFields["Household"]
    elif item[0].text == "DateHeadBirth":       item[1].text = oldSrcFields["BirthDateHead"]
    elif item[0].text == "DateSheet":           item[1].text = oldSrcFields["DateSheet"]
    elif item[0].text == "PlaceFull":           item[1].text = oldSrcFields["Place"]
    elif item[0].text == "PlaceLocality":       item[1].text = oldSrcFields["Location"]
    elif item[0].text == "PlaceCounty":         item[1].text = oldSrcFields["County"]
    elif item[0].text == "PlaceStreet":         item[1].text = oldSrcFields["Street"]
    elif item[0].text == "PlaceHouseNumber":    item[1].text = oldSrcFields["HouseNumber"]
    elif item[0].text == "EnumerationDistrict": item[1].text = oldSrcFields["EnumerationDistrict"]
    elif item[0].text == "SheetLineNumber":     item[1].text = oldSrcFields["Page"]
    # elif item[0].text == "DwellingSN":          item[1].text = oldSrcFields["Dwelling"]
    elif item[0].text == "DwellingSN":          item[1].text = oldSrcFields["Family"]
    elif item[0].text == "FilmRollNumber":      item[1].text = oldSrcFields["FilmNumber"]
    elif item[0].text == "ANC_SRC_ID":          item[1].text = oldSrcFields["ANC_RID"]
    elif item[0].text == "FS_SRC_ID":           item[1].text = oldSrcFields["FS_ark"]
    elif item[0].text == "DateCitation":        item[1].text = oldSrcFields["CitationDateUpdated"]
  #  elif item[0].text == "CD":                  item[1].text = oldSrcFields["CD"]

#  NOTE field name DwellingSN should be changed to HouseholdSN. 
#  NOTE  for now
#  NOTE  1950 census-   field DwellingSN is filled by Dwelling in old template
#  NOTE  1940 census-   field DwellingSN is filled by Family in old template which was called Household in census

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
def RunSqlNoResult ( conn, SqlStmt, myTuple):
    cur = conn.cursor()
    cur.execute(SqlStmt, myTuple)


# ================================================================
def getFieldsXmlDataAsDOM ( conn, SqlStmt, rowID ):
  cur = conn.cursor()
  cur.execute(SqlStmt, (rowID,))
  XmlTxt_raw = cur.fetchone()
  if XmlTxt_raw == None: return None
  XmlTxt=XmlTxt_raw[0].decode()

  # test for and fix old style "XML" no longer used in RM8
  xmlStart = "<Root"
  rootLoc=XmlTxt.find(xmlStart)
  if rootLoc != 0:
    XmlTxt = XmlTxt[rootLoc::]

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
