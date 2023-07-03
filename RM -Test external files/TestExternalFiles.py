import os
import sys
import time
import sqlite3
from pathlib  import Path
from datetime import datetime
import configparser
import xml.etree.ElementTree as ET
import hashlib


## This script can only read a RootsMagic database file and cannot change it.
## However, until trust is established, make a backup before use.

##  Requirements: (see ReadMe.txt for details)
##   RootsMagic v7, v8 or v9 database file
##   RM-Python-config.ini  ( Configuration ini text file to set options and parameters)
##   unifuzz64.dll
##   Python v3.9 or greater


# ===================================================DIV60==
#  Global Variables
G_MediaDirectoryPath = ""
G_DbFileFolderPath = ""
G_QT = "\""


# ===================================================DIV60==
def main():
  global G_DbFileFolderPath

  # Configuration
  IniFileName = "RM-Python-config.ini"

  # ini file must be in "current directory" and encoded as UTF-8 (no BOM).
  # see   https://docs.python.org/3/library/configparser.html
  IniFile = os.path.join(GetCurrentDirectory(), IniFileName)

  # Check that ini file is at expected path and that it is readable & valid.
  if not os.path.exists(IniFile):
      print("ERROR: The ini configuration file, " + IniFileName + " must be in the same directory as the .py or .exe file.\n\n" )
      input("Press the <Enter> key to exit...")
      return

  config = configparser.ConfigParser(empty_lines_in_values=False)
  try:
    config.read(IniFile, 'UTF-8')
  except:
   print("ERROR: The " + IniFileName + " file contains a format error and cannot be parsed.\n\n" )
   input("Press the <Enter> key to exit...")
   return

  # Set up the report file first. That's where all subsequent user messages will appear.
  try:
    report_Path   = config['FILE_PATHS']['REPORT_FILE_PATH']
  except:
    print('ERROR: REPORT_FILE_PATH must be defined in the ' + IniFileName + "\n\n")
    input("Press the <Enter> key to exit...")
    return

  try:
    # Use UTF-8 encoding for the report file. Include BOM.
    open( report_Path,  mode='w', encoding='utf-8-sig')
  except:
    print('ERROR: Cannot create the report file ' + report_Path + "\n\n")
    input("Press the <Enter> key to exit...")
    return

  # Read database and dll file paths from ini file
  with open( report_Path,  mode='w', encoding='utf-8-sig') as reportF:
    try:
      database_Path = config['FILE_PATHS']['DB_PATH']
      RMNOCASE_Path = config['FILE_PATHS']['RMNOCASE_PATH']
    except:
      reportF.write('Both DB_PATH and RMNOCASE_PATH must be specified.')
      return

    if not os.path.exists(database_Path):
      reportF.write('Path for database not found: ' + database_Path)
      reportF.write('checked for: ' + os.path.abspath(database_Path))
      return
    if not os.path.exists(RMNOCASE_Path):
      reportF.write('Path for RMNOCASE_PATH dll not found: ' + RMNOCASE_Path)
      reportF.write('checked for: ' + os.path.abspath(RMNOCASE_Path))
      return

    # RM database file specific info
    FileModificationTime = datetime.fromtimestamp(os.path.getmtime(database_Path))
    G_DbFileFolderPath = Path(database_Path).parent

    # write header to report file
    with create_DBconnection(database_Path, RMNOCASE_Path, reportF) as dbConnection:
      reportF.write ("Report generated at      = " + TimeStampNow() + "\n")
      reportF.write ("Database processed       = " + os.path.abspath(database_Path) + "\n")
      reportF.write ("Database last changed on = " + FileModificationTime.strftime("%Y-%m-%d %H:%M:%S") + "\n")
      reportF.write ("SQLite library version   = " + GetSQLiteLibraryVersion (dbConnection) + "\n\n")

      # test option values conversion to boolean
      try:
        config['OPTIONS'].getboolean('CHECK_FILES')
        config['OPTIONS'].getboolean('UNREF_FILES')
        config['OPTIONS'].getboolean('FOLDER_LIST')
        config['OPTIONS'].getboolean('NO_TAG_FILES')
        config['OPTIONS'].getboolean('DUP_FILENAMES')
        config['OPTIONS'].getboolean('DUP_FILEPATHS')
        config['OPTIONS'].getboolean('SHOW_ORIG_PATH')
        config['OPTIONS'].getboolean('HASH_FILE')
      except:
        reportF.write ("One of the OPTIONS values could not be parsed as boolean. \n")
        sys.exit()

      # Run the requested options. Usually multiple options.
      if config['OPTIONS'].getboolean('CHECK_FILES'):
         ListMissingFilesFeature(config, dbConnection, reportF)

      if config['OPTIONS'].getboolean('UNREF_FILES'):
         ListUnReferencedFilesFeature(config, dbConnection, reportF)

      if config['OPTIONS'].getboolean('FOLDER_LIST'):
         ListFoldersFeature(config, dbConnection, reportF)

      if config['OPTIONS'].getboolean('NO_TAG_FILES'):
         FilesWithNoTagsFeature(config, dbConnection, reportF)

      if config['OPTIONS'].getboolean('DUP_FILEPATHS'):
         FindDuplcateFilePathsFeature(dbConnection, reportF)

      if config['OPTIONS'].getboolean('DUP_FILENAMES'):
         FindDuplcateFileNamesFeature(dbConnection, reportF)

      if config['OPTIONS'].getboolean('HASH_FILE'):
         FileHashFeature(config, dbConnection, reportF)

    Section( "FINAL", "", reportF)
  return 0


