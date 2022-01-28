import sqlite3
from sqlite3 import Error
import sys
import os
import time
import configparser


## Tested with RootsMagic v8.1.0  (RM7 no longer supported)
##             Python for Windows v3.9.0
##             unifuzz64.dll (ver not set, MD5=06a1f485b0fae62caa80850a8c7fd7c2)

def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by the db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


def select(conn, PersonID):

    SqlStmt="""\
--- PERSON sources
  SELECT DISTINCT SourceTable.Name, CitationTable.CitationName
    FROM SourceTable
    JOIN CitationTable     ON SourceTable.SourceID = CitationTable.SourceID
    JOIN CitationLinkTable ON CitationTable.CitationID = CitationLinkTable.LinkID
    JOIN PersonTable       ON CitationLinkTable.OwnerID = PersonTable.PersonID
    WHERE PersonTable.PersonID=?
      AND CitationLinkTable.OwnerType=0

  UNION

--- NAME sources
  SELECT DISTINCT SourceTable.Name, CitationTable.CitationName
    FROM SourceTable
    JOIN CitationTable     ON SourceTable.SourceID = CitationTable.SourceID
    JOIN CitationLinkTable ON CitationTable.CitationID = CitationLinkTable.LinkID
    JOIN NameTable         ON CitationLinkTable.OwnerID = NameTable.NameID
    WHERE NameTable.OwnerID=?
      AND CitationLinkTable.OwnerType=7

  UNION

--- EVENT-PERSON sources
  SELECT DISTINCT SourceTable.Name, CitationTable.CitationName
    FROM SourceTable
    JOIN CitationTable     ON SourceTable.SourceID = CitationTable.SourceID
    JOIN CitationLinkTable ON CitationTable.CitationID = CitationLinkTable.LinkID
    JOIN EventTable ON CitationLinkTable.OwnerID = EventTable.EventID
    WHERE EventTable.OwnerID=?
      AND CitationLinkTable.OwnerType=2
      AND EventTable.OwnerType=0

  UNION

--- EVENT-FAMILY sources
  SELECT DISTINCT SourceTable.Name, CitationTable.CitationName
    FROM SourceTable
    JOIN CitationTable     ON SourceTable.SourceID = CitationTable.SourceID
    JOIN CitationLinkTable ON CitationTable.CitationID = CitationLinkTable.LinkID
    JOIN EventTable        ON CitationLinkTable.OwnerID = EventTable.EventID
    JOIN FamilyTable       ON EventTable.OwnerID = FamilyTable.FamilyID
    WHERE (FamilyTable.FatherID=? OR FamilyTable.MotherID=?)
      AND CitationLinkTable.OwnerType=2
      AND EventTable.OwnerType=1

  UNION

--- FAMILY sources
  SELECT DISTINCT SourceTable.Name, CitationTable.CitationName
    FROM SourceTable
    JOIN CitationTable     ON SourceTable.SourceID = CitationTable.SourceID
    JOIN CitationLinkTable ON CitationTable.CitationID = CitationLinkTable.LinkID
    JOIN FamilyTable       ON CitationLinkTable.OwnerID = FamilyTable.FamilyID
    WHERE (FamilyTable.FatherID=? OR FamilyTable.MotherID=?)
      AND CitationLinkTable.OwnerType=1

  ORDER BY SourceTable.Name;
"""


    cur = conn.cursor()
    cur.execute(SqlStmt, (PersonID,PersonID,PersonID,PersonID,PersonID,PersonID,PersonID) )

    rows = cur.fetchall()

    for row in rows:
        print(row[0], "     ", row[1])
    print ("\n", len(rows), " source citations found \n\n")

    return rows



def main():
  # Configuration file
  IniFile="RM-Python-config.ini"
  
  # ini file must be in "current directory" and encoded as UTF-8 if non-ASCII chars present (no BOM)
  if not os.path.exists(IniFile):
      print("ERROR: The ini configuration file, " + IniFile + " must be in the current directory." )
      return

  config = configparser.ConfigParser()
  config.read('RM-Python-config.ini', 'UTF-8')

  # Read file paths from ini file
  report_Path   = config['File Paths']['REPORT_PATH']
  database_Path = config['File Paths']['DB_PATH']
  RMNOCASE_Path = config['File Paths']['RMNOCASE_PATH']

  if not os.path.exists(database_Path):
      print('Database path not found')
      return

  FileModificationTime = time.ctime( os.path.getmtime(database_Path))

  PersonID=0
  try:
   PersonID = config['RIN']['PERSON_RIN']
  except KeyError:
    PersonID = input("No ID specified in configuration file. Enter it now: ")

  print("\n\nPersonID=", PersonID, "\n\n")

  # create a database connection
  conn = create_connection(database_Path)
  conn.enable_load_extension(True)
  conn.load_extension(RMNOCASE_Path)
  
  with conn:
      select(conn, PersonID)

  input("Hit Enter to exit")




if __name__ == '__main__':
    main()
    
