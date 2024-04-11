import os
import sys
import sqlite3
from pathlib import Path
from datetime import datetime
import configparser  # https://docs.python.org/3/library/configparser.html
import xml.etree.ElementTree as ET
import subprocess
import traceback

# Requirements: (see ReadMe.txt for details)
# RootsMagic v9 database file
# RM-Python-config.ini  ( Configuration ini file to set options and parameters)
# Python v3.11 or greater

# ===================================================DIV60==
#  Global Variables
G_DEBUG = False

# ===================================================DIV60==


def main():

    # Configuration
    IniFileName = "RM-Python-config.ini"
    db_connection = None
    report_display_app = ''

    # ===========================================DIV50==
    # Errors go to console window
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
                            IniFileName + '\n\n')

        try:
            # test open the report file
            open(report_path,  mode='w', encoding='utf-8')
        except:
            raise RMPyExcep(
                'ERROR: Cannot create the report file: ' + q_str(report_path) + '\n\n')

    except RMPyExcep as e:
        pause_console_with_message(e)
        return 1
    except Exception as e:
        traceback.print_exception(e, file=sys.stdout)
        pause_console_with_message(
            'ERROR: Application failed.\n\n'
            + str(e)
            + 'Please email console text & ini file to author.\n\n')
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
        if report_display_app != '' and not os.path.exists(report_display_app):
            input_string = report_display_app
            report_display_app = ''
            raise RMPyExcep('ERROR: Path for report-file display app not found: '
                            + input_string)

        try:
            database_path = config['FILE_PATHS']['DB_PATH']
        except:
            raise RMPyExcep(
                'ERROR: DB_PATH must be specified.')

        if not os.path.exists(database_path):
            raise RMPyExcep(
                'ERROR: Path for database path not found: ' + database_path)
        # RM database file specific
        FileModificationTime = datetime.fromtimestamp(
            os.path.getmtime(database_path))

        # Process the database for requested output
        dbConnection = create_db_connection(database_path, None)
        report_file.write("Report generated at      = " +
                          time_stamp_now() + '\n')
        report_file.write("Database processed       = " + database_path + '\n')
        report_file.write("Database last changed on = " +
                          FileModificationTime.strftime("%Y-%m-%d %H:%M:%S") + '\n')
        report_file.write("SQLite library version   = " +
                          get_SQLite_library_version(dbConnection) + '\n\n')

        # test option values conversion to boolean
        try:
            config['OPTIONS'].getboolean('CHECK_TEMPLATE_NAMES')
            config['OPTIONS'].getboolean('LIST_SOURCES')
            config['OPTIONS'].getboolean('LIST_TEMPLATE_DETAILS')
            config['OPTIONS'].getboolean('CHECK_MAPPING_DETAILS')
            config['OPTIONS'].getboolean('MAKE_CHANGES')
        except:
            raise RMPyExcep(
                'ERROR: One of the OPTIONS values could not be parsed as boolean. \n')

        # run active options
        if config['OPTIONS'].getboolean('CHECK_TEMPLATE_NAMES'):
            check_template_names_feature(config, report_file, dbConnection)
        elif config['OPTIONS'].getboolean('LIST_SOURCES'):
            list_sources_feature(config, report_file, dbConnection)
        elif config['OPTIONS'].getboolean('LIST_TEMPLATE_DETAILS'):
            list_template_details_feature(
                config, report_file, dbConnection, False)
        elif config['OPTIONS'].getboolean('CHECK_MAPPING_DETAILS'):
            check_mapping_feature(config, report_file, dbConnection)
        elif config['OPTIONS'].getboolean('MAKE_CHANGES'):
            make_changes_feature(config, report_file, dbConnection)
    except RMPyExcep as e:
        report_file.write('\n\n' + str(e) + '\n\n')
        return 1
    except (Exception, sqlite3.OperationalError) as e:
        traceback.print_exception(e, file=report_file)
        report_file.write('n\n' 'ERROR: Application failed. Please email '
                          'report & ini file to author.' '\n\n')
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
def list_template_details_feature(config, reportF, dbConnection, include_mapping):

    try:
        oldTemplateName = unquote_config_string(
            config['SOURCE_TEMPLATES']['TEMPLATE_OLD'])
        newTemplateName = unquote_config_string(
            config['SOURCE_TEMPLATES']['TEMPLATE_NEW'])

        mapping_source = config['SOURCE_TEMPLATES']['MAPPING_SOURCE']
        mapping_citation = config['SOURCE_TEMPLATES']['MAPPING_CITATION']

    except:
        raise RMPyExcep(
            "ERROR: LIST_TEMPLATE_DETAILS option requires specification"
            " of TEMPLATE_OLD and TEMPLATE_NEW, MAPPING_SOURCE & MAPPING_CITATION.")

    old_template_ID = get_src_template_ID(dbConnection, oldTemplateName)[0][0]
    new_template_ID = get_src_template_ID(dbConnection, newTemplateName)[0][0]
    dump_src_template_fields(reportF, dbConnection, old_template_ID)
    dump_src_template_fields(reportF, dbConnection, new_template_ID)

    if include_mapping:
        reportF.write(
            '\nThe field mappings, as entered in the configuration file:\n\n')
        reportF.write('Source mapping:\n')

        for each in mapping_source:
            reportF.write(each)
        reportF.write('\n\nCitation mapping:\n')
        for each in mapping_citation:
            reportF.write(each)
        reportF.write('\n\n')

    if G_DEBUG:
        reportF.write('\n\nSource fields:\n')
        reportF.write(str(parse_field_mapping(mapping_source)))
        reportF.write('Source fields:\n')
        reportF.write(str(parse_field_mapping(mapping_citation)))

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
    reportF.write('\nSources with template name: ' + q_str(old_template_name) + '\n'
                  + 'and source name like: ' +
                  q_str(source_names_like) + '\n\n'
                  + "Source #      Source Name\n\n")
    srcTuples = get_selected_sources(
        reportF, dbConnection, oldTemplateID, source_names_like)
    for src in srcTuples:
        reportF.write(str(src[0]) + '     ' + src[1] + '\n')
    return


