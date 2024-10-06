import sys
sys.path.append(r'..\RM -RMpy package')
import RMpy.launcher          # type: ignore
import RMpy.common as RMc     # type: ignore
from RMpy.common import q_str # type: ignore

import os
import xml.etree.ElementTree as ET


# Requirements:
#   RootsMagic database file
#   RM-Python-config.ini

# Tested with:
#   RootsMagic database file v10
#   Python for Windows v3.12

# Config file fields used
#    FILE_PATHS  DB_PATH
#    FILE_PATHS  REPORT_FILE_PATH
#    FILE_PATHS  REPORT_FILE_DISPLAY_APP
#
#    OPTIONS     CHECK_TEMPLATE_NAMES
#    OPTIONS     LIST_SOURCES
#    OPTIONS     LIST_TEMPLATE_DETAILS
#    OPTIONS     CHECK_MAPPING_DETAILS
#    OPTIONS     MAKE_CHANGES
#
#    SOURCE_TEMPLATES   TEMPLATE_OLD
#    SOURCE_TEMPLATES   TEMPLATE_NEW
#
#    SOURCES            SOURCE_NAME_LIKE
#
#    FIELD_MAP          MAPPING_SOURCE
#    FIELD_MAP          MAPPING_CITATION



# ====================================DIV60==
#  Global Variables
G_DEBUG = False


