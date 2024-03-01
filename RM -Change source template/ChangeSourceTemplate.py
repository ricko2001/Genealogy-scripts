import os
import sys
import time
import sqlite3
from pathlib import Path
from datetime import datetime
import configparser  # https://docs.python.org/3/library/configparser.html
import xml.etree.ElementTree as ET
import subprocess
import traceback

# WARNING make a known-good backup of the rmtree file before use.

# Requirements: (see ReadMe.txt for details)
# RootsMagic v9 database file
# RM-Python-config.ini  ( Configuration ini file to set options and parameters)
# unifuzz64.dll
# Python v3.9 or greater


# ===================================================DIV60==
#  Global Variables
G_QT = "\""


# ===================================================DIV60==
def main():

    # Configuration
    IniFileName = "RM-Python-config.ini"
    db_connection = None
    report_display_app = ''

    # ===========================================DIV50==
    # Error go to console window
    # ===========================================DIV50==

    try:
        # ini file must be in "current directory" and encoded as UTF-8 (no BOM).
        # see   https://docs.python.org/3/library/configparser.html
        IniFile = os.path.join(GetCurrentDirectory(), IniFileName)

        # Check that ini file is at expected path and that it is readable & valid.
        if not os.path.exists(IniFile):
            raise RMPyExcep("ERROR: The ini configuration file, " + IniFileName +
                            " must be in the same directory as the .py or .exe file.\n\n")

        config = configparser.ConfigParser(empty_lines_in_values=False,
                                           interpolation=None)
        try:
            config.read(IniFile, 'UTF-8')
        except:
            raise RMPyExcep("ERROR: The " + IniFileName +
                            " file contains a format error and cannot be parsed.\n\n")

        try:
            report_path = config['FILE_PATHS']['REPORT_FILE_PATH']
        except:
            raise RMPyExcep('ERROR: REPORT_FILE_PATH must be defined in the ' +
                            IniFileName + "\n\n")

        try:
            # test open the report file
            open(report_path,  mode='w', encoding='utf-8')
        except:
            raise RMPyExcep(
                'ERROR: Cannot create the report file ' + report_path + "\n\n")

    except RMPyExcep as e:
        pause_console_with_message(e)
        return 1
    except Exception as e:
        traceback.print_exception(e, file=sys.stdout)
        pause_console_with_message(
            "ERROR: Application failed. Please report.\n\n " + str(e))
        return 1

    # ===========================================DIV50==
    # Error go to Report File
    # ===========================================DIV50==

    try:

        report_file = open(report_path,  mode='w', encoding='utf-8-sig')
        report_file.write("\nReport generated at      = " +
                          time_stamp_now() + "\n")

        try:
            database_Path = config['FILE_PATHS']['DB_PATH']
            RMNOCASE_Path = config['FILE_PATHS']['RMNOCASE_PATH']
        except:
            raise RMPyExcep(
                'ERROR: Both DB_PATH and RMNOCASE_PATH must be specified.')

        if not os.path.exists(database_Path):
            raise RMPyExcep(
                'ERROR: Path for database path not found: ' + database_Path)
        if not os.path.exists(RMNOCASE_Path):
            raise RMPyExcep('ERROR: dll file not found at: ' + RMNOCASE_Path)

        # RM database file specific
        FileModificationTime = datetime.fromtimestamp(
            os.path.getmtime(database_Path))

        # Process the database for requested output
        dbConnection = create_db_connection(database_Path, RMNOCASE_Path)
        report_file.write("Report generated at      = " +
                          time_stamp_now() + "\n")
        report_file.write("Database processed       = " + database_Path + "\n")
        report_file.write("Database last changed on = " +
                          FileModificationTime.strftime("%Y-%m-%d %H:%M:%S") + "\n")
        report_file.write("SQLite library version   = " +
                          get_SQLite_library_version(dbConnection) + "\n\n")

        # test option values conversion to boolean
        try:
            config['OPTIONS'].getboolean('CHECK_TEMPLATE_NAMES')
            config['OPTIONS'].getboolean('LIST_SOURCES')
            config['OPTIONS'].getboolean('LIST_TEMPLATE_DETAILS')
            config['OPTIONS'].getboolean('MAKE_CHANGES')
        except:
            raise RMPyExcep(
                "ERROR: One of the OPTIONS values could not be parsed as boolean. \n")
            sys.exit()

        # run active options
        if config['OPTIONS'].getboolean('CHECK_TEMPLATE_NAMES'):
            check_template_names_feature(config, report_file, dbConnection)

        elif config['OPTIONS'].getboolean('LIST_TEMPLATE_DETAILS'):
            list_template_details_feature(config, report_file, dbConnection)

        elif config['OPTIONS'].getboolean('LIST_SOURCES'):
            list_sources_feature(config, report_file, dbConnection)

        elif config['OPTIONS'].getboolean('MAKE_CHANGES'):
            make_changes_feature(config, report_file, dbConnection)

    except RMPyExcep as e:
        report_file.write(str(e))
        return 1
    except Exception as e:
        traceback.print_exception(e, file=report_file)
        report_file.write("\n\n"
                          "ERROR: Application failed. Please email report file to author. ")
        return 1
    finally:
        if db_connection is not None:
            db_connection.commit()
            db_connection.close()
        report_file.close()
        if report_display_app != '':
            subprocess.Popen([report_display_app, report_path])
    return 0