# ===================================================DIV60==
def check_mapping_feature(config, report_file, dbConnection):

    # confirms each fielsd in mapping appears in the corresponding
    # template description
    list_template_details_feature(config, report_file, dbConnection, True)

    try:
        old_template_name = unquote_config_string(
            config['SOURCE_TEMPLATES']['TEMPLATE_OLD'])
        new_template_name = unquote_config_string(
            config['SOURCE_TEMPLATES']['TEMPLATE_NEW'])
        mapping_source = config['SOURCE_TEMPLATES']['MAPPING_SOURCE']
        mapping_citation = config['SOURCE_TEMPLATES']['MAPPING_CITATION']

    except:
        raise RMPyExcep(
            "ERROR: LIST_TEMPLATE_DETAILS option requires specification"
            " of TEMPLATE_OLD and TEMPLATE_NEW, MAPPING_SOURCE & MAPPING_CITATION.")

    field_mapping_source = parse_field_mapping(mapping_source)
    field_mapping_citation = parse_field_mapping(mapping_citation)

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
    for each in field_mapping_source:
        if each[0] not in old_src_fields:
            raise RMPyExcep(q_str(each[0])
                            + ' is not among the source fields in the existing source template.')
        if each[1] not in new_src_fields:
            raise RMPyExcep(q_str(each[1])
                            + ' is not among the citation fields in the new source template.')

    for each in field_mapping_citation:
        if each[0] not in old_cit_fields:
            raise RMPyExcep(q_str(each[0])
                            + ' is not among the source fields in the existing source template.')
        if each[1] not in new_cit_fields:
            raise RMPyExcep(q_str(each[1])
                            + ' is not among the citation fields in the new source template.')

    for each in field_mapping_source:
        if each[0] == 'NULL' and each[1] == 'NULL':
            raise RMPyExcep('ERROR: A NULL NULL field mapping is not allowed.')
    for each in field_mapping_citation:
        if each[0] == 'NULL' and each[1] == 'NULL':
            raise RMPyExcep('ERROR: A NULL NULL field mapping is not allowed.')

    report_file.write(
        "\n\n" "No problems detected in the specified mapping." '\n\n')
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
        mapping_source = config['SOURCE_TEMPLATES']['MAPPING_SOURCE']
        mapping_citation = config['SOURCE_TEMPLATES']['MAPPING_CITATION']
    except:
        raise RMPyExcep(
            "ERROR: MAKE_CHANGES option requires specification of TEMPLATE_OLD"
            " TEMPLATE_NEW, SOURCE_NAME_LIKE, MAPPING_SOURCE & MAPPING_CITATION.")

    oldTemplateID = get_src_template_ID(dbConnection, old_template_name)[0][0]
    newTemplateID = get_src_template_ID(dbConnection, new_template_name)[0][0]

    field_mapping_source = parse_field_mapping(mapping_source)
    field_mapping_citation = parse_field_mapping(mapping_citation)

    srcTuples = get_selected_sources(
        reportF, dbConnection, oldTemplateID, source_names_like)
    for srcTuple in srcTuples:
        reportF.write(
            '=====================================================\n')
        reportF.write(str(srcTuple[0]) + "    " + srcTuple[1] + '\n')
        convert_source(reportF, dbConnection, srcTuple[0],
                       newTemplateID, field_mapping_source, field_mapping_citation)
    return