# ===================================================DIV60==
def ListUnReferencedFilesFeature(config, dbConnection, reportF):
  FeatureName = "Unreferenced Files"

  Section( "START", FeatureName, reportF)
  # get option
  try:
    ExtFilesFolderPath = config['FILE_PATHS']['SEARCH_ROOT_FLDR_PATH']
  except:
    reportF.write ("ERROR: SEARCH_ROOT_FLDR_PATH must be specified for this option. \n")
    sys.exit()

  # Validate the folder path
  if not Path(ExtFilesFolderPath).exists():
    reportF.write ("ERROR: Directory path not found:" + G_QT + ExtFilesFolderPath + G_QT + "\n")
    sys.exit()
  if not Path(ExtFilesFolderPath).is_dir():
    reportF.write ("ERROR: Path is not a directory:" + G_QT + ExtFilesFolderPath + G_QT + "\n")
    sys.exit()

  cur= GetDBFileList(dbConnection)

  dbFileList=[]
  for row in cur:
    dirPath=ExpandDirPath(row[0])
    filePath=os.path.join(dirPath, row[1])
    dbFileList.append(filePath)

  mediaFileList = FolderContentsMinusIgnored(reportF, Path(ExtFilesFolderPath), config)

  caseSens = True
  if (caseSens == True):
    # case sensitive
    unRefFiles = list(set(mediaFileList).difference(dbFileList))
  else:
    mediaFileList_lc = [item.lower() for item in mediaFileList]
    dbFileList_lc = [item.lower() for item in dbFileList]
    unRefFiles = list(set(mediaFileList_lc).difference(dbFileList_lc))

  if len(unRefFiles) >0:
    unRefFiles.sort()

    # don't print full path from root folder
    cutoff = len(ExtFilesFolderPath)

    for i in range(len(unRefFiles)):
      reportF.write("." + str(unRefFiles[i])[cutoff:] + "\n")

    reportF.write( "\nFiles in processed folder not referenced by the database: "
         + str(len(unRefFiles))  + "\n")
  else: reportF.write ("\n    No unreferenced files were found.\n\n")

  reportF.write("    Folder processed: " + G_QT + ExtFilesFolderPath + G_QT + "\n")
  reportF.write("    Contains " + str(len(mediaFileList))
       + " files (not counting ignored items)\n")
  reportF.write("    Database file links: " + str(len(dbFileList)) + "\n")
  reportF.write("    Unexplained extra DB links: " + str( len(dbFileList) - len(mediaFileList) ) + "\n")


  Section( "END", FeatureName, reportF)
  return


# ===================================================DIV60==
def FilesWithNoTagsFeature(config, dbConnection, reportF):
  FeatureName = "Files with no Tags"
  Label_OrigPath="Path in database:  "
  FoundNoTagFiles = False

  Section( "START", FeatureName, reportF)
  # get options
  ShowOrigPath = config['OPTIONS'].getboolean('SHOW_ORIG_PATH')

  cur= GetDBNoTagFileList(dbConnection)
  # row[0] = path,   row[1] = fileName

  for row in cur:
    FoundNoTagFiles = True
    dirPathOrig = row[0]
    dirPath = ExpandDirPath(row[0])
    filePath = dirPath / row[1]
    reportF.write ( G_QT + str(filePath) + G_QT + "\n")
    if ShowOrigPath: reportF.write (Label_OrigPath + G_QT + str(dirPathOrig) + G_QT + "\n")

  if not FoundNoTagFiles: reportF.write ("\n    No files with no tags were found.\n")

  Section( "END", FeatureName, reportF)
  return


