import os
import sys
import time
import sqlite3
from datetime import datetime
import configparser


## Always make a backup before using this script.

##  Requirements: (see ReadMe.txt for details)
##   RootsMagic v7, v8 or v9 database file
##   RM-Python-config.ini  ( Configuration ini file to set options and parameters)
##   unifuzz64.dll
##   Python v3.9 or greater


# ===================================================DIV60==
#  Global Variables
G_QT = "\""


# ===================================================DIV60==
def main():

  # Configuration
  IniFileName = "RM-Python-config.ini"

  # ini file must be in "current directory" and encoded as UTF-8 if non-ASCII chars present (no BOM).
  # Determine if application is a script file or frozen exe and get its directory
  # see   https://pyinstaller.org/en/stable/runtime-information.html
  if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
    application_path = os.path.dirname(sys.executable)
  else:
    application_path = os.path.dirname(__file__)
  IniFile = os.path.join(application_path, IniFileName)

  if not os.path.exists(IniFile):
      print("ERROR: The ini configuration file, " + IniFileName + " must be in the same directory as the .py or .exe file.\n\n" )
      input("Press the <Enter> key to exit...")
      return

  config = configparser.ConfigParser()

  try:
    config.read(IniFile, 'UTF-8')
  except:
    print("ERROR: The " + IniFileName + " file contains a format error and cannot be parsed.\n\n" )
    input("Press the <Enter> key to exit...")
    return

  # Read file paths from ini file
  # see   https://docs.python.org/3/library/configparser.html

  try:
    database_Path = config['FILE_PATHS']['DB_PATH']
    RMNOCASE_Path = config['FILE_PATHS']['RMNOCASE_PATH']
  except:
    print('Both DB_PATH and RMNOCASE_PATH must be specified.')
    return


  if not os.path.exists(database_Path):
    reportF.write('Path for database not found: ' + database_Path)
    return
  if not os.path.exists(RMNOCASE_Path):
    reportF.write('Path for RMNOCASE_PATH dll not found: ' + RMNOCASE_Path)
    return


  # Process the database for requested output
  with create_DBconnection(database_Path, RMNOCASE_Path) as dbConnection:
    print ("Database processed       = " + database_Path + "\n")

    if config['OPTIONS'].getboolean('RUN_SQL'):
       RunSQLFeature(config, dbConnection)

  input("Press the <Enter> key to exit...")

  return 0


# ===================================================DIV60==
def RunSQLFeature(config, dbConnection):
  FeatureName = "Unreferenced Files"

  # get option
  if config['OPTIONS'].getboolean('QUERY_GROUP_UPDATE'):
     updateGroup = True

  try:
    SqlStmt = config['OPTIONS']['SQL_QUERY']
  except:
    print ("ERROR: SQL_QUERY must be specified for this option. \n")
    input("Press the <Enter> key to exit...")
    sys.exit()

  try:
    cur= GetDBFileList(SqlStmt, dbConnection)
  except:
    print ("ERROR: SQL_QUERY returned an error. \n")
    input("Press the <Enter> key to exit...")
    sys.exit()


  peresonIdList=[]
  for row in cur:
    peresonIdList.append(row[0])
  

  groupName = ""
  try:
    groupName = config['OPTIONS']['QUERY_GROUP_NAME']
  except:
    groupName = "SqlQueryGroup_" + TimeStamp()


  CreateGroup( groupName, peresonIdList, dbConnection)




  return

# ===================================================DIV60==
def CreateGroup(Name, Members, dbConnection):
  print (len(Members))
  print ( Name)

#  TagTable
#   TagID=rowid
#   TagType =0 for Groups
#   TagValue  for groups, value > 1000    not clear if this is required or what
#   TagName   duplicates nor constrained



  # check if name with TagTape=0 already exists and how many times
  SqlStmt = """
  SELECT count(*) FROM TagTable WHERE TagName=? AND TagType=0
  """
  cur = conn.cursor()
  cur.execute(SqlStmt, (,Name) )
  number = cur.fetch()

  print (str(number))


#  GroupID = FindGroupID(GroupName)
#  PopulateGroup(GroupID, Members)
#
#  -- Create Named Group if it does not exist 'SQL: Duplicate Events'
#  INSERT INTO TagTable 
#  VALUES
#  (
#    (SELECT TagID FROM TagTable WHERE TagName LIKE 'SQL: Duplicate Events')
#    ,0
#    ,(SELECT IFNULL(MAX(TagValue),0)+1 FROM TagTable)
#    ,'SQL: Duplicate Events'
#    ,'SQLite query'
#    ,julianday('now') - 2415018.5
#  )


#  return GroupName

# ===================================================DIV60==
def DoesGroupNameExist(Name, dbConnection):



# ===================================================DIV60==
def PopulateGroup(GroupID, Members):

-- Add members to the named group
INSERT INTO GroupTable
SELECT
 null
 ,(SELECT TagValue 
  FROM TagTable 
  WHERE TagName 
  LIKE 'SQL: Duplicate Events'
   )
 ,PersonID AS StartID
 ,PersonID AS EndID
 ,(julianday('now') - 2415018.5) AS UTCModDate 



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
def GetDBFileList(SqlStmt, dbConnection):

  cur = dbConnection.cursor()
  cur.execute(SqlStmt)
  return cur



# ===================================================DIV60==
def create_DBconnection(db_file_path, RMNOCASE_Path):
    dbConnection = None
    try:
      dbConnection = sqlite3.connect(db_file_path)
      dbConnection.enable_load_extension(True)
      dbConnection.load_extension(RMNOCASE_Path)
    except Error as e:
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
