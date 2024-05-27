import os
import sys
import sqlite3
from datetime import datetime
import configparser
from pathlib import Path
import xml.etree.ElementTree as ET
import hashlib
import subprocess
import traceback

# This script can only read a RootsMagic database file and cannot change it.
# However, until trust is established, make a backup before use.

# Requirements: (see ReadMe.txt for details)
# RootsMagic v7, v8 or v9 database file
# RM-Python-config.ini  ( Configuration ini text file to set options )
# Python v3.11 or greater
# RootsMagic v7, v8 or v9 installed (only for unref files option)


# ===================================================DIV60==
#  Global Variables
G_MediaDirectoryPath = ""
G_DbFileFolderPath = ""
G_QT = "\""


# ===================================================DIV60==
def main():

    # Configuration
    IniFileName = "RM-Python-config.ini"
    global G_DbFileFolderPath
    report_display_app = None
    db_connection = None

    # ===========================================DIV50==
    # Errors go to console window
    # ===========================================DIV50==
    try:
      # ini file must be in "current directory" and encoded as UTF-8 (no BOM).
      # see   https://docs.python.org/3/library/configparser.html
        IniFile = os.path.join(GetCurrentDirectory(), IniFileName)

        # Check that ini file is at expected path and that it is readable & valid.
        if not os.path.exists(IniFile):
            raise RMPyException("ERROR: The ini configuration file, " + IniFileName
                                + " must be in the same directory as the .py or .exe file.\n\n")

        config = configparser.ConfigParser(empty_lines_in_values=False,
                                           interpolation=None)
        try:
            config.read(IniFile, 'UTF-8')
        except:
            raise RMPyException("ERROR: The " + IniFileName
                                + " file contains a format error and cannot be parsed.\n\n")

        try:
            report_path = config['FILE_PATHS']['REPORT_FILE_PATH']
        except:
            raise RMPyException('ERROR: REPORT_FILE_PATH must be defined in the '
                                + IniFileName + "\n\n")

        try:
            # Use UTF-8 encoding for the report file. Test for write-ability
            open(report_path,  mode='w', encoding='utf-8')
        except:
            raise RMPyException('ERROR: Cannot create the report file '
                                + report_path + "\n\n")

    except RMPyException as e:
        pause_with_message(e)
        return 1
    except Exception as e:
        traceback.print_exception(e, file=sys.stdout)
        pause_with_message(
            "ERROR: Application failed. Please report. " + str(e))
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
            raise RMPyException('ERROR: Path for report file display app not found: '
                                + report_display_app)
        
        try:
            database_path = config['FILE_PATHS']['DB_PATH']
        except:
            raise RMPyException('ERROR: DB_PATH must be specified.')
        if not os.path.exists(database_path):
            raise RMPyException('Path for database not found: ' + database_path
                                + '\n\n' 'Absolute path checked:\n"'
                                + os.path.abspath(database_path) + '"')



        # RM database file info
        FileModificationTime = datetime.fromtimestamp(
            os.path.getmtime(database_path))
        G_DbFileFolderPath = Path(database_path).parent

        db_connection = create_db_connection(database_path, None)

        # write header to report file
        report_file.write("Report generated at      = " + TimeStampNow()
                      + "\nDatabase processed       = " +
                      os.path.abspath(database_path)
                      + "\nDatabase last changed on = "
                      + FileModificationTime.strftime("%Y-%m-%d %H:%M:%S")
                      + "\nSQLite library version   = "
                      + GetSQLiteLibraryVersion(db_connection) + "\n\n")

        # test option values conversion to boolean
        # if missing, treated as false
        try:
            config['OPTIONS'].getboolean('CHECK_FILES')
            config['OPTIONS'].getboolean('UNREF_FILES')
            config['OPTIONS'].getboolean('NO_TAG_FILES')
            config['OPTIONS'].getboolean('FOLDER_LIST')
            config['OPTIONS'].getboolean('DUP_FILENAMES')
            config['OPTIONS'].getboolean('DUP_FILEPATHS')
            config['OPTIONS'].getboolean('SHOW_ORIG_PATH')
            config['OPTIONS'].getboolean('HASH_FILE')
        except:
            raise RMPyException(
                "One of the OPTIONS values could not be parsed as boolean. \n")

        # Run the requested options. Usually multiple options.
        if config['OPTIONS'].getboolean('CHECK_FILES'):
            ListMissingFilesFeature(config, db_connection, report_file)

        if config['OPTIONS'].getboolean('UNREF_FILES'):
            ListUnReferencedFilesFeature(
                config, db_connection, report_file)

        if config['OPTIONS'].getboolean('FOLDER_LIST'):
            ListFoldersFeature(config, db_connection, report_file)

        if config['OPTIONS'].getboolean('NO_TAG_FILES'):
            FilesWithNoTagsFeature(config, db_connection, report_file)

        if config['OPTIONS'].getboolean('DUP_FILEPATHS'):
            FindDuplcateFilePathsFeature(db_connection, report_file)

        if config['OPTIONS'].getboolean('DUP_FILENAMES'):
            FindDuplcateFileNamesFeature(db_connection, report_file)

        if config['OPTIONS'].getboolean('HASH_FILE'):
            FileHashFeature(config, db_connection, report_file)

        Section("FINAL", "", report_file)

    except (sqlite3.OperationalError, sqlite3.ProgrammingError) as e:
        report_file.write(
            "ERROR: SQL execution returned an error \n\n" + str(e))
        return 1
    except RMPyException as e:
        report_file.write(str(e))
        return 1
    except Exception as e:
        traceback.print_exception(e, file=report_file)
        report_file.write("\n\n"
                          "ERROR: Application failed. Please send text to author. ")
        return 1
    finally:
        if db_connection is not None:
            db_connection.close()
        report_file.close()
        if report_display_app is not None:
            subprocess.Popen([report_display_app, report_path])
    return 0


