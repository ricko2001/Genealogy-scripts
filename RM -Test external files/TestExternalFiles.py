import os
import sys
from datetime import datetime
from pathlib import Path
import xml.etree.ElementTree as ET
import hashlib

sys.path.append( r'..\\RM -RMpy package' )
import RMpy.launcher # type: ignore
import RMpy.common as RMpyCom # type: ignore


# This script can only read a RootsMagic database file and cannot change it.
# However, until trust is established:
# Always make a RM database backup before using any external script.

# Requirements:
#   RootsMagic database file with associated external media files
#   RM-Python-config.ini

# Last tested with:
#   RootsMagic database v7 through v10
#   Python for Windows v3.12.3
#   RootsMagic v7 through v10 installed (only for unref files option)

# Config files fields used
#    FILE_PATHS  REPORT_FILE_PATH
#    FILE_PATHS  REPORT_FILE_DISPLAY_APP
#    FILE_PATHS  DB_PATH
#    FILE_PATHS  SEARCH_ROOT_FLDR_PATH
#    OPTIONS    CHECK_FILES
#    OPTIONS    UNREF_FILES
#    OPTIONS    FOLDER_LIST
#    OPTIONS    NO_TAG_FILES
#    OPTIONS    DUP_FILENAMES
#    OPTIONS    DUP_FILEPATHS
#    OPTIONS    HASH_FILE
#    OPTIONS    NOT_MEDIA_FLDR
#    OPTIONS    SHOW_ORIG_PATH
#    OPTIONS    CASE_SENSITIVE
#    IGNORED_OBJECTS  FOLDERS
#    IGNORED_OBJECTS  FILES


# ===================================================DIV60==
#  Globals

G_media_directory_path = None
G_db_file_folder_path = None
G_DEBUG = False


# ===================================================DIV60==
def main():

    # Configuration
    config_file_name = "RM-Python-config.ini"
    RMNOCASE_required = False
    allow_db_changes = False

    RMpy.launcher.launcher(os.path.dirname(__file__),
                    config_file_name,
                    RMNOCASE_required,
                    allow_db_changes,
                    run_selected_features)


# ===================================================DIV60==
def run_selected_features(config, db_connection, report_file):

    global G_db_file_folder_path
    # used only in function expand_relative_dir_path, but no access to config there.
    parent_dir= Path(config['FILE_PATHS']['DB_PATH']).parent
    # get the absolute path in case the DB_PATH was relative
    G_db_file_folder_path = parent_dir.resolve()

    # test option values conversion to boolean
    # if missing, treated as false
    try:
        config['OPTIONS'].getboolean('CHECK_FILES')
        config['OPTIONS'].getboolean('UNREF_FILES')
        config['OPTIONS'].getboolean('NO_TAG_FILES')
        config['OPTIONS'].getboolean('FOLDER_LIST')
        config['OPTIONS'].getboolean('DUP_FILENAMES')
        config['OPTIONS'].getboolean('DUP_FILEPATHS')
        config['OPTIONS'].getboolean('NOT_MEDIA_FLDR')
        config['OPTIONS'].getboolean('HASH_FILE')
        config['OPTIONS'].getboolean('NOT_MEDIA_FLDR')
        config['OPTIONS'].getboolean('SHOW_ORIG_PATH')
        config['OPTIONS'].getboolean('CASE_SENSITIVE')

    except:
        raise RMpyCom.RM_Py_Exception(
            "One of the OPTIONS values could not be parsed as boolean. \n")

    # Run the requested options. Usually multiple options.
    if config['OPTIONS'].getboolean('CHECK_FILES'):
        list_missing_files_feature(config, db_connection, report_file)

    if config['OPTIONS'].getboolean('UNREF_FILES'):
        list_unreferenced_files_feature(
            config, db_connection, report_file)

    if config['OPTIONS'].getboolean('NO_TAG_FILES'):
        files_with_no_tags_feature(config, db_connection, report_file)

    if config['OPTIONS'].getboolean('FOLDER_LIST'):
        list_folders_feature(config, db_connection, report_file)

    if config['OPTIONS'].getboolean('DUP_FILENAMES'):
        find_duplicate_file_names_feature(db_connection, report_file)

    if config['OPTIONS'].getboolean('DUP_FILEPATHS'):
        find_duplicate_file_paths_feature(db_connection, report_file)

    if config['OPTIONS'].getboolean('NOT_MEDIA_FLDR'):
        find_file_not_in_media_folder_feature(config, db_connection, report_file)

    if config['OPTIONS'].getboolean('HASH_FILE'):
        file_hash_feature(config, db_connection, report_file)

    section("FINAL", "", report_file)


