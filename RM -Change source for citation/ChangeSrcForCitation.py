import os
import sys
import sqlite3
import configparser
from datetime import datetime
import subprocess
import traceback

# Requirements:
#   RootsMagic database file v8 or 9
#   RM-Python-config.ini

# Tested with:
#   RootsMagic database file v9.1.6
#   Python for Windows v3.12.3

# Config files fields used
#    FILE_PATHS  REPORT_FILE_PATH
#    FILE_PATHS  REPORT_FILE_DISPLAY_APP
#    FILE_PATHS  DB_PATH


#   TODO add new feature to allow multiple moves at once by entering
#     a LIKE search criteria for Citation Name. Will probably want to
#     limit search to the existing source citations.


# ===================================================DIV60==
def main():

    # Configuration
    config_file_name = "RM-Python-config.ini"
    db_connection = None
    report_display_app = None
    RMNOCASE_required = False
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

    change_source_feature(config, db_connection, report_file)


# ===========================================DIV50==
def change_source_feature(config, db_connection, report_file):

    first_time = True
    while True:
        report_file.write(
            "\n" "========================================"  "\n")

        if (not first_time):
            if "y" != input("Go again ? (y/n)"):
                break
        first_time = False

        # Deal with the citation as it is
        citation_name = input(
            "Enter the citation name for citation to change source:\n")
        report_file.write("Citation name as entered =" + citation_name + "\n")

        SqlStmt = """
SELECT COUNT(), st.TemplateID, ct.CitationID, ct.SourceID, st.Name, ct.CitationName
  FROM SourceTable AS st
  JOIN CitationTable AS ct ON ct.SourceID = st.SourceID
 WHERE ct.CitationName LIKE ( ? || '%' )
"""

        cur = db_connection.cursor()
        cur.execute(SqlStmt, (citation_name, ))
        row = cur.fetchone()

        numberOfCitations = row[0]
        OldSourceTemplateID = row[1]
        CitationID = row[2]
        OldSourceID = row[3]
        OldSourceName = row[4]
        FullCitationName = row[5]

        if (numberOfCitations > 1):
            print('PROBLEM: Found more than 1 citation. ')
            report_file.write('PROBLEM: Found more than 1 citation.' '\n\n')
            report_file.write('No change made.' '\n\n')
            continue
        if (numberOfCitations == 0):
            print('PROBLEM: Citation not found.')
            report_file.write('PROBLEM: Citation not found.' '\n\n')
            report_file.write('No change made.' '\n\n')
            continue

        report_file.write("\nThe citation:\n" + FullCitationName +
                          "\n" "is currently found in source:\n" + OldSourceName + "\n\n")
        print("\nThe citation:\n" + FullCitationName +
              "\n" "is currently found in source:\n" + OldSourceName + "\n\n")

        # Deal with the new source
        new_source_name = input("\n\nEnter the name for the new source:\n")
        report_file.write("Source name as entered =" + new_source_name + "\n")

        SqlStmt = """
SELECT COUNT(), SourceID, TemplateID
  FROM SourceTable
 WHERE Name LIKE ( ? || '%' )
  """
        cur = db_connection.cursor()
        cur.execute(SqlStmt, (new_source_name, ))
        row = cur.fetchone()

        numfound = row[0]
        NewSourceID = row[1]
        NewSourceTemplateID = row[2]

        if (numfound > 1):
            print("PROBLEM: More than 1 source found." "\n\n")
            report_file.write("PROBLEM: More than 1 source found." "\n\n")
            report_file.write('No change made.' '\n\n')
            continue
        if (numfound == 0):
            print("PROBLEM: Source not found." "\n\n")
            report_file.write("PROBLEM: Source not found." "\n\n")
            report_file.write('No change made.' '\n\n')
            continue

        if (NewSourceID == OldSourceID):
            print(
                "PROBLEM: The citation is already using the specified new source." "\n\n")
            report_file.write(
                "PROBLEM: The citation is already using the specified new source." "\n\n")
            report_file.write('No change made.' '\n\n')
            continue

        if (NewSourceTemplateID != OldSourceTemplateID):
            print(
                "PROBLEM: The new source must be based on the same"
                " SourceTemplate as the current source." "\n\n")
            report_file.write(
                "PROBLEM: The new source must be based on the same"
                " SourceTemplate as the current source." "\n\n")
            report_file.write('No change made.' '\n')
            continue

        # update the citation to use the new source
        SqlStmt = """
UPDATE CitationTable
  SET  SourceID = ?
WHERE CitationID = ?
"""
        cur = db_connection.cursor()
        cur.execute(SqlStmt, (NewSourceID, CitationID))
        db_connection.commit()

        # Confirm update was successful

        SqlStmt = """
SELECT ct.CitationName, st.Name
  FROM SourceTable AS st
  JOIN CitationTable AS ct ON ct.SourceID = st.SourceID
 WHERE ct.CitationID = ?
"""

        cur = db_connection.cursor()
        cur.execute(SqlStmt, (CitationID, ))
        row = cur.fetchone()

        CitationName = row[0]
        SourceName = row[1]
        report_file.write("\n\n" "Confirmation of change\nCitation:\n" + CitationName
                          + "\n\n" "is now using source:\n" + SourceName + "\n")

    return 0

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
