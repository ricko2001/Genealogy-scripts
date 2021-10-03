import sqlite3
import os
import time
from pathlib  import Path
from datetime import datetime
import configparser
import xml.etree.ElementTree as ET

##  This script only reads the RootsMagic database file and cannot harm it.

##  Requirements: (see ReadMe.txt for details)
##   Rootsmagic v7 or v8.0.0.0 database file
##   unifuzz64.dll
##   RM-Python-config.ini  ( Configuration ini file to set options and parametrs)
##   Python v3.9 or greater

# TODO
# better error handling opening database
# check database schema version, or at least confirm that the database is not RM8

#  Global Variables
#  paths may be relative to user's home dir or application set "media folder"
G_HomeDirectory = ""
G_MediaDirectory = ""



# ================================================================
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
    except Error as e:
        print(e)

    return conn


# ================================================================
def ListFolders(conn, reportF):

    SqlStmt="""\
      SELECT  DISTINCT MediaPath
      FROM MultimediaTable
        ORDER BY MediaPath
"""
    cur = conn.cursor()
    cur.execute(SqlStmt)

    rows = cur.fetchall()
    reportF.write ("Start of \"Referenced Folders\" listing\n\n")

    for row in rows:
      reportF.write(row[0] + "\n")
    reportF.write (str(len(rows)) + "  folders referenced in RootsMagic file \n\n")

    reportF.write ("End of \"Referenced Folders\" listing\n\n")

    return rows


# ================================================================
def GetDBFileList(conn):

    SqlStmt="""\
      SELECT  MediaPath, MediaFile
      FROM MultimediaTable
        ORDER BY MediaPath, MediaFile
"""
    cur = conn.cursor()
    cur.execute(SqlStmt)
    return cur


# ================================================================
def ExpandDirPath(path):
  # deal with relative paths in RootsMagic 8 databases
  # RM7 path will never be changed

  # Only want to call GetMediaDirectory once, so save its value as global
  global G_MediaDirectory

  if path[0] == "~" :
     absolutePath = os.path.expanduser(path)
  elif path[0] == "?":
    if G_MediaDirectory == "":
      G_MediaDirectory = GetMediaDirectory()
    absolutePath = G_MediaDirectory + os.fspath(path)[1:]
    # this alternative is not working...   absolutePath = os.path.join(G_MediaDirectory, path[1:])
  else:
    absolutePath = path

  return absolutePath


# ================================================================
def GetMediaDirectory():

  RM_Config_FilePath = r"~\AppData\Roaming\RootsMagic\Version 8\RootsMagicUser.xml"
  # RM_Config_FilePath = r"~\Development\Genealogy\Genealogy-scripts\RM -Test external files\test-RootsMagicUser.xml"

#  if file not found, RM8 not installed, will never be used
  myPath=Path(os.path.expanduser(RM_Config_FilePath))
  if not myPath.exists():
    path = "RM8 not installed"
  else:
    root = ET.parse(myPath)
    MediaFolderPathEle = root.find( "./Folders/Media")
    path = MediaFolderPathEle.text
  return path


# ================================================================
def checkFilePaths( conn, reportF ):
  cur= GetDBFileList(conn)

  reportF.write ("Start of \"Files Not Found\" listing\n\n")
  foundSomeMissingFiles=False
  for row in cur:
    dirPath=Path(ExpandDirPath(row[0]))
    filePath=Path(os.path.join(dirPath, row[1]))
    if not dirPath.exists(): 
       foundSomeMissingFiles=True
       reportF.write ("Directory path not found:" + "\"" + str(dirPath) + "\"" + "\n")
    else:
        if filePath.exists():
            if not filePath.is_file():
                foundSomeMissingFiles=True
                reportF.write ("File path is not a file: " + "\"" + str(filePath) + "\"" + "\n")
        else:
            foundSomeMissingFiles=True
            reportF.write ("File path not found: " + "\"" + str(filePath) + "\"" + "\n")

  if foundSomeMissingFiles == False:
     reportF.write ("    No files were found missing.\n\n")
  reportF.write ("\nEnd of \"Files Not Found\" listing\n\n")
  return


