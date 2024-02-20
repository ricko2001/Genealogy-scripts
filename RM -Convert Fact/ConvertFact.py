﻿import os
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

# Utility uses RMNOCASE extension, but makes no changes to columns that use that collation.
# Rebuild index in RM should not be necessary.


# ===================================================DIV60==
def main():

    # Configuration
    IniFileName = "RM-Python-config.ini"

#  PauseWithMessage("Always have a known-good database backup before running this script\n"
#                      "You will likely want to fix problems in the first run");

    try:  # errors go to console window
        # ini file must be in "current directory" and encoded as UTF-8 (no BOM).
        # see   https://docs.python.org/3/library/configparser.html
        IniFile = os.path.join(get_current_directory(), IniFileName)

        # Check that ini file is at expected path and that it is readable & valid.
        if not os.path.exists(IniFile):
            raise RMPyException("ERROR: The ini configuration file, " + IniFileName
                                + " must be in the same directory as the .py or .exe file.\n\n")

        config = configparser.ConfigParser(empty_lines_in_values=False,
                                           interpolation=None)
        try:
            config.read(IniFile, 'UTF-8')
        except:
            raise RMPyException("ERROR: The " + IniFileName
                                + " file contains a format error and cannot be parsed.\n\n")

        try:
            report_Path = config['FILE_PATHS']['REPORT_FILE_PATH']
        except:
            raise RMPyException('ERROR: REPORT_FILE_PATH must be defined in the '
                                + IniFileName + "\n\n")

        try:
            # Use UTF-8 encoding for the report file. Test for write-ability
            open(report_Path,  mode='w', encoding='utf-8')
        except:
            raise RMPyException('ERROR: Cannot create the report file '
                                + report_Path + "\n\n")

    except RMPyException as e:
        PauseWithMessage(e)
        return 1
    except Exception as e:
        traceback.print_exception(e, file=sys.stdout)
        PauseWithMessage("ERROR: Application failed. Please report. " + str(e))
        return 1

    # Open the Report File.
    with open(report_Path,  mode='w', encoding='utf-8') as reportF:

        try:        # errors go to the report file
            try:
                database_path = config['FILE_PATHS']['DB_PATH']
            except:
                raise RMPyException('ERROR: DB_PATH must be specified.')
            if not os.path.exists(database_path):
                raise RMPyException('ERROR: Path for database not found: ' + database_path
                                    + '\n\n' 'Absolute path checked:\n"'
                                    + os.path.abspath(database_path) + '"')

            try:
                RMNOCASE_path = config['FILE_PATHS']['RMNOCASE_PATH']
            except:
                raise RMPyException('ERROR: RMNOCASE_PATH must be specified.')
            if not os.path.exists(RMNOCASE_path):
                raise RMPyException('ERROR: Path for database extension unifuzz64.dll not found: '
                                    + RMNOCASE_path
                                    + '\n\n' 'Absolute path checked:\n"'
                                    + os.path.abspath(RMNOCASE_path) + '"')

            try:
                ReportDisplayApp = config['FILE_PATHS']['REPORT_FILE_DISPLAY_APP']
            except:
                ReportDisplayApp = None
            if ReportDisplayApp != None and not os.path.exists(ReportDisplayApp):
                raise RMPyException('ERROR: Path for report file display app not found: '
                                    + ReportDisplayApp)

            try:
                fact_current = config['MAPPING']['FACT_CURRENT']
            except:
                raise RMPyException('ERROR: FACT_CURRENT must be specified.')

            try:
                fact_new = config['MAPPING']['FACT_NEW']
            except:
                raise RMPyException('ERROR: FACT_NEW must be specified.')

            try:
                role = config['MAPPING']['ROLE']
            except:
                raise RMPyException('ERROR: ROLE must be specified.')

            # RM database file info
            FileModificationTime = datetime.fromtimestamp(
                os.path.getmtime(database_path))
            G_DbFileFolderPath = Path(database_path).parent

            # write header to report file
            with create_DBconnection(database_path, RMNOCASE_path) as dbConnection:
                reportF.write("Report generated at      = " + TimeStampNow()
                              + "\n" "Database processed       = " +
                              os.path.abspath(database_path)
                              + "\n" "Database last changed on = "
                              + FileModificationTime.strftime("%Y-%m-%d %H:%M:%S")
                              + "\n" "SQLite library version   = "
                              + GetSQLiteLibraryVersion(dbConnection) + "\n\n\n")

                reportF.write('Current FactType: "' + fact_current
                              + '"\n     New FactType: "' + fact_new
                              + '"\n             Role: "' + role + '"\n\n\n')

                IDtuple = lookup_validate(
                    fact_current, fact_new, role, dbConnection, reportF)
                convert_fact(IDtuple, dbConnection, reportF)

        except RMPyException as e:
            reportF.write(str(e))
            return 1
        except Exception as e:
            traceback.print_exception(e, file=reportF)
            reportF.write(
                "\n\n" "ERROR: Application failed. Please email report file to author. ")
            return 1
        finally:
            if ReportDisplayApp != None:
                subprocess.Popen([ReportDisplayApp, report_Path])

    # report file is now closed. Can be opened for display
    if ReportDisplayApp != None:
        subprocess.Popen([ReportDisplayApp, report_Path])
    return 0