# ===================================================DIV60==
def list_missing_files_feature(config, db_connection, report_file):

    feature_name = "Files Not Found"
    label_original_path = "Path in database:  "
    found_files = 0

    section("START", feature_name, report_file)
    # get options
    try:
        show_original_path = config['OPTIONS'].getboolean('SHOW_ORIG_PATH')
    except:
        show_original_path = False

    try:
        case_sensitive = config['OPTIONS'].getboolean('CASE_SENSITIVE')
    except:
        case_sensitive = True

    # First check database for empty paths or filenames
    report_empty_paths(db_connection, report_file)

    cur = get_db_file_list(db_connection)
    for row in cur:
        if len(str(row[0])) == 0 or len(str(row[1])) == 0:
            continue
        dir_path_original = row[0]
        dir_path = expand_relative_dir_path(dir_path_original)
        file_path = Path(os.path.join(dir_path, row[1]))


        if not case_sensitive:
            # Case in-sensitive
            if not os.path.exists(dir_path):
                found_files += 1
                report_file.write(
                    f"\n" "Directory path not found:\n"
                    f"{qtStr(dir_path)} for file: {qtStr(row[1])} \n")
                if show_original_path:
                    report_file.write(f"{label_original_path} {qtStr(dir_path_original)} \n")
            else:
                if file_path.exists():
                    if not file_path.is_file():
                        found_files += 1
                        report_file.write(
                            f"\nFile path is not a file: \n"
                            f"{qtStr(file_path)} \n")
                        if show_original_path:
                            report_file.write(f"{label_original_path} {qtStr(row[0])} \n")
                else:
                    found_files += 1
                    report_file.write(f"\nFile path not found: \n{file_path} \n")
                    if show_original_path:
                        report_file.write(
                            f"{label_original_path} {qtStr(dir_path_original)} \n")
        else:
            # use case sensitive compare
            if str(dir_path) != str(os.path.realpath(dir_path)):
                found_files += 1
                report_file.write(
                    f"\n" "Directory path with correct case not found:\n"
                    f"{qtStr(dir_path)} for file: {qtStr(row[1])} \n")
                if show_original_path:
                    report_file.write(f"{label_original_path} {qtStr(dir_path_original)} \n")
            else:
                if file_path.exists():
                    if not file_path.is_file():
                        found_files += 1
                        report_file.write(
                            f"\nPath is not a file: \n{qtStr(file_path)} \n")
                        if show_original_path:
                            report_file.write(f"{label_original_path} {qtStr(row[0])} \n")
                else:
                    found_files += 1
                    report_file.write(f"\nFile name with correct case not found at path: \n{file_path} \n")
                    if show_original_path:
                        report_file.write(
                            f"{label_original_path} {qtStr(dir_path_original)} \n")

    if found_files > 0:
        report_file.write(f"\nNumber of file links in "
                          f"database not found on disk: {found_files} \n")

    if found_files == 0:
        report_file.write("\n    No files were found missing.\n")
    section("END", feature_name, report_file)
    return


