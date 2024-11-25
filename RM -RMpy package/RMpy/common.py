import sys
import sqlite3
from pathlib import Path
from datetime import datetime


# ===================================================DIV60==
def create_db_connection(db_file_path, db_extension_file_path_list):

    dbConnection = None
    try:
        dbConnection = sqlite3.connect(db_file_path)
        if db_extension_file_path_list is not None:
            dbConnection.enable_load_extension(True)
            # load SQLite extensions
            for extension in db_extension_file_path_list:
                dbConnection.load_extension(extension)
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
def reindex_RMNOCASE(dbConnection):

    SqlStmt = "REINDEX RMNOCASE"
    cur = dbConnection.cursor()
    cur.execute(SqlStmt)

# ===================================================DIV60==
def time_stamp_now(type=None):

    # return a TimeStamp string
    now = datetime.now()
    if type is None:
        dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
    elif type == 'file':
        dt_string = now.strftime("%Y-%m-%d_%H%M%S")
    return dt_string


# ===================================================DIV60==
def reindex_RMNOCASE(dbConnection):
    SqlStmt = """
REINDEX RMNOCASE
"""
    cur = dbConnection.cursor()
    cur.execute(SqlStmt, ())

    
# ===================================================DIV60==
def q_str(in_str):
    return '"' + str(in_str) + '"'


# ===================================================DIV60==
def pause_with_message(message=None):

    if (message != None):
        print(str(message))
    input("\n" "Press the <Enter> key to continue...")
    return

# ===================================================DIV60==
def get_current_directory(script_path: Path) ->Path:

    # Determine if application is a script file or frozen exe and get its directory
    # see   https://pyinstaller.org/en/stable/runtime-information.html
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        application_path = sys.executable.parent()
    else:
        application_path = script_path
    return application_path


# ===================================================DIV60==
class RM_Py_Exception(Exception):

    '''Exceptions thrown for configuration/database issues'''

# ===================================================DIV60==

