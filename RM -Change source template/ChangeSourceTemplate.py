import os
import sys
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
# Python v3.11 or greater


# ===================================================DIV60==
#  Global Variables
G_QT = "\""
G_DEBUG = False

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
        IniFile = os.path.join(get_current_directory(), IniFileName)

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
            "ERROR: Application failed.\n\n"
            + str(e)
            + "Please email console text & ini file to author.\n\n")
        return 1

    # ===========================================DIV50==
    # Error go to Report File
    # ===========================================DIV50==

    try:

        report_file = open(report_path,  mode='w', encoding='utf-8-sig')

        try:
            database_path = config['FILE_PATHS']['DB_PATH']
        except:
            raise RMPyExcep(
                'ERROR: DB_PATH must be specified.')

        if not os.path.exists(database_path):
            raise RMPyExcep(
                'ERROR: Path for database path not found: ' + database_path)

        try:
            report_display_app = config['FILE_PATHS']['REPORT_FILE_DISPLAY_APP']
        except:
            pass
        if report_display_app != '' and not os.path.exists(report_display_app):
            input_string = report_display_app
            report_display_app = ''
            raise RMPyExcep('ERROR: Path for report-file display app not found: '
                            + input_string)

        # RM database file specific
        FileModificationTime = datetime.fromtimestamp(
            os.path.getmtime(database_path))

        # Process the database for requested output
        dbConnection = create_db_connection(database_path, None)
        report_file.write("Report generated at      = " +
                          time_stamp_now() + "\n")
        report_file.write("Database processed       = " + database_path + "\n")
        report_file.write("Database last changed on = " +
                          FileModificationTime.strftime("%Y-%m-%d %H:%M:%S") + "\n")
        report_file.write("SQLite library version   = " +
                          get_SQLite_library_version(dbConnection) + "\n\n")

        # test option values conversion to boolean
        try:
            config['OPTIONS'].getboolean('CHECK_TEMPLATE_NAMES')
            config['OPTIONS'].getboolean('LIST_SOURCES')
            config['OPTIONS'].getboolean('LIST_TEMPLATE_DETAILS')
            config['OPTIONS'].getboolean('CHECK_MAPPING_DETAILS')
            config['OPTIONS'].getboolean('MAKE_CHANGES')
        except:
            raise RMPyExcep(
                "ERROR: One of the OPTIONS values could not be parsed as boolean. \n")

        # run active options
        if config['OPTIONS'].getboolean('CHECK_TEMPLATE_NAMES'):
            check_template_names_feature(config, report_file, dbConnection)
        elif config['OPTIONS'].getboolean('LIST_SOURCES'):
            list_sources_feature(config, report_file, dbConnection)
        elif config['OPTIONS'].getboolean('LIST_TEMPLATE_DETAILS'):
            list_template_details_feature(config, report_file, dbConnection)
        elif config['OPTIONS'].getboolean('CHECK_MAPPING_DETAILS'):
            check_mapping_feature(config, report_file, dbConnection)
        elif config['OPTIONS'].getboolean('MAKE_CHANGES'):
            make_changes_feature(config, report_file, dbConnection)

    except RMPyExcep as e:
        report_file.write("\n\n" + str(e) + "\n\n")
        return 1
    except Exception as e:
        traceback.print_exception(e, file=report_file)
        report_file.write("\n\n"
                          "ERROR: Application failed. Please email report & ini file to author."
                          "\n\n")
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
def check_template_names_feature(config, report_file, dbConnection):

    try:
        old_template_name = unquote_config_string(
            config['SOURCE_TEMPLATES']['TEMPLATE_OLD'])
        new_template_name = unquote_config_string(
            config['SOURCE_TEMPLATES']['TEMPLATE_NEW'])
    except:
        raise RMPyExcep(
            "ERROR: CHECK_TEMPLATE_NAMES option requires specification"
            " of both TEMPLATE_OLD and TEMPLATE_NEW.")
    check_source_templates(report_file, dbConnection,
                           old_template_name, new_template_name)
    return