# ===================================================DIV60==
def ListMissingFilesFeature(config, dbConnection, reportF):

    FeatureName = "Files Not Found"
    Label_OrigPath = "Path in database:  "
    foundSomeMissingFiles = False

    Section("START", FeatureName, reportF)
    # get options
    ShowOrigPath = config['OPTIONS'].getboolean('SHOW_ORIG_PATH')

    # First check database for empty paths or filenames
    ReportEmptyPaths(dbConnection, reportF)

    cur = GetDBFileList(dbConnection)
    # row[0] = path,   row[1] = fileName

    for row in cur:
        if len(str(row[0])) == 0 or len(str(row[1])) == 0:
            continue
        dirPathOrig = row[0]
        dirPath = ExpandDirPath(dirPathOrig)
        filePath = Path(os.path.join(dirPath, row[1]))

        if not os.path.exists(dirPath):
            foundSomeMissingFiles = True
            reportF.write("Directory path not found:\n"
                          + G_QT + str(dirPath) + G_QT + " for file: "
                          + G_QT + row[1] + G_QT + "\n")
            if ShowOrigPath:
                reportF.write(Label_OrigPath + G_QT + str(dirPathOrig)
                              + G_QT + "\n")

        else:
            if filePath.exists():
                if not filePath.is_file():
                    foundSomeMissingFiles = True
                    reportF.write("File path is not a file: \n" + G_QT
                                  + str(filePath) + G_QT + "\n")
                    if ShowOrigPath:
                        reportF.write(Label_OrigPath + G_QT
                                      + str(dirPathOrig) + G_QT + "\n")

            else:
                foundSomeMissingFiles = True
                reportF.write("File path not found: \n" + G_QT
                              + str(filePath) + G_QT + "\n")
                if ShowOrigPath:
                    reportF.write(Label_OrigPath + G_QT + str(dirPathOrig)
                                  + G_QT + "\n")

    if not foundSomeMissingFiles:
        reportF.write("\n    No files were found missing.\n")
    Section("END", FeatureName, reportF)
    return


# ===================================================DIV60==