# ===================================================DIV60==
def list_unreferenced_files_feature(config, db_connection, report_file):
    feature_name = "Unreferenced Files"

    section("START", feature_name, report_file)

    # get option
    try:
        ext_files_folder_path = config['FILE_PATHS']['SEARCH_ROOT_FLDR_PATH']
    except:
        raise RMpyCom.RM_Py_Exception(
            "ERROR: SEARCH_ROOT_FLDR_PATH must be specified for this option. \n")

    try:
        case_sensitive = config['OPTIONS'].getboolean('CASE_SENSITIVE')
    except:
        case_sensitive = True

    # Validate the folder path
    if not Path(ext_files_folder_path).exists():
        raise RMpyCom.RM_Py_Exception(
            f"ERROR: Directory path not found: {qtStr(ext_files_folder_path)} \n")
    if not Path(ext_files_folder_path).is_dir():
        raise RMpyCom.RM_Py_Exception(
            f"ERROR: Path is not a directory: {qtStr(ext_files_folder_path)} \n")

    # First check database for empty paths or filenames
    report_empty_paths(db_connection, report_file)

    cur = get_db_file_list(db_connection)

    db_file_list = []
    for row in cur:
        if len(str(row[0])) == 0 or len(str(row[1])) == 0:
            continue
        if row[0][0] == '*':
            # what's going on here?
            pass
        dirPath = expand_relative_dir_path(row[0])
        file_path = os.path.join(dirPath, row[1])
        db_file_list.append(file_path)

    filesystem_folder_file_list = folder_contents_minus_ignored(
        report_file, Path(ext_files_folder_path), config)

    if (case_sensitive == True):
        # case sensitive
        unref_files = list(set(filesystem_folder_file_list).difference(db_file_list))
    else:
        filesystem_folder_file_list_lc = [item.lower() for item in filesystem_folder_file_list]
        db_file_list_lc = [item.lower() for item in db_file_list]
        unref_files = list(set(filesystem_folder_file_list_lc).difference(db_file_list_lc))

    if len(unref_files) > 0:
        # print the files
        unref_files.sort()

        # don't print full path from root folder
        cutoff = len(ext_files_folder_path)
        for i in range(len(unref_files)):
            report_file.write("." + str(unref_files[i])[cutoff:] + "\n")

        report_file.write("\nFiles in processed folder not referenced by the database: "
                          + str(len(unref_files)) + "\n")
    else:
        report_file.write("\n    No unreferenced files were found.\n\n")

    possibly_unexpected = len(db_file_list) - len(filesystem_folder_file_list)
    summary = (
        f"\n    Folder processed:  {ext_files_folder_path}"
        f"\n    Number of files in folder: {
            len(filesystem_folder_file_list)} (exclusive of ignored items)"
        f"\n    Number of database file links: {len(db_file_list)}"
        f"\n    # DB links minus # non-ignored files: {possibly_unexpected} \n")

    report_file.write(summary)

    section("END", feature_name, report_file)
    return


# ===================================================DIV60==
def files_with_no_tags_feature(config, db_connection, report_file):

    feature_name = "Files with no Tags"
    label_orig_path = "Path in database:  "
    found_no_tag_files = False

    section("START", feature_name, report_file)
    # get options
    show_orig_path = config['OPTIONS'].getboolean('SHOW_ORIG_PATH')

    cur = get_db_no_tag_file_list(db_connection)

    for row in cur:
        found_no_tag_files = True
        dir_path_orig = row[0]
        dir_path = expand_relative_dir_path(row[0])
        file_path = Path(os.path.join(dir_path, row[1]))
        report_file.write(f"{file_path} \n")
        if show_orig_path:
            report_file.write(label_orig_path
                              + qtStr(dir_path_orig) + "\n")

    if not found_no_tag_files:
        report_file.write("\n    No files with no tags were found.\n")

    section("END", feature_name, report_file)
    return


# ===================================================DIV60==
def list_folders_feature(config, db_connection, report_file):

    feature_name = "Referenced Folders"
    label_orig_path = "Path in database:  "
    found_some_folders = False

    section("START", feature_name, report_file)
    # get options
    show_orig_path = config['OPTIONS'].getboolean('SHOW_ORIG_PATH')

    # First check database for empty paths or filenames
    # easier to handle them now than later
    report_empty_paths(db_connection, report_file)

    cur = get_db_folder_list(db_connection)
    rows = cur.fetchall()
    for row in rows:
        if len(str(row[0])) == 0:
            continue
        found_some_folders = True
        report_file.write(str(expand_relative_dir_path(row[0])) + "\n")
        if show_orig_path:
            report_file.write(f"{label_orig_path} {qtStr(row[0])} \n")

    if found_some_folders:
        report_file.write(f"\n Folders referenced in database: {len(rows)} \n")

    if not found_some_folders:
        report_file.write("\n    No folders found in database.\n")

    section("END", feature_name, report_file)

    return


