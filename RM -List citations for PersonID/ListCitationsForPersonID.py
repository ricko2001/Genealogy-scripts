import os
import sys
import sqlite3
import configparser
from datetime import datetime
import subprocess
import traceback

# List all citations associated with a Person

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
#    RIN         PERSON_RIN

# ===================================================DIV60==
def main():

    # Configuration
    config_file_name = "RM-Python-config.ini"
    db_connection = None
    report_display_app = None
    RMNOCASE_required = False
    allow_db_changes = False

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

    display_sources_feature(config, db_connection, report_file)


# ===================================================DIV60==
def display_sources_feature(config, db_connection, report_file):

    PersonID = None
    try:
        PersonID_str = config['RIN']['PERSON_RIN']
        PersonID = int(PersonID_str)

    except:
        pass
    
    if PersonID is None:
        PersonID_str = input("\n"  "PersonID/RIN =")
        try:
            PersonID = int(PersonID_str)
        except:
            raise RM_Py_Exception('ERROR: Enter an integer for the PersonID/RIN.')
        if not PersonID >0: 
            raise RM_Py_Exception('ERROR: Enter an integer larger than 0.')

    SqlStmt="""\
--      PERSON sources
SELECT DISTINCT SourceTable.Name COLLATE NOCASE, CitationTable.CitationName COLLATE NOCASE
  FROM SourceTable
  JOIN CitationTable     ON SourceTable.SourceID = CitationTable.SourceID
  JOIN CitationLinkTable ON CitationTable.CitationID = CitationLinkTable.LinkID
  WHERE CitationLinkTable.OwnerID=?
    AND CitationLinkTable.OwnerType=0

UNION

--      NAME sources
SELECT DISTINCT SourceTable.Name COLLATE NOCASE, CitationTable.CitationName COLLATE NOCASE
  FROM SourceTable
  JOIN CitationTable     ON SourceTable.SourceID = CitationTable.SourceID
  JOIN CitationLinkTable ON CitationTable.CitationID = CitationLinkTable.LinkID
  JOIN NameTable         ON CitationLinkTable.OwnerID = NameTable.NameID
  WHERE NameTable.OwnerID=?
    AND CitationLinkTable.OwnerType=7

UNION

--      EVENT-PERSON sources
SELECT DISTINCT SourceTable.Name COLLATE NOCASE, CitationTable.CitationName COLLATE NOCASE
  FROM SourceTable
  JOIN CitationTable     ON SourceTable.SourceID = CitationTable.SourceID
  JOIN CitationLinkTable ON CitationTable.CitationID = CitationLinkTable.LinkID
  JOIN EventTable ON CitationLinkTable.OwnerID = EventTable.EventID
  WHERE EventTable.OwnerID=?
    AND CitationLinkTable.OwnerType=2
    AND EventTable.OwnerType=0

UNION

--      EVENT-FAMILY sources
SELECT DISTINCT SourceTable.Name COLLATE NOCASE, CitationTable.CitationName COLLATE NOCASE
  FROM SourceTable
  JOIN CitationTable     ON SourceTable.SourceID = CitationTable.SourceID
  JOIN CitationLinkTable ON CitationTable.CitationID = CitationLinkTable.LinkID
  JOIN EventTable        ON CitationLinkTable.OwnerID = EventTable.EventID
  JOIN FamilyTable       ON EventTable.OwnerID = FamilyTable.FamilyID
  WHERE (FamilyTable.FatherID=? OR FamilyTable.MotherID=?)
    AND CitationLinkTable.OwnerType=2
    AND EventTable.OwnerType=1

UNION

--      FAMILY sources
SELECT DISTINCT SourceTable.Name COLLATE NOCASE, CitationTable.CitationName COLLATE NOCASE
  FROM SourceTable
  JOIN CitationTable     ON SourceTable.SourceID = CitationTable.SourceID
  JOIN CitationLinkTable ON CitationTable.CitationID = CitationLinkTable.LinkID
  JOIN FamilyTable       ON CitationLinkTable.OwnerID = FamilyTable.FamilyID
  WHERE (FamilyTable.FatherID=? OR FamilyTable.MotherID=?)
    AND CitationLinkTable.OwnerType=1
    
ORDER BY SourceTable.Name COLLATE NOCASE;
"""

    cur = db_connection.cursor()
    cur.execute(SqlStmt, (PersonID,PersonID,PersonID,PersonID,PersonID,PersonID,PersonID) )
    rows = cur.fetchall()

    report_file.write("PersonID = " + str(PersonID) + "\n")
    report_file.write (str(len(rows)) + " source citations found \n\n")

    for row in rows:
        report_file.write(row[0] + "\t\t" + row[1] + "\n\n")

    report_file.write("================================================" "\n\n")

    return


# ===================================================DIV60==
def create_db_connection(db_file_path, db_extension_file_path):

    dbConnection = None
    try:
        dbConnection = sqlite3.connect(db_file_path)
        if db_extension_file_path is not None:
            # load SQLite extension
            dbConnection.enable_load_extension(True)
            dbConnection.load_extension(db_extension_file_path)
    except Exception as e:
        raise RM_Py_Exception(
            e, "\n\n" "Cannot open the RM database file." "\n")
    return dbConnection


# ===================================================DIV60==
def get_SQLite_library_version(dbConnection):

    # returns a string like 3.42.0
    SqlStmt = "SELECT sqlite_version()"
    cur = dbConnection.cursor()
    cur.execute(SqlStmt)
    return cur.fetchone()[0]


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
def pause_with_message(message=None):

    if (message != None):
        print(str(message))
    input("\n" "Press the <Enter> key to continue...")
    return


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
class RM_Py_Exception(Exception):

    '''Exceptions thrown for configuration/database issues'''


# ===================================================DIV60==
# Call the "main" function
if __name__ == '__main__':
    main()

# ===================================================DIV60==