def ListUnReferencedFilesFeature(config, dbConnection, reportF):
    FeatureName = "Unreferenced Files"

    Section("START", FeatureName, reportF)
    # get option
    try:
        ExtFilesFolderPath = config['FILE_PATHS']['SEARCH_ROOT_FLDR_PATH']
    except:
        raise RMPyException(
            "ERROR: SEARCH_ROOT_FLDR_PATH must be specified for this option. \n")

    # Validate the folder path
    if not Path(ExtFilesFolderPath).exists():
        raise RMPyException("ERROR: Directory path not found:"
                            + G_QT + ExtFilesFolderPath + G_QT + "\n")
    if not Path(ExtFilesFolderPath).is_dir():
        raise RMPyException("ERROR: Path is not a directory:"
                            + G_QT + ExtFilesFolderPath + G_QT + "\n")

    # First check database for empty paths or filenames
    ReportEmptyPaths(dbConnection, reportF)

    cur = GetDBFileList(dbConnection)

    dbFileList = []
    for row in cur:
        if len(str(row[0])) == 0 or len(str(row[1])) == 0:
            continue
        if row[0][0] == '*':
            pass
        dirPath = ExpandDirPath(row[0])
        filePath = os.path.join(dirPath, row[1])
        dbFileList.append(filePath)

    mediaFileList = FolderContentsMinusIgnored(
        reportF, Path(ExtFilesFolderPath), config)

    caseSens = True
    if (caseSens == True):
        # case sensitive
        unRefFiles = list(set(mediaFileList).difference(dbFileList))
    else:
        mediaFileList_lc = [item.lower() for item in mediaFileList]
        dbFileList_lc = [item.lower() for item in dbFileList]
        unRefFiles = list(set(mediaFileList_lc).difference(dbFileList_lc))

    if len(unRefFiles) > 0:
        unRefFiles.sort()

        # don't print full path from root folder
        cutoff = len(ExtFilesFolderPath)
        for i in range(len(unRefFiles)):
            reportF.write("." + str(unRefFiles[i])[cutoff:] + "\n")

        reportF.write("\nFiles in processed folder not referenced by the database: "
                      + str(len(unRefFiles)) + "\n")
    else:
        reportF.write("\n    No unreferenced files were found.\n\n")

    reportF.write("\n    Folder processed: " + G_QT + ExtFilesFolderPath + G_QT
                  + "\n    Number of files " + str(len(mediaFileList))
                  + "  (exclusive of ignored items)"
                  + "\n    Number of database file links: " +
                  str(len(dbFileList))
                  + "\n    # DB links minus # non-ignored files: "
                  + str(len(dbFileList) - len(mediaFileList)) + "\n")

    Section("END", FeatureName, reportF)
    return


# ===================================================DIV60==
def FilesWithNoTagsFeature(config, dbConnection, reportF):

    FeatureName = "Files with no Tags"
    Label_OrigPath = "Path in database:  "
    FoundNoTagFiles = False

    Section("START", FeatureName, reportF)
    # get options
    ShowOrigPath = config['OPTIONS'].getboolean('SHOW_ORIG_PATH')

    cur = GetDBNoTagFileList(dbConnection)
    # row[0] = path,   row[1] = fileName

    for row in cur:
        FoundNoTagFiles = True
        dirPathOrig = row[0]
        dirPath = ExpandDirPath(row[0])
        filePath = Path(os.path.join(dirPath, row[1]))
        reportF.write(G_QT + str(filePath) + G_QT + "\n")
        if ShowOrigPath:
            reportF.write(Label_OrigPath
                          + G_QT + str(dirPathOrig) + G_QT + "\n")

    if not FoundNoTagFiles:
        reportF.write("\n    No files with no tags were found.\n")

    Section("END", FeatureName, reportF)
    return


# ===================================================DIV60==
def ListFoldersFeature(config, dbConnection, reportF):

    FeatureName = "Referenced Folders"
    Label_OrigPath = "Path in database:  "
    foundSomeFolders = False

    Section("START", FeatureName, reportF)
    # get options
    ShowOrigPath = config['OPTIONS'].getboolean('SHOW_ORIG_PATH')

    # First check database for empty paths or filenames
    # easier to handle them now than later
    ReportEmptyPaths(dbConnection, reportF)

    cur = GetDBFolderList(dbConnection)
    rows = cur.fetchall()
    for row in rows:
        if len(str(row[0])) == 0:
            continue
        foundSomeFolders = True
        reportF.write(str(ExpandDirPath(row[0])) + "\n")
        if ShowOrigPath:
            reportF.write(Label_OrigPath + row[0] + "\n")

    if foundSomeFolders:
        reportF.write("\nFolders referenced in database:  "
                      + str(len(rows)) + "\n")

    if not foundSomeFolders:
        reportF.write("\n    No folders found in database.\n")
    Section("END", FeatureName, reportF)

    return