# ===================================================DIV60==
def find_duplicate_file_paths_feature(db_connection, report_file):

    # this currently find exact duplicates as saved in DB path & filename (ignoring case)
    # duplicates *after expansion* of relative paths not found
    feature_name = "Duplicated File Paths"
    found_some_dup_files = False

    section("START", feature_name, report_file)
    cur = get_duplicate_file_paths_list(db_connection)

    for row in cur:
        found_some_dup_files = True
        dirPathOrig = row[0]
        dir_path = expand_relative_dir_path(row[0])
        file_path = Path(os.path.join(dir_path, row[1]))
        report_file.write(qtStr(file_path) + "\n")

    if not found_some_dup_files:
        report_file.write(
            "\n    No Duplicate File Paths in Media Gallery were found. \n")

    section("END", feature_name, report_file)
    return


# ===================================================DIV60==
def find_duplicate_file_names_feature(db_connection, report_file):

    # this finds exact filename duplicates as saved in DB (ignoring case)
    feature_ame = "Duplicated File Names"
    found_some_dup_files = False

    section("START", feature_ame, report_file)
    cur = get_duplicate_file_names_list(db_connection)

    for row in cur:
        found_some_dup_files = True
        file_name = row[0]
        report_file.write(qtStr(file_name) + "\n")

    if not found_some_dup_files:
        report_file.write(
            "\n    No Duplicate File Names in Media Gallery were found.\n")

    section("END", feature_ame, report_file)
    return


# ===================================================DIV60==
def file_hash_feature(config, db_connection, report_file):

    feature_name = "Generate media files hash"
    found_some_missing_files = False

    print("\n Please wait, HASH file may take several minutes to generate.\n")

    section("START", feature_name, report_file)
    # get option
    try:
        hash_file_folder = config['FILE_PATHS']['HASH_FILE_FLDR_PATH']
    except:
        raise RMpyCom.RM_Py_Exception(
            "ERROR: HASH_FILE_FLDR_PATH must be specified for this option. \n")

    hash_file_path = os.path.join(
        hash_file_folder,
        "MediaFiles_HASH_" + RMpyCom.time_stamp_now("file") + ".txt")

    try:
        hash_file = open(hash_file_path,  mode='w', encoding='utf-8')
    except:
        raise RMpyCom.RM_Py_Exception(
            f"ERROR: Cannot create the hash file:{qtStr(hash_file_path)} \n\n")

    report_file.write(
        f"MD5 hash of files saved in file:\n"
        f"{hash_file_path} \n\n")
    cur = get_db_file_list(db_connection)

    for row in cur:
        if len(str(row[0])) == 0 or len(str(row[1])) == 0:
            continue
        dir_path = expand_relative_dir_path(row[0])
        file_path = Path(os.path.join(dir_path, row[1]))
        if not dir_path.exists():
            found_some_missing_files = True
            report_file.write(
                f"Directory path not found: \n{dir_path} \n"
                f" for file: {qtStr(row[1])} \n")

        else:
            if file_path.exists():
                if not file_path.is_file():
                    found_some_missing_files = True
                    report_file.write(
                        f"File path is not a file: \n{file_path} \n")
                # take hash
                BUF_SIZE = 65536  # reads in 64kb chunks

                md5 = hashlib.md5()
                # or sha1 = hashlib.sha1()

                with open(file_path, 'rb') as f:
                    while True:
                        data = f.read(BUF_SIZE)
                        if not data:
                            break
                        md5.update(data)
                hash_file.write(f"{file_path!s} \n"
                                f"{md5.hexdigest()} \n\n")
            else:
                found_some_missing_files = True
                report_file.write(f"File path not found: \n{file_path} \n")

    if not found_some_missing_files:
        report_file.write("\n    All files were processed.\n")
    section("END", feature_name, report_file)

    return


