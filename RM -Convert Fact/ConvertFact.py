import os
import sys
import sqlite3
from pathlib import Path
from datetime import datetime
import configparser
import subprocess
import traceback

# Convert all Facts of one fact type to another fact type
# A family event type, may be converted to an individual fact type.
# An individual type fact may *not* be converted to a family type.

# Tested with: RootsMagic v9.1.3
#              Python for Windows v3.12.2


# ===================================================DIV60==
def main():

    # Configuration
    ini_file_name = "RM-Python-config.ini"

    try:  # errors go to console window
        # ini file must be in "current directory" and encoded as UTF-8 (no BOM).
        # see   https://docs.python.org/3/library/configparser.html
        ini_file = os.path.join(get_current_directory(), ini_file_name)

        # Check that ini file is at expected path and that it is readable & valid.
        if not os.path.exists(ini_file):
            raise RMPyExcep("ERROR: The ini configuration file, " + ini_file_name
                            + " must be in the same directory as the .py or .exe file.\n\n")

        config = configparser.ConfigParser(empty_lines_in_values=False,
                                           interpolation=None)
        try:
            config.read(ini_file, 'UTF-8')
        except:
            raise RMPyExcep("ERROR: The " + ini_file_name
                            + " file contains a format error and cannot be parsed.\n\n")

        try:
            report_path = config['FILE_PATHS']['REPORT_FILE_PATH']
        except:
            raise RMPyExcep('ERROR: REPORT_FILE_PATH must be defined in the '
                            + ini_file_name + "\n\n")

        try:
            # Use UTF-8 encoding for the report file. Test for write-ability
            open(report_path,  mode='w', encoding='utf-8')
        except:
            raise RMPyExcep('ERROR: Cannot create the report file '
                            + report_path + "\n\n")

    except RMPyExcep as e:
        PauseWithMessage(e)
        return 1
    except Exception as e:
        traceback.print_exception(e, file=sys.stdout)
        PauseWithMessage("ERROR: Application failed. Please report.\n\n " + str(e))
        return 1

    # Open the Report File.
    report_file = open(report_path,  mode='w', encoding='utf-8')

    try:        # errors go to the report file
        try:
            database_path = config['FILE_PATHS']['DB_PATH']
        except:
            raise RMPyExcep('ERROR: DB_PATH must be specified.')
        if not os.path.exists(database_path):
            raise RMPyExcep('ERROR: Path for database not found: ' + database_path
                            + '\n\n' 'Absolute path checked:\n"'
                            + os.path.abspath(database_path) + '"')

        try:
            report_display_app = config['FILE_PATHS']['REPORT_FILE_DISPLAY_APP']
        except:
            report_display_app = None
        if report_display_app != None and not os.path.exists(report_display_app):
            raise RMPyExcep('ERROR: Path for report file display app not found: '
                            + report_display_app)

        try:
            facttype_current_name = config['MAPPING']['FACTTYPE_CURRENT']
        except:
            raise RMPyExcep('ERROR: FACTTYPE_CURRENT must be specified.')

        try:
            facttype_new_name = config['MAPPING']['FACTTYPE_NEW']
        except:
            raise RMPyExcep('ERROR: FACTTYPE_NEW must be specified.')

        try:
            role_name = config['MAPPING']['ROLE']
        except:
            raise RMPyExcep('ERROR: ROLE must be specified.')

        desc_sel = ''
        try:
            desc_sel = config['MAPPING']['DESC']
        except:
            pass

        date_sel = ''
        try:
            date_sel = config['MAPPING']['DATE']
        except:
            pass

        # RM database file info
        FileModificationTime = datetime.fromtimestamp(
            os.path.getmtime(database_path))

