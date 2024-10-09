import sys
sys.path.append(r'..\RM -RMpy package')
import RMpy.launcher  # type: ignore
import RMpy.common as RMc  # type: ignore
from RMpy.common import q_str # type: ignore

import os

# Always make a database backup before using this script.
# Runs SQL statements on a database and returns results

# Requirements:
#   RootsMagic database file
#   RM-Python-config.ini
#   unifuzz64.dll (RMNOCASE collation) optionally needed depending on the SQL run

# Tested with:
#   RootsMagic database file v10
#   Python for Windows v3.12.3

# Config files fields used
#    FILE_PATHS  DB_PATH
#    FILE_PATHS  RMNOCASE_PATH
#    FILE_PATHS  REPORT_FILE_PATH
#    FILE_PATHS  REPORT_FILE_DISPLAY_APP
#    SQL  SQL_STATEMENT_1
#    SQL  SQL_STATEMENT_99

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
                           RegExp_required)


# ===================================================DIV60==
def run_selected_features(config, db_connection, report_file):
    RunSQLFeature(config, db_connection, report_file)


# ===================================================DIV60==
def RunSQLFeature(config, db_connection, report_file):

    Divider = "="*60 + "===DIV70=="

    try:
        config['SQL']['SQL_STATEMENT_1']
    except:
        raise RMc.RM_Py_Exception(
            'ERROR: SQL - SQL_STATEMENT_1 must be specified.')

    for n in range(1, 99):
        key_name = "SQL_STATEMENT_" + str(n)
        try:
            sql_stmt = config['SQL'][key_name]
        except:
            break

        report_file.write(
            f"\n{Divider}"
            f"\nThe SQL that was run for {key_name}: \n\n{sql_stmt}"
            f"\n\nThe results:\n\n")

        try:
            # run the SQL statement
            cur = db_connection.cursor()
            cur.execute(sql_stmt)

            result = cur.fetchall()
            for row in result:
                report_file.write(str(row) + "\n")
        except Exception as e:
            raise RMc.RM_Py_Exception(
                f"\nERROR: Cannot run the SQL.\n\n{str(e)}\n\n{Divider}\n")

    report_file.write(f"\n{Divider}\n")
    return


# ===================================================DIV60==
# Call the "main" function
if __name__ == '__main__':
    main()

# ===================================================DIV60==
