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
##  SQLite tool to determine record numbers for SourceTemplates


# ================================================================
def create_DBdbConnectionection(db_file):
    dbConnection = None
    try:
        dbConnection = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return dbConnection


# ================================================================
def GetListOfRows ( dbConnection, SqlStmt):
    # SqlStmt should return a set of single values
    cur = dbConnection.cursor()
    cur.execute(SqlStmt)

    result = []
    for t in cur:
      for x in t:
        result.append(x)
    return result


# ================================================================
def getCitationsForSrc ( dbConnection, oldSourceID):
    # get citations for oldSourceID
    SqlStmt = """
    SELECT CitationID, CitationName
      FROM CitationTable
      WHERE SourceID = ?
      """
    cur = dbConnection.cursor()
    cur.execute(SqlStmt, (oldSourceID,))
    return cur.fetchall()

    #citationIDsForSrc= []
    #
    ## change the data structure from list of tuples to list of ints
    #for each in citationsIDs:
    #    citationIDsForSrc.append(each[0])
    #
    #return sjucitationIDsForSrc


# ================================================================
def Convert ( dbConnection, srcID, newTemplateID, fieldMapping):
  # edit the src XML

  #get the  existing surce XML

  # Get the SourceTable.Fields BLOB from the srcID to extract its data
  SqlStmt_src_r = """
  SELECT Fields
    FROM SourceTable
    WHERE SourceID = ?
    """
  cur = dbConnection.cursor()
  cur.execute(SqlStmt_src_r, (srcID,))
  srcField = cur.fetchone()[0].decode()

  # test for and fix old style "XML" no longer used in RM8
  xmlStart = "<Root"
  rootLoc=srcField.find(xmlStart)
  if rootLoc != 0:
      srcField = srcField[rootLoc::]

  # read into DOM and parse for needed values
  srcRoot = ET.fromstring(srcField)
  newField = srcRoot.find(".//Fields")
  if newField == None: ET.SubElement( srcRoot, "Fields")

#  print("source XML OLD START ============================")
#  ET.indent(srcRoot)
#  ET.dump(srcRoot)
#  print("source XML OLD END ==============================")

  # change fields in source as per mapping:
  for eachMap in fieldMapping: 
    if eachMap[0] == "y": continue

    if eachMap[1] == "NULL":
      # create a name and value pair.
      newPair = ET.SubElement( newField, "Field")
      ET.SubElement( newPair, "Name").text = eachMap[2]
      ET.SubElement( newPair, "Value")
      continue

    for eachField in srcRoot.findall('.//Field'):
      if eachField.find('Name').text == eachMap[1]:
        if eachMap[2] == "NULL":
          # delete the unused field
          srcRoot.find(".//Fields").remove(eachField)
          break
        eachField.find('Name').text = eachMap[2]
        break
      # end of for eachField loop
    #end of for eachMap loop

#  print("source XML NEW START ============================")
#  ET.indent(srcRoot)
#  ET.dump(srcRoot)
#  print("source XML NEW END ==============================")
#  sys.exit()

  # Update the source with new XML and new templateID
  newSrcFields = ET.tostring(srcRoot, encoding="unicode")
  SqlStmt_src_w = """
  UPDATE SourceTable
    SET Fields = ?, TemplateID = ?
    WHERE SourceID = ?
    """
  dbConnection.execute(SqlStmt_src_w, (newSrcFields, newTemplateID, srcID) )

  #deal with this source's citations
  for citationTuple in getCitationsForSrc(dbConnection, srcID):
    print("   ", citationTuple[0],"    ", citationTuple[1][:70])
    # Get the CitationTable.Fields BLOB from the citation to extract its data
    SqlStmt_cit_r = """
    SELECT Fields
      FROM CitationTable
      WHERE citationID = ?
      """
    cur = dbConnection.cursor()
    cur.execute(SqlStmt_cit_r, (citationTuple[0],))
    citFields = cur.fetchone()[0].decode()

    # test for and fix old style "XML" no longer used in RM8
    xmlStart = "<Root"
    rootLoc=citFields.find(xmlStart)
    if rootLoc != 0:
      citFields = citFields[rootLoc::]

    # read into DOM and parse for needed values
    citRoot = ET.fromstring(citFields)
    newField = citRoot.find(".//Fields")
    if newField == None: ET.SubElement( citRoot, "Fields")

#    print("citation XML OLD START ============================")
#    ET.indent(srcRoot)
#    ET.dump(srcRoot)
#    print("citation XML OLD END ==============================")
#    sys.exit()

    # change fields in citation as per mapping:
    for eachMap in fieldMapping:
      if eachMap[0] == "y": continue

      if eachMap[1] == "NULL":
        # create a name and value pair.
        newField = citRoot.find(".//Fields")
        newPair = ET.SubElement( newField, "Field")
        ET.SubElement( newPair, "Name").text = eachMap[2]
        ET.SubElement( newPair, "Value")
        continue

      for eachField in citRoot.findall('.//Field'):
        if eachField.find('Name').text == eachMap[1]:
          if eachMap[2] == "NULL":
            # delete the unused field
            srcRoot.find(".//Fields").remove(eachField)
            break
          eachField.find('Name').text = eachMap[2]
          break
      # end of for eachField loop
    #end of for eachMap loop

