import os
import sys
import sqlite3
from datetime import datetime
import configparser
import subprocess
import traceback

# Always make a database backup before using this script.

# Requirements:
#   RootsMagic database file
#   RM-Python-config.ini

# Tested with: 
#   RootsMagic database file v9.1.6
#   Python for Windows v3.12.3

# Config files fields used
#    FILE_PATHS  REPORT_FILE_PATH
#    FILE_PATHS  REPORT_FILE_DISPLAY_APP
#    FILE_PATHS  DB_PATH
#    FILE_PATHS  RMNOCASE_PATH
#
#    OPTIONS     GROUP_FROM_SQL_OPTION_SET
#
#    <value of G_F_S_O_S>     RM_GROUP_NAME
#    <value of G_F_S_O_S>     UPDATE_GROUP
#    <value of G_F_S_O_S>     SQL_QUERY
#    <value of G_F_S_O_S>     UPDATE_GROUP


# ===================================================DIV60==
def main():

    # Configuration
    config_file_name = "RM-Python-config.ini"
    db_connection = None
    report_display_app = None
    RMNOCASE_required = True
    allow_db_changes = True

    # ===========================================DIV50==
    # Errors go to console window
    # ===========================================DIV50==
    try:
        # config file must be in "current directory" and encoded as UTF-8 (no BOM).
        # see   https://docs.python.org/3/library/configparser.html
        config_file_path = os.path.join(
            get_current_directory(), config_file_name)

        # Check that config file is at expected path and that it is readable & valid.
        if not os.path.exists(config_file_path):
            raise RM_Py_Exception(
                "ERROR: The configuration file, " + config_file_name
                + " must be in the same directory as the .py or .exe file." "\n\n")

        config = configparser.ConfigParser(empty_lines_in_values=False,
                                           interpolation=None)
        try:
            config.read(config_file_path, 'UTF-8')
        except:
            raise RM_Py_Exception(
                "ERROR: The " + config_file_name
                + " file contains a format error and cannot be parsed." "\n\n")
        try:
            report_path = config['FILE_PATHS']['REPORT_FILE_PATH']
        except:
            raise RM_Py_Exception(
                'ERROR: REPORT_FILE_PATH must be defined in the '
                + config_file_name + "\n\n")
        try:
            # Use UTF-8 encoding for the report file. Test for write-ability
            open(report_path,  mode='w', encoding='utf-8')
        except:
            raise RM_Py_Exception('ERROR: Cannot create the report file '
                                  + report_path + "\n\n")

    except RM_Py_Exception as e:
        pause_with_message(e)
        return 1
    except Exception as e:
        traceback.print_exception(e, file=sys.stdout)
        pause_with_message(
            "ERROR: Application failed. Please email error report:" "\n\n " +
            str(e)
            + "\n\n" "to the author")
        return 1

    # open the already tested report file
    report_file = open(report_path,  mode='w', encoding='utf-8')

    # ===========================================DIV50==
    # Errors from here forward, go to Report File
    # ===========================================DIV50==
    try:
        try:
            report_display_app = config['FILE_PATHS']['REPORT_FILE_DISPLAY_APP']
        except:
            pass
        if report_display_app is not None and not os.path.exists(report_display_app):
            raise RM_Py_Exception(
                'ERROR: Path for report file display app not found: '
                + report_display_app)

        try:
            database_path = config['FILE_PATHS']['DB_PATH']
        except:
            raise RM_Py_Exception('ERROR: DB_PATH must be specified.')
        if not os.path.exists(database_path):
            raise RM_Py_Exception(
                'ERROR: Path for database not found: ' + database_path
                + '\n\n' 'Absolute path checked:\n"'
                + os.path.abspath(database_path) + '"')

        if RMNOCASE_required:
            try:
                rmnocase_path = config['FILE_PATHS']['RMNOCASE_PATH']
            except:
                raise RM_Py_Exception(
                    'ERROR: RMNOCASE_PATH must be specified.')
            if not os.path.exists(rmnocase_path):
                raise RM_Py_Exception(
                    'ERROR: Path for RMNOCASE extension (unifuzz64.dll) not found: '
                    + rmnocase_path
                    + '\n\n' 'Absolute path checked:\n"'
                    + os.path.abspath(rmnocase_path) + '"')

        # RM database file info
        file_modification_time = datetime.fromtimestamp(
            os.path.getmtime(database_path))

        if RMNOCASE_required:
            db_connection = create_db_connection(database_path, rmnocase_path)
        else:
            db_connection = create_db_connection(database_path, None)

        # write header to report file
        report_file.write("Report generated at      = " + time_stamp_now()
                          + "\n" "Database processed       = "
                          + os.path.abspath(database_path)
                          + "\n" "Database last changed on = "
                          + file_modification_time.strftime("%Y-%m-%d %H:%M:%S")
                          + "\n" "SQLite library version   = "
                          + get_SQLite_library_version(db_connection) + "\n\n\n\n")

        run_selected_features(config, db_connection, report_file)

    except (sqlite3.OperationalError, sqlite3.ProgrammingError) as e:
        report_file.write(
            "ERROR: SQL execution returned an error \n\n" + str(e))
        return 1
    except RM_Py_Exception as e:
        report_file.write(str(e))
        return 1
    except Exception as e:
        traceback.print_exception(e, file=report_file)
        report_file.write(
            "\n\n" "ERROR: Application failed. Please email report file to author. ")
        return 1
    finally:
        if db_connection is not None:
            if allow_db_changes:
                db_connection.commit()
            db_connection.close()
        report_file.close()
        if report_display_app is not None:
            subprocess.Popen([report_display_app, report_path])
    return 0