# ===================================================DIV60==
def find_file_not_in_media_folder_feature(config, db_connection, report_file):

    feature_name = "Files Not in Media Folder"
    label_orig_path = "Path in database:  "
    found_files = 0

    section("START", feature_name, report_file)
    # get options
    show_original_path = config['OPTIONS'].getboolean('SHOW_ORIG_PATH')

    # First check database for empty paths or filenames
    report_empty_paths(db_connection, report_file)

    cur = get_db_file_list(db_connection)
    rows = cur.fetchall()
    for row in rows:
        if len(str(row[0])) == 0:
            continue
        if row[0][0] != '?':
            found_files += 1
            dir_path = expand_relative_dir_path(row[0])
            file_path = Path(os.path.join(dir_path, row[1]))
            report_file.write(f"\n{file_path} \n")
            if show_original_path:
                report_file.write(f"{label_orig_path} {qtStr(row[0])} \n")

    if found_files > 0:
        report_file.write(f"\nNumber of file links in database not in Media Folder: {found_files} \n")

    if found_files == 0:
        report_file.write(
            "\n    All file links in the database "
             "point to the Media Folder.\n")

    section("END", feature_name, report_file)

    return

# ===================================================DIV60==
def get_db_folder_list(dbConnection):

    SqlStmt = """
  SELECT  DISTINCT MediaPath
  FROM MultimediaTable
    ORDER BY MediaPath
  """
    cur = dbConnection.cursor()
    cur.execute(SqlStmt)
    return cur


# ===================================================DIV60==
def get_db_file_list(db_connection):

    SqlStmt = """
  SELECT  MediaPath, MediaFile
  FROM MultimediaTable
    ORDER BY MediaPath, MediaFile COLLATE NOCASE
  """
    cur = db_connection.cursor()
    cur.execute(SqlStmt)
    return cur


# ===================================================DIV60==
def report_empty_paths(db_connection, report_file):

    # First check database for empty paths or filenames
    # easier to handle them now than later

    SqlStmt = """
    SELECT  MediaPath, MediaFile, Caption, Description
    FROM MultimediaTable
    WHERE MediaPath == ''
       OR MediaFile == ''COLLATE NOCASE
    """
    cur = db_connection.cursor()
    cur.execute(SqlStmt)

    rows = cur.fetchall()
    if len(rows) != 0:
        report_file.write(
            f"{len(rows)} entires with blank filename or path found:\n\n")
        for row in rows:
            # MediaPath, MediaFile, Caption, Description
            report_file.write(
                f"Path       = {row[0]} \n"
                f"File Name  = {row[1]} \n"
                f"Caption    = {row[2]} \n"
                f"Description= {row[3]} \n\n")


# ===================================================DIV60==
def get_db_no_tag_file_list(db_connection):

    SqlStmt = """
  SELECT MediaPath, MediaFile
  FROM MultimediaTable mmt
  LEFT JOIN MediaLinkTable mlt ON mlt.MediaID =  mmt.MediaID
   WHERE OwnerType is NULL
   ORDER by MediaPath, MediaFile COLLATE NOCASE
   """
    cur = db_connection.cursor()
    cur.execute(SqlStmt)
    return cur


# ===================================================DIV60==
def get_duplicate_file_names_list(db_connection):

    # see for examples
    # https://database.guide/6-ways-to-select-duplicate-rows-in-sqlite/
    SqlStmt = """
  SELECT p.MediaFile, COUNT(*) AS "Count"
  FROM MultimediaTable p
  GROUP BY MediaFile COLLATE NOCASE
  HAVING COUNT(*) > 1
  ORDER BY p.MediaFile COLLATE NOCASE
  """
    cur = db_connection.cursor()
    cur.execute(SqlStmt)
    return cur


# ===================================================DIV60==
def get_duplicate_file_paths_list(db_connection):

    SqlStmt = """
  SELECT p.MediaPath, p.MediaFile, COUNT(*) AS "Count"
  FROM MultimediaTable p
  GROUP BY MediaPath COLLATE NOCASE, MediaFile COLLATE NOCASE
  HAVING COUNT(*) > 1
  ORDER BY p.MediaFile COLLATE NOCASE
  """
    cur = db_connection.cursor()
    cur.execute(SqlStmt)
    return cur