# ===================================================DIV60==
def lookup_validate(fact_current_name, fact_new_name, role_name, dbConnection, reportF):

    # confirm fact_current_name is unique
    SqlStmt = """
  SELECT FactTypeID, OwnerType
    FROM FactTypeTable ftt
   WHERE ftt.Name = ?
  """
    cur = dbConnection.cursor()
    cur.execute(SqlStmt, (fact_current_name,))
    rows = cur.fetchall()
    if len(rows) == 0:
        raise RMPyException(
            "ERROR: The entered Current FactType name could not be found.\n")
    if len(rows) > 1:
        raise RMPyException(
            "ERROR: The entered Current FactType name is not unique. Fix this.\n")

    FamilyTypeFact = False
    if rows[0][1] == 1:
        FamilyTypeFact = True
        reportF.write("'Current FactType' is of type 'FAMILY'.\n\n\n")
    FactTypeID_current = rows[0][0]

    cur = dbConnection.cursor()
    cur.execute(SqlStmt, (fact_new_name,))
    rows = cur.fetchall()
    if len(rows) == 0:
        raise RMPyException(
            "ERROR: The entered New FactType name could not be found.\n")
    if len(rows) > 1:
        raise RMPyException(
            "ERROR: The entered New FactType name is not unique. Fix this.\n")
    if rows[0][1] == 1:
        reportF.write("The entered New FactType name is a FAMILY type.\n")
    FactTypeID_new = rows[0][0]

    RoleTypeID = 0

    if FamilyTypeFact:
        SqlStmt = """
  SELECT RoleID, EventType
    FROM RoleTable rt
    WHERE rt.RoleName = ?
      AND rt.EventType = ?
  """
        cur = dbConnection.cursor()
        cur.execute(SqlStmt, (role_name, FactTypeID_new))
        rows = cur.fetchall()
        if len(rows) == 0:
            raise RMPyException(
                "The entered Role name could not be found associated with the new fact type.\n")
        if len(rows) > 1:
            raise RMPyException(
                "The entered Role name is not unique for the new fact type. Fix this.\n")
        RoleTypeID = rows[0][0]

# All of the roles used by the old fact must also appear in the new fact
# List Roles that user needs to create for the new Fact Type
    SqlStmt = """
SELECT DISTINCT RoleID, RoleName
      FROM RoleTable AS rt
INNER JOIN WitnessTable AS wt ON wt.Role = rt.RoleID
INNER JOIN EventTable   AS et ON et.EventID = wt.EventID
INNER JOIN FactTypeTable AS ftt ON et.EventType = ftt.FactTypeID
      WHERE ftt.FactTypeID = :curr_FTid  --OldFactType
        AND RoleName NOT IN (
            SELECT RoleName
              FROM RoleTable rt
              WHERE EventType = :new_FTid )  -- NewFactType
"""
    cur = dbConnection.cursor()
    cur.execute(SqlStmt, {"curr_FTid": FactTypeID_current,
                "new_FTid": FactTypeID_new})
    rows = cur.fetchall()
    if len(rows) != 0:
        reportF.write("The following Roles are in use by the Current Fact Type,\n"
                      + "but do not exist for the New Fact Type.\n"
                      + "They will either need to be defined for the new Fact Type\n"
                      + "or eliminated from use by the Old Fact type.\n"
                      + "Coordinating the roles may be accomplished by altering the\n"
                      + "Role Names. This must be done before Fact conversion\n"
                      + "can be performed.\n\n"
                      + "--Missing Roles:--\n")
        for row in rows:
            reportF.write(str(row[1]) + "\n")
        reportF.write("\n\n\n")
        raise RMPyException(
            "ERROR: Roles need to be coordinated between the Old and New Fact Types.\n")

    return (FactTypeID_current, FactTypeID_new, RoleTypeID, FamilyTypeFact)