# ===================================================DIV60==
def FindDuplcateFilePathsFeature(dbConnection, reportF):
# this currently find exact duplicates as saved in DB path & filename (ignoring case)
# duplicates *after expansion* of relative paths not found
  FeatureName = "Duplicated File Paths"
  foundSomeDupFiles = False

  Section( "START", FeatureName, reportF)
  cur= GetDuplicateFilePathsList(dbConnection)

  for row in cur:
    foundSomeDupFiles = True
    dirPathOrig = row[0]
    dirPath = ExpandDirPath(row[0])
    filePath = dirPath / row[1]
    reportF.write (G_QT + str(filePath) + G_QT + "\n")

  if not foundSomeDupFiles: reportF.write ("\n    No Duplicate File Paths in Media Gallery were found.\n")

  Section( "END", FeatureName, reportF)
  return


# ===================================================DIV60==
def FindDuplcateFileNamesFeature(dbConnection, reportF):
# this finds exact filename duplicates as saved in DB (ignoring case)
  FeatureName = "Duplicated File Names"
  foundSomeDupFiles = False

  Section( "START", FeatureName, reportF)
  cur= GetDuplicateFileNamesList(dbConnection)

  for row in cur:
    foundSomeDupFiles = True
    fileName = row[0]
    reportF.write (G_QT + str(fileName) + G_QT + "\n")

  if not foundSomeDupFiles: reportF.write ("\n    No Duplicate File Names in Media Gallery were found.\n")

  Section( "END", FeatureName, reportF)
  return


# ===================================================DIV60==
def ListFoldersFeature(config, dbConnection, reportF):
  FeatureName = "Referenced Folders"
  Label_OrigPath="Path in database:  "
  foundSomeFolders=False

  Section( "START", FeatureName, reportF)
  # get options
  ShowOrigPath = config['OPTIONS'].getboolean('SHOW_ORIG_PATH')

  cur= GetDBFolderList(dbConnection)
  rows = cur.fetchall()
  for row in rows:
    foundSomeFolders=True
    reportF.write(str(ExpandDirPath(row[0])) + "\n")
    if ShowOrigPath: reportF.write(Label_OrigPath + row[0] + "\n")

  if foundSomeFolders: reportF.write ("\nFolders referenced in database:  " + str(len(rows)) +  "\n")

  if not foundSomeFolders: reportF.write ("\n    No folders found in database.\n")
  Section( "END", FeatureName, reportF)

  return


# ===================================================DIV60==
def ListMissingFilesFeature( config, dbConnection, reportF ):
  FeatureName = "Files Not Found"
  Label_OrigPath="Path in database:  "
  foundSomeMissingFiles=False

  Section( "START", FeatureName, reportF)
  # get options
  ShowOrigPath = config['OPTIONS'].getboolean('SHOW_ORIG_PATH')

  cur= GetDBFileList(dbConnection)
  # row[0] = path,   row[1] = fileName

  for row in cur:
    dirPathOrig = row[0]
    dirPath = ExpandDirPath(row[0])
    filePath = dirPath / row[1]
    if not dirPath.exists():
      foundSomeMissingFiles=True
      reportF.write ("Directory path not found:\n"
            + G_QT + str(dirPath) + G_QT + " for file: " + G_QT + row[1] + G_QT + "\n")
      if ShowOrigPath: reportF.write (Label_OrigPath + G_QT + str(dirPathOrig) + G_QT + "\n")

    else:
      if filePath.exists():
        if not filePath.is_file():
          foundSomeMissingFiles=True
          reportF.write ("File path is not a file: \n" + G_QT + str(filePath) + G_QT + "\n")
          if ShowOrigPath: reportF.write (Label_OrigPath + G_QT + str(dirPathOrig) + G_QT + "\n")

      else:
        foundSomeMissingFiles=True
        reportF.write ("File path not found: \n" + G_QT + str(filePath) + G_QT + "\n")
        if ShowOrigPath: reportF.write (Label_OrigPath + G_QT + str(dirPathOrig) + G_QT + "\n")

  if not foundSomeMissingFiles: reportF.write ("\n    No files were found missing.\n")
  Section( "END", FeatureName, reportF)
  return