#        db_connection = create_db_connection(database_path, rmnocase_path)
        db_connection = create_db_connection(database_path, None)

        # write header to report file
        report_file.write("Report generated at      = " + TimeStampNow()
                          + "\n" "Database processed       = "
                          + os.path.abspath(database_path)
                          + "\n" "Database last changed on = "
                          + FileModificationTime.strftime("%Y-%m-%d %H:%M:%S")
                          + "\n" "SQLite library version   = "
                          + GetSQLiteLibraryVersion(db_connection) + "\n\n\n\n")

        report_file.write('FACTTYPE_CURRENT: "' + facttype_current_name + '"\n'
                          + '    FACTTYPE_NEW: "' + facttype_new_name + '"\n')
        if role_name != '':
            report_file.write('            ROLE: "' + role_name + '"\n')
        if desc_sel != '':
            report_file.write('            DESC: "' + desc_sel + '"\n')
        if date_sel != '':
            report_file.write('            DATE: "' + date_sel + '"\n')
        report_file.write('\n\n\n')

        out_tuple = lookup_validate(
            facttype_current_name, facttype_new_name,
            role_name, db_connection, report_file)

        convert_fact(out_tuple, desc_sel, date_sel, db_connection, report_file)

    except RMPyExcep as e:
        report_file.write(str(e))
        return 1
    except Exception as e:
        traceback.print_exception(e, file=report_file)
        report_file.write("\n\n"
                          "ERROR: Application failed. Please email report file to author. ")
        return 1
    finally:
        db_connection.commit()
        db_connection.close()
        report_file.close()
        if report_display_app != None:
            subprocess.Popen([report_display_app, report_path])
    return 0


# ===================================================DIV60==
def lookup_validate(facttype_curr_name, facttype_new_name, role_name, dbConnection, reportF):

    # confirm fact type names are unique and of correct type
    SqlStmt = """
SELECT FactTypeID, OwnerType
  FROM FactTypeTable ftt
 WHERE ftt.Name = ? COLLATE NOCASE
"""
    cur = dbConnection.cursor()
    cur.execute(SqlStmt, (facttype_curr_name,))
    rows = cur.fetchall()
    if len(rows) == 0:
        raise RMPyExcep(
            "ERROR: The entered Current FactType name could not be found.\n")
    if len(rows) > 1:
        raise RMPyExcep(
            "ERROR: The entered Current FactType name is not unique. Fix this.\n")
    facttype_curr_id = rows[0][0]
    facttype_is_family_curr = False
    if rows[0][1] == 1:
        facttype_is_family_curr = True
        reportF.write("'Current FactType' is of type 'FAMILY'.\n\n\n")

    cur = dbConnection.cursor()
    cur.execute(SqlStmt, (facttype_new_name,))
    rows = cur.fetchall()
    if len(rows) == 0:
        raise RMPyExcep(
            "ERROR: The entered New FactType name could not be found.\n")
    if len(rows) > 1:
        raise RMPyExcep(
            "ERROR: The entered New FactType name is not unique. Fix this.\n")
    facttype_new_id = rows[0][0]
    facttype_is_family_new = False
    if rows[0][1] == 1:
        facttype_is_family_new = True
        reportF.write("New FactType name is of type FAMILY.\n\n\n")

    role_id = 0
    if facttype_is_family_curr and not facttype_is_family_new:
        # need to use role name for the new witness
        SqlStmt = """
SELECT RoleID, EventType
  FROM RoleTable rt
 WHERE rt.RoleName = ? COLLATE NOCASE
   AND rt.EventType = ?
"""
        cur = dbConnection.cursor()
        cur.execute(SqlStmt, (role_name, facttype_new_id))
        rows = cur.fetchall()
        if len(rows) == 0:
            raise RMPyExcep(
                "The entered Role name could not be found associated with the new fact type.\n")
        if len(rows) > 1:
            raise RMPyExcep(
                "The entered Role name is not unique for the new fact type. Fix this.\n")
        role_id = rows[0][0]


    # All of the roles used by the old fact must also appear in the new fact
    # List Roles that user needs to create for the new Fact Type
    SqlStmt = """
SELECT DISTINCT RoleID, RoleName  COLLATE NOCASE
      FROM RoleTable AS rt
INNER JOIN WitnessTable AS wt ON wt.Role = rt.RoleID
INNER JOIN EventTable   AS et ON et.EventID = wt.EventID
INNER JOIN FactTypeTable AS ftt ON et.EventType = ftt.FactTypeID
      WHERE ftt.FactTypeID = :curr_FTid  --OldFactType
        AND RoleName  COLLATE NOCASE NOT IN (
            SELECT RoleName
              FROM RoleTable rt
              WHERE EventType = :new_FTid )  -- NewFactType
"""
    cur = dbConnection.cursor()
    cur.execute(SqlStmt, {"curr_FTid": facttype_curr_id,
                "new_FTid": facttype_new_id})
    rows = cur.fetchall()
    if len(rows) != 0:
        reportF.write("The following Roles are in use by the Current Fact Type,\n"
                      + "but do not exist for the New Fact Type.\n"
                      + "They will either need to be defined for the new Fact Type\n"
                      + "or eliminated from use by the Current Fact type.\n"
                      + "Coordinating the roles may be accomplished by altering the\n"
                      + "Role Names. This must be done before Fact conversion\n"
                      + "can be performed.\n\n\n"
                      + "--Missing Roles:--\n")
        for row in rows:
            reportF.write(str(row[1]) + "\n")
        reportF.write("\n\n\n")
        raise RMPyExcep(
            "ERROR: Roles need to be coordinated between the Current and New Fact Types.\n")

    return (facttype_curr_id, facttype_new_id, role_id, facttype_is_family_curr,
             facttype_is_family_new)


