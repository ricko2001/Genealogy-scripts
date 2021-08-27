import sqlite3
import os
from pathlib  import Path
from datetime import datetime
import configparser


## Tested with RootsMagic v7.6.5  (not tested with RM 8)
##             Python for Windows v3.9.0 64bit  
##             unifuzz64.dll (ver not set, MD5=06a1f485b0fae62caa80850a8c7fd7c2)
##      
##  Python download-
##  https://www.python.org/downloads/windows/    
##  find the link near bottom of page for "Windows installer (64-bit)"
##
##  unifuzz64.dll download-
##  https://sqlitetoolsforrootsmagic.com/wp-content/uploads/2018/05/unifuzz64.dll
##  above link found in this context-
##  https://sqlitetoolsforrootsmagic.com/rmnocase-faking-it-in-sqlite-expert-command-line-shell-et-al/


## Configuration ini file:    RM-Python-config.ini
## exmaple ini file:

#[File Paths]
#DB_PATH        = C:\Users\me\Documents\Genealogy\GeneDB\MyRM-File.rmgc
#REPORT_PATH    = C:\Users\me\Documents\Genealogy\GeneDB\ExternalFilesReport.txt
#RMNOCASE_PATH   = C:\Users\me\Documents\Genealogy\GeneDB\SW\unifuzz64.dll
#SEARCH_ROOT_FLDR_PATH = C:\Users\me\Documents\Genealogy\GeneDB\Exhibits
#
#[Options]
#CHECK_FILES     = on
#FOLDER_LIST     = off
#UNREF_FILES     = on
#
#[Ignored Objects]
#
#folders = 
#  Audio
#  Waldzeller Häuserbuch -Oehring
#
#
#filenames = 
#  Archive- Bamberg.txt
#  Archive- Würzburg.txt
#
#[END]
#


# TODO
# better error handling opening database
# check database schema version
# list references to any file not found


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
    reportF.write ("Folder List:\n\n")
    for row in rows:
        reportF.write(row[0] + "\n")
    reportF.write (str(len(rows)) + "  rows returned \n\n")

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
def checkFilePaths( conn, reportF ):
  cur= GetDBFileList(conn)

  reportF.write ("File not found warnings:\n\n")

  for row in cur:
    dirPath=Path(row[0])
    filePath=Path(row[0] + row[1])
    if not dirPath.exists(): 
       reportF.write ("Directory path not found:" + "\"" + str(dirPath) + "\"" + "\n")
    else:
        
        if filePath.exists():
            if not filePath.is_file():
                reportF.write ("File path is not a file:" + "\"" + str(filePath) + "\"" + "\n")
        else:
            reportF.write ("File path not found:" + "\"" + str(filePath) + "\"" + "\n")
  return


# ================================================================
def FolderContents(dirPath, config):

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
    dirPath=Path(row[0])
    filePath=Path(row[0] + row[1])
    dbFileList.append(str(filePath))

  MediaFolderPath = Path(config['File Paths']['SEARCH_ROOT_FLDR_PATH'])
  if not MediaFolderPath.exists(): 
    reportF.write ("Directory path not found:" + "\"" + str(MediaFolderPath) + "\"" + "\n")
    sys.exit()
  if not MediaFolderPath.is_dir():
    reportF.write ("Path is not a directory:" + "\"" + str(MediaFolderPath) + "\"" + "\n")
    sys.exit()
  mediaFileList = FolderContents(MediaFolderPath, config)

  unRefFiles = list(set(mediaFileList).difference(dbFileList))
  unRefFiles.sort()

  reportF.write("\n\n\n")
  reportF.write("Unreferenced Files Report\n")
  reportF.write("Files in media root folder " + str(MediaFolderPath) + " not referenced in RootsMagic database." + "\n")
  reportF.write("Found " + str(len(mediaFileList)) + " files in the folder, and " + str(len(dbFileList)) + " files in the database." + "\n")
  reportF.write( str(len(unRefFiles)) + " files in media root folder that are not referenced by the database."   "\n")
  reportF.write( "\n\n")

  # don't print full path from root folder
  cutoff = len(str(MediaFolderPath))

  for i in range(len(unRefFiles)):
    reportF.write("." + str(unRefFiles[i])[cutoff:] + "\n")

  return

# ================================================================
def CheckForTrue( inputString):
     return inputString.lower()  in ['on', 'true', '1', 't', 'y', 'yes']

# ================================================================
def TS():
     # datetime object containing current date and time
     now = datetime.now()
     dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
     return dt_string
     
# ================================================================
def main():
    # Configuration
    IniFile="RM-Python-config.ini"
    
    # ini file must be in "current directory" and encoded as UTF-8 if non ASCII chars present (no BOM)
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

    # Read processing options from ini file

    ListFilesNotFound        = config['Options']['CHECK_FILES']
    ListAllReferencedFolders = config['Options']['FOLDER_LIST']
    ListUnReferenced         = config['Options']['UNREF_FILES']

   # Process the database
   
    with create_connection(database_Path) as conn:
      conn.enable_load_extension(True)
      conn.load_extension(RMNOCASE_Path)
    
#      with open( report_Path, "w") as reportF:
      with open( report_Path,  mode='w', encoding='utf-8-sig') as reportF:
#        reportF.write(str(codecs.BOM_UTF8))
        reportF.write ("report generated at = " + TS() + "\n")	
        reportF.write ("Database processed  = " + database_Path + "\n\n\n")


        if CheckForTrue(ListFilesNotFound):
           checkFilePaths(conn, reportF)
        
        if CheckForTrue(ListAllReferencedFolders):
           reportF.write ("\n\n\n")
           ListFolders(conn, reportF)
        
        if CheckForTrue(ListUnReferenced):
           reportF.write ("\n\n\n")
           NonReferencedFiles(config, conn, reportF)
        
        reportF.write ("\n\n\n")
        reportF.write ("End of report \n")
  
       

if __name__ == '__main__':
    main()