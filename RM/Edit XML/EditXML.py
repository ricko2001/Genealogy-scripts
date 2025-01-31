import os
import sys
import xml.etree.ElementTree as ET
import re

sys.path.append( r'..\\RM -RMpy package' )
import RMpy.launcher # type: ignore
import RMpy.common as RMc # type: ignore

# Requirements:
#   RootsMagic database file
#   RM-Python-config.ini

# Tested with:
#   RootsMagic database file v10.0.1,0
#   Python for Windows v3.12.3


# ====================================DIV60==
#  Global Variables
G_DEBUG = False


# ===================================================DIV60==
def main():

    # Configuration
    config_file_name = "RM-Python-config.ini"
    RMNOCASE_required = False
    RegExp_required = False
    allow_db_changes = True

    RMpy.launcher.launcher(os.path.dirname(__file__),
                    config_file_name,
                    run_selected_features,
                    allow_db_changes,
                    RMNOCASE_required,
                    RegExp_required )


# ===================================================DIV60==
def run_selected_features(config, db_connection, report_file):

    edit_the_xml(config, db_connection, report_file)

# ===================================================DIV60==
def edit_the_xml(config, db_connection, report_file):

    try:
        table_to_edit = config['OPTIONS']['TABLE']
        field_name = config['OPTIONS']['FIELD_NAME']
    except:
        raise RMc.RM_Py_Exception(
            "ERROR: Check Options for errors")

#  Get the table name
# for now, hard code all params

# get the list of rows by using 
# for source  select with like source name or template id
# for citation  select with like  citation name or source id
# for src_template select with like  template name

    table = "CitationTable"

    field_name = "MemorialID"

    SqlStmt = """
SELECT CitationID
FROM CitationTable as ct
WHERE ct.SourceID = 828
"""

    # compile the regular expressions
    ok_as_is = re.compile(r"^\d+$")
    isolate_id = re.compile(r"(\d+)")

    for row in  get_list_of_rows(db_connection, SqlStmt):
        # def get_root_element(dbConnection, SourceID=None, CitationID=None):
        root_element = get_root_element(db_connection, None, row)

        # test and if needed, edit the XML in the DOM
        field_found = root_element.find("Fields/Field[Name='" + field_name + "']")
        if field_found is None:
            report_file.write(str(row) + "     " + "null field_found"  + "\n ")
            print(str(row) + "source XML OLD START ============================")
            ET.indent(root_element)
            ET.dump(root_element)
            print("source XML OLD END ==============================")

            continue

        field_value = field_found.find('Value')
        old_text = field_value.text

        if old_text is None:
            report_file.write(str(row) + "     " + "null old_text"  + "\n ")
            continue

        if  ok_as_is.search( old_text ):
            report_file.write(str(row) + "     " + old_text  + "\n ")
            continue

        if G_DEBUG:
            print("source XML OLD START ============================")
            ET.indent(root_element)
            ET.dump(root_element)
            print("source XML OLD END ==============================")

        id_match = isolate_id.search(old_text)
        id = id_match.group(1)

        #    Find A Grave Memorial# 149361756
        #    Grave Memorial# 191562772</A>

        report_file.write(str(row) + "     " + old_text + "     " + id + "\n ")

        field_value.text = id

        if G_DEBUG:
            print("source XML NEW START ============================")
            ET.indent(root_element)
            ET.dump(root_element)
            print("source XML NEW END ==============================")


        # Update the source with new XML and new templateID
        newXML = ET.tostring(root_element, encoding="unicode")

        SqlStmt_src_w = """
UPDATE CitationTable
   SET Fields = ?
 WHERE CitationID = ?
"""
        db_connection.execute(SqlStmt_src_w, (newXML, row))
        db_connection.commit()

# ===================================================DIV60==
def adjust_xml_fields(field_mapping, root_element):

    fields_element = root_element.find(".//Fields")
    # change fields in citation as per mapping:
    for transform in field_mapping:
        if transform[0] == transform[1]:
            continue
        if transform[0] == "NULL":
            # check whether field transform[1] exists as a Name
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
            # found the xml field for the transform under consideration
            # now check if transform 1 is null (already checked for transform 0 is null)
            if transform[1] == "NULL":
                # delete the unused field
                root_element.find(".//Fields").remove(eachField)
                break
            # Do the re-name, but first check for existing field with that name
            # xpath search Fields/Field[Name='name of transform1']
            field_names_transform1 = root_element.find("Fields/Field[Name='" + transform[1] + "']")
            if field_names_transform1 == None:
                # target doesn't exist, so rename source to the target name
                eachField.find('Name').text = transform[1]
                break
            else:
                raise RMc.RM_Py_Exception(
                    "Tried to create duplicate Name in citation XML.")
        # end of for eachField loop
    # end of for each transform loop




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
# Call the "main" function
if __name__ == '__main__':
    main()

# ===================================================DIV60==
