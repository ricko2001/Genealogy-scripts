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

# Tested with:
#   RootsMagic database file v10
#   Python for Windows v3.13

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

    RMpy.launcher.launcher(Path(__file__).parent,
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
            raise RMc.RM_Py_Exception(
                'ERROR: Enter an integer for the PersonID/RIN.')
        if not PersonID > 0:
            raise RMc.RM_Py_Exception('ERROR: Enter an integer larger than 0.')

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
# Call the "main" function
if __name__ == '__main__':
    main()

# ===================================================DIV60==