# ===================================================DIV60==
def FileHashFeature(config, dbConnection, reportF):
  FeatureName = "Generate media files hash"
  Label_OrigPath="Saved at:  "
  foundSomeMissingFiles=False

  Section( "START", FeatureName, reportF)
  # get option
  try:
    hashFileFolder = config['FILE_PATHS']['HASH_FILE_FLDR_PATH']
  except:
    reportF.write ("ERROR: HASH_FILE_FLDR_PATH must be specified for this option. \n")
    sys.exit()

  hashFilePath = os.path.join( hashFileFolder , "MediaFiles_HASH_" + TimeStampNow("file") +".txt" )

  try:
    hashFile = open( hashFilePath,  mode='w', encoding='utf-8-sig')
  except:
    print('ERROR: Cannot create the hash file ' + hashFilePath + "\n\n")
    input("Press the <Enter> key to exit...")
    return

  reportF.write( "MD5 hash of files saved in file:\n" + str(hashFilePath) + "\n\n")
  cur= GetDBFileList(dbConnection)
  # row[0] = path,   row[1] = fileName

  for row in cur:
    dirPathOrig = row[0]
    dirPath = ExpandDirPath(row[0])
    filePath = dirPath / row[1]
    if not dirPath.exists():
      foundSomeMissingFiles=True
      reportF.write ("Directory path not found:\n"
            + G_QT + str(dirPath) + G_QT + " for file: " + G_QT + row[1] + G_QT + "\n")

    else:
      if filePath.exists():
        if not filePath.is_file():
          foundSomeMissingFiles=True
          reportF.write ("File path is not a file: \n" + G_QT + str(filePath) + G_QT + "\n")
        # take hash
        BUF_SIZE = 65536  # lets read stuff in 64kb chunks!

        md5 = hashlib.md5()
        # or sha1 = hashlib.sha1()

        with open(filePath, 'rb') as f:
            while True:
                data = f.read(BUF_SIZE)
                if not data:
                    break
                md5.update(data)
        hashFile.write( str(filePath) + "\n" + md5.hexdigest() + "\n\n" )
      else:
        foundSomeMissingFiles=True
        reportF.write ("File path not found: \n" + G_QT + str(filePath) + G_QT + "\n")

  if not foundSomeMissingFiles: reportF.write ("\n    All files were processed.\n")

  Section( "END", FeatureName, reportF)
  return


# ===================================================DIV60==
def GetDBFolderList(dbConnection):
  SqlStmt="""\
  SELECT  DISTINCT MediaPath
  FROM MultimediaTable
    ORDER BY MediaPath
"""
  cur = dbConnection.cursor()
  cur.execute(SqlStmt)
  return cur


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
def GetDBFileList(dbConnection):
  SqlStmt="""\
  SELECT  MediaPath, MediaFile
  FROM MultimediaTable
    ORDER BY MediaPath, MediaFile
"""
  cur = dbConnection.cursor()
  cur.execute(SqlStmt)
  return cur


# ===================================================DIV60==
def GetDBNoTagFileList(dbConnection):

  SqlStmt="""\
  SELECT MediaPath, MediaFile
  FROM MultimediaTable mmt
  LEFT JOIN MediaLinkTable mlt ON mlt.MediaID =  mmt.MediaID
   WHERE OwnerType is NULL
   ORDER by MediaPath, MediaFile
"""
  cur = dbConnection.cursor()
  cur.execute(SqlStmt)
  return cur


# ===================================================DIV60==
def GetDuplicateFileNamesList(dbConnection):
  # see for examples https://database.guide/6-ways-to-select-duplicate-rows-in-sqlite/
  SqlStmt="""\
  SELECT p.MediaFile, COUNT(*) AS "Count"
  FROM MultimediaTable p
  GROUP BY MediaFile COLLATE NOCASE
  HAVING COUNT(*) > 1
  ORDER BY p.MediaFile
  """
  cur = dbConnection.cursor()
  cur.execute(SqlStmt)
  return cur


# ===================================================DIV60==
def GetDuplicateFilePathsList(dbConnection):
  # see for examples https://database.guide/6-ways-to-select-duplicate-rows-in-sqlite/
  SqlStmt="""\
  SELECT p.MediaPath, p.MediaFile, COUNT(*) AS "Count"
  FROM MultimediaTable p
  GROUP BY MediaPath COLLATE NOCASE, MediaFile COLLATE NOCASE
  HAVING COUNT(*) > 1
  ORDER BY p.MediaFile
  """
  cur = dbConnection.cursor()
  cur.execute(SqlStmt)
  return cur


