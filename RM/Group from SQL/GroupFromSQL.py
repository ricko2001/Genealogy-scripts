import sys
from pathlib import Path
sys.path.append( str(Path.resolve(Path.cwd() / r'..\RM -RMpy package')))
import RMpy.launcher  # type: ignore
import RMpy.common as RMc  # type: ignore
from RMpy.common import q_str # type: ignore

import os


# Always make a database backup before using this script.

# Requirements:
#   RootsMagic database file
#   RM-Python-config.ini

# Tested with:
#   RootsMagic database file v10
#   Python for Windows v3.12

# Config files fields used
#    [FILE_PATHS]  REPORT_FILE_PATH
#    [FILE_PATHS]  REPORT_FILE_DISPLAY_APP
#    [FILE_PATHS]  DB_PATH
#    [FILE_PATHS]  RMNOCASE_PATH
#    [OPTIONS]     GROUP_NAME
#  note: GROUP_NAME may be a list of names, one per line.

#  note:Section name is the same label as [OPTIONS] GROUP_NAME's value
#    [GROUP_NAME_Value]  SQL_QUERY   the SQL to select group members


# ===================================================DIV60==
def main():

    # Configuration
    utility_info = {}
    utility_info["utility_name"]      = "GroupFromSQL" 
    utility_info["utility_version"]   = "1.3.2"
    # utility_info["utility_version"] = "APPLICATION_VERSION_NUMBER_RM_UTILS_OVERRIDE"
    utility_info["config_file_name"]  = "RM-Python-config.ini"
    utility_info["script_path"]  = Path(__file__).parent
    utility_info["run_features_function"]  = run_selected_features
    utility_info["allow_db_changes"]  = True
    utility_info["RMNOCASE_required"] = False
    utility_info["RegExp_required"]   = False

    RMpy.launcher.launcher(utility_info)

# ===================================================DIV60==
def run_selected_features(config, db_connection, report_file):

    RunSQLGroupFeature(config, db_connection, report_file)


# ===================================================DIV60==
def RunSQLGroupFeature(config, db_connection, report_file):

    try:
        group_name_list = config['OPTIONS'].get(
            'GROUP_NAME').split('\n')
    except:
        raise RMc.RM_Py_Exception(
            'section: [OPTIONS],  key: GROUP_NAME   not found.')

    for group_name in group_name_list:
        if group_name == '':
            continue
        try:
            config[group_name]
        except:
            raise RMc.RM_Py_Exception(
                f'section: [{q_str(group_name)}]   not found.')

    for group_name in group_name_list:
        if group_name == '':
            continue
        update_group(db_connection, config, report_file, group_name)

    return


# ===================================================DIV60==
def update_group(db_connection, config, report_file, group_name):

    GroupID = confirm_DB_group_name(group_name, report_file, db_connection)

    try:
        SQL_statement = config[group_name]['SQL_QUERY']
    except:
        raise RMc.RM_Py_Exception(
            f'section: [{q_str(group_name)}],  key: SQL_QUERY not found.')

    if SQL_statement == '':
        raise RMc.RM_Py_Exception(
            'section: [GROUP_NAME], key: SQL_QUERY No value entered. Nothing to do.')

    viewStmt = "DROP VIEW IF EXISTS PersonIdList_RJO_utils"
    try:
        cur = db_connection.cursor()
        cur.execute(viewStmt)
    except RMc.RM_Py_Exception as e:
        # database open issues don't appear until here !
        raise RMc.RM_Py_Exception(f'Cannot open the database.\n{str(e)}')

    # generate the SQL statement and create the view
    SqlStmt = "CREATE TEMP VIEW PersonIdList_RJO_utils AS " + SQL_statement
    try:
        cur = db_connection.cursor()
        cur.execute(SqlStmt)
    except:
        raise RMc.RM_Py_Exception(
            "ERROR: Creating a VIEW on SQL_QUERY returned an error. \n" +
            "SQL entered was:\n\n" + SQL_statement + "\n")

    # errors in SQL show up here, not in view creation
    try:
        SqlStmt = "select count() from PersonIdList_RJO_utils"
        cur = db_connection.cursor()
        cur.execute(SqlStmt)
        numInView = cur.fetchone()[0]
        report_file.write(
            str(numInView) + " persons selected by the SQL statement:\n")
    except:
        raise ("ERROR: SQL_QUERY returned an error when run as a VIEW. \n\n" +
               "SQL entered was:\n" + SQL_statement + "\n")

    report_file.write(SQL_statement + "\n\n\n")

    PopulateGroup(GroupID, db_connection)

    viewStmt = "DROP VIEW IF EXISTS PersonIdList_RJO_utils"
    cur = db_connection.cursor()
    cur.execute(viewStmt)


# ===================================================DIV60==
def confirm_DB_group_name(Name, report_file, db_connection):
    #  TagTable
    #   TagID=rowid
    #   TagType =0 for Groups
    #   TagName   duplicates not constrained

    Divider = "="*50 + "===DIV60=="
    report_file.write(f"{Divider}\n\n")

    # check how many groupNames with name and TagTape=0 already exist
    SqlStmt = """
SELECT count(*), TagValue 
FROM TagTable 
WHERE TagName=? COLLATE NOCASE AND TagType=0 COLLATE NOCASE
"""
    cur = db_connection.cursor()
    cur.execute(SqlStmt, (Name,))
    result = cur.fetchone()
    existingNumber = result[0]
    GroupID = result[1]

    if existingNumber > 1:
        raise RMc.RM_Py_Exception(f"\nERROR: Group: {q_str(Name)}  exists more than once in the database.\n"
                                  "Rename one of the duplicates. \n")

    if existingNumber == 1:
        report_file.write(f"Group: {q_str(Name)} will be updated. \n")

    else:  # existingNumber == 0
        raise RMc.RM_Py_Exception(
            f"\nERROR: Group: {q_str(Name)} does not exist in the database. \n")

    return GroupID


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
    except RMc.RM_Py_Exception:
        ('Cannot clear the group members. Close RM and try again.\n' + str(e))

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
        raise RMc.RM_Py_Exception(
            'Cannot populate group. Close RM and try again.\n' + str(e))

    return


# ===================================================DIV60==
# Call the "main" function
if __name__ == '__main__':
    main()

# ===================================================DIV60==