# ===================================================DIV60==
def section(pos, name, report_file):

    Divider = "="*60 + "===DIV70==\n"
    if pos == "START":
        text = f"\n{Divider}\n=== Start of {qtStr(name)} listing\n\n"
    elif pos == "END":
        text = f"\n=== End of {qtStr(name)} listing\n"
    elif pos == "FINAL":
        text = f"\n{Divider} \n=== End of Report\n"
    else:
        raise RMpyCom.RM_Py_Exception(
            "INTERNAL ERROR: Section position not correctly defined")

    report_file.write(text)
    report_file.flush()
    return


# ===================================================DIV60==
def expand_relative_dir_path(in_path):

    # deal with relative paths in RootsMagic 8 + 9 databases
    # RM7 path are always absolute and will never be processed here

    global G_media_directory_path
    # use this global as sort of a static constant. Want it initialed once.

    path = str(in_path)
    # input parameter path should always be of type str, output will be Path
    # note when using Path / operator, second operand should not be absolute

    if path[0] == "~":
        absolute_path = Path(os.path.expanduser(path))

    elif path[0] == "?":
        if G_media_directory_path is None:
            G_media_directory_path = get_media_directory()
        if len(path) == 1:
            absolute_path = Path(G_media_directory_path)
        else:
            absolute_path = Path(G_media_directory_path) / path[2:]

    elif path[0] == "*":
        if len(path) == 1:
            absolute_path = Path(G_db_file_folder_path)
        else:
            absolute_path = Path(G_db_file_folder_path) / path[2:]

    else:
        absolute_path = Path(path)

    return absolute_path


# ===================================================DIV60==
def get_media_directory():

    #  Relies on the RM installed xml file containing application preferences
    #  File location set by RootsMagic installer
    RM_Config_FilePath_9 = r"~\AppData\Roaming\RootsMagic\Version 9\RootsMagicUser.xml"
    RM_Config_FilePath_8 = r"~\AppData\Roaming\RootsMagic\Version 8\RootsMagicUser.xml"

    media_folder_path = "RM8 or later not installed"

#  If xml settings file for RM 8 or 9 not found, return the mediaPath containing the
#  RM8 or later not installed message. It will never be used because RM 7 and earlier
#  does not need to know the media folder path.

#  Potential problem if RM 8 and 9 both installed and they have different
#  media folders specified. The highest version number path is found here.

#  Could base this off of the database version number, but that's not readily available.

    xmlSettingsPath = Path(os.path.expanduser(RM_Config_FilePath_9))
    if not xmlSettingsPath.exists():
        xmlSettingsPath = Path(os.path.expanduser(RM_Config_FilePath_8))
        if not xmlSettingsPath.exists():
            return media_folder_path

    root = ET.parse(xmlSettingsPath)
    media_folder_path_ele = root.find("./Folders/Media")
    media_folder_path = media_folder_path_ele.text

    return media_folder_path


# ===================================================DIV60==
def folder_contents_minus_ignored(report_file, dir_path, config):

    ignored_folder_names = []
    ignored_file_names = []
    try:
        ignored_folder_names = config['IGNORED_OBJECTS'].get(
            'FOLDERS').split('\n')
    except:
        report_file.write("No ignored folders specified. \n\n")
    try:
        ignored_file_names = config['IGNORED_OBJECTS'].get(
            'FILENAMES').split('\n')
    except:
        report_file.write("No ignored files specified. \n\n")

    media_file_list = []
    for (dir_name, dir_names, file_names) in os.walk(dir_path, topdown=True):

        for igFldrName in ignored_folder_names:
            if igFldrName in dir_names:
                dir_names.remove(igFldrName)

        for igFileName in ignored_file_names:
            if igFileName in file_names:
                file_names.remove(igFileName)

        for filename in file_names:
            media_file_list.append(str(os.path.join(dir_name, filename)))

    return media_file_list


# ===================================================DIV60==
def qtStr(input):
    return f"\"{input!s}\""


# ===================================================DIV60==
# Call the "main" function
if __name__ == '__main__':
    main()

# ===================================================DIV60==