# ===================================================DIV60==
def GetSQLiteLibraryVersion (dbConnection):
  # returns a string like 3.42.0
  SqlStmt="""\
  SELECT sqlite_version()
  """
  cur = dbConnection.cursor()
  cur.execute(SqlStmt)
  return cur.fetchone()[0]


# ===================================================DIV60==
def Section (pos, name, reportF):
  Divider = "="*60 + "===DIV70==\n"
  if   pos == "START":  text = "\n" + Divider + "\n=== Start of \"" + name + "\" listing\n\n"
  elif pos == "END":  text = "\n=== End of \"" + name + "\" listing\n"
  elif pos == "FINAL":  text = "\n" + Divider + "\n=== End of Report\n"
  else:
    text = "not defined"
    print("INTERNAL ERROR: Section position not correctly defined")
    input("Press the <Enter> key to exit...")
    sys.exit()

  reportF.write (text)
  reportF.flush()
  return


# ===================================================DIV60==
def create_DBconnection(db_file_path, RMNOCASE_Path, reportF):
    dbConnection = None
    try:
      dbConnection = sqlite3.connect(db_file_path)
      dbConnection.enable_load_extension(True)
      dbConnection.load_extension(RMNOCASE_Path)
    except Error as e:
        reportF.write(e)
        reportF.write("\n\n")
        reportF.write( "Cannot open the RM database file. \n")
        input("Press the <Enter> key to exit...")
        sys.exit()
    return dbConnection


# ===================================================DIV60==
def ExpandDirPath(in_path):
  # deal with relative paths in RootsMagic 8 + 9 databases
  # RM7 path are always absolute and will never be changed here

  global G_MediaDirectoryPath
  path = str(in_path)
  # input parameter path should always be of type str, output will be Path
  # note when using Path / operator, second operand should not be absolute

  if path[0] == "~" :
     absolutePath = Path(os.path.expanduser(path))

  elif path[0] == "?":
    if G_MediaDirectoryPath == "":
       G_MediaDirectoryPath = GetMediaDirectory()
    if len(path) == 1 : absolutePath = Path(G_MediaDirectoryPath)
    else: absolutePath = Path(G_MediaDirectoryPath) / path[2:]

  elif path[0] == "*":
    if len(path) == 1 : absolutePath = Path(G_DbFileFolderPath)
    else: absolutePath = Path(G_DbFileFolderPath) / path[2:]

  else:
    absolutePath = Path(path)

  return absolutePath


# ===================================================DIV60==
def GetMediaDirectory():
#  File location set by RootsMagic installer
  RM_Config_FilePath_9 = r"~\AppData\Roaming\RootsMagic\Version 9\RootsMagicUser.xml"
  RM_Config_FilePath_8 = r"~\AppData\Roaming\RootsMagic\Version 8\RootsMagicUser.xml"

  mediaFolderPath = "RM8 or later not installed"

#  If xml settings file for RM 8 or 9 not found, return the medaiPath containing the
#  RM8 or later not installed message. It will never be used  becasue RM 7 does not
#  need to know the media folder path.

#  Potential problem if RM 8 and 9 both installed and they have different
#  media folders specified. The highest ver number path is found here.

#  Could base this off of the database version number, but that's not readily available.

  xmlSettingsPath=Path(os.path.expanduser(RM_Config_FilePath_9))
  if not xmlSettingsPath.exists():
    xmlSettingsPath=Path(os.path.expanduser(RM_Config_FilePath_8))
    if not xmlSettingsPath.exists():
      return mediaFolderPath

  root = ET.parse(xmlSettingsPath)
  MediaFolderPathEle = root.find( "./Folders/Media")
  mediaFolderPath = MediaFolderPathEle.text

  return mediaFolderPath


# ===================================================DIV60==
def FolderContentsMinusIgnored(reportF, dirPath, config):
  ignoredFolderNames=[]
  ignoredFileNames=[]
  try:
    ignoredFolderNames = config['IGNORED_OBJECTS'].get('FOLDERS').split('\n')
  except:
    reportF.write ("No ignored folders specified.\n\n")
  try:
    ignoredFileNames   = config['IGNORED_OBJECTS'].get('FILENAMES').split('\n')
  except:
    reportF.write ("No ignored files specified.\n\n")

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
# Call the "main" function
if __name__ == '__main__':
    main()

# ===================================================DIV60==
