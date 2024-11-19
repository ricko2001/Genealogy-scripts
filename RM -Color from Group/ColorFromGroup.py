import sys
sys.path.append(r'..\RM -RMpy package')
import RMpy.launcher  # type: ignore
import RMpy.common as RMc  # type: ignore
from RMpy.common import q_str # type: ignore

import os


# Always make a database backup before using this script.

# Requirements:
#   RootsMagic database file
#   RM-Python-config.ini

# Tested with:
#   RootsMagic database file v10
#   Python for Windows v3.12

# See ReadMe.txt file for more details

# ===================================================DIV60==
def main():

    # Configuration
    config_file_name = "RM-Python-config.ini"
    allow_db_changes = True
    RMNOCASE_required = False
    RegExp_required = False

    RMpy.launcher.launcher(os.path.dirname(__file__),
                           config_file_name,
                           run_selected_features,
                           allow_db_changes,
                           RMNOCASE_required,
                           RegExp_required)


# ===================================================DIV60==
def run_selected_features(config, db_connection, report_file):

    color_from_group_feature(config, db_connection, report_file)


# ===================================================DIV60==
def color_from_group_feature(config, db_connection, report_file):

    try:
        color_command_list = config['OPTIONS'].get(
            'COLOR').split('\n')
    except:
        raise RMc.RM_Py_Exception(
            'section: [OPTIONS],  key: COLOR   not found.')

    # confirm that the corresponding sections exist
    for color_cmd in color_command_list:
        if color_cmd == '':
            continue
        try:
            config[color_cmd]
        except:
            raise RMc.RM_Py_Exception(
                f'section: [{q_str(color_cmd)}]   not found.')

    for color_cmd in color_command_list:
        if color_cmd == '':
            continue
        exec_color_cmd(db_connection, config, report_file, color_cmd)

    return


# ===================================================DIV60==
def exec_color_cmd(db_connection, config, report_file, color_cmd):

    try:
        group_name = config[color_cmd].get('GROUP')
    except:
        raise RMc.RM_Py_Exception(
            f'section: [{color_cmd}],  key: GROUP    not found.')

    try:
        action = config[color_cmd].get('ACTION')
    except:
        raise RMc.RM_Py_Exception(
            f'section: [{color_cmd}],  key: ACTION    not found.')

    try:
        color_txt = config[color_cmd].get('COLOR')
    except:
        raise RMc.RM_Py_Exception(
            f'section: [{color_cmd}],  key: COLOR    not found.')

    try:
        code_set = config[color_cmd].get('COLOR_CODE_SET')
    except:
        raise RMc.RM_Py_Exception(
            f'section: [{color_cmd}],  key: COLOR_CODE_SET    not found.')

    # Validate the input
    # group_name
    if group_name == "_ALL":
        group_id = 0
    else:
        group_id = confirm_DB_group_name(group_name, report_file, db_connection)

    # action
    if (action != "set"
        and action != "clear"
        ):
        raise RMc.RM_Py_Exception(
            f'section: [{color_cmd}],  key: ACTION    is not supported.')

    # color_txt
    try:
        if (int(color_txt) <0 or int(color_txt) >27):
            raise RMc.RM_Py_Exception(
                f'section: [{color_cmd}],  key: COLOR    is out of range.')
    except TypeError:
            raise RMc.RM_Py_Exception(
                f'section: [{color_cmd}],  key: COLOR    is not an integer.')

    # code_set
    try:
        if (int(code_set) <1 or int(code_set) >10):
            raise RMc.RM_Py_Exception(
                f'section: [{color_cmd}],  key: COLOR_CODE_SET    is out of range.')
    except TypeError:
            raise RMc.RM_Py_Exception(
                f'section: [{color_cmd}],  key: COLOR_CODE_SET    is not an integer.')


    update_people_colors(db_connection, group_id, int(code_set), int(color_txt), action)

    return


# ===================================================DIV60==
def update_people_colors(db_connection, group_id, color_group, color, action):

# translate UI_color into DB_color
    db_color_num = translate_ui_color_to_db( ui_number = color)

# Construct SQL statement so correct color group column is updated
# Careful- can't use a SQL variable, must use python string manipulation.

    if color_group <1 or color_group>10:
            raise RMc.RM_Py_Exception('color_group is out of range.')
    if color_group== 0:
        col_num_str=''
    else:
        col_num_str = str(color_group -1)

    proto_set_SqlStmt = """
UPDATE  PersonTable AS pt
SET Color{num}  = :color
FROM (
    SELECT pt2.PersonID
    FROM PersonTable AS pt2
    JOIN GroupTable AS gt ON pt2.PersonID BETWEEN gt.StartID AND gt.EndID
    WHERE gt.GroupID = :group_id ) AS id
WHERE pt.PersonID = id.PersonID;
"""

    proto_clear_SqlStmt = """
UPDATE  PersonTable
SET Color{num}  = 0
WHERE Color{num} <> 0;
"""

    if action == "set":
        SqlStmt = proto_set_SqlStmt.format(num=col_num_str)
        cur = db_connection.cursor()
        cur.execute(SqlStmt, { "color":str(db_color_num), "group_id":str(group_id) })

    elif action == "clear":
        SqlStmt = proto_clear_SqlStmt.format(num=col_num_str)
        cur = db_connection.cursor()
        cur.execute(SqlStmt)


# ===================================================DIV60==
def translate_ui_color_to_db( ui_number=None, ui_color_name=None, ui_name=None):
    # provide one of either input argument
