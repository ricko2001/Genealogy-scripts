import os
import sys
import sqlite3
from datetime import datetime
import configparser
from pathlib import Path
import subprocess
import traceback

sys.path.append( r'..\RM -Dates and Sort Dates' )
# OR have a copy in the same dir as this script
import RMDate


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
#   Re-order citations attached to a particular fact.


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

    change_citation_order_feature(config, db_connection, report_file)


# ===================================================DIV60==
def change_citation_order_feature(config, db_connection, report_file):

    try:
      PersonID = get_PersonID_from_user( db_connection, report_file)

      # TODO  support associations, tasks
      attacdhed_to = input(
         "\nAre the citations attached to a Fact (f), a name (n) or the Person (p)?:\n")

      if attacdhed_to == "":
        raise RM_Py_Exception("Cannot interpret response.")

      if attacdhed_to in "Pp":
        rows = attached_to_person( PersonID, db_connection)

      elif attacdhed_to in "Ff":
        rows = attached_to_fact(PersonID, db_connection)

      elif attacdhed_to in "Nn":
        rows = attached_to_name(PersonID, db_connection)

      else:
        raise RM_Py_Exception("Cannot interpret response.")

      rowDict = order_the_local_citations(rows, report_file)
      UpdateDatabase(rowDict, db_connection)

    except KeyboardInterrupt:
      raise RM_Py_Exception('ERROR: User terminated app with control C')

    return 0


# ===========================================DIV50==
def get_PersonID_from_user( dbConnection, report_file ):

    # input the PersonID / RIN
    PersonID = input("Enter the RIN of the person who has the citations to reorder:\n")

    SqlStmt = """
    SELECT nt.Prefix, nt.Given, nt.Surname, nt.Suffix
      FROM PersonTable AS pt
      INNER JOIN NameTable AS nt ON nt.OwnerID=pt.PersonID
      WHERE nt.OwnerID = ?
        AND nt.IsPrimary = 1
    """

    cur = dbConnection.cursor()
    cur.execute( SqlStmt, (PersonID, ) )
    rows = cur.fetchall()

    if len(rows) == 0:
      raise RM_Py_Exception("That RIN does not exist.")
    elif len(rows) > 1:
      raise RM_Py_Exception("PersonID index not primary key??. Not unique.")
    elif len(rows) == 1:
      print( "RIN= " + PersonID + "  points to:\n" 
           + rows[0][0], rows[0][1], rows[0][2], rows[0][3], )
      report_file.write( "RIN= " + PersonID + "  points to:\n" 
           + rows[0][0] + " " + rows[0][1] + " "+ rows[0][2] + " " + rows[0][3] + "\n\n" )
      
    return PersonID


# ===========================================DIV50==
def attached_to_name( PersonID, db_connection):

    # Select nameID's that have more than 1 citation attached
    SqlStmt = """
    SELECT  nt.NameID, nt.Prefix, nt.Given, nt.Surname, nt.Suffix
      FROM NameTable AS nt
          INNER JOIN CitationLinkTable AS clt ON clt.OwnerID = nt.NameID AND clt.OwnerType = 7
          WHERE  nt.OwnerID = ?
          GROUP BY nt.NameID
          HAVING COUNT() > 1
    """
    cur = db_connection.cursor()
    cur.execute( SqlStmt, (PersonID, ) )
    rows = cur.fetchall()

    numberOfNames = len(rows)
    if (numberOfNames == 0):
      raise RM_Py_Exception('Either RIN does not exist or no names found. ')
    elif (numberOfNames > 1):
  #    raise RM_Py_Exception('Found more than 1 name. Try again.')
      nameID = select_name_from_list(rows)
    elif (numberOfNames == 1):
      pause_with_message('One name found.')
      #continue ...

    NameID = rows[0][0]
    print (NameID)
    SqlStmt = """
    SELECT clt.SortOrder, clt.LinkID, st.Name, ct.CitationName
      FROM CitationTable AS ct
      JOIN CitationLinkTable AS clt ON clt.CitationID = ct.CitationID
      JOIN SourceTable AS st ON ct.SourceID = st.SourceID
      WHERE clt.OwnerID = ?
        AND clt.OwnerType = 7
    ORDER BY clt.SortOrder ASC
    """
    cur = db_connection.cursor()
    cur.execute( SqlStmt, (NameID, ) )
    rows = cur.fetchall()

    return rows


