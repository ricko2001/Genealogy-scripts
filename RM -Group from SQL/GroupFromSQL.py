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
  # Configuration
  IniFileName = "RM-Python-config.ini"

  # ini file must be in "current directory" and encoded as UTF-8 (no BOM).
  # see   https://docs.python.org/3/library/configparser.html
  IniFile = os.path.join(GetCurrentDirectory(), IniFileName)

  # Check that ini file is at expected path and that it is readable & valid.
  if not os.path.exists(IniFile):
      print("ERROR: The ini configuration file, " + IniFileName + 
           " must be in the same directory as the .py or .exe file.\n\n" )
      input("Press the <Enter> key to exit...")
      return 1

  config = configparser.ConfigParser(empty_lines_in_values=False, interpolation=None)
  try:
    config.read(IniFile, 'UTF-8')
  except Exception as e:
    print("ERROR: The " + IniFileName + 
             " file contains a format error and cannot be parsed.\n\n" )
    print (e)
    input("Press the <Enter> key to exit...")
    return 1

  # Read database and dll file paths from ini file
  try:
    database_Path = config['FILE_PATHS']['DB_PATH']
    RMNOCASE_Path = config['FILE_PATHS']['RMNOCASE_PATH']
  except Exception as e:
    print('Both DB_PATH and RMNOCASE_PATH must be specified.')
    print (str(e) + " not found")
    input("Press the <Enter> key to exit...")
    return 1

  if not os.path.exists(database_Path):
    print('Path for database file not found: ' + database_Path)
    print ('Path checked: ' + os.path.abspath(database_Path))
    return 1
  if not os.path.exists(RMNOCASE_Path):
    print('Path for RMNOCASE_PATH dll file not found: ' + RMNOCASE_Path)
    return 1

  # Validate existence of all required key values before opening database
  try:
    OptSet = config['OPTIONS']['GROUP_FROM_SQL_OPTION_SET']
    if OptSet == '':
      # This is the way to inactivate the database processing, 
      # but allow testing of file paths.
      print('No value for "GROUP_FROM_SQL_OPTION_SET" was entered. \nexiting.' )
      input("Press the <Enter> key to exit...")
      return 0
  except:
    print('"GROUP_FROM_SQL_OPTION_SET" key not found. exiting.')
    input("Press the <Enter> key to exit...")
    return 1

  try:
    config[OptSet]
  except:
    print('section: [' + OptSet + ']   not found. \n\nNo changes made.')
    input("Press the <Enter> key to exit...")
    return 1

  try:
    config[OptSet]['UPDATE_GROUP']
  except:
    print('section: [' + OptSet + '],  value: UPDATE_GROUP   not found. \n\nNo changes made.')
    input("Press the <Enter> key to exit...")
    return 1

  try:
    config[OptSet]['RM_GROUP_NAME']
  except:
    print('section: [' + OptSet + '],  value: RM_GROUP_NAME   not found. \n\nNo changes made.')
    input("Press the <Enter> key to exit...")
    return 1

  try:
    config[OptSet]['SQL_QUERY']
  except:
    print('section: [' + OptSet + '],  value: SQL_QUERY   not found. \n\nNo changes made.')
    input("Press the <Enter> key to exit...")
    return 1

  # Process the SQL and create the group

  with create_DBconnection(database_Path, RMNOCASE_Path) as dbConnection:
    print ("\nDatabase processed = " + os.path.abspath(database_Path) + "\n")
    RunSQLGroupFeature(config, dbConnection)

  input("Press the <Enter> key to exit...")

  return 0


# ===================================================DIV60==
def RunSQLGroupFeature(config, dbConnection):
  # get value, key existence already validated
  OptSet = config['OPTIONS']['GROUP_FROM_SQL_OPTION_SET']

  # get value, key existence already validated
  updateGroup = False
  if config[OptSet].getboolean('UPDATE_GROUP'):
    updateGroup = True

  viewStmt = "DROP VIEW IF EXISTS PersonIdList_RJO_utils"
  cur = dbConnection.cursor()
  cur.execute( viewStmt )

  # get value, key existence already validated
  SQLvalue = config[OptSet]['SQL_QUERY']

  # generate the SQL statement and create the view
  SqlStmt = "CREATE TEMP VIEW PersonIdList_RJO_utils AS " + SQLvalue
  try:
    cur = dbConnection.cursor()
    cur.execute( SqlStmt )
  except:
    print ("ERROR: Creating a VIEW on SQL_QUERY returned an error. \n")
    print ("SQL entered was:\n" + SQLvalue + "\n")
    sys.exit()

  # errors in SQL show up here, not in view creation
  try:  
    SqlStmt = "select count() from PersonIdList_RJO_utils"
    cur = dbConnection.cursor()
    cur.execute( SqlStmt )
    numInView = cur.fetchone()[0]
    print ("# of persons selected: " + str(numInView) + "\n")
  except:
    print ("ERROR: SQL_QUERY returned an error when run as a VIEW. \n")
    print ("SQL entered was:\n" + SQLvalue + "\n")
    sys.exit()

  # group name key existence already determined, so this try is not needed
  groupName = ""
  try:
    groupName = config[OptSet]['RM_GROUP_NAME']
  except:
    groupName = "SqlQueryGroup_" + TimeStampNow()

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
#   TagValue  for groups, value > 1000    not clear if this is required  to be >1000 or what
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
       print('Database probably locked. Close RM and try again.')
       print (e)
       # return does cleanup and pause
       return

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
    print('Database probably locked. Close RM and try again.')
    print (e)
    # return does cleanup and pause
    return


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
    print('Database probably locked. Close RM and try again.')
    print (e)
    # return does cleanup and pause
    return

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
        print(e)
        print( "Cannot open the RM database file. \n")
        input("Press the <Enter> key to exit...")
        sys.exit()
    return dbConnection


# ===================================================DIV60==
# Call the "main" function
if __name__ == '__main__':
    main()

# ===================================================DIV60==