# ================================================================
def FolderContentsMinusIgnored(dirPath, config):

  ignoredFolderNames = config.get('Ignored Objects', 'folders').split('\n')
  ignoredFileNames   = config.get('Ignored Objects', 'filenames').split('\n')

  mediaFileList = []
  for (dirname, dirnames, filenames) in os.walk(dirPath, topdown=True):

    for fldrName in ignoredFolderNames:
      if fldrName in dirnames:
       dirnames.remove(fldrName)

    for igFileName in ignoredFileNames:
      if igFileName in filenames:
        filenames.remove(igFileName)

    for filename in filenames:
        mediaFileList.append(str(os.path.join(dirname, filename)))

  return mediaFileList


# ================================================================
def NonReferencedFiles(config, conn, reportF):

  dbFileList=[]
  cur= GetDBFileList(conn)
  for row in cur:
    dirPath=ExpandDirPath(row[0])
    filePath=os.path.join(dirPath, row[1])
    dbFileList.append(filePath)

  ExtFilesFolderPath = Path(config['File Paths']['SEARCH_ROOT_FLDR_PATH'])
  if not ExtFilesFolderPath.exists(): 
    reportF.write ("Directory path not found:" + "\"" + str(ExtFilesFolderPath) + "\"" + "\n")
    sys.exit()
  if not ExtFilesFolderPath.is_dir():
    reportF.write ("Path is not a directory:" + "\"" + str(ExtFilesFolderPath) + "\"" + "\n")
    sys.exit()
  mediaFileList = FolderContentsMinusIgnored(ExtFilesFolderPath, config)

  unRefFiles = list(set(mediaFileList).difference(dbFileList))
  unRefFiles.sort()

  reportF.write("\n\n\n")
  reportF.write("Start \"Unreferenced Files\" listing\n\n")
  reportF.write("Folder to search: " + str(ExtFilesFolderPath) + "\n")
  reportF.write("Media folder contains " + str(len(mediaFileList)) + " files (not counting ignored items)\n")
  reportF.write("Database contains " + str(len(dbFileList)) + " file links\n")
  reportF.write( str(len(unRefFiles)) + " files in media root folder are not referenced by the database\n\n\n")

  # don't print full path from root folder
  cutoff = len(str(ExtFilesFolderPath))

  for i in range(len(unRefFiles)):
    reportF.write("." + str(unRefFiles[i])[cutoff:] + "\n")

  reportF.write("\nEnd \"Unreferenced Files\" listing\n")

  return


# ================================================================
def CheckForTrue( inputString):
     return inputString.lower()  in ['on', 'true', '1', 't', 'y', 'yes']


# ================================================================
def TS():
     # return a TimeStamp string
     now = datetime.now()
     dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
     return dt_string


# ================================================================
def main():
    # Configuration
    IniFile="RM-Python-config.ini"
    
    # ini file must be in "current directory" and encoded as UTF-8 if non-ASCII chars present (no BOM)
    if not os.path.exists(IniFile):
        print("The ini configuration file, " + IniFile + " must be in the current directory." )
        return

    config = configparser.ConfigParser()
    config.read('RM-Python-config.ini', 'UTF-8')

    # Read file paths from ini file
    report_Path   = config['File Paths']['REPORT_PATH']
    database_Path = config['File Paths']['DB_PATH']
    RMNOCASE_Path = config['File Paths']['RMNOCASE_PATH']

    if not os.path.exists(database_Path):
        print('Database path not found')
        return
    FileModificationTime = time.ctime( os.path.getmtime(database_Path))


    # Read processing options from ini file

    ListFilesNotFound        = config['Options']['CHECK_FILES']
    ListAllReferencedFolders = config['Options']['FOLDER_LIST']
    ListUnReferencedFiles    = config['Options']['UNREF_FILES']

   # Process the database

    with create_connection(database_Path) as conn:
      conn.enable_load_extension(True)
      conn.load_extension(RMNOCASE_Path)

      with open( report_Path,  mode='w', encoding='utf-8-sig') as reportF:
        reportF.write ("Report generated at = " + TS() + "\n")  
        reportF.write ("Database processed  = " + database_Path + "\n")
        reportF.write ("Database last changed on = " + FileModificationTime + "\n\n\n")

        if CheckForTrue(ListFilesNotFound):
           checkFilePaths(conn, reportF)

        if CheckForTrue(ListUnReferencedFiles):
           reportF.write ("\n\n\n")
           NonReferencedFiles(config, conn, reportF)

        if CheckForTrue(ListAllReferencedFolders):
           reportF.write ("\n\n\n")
           ListFolders(conn, reportF)

        reportF.write ("\n\n")
        reportF.write ("End of report \n")


# Call the "main" function
if __name__ == '__main__':
    main()