# ===================================================DIV60==
def run_selected_features(config, db_connection, report_file):

    RunSQLGroupFeature(config, db_connection, report_file)


# ===================================================DIV60==
def RunSQLGroupFeature(config, db_connection, report_file):

    try:
        ActiveOptionsSection = config['OPTIONS']['GROUP_FROM_SQL_OPTION_SET']
    except:
        raise Exception(
            'section: [OPTIONS],  key: GROUP_FROM_SQL_OPTION_SET   not found.')
    try:
        config[ActiveOptionsSection]
    except:
        raise Exception(
            'section: [' + ActiveOptionsSection + ']   not found.')
    try:
        groupName = config[ActiveOptionsSection]['RM_GROUP_NAME']
    except:
        raise Exception(
            'section: [' + ActiveOptionsSection + '],  key: RM_GROUP_NAME   not found.')
    try:
        config[ActiveOptionsSection]['UPDATE_GROUP']
    except:
        raise Exception(
            'section: [' + ActiveOptionsSection + '],  key: UPDATE_GROUP   not found.')
    try:
        SQLvalue =config[ActiveOptionsSection]['SQL_QUERY']
    except:
        raise Exception(
            'section: [' + ActiveOptionsSection + '],  key: SQL_QUERY   not found.')
    try:
        updateGroup = config[ActiveOptionsSection].getboolean('UPDATE_GROUP')
    except:
        raise Exception(
            'section: [' + ActiveOptionsSection + '],  key: UPDATE_GROUP value not interpretable.')


    viewStmt = "DROP VIEW IF EXISTS PersonIdList_RJO_utils"
    try:
        cur = db_connection.cursor()
        cur.execute(viewStmt)
    except Exception as e:
        # database open issues don't appear until here !
        raise Exception('Cannot open the database.\n' + str(e))

    if ActiveOptionsSection == '':
        raise Exception('section: [OPTIONS], key: GROUP_FROM_SQL_OPTION_SET \n' +
                        'No value entered.\n Nothing to do.')
    
    if SQLvalue == '':
        raise Exception('section: [GROUP_FROM_SQL_OPTION_SET], key:  \n' +
                        'No value entered.\n Nothing to do.')


    # generate the SQL statement and create the view
    SqlStmt = "CREATE TEMP VIEW PersonIdList_RJO_utils AS " + SQLvalue
    try:
        cur = db_connection.cursor()
        cur.execute(SqlStmt)
    except:
        raise Exception("ERROR: Creating a VIEW on SQL_QUERY returned an error. \n" +
                        "SQL entered was:\n\n" + SQLvalue + "\n")

    # errors in SQL show up here, not in view creation
    try:
        SqlStmt = "select count() from PersonIdList_RJO_utils"
        cur = db_connection.cursor()
        cur.execute(SqlStmt)
        numInView = cur.fetchone()[0]
        report_file.write("# of persons selected: " + str(numInView) + "\n")
    except:
        raise ("ERROR: SQL_QUERY returned an error when run as a VIEW. \n\n" +
               "SQL entered was:\n" + SQLvalue + "\n")

    CreateGroup(groupName, updateGroup, report_file, db_connection)

    report_file.write("\nSQL used to specify group membership:\n\n" + SQLvalue)

    viewStmt = "DROP VIEW IF EXISTS PersonIdList_RJO_utils"
    cur = db_connection.cursor()
    cur.execute(viewStmt)

    return


