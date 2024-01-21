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
##   RootsMagic v8 or v9 database file
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
    PauseWithMessage("ERROR: The ini configuration file, " + IniFileName + 
             " must be in the same directory as the .py or .exe file.\n\n" )
    return 1

  config = configparser.ConfigParser(empty_lines_in_values=False,
                                      interpolation=None)
  try:
    config.read(IniFile, 'UTF-8')
  except:
    PauseWithMessage("ERROR: The " + IniFileName + 
          " file contains a format error and cannot be parsed.\n\n" )
    return 1

  # Read database file path from ini file
  try:
    database_Path = config['FILE_PATHS']['DB_PATH']
  except:
    PauseWithMessage('DB_PATH must be specified.')
    return 1

  if not os.path.exists(database_Path):
    PauseWithMessage('Path for database not found: ' + database_Path +
           '\nchecked for: ' + os.path.abspath(database_Path))
    return 1

  dbConnection = create_DBconnection(database_Path)

  print("\nDatabase = " + os.path.abspath(database_Path) + "\n")





  # input the PersonID  RIN and type
  PersonID = input("Enter the RIN:\n")
  FactTypeID = input("Enter the FactTypeID:\n")

  SqlStmt = """
   SELECT COUNT(), et.EventID
    FROM EventTable AS et
    WHERE et.OwnerID = ?
      AND et.OwnerType = 0
      AND et.EventType = ?
   """

  cur = dbConnection.cursor()
  cur.execute( SqlStmt, (PersonID, FactTypeID) )
  row = cur.fetchone()

  numberOfEvents = row[0]
  EventID = row[1]


  if (numberOfEvents > 1):
    PauseWithMessage('Found more than 1 event. Try again.')
    return 1
  if (numberOfEvents == 0):
    PauseWithMessage('Event not found. Try again.')
    return 1


  SqlStmt = """
  SELECT clt.SortOrder, clt.LinkID, st.Name, ct.CitationName
    FROM CitationTable AS ct
    JOIN CitationLinkTable AS clt ON clt.CitationID = ct.CitationID
    JOIN SourceTable AS st ON ct.SourceID = st.SourceID
    WHERE clt.OwnerID = ?
      AND clt.OwnerType = 2
  ORDER BY clt.SortOrder ASC
    """
  cur = dbConnection.cursor()
  cur.execute( SqlStmt, (EventID, ) )
  rows = cur.fetchall()

  for row in rows:
    print (row[2] + "  ==  " + row[3])
  
  rowDict = dict()

  for i in range( 0, len(rows)):
    rowDict[i] =( (rows[i][1], (rows[i][2], rows[i][3])))



#  for i in range( 0, len(rowDict)):
#    print( rowDict[i] )

  print ("\n\n\n")

  for i in range( 0, len(rowDict)):
    print( i, rowDict[i][1] )

  Done = False
  while not Done:
    for j in range( 0, len(rowDict)-1):
      firstStr =  input( "position (or s)" + str(j) + " : ")
      if firstStr == '': firstStr = j
      if firstStr in 'Ss': break
      swapVal = int(firstStr)
      rowDict[swapVal], rowDict[j] = rowDict[j], rowDict[swapVal]
      for i in range( 0, len(rowDict)):
        print( i, rowDict[i][1] )

    print ("\n\n\n")

    for i in range( 0, len(rowDict)):
      print( i, rowDict[i][0],  rowDict[i][1] )
    
    if input("Finished ? Yy/Nn") in "Yy": Done = True


  # Close the connection so that it's not open when waiting at the Pause.
  dbConnection.close()
 
  PauseWithMessage()
  return 0


# ===================================================DIV60==
def PauseWithMessage(message = None):
  if (message != None): 
    print(message)
  input("\nPress the <Enter> key to exit...")
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
