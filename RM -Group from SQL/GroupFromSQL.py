import os
import sys
import time
import sqlite3
from datetime import datetime
import configparser


## Always make a database backup before using this script.

##  Requirements: (see ReadMe.txt for details)
##   RootsMagic v9 database file
##   RM-Python-config.ini  ( Configuration ini file to set options and parameters)
##   unifuzz64.dll
##   Python v3.9 or greater


# ===================================================DIV60==
def main():
  # ini file must be in "current directory" and encoded as UTF-8 (no BOM).
  # see   https://docs.python.org/3/library/configparser.html

  # Configuration
  IniFileName = "RM-Python-config.ini"
  IniFile = os.path.join(GetCurrentDirectory(), IniFileName)
  try:
    TestConfigurationFile(IniFileName)
  except:
    return

  # Inifile validated already
  config = configparser.ConfigParser(empty_lines_in_values=False, interpolation=None)
  config.read(IniFile, 'UTF-8')

  database_Path = config['FILE_PATHS']['DB_PATH']
  RMNOCASE_Path = config['FILE_PATHS']['RMNOCASE_PATH']

  # Process the SQL and create the group
  try:
    with create_DBconnection(database_Path, RMNOCASE_Path) as dbConnection:
      print ("\nDatabase = " + os.path.abspath(database_Path) + "\n")
      RunSQLGroupFeature(config, dbConnection)

  except Exception as RunError:
    print( str(RunError))
    Pause()
    return 2

  #sucess !
  Pause()
  return 0


# ===================================================DIV60==
def TestConfigurationFile(IniFileName):
  IniFile = os.path.join(GetCurrentDirectory(), IniFileName)

  try:
    # Check that ini file is at expected path and that it is readable & valid.
    if not os.path.exists(IniFile):
      raise Exception("ERROR: The ini configuration file, " + IniFileName + 
             " must be in the same directory as the .py or .exe file.\n\n" )
  
    config = configparser.ConfigParser(empty_lines_in_values=False, interpolation=None)
    try:
      config.read(IniFile, 'UTF-8')
    except Exception as e:
      raise Exception("ERROR: The " + IniFileName + 
               " file contains a format error and cannot be parsed.\n\n" + 
                str(e) )

    # Read database and dll file paths from ini file
    try:
      database_Path = config['FILE_PATHS']['DB_PATH']
    except:
      raise Exception('DB_PATH must be specified.')

    try:
      RMNOCASE_Path = config['FILE_PATHS']['RMNOCASE_PATH']
    except:
      raise Exception('RMNOCASE_PATH must be specified.')

    if not os.path.exists(database_Path):
      raise Exception('DB_PATH for database file not found as specified: ' + database_Path +
              '\nPath checked: ' + os.path.abspath(database_Path))

    if not os.path.exists(RMNOCASE_Path):
      raise Exception('RMNOCASE_PATH for dll file not found as specified: ' + RMNOCASE_Path +
              '\nPath checked: ' + os.path.abspath(RMNOCASE_Path))

    try:
      ActiveOptionsSection = config['OPTIONS']['GROUP_FROM_SQL_OPTION_SET']
    except:
      raise Exception('section: [OPTIONS],  key: GROUP_FROM_SQL_OPTION_SET   not found.')

    if ActiveOptionsSection == '':
        raise Exception('section: [OPTIONS], key: GROUP_FROM_SQL_OPTION_SET \n' +
                                    'No value entered.\n Nothing to do.' )

    try:
      config[ActiveOptionsSection]
    except:
      raise Exception('section: [' + ActiveOptionsSection + ']   not found.')

    try:
      config[ActiveOptionsSection]['RM_GROUP_NAME']
    except:
      raise Exception('section: [' + ActiveOptionsSection + '],  key: RM_GROUP_NAME   not found.')

    try:
      config[ActiveOptionsSection]['UPDATE_GROUP']
    except:
      raise Exception('section: [' + ActiveOptionsSection + '],  key: UPDATE_GROUP   not found.')

    try:
      config[ActiveOptionsSection]['SQL_QUERY']
    except:
      raise Exception('section: [' + ActiveOptionsSection + '],  key: SQL_QUERY   not found.')

    try:
      config[ActiveOptionsSection].getboolean('UPDATE_GROUP')
    except:
      raise Exception('section: [' + ActiveOptionsSection + '],  key: UPDATE_GROUP value not interpretable.')

  except Exception as config_message:
    # Handle all configuration test failures
    print( IniFileName + " file configuration error\n")
    print( str(config_message) )
    print( "\nNo changes made." )
    Pause()
    raise
  return


