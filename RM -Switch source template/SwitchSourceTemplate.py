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

# ===================================================DIV60==
#  Global Variables
G_QT = "\""

# ===================================================DIV60==
def create_DBdbConnectionection( db_file):
    dbConnection = None
    try:
        dbConnection = sqlite3.connect(db_file)
    except Error as e:
        reportF.write(e)

    return dbConnection


# ===================================================DIV60==
def GetListOfRows ( dbConnection, SqlStmt):
    # SqlStmt should return a set of single values
    cur = dbConnection.cursor()
    cur.execute(SqlStmt)

    result = []
    for t in cur:
      for x in t:
        result.append(x)
    return result


# ===================================================DIV60==
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


# ===================================================DIV60==
def ConvertSource ( reportF, dbConnection, srcID, newTemplateID, fieldMapping):
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

  #print("source XML OLD START ============================")
  #ET.indent(srcRoot)
  #ET.dump(srcRoot)
  #print("source XML OLD END ==============================")

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

  #print("source XML NEW START ============================")
  #ET.indent(srcRoot)
  #ET.dump(srcRoot)
  #print("source XML NEW END ==============================")
  #sys.exit()

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
    reportF.write("   " + str(citationTuple[0]) + "    " + citationTuple[1][:70] + "\n")
    ConvertCitation( dbConnection, citationTuple[0], fieldMapping)
    #end loop for citations

  dbConnection.commit()
  return


# ===================================================DIV60==
def ConvertCitation( dbConnection, citationID, fieldMapping):
  # Get the CitationTable.Fields BLOB from the citation to extract its data
  SqlStmt_cit_r = """
  SELECT Fields
    FROM CitationTable
    WHERE citationID = ?
    """
  cur = dbConnection.cursor()
  cur.execute(SqlStmt_cit_r, (citationID,))
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

  #print("citation XML OLD START ============================")
  #ET.indent(srcRoot)
  #ET.dump(srcRoot)
  #print("citation XML OLD END ==============================")
  #sys.exit()

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

  #print("citation XML NEW START ============================")
  #ET.indent(srcRoot)
  #ET.dump(srcRoot)
  #print("citation XML NEW END ==============================")
  #sys.exit()

  newCitFileds = ET.tostring(citRoot, encoding="unicode")
  # Update the citation with new XML and new templateID
  SqlStmt_cit_w = """
  UPDATE CitationTable
    SET Fields = ?
    WHERE CitationID = ? 
    """
  dbConnection.execute(SqlStmt_cit_w, (newCitFileds, citationID) )
  return


# ===================================================DIV60==
def CheckForTrue( inputString):
  return inputString.lower()  in ['on', 'true', '1', 't', 'y', 'yes']


# ===================================================DIV60==
def CheckSourceTemplates(reportF, dbConnection, oldTemplateName, newTemplateName):
  if newTemplateName == oldTemplateName:
    reportF.write( "The old and new template names must be different." )
    return

  IDs = []
  IDs = GetSrcTempID( dbConnection, oldTemplateName )
  if len(IDs) == 0:
    reportF.write( "Could not find a SourceTemplate named: " + oldTemplateName )
    return
  if len(IDs) > 1:
    reportF.write( G_QT + oldTemplateName + G_QT + " is not a unique name. Edit the name in RM and try again" )
    return
  reportF.write( G_QT + oldTemplateName + G_QT + " checks out OK\n" )

 
  IDs = GetSrcTempID( dbConnection, newTemplateName )
  if len(IDs) == 0:
    reportF.write( "Could not find a SourceTemplate named: " + newTemplateName )
    return
  if len(IDs) > 1:
    reportF.write( G_QT + newTemplateName + G_QT + " is not a unique name. Edit the name in RM and try again" )
    return
  reportF.write( G_QT + newTemplateName + G_QT + " checks out OK\n" )

  return

# ===================================================DIV60==
def GetSrcTempID( dbConnection, TemplateName):
  SqlStmt = """
  SELECT TemplateID
   FROM SourceTemplateTable
   WHERE Name = ?
    """
  cur = dbConnection.execute(SqlStmt, (TemplateName,) )
  rows=[]  
  rows = cur.fetchall()
  return rows

# ===================================================DIV60==
def DumpSrcTemplateFields (reportF, dbConnection, oldTemplateID, newTemplateID):
  for ID in (oldTemplateID, newTemplateID):
    # dump fields in Templates
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
    reportF.write(templateName + "\n")
    for item in fieldItr:
        if CheckForTrue(item.find("CitationField").text):
          fieldLoc = "citation"
        else:
          fieldLoc ="source  "
        reportF.write(fieldLoc + "   " + item.find("Type").text + "      " + item.find("FieldName").text  + "\n")
    reportF.write("\n\n")

  #end for both templates
  return


# ===================================================DIV60==
def ListSourcesSelected(reportF, dbConnection, oldTemplateID, SourceNamesLike):
  SqlStmt = """
  SELECT  ST.SourceID, ST.Name
    FROM SourceTable ST
    JOIN SourceTemplateTable STT ON ST.TemplateID = STT.TemplateID
    WHERE ST.TemplateID = ? AND ST.Name LIKE ?
    """
  cur = dbConnection.cursor()
  cur.execute(SqlStmt, (oldTemplateID,SourceNamesLike))
  srcTuples = cur.fetchall()
  if len(srcTuples) == 0: 
    reportF.write( "No sources found with specified search criteria.\n")
    return
  for src in srcTuples:
    reportF.write (str(src[0]) + "    " + src[1] + "\n")
  return


