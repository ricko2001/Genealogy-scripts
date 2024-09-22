import os
import sys
import sqlite3
from datetime import datetime

sys.path.append( r'..\\RM -RMpy package' )
import RMpy.launcher # type: ignore
import RMpy.common as RMc # type: ignore

# List all citations associated with a Person

# Requirements:
#   RootsMagic database file
#   RM-Python-config.ini

# Tested with:
#   RootsMagic database file v10.0.1
#   Python for Windows v3.12.3

# Config files fields used
#    FILE_PATHS  REPORT_FILE_PATH
#    FILE_PATHS  REPORT_FILE_DISPLAY_APP
#    FILE_PATHS  DB_PATH
#    RIN         PERSON_RIN (optional)

# ===================================================DIV60==


def main():

    # Configuration
    config_file_name = "RM-Python-config.ini"
    allow_db_changes = False
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

    display_sources_feature(config, db_connection, report_file)


# ===================================================DIV60==
def display_sources_feature(config, db_connection, report_file):

    PersonID = None
    try:
        PersonID_str = config['RIN']['PERSON_RIN']
        PersonID = int(PersonID_str)

    except:
        pass

    if PersonID is None:
        PersonID_str = input("\n"  "PersonID/RIN =")
        try:
            PersonID = int(PersonID_str)
        except:
            raise RM_Py_Exception(
                'ERROR: Enter an integer for the PersonID/RIN.')
        if not PersonID > 0:
            raise RM_Py_Exception('ERROR: Enter an integer larger than 0.')

    SqlStmt = """\
WITH
  constants(C_Person) AS (
    SELECT   ?   AS C_Person
    )
--      person citations
SELECT DISTINCT st.Name COLLATE NOCASE, ct.CitationName COLLATE NOCASE
  FROM SourceTable        AS st
  INNER JOIN CitationTable      AS ct    ON ct.SourceID = st.SourceID
  INNER JOIN CitationLinkTable  AS clt   ON clt.CitationID = ct.CitationID
 WHERE clt.OwnerID=(SELECT C_Person FROM constants)
    AND clt.OwnerType=0

UNION
--      name citations
SELECT DISTINCT st.Name COLLATE NOCASE, ct.CitationName COLLATE NOCASE
  FROM SourceTable        AS st
  INNER JOIN CitationTable      AS ct    ON ct.SourceID = st.SourceID
  INNER JOIN CitationLinkTable  AS clt   ON clt.CitationID = ct.CitationID
  INNER JOIN NameTable          AS nt    ON nt.NameID = clt.OwnerID
 WHERE nt.OwnerID=(SELECT C_Person FROM constants)
    AND clt.OwnerType=7

UNION
--      fact-person citations
SELECT DISTINCT st.Name COLLATE NOCASE, ct.CitationName COLLATE NOCASE
  FROM SourceTable        AS st
  INNER JOIN CitationTable      AS ct    ON ct.SourceID = st.SourceID
  INNER JOIN CitationLinkTable  AS clt   ON clt.CitationID = ct.CitationID
  INNER JOIN EventTable         AS et    ON et.EventID = clt.OwnerID
 WHERE et.OwnerID=(SELECT C_Person FROM constants)
    AND clt.OwnerType=2
    AND et.OwnerType=0

UNION
--      fact-family citations
SELECT DISTINCT st.Name COLLATE NOCASE, ct.CitationName COLLATE NOCASE
  FROM SourceTable        AS st
  INNER JOIN CitationTable      AS ct    ON ct.SourceID = st.SourceID
  INNER JOIN CitationLinkTable  AS clt   ON clt.CitationID = ct.CitationID
  INNER JOIN EventTable         AS et    ON et.EventID = clt.OwnerID
  INNER JOIN FamilyTable        AS ft    ON ft.FamilyID = et.OwnerID
 WHERE (ft.FatherID=(SELECT C_Person FROM constants) OR ft.MotherID=(SELECT C_Person FROM constants))
    AND clt.OwnerType=2
    AND et.OwnerType=1

UNION
--      family citations
SELECT DISTINCT st.Name COLLATE NOCASE, ct.CitationName COLLATE NOCASE
  FROM SourceTable        AS st
  INNER JOIN CitationTable      AS ct    ON ct.SourceID = st.SourceID
  INNER JOIN CitationLinkTable  AS clt   ON clt.CitationID = ct.CitationID
  INNER JOIN FamilyTable        AS ft    ON ft.FamilyID = clt.OwnerID
 WHERE (ft.FatherID=(SELECT C_Person FROM constants) OR ft.MotherID=(SELECT C_Person FROM constants))
    AND clt.OwnerType=1

UNION
--      association citations
SELECT DISTINCT st.Name COLLATE NOCASE, ct.CitationName COLLATE NOCASE
  FROM SourceTable              AS st
  INNER JOIN CitationTable      AS ct   ON ct.SourceID = st.SourceID
  INNER JOIN CitationLinkTable  AS clt  ON clt.CitationID = ct.CitationID
  INNER JOIN FANTable           AS ft   ON ft.FanID = clt.OwnerID
 WHERE (ft.ID1=(SELECT C_Person FROM constants) OR ft.ID2=(SELECT C_Person FROM constants))
    AND clt.OwnerType=19

UNION
--      shared fact citations
SELECT DISTINCT st.Name COLLATE NOCASE, ct.CitationName COLLATE NOCASE
  FROM SourceTable             AS st
  INNER JOIN CitationTable     AS ct  ON ct.SourceID = st.SourceID
  INNER JOIN CitationLinkTable AS clt ON clt.CitationID = ct.CitationID
  INNER JOIN EventTable        AS et  ON et.EventID = clt.OwnerID
  INNER JOIN WitnessTable      AS wt  ON et.EventID = wt.EventID
 WHERE wt.PersonID=(SELECT C_Person FROM constants)
    AND clt.OwnerType=2
    AND et.OwnerType=0

ORDER BY st.Name COLLATE NOCASE;
"""

    cur = db_connection.cursor()
    cur.execute(SqlStmt, (PersonID,))
    rows = cur.fetchall()

    report_file.write("PersonID = " + str(PersonID) + "\n")
    report_file.write(str(len(rows)) + " source citations found \n\n")

    for row in rows:
        report_file.write(row[0] + "\t\t" + row[1] + "\n\n")

    report_file.write(
        "================================================" "\n\n")

    return


# ===================================================DIV60==
def create_db_connection(db_file_path, db_extension_file_path):

    dbConnection = None
    try:
        dbConnection = sqlite3.connect(db_file_path)
        if db_extension_file_path is not None:
            # load SQLite extension
            dbConnection.enable_load_extension(True)
            dbConnection.load_extension(db_extension_file_path)
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
def time_stamp_now(type=""):

    # return a TimeStamp string
    now = datetime.now()
    if type == '':
        dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
    elif type == 'file':
        dt_string = now.strftime("%Y-%m-%d_%H%M%S")
    return dt_string


# ===================================================DIV60==
def pause_with_message(message=None):

    if (message != None):
        print(str(message))
    input("\n" "Press the <Enter> key to continue...")
    return


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