# ===================================================DIV60==
def main():

    # Configuration
    config_file_name = "RM-Python-config.ini"
    RMNOCASE_required = False
    allow_db_changes = True
    RegExp_required = False

    RMpy.launcher.launcher(os.path.dirname(__file__),
                    config_file_name,
                    run_selected_features,
                    allow_db_changes,
                    RMNOCASE_required,
                    RegExp_required )


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
        raise RMc.RM_Py_Exception(
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
        raise RMc.RM_Py_Exception(
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

        mapping_source = config['FIELD_MAP']['MAPPING_SOURCE']
        mapping_citation = config['FIELD_MAP']['MAPPING_CITATION']

    except:
        raise RMc.RM_Py_Exception(
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
        raise RMc.RM_Py_Exception(
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
        mapping_source = config['FIELD_MAP']['MAPPING_SOURCE']
        mapping_citation = config['FIELD_MAP']['MAPPING_CITATION']

    except:
        raise RMc.RM_Py_Exception(
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
            raise RMc.RM_Py_Exception(q_str(each[0])
                                  + ' is not among the source fields in the existing source template.')
        if each[1] not in new_src_fields:
            raise RMc.RM_Py_Exception(q_str(each[1])
                                  + ' is not among the citation fields in the new source template.')

    for each in field_mapping_citation:
        if each[0] not in old_cit_fields:
            raise RMc.RM_Py_Exception(q_str(each[0])
                                  + ' is not among the source fields in the existing source template.')
        if each[1] not in new_cit_fields:
            raise RMc.RM_Py_Exception(q_str(each[1])
                                  + ' is not among the citation fields in the new source template.')

    for each in field_mapping_source:
        if each[0] == 'NULL' and each[1] == 'NULL':
            raise RMc.RM_Py_Exception(
                'ERROR: A NULL NULL field mapping is not allowed.')
    for each in field_mapping_citation:
        if each[0] == 'NULL' and each[1] == 'NULL':
            raise RMc.RM_Py_Exception(
                'ERROR: A NULL NULL field mapping is not allowed.')

    report_file.write(
        "\n\n" "No problems detected in the specified mapping." '\n\n')
    return


# ===================================================DIV60==
def make_changes_feature(config, reportF, dbConnection):

    # TODO requires RMNOCASE. Do this in another utility.
    # if config['CITATIONS'].getboolean('EMPTY_CIT_NAME'):
    #     RMc.reindex_RMNOCASE(dbConnection)

    try:
        old_template_name = unquote_config_string(
            config['SOURCE_TEMPLATES']['TEMPLATE_OLD'])
        new_template_name = unquote_config_string(
            config['SOURCE_TEMPLATES']['TEMPLATE_NEW'])
        source_names_like = unquote_config_string(
            config['SOURCES']['SOURCE_NAME_LIKE'])
        mapping_source = config['FIELD_MAP']['MAPPING_SOURCE']
        mapping_citation = config['FIELD_MAP']['MAPPING_CITATION']
        # TODO confirm empty citation name boolean
    except:
        raise RMc.RM_Py_Exception(
            "ERROR: MAKE_CHANGES option requires specification of TEMPLATE_OLD"
            " TEMPLATE_NEW, SOURCE_NAME_LIKE, MAPPING_SOURCE & MAPPING_CITATION.")

    oldTemplateID = get_src_template_ID(dbConnection, old_template_name)[0][0]
    newTemplateID = get_src_template_ID(dbConnection, new_template_name)[0][0]

    field_mapping_source = parse_field_mapping(mapping_source)
    field_mapping_citation = parse_field_mapping(mapping_citation)

    # srcTuples has a subset of sourceTable rows and columns
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

    adjust_xml_fields(field_mapping_source, root_element)

    if G_DEBUG:
        print("source XML NEW START ============================")
        ET.indent(root_element)
        ET.dump(root_element)
        print("source XML NEW END ==============================")

    # deal with this source's citations
    for citationTuple in get_citations_of_source(dbConnection, srcID):
        reportF.write(
            "   " + q_str(str(citationTuple[0])) + "    " + citationTuple[1][:70] + '\n')
        convert_citation(
            citationTuple[0], field_mapping_citation, config, dbConnection)
        # end loop for citations

    # Update the source with new XML and new templateID
    newSrcFields = ET.tostring(root_element, encoding="unicode")
    SqlStmt_src_w = """
UPDATE SourceTable
   SET Fields = ?, TemplateID = ?
 WHERE SourceID = ?
"""
    dbConnection.execute(SqlStmt_src_w, (newSrcFields, newTemplateID, srcID))

    dbConnection.commit()
    return


# ===================================================DIV60==
def convert_citation(citation_ID, field_mapping_citation, config, dbConnection):

    root_element = get_root_element(dbConnection, None, citation_ID)

    if G_DEBUG:
        print("citation XML OLD START ============================")
        ET.indent(root_element)
        ET.dump(root_element)
        print("citation XML OLD END ==============================")

    adjust_xml_fields(field_mapping_citation, root_element)

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
    #  requires RMNOCASE. Do this in a different utility. TODO
    #  if config['CITATIONS'].getboolean('EMPTY_CIT_NAME'):
    #      empty_citation_name(citation_ID, dbConnection)
    return


# ===================================================DIV60==
def adjust_xml_fields(field_mapping, root_element):

    fields_element = root_element.find(".//Fields")
    # change fields in XML as per mapping:
    for transform in field_mapping:
        # transform[0] is the From, transform[1] is the To.
        if transform[0] == transform[1]:
            continue
        if transform[0] == "NULL":
            # check whether transform[1] already exists as a Name
            if root_element.find("Fields/Field[Name='" + transform[1] + "']") == None:
                # if it does not exist, create it
                # create a field with name transform[1] with empty value.
                newPair = ET.SubElement(fields_element, "Field")
                ET.SubElement(newPair, "Name").text = transform[1]
                ET.SubElement(newPair, "Value")
            else:
                raise RMc.RM_Py_Exception(
                    "Tried to create duplicate Name in XML. NULL on left")
            continue
        # for each existing field in the XML...
        fields_in_xml = fields_element.findall('.//Field')
        for eachField in fields_in_xml:
            current_xml_field_name = eachField.find('Name').text
            #current_xml_field_value = eachField.find('Value').text
            if current_xml_field_name != transform[0]:
                # not the relevant XML field, continue with the next
                continue
            # found the xml field for the From field of the transform  under consideration
            # now check if transform 1 (To field) is null (already checked for transform 0 is null)
            if transform[1] == "NULL":
                # delete the field
                root_element.find(".//Fields").remove(eachField)
                break
            # Do the rename, but first check for existing field with that name
            # xpath search Fields/Field[Name='name of transform1']
            field_names_transform1 = root_element.find("Fields/Field[Name='" + transform[1] + "']")
            if field_names_transform1 == None:
                # target doesn't exist, so rename source to the target name
                eachField.find('Name').text = transform[1]
                break
            else:
                raise RMc.RM_Py_Exception(
                    "Tried to create duplicate Name in XML.")
        # end of for eachField loop
    # end of for each transform loop


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
        raise RMc.RM_Py_Exception("ERROR internal: both inputs None")

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
        raise RMc.RM_Py_Exception(
            "No sources found with specified search criteria.\n")
    return srcTuples


# ===================================================DIV60==
# Call the "main" function
if __name__ == '__main__':
    main()

# ===================================================DIV60==
