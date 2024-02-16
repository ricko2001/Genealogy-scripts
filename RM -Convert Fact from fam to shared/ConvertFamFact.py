# Convert Fam type facts to individual facts
# not intended for Marriage, Divorce etc or Number of children facts

import sqlite3
from sqlite3 import Error
import sys

## Tested with RootsMagic v9.1.3
##             Python for Windows v3.11.0
##             unifuzz64.dll (ver not set, MD5=06a1f485b0fae62caa80850a8c7fd7c2)

# ===================================================DIV60==
def main():
  # Configuration
  IniFileName = "RM-Python-config.ini"

 # PauseWithMessage("Always have a known-good database backup before running this script");


  try:        #errors go to console window
    # ini file must be in "current directory" and encoded as UTF-8 (no BOM).
    # see   https://docs.python.org/3/library/configparser.html
    IniFile = os.path.join(GetCurrentDirectory(), IniFileName)

    # Check that ini file is at expected path and that it is readable & valid.
    if not os.path.exists(IniFile):
        raise RMPyException("ERROR: The ini configuration file, " + IniFileName
              + " must be in the same directory as the .py or .exe file.\n\n" )

    config = configparser.ConfigParser(empty_lines_in_values=False,
                                       interpolation=None)
    try:
      config.read(IniFile, 'UTF-8')
    except:
     raise RMPyException("ERROR: The " + IniFileName
           + " file contains a format error and cannot be parsed.\n\n" )

    try:
      database_Path = config['FILE_PATHS']['DB_PATH']
    except:
      raise RMPyException('DB_PATH must be specified.')
  
    if not os.path.exists(database_Path):
      raise RMPyException('Path for database not found: ' + database_Path
                         +'\n\nAbsolute path checked:\n"'
                         + os.path.abspath(database_Path) + '"')

    try:
      RMNOCAE_Path = config['FILE_PATHS']['RMNOCASE_PATH']
    except:
      raise RMPyException('RMNOCASE_PATH must be specified.')
  
    if not os.path.exists(RMNOCAE_Path):
      raise RMPyException('Path for database extension unifuzz64.dll not found: ' + RMNOCAE_Path
                         +'\n\nAbsolute path checked:\n"'
                         + os.path.abspath(RMNOCAE_Path) + '"')





  except RMPyException as e:
    PauseWithMessage( e );
    return 1
  except Exception as e:
    traceback.print_exception(e, file=sys.stdout)
    PauseWithMessage( "Application failed. Please report. " + str(e) );
    return 1

# get from ini file values for
#  CURRENT_FACT
#  NEW_FACT
#  ROLE  for the spouse

# do one set of conversions at a time.

# first use integers
# then switvh to names in quotes

# confirm CURRENT_FACT is a family fact and new is indiv fact type




    # Facts to convert				 new fact to create
    #  FTID	name				FTID	name			2nd person		RoleID
    #  311	Census fam			18		Census			spouse			420 
    #  310	Residence fam		29		Residence		spouse			417 
    # 1071	Psgr List fam 		1001	Psgr List		Principal2		421
    # 1066	Note fam			1026	Note			Principal2		416 

    frFactToFactRole = [
     (  311,   18, 420 ),
     (  310,   29, 417 ),
     ( 1071, 1001, 421 ),
     ( 1066, 1026, 416 ) ] 



    dbConn = create_connection(database, RMNOCASE_extention)

    for FactSet in frFactToFactRole:
      FactTypeID    = FactSet[0]
      newFactTypeID = FactSet[1]
      roleID        = FactSet[2]

      print ( "Original FactTypeID: ", FactTypeID, "New FactTypeID: ", newFactTypeID, "roleID:" , roleID )

      listOfFactIDs = getListOfEventsToConvert(FactTypeID, dbConn)

      print (len(listOfFactIDs), "Facts of this type to be converted \n\n")

      for  FactToConevert in listOfFactIDs:
        print (FactToConevert)

        FamID = getFamilyIDfromEvent(FactToConevert, dbConn)
        FatherMother = getFatherMotherIDs(FamID, dbConn)

        FatherID = FatherMother[0]
        MotherID = FatherMother[1]
        print ("  Father ID: ",  FatherID, "    MotherID: ",  MotherID)

        changeTheEvent(FactToConevert, FatherID, newFactTypeID, dbConn)
        addWitness( FactToConevert, MotherID, roleID, dbConn)

  except Error as e:
    print( "Encountered an error", e )
  return 0