# ===================================================DIV60==
def check_template_names_feature(config, reportF, dbConnection):

    try:
        oldTemplateName = config['SOURCE_TEMPLATES']['TEMPLATE_OLD']
        newTemplateName = config['SOURCE_TEMPLATES']['TEMPLATE_NEW']
    except:
        reportF.write(
            "ERROR: CHECK_TEMPLATE_NAMES option requires specification of both TEMPLATE_OLD and TEMPLATE_NEW.")
        return
    check_source_templates(reportF, dbConnection,
                         oldTemplateName, newTemplateName)
    return


# ===================================================DIV60==
def list_template_details_feature(config, reportF, dbConnection):

    try:
        oldTemplateName = config['SOURCE_TEMPLATES']['TEMPLATE_OLD']
        newTemplateName = config['SOURCE_TEMPLATES']['TEMPLATE_NEW']
        mapping = config['SOURCE_TEMPLATES']['MAPPING']
    except:
        reportF.write(
            "ERROR: LIST_TEMPLATE_DETAILS option requires specification of TEMPLATE_OLD and TEMPLATE_NEW and MAPPING.")
        return

    oldTemplateID = GetSrcTempID(dbConnection, oldTemplateName)[0][0]
    newTemplateID = GetSrcTempID(dbConnection, newTemplateName)[0][0]
    dump_src_template_fields(reportF, dbConnection, oldTemplateID)
    dump_src_template_fields(reportF, dbConnection, newTemplateID)
    reportF.write(
        "\nThe field mappings, as entered in the configuration file: \n")
    for each in mapping:
        reportF.write(each)
    reportF.write("\n\n")
    return


# ===================================================DIV60==
def list_sources_feature(config, reportF, dbConnection):

    try:
        oldTemplateName = config['SOURCE_TEMPLATES']['TEMPLATE_OLD']
        srcNamesLike = config['SOURCES']['SOURCE_NAME_LIKE']
    except:
        reportF.write(
            "ERROR: LIST_SOURCES option requires specification of both TEMPLATE_OLD and SOURCE_NAME_LIKE.")
        return
    oldTemplateID = GetSrcTempID(dbConnection, oldTemplateName)[0][0]
    reportF.write("\nSources with template name:\n" + oldTemplateName +
                  "\nand source name like:\n" + srcNamesLike + "\n\nSource #      Source Name\n\n")
    srcTuples = GetSelectedSources(
        reportF, dbConnection, oldTemplateID, srcNamesLike)
    for src in srcTuples:
        reportF.write(str(src[0]) + "    " + src[1] + "\n")
    return


# ===================================================DIV60==
def make_changes_feature(config, reportF, dbConnection):

    try:
        oldTemplateName = config['SOURCE_TEMPLATES']['TEMPLATE_OLD']
        newTemplateName = config['SOURCE_TEMPLATES']['TEMPLATE_NEW']
        srcNamesLike = config['SOURCES']['SOURCE_NAME_LIKE']
        fieldMapping = config['SOURCE_TEMPLATES']['MAPPING']
    except:
        reportF.write(
            "ERROR: MAKE_CHANGES option requires specification of TEMPLATE_OLD and TEMPLATE_NEW and SOURCE_NAME_LIKE and MAPPING.")
        return

    oldTemplateID = GetSrcTempID(dbConnection, oldTemplateName)[0][0]
    newTemplateID = GetSrcTempID(dbConnection, newTemplateName)[0][0]

    mapping = parse_field_mapping(fieldMapping)

    srcTuples = GetSelectedSources(
        reportF, dbConnection, oldTemplateID, srcNamesLike)
    for srcTuple in srcTuples:
        reportF.write(
            "=====================================================\n")
        reportF.write(str(srcTuple[0]) + "    " + srcTuple[1] + "\n")
        convert_source(reportF, dbConnection,
                      srcTuple[0], newTemplateID, mapping)
    return