# ===========================================DIV50==
def select_name_from_list( rows ):

    # .SortOrder, .LinkID, st.Name, .CitationName

    for i in range( 1, len(rows)+1):
      print (i, rows[i-1][1], rows[i-1][2], rows[i-1][3], rows[i-1][4] )

    try:
      citation_number = int(input("Which name's citations shall be ordered? ") )
    except ValueError as e:
      raise RM_Py_Exception('Type a number')

    nameID = rows[citation_number -1][0]

    return nameID


# ===========================================DIV50==
def select_event_from_list(rows):

    # et.EventID, ftt.Name, et.Date, et.Details

    for i in range( 1, len(rows)+1):
      #print (i, rows[i-1][1], rows[i-1][2], rows[i-1][3] )
      print (i, rows[i-1][1] + ":    " + RMDate.from_RMDate(rows[i-1][2], RMDate.Format.SHORT), rows[i-1][3] )

    try:
      citation_number = int(input("Which event's citations shall be ordered? ") )
    except ValueError as e:
      raise RM_Py_Exception('Type a number')

    eventID = rows[citation_number -1][0]

    return eventID


# ===========================================DIV50==
def attached_to_fact( PersonID, db_connection):

    EventID = None

    FactTypeID = input("Enter the FactTypeID or\n" +
                "blank for full list of attached Facts with more than one citation\n")

    if FactTypeID == '':
    # Select all EventID's that have more than 1 citation attached
      SqlStmt = """
      SELECT et.EventID, ftt.Name, et.Date, et.Details
        FROM EventTable AS et
        INNER JOIN FactTypeTable AS ftt ON ftt.FactTypeID = et.EventType
        INNER JOIN CitationLinkTable AS clt ON clt.OwnerID = et.EventID AND clt.OwnerType = 2
        WHERE et.OwnerID = ?
          AND et.OwnerType = 0
          AND clt.OwnerType = 2
        GROUP BY et.EventID
        HAVING COUNT() > 1
      """

      cur = db_connection.cursor()
      cur.execute( SqlStmt, (PersonID, ) )
      rows = cur.fetchall()

    else:
      # Select EventID's of specified type that have more than 1 citation attached
      SqlStmt = """
      SELECT et.EventID, ftt.Name, et.Date, et.Details
        FROM EventTable AS et
        INNER JOIN FactTypeTable AS ftt ON ftt.FactTypeID = et.EventType
        INNER JOIN CitationLinkTable AS clt ON clt.OwnerID = et.EventID AND clt.OwnerType = 2
        WHERE et.OwnerID = ?
          AND et.OwnerType = 0
          AND et.EventType = ?
        GROUP BY et.EventID
        HAVING COUNT() > 1
      """

      cur = db_connection.cursor()
      cur.execute( SqlStmt, (PersonID, FactTypeID) )
      rows = cur.fetchall()


    numberOfEvents = len(rows)
    print(numberOfEvents)
    if (numberOfEvents > 1):
      EventID = select_event_from_list(rows)
    elif (numberOfEvents == 0):
      raise RM_Py_Exception('No events with more than one citation found. Try again.')
    elif (numberOfEvents == 1):
      EventID = rows[0][0]
      print("Found one event with more than one citation.\n" +
            #rows[0][1], rows[0][2], rows[0][3] )
            rows[0][1], ":    " + RMDate.from_RMDate(rows[0][2], RMDate.Format.SHORT) , rows[0][3] )

    SqlStmt = """
    SELECT clt.SortOrder, clt.LinkID, st.Name, ct.CitationName
      FROM CitationTable AS ct
      JOIN CitationLinkTable AS clt ON clt.CitationID = ct.CitationID
      JOIN SourceTable AS st ON ct.SourceID = st.SourceID
      WHERE clt.OwnerID = ?
        AND clt.OwnerType = 2
    ORDER BY clt.SortOrder ASC
    """
    cur = db_connection.cursor()
    cur.execute( SqlStmt, (EventID, ) )
    rows = cur.fetchall()

    return rows


