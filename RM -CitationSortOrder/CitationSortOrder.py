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

#   Re-order citations attached to a particular fact.


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


  # input the PersonID  RIN
  PersonID = input("Enter the RIN of the person who has the citations:\n")

  attacdhedTo = input("Are the citations attached to a Fact (f), a name (n) or the Person (p)?:\n")

# ===========================================DIV50==
  if attacdhedTo in "P p":

    SqlStmt = """
     SELECT clt.SortOrder, clt.LinkID, st.Name, ct.CitationName
       FROM CitationTable AS ct
       JOIN CitationLinkTable AS clt ON clt.CitationID = ct.CitationID
       JOIN SourceTable AS st ON ct.SourceID = st.SourceID
       WHERE clt.OwnerID = ?
         AND clt.OwnerType = 0
     ORDER BY clt.SortOrder ASC
    """
    cur = dbConnection.cursor()
    cur.execute( SqlStmt, (PersonID, ) )
    rows = cur.fetchall()

    if len(rows) == 0:
      PauseWithMessage("Either RIN does not exist or that person has no citations attached.")
      return 1

# ===========================================DIV50==
  elif attacdhedTo in "F f":

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

# ===========================================DIV50==
  elif attacdhedTo in "N n":

    SqlStmt = """
     SELECT COUNT(), nt.NameID
      FROM NameTable AS nt
      WHERE nt.OwnerID = ?
    """

    cur = dbConnection.cursor()
    cur.execute( SqlStmt, (PersonID, ) )
    rows = cur.fetchall()
    
    print (rows)
    numberOfNames = rows[0][0]

    if (numberOfNames == 0):
      PauseWithMessage('Either RIN does not exist or no names found. ')
      return 1
    elif (numberOfNames > 1):
      PauseWithMessage('Found more than 1 name. Try again.')
      return 1
    elif (numberOfNames == 1):
      PauseWithMessage('One name found.')

    NameID = rows[0][1]
    print (NameID)

    SqlStmt = """
     SELECT clt.SortOrder, clt.LinkID, st.Name, ct.CitationName
       FROM CitationTable AS ct
       JOIN CitationLinkTable AS clt ON clt.CitationID = ct.CitationID
       JOIN SourceTable AS st ON ct.SourceID = st.SourceID
       WHERE clt.OwnerID = ?
         AND clt.OwnerType = 7
     ORDER BY clt.SortOrder ASC
    """
    cur = dbConnection.cursor()
    cur.execute( SqlStmt, (NameID, ) )
    rows = cur.fetchall()

# ===========================================DIV50==
  else:
    PauseWithMessage("Cannot interpret response.")
    return 1


# ===========================================DIV50==
# Do the re-order

  rowDict = dict()
  # Create the origin 1 based dictionary
  # Use 1 based indexing for human users
  for i in range( 0, len(rows)):
    rowDict[i+1] =( (rows[i][1], (rows[i][2], rows[i][3])))

  print ("\n\n")

  # range limit when using 1 based indexing
  citNumberLimit = len(rowDict) +1

  print ( "\n" +
          "To re-order citations, at each prompt, enter one of:\n"+
          "*  the number of the citation that should go into this slot\n" +
          "*  nothing- to accept current slot as correct\n" +
          "*  s to accept current and following slots as correct\n")

  Done = False
  while not Done:
    # Print the list in current order
    for i in range( 1, citNumberLimit):
      print( i, rowDict[i][1] )

    for j in range( 1, citNumberLimit-1):
      response =  str(input( "\nWhat goes in slot # " + str(j) + " : "))
      if response == '': continue
      elif response in 'S s': break
      else :
        try:
          swapVal = int(response)
        except ValueError:
          print('Please enter an integer, blank or S or s')
          return 1
      rowDict[swapVal], rowDict[j] = rowDict[j], rowDict[swapVal]
      print ("\n\n")
      for i in range( 1, citNumberLimit):
        print( i, rowDict[i][1] )

    print ("\n\n")

    # Print order after a round of sorting
    for i in range( 1, citNumberLimit):
      print( i, rowDict[i][1] )

    respponse = input("\n\n" +
                      "Are you satisfied with the citation order shown above?\n" +
                      "Enter one of-\n" +
                      "*  Y/y to make the citation order change as shown above\n" +
                      "*  N/n to go back and do another round of re-ordering\n"+
                      "*  A/a to abort and not make any changes to the database \n")
    if respponse  in "Yy":
      Done = True
    elif respponse  in "Aa":
      PauseWithMessage("No changes made to database")
      return 1
    # assume No
    print ("\n\n")

  # End while Done


  # Now update the SortOrder column for the given Citation Links
  SqlStmt = """
  UPDATE  CitationLinkTable AS clt
    SET SortOrder = ?
    WHERE LinkID = ?
  """
  for i in range( 1, citNumberLimit):
    cur = dbConnection.cursor()
    cur.execute( SqlStmt, (i, rowDict[i][0]) )
    dbConnection.commit()


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
        PauseWithMessage( "\n\nCannot open the RM database file. \n")
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
