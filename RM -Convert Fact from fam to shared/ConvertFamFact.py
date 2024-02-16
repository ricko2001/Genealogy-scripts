import os, sys
import sqlite3
from pathlib import Path
from datetime import datetime
import configparser
import xml.etree.ElementTree as ET
import hashlib
import subprocess
import traceback

# Convert Fam type facts to individual facts
# not intended for Marriage, Divorce etc or Number of children facts


#  where can FactType NAMES be found- not abbrev


## Tested with RootsMagic v9.1.3
##             Python for Windows v3.11.0
##             unifuzz64.dll (ver not set, MD5=06a1f485b0fae62caa80850a8c7fd7c2)

# ===================================================DIV60==
def main():
  # Configuration
  IniFileName = "RM-Python-config.ini"

#  PauseWithMessage("Always have a known-good database backup before running this script\n"
#                      "You will likely want to fix problems in the first run");


# consider whether the util should be more general say convert any fact tinto any other?

# the first person in fam fact will retain the new indiv fact, the second person will be shared fact.

# All of the roles used in the old fact must also appear in the new fact


    # Facts to convert				 new fact to create
    #  FTID	name				FTID	name			2nd person		RoleID
    #  311	Census fam			18		Census			spouse			420 
    #  310	Residence fam		29		Residence		spouse			417 
    # 1071	Psgr List fam 		1001	Psgr List		Principal2		421
    # 1066	Note fam			1026	Note			Principal2		416 


  try:        #errors go to console window
    # ini file must be in "current directory" and encoded as UTF-8 (no BOM).
    # see   https://docs.python.org/3/library/configparser.html
    IniFile = os.path.join(get_current_directory(), IniFileName)

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
      report_Path   = config['FILE_PATHS']['REPORT_FILE_PATH']
    except:
      raise RMPyException('ERROR: REPORT_FILE_PATH must be defined in the '
            + IniFileName + "\n\n")

    try:
      # Use UTF-8 encoding for the report file. Test for write-ability
      open( report_Path,  mode='w', encoding='utf-8')
    except:
      raise RMPyException('ERROR: Cannot create the report file '
            + report_Path + "\n\n")

  except RMPyException as e:
    PauseWithMessage( e );
    return 1
  except Exception as e:
    traceback.print_exception(e, file=sys.stdout)
    PauseWithMessage( "Application failed. Please report. " + str(e) );
    return 1

  # Open the Report File.

  with open( report_Path,  mode='w', encoding='utf-8') as reportF:

    try:        # errors go to the report file
      try:
        database_path = config['FILE_PATHS']['DB_PATH']
      except:
        raise RMPyException('DB_PATH must be specified.')
      if not os.path.exists(database_path):
        raise RMPyException('Path for database not found: ' + database_path
                           +'\n\nAbsolute path checked:\n"'
                           + os.path.abspath(database_path) + '"')
  
      try:
        RMNOCAE_path = config['FILE_PATHS']['RMNOCASE_PATH']
      except:
        raise RMPyException('RMNOCASE_PATH must be specified.') 
      if not os.path.exists(RMNOCAE_path):
        raise RMPyException('Path for database extension unifuzz64.dll not found: ' + RMNOCAE_path
                           +'\n\n Absolute path checked:\n"'
                           + os.path.abspath(RMNOCAE_path) + '"')

      try:
        ReportDisplayApp = config['FILE_PATHS']['REPORT_FILE_DISPLAY_APP']
      except:
        ReportDisplayApp = None
      if ReportDisplayApp != None and not os.path.exists(ReportDisplayApp):
        raise RMPyException('Path for report file display app not found: '
                           + ReportDisplayApp)

      try:
        fact_current = config['MAPPING']['FACT_CURRENT']
      except:
        raise RMPyException('FACT_CURRENT must be specified.')
  
      try:
        fact_new = config['MAPPING']['FACT_NEW']
      except:
        raise RMPyException('FACT_NEW must be specified.')
  
      try:
        role = config['MAPPING']['ROLE']
      except:
        raise RMPyException('ROLE must be specified.')

      # RM database file info
      FileModificationTime = datetime.fromtimestamp(os.path.getmtime(database_path))
      G_DbFileFolderPath = Path(database_path).parent

      # write header to report file
      with create_DBconnection(database_path, RMNOCAE_path) as dbConnection:
        reportF.write ("Report generated at      = " + TimeStampNow()
                       + "\nDatabase processed       = " + os.path.abspath(database_path)
                       + "\nDatabase last changed on = "
                       + FileModificationTime.strftime("%Y-%m-%d %H:%M:%S")
                       + "\nSQLite library version   = "
                       + GetSQLiteLibraryVersion (dbConnection) + "\n\n")


        reportF.write ('Original FactType: "' + fact_current + '"\nNew FactType: "'
                      + fact_new + '"\nrole: "' + role + '"\n\n\n')

        lookup_validate (fact_current, fact_new, role, dbConnection, reportF)

        convert_fact (fact_current, fact_new, role, dbConnection, reportF)



    except RMPyException as e:
      reportF.write( str(e) )
      return 1
    except Exception as e:
      traceback.print_exception(e, file=reportF)
      reportF.write( "\n\n Application failed. Please email report file to author. ")
      return 2


  # report file is now closed. Can be opened for display
  if ReportDisplayApp != None:
    subprocess.Popen( [ReportDisplayApp, report_Path] )
  return 0