# ===================================================DIV60==
def parseFieldMapping( text ):
# convert string to list of 2-tuple strings
 text = text.strip()
 list = text.split('\n')
 newList = []
 for each in list:
     newList.append( tuple(each.split()))
 return newList


# ===================================================DIV60==
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
  #  https://docs.python.org/3/library/configparser.html

  try:
    report_Path   = config['FILE_PATHS']['REPORT_FILE_PATH']
  except:
    print('REPORT_FILE_PATH must be specified.')
    return

  with open( report_Path,  mode='w', encoding='utf-8-sig') as reportF:
    try:
      database_Path = config['FILE_PATHS']['DB_PATH']
      RMNOCASE_Path = config['FILE_PATHS']['RMNOCASE_PATH']
    except:
      reportF.write('Both DB_PATH and RMNOCASE_PATH must be specified.')
      return
    
    if not os.path.exists(database_Path):
      reportF.write('Database path not found. Fix configuration file and try again.')
      return
    if not os.path.exists(RMNOCASE_Path):
      reportF.write('RMNOCASE path not found. Fix configuration file and try again.')
      return
  
  
    # Process the database
    with create_DBdbConnectionection(database_Path) as dbConnection:
      dbConnection.enable_load_extension(True)
      dbConnection.load_extension(RMNOCASE_Path)
    
      #act on options which are active
      if config['OPTIONS'].getboolean('CHECK_TEMPLATE_NAMES'):
        try:
          oldTemplateName  =  config['SOURCE_TEMPLATES']['TEMPLATE_OLD']
          newTemplateName  =  config['SOURCE_TEMPLATES']['TEMPLATE_NEW']
        except:
          reportF.write( "CHECK_TEMPLATE_NAMES option requires specification of both TEMPLATE_OLD and TEMPLATE_NEW.")
          return
        CheckSourceTemplates(reportF, dbConnection, oldTemplateName, newTemplateName)
        return


      if config['OPTIONS'].getboolean('LIST_SOURCES'):
        try:
          oldTemplateName  =  config['SOURCE_TEMPLATES']['TEMPLATE_OLD']
          srcNamesLike   =  config['SOURCES']['SOURCE_NAME_LIKE']
        except:
          reportF.write( "LIST_SOURCES option requires specification of both TEMPLATE_OLD and SOURCE_NAME_LIKE.")
          return
        oldTemplateID = GetSrcTempID(dbConnection, oldTemplateName)[0][0]
        ListSourcesSelected(reportF, dbConnection, oldTemplateID, srcNamesLike)
        return
  
      if config['OPTIONS'].getboolean('LIST_TEMPLATE_DETAILS'):
        try:
          oldTemplateName  =  config['SOURCE_TEMPLATES']['TEMPLATE_OLD']
          newTemplateName  =  config['SOURCE_TEMPLATES']['TEMPLATE_NEW']
          mapping          =  config['SOURCE_TEMPLATES']['MAPPING']
        except:
          reportF.write( "LIST_TEMPLATE_DETAILS option requires specification of TEMPLATE_OLD and TEMPLATE_NEW and MAPPING.")
          return

        oldTemplateID = GetSrcTempID(dbConnection, oldTemplateName)[0][0]
        newTemplateID = GetSrcTempID(dbConnection, newTemplateName)[0][0]
        DumpSrcTemplateFields( reportF, dbConnection, oldTemplateID, newTemplateID)
        reportF.write("\n\n The field mapping, as entered in the ini configuration file: \n")
        for each in mapping:
          reportF.write (each)
        reportF.write("\n\n")
        return
  
      if config['OPTIONS'].getboolean('MAKE_CHANGES'):
        try:
          oldTemplateName  =  config['SOURCE_TEMPLATES']['TEMPLATE_OLD']
          newTemplateName  =  config['SOURCE_TEMPLATES']['TEMPLATE_NEW']
          srcNamesLike     =  config['SOURCES']['SOURCE_NAME_LIKE']
          fieldMapping     =  config['SOURCE_TEMPLATES']['MAPPING']
        except:
          reportF.write( "MAKE_CHANGES option requires specification of TEMPLATE_OLD and TEMPLATE_NEW and SOURCE_NAME_LIKE and MAPPING.")
          return

      oldTemplateID = GetSrcTempID(dbConnection, oldTemplateName)[0][0]
      newTemplateID = GetSrcTempID(dbConnection, newTemplateName)[0][0]

      mapping = parseFieldMapping(fieldMapping)
      
      SqlStmt = """
      SELECT  ST.SourceID, ST.Name
        FROM SourceTable ST
        JOIN SourceTemplateTable STT ON ST.TemplateID = STT.TemplateID
        WHERE ST.TemplateID = ? AND ST.Name LIKE ?
        """
      cur = dbConnection.cursor()
      cur.execute(SqlStmt, (oldTemplateID,srcNamesLike))
      listSourceIDtuples = cur.fetchall()
#      print (type())
      
      for srcTuple in listSourceIDtuples:
        reportF.write ("=====================================================\n")
        reportF.write (str(srcTuple[0]) + "    " + srcTuple[1] + "\n")
        ConvertSource (reportF, dbConnection, srcTuple[0], newTemplateID, mapping)
    
  return 0


# ===================================================DIV60==
# Call the "main" function
if __name__ == '__main__':
    main()