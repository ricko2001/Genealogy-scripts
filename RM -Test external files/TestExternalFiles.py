import sqlite3
import os
import time
from pathlib  import Path
from datetime import datetime
import configparser
import xml.etree.ElementTree as ET

##  This script only reads RootsMagic database files and will not harm it.
## However, until trust is established, make a backup before use.

##  Requirements: (see ReadMe.txt for details)
##   RootsMagic v7 or v8.0 database file
##   RM-Python-config.ini  ( Configuration ini file to set options and parameters)
##   unifuzz64.dll
##   Python v3.9 or greater

# TODO
# better error handling when opening database


# ===================================================DIV60==
#  Global Variables
G_MediaDirectoryPath = ""
G_DbFileFolderPath = ""
G_Divider = "=====================================================DIV60=="
G_QT = "\""


# ===================================================DIV60==
def create_DBconnection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


# ===================================================DIV60==
def ListFoldersFeature(conn, reportF):
    SqlStmt="""\
      SELECT  DISTINCT MediaPath
      FROM MultimediaTable
        ORDER BY MediaPath
"""
    cur = conn.cursor()
    cur.execute(SqlStmt)

    rows = cur.fetchall()
    reportF.write (G_Divider + "\nStart of \"Referenced Folders\" listing\n\n")

    for row in rows:
      reportF.write(row[0] + "\n")
    reportF.write ("\n" + str(len(rows)) + "  folders referenced in RootsMagic file \n")

    reportF.write ("End of \"Referenced Folders\" listing\n\n")

    return rows


# ===================================================DIV60==
def GetDBFileList(conn):
    SqlStmt="""\
      SELECT  MediaPath, MediaFile
      FROM MultimediaTable
        ORDER BY MediaPath, MediaFile
"""
    cur = conn.cursor()
    cur.execute(SqlStmt)
    return cur

# ===================================================DIV60==
def GetDBNoTagFileList(conn):

    SqlStmt="""\
      SELECT MediaPath, MediaFile
      FROM MultimediaTable mmt
      LEFT JOIN MediaLinkTable mlt ON mlt.MediaID =  mmt.MediaID
       WHERE OwnerType is NULL
       ORDER by MediaPath, MediaFile
"""
    cur = conn.cursor()
    cur.execute(SqlStmt)
    return cur

# ===================================================DIV60==
def GetDuplicateFileList(conn):

    SqlStmt="""\
      SELECT p.MediaPath, p.MediaFile, p.rowid
      FROM MultimediaTable p 
      JOIN 
      (
      SELECT MediaPath, MediaFile, count(*) as cnt 
      FROM MultimediaTable 
      GROUP BY MediaPath, MediaFile
      ) t 
      ON LOWER(p.MediaPath) = LOWER(t.MediaPath) AND LOWER(p.MediaFile) = LOWER(t.MediaFile) 
      WHERE t.cnt > 1 
      
      ORDER BY p.MediaFile;
"""
    cur = conn.cursor()
    cur.execute(SqlStmt)
    return cur

# ===================================================DIV60==
def ExpandDirPath(in_path):
  # deal with relative paths in RootsMagic 8 databases
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
  RM_Config_FilePath = r"~\AppData\Roaming\RootsMagic\Version 8\RootsMagicUser.xml"

#  if file not found, RM8 not installed, Media folder path will never be used
  myPath=Path(os.path.expanduser(RM_Config_FilePath))
  if not myPath.exists():
    path = "RM8 not installed"
  else:
    root = ET.parse(myPath)
    MediaFolderPathEle = root.find( "./Folders/Media")
    path = MediaFolderPathEle.text
  return path


# ===================================================DIV60==
def ListMissingFilesFeature( config, conn, reportF ):
  # get options
  ShowOrigPath = config['Options'].getboolean('SHOW_ORIG_PATH')

  cur= GetDBFileList(conn)
  # row[0] = path,   row[1] = fileName

  Label_OrigPath="  Actual path in MultimediaTable:"

  reportF.write (G_Divider + "\n=== Start of \"Files Not Found\" listing\n")
  foundSomeMissingFiles=False
  for row in cur:
    dirPathOrig = row[0]
    dirPath = ExpandDirPath(row[0])
    filePath = dirPath / row[1]
    if not dirPath.exists(): 
       foundSomeMissingFiles=True
       reportF.write ("\nDirectory path not found:\n" 
             + G_QT + str(dirPath) + G_QT + " for file: " + G_QT + row[1] + G_QT + "\n")
       if ShowOrigPath: reportF.write (Label_OrigPath + G_QT + str(dirPathOrig) + G_QT + "\n")

    else:
        if filePath.exists():
            if not filePath.is_file():
                foundSomeMissingFiles=True
                reportF.write ("\nFile path is not a file: \n" + G_QT + str(filePath) + G_QT + "\n")
                if ShowOrigPath: reportF.write (Label_OrigPath + G_QT + str(dirPathOrig) + G_QT + "\n")

        else:
            foundSomeMissingFiles=True
            reportF.write ("\nFile path not found: \n" + G_QT + str(filePath) + G_QT + "\n")
            if ShowOrigPath: reportF.write (Label_OrigPath + G_QT + str(dirPathOrig) + G_QT + "\n")


  if foundSomeMissingFiles == False:
     reportF.write ("\n    No files were found missing.\n")
  reportF.write ("\n=== End of \"Files Not Found\" listing\n\n")
  return


