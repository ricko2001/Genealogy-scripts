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

  try:
    # Configuration
    IniFileName = "RM-Python-config.ini"

    # ini file must be in "current directory" and encoded as UTF-8 (no BOM).
    # see   https://docs.python.org/3/library/configparser.html
    IniFile = os.path.join(GetCurrentDirectory(), IniFileName)

    # Check that ini file is at expected path and that it is readable & valid.
    if not os.path.exists(IniFile):
      raise Exception("ERROR: The ini configuration file, " + IniFileName +
               " must be in the same directory as the .py or .exe file.\n\n" )

    config = configparser.ConfigParser(empty_lines_in_values=False,
                                        interpolation=None)
    try:
      config.read(IniFile, 'UTF-8')
    except:
      raise Exception("ERROR: The " + IniFileName +
            " file contains a format error and cannot be parsed.\n\n" )

    # Read database file path from ini file
    try:
      database_Path = config['FILE_PATHS']['DB_PATH']
    except:
      raise Exception('DB_PATH must be specified.')

    if not os.path.exists(database_Path):
      raise Exception('Path for database not found: ' + database_Path +
             '\nchecked for: ' + os.path.abspath(database_Path))

    dbConnection = create_DBconnection(database_Path)

    print("\nDatabase = " + os.path.abspath(database_Path) + "\n")

    PersonID = GetRINFromUser( dbConnection )

    attacdhedTo = input("\nAre the citations attached to a Fact (f), a name (n) or the Person (p)?:\n")

    if attacdhedTo == "":
      raise Exception("Cannot interpret response.")

    if attacdhedTo in "P p":
      rows = AttachedToPerson( PersonID, dbConnection)

    elif attacdhedTo in "F f":
      rows = AttachedToFact( PersonID, dbConnection)

    elif attacdhedTo in "N n":
      rows = AttachedToName( PersonID, dbConnection)

    else:
      raise Exception("Cannot interpret response.")

    rowDict = OrderTheLocalCitations( rows )
    UpdateDatabase( rowDict, dbConnection )

    # Close the connection so that it's not open when waiting at the Pause.
    dbConnection.close()

  except Exception as RunError:
    print( str(RunError))

  PauseWithMessage()
  return 0

# ===========================================DIV50==
def GetRINFromUser( dbConnection ):
  # input the PersonID  RIN
  PersonID = input("Enter the RIN of the person who has the citations:\n")

  SqlStmt = """
   SELECT nt.Prefix, nt.Given, nt.Surname, nt.Suffix
    FROM PersonTable AS pt
    INNER JOIN NameTable AS nt ON nt.OwnerID=pt.PersonID
    WHERE nt.OwnerID = ?
      AND nt.IsPrimary = 1
   """

  cur = dbConnection.cursor()
  cur.execute( SqlStmt, (PersonID, ) )
  rows = cur.fetchall()

  if len(rows) == 0:
    raise Exception("That RIN does not exist.")
  elif len(rows) > 1:
    raise Exception("PersonID index not primary key. Not unique.")
  elif len(rows) ==1:
   print( "RIN= " + PersonID + "  points to:\n" +
          rows[0][0], rows[0][1], rows[0][2], rows[0][3], )

  return PersonID

# ===========================================DIV50==
def AttachedToName( PersonID, dbConnection):

  # Select nameID's that have more than 1 citation attached
  SqlStmt = """
   SELECT  nt.NameID, nt.Prefix, nt.Given, nt.Surname, nt.Suffix
    FROM NameTable AS nt
        INNER JOIN CitationLinkTable AS clt ON clt.OwnerID = nt.NameID AND clt.OwnerType = 7
        WHERE  nt.OwnerID = ?
        GROUP BY nt.NameID
        HAVING COUNT() > 1
  """
  cur = dbConnection.cursor()
  cur.execute( SqlStmt, (PersonID, ) )
  rows = cur.fetchall()

  numberOfNames = len(rows)
  if (numberOfNames == 0):
    raise Exception('Either RIN does not exist or no names found. ')
  elif (numberOfNames > 1):
#    raise Exception('Found more than 1 name. Try again.')
    nameID = SelectNameFromList(rows)
  elif (numberOfNames == 1):
    PauseWithMessage('One name found.')
    #continue ...


  NameID = rows[0][0]
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

  return rows


# ===========================================DIV50==
def SelectNameFromList( rows ):

  # clt.SortOrder, clt.LinkID, st.Name, ct.CitationName

  for i in range( 1, len(rows)+1):
    print (i, rows[i-1][1], rows[i-1][2], rows[i-1][3], rows[i-1][4] )

  try:
    citNumber = int(input("Which name's citations shall be ordered? ") )
  except ValueError as e:
    raise Exception('Type a number')

  nameID = rows[citNumber -1][0]

  return nameID