# ===================================================DIV60==
def list_template_details_feature(config, reportF, dbConnection):

    try:
        oldTemplateName = unquote_config_string(
            config['SOURCE_TEMPLATES']['TEMPLATE_OLD'])
        newTemplateName = unquote_config_string(
            config['SOURCE_TEMPLATES']['TEMPLATE_NEW'])
        mapping = config['SOURCE_TEMPLATES']['MAPPING']
    except:
        raise RMPyExcep(
            "ERROR: LIST_TEMPLATE_DETAILS option requires specification"
            " of TEMPLATE_OLD and TEMPLATE_NEW and MAPPING.")

    oldTemplateID = get_src_template_ID(dbConnection, oldTemplateName)[0][0]
    newTemplateID = get_src_template_ID(dbConnection, newTemplateName)[0][0]
    dump_src_template_fields(reportF, dbConnection, oldTemplateID)
    dump_src_template_fields(reportF, dbConnection, newTemplateID)
    reportF.write(
        "\nThe field mappings, as entered in the configuration file: \n")
    for each in mapping:
        reportF.write(each)
    reportF.write("\n\n" "Mapping after parsing." "\n\n")
    reportF.write(str(parse_field_mapping(mapping)))
    reportF.write("\n\n")

    return


# ===================================================DIV60==
def list_sources_feature(config, reportF, dbConnection):

    try:
        old_template_name = unquote_config_string(
            config['SOURCE_TEMPLATES']['TEMPLATE_OLD'])
        source_names_like = unquote_config_string(
            config['SOURCES']['SOURCE_NAME_LIKE'])
    except:
        raise RMPyExcep(
            "ERROR: LIST_SOURCES option requires specification of"
            " both TEMPLATE_OLD and SOURCE_NAME_LIKE.")

    oldTemplateID = get_src_template_ID(dbConnection, old_template_name)[0][0]
    reportF.write('\nSources with template name: "' + old_template_name + '"\n'
                  + 'and source name like: "' + source_names_like + '"\n\n'
                  + "Source #      Source Name\n\n")
    srcTuples = get_selected_sources(
        reportF, dbConnection, oldTemplateID, source_names_like)
    for src in srcTuples:
        reportF.write(str(src[0]) + "    " + src[1] + "\n")
    return


# ===================================================DIV60==
def check_mapping_feature(config, report_file, dbConnection):

    list_template_details_feature(config, report_file, dbConnection)

    try:
        old_template_name = unquote_config_string(
            config['SOURCE_TEMPLATES']['TEMPLATE_OLD'])
        new_template_name = unquote_config_string(
            config['SOURCE_TEMPLATES']['TEMPLATE_NEW'])
        field_mapping = config['SOURCE_TEMPLATES']['MAPPING']
    except:
        raise RMPyExcep(
            "ERROR: LIST_TEMPLATE_DETAILS option requires specification"
            " of TEMPLATE_OLD and TEMPLATE_NEW and MAPPING.")

    mapping = parse_field_mapping(field_mapping)

    old_template_ID = get_src_template_ID(
        dbConnection, old_template_name)[0][0]
    new_template_ID = get_src_template_ID(
        dbConnection, new_template_name)[0][0]

    new_st_fields = get_list_src_template_fields(new_template_ID, dbConnection)
    old_st_fields = get_list_src_template_fields(old_template_ID, dbConnection)

    # make lists of the 4 types of source template fields
    old_src_fields = []
    for each in old_st_fields:
        if each[1] == "source":
            old_src_fields.append(each[3])
    old_src_fields.append('NULL')

    old_cit_fields = []
    for each in old_st_fields:
        if each[1] == "citation":
            old_cit_fields.append(each[3])
    old_cit_fields.append('NULL')

    new_src_fields = []
    for each in new_st_fields:
        if each[1] == "source":
            new_src_fields.append(each[3])
    new_src_fields.append('NULL')

    new_cit_fields = []
    for each in new_st_fields:
        if each[1] == "citation":
            new_cit_fields.append(each[3])
    new_cit_fields.append('NULL')

    # Confirm that the entered mapping uses correct fields
    first_field_error = False
    for each in mapping:
        if each[0] == 'source':
            if each[1] not in old_src_fields:
                raise RMPyExcep(each[1]
                                + " is not among the source fields in the existing source template.")
            if each[2] not in new_src_fields:
                raise RMPyExcep(each[2]
                                + " is not among the citation fields in the new source template.")
        elif each[0] == 'citation':
            if each[1] not in old_cit_fields:
                raise RMPyExcep(each[1]
                                + " is not among the source fields in the existing source template.")
            if each[2] not in new_cit_fields:
                raise RMPyExcep(each[2]
                                + " is not among the citation fields in the new source template.")
        else:
            raise RMPyExcep('ERROR: at least one field mapping'
                            ' does not start with source or citation')

    for each in mapping:
        if each[1] == 'NULL' and each[2] == 'NULL':
            raise RMPyExcep('ERROR: A NULL NULL field mapping is not allowed.')

    report_file.write(
        "\n\n" "No problems detected in the specified mapping." "\n\n")
    return


