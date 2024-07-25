import os
import sys
import sqlite3
from datetime import datetime
import configparser
import subprocess
import traceback

sys.path.append( r'..\\RM -RMpy package' )
import RMpy.launcher # type: ignore
import RMpy.common as RMc # type: ignore

# Always make a database backup before using this script.
# Runs one or two SQL statements on a database and returns results

# Requirements:
#   RootsMagic database file
#   RM-Python-config.ini
#   unifuzz64.dll (RMNOCASE collation) optionally needed depending on the SQL run

# Tested with:
#   RootsMagic database file v9.1.6
#   Python for Windows v3.12.3

# Config files fields used
#    FILE_PATHS  REPORT_FILE_PATH
#    FILE_PATHS  REPORT_FILE_DISPLAY_APP
#    FILE_PATHS  DB_PATH
#    FILE_PATHS  RMNOCASE_PATH
#    SQL  SQL_STATEMENT_1
#    SQL  SQL_STATEMENT_2

# ===================================================DIV60==
def main():

    # Configuration

    # Configuration
    config_file_name = "RM-Python-config.ini"
    allow_db_changes = True
    RMNOCASE_required = True
    RegExp_required = False

    RMpy.launcher.launcher(os.path.dirname(__file__),
                    config_file_name,
                    run_selected_features,
                    allow_db_changes,
                    RMNOCASE_required,
                    RegExp_required )


# ===================================================DIV60==
def run_selected_features(config, db_connection, report_file):
    RunSQLFeature(config, db_connection, report_file)


# ===================================================DIV60==
def RunSQLFeature(config, db_connection, report_file):

    try:
        SqlStmt = config['SQL']['SQL_STATEMENT_1']
    except:
        raise RMc.RM_Py_Exception(
            'ERROR: SQL - SQL_STATEMENT_1 must be specified.')

    # run the SQL statement
    cur = db_connection.cursor()
    cur.execute(SqlStmt)

    report_file.write("===============================================\n"
                      "The SQL that was run: \n\n" + SqlStmt
                      + "\n\n" "The results:" "\n\n")

    result = cur.fetchall()
    for row in result:
        report_file.write(str(row) + "\n")

    SqlStmt = None
    try:
        SqlStmt = config['SQL']['SQL_STATEMENT_2']
    except:
        pass

    if SqlStmt is not None:
        # run the second SQL statement
        cur = db_connection.cursor()
        cur.execute(SqlStmt)

        report_file.write("===============================================\n"
                          "The SQL that was run: \n\n"
                          + SqlStmt + "\n\nThe results:\n\n")

        result = cur.fetchall()
        for row in result:
            report_file.write(str(row) + "\n")

    return


# ===================================================DIV60==
# Call the "main" function
if __name__ == '__main__':
    main()

# ===================================================DIV60==
