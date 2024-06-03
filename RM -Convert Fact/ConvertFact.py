import os
import sys
import sqlite3
from datetime import datetime
import configparser
import subprocess
import traceback

# Convert all Facts of one fact type to another fact type
# A family event type, may be converted to an individual fact type.
# An individual type fact may *not* be converted to a family type.

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
#
#    MAPPING     FACTTYPE_CURRENT
#    MAPPING     FACTTYPE_NEW
#    MAPPING     ROLE
#    MAPPING     DESC
#    MAPPING     DATE


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

    convert_fact(config, db_connection, report_file)


# ===================================================DIV60==
def convert_fact(config, db_connection, report_file):

    role_name = None
    desc_sel = None
    date_sel = None

    try:
        facttype_current_name = config['MAPPING']['FACTTYPE_CURRENT']
    except:
        raise RM_Py_Exception('ERROR: FACTTYPE_CURRENT must be specified.')
    try:
        facttype_new_name = config['MAPPING']['FACTTYPE_NEW']
    except:
        raise RM_Py_Exception('ERROR: FACTTYPE_NEW must be specified.')

    try:
        role_name = config['MAPPING']['ROLE']
    except:
        pass
    try:
        desc_sel = config['MAPPING']['DESC']
    except:
        pass
    try:
        date_sel = config['MAPPING']['DATE']
    except:
        pass

    report_file.write('FACTTYPE_CURRENT: "' + facttype_current_name + '"\n'
                      + '    FACTTYPE_NEW: "' + facttype_new_name + '"\n')
    if role_name is not None:
        report_file.write('            ROLE: "' + role_name + '"\n')
    if desc_sel is not None:
        report_file.write('            DESC: "' + desc_sel + '"\n')
    if date_sel is not None:
        report_file.write('            DATE: "' + date_sel + '"\n')
    report_file.write('\n')

    return_tuple = lookup_and_validate(facttype_current_name, facttype_new_name,
                                       role_name, db_connection, report_file)

    facttype_cur_id = return_tuple[0]
    facttype_new_id = return_tuple[1]
    roleID = return_tuple[2]
    facttype_is_fam_cur = return_tuple[3]
    facttype_is_fam_new = return_tuple[4]

    list_of_fact_id = get_list_of_events_to_convert(
        facttype_cur_id, facttype_is_fam_cur, desc_sel, date_sel, db_connection)
    if len(list_of_fact_id) == 0:
        raise RM_Py_Exception("Nothing to convert !\n\n")
    report_file.write("Number of facts found to convert: "
                      + str(len(list_of_fact_id)) + '\n\n')
    if facttype_is_fam_cur and not facttype_is_fam_new:
        report_file.write(
            "Facts attached to these families were converted:\n"
            "  Father ID:   Mother ID: ")
        for fact_to_convert in list_of_fact_id:
            FamID = get_FamilyID_from_EventID(fact_to_convert, db_connection)
            FatherMother = get_father_mother_IDs(FamID, db_connection)
            FatherID = FatherMother[0]
            MotherID = FatherMother[1]
            report_file.write("\n    " + str(FatherID) +
                              "           " + str(MotherID))
            if FatherID != 0:
                change_the_event(fact_to_convert, FatherID,
                                 facttype_new_id, facttype_is_fam_new,
                                 db_connection)
            elif FatherID == 0 and MotherID != 0:
                change_the_event(fact_to_convert, MotherID,
                                 facttype_new_id, facttype_is_fam_new,
                                 db_connection)
            else:
                raise RM_Py_Exception(
                    "ERROR: Internal, found a empty 0,0 family")
            update_role_in_existing_witnesses(
                fact_to_convert, facttype_new_id, db_connection)
            if MotherID != 0:
                add_new_witness(fact_to_convert, MotherID,
                                roleID, db_connection)
    elif facttype_is_fam_cur and facttype_is_fam_new:
        report_file.write(
            "Facts attached to these families were converted:\n"
            "  Father ID:   Mother ID: ")
        for fact_to_convert in list_of_fact_id:
            FamID = get_FamilyID_from_EventID(fact_to_convert, db_connection)
            FatherMother = get_father_mother_IDs(FamID, db_connection)
            FatherID = FatherMother[0]
            MotherID = FatherMother[1]
            report_file.write("\n    " + str(FatherID) +
                              "           " + str(MotherID))
            change_the_event(fact_to_convert, FatherID,
                             facttype_new_id, facttype_is_fam_new,
                             db_connection)
            update_role_in_existing_witnesses(
                fact_to_convert, facttype_new_id, db_connection)
    elif not facttype_is_fam_cur and not facttype_is_fam_new:
        report_file.write(
            "Facts attached to these Persons (ID) were converted:")
        for fact_to_convert in list_of_fact_id:
            person_id = get_PersonID_from_EventID(
                fact_to_convert, db_connection)
            report_file.write("\n  " + str(person_id))
            change_the_event(fact_to_convert, person_id,
                             facttype_new_id, facttype_is_fam_new,
                             db_connection)
            update_role_in_existing_witnesses(
                fact_to_convert, facttype_new_id, db_connection)
    else:
        raise RM_Py_Exception(
            "ERROR: Internal. Fact P>F type combo not supported.")
    return