# ===================================================DIV60==
def lookup_validate( fact_current_name, fact_new_name, role_name, dbConnection, reportF):
  # confirm fact_current_name is unique
  SqlStmt = """
  SELECT FactTypeID, OwnerType
    FROM FactTypeTable ftt
  WHERE  ftt.Name = ?
  """

  with dbConnection:
    cur = dbConnection.cursor()
    cur.execute(SqlStmt, (fact_current_name,))
    rows = cur.fetchall()
  if len(rows) == 0:
    raise RMPyException ( "The entered current fact type name could not be found.\n")
  if len(rows) > 1:
    raise RMPyException ( "The entered current fact type name is not unique. Fix this.\n")
  if rows[0][1] == 1:
    reportF.write( "The entered current fact type name is a FAMILY type.\n")
  FactTypeID_current = rows[0][0] 

  with dbConnection:
    cur = dbConnection.cursor()
    cur.execute(SqlStmt, (fact_new_name,))
    rows = cur.fetchall()
  if len(rows) == 0:
    raise RMPyException ( "The entered new fact type name could not be found.\n")
  if len(rows) > 1:
    raise RMPyException ( "The entered new fact type name is not unique. Fix this.\n")
  if rows[0][1] == 1:
    reportF.write( "The entered new fact type name is a FAMILY type.\n")
  FactTypeID_new = rows[0][0] 


  SqlStmt = """
  SELECT RoleID, EventType
    FROM RoleTable rt
  WHERE  rt.RoleName = ?
     AND rt.EventType = ?
  """

  with dbConnection:
    cur = dbConnection.cursor()
    cur.execute(SqlStmt, (role_name, FactTypeID_new))
    rows = cur.fetchall()
  if len(rows) == 0:
    raise RMPyException ( "The entered Role type name could not be found associated with the new fact type.\n")
  if len(rows) > 1:
    raise RMPyException ( "The entered Role type name is not unique for the new fact type. Fix this.\n")
  RoleTypeID = rows[0][0] 

# All of the roles used in the old fact must also appear in the new fact
  SqlStmt = """
  SELECT RoleID, EventType
    FROM RoleTable rt
  WHERE  rt.RoleName = ?
     AND rt.EventType = ?
  """

  with dbConnection:
    cur = dbConnection.cursor()
    cur.execute(SqlStmt, (role_name, FactTypeID_new))
    rows = cur.fetchall()


  return ( FactTypeID_current, FactTypeID_new, RoleTypeID)