# ===================================================DIV60==
def convert_fact(input_tuple,  desc_sel, date_sel, db_connection, report_file):

    facttype_cur_id = input_tuple[0]
    facttype_new_id = input_tuple[1]
    roleID = input_tuple[2]
    facttype_is_fam_cur = input_tuple[3]
    facttype_is_fam_new = input_tuple[4]

    list_of_fact_id = getListOfEventsToConvert(
        facttype_cur_id, facttype_is_fam_cur, desc_sel, date_sel, db_connection)
    if len(list_of_fact_id) == 0:
        raise RMPyExcep("Nothing to convert !\n\n")
    report_file.write("Number of facts found to convert: "
                      + str(len(list_of_fact_id)) + '\n\n')
    if facttype_is_fam_cur and not facttype_is_fam_new:
        report_file.write(
            "Facts attached to these families were converted:\n  Father ID:   Mother ID: ")
        for fact_to_convert in list_of_fact_id:
            FamID = getFamilyIDfromEvent(fact_to_convert, db_connection)
            FatherMother = getFatherMotherIDs(FamID, db_connection)
            FatherID = FatherMother[0]
            MotherID = FatherMother[1]
            report_file.write("\n    " + str(FatherID) +
                              "           " + str(MotherID))
            if FatherID != 0:
                changeTheEvent(fact_to_convert, FatherID,
                               facttype_new_id, db_connection)
            elif FatherID == 0 and MotherID != 0:
                changeTheEvent(fact_to_convert, MotherID,
                               facttype_new_id, db_connection)
            else:
                raise RMPyExcep("ERROR: Internal, found a 0,0 family")
            updateRoleInExistingWitnesses(
                fact_to_convert, facttype_new_id, db_connection)
            if MotherID != 0:
                addNewWitness(fact_to_convert, MotherID, roleID, db_connection)
    elif facttype_is_fam_cur and facttype_is_fam_new:
        report_file.write(
            "Facts attached to these families were converted:\n  Father ID:   Mother ID: ")
        for fact_to_convert in list_of_fact_id:
            FamID = getFamilyIDfromEvent(fact_to_convert, db_connection)
            FatherMother = getFatherMotherIDs(FamID, db_connection)
            FatherID = FatherMother[0]
            MotherID = FatherMother[1]
            report_file.write("\n    " + str(FatherID) +
                              "           " + str(MotherID))
            changeTheEvent(fact_to_convert, FatherID,
                           facttype_new_id, db_connection)
            updateRoleInExistingWitnesses(
                fact_to_convert, facttype_new_id, db_connection)
    elif not facttype_is_fam_cur and not facttype_is_fam_new:
        report_file.write(
            "Facts attached to these Persons (ID) were converted:")
        for fact_to_convert in list_of_fact_id:
            person_id = getPersonIDfromEventID(fact_to_convert, db_connection)
            report_file.write("\n  " + str(person_id))
            changeTheEvent(fact_to_convert, person_id,
                           facttype_new_id, db_connection)
            updateRoleInExistingWitnesses(
                fact_to_convert, facttype_new_id, db_connection)
    else:
        raise RMPyExcep("ERROR: Internal. Fact P-F type combo not supported.")
    return