# ===========================================DIV50==
def attached_to_person( PersonID, db_connection):

    SqlStmt = """
    SELECT clt.SortOrder, clt.LinkID, st.Name, ct.CitationName
      FROM CitationTable AS ct
      JOIN CitationLinkTable AS clt ON clt.CitationID = ct.CitationID
      JOIN SourceTable AS st ON ct.SourceID = st.SourceID
      WHERE clt.OwnerID = ?
        AND clt.OwnerType = 0
    ORDER BY clt.SortOrder ASC
    """
    cur = db_connection.cursor()
    cur.execute( SqlStmt, (PersonID, ) )
    rows = cur.fetchall()
    if len(rows) == 0:
      raise RM_Py_Exception( "Person has no citations attached")
    if len(rows) == 1:
      raise RM_Py_Exception( "Person has only one citation attached")
    return rows


# ===========================================DIV50==
def order_the_local_citations( rows, report_file):

    rowDict = dict()
    # Create the origin 1 based dictionary
    # Use 1 based indexing for human users
    for i in range( 0, len(rows)):
      rowDict[i+1] =( (rows[i][1], (rows[i][2], rows[i][3])))

    print ("\n\n")

    # range limit when using 1 based indexing
    citation_number_limit = len(rowDict) +1

    print ( "\n" +
            "------------------------------------------------------\n" +
            "To re-order citations, at each prompt, enter one of:\n"+
            "*  the number of the citation that should go into this slot\n" +
            "*  nothing- to accept current slot as correct\n" +
            "*  s to accept current and following slots as correct\n" +
            "*  a to abort and make no chnages\n" +
            "------------------------------------------------------\n" )

    Done = False
    while not Done:
        # Print the list in current order
        for i in range( 1, citation_number_limit):
            print( i, rowDict[i][1] )
        report_file.write("\n\n Original order \n")
        for i in range( 1, citation_number_limit):
            report_file.write( str(i) + "   " + str(rowDict[i][1]) + "\n" )

        for j in range( 1, citation_number_limit-1):
            response =  str(input( "\nWhat goes in slot # " + str(j) + " : "))
            if response == '': continue
            elif response in 'S s': break
            elif response in 'A a': raise RM_Py_Exception("No changes made to database")
            else :
                try:
                    swapVal = int(response)
                except ValueError:
                    raise RM_Py_Exception('Enter an integer, blank,  or S or s or A or a')
            rowDict[swapVal], rowDict[j] = rowDict[j], rowDict[swapVal]
            print ("\n\n")
            for i in range( 1, citation_number_limit):
                print( i, rowDict[i][1] )

        print ("\n\n")

        # Print order after a round of sorting
        for i in range( 1, citation_number_limit):
            print( i, rowDict[i][1] )

        respponse = input("\n\n"
                        "Satisfied with the citation order shown above?\n"
                        "Enter one of-\n"
                        "*  Y/y to make the citation order change as shown above\n"
                        "*  N/n to go back and do another round of re-ordering\n"
                        "*  A/a to abort and not make any changes to the database \n")
        if respponse  in "Yy":
            # Print order after a round of sorting
            for i in range( 1, citation_number_limit):
                print( i, rowDict[i][1] )
            report_file.write("\n\n Current order \n")
            for i in range( 1, citation_number_limit):
                report_file.write( str(i) + "   " + str(rowDict[i][1]) + "\n" )
            Done = True
        elif respponse  in "Aa":
            raise RM_Py_Exception("No changes made to database")
        # assume No
        print ("\n\n")
        # End while Done

    return rowDict


# ===========================================DIV50==
def UpdateDatabase( rowDict, db_connection ):

    # range limit when using 1 based indexing
    citNumberLimit = len(rowDict) +1

    # Now update the SortOrder column for the given Citation Links
    SqlStmt = """
    UPDATE  CitationLinkTable AS clt
      SET SortOrder = ?
      WHERE LinkID = ?
    """

    for i in range( 1, len(rowDict)+1):
      cur = db_connection.cursor()
      cur.execute( SqlStmt, (i, rowDict[i][0]) )
      db_connection.commit()

    return


# ===================================================DIV60==
def create_db_connection(db_file_path, db_extension):

    db_connection = None
    try:
        db_connection = sqlite3.connect(db_file_path)
        if db_extension is not None and db_extension != '':
            # load SQLite extension
            db_connection.enable_load_extension(True)
            db_connection.load_extension(db_extension)
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
