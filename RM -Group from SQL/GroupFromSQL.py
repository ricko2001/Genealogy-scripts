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
# Call the "main" function
if __name__ == '__main__':
    main()

# ===================================================DIV60==
