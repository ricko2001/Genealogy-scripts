# Convert Fam type facts to individual facts
# not intended for Marriage, Divorce etc or Number of children facts

import sqlite3
from sqlite3 import Error
import sys

## Tested with RootsMagic v7.6.5
##             Python for Windows v3.9.0
##             unifuzz64.dll (ver not set, MD5=06a1f485b0fae62caa80850a8c7fd7c2)

# ====================================
def create_connection(db_file, RMNOCASE_extention):
  conn = None

  conn = sqlite3.connect(db_file)

  # load extension used by RootsMagic
  conn.enable_load_extension(True)
  conn.load_extension(RMNOCASE_extention)

  return conn


# ====================================
def getFamilyIDfromEvent(ID, dbConn):

  SqlStmt = """\
    SELECT OwnerID
      FROM EventTable et
    WHERE
      et.EventID = ?
"""

  with dbConn:
    cur = dbConn.cursor()
    cur.execute(SqlStmt, (ID,))
    rows = cur.fetchall()

    if (len(rows) != 1):
      print ("more than one owner ID found")
      raise Error

  return rows[0][0]



# ====================================
def getListOfEventsToConvert(ID, dbConn):

  SqlStmt = """\
    SELECT EventID
      FROM EventTable et
      WHERE
        et.EventType = ?
        AND
        et.OwnerType = 1
"""

  with dbConn:
    cur = dbConn.cursor()
    cur.execute(SqlStmt, (ID,))
    rows = cur.fetchall()

    listOfFactIDs = []
    for x in range( len(rows) ):
      listOfFactIDs.append( rows [x] [0] )

  return listOfFactIDs


# ====================================
def getFatherMotherIDs(ID, dbConn):

  SqlStmt = """\
    SELECT FatherID, MotherID
    from FamilyTable ft
    WHERE
    ft.FamilyID = ?
"""

  with dbConn:
    cur = dbConn.cursor()
    cur.execute(SqlStmt, (ID,))
    rows = cur.fetchall()

    if (len(rows) != 1):
      print ("more than one row returned getting family id")
      raise Error

  return [ rows [0][0], rows [0][1] ]


# ====================================
def changeTheEvent(EventID, OwnerID, newEventTypeID, dbConn):

  SqlStmt = """\
    UPDATE EventTable
      SET OwnerType = 0,
          EventType= ?,
          OwnerID = ?
    WHERE
          EventID = ?
"""

  with dbConn:
    cur = dbConn.cursor()
    cur.execute(SqlStmt, (newEventTypeID, OwnerID, EventID) )


# ====================================
def addWitness( EventID, OwnerID, RoleID, dbConn):

  SqlStmt = """\
     INSERT INTO WitnessTable
        ( EventID, PersonID, Role)
      VALUES ( ?, ?, ? )
"""
  with dbConn:
    cur = dbConn.cursor()
    cur.execute(SqlStmt, ( EventID, OwnerID, RoleID ))


# ====================================
def main():
  try:
    # test database
     # TODO database = r"C:\Users\rotter\source\Python\RmFamFactConvert\test DB-convert fam\Fam CONVERT test  Otter-Saito.rmgc"

     # production
    database = r"C:\Users\rotter\Documents\Genealogy\GeneDB\Otter-Saito.rmgc"

    RMNOCASE_extention = r"C:\Users\rotter\Documents\Genealogy\Genealogy SW\RootsMagic\SQL access\RMNOCASE\unifuzz64.dll"

    # Facts to convert
    #  311	Cesus fam			18		Census			role	420 Principal2
    #  310	Residence fam		29		Residence		role	417 Principal2
    # 1071	Psgr List fam 		1001	Psgr List		role	421 Principal2
    # 1066	Note fam			1026	Note			role	416 Principal2

    frFactToFactRole = [
     (  311,   18, 420 ),
     (  310,   29, 417 ),
     ( 1071, 1001, 421 ),
     ( 1066, 1026, 416 ) ] 

    print( "Always have a known-good database backup before running this script")
    input("Press the <Enter> key to continue...")


    dbConn = create_connection(database, RMNOCASE_extention)

    for FactSet in frFactToFactRole:
      FactTypeID    = FactSet[0]
      newFactTypeID = FactSet[1]
      roleID        = FactSet[2]

      print ( "Original FactTypeID: ", FactTypeID, "New FactTypeID: ", newFactTypeID, "roleID:" , roleID )

      listOfFactIDs = getListOfEventsToConvert(FactTypeID, dbConn)

      print (len(listOfFactIDs), "Facts of this type to be converted \n\n")

      for  FactToConevert in listOfFactIDs:
        print (FactToConevert)

        FamID = getFamilyIDfromEvent(FactToConevert, dbConn)
        FatherMother = getFatherMotherIDs(FamID, dbConn)

        FatherID = FatherMother[0]
        MotherID = FatherMother[1]
        print ("  Father ID: ",  FatherID, "    MotherID: ",  MotherID)

        changeTheEvent(FactToConevert, FatherID, newFactTypeID, dbConn)
        addWitness( FactToConevert, MotherID, roleID, dbConn)

  except Error as e:
    print( "Encountered an error", e )
  return 0


# ====================================
if __name__ == '__main__':
    main()

