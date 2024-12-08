import sys
from pathlib import Path
sys.path.append( str(Path.resolve(Path.cwd() / r'..\RM -RMpy package')))
import RMpy.launcher  # type: ignore
import RMpy.common as RMc  # type: ignore
from RMpy.common import q_str # type: ignore

import os


# Requirements:
#   RootsMagic database file v8 or 9
#   RM-Python-config.ini

# Tested with:
#   RootsMagic database file v10
#   Python for Windows v3.13

# Config files fields used
#    FILE_PATHS  REPORT_FILE_PATH
#    FILE_PATHS  REPORT_FILE_DISPLAY_APP
#    FILE_PATHS  DB_PATH


#   TODO add new feature to allow multiple moves at once by entering
#     a LIKE search criteria for Citation Name. Will probably want to
#     limit search to the existing source citations.

# ===================================================DIV60==
def main():

    # Configuration
    config_file_name = "RM-Python-config.ini"
    allow_db_changes = True
    RMNOCASE_required = False
    RegExp_required = False

    RMpy.launcher.launcher(Path(__file__).parent,
                           config_file_name,
                           run_selected_features,
                           allow_db_changes,
                           RMNOCASE_required,
                           RegExp_required)


# ===================================================DIV60==
def run_selected_features(config, db_connection, report_file):

    change_source_feature(config, db_connection, report_file)


# ===========================================DIV50==
def change_source_feature(config, db_connection, report_file):

    first_time = True
    while True:
        report_file.write(
            "\n" "========================================"  "\n")

        if (not first_time):
            if "y" != input("Go again ? (y/n)"):
                break
        first_time = False

        # Deal with the citation as it is
        citation_name = input(
            "Enter the citation name for citation to change source:\n")
        report_file.write("Citation name as entered =" + citation_name + "\n")

        SqlStmt = """
SELECT COUNT(), st.TemplateID, ct.CitationID, ct.SourceID, st.Name, ct.CitationName
  FROM SourceTable AS st
  JOIN CitationTable AS ct ON ct.SourceID = st.SourceID
 WHERE ct.CitationName LIKE ( ? || '%' )
"""

        cur = db_connection.cursor()
        cur.execute(SqlStmt, (citation_name, ))
        row = cur.fetchone()

        numberOfCitations = row[0]
        OldSourceTemplateID = row[1]
        CitationID = row[2]
        OldSourceID = row[3]
        OldSourceName = row[4]
        FullCitationName = row[5]

        if (numberOfCitations > 1):
            print('PROBLEM: Found more than 1 citation. ')
            report_file.write('PROBLEM: Found more than 1 citation.' '\n\n')

            report_file.write('No change made.' '\n\n')
            continue
        if (numberOfCitations == 0):
            print('PROBLEM: Citation not found.')
            report_file.write('PROBLEM: Citation not found.' '\n\n')
            report_file.write('No change made.' '\n\n')
            continue

        report_file.write("\nThe citation:\n" + FullCitationName +
                          "\n" "is currently found in source:\n" + OldSourceName + "\n\n")
        print("\nThe citation:\n" + FullCitationName +
              "\n" "is currently found in source:\n" + OldSourceName + "\n\n")

        # Deal with the new source
        new_source_name = input("\n\nEnter the name for the new source:\n")
        report_file.write("Source name as entered =" + new_source_name + "\n")

        SqlStmt = """
SELECT COUNT(), SourceID, TemplateID
  FROM SourceTable
 WHERE Name LIKE ( ? || '%' )
  """
        cur = db_connection.cursor()
        cur.execute(SqlStmt, (new_source_name, ))
        row = cur.fetchone()

        number_found = row[0]
        NewSourceID = row[1]
        NewSourceTemplateID = row[2]

        if (number_found > 1):
            print("PROBLEM: More than 1 source found." "\n\n")
            report_file.write("PROBLEM: More than 1 source found." "\n\n")
            report_file.write('No change made.' '\n\n')
            continue
        if (number_found == 0):
            print("PROBLEM: Source not found." "\n\n")
            report_file.write("PROBLEM: Source not found." "\n\n")
            report_file.write('No change made.' '\n\n')
            continue

        if (NewSourceID == OldSourceID):
            print(
                "PROBLEM: The citation is already using the specified new source." "\n\n")
            report_file.write(
                "PROBLEM: The citation is already using the specified new source." "\n\n")
            report_file.write('No change made.' '\n\n')
            continue

        if (NewSourceTemplateID != OldSourceTemplateID):
            print(
                "PROBLEM: The new source must be based on the same"
                " SourceTemplate as the current source." "\n\n")
            report_file.write(
                "PROBLEM: The new source must be based on the same"
                " SourceTemplate as the current source." "\n\n")
            report_file.write('No change made.' '\n')
            continue

        # update the citation to use the new source
        SqlStmt = """
UPDATE CitationTable
  SET  SourceID = ?
WHERE CitationID = ?
"""
        cur = db_connection.cursor()
        cur.execute(SqlStmt, (NewSourceID, CitationID))
        db_connection.commit()

        # Confirm update was successful

        SqlStmt = """
SELECT ct.CitationName, st.Name
  FROM SourceTable AS st
  JOIN CitationTable AS ct ON ct.SourceID = st.SourceID
 WHERE ct.CitationID = ?
"""

        cur = db_connection.cursor()
        cur.execute(SqlStmt, (CitationID, ))
        row = cur.fetchone()

        CitationName = row[0]
        SourceName = row[1]
        report_file.write("\n\n" "Confirmation of change\nCitation:\n" + CitationName
                          + "\n\n" "is now using source:\n" + SourceName + "\n")

    return 0


# ===================================================DIV60==
# Call the "main" function
if __name__ == '__main__':
    main()

# ===================================================DIV60==