# ===================================================DIV60==
def lookup_and_validate(facttype_curr_name, facttype_new_name,
                        role_name, db_connection, report_file):

    # confirm fact type names are unique and of correct type
    SqlStmt = """
SELECT FactTypeID, OwnerType
  FROM FactTypeTable ftt
 WHERE ftt.Name = ? COLLATE NOCASE
"""
    cur = db_connection.cursor()
    cur.execute(SqlStmt, (facttype_curr_name,))
    rows = cur.fetchall()
    if len(rows) == 0:
        raise RM_Py_Exception(
            "ERROR: The entered Current FactType name could not be found.\n")
    if len(rows) > 1:
        raise RM_Py_Exception(
            "ERROR: The entered Current FactType name is not unique. Fix this.\n")
    facttype_curr_id = rows[0][0]
    if rows[0][1] == 1:
        facttype_is_family_curr = True
        report_file.write("FACTTYPE_CURRENT kind is 'FAMILY'.\n")
    else:
        facttype_is_family_curr = False
        report_file.write("FACTTYPE_CURRENT kind is 'PERSONAL'.\n")

    cur = db_connection.cursor()
    cur.execute(SqlStmt, (facttype_new_name,))
    rows = cur.fetchall()
    if len(rows) == 0:
        raise RM_Py_Exception(
            "ERROR: The entered New Fact Type name could not be found.\n")
    if len(rows) > 1:
        raise RM_Py_Exception(
            "ERROR: The entered New Fact Type name is not unique. Fix this.\n")
    facttype_new_id = rows[0][0]
    if rows[0][1] == 1:
        facttype_is_family_new = True
        report_file.write("FACTTYPE_NEW kind is 'FAMILY'.\n\n\n")
    else:
        facttype_is_family_new = False
        report_file.write("FACTTYPE_NEW kind is 'PERSONAL'.\n\n\n")

    role_id = 0
    if facttype_is_family_curr and not facttype_is_family_new:
        # need to use role name for the new witness
        if role_name is None:
            raise RM_Py_Exception('ERROR: ROLE must be specified'
                                  ' for this conversion.')
        SqlStmt = """
SELECT RoleID, EventType
  FROM RoleTable rt
 WHERE rt.RoleName = ? COLLATE NOCASE
   AND rt.EventType = ?
"""
        cur = db_connection.cursor()
        cur.execute(SqlStmt, (role_name, facttype_new_id))
        rows = cur.fetchall()
        if len(rows) == 0:
            raise RM_Py_Exception(
                "ERROR: The entered Role name could not be found"
                " associated with the new fact type.\n")
        if len(rows) > 1:
            raise RM_Py_Exception(
                "The entered Role name is not unique for the new"
                " fact type. Fix this.\n")
        role_id = rows[0][0]

    # All of the roles used by the old facts must also appear in the
    # new fact type.
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
    cur = db_connection.cursor()
    cur.execute(SqlStmt, {"curr_FTid": facttype_curr_id,
                "new_FTid": facttype_new_id})
    rows = cur.fetchall()
    if len(rows) != 0:
        report_file.write("The following Roles are in use by the Current"
                          " Fact Type,\n"
                          + "but do not exist for the New Fact Type.\n"
                          + "They will either need to be defined for"
                          " the new Fact Type\n"
                          + "or eliminated from use by the Current Fact type.\n"
                          + "Coordinating the roles may be accomplished"
                          " by altering the\n"
                          + "Role Names. This must be done before fact type\n"
                          + "conversion can be performed.\n\n\n"
                          + "--Missing Roles:--\n")
        for row in rows:
            report_file.write(str(row[1]) + "\n")
        report_file.write("\n\n\n")
        raise RM_Py_Exception(
            "ERROR: Roles need to be coordinated between the Current and New Fact Types.\n")

    return (facttype_curr_id, facttype_new_id, role_id, facttype_is_family_curr,
            facttype_is_family_new)