# ===================================================DIV60==
def make_changes_feature(config, reportF, dbConnection):

    try:
        old_template_name = unquote_config_string(
            config['SOURCE_TEMPLATES']['TEMPLATE_OLD'])
        new_template_name = unquote_config_string(
            config['SOURCE_TEMPLATES']['TEMPLATE_NEW'])
        source_names_like = unquote_config_string(
            config['SOURCES']['SOURCE_NAME_LIKE'])
        field_mapping = config['SOURCE_TEMPLATES']['MAPPING']
    except:
        raise RMPyExcep(
            "ERROR: MAKE_CHANGES option requires specification of TEMPLATE_OLD"
             " and TEMPLATE_NEW and SOURCE_NAME_LIKE and MAPPING.")

    oldTemplateID = get_src_template_ID(dbConnection, old_template_name)[0][0]
    newTemplateID = get_src_template_ID(dbConnection, new_template_name)[0][0]

    mapping = parse_field_mapping(field_mapping)

    srcTuples = get_selected_sources(
        reportF, dbConnection, oldTemplateID, source_names_like)
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

    if G_DEBUG:
        print("source XML OLD START ============================")
        ET.indent(srcRoot)
        ET.dump(srcRoot)
        print("source XML OLD END ==============================")

    # change fields in source as per mapping:
    for transform in fieldMapping:
        if transform[0] == "citation":
            continue

        if transform[1] == "NULL":
            # create a name and empty value pair.
            newPair = ET.SubElement(newField, "Field")
            ET.SubElement(newPair, "Name").text = transform[2]
            ET.SubElement(newPair, "Value")
            continue

        for eachField in srcRoot.findall('.//Field'):
            if eachField.find('Name').text == transform[1]:
                if transform[2] == "NULL":
                    # delete the unused field
                    srcRoot.find(".//Fields").remove(eachField)
                    break
                eachField.find('Name').text = transform[2]
                break
            # end of for eachField loop
        # end of for each transform loop

    if G_DEBUG:
        print("source XML NEW START ============================")
        ET.indent(srcRoot)
        ET.dump(srcRoot)
        print("source XML NEW END ==============================")

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

    if G_DEBUG:
        print("citation XML OLD START ============================")
        ET.indent(citRoot)
        ET.dump(citRoot)
        print("citation XML OLD END ==============================")

    # change fields in citation as per mapping:
    for transform in fieldMapping:
        if transform[0] == "source":
            continue
        if transform[1] == "NULL":
            # create a name and value pair.
            newField = citRoot.find(".//Fields")
            newPair = ET.SubElement(newField, "Field")
            ET.SubElement(newPair, "Name").text = transform[2]
            ET.SubElement(newPair, "Value")
            continue

        for eachField in citRoot.findall('.//Field'):
            if eachField.find('Name').text == transform[1]:
                if transform[2] == "NULL":
                    # delete the unused field
                    citRoot.find(".//Fields").remove(eachField)
                    break
                eachField.find('Name').text = transform[2]
                break
        # end of for eachField loop
    # end of for each transform loop

    if G_DEBUG:
        print("citation XML NEW START ============================")
        ET.indent(citRoot)
        ET.dump(citRoot)
        print("citation XML NEW END ==============================")

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
def OLD_parse_field_mapping(text):

    # convert string to list of 3-tuple strings
    text = text.strip()
    list = text.split('\n')
    newList = []
    for each in list:
        newList.append(tuple(each.split()))
    return newList

