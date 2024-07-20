import os
import sys
import xml.etree.ElementTree as ET

sys.path.append( r'..\\RM -RMpy package' )
import RMpy.launcher # type: ignore
import RMpy.common as RMpyCom # type: ignore

# Requirements:
#   RootsMagic database file
#   RM-Python-config.ini

# Tested with:
#   RootsMagic database file v10.0.0
#   Python for Windows v3.12.3

# Config file fields used
#    FILE_PATHS  REPORT_FILE_PATH
#    FILE_PATHS  REPORT_FILE_DISPLAY_APP
#    FILE_PATHS  DB_PATH
#
#    SOURCE_TEMPLATES   TEMPLATE_OLD
#    SOURCE_TEMPLATES   TEMPLATE_NEW
#    SOURCE_TEMPLATES   MAPPING_SOURCE
#    SOURCE_TEMPLATES   MAPPING_CITATION
#    SOURCES            SOURCE_NAME_LIKE
#
#    OPTIONS     CHECK_TEMPLATE_NAMES
#    OPTIONS     LIST_SOURCES
#    OPTIONS     LIST_TEMPLATE_DETAILS
#    OPTIONS     CHECK_MAPPING_DETAILS
#    OPTIONS     MAKE_CHANGES


# ====================================DIV60==
#  Global Variables
G_DEBUG = False


# ===================================================DIV60==
def main():

    # Configuration
    config_file_name = "RM-Python-config.ini"
    RMNOCASE_required = True
    allow_db_changes = True

    RMpy.launcher.launcher(os.path.dirname(__file__),
                    config_file_name,
                    RMNOCASE_required,
                    allow_db_changes,
                    run_selected_features)


# ===================================================DIV60==
def run_selected_features(config, db_connection, report_file):

    # test option values conversion to boolean
    try:
        config['OPTIONS'].getboolean('CHECK_TEMPLATE_NAMES')
        config['OPTIONS'].getboolean('LIST_SOURCES')
        config['OPTIONS'].getboolean('LIST_TEMPLATE_DETAILS')
        config['OPTIONS'].getboolean('CHECK_MAPPING_DETAILS')
        config['OPTIONS'].getboolean('MAKE_CHANGES')
    except:
        raise RMpyCom.RM_Py_Exception(
            'ERROR: One of the OPTIONS values could not be parsed as boolean. \n')

    # run active options
    if config['OPTIONS'].getboolean('CHECK_TEMPLATE_NAMES'):
        check_template_names_feature(config, report_file, db_connection)
    elif config['OPTIONS'].getboolean('LIST_SOURCES'):
        list_sources_feature(config, report_file, db_connection)
    elif config['OPTIONS'].getboolean('LIST_TEMPLATE_DETAILS'):
        list_template_details_feature(
            config, report_file, db_connection, False)
    elif config['OPTIONS'].getboolean('CHECK_MAPPING_DETAILS'):
        check_mapping_feature(config, report_file, db_connection)
    elif config['OPTIONS'].getboolean('MAKE_CHANGES'):
        make_changes_feature(config, report_file, db_connection)