#def translate_ui_color_to_db( ui_number, ui_color_name=None, ui_name=None):

    if ui_number is not None:
        if ui_number == 1:
            db_color= 4
        elif ui_number == 2:
            db_color= 15
        elif ui_number == 3:
            db_color= 16
        elif ui_number == 4:
            db_color= 17
        elif ui_number == 5:
            db_color= 18
        elif ui_number == 6:
            db_color= 6
        elif ui_number == 7:
            db_color= 19
        elif ui_number == 8:
            db_color= 20
        elif ui_number == 9:
            db_color= 7
        elif ui_number == 10:
            db_color= 1
        elif ui_number == 11:
            db_color= 21
        elif ui_number == 12:
            db_color= 5
        elif ui_number == 13:
            db_color= 2
        elif ui_number == 14:
            db_color= 9
        elif ui_number == 15:
            db_color= 22
        elif ui_number == 16:
            db_color= 3
        elif ui_number == 17:
            db_color= 11
        elif ui_number == 18:
            db_color= 14
        elif ui_number == 19:
            db_color= 8
        elif ui_number == 20:
            db_color= 12
        elif ui_number == 21:
            db_color= 23
        elif ui_number == 22:
            db_color= 24
        elif ui_number == 23:
            db_color= 25
        elif ui_number == 24:
            db_color= 13
        elif ui_number == 25:
            db_color= 10
        elif ui_number == 26:
            db_color= 26
        elif ui_number == 27:
            db_color= 27

    elif ui_color_name is not None:
        ui_color_name_lower = ui.color_name.lower()

        if ui_color_name_lower == "Pink".lower():
            db_color = 4
        elif ui_color_name_lower == "Apricot".lower():
            db_color= 15
        elif ui_color_name_lower == "Lemon".lower():
            db_color= 16
        elif ui_color_name_lower == "Chartreuse".lower():
            db_color= 17
        elif ui_color_name_lower == "Mint".lower():
            db_color= 18
        elif ui_color_name_lower == "Aqua".lower():
            db_color= 6
        elif ui_color_name_lower == "Azure".lower():
            db_color= 19
        elif ui_color_name_lower == "Mauve".lower():
            db_color= 20
        elif ui_color_name_lower == "Silver".lower():
            db_color= 7
        elif ui_color_name_lower == "Red".lower():
            db_color= 1
        elif ui_color_name_lower == "Orange".lower():
            db_color= 21
        elif ui_color_name_lower == "Yellow".lower():
            db_color= 5
        elif ui_color_name_lower == "Lime".lower():
            db_color= 2
        elif ui_color_name_lower == "Green".lower():
            db_color= 9
        elif ui_color_name_lower == "Turquoise".lower():
            db_color= 22
        elif ui_color_name_lower == "Blue".lower():
            db_color= 3
        elif ui_color_name_lower == "Purple".lower():
            db_color= 11
        elif ui_color_name_lower == "Grey".lower():
            db_color= 14
        elif ui_color_name_lower == "Maroon".lower():
            db_color= 8
        elif ui_color_name_lower == "Brown".lower():
            db_color= 12
        elif ui_color_name_lower == "Khaki".lower():
            db_color= 23
        elif ui_color_name_lower == "Olive".lower():
            db_color= 24
        elif ui_color_name_lower == "Forest".lower():
            db_color= 25
        elif ui_color_name_lower == "Teal".lower():
            db_color= 13
        elif ui_color_name_lower == "Navy".lower():
            db_color= 10
        elif ui_color_name_lower == "Aubergine".lower():
            db_color= 26
        elif ui_color_name_lower == "Slate".lower():
            db_color= 27

    elif ui_name is not None:
        raise RMc.RM_Py_Exception( "ui_name translation not yet implemented")
    else:
        raise RMc.RM_Py_Exception( "An argument must be provided to translate_ui_color_to_db")

    return db_color


# ===================================================DIV60==
def group_members(group_id, db_connection):

    member_list = []
    # check how many groupNames with name and TagType=0 already exist
    SqlStmt = """
SELECT  StartID,  EndID
FROM GroupTable 
WHERE GroupID = ?
ORDER BY StartID
"""
    cur = db_connection.cursor()
    cur.execute(SqlStmt, (group_id,))
    result = cur.fetchall()
    for line_set in result:
        if line_set[0] == line_set[1]:
            member_list.append(line_set[0])
        else:
            for i in range(line_set[0], line_set[1]):
                member_list.append(i)

    return member_list



# ===================================================DIV60==
def confirm_DB_group_name(Name, report_file, db_connection):
    #  TagTable
    #   TagID=rowid
    #   TagType =0 for Groups
    #   TagName   duplicates not constrained

    Divider = "="*50 + "===DIV60=="
    report_file.write(f"{Divider}\n\n")

    # check how many groupNames with name and TagType=0 already exist
    SqlStmt = """
SELECT count(*), TagValue 
FROM TagTable 
WHERE TagName=? COLLATE NOCASE AND TagType=0 COLLATE NOCASE
"""
    cur = db_connection.cursor()
    cur.execute(SqlStmt, (Name,))
    result = cur.fetchone()
    existingNumber = result[0]
    GroupID = result[1]

    if existingNumber > 1:
        raise RMc.RM_Py_Exception(f"\nERROR: Group: {q_str(Name)}  exists more than once in the database.\n"
                                  "Rename one of the duplicates. \n")

    if existingNumber == 1:
        report_file.write(f"Group: {q_str(Name)} will be used to update color. \n")

    else:  # existingNumber == 0
        raise RMc.RM_Py_Exception(
            f"\nERROR: Group: {q_str(Name)} does not exist in the database. \n")

    return GroupID





# ===================================================DIV60==
# Call the "main" function
if __name__ == '__main__':
    main()

# ===================================================DIV60==