# ===================================================DIV60==
def CreateGroup(Name, updateGroup, report_file, dbConnection):
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
    cur.execute(SqlStmt, (Name,))
    result = cur.fetchone()
    existingNumber = result[0]
    GroupID = result[1]

    if existingNumber > 1:
        report_file.write("\nERROR: Group: " + Name +
              " already exists more than once.\n Use a different name. \n")
        # return does cleanup and pause
        return

    if existingNumber == 1 and not updateGroup:
        report_file.write("\nERROR: Group: " + Name +
              " already exists and Update was not specified.\n Use a different name or allow update. \n")
        # return does cleanup and pause
        return

    if existingNumber == 1 and updateGroup:
        report_file.write("\nINFO: Group: " + Name +
              " already exists and will be updated. \n")

    else:  # existingNumber == 0
        report_file.write("\nINFO: Group: " + Name + " will be created. \n")

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
            cur.execute(SqlStmt, (Name,))
        except Exception as e:
            raise Exception(
                'Cannot update TagTable. Close RM and try again.\n' + str(e))

        SqlStmt = """
    SELECT TagValue from TagTable where TagID == last_insert_rowid()
    """
        cur = dbConnection.cursor()
        cur.execute(SqlStmt)
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
        cur.execute(SqlStmt, (GroupID,))
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
        cur.execute(SqlStmt, (GroupID,))
    except Exception as e:
        raise Exception(
            'Cannot populate group. Close RM and try again.\n' + str(e))

    return


# ===================================================DIV60==
def pause_with_message(message=None):

    if (message != None):
        print(str(message))
    input("\n" "Press the <Enter> key to continue...")
    return


# ===================================================DIV60==
def time_stamp_now(type=""):

    # return a TimeStamp string
    now = datetime.now()
    if type == '':
        dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
    elif type == 'file':
        dt_string = now.strftime("%Y-%m-%d_%H%M%S")
    return dt_string


# ===================================================DIV60==
def get_SQLite_library_version(dbConnection):

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
def create_db_connection(db_file_path, db_extension):

    db_connection = None
    try:
        db_connection = sqlite3.connect(db_file_path)
        if db_extension is not None and db_extension != '':
            # load SQLite extension
            db_connection.enable_load_extension(True)
            db_connection.load_extension(db_extension)
    except Exception as e:
        raise RM_Py_Exception(e, "\n\n" "Cannot open the RM database file." "\n")
    return db_connection


# ===================================================DIV60==
class RM_Py_Exception(Exception):

    '''Exceptions thrown for configuration/database issues'''


# ===================================================DIV60==
# Call the "main" function
if __name__ == '__main__':
    main()

# ===================================================DIV60==