# ===================================================DIV60==
def updateRoleInExistingWitnesses(FactToConvert, FactTypeID_new, dbConnection):

    # List of all Witness records that need their role updated
    SqlStmt = """
SELECT wt.WitnessID, rt.RoleName
  FROM WitnessTable AS wt
INNER JOIN RoleTable AS rt ON rt.RoleID = wt.Role
      WHERE wt.EventID = :FactId
  ORDER BY rt.RoleName  COLLATE NOCASE
"""
    cur = dbConnection.cursor()
    cur.execute(SqlStmt, {"FactId": FactToConvert})
    rows = cur.fetchall()

    # each row is a witness record
    for row in rows:
        WitnessToUpdate = row[0]
        RolNameToUse = row[1]

        SqlStmt = """
  SELECT RoleID
    FROM RoleTable
   WHERE EventType = :new_FTid
     AND RoleName = :RoleName COLLATE NOCASE
  """
        cur = dbConnection.cursor()
        cur.execute(SqlStmt, {"new_FTid": FactTypeID_new,
                              "RoleName": RolNameToUse})
        row = cur.fetchone()
        newRoleID = row[0]

        SqlStmt = """
  UPDATE WitnessTable
     SET Role = :RoleID,
         UTCModDate = julianday('now') - 2415018.5
   WHERE WitnessID = :WitnessID
  """
        cur = dbConnection.cursor()
        cur.execute(
            SqlStmt, {"WitnessID": WitnessToUpdate, 
                         "RoleID": newRoleID})
        row = cur.fetchone()
    return


# ===================================================DIV60==
def getPersonIDfromEventID(ID, dbConn):

    SqlStmt = """
SELECT OwnerID
  FROM EventTable
 WHERE EventID = ?
"""
    cur = dbConn.cursor()
    cur.execute(SqlStmt, (ID,))
    row = cur.fetchone()
    return row[0]


# ===================================================DIV60==
def getFamilyIDfromEvent(ID, dbConn):

    SqlStmt = """
SELECT OwnerID
  FROM EventTable et
WHERE  et.EventID = ?
"""
    cur = dbConn.cursor()
    cur.execute(SqlStmt, (ID,))
    rows = cur.fetchall()

    if (len(rows) != 1):
        raise RMPyExcep("More than one owner ID found")
    return rows[0][0]