# ===================================================DIV60==
def check_template_names_feature(config, report_file, dbConnection):

    try:
        old_template_name = unquote_config_string(
            config['SOURCE_TEMPLATES']['TEMPLATE_OLD'])
        new_template_name = unquote_config_string(
            config['SOURCE_TEMPLATES']['TEMPLATE_NEW'])
    except:
        raise RMpyCom.RM_Py_Exception(
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
        raise RMpyCom.RM_Py_Exception(
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
        raise RMpyCom.RM_Py_Exception(
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

    # confirms each field in mapping appears in the corresponding
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
        raise RMpyCom.RM_Py_Exception(
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
    for each in field_mapping_source:
        if each[0] not in old_src_fields:
            raise RMpyCom.RM_Py_Exception(q_str(each[0])
                                  + ' is not among the source fields in the existing source template.')
        if each[1] not in new_src_fields:
            raise RMpyCom.RM_Py_Exception(q_str(each[1])
                                  + ' is not among the citation fields in the new source template.')

    for each in field_mapping_citation:
        if each[0] not in old_cit_fields:
            raise RMpyCom.RM_Py_Exception(q_str(each[0])
                                  + ' is not among the source fields in the existing source template.')
        if each[1] not in new_cit_fields:
            raise RMpyCom.RM_Py_Exception(q_str(each[1])
                                  + ' is not among the citation fields in the new source template.')

    for each in field_mapping_source:
        if each[0] == 'NULL' and each[1] == 'NULL':
            raise RMpyCom.RM_Py_Exception(
                'ERROR: A NULL NULL field mapping is not allowed.')
    for each in field_mapping_citation:
        if each[0] == 'NULL' and each[1] == 'NULL':
            raise RMpyCom.RM_Py_Exception(
                'ERROR: A NULL NULL field mapping is not allowed.')

    report_file.write(
        "\n\n" "No problems detected in the specified mapping." '\n\n')
    return


# ===================================================DIV60==
def make_changes_feature(config, reportF, dbConnection):

    if config['CITATIONS'].getboolean('EMPTY_CIT_NAME'):
        reindex_RMNOCASE(dbConnection)

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
        raise RMpyCom.RM_Py_Exception(
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
        convert_source(reportF, dbConnection, srcTuple[0], newTemplateID, 
                       field_mapping_source, field_mapping_citation, config)
    return


# ===================================================DIV60==
def convert_source(reportF, dbConnection, srcID, newTemplateID,
                   field_mapping_source, field_mapping_citation, config):

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
                raise RMpyCom.RM_Py_Exception(
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
                    raise RMpyCom.RM_Py_Exception(
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
            dbConnection, citationTuple[0], field_mapping_citation, config)
        # end loop for citations

    dbConnection.commit()
    return


# ===================================================DIV60==
def convert_citation(dbConnection, citation_ID, field_mapping_citation, config):

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
                raise RMpyCom.RM_Py_Exception(
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
                    raise RMpyCom.RM_Py_Exception(
                        "Tried to create duplicate Name in citation XML.")
                break
        # end of for eachField loop
    # end of for each transform loop

    if G_DEBUG:
        print("citation XML NEW START ============================")
        ET.indent(root_element)
        ET.dump(root_element)
        print("citation XML NEW END ==============================")

    newCitFields = ET.tostring(root_element, encoding="unicode")
    # Update the citation with new XML and new templateID
    SqlStmt = """
UPDATE CitationTable
   SET Fields = ?
 WHERE CitationID = ? 
"""
    dbConnection.execute(SqlStmt, (newCitFields, citation_ID))
    if config['CITATIONS'].getboolean('EMPTY_CIT_NAME'):
        empty_citation_name(citation_ID, dbConnection)
    return


# ===================================================DIV60==
def reindex_RMNOCASE(dbConnection):
    SqlStmt = """
REINDEX RMNOCASE
"""
    cur = dbConnection.cursor()
    cur.execute(SqlStmt, ())


# ===================================================DIV60==
def empty_citation_name(CitationID, dbConnection):
    SqlStmt = """
UPDATE CitationTable
  SET CitationName = ''
 WHERE CitationID = ?
"""
    cur = dbConnection.cursor()
    cur.execute(SqlStmt, (CitationID,))


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
        raise RMpyCom.RM_Py_Exception("ERROR internal: both inputs None")

    cur = dbConnection.cursor()
    cur.execute(SqlStmt, (ID,))
    xml_text = cur.fetchone()[0]
    if type(xml_text) is not str:
        xml_text=xml_text.decode('utf-8')

    # test for and "fix" old style XML no longer used in RMv>=8
    xml_real_start_string = "<Root"
    root_location = xml_text.find(xml_real_start_string)
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
        item_set = list(each_line.split(sep='>'))
        item_set = [x.strip() for x in item_set]
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
        raise RMpyCom.RM_Py_Exception(
            "No sources found with specified search criteria.\n")
    return srcTuples


# ===================================================DIV60==
# Call the "main" function
if __name__ == '__main__':
    main()

# ===================================================DIV60==
