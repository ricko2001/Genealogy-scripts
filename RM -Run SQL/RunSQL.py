import sys
from pathlib import Path
sys.path.append( str(Path.resolve(Path.cwd() / r'..\RM -RMpy package')))
import RMpy.launcher  # type: ignore
import RMpy.common as RMc  # type: ignore
from RMpy.common import q_str # type: ignore

import os

# Requirements:
#   RootsMagic database file
#   RM-Python-config.ini
#   unifuzz64.dll (RMNOCASE collation) optionally needed depending on the SQL run

# Tested with:
#   RootsMagic database file v10
#   Python for Windows v3.13

# Config files fields used
#    FILE_PATHS  DB_PATH
#    FILE_PATHS  RMNOCASE_PATH
#    FILE_PATHS  REPORT_FILE_PATH
#    FILE_PATHS  REPORT_FILE_DISPLAY_APP
#    SQL  SQL_STATEMENT_1
#    SQL  SQL_STATEMENT_99
#    SQL  SQL_SCRIPT_1
#    SQL  SQL_SCRIPT_99

# ===================================================DIV60==
def main():

    # Configuration
    utility_info = {}
    utility_info["utility_name"]      = "RunSQL" 
    utility_info["utility_version"]   = "1.2.1"
    # utility_info["utility_version"] = "APPLICATION_VERSION_NUMBER_RM_UTILS_OVERRIDE"
    utility_info["config_file_name"]  = "RM-Python-config.ini"
    utility_info["script_path"]  = Path(__file__).parent
    utility_info["run_features_function"]  = run_selected_features
    utility_info["allow_db_changes"]  = True
    utility_info["RMNOCASE_required"] = True
    utility_info["RegExp_required"]   = False

    RMpy.launcher.launcher(utility_info)


# ===================================================DIV60==
def run_selected_features(config, db_connection, report_file):
    RunSQLFeature(config, db_connection, report_file)


# ===================================================DIV60==
def RunSQLFeature(config, db_connection, report_file):

    Divider = "="*60 + "===DIV70=="

#   First run the SQL statements
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

#   Next run the SQL scripts
    for n in range(1, 99):
        key_name = "SQL_SCRIPT_" + str(n)
        try:
            sql_file = config['SQL'][key_name]
        except:
            break

        if not os.path.exists(sql_file):
            raise RMc.RM_Py_Exception(
                f"ERROR: The SQL script file: {sql_file} cannot be found.\n\n")

        with open(sql_file, 'r') as file_h:
            sql_script_text = file_h.read()

        try:
            # run the SQL script
            cur = db_connection.cursor()
            cur.executescript(sql_script_text)
        except Exception as e:
            raise RMc.RM_Py_Exception(
                f"\nERROR: Cannot run the SQL script.\n\n{str(e)}\n\n{Divider}\n")

        report_file.write(
            f"\n{Divider}"
            f"\nThe SQL file run for {key_name}: {sql_file}"
            f"\nNo results are displayed from scripts.\nThe script did not generate an error message.\n\n" )

    report_file.write(f"\n{Divider}\n")
    return


# ===================================================DIV60==
# Call the "main" function
if __name__ == '__main__':
    main()

# ===================================================DIV60==