# ===================================================DIV60==
def getListOfEventsToConvert(ID, FamilyType, desc_sel, date_sel, dbConn):

    OwnerType = 0
    if FamilyType:
        OwnerType = 1

    if desc_sel != '' and date_sel == '':
        SqlStmt = """
SELECT EventID
  FROM EventTable et
 WHERE et.EventType = ?
   AND et.OwnerType = ?
   AND et.Details LIKE (?)
 ORDER BY OwnerID
"""
        cur = dbConn.cursor()
        cur.execute(SqlStmt, (ID, OwnerType, desc_sel))
    elif desc_sel == '' and date_sel != '':
        SqlStmt = """
SELECT EventID
  FROM EventTable et
 WHERE et.EventType = ?
   AND et.OwnerType = ?
   AND SUBSTR(et.Date,4,4) = ?
 ORDER BY OwnerID
"""
        cur = dbConn.cursor()
        cur.execute(SqlStmt, (ID, OwnerType, date_sel))
    elif desc_sel == '' and date_sel == '':
        SqlStmt = """
SELECT EventID
  FROM EventTable et
 WHERE et.EventType = ?
   AND et.OwnerType = ?
 ORDER BY OwnerID
"""
        cur = dbConn.cursor()
        cur.execute(SqlStmt, (ID, OwnerType))
    elif desc_sel != '' and date_sel != '':
        SqlStmt = """
SELECT EventID
  FROM EventTable et
 WHERE et.EventType = ?
   AND et.OwnerType = ?
   AND SUBSTR(et.Date,4,4) = ?
   AND et.Details LIKE (?)
 ORDER BY OwnerID
"""
        cur = dbConn.cursor()
        cur.execute(SqlStmt, (ID, OwnerType, date_sel, desc_sel))
    else:
        raise RMPyExcep('Combo search terms not supported')

    rows = cur.fetchall()
    listOfFactIDs = []
    for x in range(len(rows)):
        listOfFactIDs.append(rows[x][0])
    return listOfFactIDs


# ===================================================DIV60==
def getFatherMotherIDs(ID, dbConn):

    SqlStmt = """
SELECT FatherID, MotherID
  FROM FamilyTable ft
 WHERE ft.FamilyID = ?
"""
    cur = dbConn.cursor()
    cur.execute(SqlStmt, (ID,))
    rows = cur.fetchall()

    if (len(rows) != 1):
        raise RMPyExcep("More than one row returned getting family id")
    return rows[0]


# ===================================================DIV60==
def changeTheEvent(EventID, OwnerID, newEventTypeID, dbConn):

    SqlStmt = """
UPDATE EventTable
   SET OwnerType = 0,
       EventType= ?,
       OwnerID = ?
 WHERE EventID = ?
"""
    cur = dbConn.cursor()
    cur.execute(SqlStmt, (newEventTypeID, OwnerID, EventID))
    return


# ===================================================DIV60==
def addNewWitness(EventID, OwnerID, RoleID, dbConn):

    SqlStmt = """
INSERT INTO WitnessTable
  ( EventID, PersonID, Role, UTCModDate)
  VALUES ( ?, ?, ?, julianday('now') - 2415018.5 )
"""
    cur = dbConn.cursor()
    cur.execute(SqlStmt, (EventID, OwnerID, RoleID))
    return


# ===================================================DIV60==
def create_db_connection(db_file_path, db_extension):

    dbConnection = None
    try:
        dbConnection = sqlite3.connect(db_file_path)
        if db_extension is not None:
            # load SQLite extension
            dbConnection.enable_load_extension(True)
            dbConnection.load_extension(db_extension)
    except Exception as e:
        raise RMPyExcep(e, "\n\n" "Cannot open the RM database file." "\n")
    return dbConnection


# ===================================================DIV60==
def PauseWithMessage(message=None):

    if (message != None):
        print(str(message))
    input("\n" "Press the <Enter> key to continue...")
    return


# ===================================================DIV60==
def TimeStampNow(type=""):

    # return a TimeStamp string
    now = datetime.now()
    if type == '':
        dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
    elif type == 'file':
        dt_string = now.strftime("%Y-%m-%d_%H%M%S")
    return dt_string


# ===================================================DIV60==
def GetSQLiteLibraryVersion(dbConnection):

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
class RMPyExcep(Exception):

    '''Exceptions thrown for configuration/database issues'''


# ===================================================DIV60==
# Call the "main" function
if __name__ == '__main__':
    main()

# ===================================================DIV60==