# ===================================================DIV60==
def convert_source(reportF, dbConnection, srcID, newTemplateID,
                   field_mapping_source, field_mapping_citation):

    root_element = get_root_element(dbConnection, SourceID=srcID)
    fields_element = root_element.find(".//Fields")
   # change fields in source as per mapping:
    for transform in field_mapping_source:
        if transform[0] == transform[1]:
            continue
        if transform[0] == "NULL":
            # check whether field transform[1] exists as a Name
            if root_element.find("Fields/Field[Name='" + transform[1] + "']") == None:
                # if it does not exist, create it
                # create a name and empty value pair.
                newPair = ET.SubElement(fields_element, "Field")
                ET.SubElement(newPair, "Name").text = transform[1]
                ET.SubElement(newPair, "Value")
            else:
                raise RMPyExcep(
                    "Tried to create duplicate Name in source XML.NULL on left")
            continue
        for eachField in fields_element.findall('.//Field'):
            if eachField.find('Name').text == transform[0]:
                if transform[1] == "NULL":
                    # delete the unused field
                    fields_element.remove(eachField)
                    break
                if root_element.find("Fields/Field[Name='" + transform[1] + "']") == None:
                    eachField.find('Name').text = transform[1]
                else:
                    raise RMPyExcep(
                        "Tried to create duplicate Name in source XML.")
                break
            # end of for eachField loop
        # end of for each transform loop

    if G_DEBUG:
        print("source XML NEW START ============================")
        ET.indent(root_element)
        ET.dump(root_element)
        print("source XML NEW END ==============================")

    # Update the source with new XML and new templateID
    newSrcFields = ET.tostring(root_element, encoding="unicode")
    SqlStmt_src_w = """
UPDATE SourceTable
   SET Fields = ?, TemplateID = ?
 WHERE SourceID = ?
"""
    dbConnection.execute(SqlStmt_src_w, (newSrcFields, newTemplateID, srcID))

    # deal with this source's citations
    for citationTuple in get_citations_of_source(dbConnection, srcID):
        reportF.write(
            "   " + q_str(str(citationTuple[0])) + "    " + citationTuple[1][:70] + '\n')
        convert_citation(
            dbConnection, citationTuple[0], field_mapping_citation)
        # end loop for citations

    dbConnection.commit()
    return