# ===================================================DIV60==

# ===================================================DIV60==
def create_connection(db_file, RMNOCASE_extention):
  conn = None

  conn = sqlite3.connect(db_file)

  # load extension used by RootsMagic
  conn.enable_load_extension(True)
  conn.load_extension(RMNOCASE_extention)

  return conn


# ===================================================DIV60==
def getFamilyIDfromEvent(ID, dbConn):

  SqlStmt = """\
    SELECT OwnerID
      FROM EventTable et
    WHERE
      et.EventID = ?
"""

  with dbConn:
    cur = dbConn.cursor()
    cur.execute(SqlStmt, (ID,))
    rows = cur.fetchall()

    if (len(rows) != 1):
      print ("more than one owner ID found")
      raise Error

  return rows[0][0]



# ===================================================DIV60==
def getListOfEventsToConvert(ID, dbConn):

  SqlStmt = """\
    SELECT EventID
      FROM EventTable et
      WHERE
        et.EventType = ?
        AND
        et.OwnerType = 1
"""

  with dbConn:
    cur = dbConn.cursor()
    cur.execute(SqlStmt, (ID,))
    rows = cur.fetchall()

    listOfFactIDs = []
    for x in range( len(rows) ):
      listOfFactIDs.append( rows [x] [0] )

  return listOfFactIDs


# ===================================================DIV60==
def getFatherMotherIDs(ID, dbConn):

  SqlStmt = """\
    SELECT FatherID, MotherID
    from FamilyTable ft
    WHERE
    ft.FamilyID = ?
"""

  with dbConn:
    cur = dbConn.cursor()
    cur.execute(SqlStmt, (ID,))
    rows = cur.fetchall()

    if (len(rows) != 1):
      print ("more than one row returned getting family id")
      raise Error

  return [ rows [0][0], rows [0][1] ]


# ===================================================DIV60==
def changeTheEvent(EventID, OwnerID, newEventTypeID, dbConn):

  SqlStmt = """\
    UPDATE EventTable
      SET OwnerType = 0,
          EventType= ?,
          OwnerID = ?
    WHERE
          EventID = ?
"""

  with dbConn:
    cur = dbConn.cursor()
    cur.execute(SqlStmt, (newEventTypeID, OwnerID, EventID) )


# ===================================================DIV60==
def addWitness( EventID, OwnerID, RoleID, dbConn):

  SqlStmt = """\
     INSERT INTO WitnessTable
        ( EventID, PersonID, Role)
      VALUES ( ?, ?, ? )
"""
  with dbConn:
    cur = dbConn.cursor()
    cur.execute(SqlStmt, ( EventID, OwnerID, RoleID ))


# ===================================================DIV60==
def create_DBconnection(db_file_path, reportF):
  dbConnection = None
  try:
    dbConnection = sqlite3.connect(db_file_path)
  except Error as e:
    raise RMPyException(e, "\n\nCannot open the RM database file. \n")

  return dbConnection


# ===================================================DIV60==
def PauseWithMessage(message = None):
  if (message != None):
    print(str(message))
  input("\nPress the <Enter> key to exit...")
  return


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
class RMPyException(Exception):
  '''Exceptions thrown for configuration/database issues'''


# ===================================================DIV60==
# Call the "main" function
if __name__ == '__main__':
  main()

# ===================================================DIV60==