# ===================================================DIV60==
def convert_source(reportF, dbConnection, srcID, newTemplateID, fieldMapping):

    # Get the SourceTable.Fields BLOB from the srcID to extract its data
    SqlStmt_src_r = """
SELECT Fields
  FROM SourceTable
 WHERE SourceID = ?
"""
    cur = dbConnection.cursor()
    cur.execute(SqlStmt_src_r, (srcID,))
    srcField = cur.fetchone()[0].decode()

    # test for and fix old style "XML" no longer used in RM8
    xmlStart = "<Root"
    rootLoc = srcField.find(xmlStart)
    if rootLoc != 0:
        srcField = srcField[rootLoc::]

    # read into DOM and parse for needed values
    srcRoot = ET.fromstring(srcField)
    newField = srcRoot.find(".//Fields")
    if newField == None:
        ET.SubElement(srcRoot, "Fields")

    # print("source XML OLD START ============================")
    # ET.indent(srcRoot)
    # ET.dump(srcRoot)
    # print("source XML OLD END ==============================")

    # change fields in source as per mapping:
    for eachMap in fieldMapping:
        if eachMap[0] == "y":
            continue

        if eachMap[1] == "NULL":
            # create a name and value pair.
            newPair = ET.SubElement(newField, "Field")
            ET.SubElement(newPair, "Name").text = eachMap[2]
            ET.SubElement(newPair, "Value")
            continue

        for eachField in srcRoot.findall('.//Field'):
            if eachField.find('Name').text == eachMap[1]:
                if eachMap[2] == "NULL":
                    # delete the unused field
                    srcRoot.find(".//Fields").remove(eachField)
                    break
                eachField.find('Name').text = eachMap[2]
                break
            # end of for eachField loop
        # end of for eachMap loop

    # print("source XML NEW START ============================")
    # ET.indent(srcRoot)
    # ET.dump(srcRoot)
    # print("source XML NEW END ==============================")
    # sys.exit()

    # Update the source with new XML and new templateID
    newSrcFields = ET.tostring(srcRoot, encoding="unicode")
    SqlStmt_src_w = """
UPDATE SourceTable
   SET Fields = ?, TemplateID = ?
 WHERE SourceID = ?
"""
    dbConnection.execute(SqlStmt_src_w, (newSrcFields, newTemplateID, srcID))

    # deal with this source's citations
    for citationTuple in get_citations_for_source(dbConnection, srcID):
        reportF.write(
            "   " + str(citationTuple[0]) + "    " + citationTuple[1][:70] + "\n")
        convert_citation(dbConnection, citationTuple[0], fieldMapping)
        # end loop for citations

    dbConnection.commit()
    return


# ===================================================DIV60==
def convert_citation(dbConnection, citationID, fieldMapping):

    # Get the CitationTable.Fields BLOB from the citation to extract its data
    SqlStmt_cit_r = """
SELECT Fields
  FROM CitationTable
 WHERE citationID = ?
"""
    cur = dbConnection.cursor()
    cur.execute(SqlStmt_cit_r, (citationID,))
    citFields = cur.fetchone()[0].decode()

    # test for and fix old style "XML" no longer used in RM8
    xmlStart = "<Root"
    rootLoc = citFields.find(xmlStart)
    if rootLoc != 0:
        citFields = citFields[rootLoc::]

    # read into DOM and parse for needed values
    citRoot = ET.fromstring(citFields)
    newField = citRoot.find(".//Fields")
    if newField == None:
        ET.SubElement(citRoot, "Fields")

    # print("citation XML OLD START ============================")
    # ET.indent(srcRoot)
    # ET.dump(srcRoot)
    # print("citation XML OLD END ==============================")
    # sys.exit()

    # change fields in citation as per mapping:
    for eachMap in fieldMapping:
        if eachMap[0] == "n":
            continue

        if eachMap[1] == "NULL":
            # create a name and value pair.
            newField = citRoot.find(".//Fields")
            newPair = ET.SubElement(newField, "Field")
            ET.SubElement(newPair, "Name").text = eachMap[2]
            ET.SubElement(newPair, "Value")
            continue

        for eachField in citRoot.findall('.//Field'):
            if eachField.find('Name').text == eachMap[1]:
                if eachMap[2] == "NULL":
                    # delete the unused field
                    citRoot.find(".//Fields").remove(eachField)
                    break
                eachField.find('Name').text = eachMap[2]
                break
        # end of for eachField loop
    # end of for eachMap loop

    # print("citation XML NEW START ============================")
    # ET.indent(srcRoot)
    # ET.dump(srcRoot)
    # print("citation XML NEW END ==============================")
    # sys.exit()

    newCitFileds = ET.tostring(citRoot, encoding="unicode")
    # Update the citation with new XML and new templateID
    SqlStmt_cit_w = """
UPDATE CitationTable
   SET Fields = ?
 WHERE CitationID = ? 
"""
    dbConnection.execute(SqlStmt_cit_w, (newCitFileds, citationID))
    return