# ===================================================DIV60==
def FindDuplcateFilePathsFeature(dbConnection, reportF):

    # this currently find exact duplicates as saved in DB path & filename (ignoring case)
    # duplicates *after expansion* of relative paths not found
    FeatureName = "Duplicated File Paths"
    foundSomeDupFiles = False

    Section("START", FeatureName, reportF)
    cur = GetDuplicateFilePathsList(dbConnection)

    for row in cur:
        foundSomeDupFiles = True
        dirPathOrig = row[0]
        dirPath = ExpandDirPath(row[0])
        filePath = Path(os.path.join(dirPath, row[1]))
        reportF.write(G_QT + str(filePath) + G_QT + "\n")

    if not foundSomeDupFiles:
        reportF.write(
            "\n    No Duplicate File Paths in Media Gallery were found.\n")

    Section("END", FeatureName, reportF)
    return


# ===================================================DIV60==
def FindDuplcateFileNamesFeature(dbConnection, reportF):

    # this finds exact filename duplicates as saved in DB (ignoring case)
    FeatureName = "Duplicated File Names"
    foundSomeDupFiles = False

    Section("START", FeatureName, reportF)
    cur = GetDuplicateFileNamesList(dbConnection)

    for row in cur:
        foundSomeDupFiles = True
        fileName = row[0]
        reportF.write(G_QT + str(fileName) + G_QT + "\n")

    if not foundSomeDupFiles:
        reportF.write(
            "\n    No Duplicate File Names in Media Gallery were found.\n")

    Section("END", FeatureName, reportF)
    return


# ===================================================DIV60==
def FileHashFeature(config, dbConnection, reportF):

    FeatureName = "Generate media files hash"
    Label_OrigPath = "Saved at:  "
    foundSomeMissingFiles = False

    print("\n Please wait, HASH file may take several minutes to generate.\n")

    Section("START", FeatureName, reportF)
    # get option
    try:
        hashFileFolder = config['FILE_PATHS']['HASH_FILE_FLDR_PATH']
    except:
        raise RMPyException(
            "ERROR: HASH_FILE_FLDR_PATH must be specified for this option. \n")

    hashFilePath = os.path.join(hashFileFolder, "MediaFiles_HASH_"
                                + TimeStampNow("file") + ".txt")

    try:
        hashFile = open(hashFilePath,  mode='w', encoding='utf-8')
    except:
        raise RMPyException('ERROR: Cannot create the hash file '
                            + hashFilePath + "\n\n")

    reportF.write("MD5 hash of files saved in file:\n" +
                  str(hashFilePath) + "\n\n")
    cur = GetDBFileList(dbConnection)
    # row[0] = path,   row[1] = fileName

    for row in cur:
        if len(str(row[0])) == 0 or len(str(row[1])) == 0:
            continue
        dirPathOrig = row[0]
        dirPath = ExpandDirPath(row[0])
        filePath = Path(os.path.join(dirPath, row[1]))
        if not dirPath.exists():
            foundSomeMissingFiles = True
            reportF.write("Directory path not found:\n"
                          + G_QT + str(dirPath) + G_QT + " for file: "
                          + G_QT + row[1] + G_QT + "\n")

        else:
            if filePath.exists():
                if not filePath.is_file():
                    foundSomeMissingFiles = True
                    reportF.write("File path is not a file: \n"
                                  + G_QT + str(filePath) + G_QT + "\n")
                # take hash
                BUF_SIZE = 65536  # reads in 64kb chunks

                md5 = hashlib.md5()
                # or sha1 = hashlib.sha1()

                with open(filePath, 'rb') as f:
                    while True:
                        data = f.read(BUF_SIZE)
                        if not data:
                            break
                        md5.update(data)
                hashFile.write(str(filePath) + "\n" + md5.hexdigest() + "\n\n")
            else:
                foundSomeMissingFiles = True
                reportF.write("File path not found: \n"
                              + G_QT + str(filePath) + G_QT + "\n")

    if not foundSomeMissingFiles:
        reportF.write("\n    All files were processed.\n")
    Section("END", FeatureName, reportF)

    return