# ===================================================DIV60==
def RunSQLGroupFeature(config, dbConnection):
  # config already validated, no error checking on config needed here

  ActiveOptionsSection = config['OPTIONS']['GROUP_FROM_SQL_OPTION_SET']

  viewStmt = "DROP VIEW IF EXISTS PersonIdList_RJO_utils"
  try:
    cur = dbConnection.cursor()
    cur.execute( viewStmt )
  except Exception as e:
    # database open issues don't appear until here !
    raise Exception('Cannot open the database.\n' + str(e) )

  SQLvalue = config[ActiveOptionsSection]['SQL_QUERY']

  # generate the SQL statement and create the view
  SqlStmt = "CREATE TEMP VIEW PersonIdList_RJO_utils AS " + SQLvalue
  try:
    cur = dbConnection.cursor()
    cur.execute( SqlStmt )
  except:
    raise Exception("ERROR: Creating a VIEW on SQL_QUERY returned an error. \n" +
                "SQL entered was:\n\n" + SQLvalue + "\n")

  # errors in SQL show up here, not in view creation
  try:  
    SqlStmt = "select count() from PersonIdList_RJO_utils"
    cur = dbConnection.cursor()
    cur.execute( SqlStmt )
    numInView = cur.fetchone()[0]
    print ("# of persons selected: " + str(numInView) + "\n")
  except:
    raise ("ERROR: SQL_QUERY returned an error when run as a VIEW. \n\n" +
           + "SQL entered was:\n" + SQLvalue + "\n")

  groupName = config[ActiveOptionsSection]['RM_GROUP_NAME']
  updateGroup = config[ActiveOptionsSection].getboolean('UPDATE_GROUP')

  CreateGroup( groupName, updateGroup, dbConnection)

  viewStmt = "DROP VIEW IF EXISTS PersonIdList_RJO_utils"
  cur = dbConnection.cursor()
  cur.execute( viewStmt )

  return


# ===================================================DIV60==
def CreateGroup(Name, updateGroup, dbConnection):
#  TagTable
#   TagID=rowid
#   TagType =0 for Groups
#   TagValue  for groups, value > 1000   
#      not clear if this is required  to be >1000 or what
#   TagName   duplicates nor constrained

  # check how many groupNames with name and TagTape=0 already exist
  SqlStmt = """
  SELECT count(*), TagValue FROM TagTable WHERE TagName=? AND TagType=0
  """
  cur = dbConnection.cursor()
  cur.execute(SqlStmt, (Name,) )
  result = cur.fetchone()
  existingNumber = result[0]
  GroupID = result[1]

  if existingNumber >1 :
    print ("ERROR: Group: " + Name + 
          " already exists more than once.\n Use a different name. \n")
    # return does cleanup and pause
    return

  if existingNumber == 1 and not updateGroup :
    print ("ERROR: Group: " + Name +
          " already exists and Update was not specified.\n Use a different name or allow update. \n")
    # return does cleanup and pause
    return

  if existingNumber == 1 and updateGroup :
    print ("INFO: Group: " + Name + 
          " already exists and will be updated. \n")

  else:  # existingNumber == 0
    print ("INFO: Group: " + Name + " will be created. \n")

    SqlStmt = """
    INSERT INTO TagTable (TagType, TagValue, TagName, Description, UTCModDate)
    VALUES
    (
      0
      ,(SELECT IFNULL(MAX(TagValue),0)+1 FROM TagTable)
      ,?
      ,'Created or updated by external utility'
      ,julianday('now') - 2415018.5
    )
    """
    try:
      cur = dbConnection.cursor()
      cur.execute(SqlStmt, (Name,) )
    except Exception as e:
      raise Exception('Cannot update TagTable. Close RM and try again.\n' + str(e) )

    SqlStmt = """
    SELECT TagValue from TagTable where TagID == last_insert_rowid()
    """
    cur = dbConnection.cursor()
    cur.execute(SqlStmt )
    GroupID = cur.fetchone()[0]

  PopulateGroup(GroupID, dbConnection)

  return


# ===================================================DIV60==
def PopulateGroup(GroupID, dbConnection):
  # print ("GroupID=" + str(GroupID))

  # Empty out the group if it has any members
  SqlStmt = """
  DELETE FROM GroupTable 
  WHERE GroupID = ?
  """
  try:
    cur = dbConnection.cursor()
    cur.execute(SqlStmt, (GroupID,) )
  except Exception as e:
    print('Cannot clear the group members. Close RM and try again.\n' + str(e))


  # add the members
  SqlStmt = """
  INSERT INTO GroupTable
  SELECT
   null
   ,?        AS GroupID
   ,PersonID AS StartID
   ,PersonID AS EndID
   ,(julianday('now') - 2415018.5) AS UTCModDate 

  FROM PersonIdList_RJO_utils
  """
  try:
    cur = dbConnection.cursor()
    cur.execute(SqlStmt, (GroupID,) )
  except Exception as e:
    raise Exception('Cannot populate group. Close RM and try again.\n' + str(e))


  return


# ===================================================DIV60==
def Pause():
  input("Press the <Enter> key to exit...")
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
def GetCurrentDirectory():
  # Determine if application is a script file or frozen exe and get its directory
  # see   https://pyinstaller.org/en/stable/runtime-information.html
  if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    application_path = os.path.dirname(sys.executable)
  else:
    application_path = os.path.dirname(__file__)
  return application_path


# ===================================================DIV60==
def create_DBconnection(db_file_path, RMNOCASE_Path):
  dbConnection = None

  try:
    dbConnection = sqlite3.connect(db_file_path)
    dbConnection.enable_load_extension(True)
    dbConnection.load_extension(RMNOCASE_Path)
  except Exception as e:
     raise Exception( "Cannot open the RM database file. \n" + str(e))

  return dbConnection

# ===================================================DIV60==
# Call the "main" function
if __name__ == '__main__':
    main()

# ===================================================DIV60==