# ===================================================DIV60==
def convert_fact ( FactTypeID, newFactTypeID, roleID, dbConnection, reportF):

  listOfFactIDs = getListOfEventsToConvert(FactTypeID, dbConnection)

  # PauseWithMessage (str(len(listOfFactIDs)) + "  Facts will be converted \n\n")

  for  FactToConevert in listOfFactIDs:
    reportF.write (str(FactToConevert))

    FamID = getFamilyIDfromEvent(FactToConevert, dbConnection)
    FatherMother = getFatherMotherIDs(FamID, dbConnection)

    FatherID = FatherMother[0]
    MotherID = FatherMother[1]
    reportF.write ("  Father ID: " +  str(FatherID) + "    MotherID: " + str(MotherID))

    changeTheEvent(FactToConevert, FatherID, newFactTypeID, dbConnection)
    addWitness( FactToConevert, MotherID, roleID, dbConnection)


# ===================================================DIV60==
def getFamilyIDfromEvent(ID, dbConn):

  SqlStmt = """
  SELECT OwnerID
    FROM EventTable et
  WHERE  et.EventID = ?
  """

  with dbConn:
    cur = dbConn.cursor()
    cur.execute(SqlStmt, (ID,))
    rows = cur.fetchall()

    if (len(rows) != 1):
      reportF.write ("more than one owner ID found")
      raise Error

  return rows[0][0]



# ===================================================DIV60==
def getListOfEventsToConvert(ID, dbConn):

  SqlStmt = """
  SELECT EventID
    FROM EventTable et
   WHERE et.EventType = ?
     AND et.OwnerType = 1
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

  SqlStmt = """
  SELECT FatherID, MotherID
    FROM FamilyTable ft
   WHERE ft.FamilyID = ?
  """

  with dbConn:
    cur = dbConn.cursor()
    cur.execute(SqlStmt, (ID,))
    rows = cur.fetchall()

    if (len(rows) != 1):
      reportF.write ("more than one row returned getting family id")
      raise Error

  return [ rows [0][0], rows [0][1] ]


# ===================================================DIV60==
def changeTheEvent(EventID, OwnerID, newEventTypeID, dbConn):

  SqlStmt = """
  UPDATE EventTable
     SET OwnerType = 0,
         EventType= ?,
         OwnerID = ?
   WHERE EventID = ?
  """

  with dbConn:
    cur = dbConn.cursor()
    cur.execute(SqlStmt, (newEventTypeID, OwnerID, EventID) )


# ===================================================DIV60==
def addWitness( EventID, OwnerID, RoleID, dbConn):

  SqlStmt = """
  INSERT INTO WitnessTable
    ( EventID, PersonID, Role)
    VALUES ( ?, ?, ? )
  """
  with dbConn:
    cur = dbConn.cursor()
    cur.execute(SqlStmt, ( EventID, OwnerID, RoleID ))


# ===================================================DIV60==
def create_DBconnection(db_file_path, db_extension):
  dbConnection = None
  try:
    dbConnection = sqlite3.connect(db_file_path)

    # load SQLite extension
    dbConnection.enable_load_extension(True)
    dbConnection.load_extension(db_extension)
  except Exception as e:
    raise RMPyException(e, "\n\n" "Cannot open the RM database file." "\n")

  return dbConnection

# ===================================================DIV60==
def PauseWithMessage(message = None):
  if (message != None):
    print(str(message))
  input("\n" "Press the <Enter> key to continue...")
  return


# ===================================================DIV60==
def TimeStampNow(type=""):
  # return a TimeStamp string
  now = datetime.now()
  if type == '':
    dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
  elif type == 'file':
    dt_string = now.strftime("%Y-%m-%d_%H%M%S")
  return dt_string


# ===================================================DIV60==
def GetSQLiteLibraryVersion (dbConnection):
  # returns a string like 3.42.0
  SqlStmt="""
  SELECT sqlite_version()
  """
  cur = dbConnection.cursor()
  cur.execute(SqlStmt)
  return cur.fetchone()[0]

# ===================================================DIV60==
def get_current_directory():
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