# ===================================================DIV60==
def GetDBFolderList(dbConnection):

    SqlStmt = """
  SELECT  DISTINCT MediaPath
  FROM MultimediaTable
    ORDER BY MediaPath
  """
    cur = dbConnection.cursor()
    cur.execute(SqlStmt)
    return cur


# ===================================================DIV60==
def GetDBFileList(dbConnection):

    SqlStmt = """
  SELECT  MediaPath, MediaFile
  FROM MultimediaTable
    ORDER BY MediaPath, MediaFile COLLATE NOCASE
  """
    cur = dbConnection.cursor()
    cur.execute(SqlStmt)
    return cur


# ===================================================DIV60==
def ReportEmptyPaths(dbConnection, report_file):

    # First check database for empty paths or filenames
    # easier to handle them now than later

    SqlStmt = """
    SELECT  MediaPath, MediaFile, Caption, Description
    FROM MultimediaTable
    WHERE MediaPath == ''
       OR MediaFile == ''COLLATE NOCASE
    """
    cur = dbConnection.cursor()
    cur.execute(SqlStmt)

    rows = cur.fetchall()
    if len(rows) != 0:
        report_file.write(str(len(rows)) +
                      " entires with blank filename or path found:\n\n")
        for row in rows:
            # MediaPath, MediaFile, Caption, Description
            report_file.write("Path       =" + str(row[0]) + '\nFile Name  ='
                          + str(row[1]) + '\nCaption    ='
                          + row[2] + "\nDescription=" + row[3] + "\n\n")


# ===================================================DIV60==
def GetDBNoTagFileList(dbConnection):

    SqlStmt = """
  SELECT MediaPath, MediaFile
  FROM MultimediaTable mmt
  LEFT JOIN MediaLinkTable mlt ON mlt.MediaID =  mmt.MediaID
   WHERE OwnerType is NULL
   ORDER by MediaPath, MediaFile COLLATE NOCASE
   """
    cur = dbConnection.cursor()
    cur.execute(SqlStmt)
    return cur


# ===================================================DIV60==
def GetDuplicateFileNamesList(dbConnection):

    # see for examples
    # https://database.guide/6-ways-to-select-duplicate-rows-in-sqlite/
    SqlStmt = """
  SELECT p.MediaFile, COUNT(*) AS "Count"
  FROM MultimediaTable p
  GROUP BY MediaFile COLLATE NOCASE
  HAVING COUNT(*) > 1
  ORDER BY p.MediaFile COLLATE NOCASE
  """
    cur = dbConnection.cursor()
    cur.execute(SqlStmt)
    return cur


# ===================================================DIV60==
def GetDuplicateFilePathsList(dbConnection):

    SqlStmt = """
  SELECT p.MediaPath, p.MediaFile, COUNT(*) AS "Count"
  FROM MultimediaTable p
  GROUP BY MediaPath COLLATE NOCASE, MediaFile COLLATE NOCASE
  HAVING COUNT(*) > 1
  ORDER BY p.MediaFile COLLATE NOCASE
  """
    cur = dbConnection.cursor()
    cur.execute(SqlStmt)
    return cur


# ===================================================DIV60==
def GetSQLiteLibraryVersion(dbConnection):

    # returns a string like 3.42.0
    SqlStmt = """
  SELECT sqlite_version()
  """
    cur = dbConnection.cursor()
    cur.execute(SqlStmt)
    return cur.fetchone()[0]


# ===================================================DIV60==
def GetCurrentDirectory():

    # Determine if application is a script file or frozen exe and get its directory
    # see   https://pyinstaller.org/en/stable/runtime-information.html
    if getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS'):
        application_path = os.path.dirname(sys.executable)
    else:
        application_path = os.path.dirname(__file__)
    return application_path


# ===================================================DIV60==
def TimeStampNow(type=""):

    # return a TimeStamp string
    now = datetime.now()
    if type == '':
        dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
    elif type == 'file':
        dt_string = now.strftime("%Y-%m-%d_%H%M%S")
    return dt_string