#    print("citation XML NEW START ============================")
#    ET.indent(srcRoot)
#    ET.dump(srcRoot)
#    print("citation XML NEW END ==============================")
#    sys.exit()

    newCitFileds = ET.tostring(citRoot, encoding="unicode")
    # Update the citation with new XML and new templateID
    SqlStmt_cit_w = """
    UPDATE CitationTable
      SET Fields = ?
      WHERE CitationID = ? 
      """
    dbConnection.execute(SqlStmt_cit_w, (newCitFileds, citationTuple[0]) )

    #end loop for citations

  dbConnection.commit()

  return


# ================================================================
def CheckForTrue( inputString):
  return inputString.lower()  in ['on', 'true', '1', 't', 'y', 'yes']


# ================================================================
def DumpSrcTemplateFields ( dbConnection, oldTemplateID, newTemplateID):
  for ID in (oldTemplateID, newTemplateID):
    # dump fields in Template to stdout
    SqlStmt = """
    SELECT FieldDefs, Name
      FROM SourceTemplateTable
      WHERE TemplateID = ?
      """
    cur = dbConnection.cursor()
    cur.execute(SqlStmt, (ID,))
    #text = cur.fetchone()[0].decode()
    textTuple = cur.fetchone()
    templateName= textTuple[1]
    newRoot = ET.fromstring(textTuple[0].decode())

    fieldItr = newRoot.findall(".Fields/Field")
    print(templateName, "\n")
    for item in fieldItr:
        if CheckForTrue(item.find("CitationField").text):
          fieldLoc ="citation"
        else:
          fieldLoc ="source  "
        print(fieldLoc, "      ", item.find("FieldName").text)
    print("\n\n")

  #end for both templates
  return


# ================================================================
def ListSourcesSelected( dbConnection, oldTemplateID, SourceNamesLike):
  SqlStmt = """
  SELECT  ST.SourceID, ST.Name
    FROM SourceTable ST
    JOIN SourceTemplateTable STT ON ST.TemplateID = STT.TemplateID
    WHERE ST.TemplateID = ? AND ST.Name LIKE ?
    """
  cur = dbConnection.cursor()
  cur.execute(SqlStmt, (oldTemplateID,SourceNamesLike))
  srcTuples = cur.fetchall()
  for src in srcTuples:
    print (src[0], "    ", src[1])
  return


# ================================================================
def parseFieldMapping( text ):
# convert string to list of 2-tuple strings
 text = text.strip()
 list = text.split('\n')
 newList = []
 for each in list:
     newList.append( tuple(each.split()))
 return newList


# ================================================================
def main():
  # Configuration
  IniFile="RM-Python-config.ini"
  # ini file must be in "current directory" and encoded as UTF-8 if non-ASCII chars present (no BOM)
  # Can specify an ini file location instead...
  #IniFile=r"C:/Users/rotter/Development/Genealogy/Genealogy-scripts/RM -Switch source template" + r"/" + IniFile
  #print (IniFile)
  if not os.path.exists(IniFile):
      print("ERROR: The ini configuration file, " + IniFile + " must be in the current directory." )
      return

  config = configparser.ConfigParser(interpolation=None)
  config.read(IniFile, 'UTF-8')

  # Read file paths from ini file
  database_Path = config['File Paths']['DB_PATH']
  RMNOCASE_Path = config['File Paths']['RMNOCASE_PATH']
  
  if not os.path.exists(database_Path):
      print('Database path not found. Fix configuration file and try again.')
      return

  # Process the database
  with create_DBdbConnectionection(database_Path) as dbConnection:
    dbConnection.enable_load_extension(True)
    dbConnection.load_extension(RMNOCASE_Path)
  
    oldTemplateID =  config['Source_Templates']['old']
    newTemplateID =  config['Source_Templates']['new']
    srcNamesLike  =  config['Source_Templates']['SourceNamesLike']
    fieldMapping  =  config['Source_Templates']['mapping']

    mapping = parseFieldMapping(fieldMapping)

    #check if special options are active
    if CheckForTrue( config['Source_Templates']['List_Fields']):
      DumpSrcTemplateFields( dbConnection, oldTemplateID, newTemplateID)
      print("\n")
      for each in mapping:
        print (each)
      print("\n\n")
      return

    if CheckForTrue( config['Source_Templates']['List_Sources']):
      ListSourcesSelected( dbConnection, oldTemplateID, srcNamesLike)
      return
  
  SqlStmt = """
  SELECT  ST.SourceID, ST.Name
    FROM SourceTable ST
    JOIN SourceTemplateTable STT ON ST.TemplateID = STT.TemplateID
    WHERE ST.TemplateID = ? AND ST.Name LIKE ?
    """
  cur = dbConnection.cursor()
  cur.execute(SqlStmt, (oldTemplateID,srcNamesLike))
  listSourceIDtuples = cur.fetchall()
  
  for srcTuple in listSourceIDtuples:
    print ("=====================================================")
    print (srcTuple[0], "    ", srcTuple[1])
    Convert (dbConnection, srcTuple[0], newTemplateID, mapping)

  return 0


# ================================================================
# Call the "main" function
if __name__ == '__main__':
    main()