import os
import sys
from datetime import datetime

sys.path.append( r'..\\RM -RMpy package' )
import RMpy.launcher # type: ignore
import RMpy.common as RMc # type: ignore

# Always make a database backup before using this script.

# Requirements:
#   RootsMagic database file
#   RM-Python-config.ini

# Tested with: 
#   RootsMagic database file v10.0.1
#   Python for Windows v3.12.3

# Config files fields used
#    [FILE_PATHS]  REPORT_FILE_PATH
#    [FILE_PATHS]   REPORT_FILE_DISPLAY_APP
#    [FILE_PATHS]  DB_PATH
#    [FILE_PATHS]  RMNOCASE_PATH
#
#    [OPTIONS]     GROUP_NAME

#  note:Section name is the same label as [OPTIONS] GROUP_NAME's value
#    [GROUP_NAME_Value]  SQL_QUERY   the SQL to select group members


# ===================================================DIV60==
def main():

    # Configuration
    config_file_name = "RM-Python-config.ini"
    allow_db_changes = True
    RMNOCASE_required = False
    RegExp_required = False

    RMpy.launcher.launcher(os.path.dirname(__file__),
                    config_file_name,
                    run_selected_features,
                    allow_db_changes,
                    RMNOCASE_required,
                    RegExp_required )


# ===================================================DIV60==
def run_selected_features(config, db_connection, report_file):

    RunSQLGroupFeature(config, db_connection, report_file)


# ===================================================DIV60==
def RunSQLGroupFeature(config, db_connection, report_file):

    try:
        group_name = config['OPTIONS']['GROUP_NAME']
    except:
        raise RMc.RM_Py_Exception(
            'section: [OPTIONS],  key: GROUP_NAME   not found.')
    try:
        config[group_name]
    except:
        raise RMc.RM_Py_Exception(
            'section: [' + group_name + ']   not found.')
    try:
        SQL_statement =config[group_name]['SQL_QUERY']
    except:
        raise RMc.RM_Py_Exception(
            'section: [' + group_name + '],  key: SQL_QUERY   not found.')


    viewStmt = "DROP VIEW IF EXISTS PersonIdList_RJO_utils"
    try:
        cur = db_connection.cursor()
        cur.execute(viewStmt)
    except RMc.RM_Py_Exception as e:
        # database open issues don't appear until here !
        raise RMc.RM_Py_Exception(
            'Cannot open the database.\n' + str(e))

    if group_name == '':
        raise RMc.RM_Py_Exception(
            'section: [OPTIONS], key: group_name \n' +
            'No value entered.\n Nothing to do.')
    
    if SQL_statement == '':
        raise RMc.RM_Py_Exception(
            'section: [GROUP_NAME], key: SQL_QUERY \n' +
            'No value entered.\n Nothing to do.')


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
        report_file.write("# of persons selected: " + str(numInView) + "\n")
    except:
        raise ("ERROR: SQL_QUERY returned an error when run as a VIEW. \n\n" +
               "SQL entered was:\n" + SQL_statement + "\n")

    GroupID = ConfirmGroup(group_name, report_file, db_connection)

    PopulateGroup(GroupID, db_connection)

    report_file.write("\nSQL used to specify group membership:\n\n" + SQL_statement)

    viewStmt = "DROP VIEW IF EXISTS PersonIdList_RJO_utils"
    cur = db_connection.cursor()
    cur.execute(viewStmt)

    return


# ===================================================DIV60==
def ConfirmGroup(Name, report_file, db_connection):
    #  TagTable
    #   TagID=rowid
    #   TagType =0 for Groups
    #   TagName   duplicates not constrained

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
        raise RMc.RM_Py_Exception("\nERROR: Group: " + Name +
              " already exists more than once.\n Use a different name, or rename one of them. \n")

    if existingNumber == 1:
        report_file.write("\nINFO: Group: " + Name +
              " exists and will be updated. \n")

    else:  # existingNumber == 0
        raise RMc.RM_Py_Exception("\nINFO: Group: " 
            + Name + " does not exist in the database. \n")

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
    except RMc.RM_Py_Exception: (
        'Cannot clear the group members. Close RM and try again.\n' + str(e))

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
