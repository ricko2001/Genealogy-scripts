import os
import sys
import time
import sqlite3
from pathlib  import Path
from datetime import datetime
import configparser
import xml.etree.ElementTree as ET
import hashlib


##  Requirements: (see ReadMe.txt for details)
##   RootsMagic v7, v8 or v9 database file
##   RM-Python-config.ini  ( Configuration ini text file to set options and parameters)
##   Python v3.9 or greater

#   Transfer a citation from old source to new source -only if sources use same template
#   input citation name
#   confirm there is only 1 match to like input%
#   display existing source name
#   input new source name
#   confirm there is only 1 match to like input%
#   confirm old and new source both use same template
#   ask for confirm
#   change the owning source



# ===================================================DIV60==
def main():

  # Configuration
  IniFileName = "RM-Python-config.ini"

  # ini file must be in "current directory" and encoded as UTF-8 (no BOM).
  # see   https://docs.python.org/3/library/configparser.html
  IniFile = os.path.join(GetCurrentDirectory(), IniFileName)

  # Check that ini file is at expected path and that it is readable & valid.
  if not os.path.exists(IniFile):
      print("ERROR: The ini configuration file, " + IniFileName + " must be in the same directory as the .py or .exe file.\n\n" )
      input("Press the <Enter> key to exit...")
      return

  config = configparser.ConfigParser(empty_lines_in_values=False, interpolation=None)
  try:
    config.read(IniFile, 'UTF-8')
  except:
   print("ERROR: The " + IniFileName + " file contains a format error and cannot be parsed.\n\n" )
   input("Press the <Enter> key to exit...")
   return

  # Read database file path from ini file
  try:
    database_Path = config['FILE_PATHS']['DB_PATH']
  except:
    print('DB_PATH must be specified.')
    return

  if not os.path.exists(database_Path):
    print('Path for database not found: ' + database_Path)
    print('checked for: ' + os.path.abspath(database_Path))
    return

  dbConnection = create_DBconnection(database_Path)
  print("\nDatabase = " + os.path.abspath(database_Path) + "\n")

  # Deal with the citation as it is
  CitName = input("Enter the citation name for citation to change source:\n")

  SqlStmt = """
   SELECT COUNT(), st.TemplateID, ct.CitationID, ct.SourceID, st.Name
    FROM SourceTable AS st
    JOIN CitationTable AS ct ON ct.SourceID = st.SourceID
    WHERE ct.CitationName LIKE ( ? || '%' )
   """

  cur = dbConnection.cursor()
  cur.execute( SqlStmt, (CitName, ) )
  row = cur.fetchone()

  numberOfCitations = row[0]
  OldSourceTemplateID = row[1]
  CitationID = row[2]
  OldSourceID = row[3]
  OldSourceName= row[4]

  if (numberOfCitations > 1):
    print('Found more than 1 citation. Try again.')
    return 1
  if (numberOfCitations == 0):
    print('Citation not found. Try again.')
    return 1

  print( "\nThis citation is currently using source:\n" + OldSourceName)


  # Deal with the new source
  NewSrcName = input("\n\nEnter the name for the new source:\n")

  SqlStmt = """
   SELECT COUNT(), SourceID, TemplateID
     FROM SourceTable
     WHERE Name LIKE ( ? || '%' )
    """
  cur = dbConnection.cursor()
  cur.execute( SqlStmt, (NewSrcName, ) )
  row = cur.fetchone()

  numfound = row[0]
  NewSourceID = row[1]
  NewSourceTemplateID = row[2]

  if (numfound > 1):
    print('More than 1 source found. Try again.')
    return 1
  if (numfound == 0):
    print('Source not found. Try again.')
    return 1

  if (NewSourceID == OldSourceID):
    print('The citation is already using the specified new source. Try again.')
    return 1

  if (NewSourceTemplateID != OldSourceTemplateID):
    print('The new source must be based on the same SourceTemplate as the current source. Try again.')
    return 1


  # update the citation to use the new source
  SqlStmt = """
  UPDATE CitationTable
    SET  SourceID = ?
    WHERE CitationID = ?
   """
  cur = dbConnection.cursor()
  cur.execute( SqlStmt, (NewSourceID, CitationID ) )
  dbConnection.commit()

  # Confirm update was successful

  SqlStmt = """
   SELECT ct.CitationName, st.Name
    FROM SourceTable AS st
    JOIN CitationTable AS ct ON ct.SourceID = st.SourceID
    WHERE ct.CitationID = ?
   """

  cur = dbConnection.cursor()
  cur.execute( SqlStmt, (CitationID, ) )
  row = cur.fetchone()

  CitationName = row[0]
  SourceName = row[1]

  print( "\n\nConfirmation of change\nCitation:\n" + CitationName + "\n\nis now using source:\n" + SourceName + "\n\n")
  Pause()
  return 0


# ===================================================DIV60==
def Pause():
  input("Press the <Enter> key to exit...")
  return


# ===================================================DIV60==
def create_DBconnection(db_file_path):
    dbConnection = None
    try:
      dbConnection = sqlite3.connect(db_file_path)
    except Error as e:
        print(e)
        print("\n\n")
        print( "Cannot open the RM database file. \n")
        input("Press the <Enter> key to exit...")
        sys.exit()
    return dbConnection


# ===================================================DIV60==
def GetCurrentDirectory():
  # Determine if application is a script file or frozen exe and get its directory
  # see   https://pyinstaller.org/en/stable/runtime-information.html
  if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    application_path = os.path.dirname(sys.executable)
  else:
    application_path = os.path.dirname(__file__)
  return application_path


# ===================================================DIV60==
# Call the "main" function
if __name__ == '__main__':
    main()

# ===================================================DIV60==