# ===================================================DIV60==
def Section(pos, name, report_file):

    Divider = "="*60 + "===DIV70==\n"
    if pos == "START":
        text = "\n" + Divider + "\n=== Start of \"" + name + "\" listing\n\n"
    elif pos == "END":
        text = "\n=== End of \"" + name + "\" listing\n"
    elif pos == "FINAL":
        text = "\n" + Divider + "\n=== End of Report\n"
    else:
        raise RMPyException(
            "INTERNAL ERROR: Section position not correctly defined")

    report_file.write(text)
    report_file.flush()
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
        raise RMPyException(e, "\n\n" "Cannot open the RM database file." "\n")
    return db_connection


# ===================================================DIV60==
def ExpandDirPath(in_path):

    # deal with relative paths in RootsMagic 8 + 9 databases
    # RM7 path are always absolute and will never be processed here

    global G_MediaDirectoryPath
    path = str(in_path)
    # input parameter path should always be of type str, output will be Path
    # note when using Path / operator, second operand should not be absolute

    if path[0] == "~":
        absolutePath = Path(os.path.expanduser(path))

    elif path[0] == "?":
        if G_MediaDirectoryPath == "":
            G_MediaDirectoryPath = GetMediaDirectory()
        if len(path) == 1:
            absolutePath = Path(G_MediaDirectoryPath)
        else:
            absolutePath = Path(G_MediaDirectoryPath) / path[2:]

    elif path[0] == "*":
        if len(path) == 1:
            absolutePath = Path(G_DbFileFolderPath)
        else:
            absolutePath = Path(G_DbFileFolderPath) / path[2:]

    else:
        absolutePath = Path(path)

    return absolutePath


# ===================================================DIV60==
def GetMediaDirectory():

    #  Relies on the RM installed xml file containing application preferences
    #  File location set by RootsMagic installer
    RM_Config_FilePath_9 = r"~\AppData\Roaming\RootsMagic\Version 9\RootsMagicUser.xml"
    RM_Config_FilePath_8 = r"~\AppData\Roaming\RootsMagic\Version 8\RootsMagicUser.xml"

    mediaFolderPath = "RM8 or later not installed"

#  If xml settings file for RM 8 or 9 not found, return the medaiPath containing the
#  RM8 or later not installed message. It will never be used because RM 7 and earlier
#  does not need to know the media folder path.

#  Potential problem if RM 8 and 9 both installed and they have different
#  media folders specified. The highest version number path is found here.

#  Could base this off of the database version number, but that's not readily available.

    xmlSettingsPath = Path(os.path.expanduser(RM_Config_FilePath_9))
    if not xmlSettingsPath.exists():
        xmlSettingsPath = Path(os.path.expanduser(RM_Config_FilePath_8))
        if not xmlSettingsPath.exists():
            return mediaFolderPath

    root = ET.parse(xmlSettingsPath)
    MediaFolderPathEle = root.find("./Folders/Media")
    mediaFolderPath = MediaFolderPathEle.text

    return mediaFolderPath


# ===================================================DIV60==
def FolderContentsMinusIgnored(reportF, dirPath, config):

    ignoredFolderNames = []
    ignoredFileNames = []
    try:
        ignoredFolderNames = config['IGNORED_OBJECTS'].get(
            'FOLDERS').split('\n')
    except:
        reportF.write("No ignored folders specified.\n\n")
    try:
        ignoredFileNames = config['IGNORED_OBJECTS'].get(
            'FILENAMES').split('\n')
    except:
        reportF.write("No ignored files specified.\n\n")

    mediaFileList = []
    for (dirname, dirnames, filenames) in os.walk(dirPath, topdown=True):

        for igFldrName in ignoredFolderNames:
            if igFldrName in dirnames:
                dirnames.remove(igFldrName)

        for igFileName in ignoredFileNames:
            if igFileName in filenames:
                filenames.remove(igFileName)

        for filename in filenames:
            mediaFileList.append(str(os.path.join(dirname, filename)))

    return mediaFileList


# ===================================================DIV60==
def pause_with_message(message=None):

    if (message != None):
        print(str(message))
    input("\n" "Press the <Enter> key to continue...")
    return

# ===================================================DIV60==
class RMPyException(Exception):

    '''Exceptions thrown for configuration/database issues'''


# ===================================================DIV60==
# Call the "main" function
if __name__ == '__main__':
    main()

# ===================================================DIV60==
