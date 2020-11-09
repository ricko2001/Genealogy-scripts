import sqlite3
from sqlite3 import Error
import sys

## Tested with RootsMagic v7.6.5
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
      --- person event sources
      SELECT DISTINCT SourceTable.Name
      FROM SourceTable
        JOIN CitationTable ON SourceTable.SourceID = CitationTable.SourceID
        JOIN EventTable ON CitationTable.OwnerID = EventTable.EventID
        WHERE EventTable.OwnerID=? and CitationTable.OwnerType=2 and EventTable.OwnerType=0

      UNION

      --- family event sources for males
      SELECT DISTINCT SourceTable.Name
      FROM SourceTable
        JOIN CitationTable ON SourceTable.SourceID = CitationTable.SourceID
        JOIN EventTable ON CitationTable.OwnerID = EventTable.EventID
        JOIN FamilyTable ON EventTable.OwnerID = FamilyTable.FamilyID
        WHERE FamilyTable.FatherID=? and CitationTable.OwnerType=2 and EventTable.OwnerType=1

      UNION

      --- family event sources for females
      SELECT DISTINCT SourceTable.Name
      FROM SourceTable
        JOIN CitationTable ON SourceTable.SourceID = CitationTable.SourceID
        JOIN EventTable ON CitationTable.OwnerID = EventTable.EventID
        JOIN FamilyTable ON EventTable.OwnerID = FamilyTable.FamilyID
        WHERE FamilyTable.MotherID=? and CitationTable.OwnerType=2 and EventTable.OwnerType=1

      UNION

      --- person sources
      SELECT DISTINCT SourceTable.Name
      FROM SourceTable
        JOIN CitationTable ON SourceTable.SourceID = CitationTable.SourceID
        JOIN PersonTable   ON PersonTable.PersonID = CitationTable.OwnerID
        WHERE PersonTable.PersonID=? and CitationTable.OwnerType=0

      UNION

      --- name sources
      SELECT DISTINCT SourceTable.Name
      FROM SourceTable
        JOIN CitationTable ON SourceTable.SourceID = CitationTable.SourceID
        JOIN NameTable ON CitationTable.OwnerID = NameTable.NameID
        WHERE NameTable.OwnerID=? and CitationTable.OwnerType=7 

      UNION

      --- family sources for males
      SELECT DISTINCT SourceTable.Name
      FROM SourceTable
        JOIN CitationTable ON SourceTable.SourceID = CitationTable.SourceID
        JOIN FamilyTable ON CitationTable.OwnerID = FamilyTable.FamilyID
        WHERE FamilyTable.FatherID=? and CitationTable.OwnerType=1

      UNION

      --- family sources for females
      SELECT DISTINCT SourceTable.Name
      FROM SourceTable
        JOIN CitationTable ON SourceTable.SourceID = CitationTable.SourceID
        JOIN FamilyTable ON CitationTable.OwnerID = FamilyTable.FamilyID
        WHERE FamilyTable.MotherID=? and CitationTable.OwnerType=1

      ORDER BY SourceTable.Name;
"""


    cur = conn.cursor()
    cur.execute(SqlStmt, (PersonID,PersonID,PersonID,PersonID,PersonID,PersonID,PersonID) )

    rows = cur.fetchall()

    for row in rows:
        print(row[0])
    print (len(rows), "rows returned \n\n")

    return rows



def main():
    PersonID=0
    if len(sys.argv) != 2 :
       print ("Call with PersonID")
       return
    PersonID = sys.argv[1]
    print("PersonID=", PersonID)

   # test datavbase
   # database = r"C:\Users\rotter\Documents\Genealogy\Genealogy SW\RootsMagic\SQL access\test DB\test copy Otter-Saito.rmgc"

   # production
    database = r"C:\Users\rotter\Documents\Genealogy\GeneDB\Otter-Saito.rmgc"

    RMNOCASE_extention=r"C:\Users\rotter\Documents\Genealogy\Genealogy SW\RootsMagic\SQL access\RMNOCASE\unifuzz64.dll"

    # create a database connection
    conn = create_connection(database)
    conn.enable_load_extension(True)
    conn.load_extension(RMNOCASE_extention)

    with conn:
        select(conn, PersonID)




if __name__ == '__main__':
    main()
    