# ===================================================DIV60==
def FolderContentsMinusIgnored(dirPath, config):
  ignoredFolderNames = config.get('Ignored Objects', 'folders').split('\n')
  ignoredFileNames   = config.get('Ignored Objects', 'filenames').split('\n')

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
def ListUnReferencedFilesFeature(config, conn, reportF):
  foundSomeExtraFiles=False
  reportF.write(G_Divider + "\n=== Start \"Unreferenced Files\" listing\n\n")

  ExtFilesFolderPath = Path(config['File Paths']['SEARCH_ROOT_FLDR_PATH'])
  if not ExtFilesFolderPath.exists(): 
    reportF.write ("ERROR: Directory path not found:" + "\"" + str(ExtFilesFolderPath) + "\"" + "\n")
    sys.exit()
  if not ExtFilesFolderPath.is_dir():
    reportF.write ("ERROR: Path is not a directory:" + "\"" + str(ExtFilesFolderPath) + "\"" + "\n")
    sys.exit()
  cur= GetDBFileList(conn)

  dbFileList=[]
  for row in cur:
    dirPath=ExpandDirPath(row[0])
    filePath=os.path.join(dirPath, row[1])
    dbFileList.append(filePath)

  mediaFileList = FolderContentsMinusIgnored(ExtFilesFolderPath, config)

  unRefFiles = list(set(mediaFileList).difference(dbFileList))
  if len(unRefFiles) >0: foundSomeExtraFiles=True
  unRefFiles.sort()


  if foundSomeExtraFiles:

    # don't print full path from root folder
    cutoff = len(str(ExtFilesFolderPath))

    for i in range(len(unRefFiles)):
      reportF.write("." + str(unRefFiles[i])[cutoff:] + "\n")


    reportF.write( "\n\nNumber of files in External files folder not referenced by the database: "
         + str(len(unRefFiles))  + "\n\n\n")

  else:
    reportF.write ("    No unreferenced files were found.\n\n")

  reportF.write("Folder processed: " + str(ExtFilesFolderPath) + "\n")
  reportF.write("External files folder contains " + str(len(mediaFileList)) 
       + " files (not counting ignored items)\n")
  reportF.write("Database contains " + str(len(dbFileList)) + " file links\n\n")

  reportF.write("=== End \"Unreferenced Files\" listing\n\n")
  return



# ===================================================DIV60==
def FilesWithNoTagsFeature(config, conn, reportF):
  # get options
  ShowOrigPath = config['Options'].getboolean('SHOW_ORIG_PATH')

  cur= GetDBNoTagFileList(conn)
  # row[0] = path,   row[1] = fileName
  Label_OrigPath="  Actual path in MultimediaTable:"

  FoundNoTagFiles = True
  reportF.write (G_Divider + "\n=== Start of \"Files with no Tags\" listing\n")


  for row in cur:
    FoundNoTagFiles = False
    dirPathOrig = row[0]
    dirPath = ExpandDirPath(row[0])
    filePath = dirPath / row[1]
    reportF.write ("\n" + G_QT + str(filePath) + G_QT + "\n")
    if ShowOrigPath: reportF.write (Label_OrigPath + G_QT + str(dirPathOrig) + G_QT + "\n")

  if FoundNoTagFiles: reportF.write ("\n    No files with no tags were found.\n")

  reportF.write ("\n=== End of \"Files with no Tags\" listing\n\n")

  return


# ===================================================DIV60==
def FindDuplcateFilesFeature(conn, reportF):
  foundSomeDupFiles=False

  return


# ===================================================DIV60==
def TimeStamp():
     # return a TimeStamp string
     now = datetime.now()
     dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
     return dt_string


# ===================================================DIV60==
def main():
  global G_DbFileFolderPath

  # Configuration file
  IniFile="RM-Python-config.ini"
  
  # ini file must be in "current directory" and encoded as UTF-8 if non-ASCII chars present (no BOM)
  if not os.path.exists(IniFile):
      print("ERROR: The ini configuration file, " + IniFile + " must be in the current directory." )
      return

  config = configparser.ConfigParser()
  config.read(IniFile, 'UTF-8')

  # Read file paths from ini file
  report_Path   = config['File Paths']['REPORT_PATH']
  database_Path = config['File Paths']['DB_PATH']
  RMNOCASE_Path = config['File Paths']['RMNOCASE_PATH']

  if not os.path.exists(database_Path):
      print('Database path not found')
      return

  FileModificationTime = datetime.fromtimestamp(os.path.getmtime(database_Path))

  G_DbFileFolderPath = Path(database_Path).parent

  # Process the database for requested output
  with create_DBconnection(database_Path) as conn:
    conn.enable_load_extension(True)
    conn.load_extension(RMNOCASE_Path)

    with open( report_Path,  mode='w', encoding='utf-8-sig') as reportF:
      reportF.write ("Report generated at      = " + TimeStamp() + "\n")  
      reportF.write ("Database processed       = " + database_Path + "\n")
      reportF.write ("Database last changed on = " + FileModificationTime.strftime("%Y-%m-%d %H:%M:%S") + "\n\n")

      if config['Options'].getboolean('CHECK_FILES'):
         ListMissingFilesFeature(config, conn, reportF)

      if config['Options'].getboolean('UNREF_FILES'):
         ListUnReferencedFilesFeature(config, conn, reportF)

      if config['Options'].getboolean('FOLDER_LIST'):
         ListFoldersFeature(conn, reportF)

      if config['Options'].getboolean('NO_TAG_FILES'):
         FilesWithNoTagsFeature(config, conn, reportF)

      if config['Options'].getboolean('DUP_FILES'):
         FindDuplcateFilesFeature(conn, reportF)

      #reportF.write ("\n")
      reportF.write (G_Divider + "\n\nEnd of report \n")
  return 0


# ===================================================DIV60==
# Call the "main" function
if __name__ == '__main__':
    main()