# ===================================================DIV60==
def get_citations_for_source(dbConnection, oldSourceID):

    # get citations for oldSourceID
    SqlStmt = """
SELECT CitationID, CitationName
  FROM CitationTable
 WHERE SourceID = ?
"""
    cur = dbConnection.cursor()
    cur.execute(SqlStmt, (oldSourceID,))
    return cur.fetchall()


# ===================================================DIV60==
def parse_field_mapping(text):

    # convert string to list of 2-tuple strings
    text = text.strip()
    list = text.split('\n')
    newList = []
    for each in list:
        newList.append(tuple(each.split()))
    return newList


# ===================================================DIV60==
def get_list_of_rows(dbConnection, SqlStmt):

    # SqlStmt should return a set of single values
    cur = dbConnection.cursor()
    cur.execute(SqlStmt)

    result = []
    for t in cur:
        for x in t:
            result.append(x)
    return result


# ===================================================DIV60==
def check_source_templates(reportF, dbConnection, oldTemplateName, newTemplateName):

    if newTemplateName == oldTemplateName:
        reportF.write("The old and new template names must be different.")
        return

    IDs = []
    IDs = GetSrcTempID(dbConnection, oldTemplateName)
    if len(IDs) == 0:
        reportF.write(
            "Could not find a SourceTemplate named: " + oldTemplateName)
        return
    if len(IDs) > 1:
        reportF.write(G_QT + oldTemplateName + G_QT +
                      " is not a unique name. Edit the name in RM and try again")
        return
    reportF.write(G_QT + oldTemplateName + G_QT + " checks out OK\n")

    IDs = GetSrcTempID(dbConnection, newTemplateName)
    if len(IDs) == 0:
        reportF.write(
            "Could not find a SourceTemplate named: " + newTemplateName)
        return
    if len(IDs) > 1:
        reportF.write(G_QT + newTemplateName + G_QT +
                      " is not a unique name. Edit the name in RM and try again")
        return
    reportF.write(G_QT + newTemplateName + G_QT + " checks out OK\n")

    return


# ===================================================DIV60==
def get_src_template_ID(dbConnection, TemplateName):
    SqlStmt = """
SELECT TemplateID
  FROM SourceTemplateTable
 WHERE Name = ?
"""
    cur = dbConnection.execute(SqlStmt, (TemplateName,))
    rows = []
    rows = cur.fetchall()
    return rows


# ===================================================DIV60==
def dump_src_template_fields(reportF, dbConnection, TemplateID):
    # dump fields in Templates
    SqlStmt = """
SELECT FieldDefs, Name
  FROM SourceTemplateTable
 WHERE TemplateID = ?
"""
    cur = dbConnection.cursor()
    cur.execute(SqlStmt, (TemplateID,))
    # text = cur.fetchone()[0].decode()
    textTuple = cur.fetchone()
    templateName = textTuple[1]
    newRoot = ET.fromstring(textTuple[0].decode())

    fieldItr = newRoot.findall(".Fields/Field")
    reportF.write(templateName + "\n")
    for item in fieldItr:
        if "True" == item.find("CitationField").text:
            fieldLoc = "citation"
        else:
            fieldLoc = "source  "
        reportF.write(fieldLoc + "   " + item.find("Type").text +
                      "      " + item.find("FieldName").text + "\n")
    reportF.write("\n\n")
    return


# ===================================================DIV60==
def get_selected_sources(reportF, dbConnection, oldTemplateID, SourceNamesLike):
    SqlStmt = """
SELECT st.SourceID, st.Name
  FROM SourceTable st
  JOIN SourceTemplateTable stt ON st.TemplateID = stt.TemplateID
 WHERE st.TemplateID = ? AND st.Name LIKE ?
"""
    cur = dbConnection.cursor()
    cur.execute(SqlStmt, (oldTemplateID, SourceNamesLike))
    srcTuples = cur.fetchall()
    if len(srcTuples) == 0:
        reportF.write("No sources found with specified search criteria.\n")
        return
    return srcTuples


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
def time_stamp_now(type=""):

    # return a TimeStamp string
    now = datetime.now()
    if type == '':
        dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
    elif type == 'file':
        dt_string = now.strftime("%Y-%m-%d_%H%M%S")
    return dt_string


# ===================================================DIV60==
def pause_console_with_message(message=None):

    if (message != None):
        print(str(message))
    input("\n" "Press the <Enter> key to continue...")
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
def get_SQLite_library_version(dbConnection):

    # returns a string like 3.42.0
    SqlStmt = """
SELECT sqlite_version()
"""
    cur = dbConnection.cursor()
    cur.execute(SqlStmt)
    return cur.fetchone()[0]


# ===================================================DIV60==
class RMPyExcep(Exception):

    '''Exceptions thrown for configuration/database issues'''


# ===================================================DIV60==
# Call the "main" function
if __name__ == '__main__':
    main()