# ===================================================DIV60==
def convert_citation(dbConnection, citation_ID, field_mapping_citation):

    root_element = get_root_element(dbConnection, None, citation_ID)
    fields_element = root_element.find(".//Fields")

    if G_DEBUG:
        print("citation XML OLD START ============================")
        ET.indent(root_element)
        ET.dump(root_element)
        print("citation XML OLD END ==============================")

    # change fields in citation as per mapping:
    for transform in field_mapping_citation:
        if transform[0] == transform[1]:
            continue
        if transform[0] == "NULL":
            # check whether field transform[1] exists as a Name
            if root_element.find("Fields/Field[Name='" + transform[1] + "']") == None:
                # if it does not exist, create it
                # create a name and empty value pair.
                newPair = ET.SubElement(fields_element, "Field")
                ET.SubElement(newPair, "Name").text = transform[1]
                ET.SubElement(newPair, "Value")
            else:
                raise RMPyExcep(
                    "Tried to create duplicate Name in citation XML. NULL on left")
            continue
            # create a name and value pair.
            newPair = ET.SubElement(fields_element, "Field")
            ET.SubElement(newPair, "Name").text = transform[1]
            ET.SubElement(newPair, "Value")
            continue

        for eachField in fields_element.findall('.//Field'):
            if eachField.find('Name').text == transform[0]:
                if transform[1] == "NULL":
                    # delete the unused field
                    root_element.find(".//Fields").remove(eachField)
                    break
                if root_element.find("Fields/Field[Name='" + transform[1] + "']") == None:
                    eachField.find('Name').text = transform[1]
                else:
                    raise RMPyExcep(
                        "Tried to create duplicate Name in citation XML.")
                break
        # end of for eachField loop
    # end of for each transform loop

    if G_DEBUG:
        print("citation XML NEW START ============================")
        ET.indent(root_element)
        ET.dump(root_element)
        print("citation XML NEW END ==============================")

    newCitFileds = ET.tostring(root_element, encoding="unicode")
    # Update the citation with new XML and new templateID
    SqlStmt = """
UPDATE CitationTable
   SET Fields = ?
 WHERE CitationID = ? 
"""
    dbConnection.execute(SqlStmt, (newCitFileds, citation_ID))
    return


# ===================================================DIV60==
def get_root_element(dbConnection, SourceID=None, CitationID=None):

    # Get the Table.Fields BLOB from the ID to extract its data
    if SourceID is not None:
        ID = SourceID
        SqlStmt = """
SELECT Fields
  FROM SourceTable
 WHERE SourceID = ?
"""
    elif CitationID is not None:
        ID = CitationID
        SqlStmt = """
SELECT Fields
  FROM CitationTable
 WHERE CitationID = ?
"""
    else:
        raise RMPyExcep("ERROR internal: both inputs None")

    cur = dbConnection.cursor()
    cur.execute(SqlStmt, (ID,))
    xml_text = cur.fetchone()[0].decode()

    # test for and "fix" old style XML no longer used in RMv>=8
    xml_real_start_chars = "<Root"
    root_location = xml_text.find(xml_real_start_chars)
    xml_text = xml_text[root_location::]

    # Extraneous characters are not read into DOM or written back
    # Read into DOM and parse for needed values
    root_element = ET.fromstring(xml_text)
    fields_element = root_element.find(".//Fields")

    # Fix XML that is missing the Fields element
    if fields_element == None:
        ET.SubElement(root_element, "Fields")

    return root_element


# ===================================================DIV60==
def get_citations_of_source(dbConnection, oldSourceID):

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
def parse_field_mapping(in_str):

    # convert string to list of lists (of 3 strings)
    in_str = in_str.strip()
    list_of_lines = in_str.splitlines()
    list_of_lists = []
    for each_line in list_of_lines:
        item_set = list(each_line.split())
        item_set = [x.strip('"') for x in item_set]
        list_of_lists.append(item_set)
    return list_of_lists


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


def q_str(in_str):
    return '"' + in_str + '"'

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
            'Could not find a SourceTemplate named: ' + q_str(oldTemplateName))
        return
    if len(IDs) > 1:
        reportF.write(q_str(oldTemplateName) +
                      " is not a unique name. Edit the name in RM and try again")
        return
    reportF.write(q_str(oldTemplateName) + " checks out OK\n")

    IDs = get_src_template_ID(dbConnection, newTemplateName)
    if len(IDs) == 0:
        reportF.write(
            'Could not find a SourceTemplate named: ' + q_str(newTemplateName))
        return
    if len(IDs) > 1:
        reportF.write(q_str(newTemplateName)
                      + " is not a unique name. Edit the name in RM and try again")
        return
    reportF.write(q_str(newTemplateName) + " checks out OK\n")

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
    reportF.write(field_list[0][0] + '\n')
    for item in field_list:
        reportF.write(item[1] + '   ' + item[2] +
                      '     ' + q_str(item[3]) + '\n')
    reportF.write('\n\n')

    for item in field_list:
        if item[3].count(" ") != 0:
            reportF.write("NOTE: At least one field name above has leading, trailing"
                          " or embedded whitespace !! See ReadMe file for help.")
            reportF.write('\n\n')
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
    input('\n' "Press the <Enter> key to continue...")
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
        raise RMPyExcep(e, '\n\n' "Cannot open the RM database file." '\n')
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
