import os
import sys
import time
import sqlite3
from datetime import datetime
import configparser
import subprocess
import traceback

## Always make a database backup before using this script.
## Runs one or two SQL statements on a database and returns results

##  Requirements: (see ReadMe.txt for details)
##   RM-Python-config.ini  ( Configuration ini file to set options and parameters)
##   optional - unifuzz64.dll
##   Python v3.9 or greater


# ===================================================DIV60==
def main():
  # ini file must be in "current directory" and encoded as UTF-8 (no BOM).
  # see   https://docs.python.org/3/library/configparser.html

  # Configuration
  ini_file_name = "RM-Python-config.ini"
  db_connection = None
  rmnocase_path = None
  report_display_app = None

  try:  # errors go to console window
    # ini file must be in "current directory" and encoded as UTF-8 (no BOM).
    # see   https://docs.python.org/3/library/configparser.html
    ini_file = os.path.join(get_current_directory(), ini_file_name)

    # Check that ini file is at expected path and that it is readable & valid.
    if not os.path.exists(ini_file):
        raise RMPyExcep("ERROR: The ini configuration file, " + ini_file_name
                        + " must be in the same directory as the .py or .exe file.\n\n")

    config = configparser.ConfigParser(empty_lines_in_values=False,
                                        interpolation=None)
    try:
        config.read(ini_file, 'UTF-8')
    except:
        raise RMPyExcep("ERROR: The " + ini_file_name
                        + " file contains a format error and cannot be parsed.\n\n")

    try:
        report_path = config['FILE_PATHS']['REPORT_FILE_PATH']
    except:
        raise RMPyExcep('ERROR: REPORT_FILE_PATH must be defined in the '
                        + ini_file_name + "\n\n")

    try:
        # Use UTF-8 encoding for the report file. Test for write-ability
        open(report_path,  mode='w', encoding='utf-8')
    except:
        raise RMPyExcep('ERROR: Cannot create the report file '
                        + report_path + "\n\n")

  except RMPyExcep as e:
      PauseWithMessage(e)
      return 1
  except Exception as e:
      traceback.print_exception(e, file=sys.stdout)
      PauseWithMessage("ERROR: Application failed. Please report.\n\n " + str(e))
      return 1

  # Open the Report File.
  report_file = open(report_path,  mode='w', encoding='utf-8')

  try:        # errors go to the report file
    try:
      database_path = config['FILE_PATHS']['DB_PATH']
    except:
      raise RMPyExcep('ERROR: DB_PATH must be specified.')
    if not os.path.exists(database_path):
      raise RMPyExcep('ERROR: Path for database not found: ' + database_path
                        + '\n\n' 'Absolute path checked:\n"'
                        + os.path.abspath(database_path) + '"')

    try:
      rmnocase_path = config['FILE_PATHS']['RMNOCASE_PATH']
    except:
     pass
    if rmnocase_path is not None and not os.path.exists(rmnocase_path):
      raise RMPyExcep('ERROR: Path for RMNOCASE dll file not found: ' + rmnocase_path
                        + '\n\n' 'Absolute path checked:\n"'
                        + os.path.abspath(database_path) + '"')

    try:
        report_display_app = config['FILE_PATHS']['REPORT_FILE_DISPLAY_APP']
    except:
        pass
    if report_display_app is not None and not os.path.exists(report_display_app):
        raise RMPyExcep('ERROR: Path for report file display app not found: '
                        + report_display_app)

    # RM database file info
    FileModificationTime = datetime.fromtimestamp(
        os.path.getmtime(database_path))

    db_connection = create_db_connection(database_path, rmnocase_path)

    # write header to report file
    report_file.write("Report generated at      = " + TimeStampNow()
                      + "\n" "Database processed       = "
                      + os.path.abspath(database_path)
                      + "\n" "Database last changed on = "
                      + FileModificationTime.strftime("%Y-%m-%d %H:%M:%S")
                      + "\n" "SQLite library version   = "
                      + GetSQLiteLibraryVersion(db_connection) + "\n\n\n\n")
      
    RunSQLFeature(config, report_file, db_connection)

  except sqlite3.OperationalError as e:
    report_file.write("ERROR: SQL_QUERY returned an error \n\n" +str(e))
    return 1
  
  except RMPyExcep as e:
      report_file.write(str(e))
      return 1
  except Exception as e:
      traceback.print_exception(e, file=report_file)
      report_file.write("\n\n"
                        "ERROR: Application failed. Please email report file to author. ")
      return 1
  finally:
      if db_connection is not None:
          db_connection.commit()
          db_connection.close()
      report_file.close()
      if report_display_app is not None:
          subprocess.Popen([report_display_app, report_path])
  return 0


# ===================================================DIV60==
def RunSQLFeature(config, report_file, dbConnection):
  try:
    SqlStmt = config['SQL']['SQL_STATEMENT_1']
  except:
     raise RMPyExcep('ERROR: SQL - SQL_STATEMENT_1 must be specified.')

  # run the SQL statement
  cur = dbConnection.cursor()
  cur.execute( SqlStmt )

  report_file.write( "===============================================\n"
                    "The SQL that was run: \n\n" + SqlStmt + "\n\nThe results:\n\n")

  result = cur.fetchall()
  for row in result:
    report_file.write( str(row) + "\n")

  SqlStmt = None
  try:
    SqlStmt = config['SQL']['SQL_STATEMENT_2']
  except:
    pass

  if SqlStmt is not None:
    # run the second SQL statement
    cur = dbConnection.cursor()
    cur.execute( SqlStmt )
    
    report_file.write( "===============================================\n"
                    "The SQL that was run: \n\n" + SqlStmt + "\n\nThe results:\n\n")

    result = cur.fetchall()
    for row in result:
        report_file.write( str(row) + "\n")

  return


# ===================================================DIV60==
def create_db_connection(db_file_path, db_extension):

    dbConnection = None
    try:
        dbConnection = sqlite3.connect(db_file_path)
        if db_extension is not None and db_extension != '':
            # load SQLite extension
            dbConnection.enable_load_extension(True)
            dbConnection.load_extension(db_extension)
    except Exception as e:
        raise RMPyExcep(e, "\n\n" "Cannot open the RM database file." "\n")
    return dbConnection


# ===================================================DIV60==
def PauseWithMessage(message=None):

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
def GetSQLiteLibraryVersion(dbConnection):

    # returns a string like 3.42.0
    SqlStmt = "SELECT sqlite_version()"
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
class RMPyExcep(Exception):

    '''Exceptions thrown for configuration/database issues'''


# ===================================================DIV60==
# Call the "main" function
if __name__ == '__main__':
    main()

# ===================================================DIV60==