# ===========================================DIV50==
def SelectEventFromList( rows ):

  # et.EventID, ftt.Name, et.Date, et.Details

  for i in range( 1, len(rows)+1):
    print (i, rows[i-1][1], rows[i-1][2], rows[i-1][3] )

  try:
    citNumber = int(input("Which event's citations shall be ordered? ") )
  except ValueError as e:
    raise Exception('Type a number')

  eventID = rows[citNumber -1][0]

  return eventID


# ===========================================DIV50==
def AttachedToFact( PersonID, dbConnection):

  EventID = None

  FactTypeID = input("Enter the FactTypeID or\n" +
              "blank for full list of attached Facts with more than one citation\n")

  if FactTypeID == '':
  # Select all EventID's that have more than 1 citation attached

    SqlStmt = """
     SELECT et.EventID, ftt.Name, et.Date, et.Details
      FROM EventTable AS et
      INNER JOIN FactTypeTable AS ftt ON ftt.FactTypeID = et.EventType
      INNER JOIN CitationLinkTable AS clt ON clt.OwnerID = et.EventID AND clt.OwnerType = 2
      WHERE et.OwnerID = ?
        AND et.OwnerType = 0
        AND clt.OwnerType = 2
      GROUP BY et.EventID
      HAVING COUNT() > 1
     """

    cur = dbConnection.cursor()
    cur.execute( SqlStmt, (PersonID, ) )
    rows = cur.fetchall()

  else:
    # Select EventID's of speciified type that have more than 1 citation attached

    SqlStmt = """
     SELECT et.EventID, ftt.Name, et.Date, et.Details
      FROM EventTable AS et
      INNER JOIN FactTypeTable AS ftt ON ftt.FactTypeID = et.EventType
      INNER JOIN CitationLinkTable AS clt ON clt.OwnerID = et.EventID AND clt.OwnerType = 2
      WHERE et.OwnerID = ?
        AND et.OwnerType = 0
        AND et.EventType = ?
      GROUP BY et.EventID
      HAVING COUNT() > 1
     """

    cur = dbConnection.cursor()
    cur.execute( SqlStmt, (PersonID, FactTypeID) )
    rows = cur.fetchall()


  numberOfEvents = len(rows)
  print(numberOfEvents)
  if (numberOfEvents > 1):
    EventID = SelectEventFromList(rows)
  elif (numberOfEvents == 0):
    raise Exception('No events with more than one citation found. Try again.')
  elif (numberOfEvents == 1):
    EventID = rows[0][0]
    print("Found one event with more than one citation.\n" +
          rows[0][1], rows[0][2], rows[0][3] )
    


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

  return rows

# ===========================================DIV50==
def AttachedToPerson( PersonID, dbConnection):

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
    raise Exception( "Person has no citations attached")
  if len(rows) == 1:
    raise Exception( "Person has only one citation attached")
  return rows


# ===========================================DIV50==
def UpdateDatabase( rowDict, dbConnection ):

  # range limit when using 1 based indexing
  citNumberLimit = len(rowDict) +1

  # Now update the SortOrder column for the given Citation Links
  SqlStmt = """
  UPDATE  CitationLinkTable AS clt
    SET SortOrder = ?
    WHERE LinkID = ?
  """

  for i in range( 1, len(rowDict)+1):
    cur = dbConnection.cursor()
    cur.execute( SqlStmt, (i, rowDict[i][0]) )
    dbConnection.commit()

  return

# ===========================================DIV50==
def OrderTheLocalCitations( rows):
  rowDict = dict()
  # Create the origin 1 based dictionary
  # Use 1 based indexing for human users
  for i in range( 0, len(rows)):
    rowDict[i+1] =( (rows[i][1], (rows[i][2], rows[i][3])))

  print ("\n\n")

  # range limit when using 1 based indexing
  citNumberLimit = len(rowDict) +1

  print ( "\n" +
          "------------------------------------------------------\n" +
          "To re-order citations, at each prompt, enter one of:\n"+
          "*  the number of the citation that should go into this slot\n" +
          "*  nothing- to accept current slot as correct\n" +
          "*  s to accept current and following slots as correct\n" +
          "*  a to abort and make no chnages\n" +
          "------------------------------------------------------\n" )

  Done = False
  while not Done:
    # Print the list in current order
    for i in range( 1, citNumberLimit):
      print( i, rowDict[i][1] )

    for j in range( 1, citNumberLimit-1):
      response =  str(input( "\nWhat goes in slot # " + str(j) + " : "))
      if response == '': continue
      elif response in 'S s': break
      elif response in 'A a': raise Exception("No changes made to database")
      else :
        try:
          swapVal = int(response)
        except ValueError:
          raise Exception('Please enter an integer, blank,  or S or s or A or a')
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
      raise Exception("No changes made to database")
    # assume No
    print ("\n\n")
    # End while Done

  return rowDict


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
        raise Exception( "str(e)" + "\nCannot open the RM database file. \n")
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