# ===================================================DIV60==
def convert_fact(IDtuple, dbConnection, reportF):

    FactTypeID = IDtuple[0]
    newFactTypeID = IDtuple[1]
    roleID = IDtuple[2]
    FamilyTypeFact = IDtuple[3]

    listOfFactIDs = getListOfEventsToConvert(
        FactTypeID, FamilyTypeFact, dbConnection)
    if len(listOfFactIDs) == 0:
        raise RMPyException("Nothing to convert !\n\n")

    if FamilyTypeFact:
        reportF.write(
            "Facts attached to these families were converted:\n  Father ID:   Mother ID: ")
        for FactToConvert in listOfFactIDs:
            FamID = getFamilyIDfromEvent(FactToConvert, dbConnection)
            FatherMother = getFatherMotherIDs(FamID, dbConnection)

            FatherID = FatherMother[0]
            MotherID = FatherMother[1]
            reportF.write("\n    " + str(FatherID) +
                          "           " + str(MotherID))

            changeTheEvent(FactToConvert, FatherID,
                           newFactTypeID, dbConnection)
            updateRoleInExistingWitnesses(
                FactToConvert, newFactTypeID, dbConnection)
            addNewWitness(FactToConvert, MotherID, roleID, dbConnection)
    else:
        reportF.write("Facts attached to these Persons (ID) were converted:")
        for FactToConvert in listOfFactIDs:
            PersonID = getPersonIDfromEventID(FactToConvert, dbConnection)
            reportF.write("\n  " + str(PersonID))
            changeTheEvent(FactToConvert, PersonID,
                           newFactTypeID, dbConnection)
            updateRoleInExistingWitnesses(
                FactToConvert, newFactTypeID, dbConnection)

    return


# ===================================================DIV60==
def updateRoleInExistingWitnesses(FactToConvert, FactTypeID_new, dbConnection):

    # List of all Witness records that need their role updated
    SqlStmt = """
SELECT wt.WitnessID, rt.RoleName
  FROM WitnessTable AS wt
INNER JOIN RoleTable AS rt ON rt.RoleID = wt.Role
      WHERE wt.EventID = :FactId
  ORDER BY rt.RoleName
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
      AND RoleName = :RoleName
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
            SqlStmt, {"WitnessID": WitnessToUpdate, "RoleID": newRoleID})
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
        raise RMPyException("more than one owner ID found")
    return rows[0][0]


# ===================================================DIV60==
def getListOfEventsToConvert(ID, FamilyType, dbConn):

    OwnerType = 0
    if FamilyType:
        OwnerType = 1

    SqlStmt = """
SELECT EventID
  FROM EventTable et
  WHERE et.EventType = ?
    AND et.OwnerType = ?
  ORDER BY OwnerID
"""
    cur = dbConn.cursor()
    cur.execute(SqlStmt, (ID, OwnerType))
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
        raise RMPyException("more than one row returned getting family id")
    return [rows[0][0], rows[0][1]]

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
def create_DBconnection(db_file_path, db_extension):

    dbConnection = None
    try:
        dbConnection = sqlite3.connect(db_file_path)
        # load SQLite extension
        dbConnection.enable_load_extension(True)
        dbConnection.load_extension(db_extension)
    except Exception as e:
        raise RMPyException(e, "\n\n" "Cannot open the RM database file." "\n")
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
    SqlStmt = """
SELECT sqlite_version()
"""
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
class RMPyException(Exception):

    '''Exceptions thrown for configuration/database issues'''


# ===================================================DIV60==
# Call the "main" function
if __name__ == '__main__':
    main()

# ===================================================DIV60==