# ===================================================DIV60==
def update_role_in_existing_witnesses(FactToConvert, FactTypeID_new, db_connection):

    # List of all Witness records that need their role updated
    SqlStmt = """
SELECT wt.WitnessID, rt.RoleName
  FROM WitnessTable AS wt
INNER JOIN RoleTable AS rt ON rt.RoleID = wt.Role
      WHERE wt.EventID = :FactId
  ORDER BY rt.RoleName  COLLATE NOCASE
"""
    cur = db_connection.cursor()
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
        cur = db_connection.cursor()
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
        cur = db_connection.cursor()
        cur.execute(
            SqlStmt, {"WitnessID": WitnessToUpdate,
                      "RoleID": newRoleID})
        row = cur.fetchone()
    return


# ===================================================DIV60==
def get_PersonID_from_EventID(ID, db_connection):

    SqlStmt = """
SELECT OwnerID
  FROM EventTable
 WHERE EventID = ?
"""
    cur = db_connection.cursor()
    cur.execute(SqlStmt, (ID,))
    row = cur.fetchone()
    return row[0]


# ===================================================DIV60==
def get_FamilyID_from_EventID(ID, db_connection):

    SqlStmt = """
SELECT OwnerID
  FROM EventTable et
WHERE  et.EventID = ?
"""
    cur = db_connection.cursor()
    cur.execute(SqlStmt, (ID,))
    rows = cur.fetchall()

    if (len(rows) != 1):
        raise RM_Py_Exception("More than one owner ID found")
    return rows[0][0]


# ===================================================DIV60==
def get_list_of_events_to_convert(ID, FamilyType,
                                  desc_sel, date_sel, db_connection):

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
        cur = db_connection.cursor()
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
        cur = db_connection.cursor()
        cur.execute(SqlStmt, (ID, OwnerType, date_sel))
    elif desc_sel == '' and date_sel == '':
        SqlStmt = """
SELECT EventID
  FROM EventTable et
 WHERE et.EventType = ?
   AND et.OwnerType = ?
 ORDER BY OwnerID
"""
        cur = db_connection.cursor()
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
        cur = db_connection.cursor()
        cur.execute(SqlStmt, (ID, OwnerType, date_sel, desc_sel))
    else:
        raise RM_Py_Exception('Combo search terms not supported')

    rows = cur.fetchall()
    listOfFactIDs = []
    for x in range(len(rows)):
        listOfFactIDs.append(rows[x][0])
    return listOfFactIDs


# ===================================================DIV60==
def get_father_mother_IDs(ID, db_connection):

    SqlStmt = """
SELECT FatherID, MotherID
  FROM FamilyTable ft
 WHERE ft.FamilyID = ?
"""
    cur = db_connection.cursor()
    cur.execute(SqlStmt, (ID,))
    rows = cur.fetchall()

    if (len(rows) != 1):
        raise RM_Py_Exception(
            "ERROR INTERNAL More than one row returned getting family id")
    return rows[0]


# ===================================================DIV60==
def change_the_event(EventID, OwnerID, newEventTypeID,
                     facttype_is_fam_new, db_connection):

    if facttype_is_fam_new:
        OwnerType = 1
    else:
        OwnerType = 0

    SqlStmt = """
UPDATE EventTable
   SET OwnerType = ?,
       EventType= ?,
       OwnerID = ?
 WHERE EventID = ?
"""
    cur = db_connection.cursor()
    cur.execute(SqlStmt, (OwnerType, newEventTypeID, OwnerID, EventID))
    return


# ===================================================DIV60==
def add_new_witness(EventID, OwnerID, RoleID, db_connection):

    SqlStmt = """
INSERT INTO WitnessTable
  ( EventID, PersonID, Role, UTCModDate)
  VALUES ( ?, ?, ?, julianday('now') - 2415018.5 )
"""
    cur = db_connection.cursor()
    cur.execute(SqlStmt, (EventID, OwnerID, RoleID))
    return


# ===================================================DIV60==
def create_db_connection(db_file_path, db_extension_file_path):

    db_connection = None
    try:
        db_connection = sqlite3.connect(db_file_path)
        if db_extension_file_path is not None:
            # load SQLite extension
            db_connection.enable_load_extension(True)
            db_connection.load_extension(db_extension_file_path)
    except Exception as e:
        raise RM_Py_Exception(
            e, "\n\n" "Cannot open the RM database file." "\n")
    return db_connection


# ===================================================DIV60==
def pause_with_message(message=None):

    if (message != None):
        print(str(message))
    input("\n" "Press the <Enter> key to continue...")
    return


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
def get_SQLite_library_version(dbConnection):

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
class RM_Py_Exception(Exception):

    '''Exceptions thrown for configuration/database issues'''


# ===================================================DIV60==
# Call the "main" function
if __name__ == '__main__':
    main()

# ===================================================DIV60==