# ===================================================DIV60==
def parse_field_mapping(instr):

    text = instr.strip()
    list = text.split('\n')
    newList = []
    for each in list:
        if each.count('"') == 0:
            newList.append(tuple(each.split()))
        else:
            if each.count('"') != 6:
                raise RMPyExcep(
                    "ERROR: mapping line hmust have 0 or 6 quote chars.")
            new_line_list = []
            for sub in each.split('"'):
                if sub.strip() != '':
                    new_line_list.append(sub)
            if len(new_line_list) != 3:
                raise RMPyExcep("ERROR: failed to parse map line with quotes.")
            newList.append(tuple(new_line_list))
    return newList


# ===================================================DIV60==
def unquote_config_string(instr):
    
    # deals with names with leading and/or trailing space or quote characters
    # name must be enclosed in quotes.
    # can't deal with names containing both kinds of quotes and spaces !!
    if instr.count('"') == 0 and instr.count("'") == 0:
        return instr
    else:
        if instr[0] == '"':
            return instr.replace('"', '')
        elif instr[0] == "'":
            return instr.replace("'", '')


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
    IDs = get_src_template_ID(dbConnection, oldTemplateName)
    if len(IDs) == 0:
        reportF.write(
            "Could not find a SourceTemplate named: " + oldTemplateName)
        return
    if len(IDs) > 1:
        reportF.write(G_QT + oldTemplateName + G_QT +
                      " is not a unique name. Edit the name in RM and try again")
        return
    reportF.write(G_QT + oldTemplateName + G_QT + " checks out OK\n")

    IDs = get_src_template_ID(dbConnection, newTemplateName)
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
 WHERE Name = ? COLLATE NOCASE
"""
    cur = dbConnection.execute(SqlStmt, (TemplateName,))
    rows = []
    rows = cur.fetchall()
    return rows


# ===================================================DIV60==
def dump_src_template_fields(reportF, dbConnection, TemplateID):

    field_list = get_list_src_template_fields(TemplateID, dbConnection)
    reportF.write(field_list[0][0] + "\n")
    for item in field_list:
        reportF.write(item[1] + '   ' + item[2] + '     "' + item[3] + '"\n')
    reportF.write("\n\n")

    for item in field_list:
        if item[3].count(" ") != 0:
            reportF.write("NOTE: At least one field name above has leading, trailing"
                          " or embedded whitespace !! See ReadMe file for help.")
            reportF.write("\n\n")
            break
    return


# ===================================================DIV60==
def get_list_src_template_fields(TemplateID, dbConnection):

    SqlStmt = """
SELECT FieldDefs, Name
  FROM SourceTemplateTable
 WHERE TemplateID = ?
"""
    cur = dbConnection.cursor()
    cur.execute(SqlStmt, (TemplateID,))
    textTuple = cur.fetchone()
    newRoot = ET.fromstring(textTuple[0].decode())
    st_name = textTuple[1]
    field_list = []

    fieldItr = newRoot.findall(".Fields/Field")
    for item in fieldItr:
        if "True" == item.find("CitationField").text:
            fieldLoc = "citation"
        else:
            fieldLoc = "source"
        field_list.append(
            (st_name, fieldLoc, item.find("Type").text, item.find("FieldName").text)
        )

    return field_list


# ===================================================DIV60==
def get_selected_sources(reportF, dbConnection, oldTemplateID, SourceNamesLike):
    SqlStmt = """
SELECT st.SourceID, st.Name
  FROM SourceTable st
  JOIN SourceTemplateTable stt ON st.TemplateID = stt.TemplateID
 WHERE st.TemplateID = ? AND st.Name LIKE ?   COLLATE NOCASE
"""
    cur = dbConnection.cursor()
    cur.execute(SqlStmt, (oldTemplateID, SourceNamesLike))
    srcTuples = cur.fetchall()
    if len(srcTuples) == 0:
        raise RMPyExcep("No sources found with specified search criteria.\n")
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
    SqlStmt = "SELECT sqlite_version()"
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

# ===================================================DIV60==
