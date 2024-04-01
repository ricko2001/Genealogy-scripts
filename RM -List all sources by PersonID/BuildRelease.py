import os
import sys
import time
import yaml 
from datetime import datetime
from pathlib import Path
import subprocess
import zipfile
import shutil

def main():
    print('''
Update all files in local git - make sure main branch is correct.
Test script.py, readme.txt, _util_info.yaml
push code to github main
This script is to be run from the "RM -<fldr name>" folder, where the py file is.
It will create a subfolder -  Release "<util_name> v<short_ver_num>  <time>"
where all building is done.
That subfolder should be moved to the upper level Releases folder when done.
''')
     
    try:        
        with open('_util_info.yaml', 'r') as f:
            doc = yaml.safe_load(f)
            version_number_full = doc["Version"]
            util_name = doc["InternalName"]
            util_file_name = doc["OriginalFilename"]
            distribution_file_list = doc["DistributionFileList"]


        version_number_short = version_number_full[0:-2]
        distribution_dir_name=util_name + ' v' + version_number_short
        release_dir_name=("Release " + util_name + ' v' 
                        + version_number_short + "  " + TimeStampNow('file'))

        if os.path.exists( release_dir_name):
            raise Exception("Folder already exists")

        os.mkdir(release_dir_name)

        # create empty build log file to be filled in by user
        Path( os.path.join(release_dir_name, "Build_Log.txt")).touch()

        os.mkdir(os.path.join(release_dir_name, distribution_dir_name))
        # These are files that will be distributed in the zip

        distribution_dir_path=os.path.join( ".", release_dir_name, distribution_dir_name)

        # copy the files to the distribution folder to prepare for pyinstaller run
        for file in distribution_file_list:
            shutil.copy(file, distribution_dir_path )
        # can't get this easily from the yaml list
        shutil.copy(util_name + ".py",     distribution_dir_path )
        shutil.copy("_util_info.yaml",     distribution_dir_path )

        os.chdir(distribution_dir_path)

        # create the Version.py file for pyinstaller from _util_info.yaml
        subprocess.run("create-version-file _util_info.yaml --outfile Version_rc.txt")

        # create the exe file
        subprocess.run("pyinstaller --onefile --version-file Version_rc.txt  " + util_name + ".py")

        os.remove("_util_info.yaml")
        os.remove("Version_rc.txt")
        shutil.move(util_name + ".spec",  os.path.join("build", util_name + ".spec"))

        shutil.copy(os.path.join( "dist", util_file_name), util_file_name)
        shutil.move( "build", "..")
        shutil.move( "dist", "..")
        os.chdir("..")

        make_zipfile(distribution_dir_name + ".zip", distribution_dir_name)

        PauseWithMessage(" hit Enter to continue")

        print(

'''
RELEASE PROCEDURE for GitHub
use git tag name = %APPNAME%_v%VERSION_NUMBER%
see -  https://git-scm.com/docs/git-tag
Tag the local repo with an annotated tag  - no spaces allowed in tag name
git tag --annotate %APPNAME%_v%VERSION_NUMBER%
write text in default text editor, save and close. Perhaps mini release notes?
push the local tag to github main
git push origin %APPNAME%_v%VERSION_NUMBER%
tags can be deleted and or renamed-  see   https://phoenixnap.com/kb/git-rename-tag
Draft a release
Check previous title for pattern (use spaces in title, not in tag)
use release title  = %APPNAME% v%VERSION_NUMBER%
Add release info, refer to previous descriptions for what to write.
Add the zip file
Save as draft and let it sit and age for a while
Publish the release
Write an announcement post to groups.
in Terminal use - Shift-Control-A,  Shift-Control-C  
and paste into a new Build_output.txt file, and put it into Release folder/
============================================
END OF SCRIPT
============================================
''')
        PauseWithMessage(" hit Enter to continue, window will close")

    except Exception as e:
        print(str(e))
        PauseWithMessage("\n\n hit Enter to continue, window will close")
        return 1
    return 0

# ===================================================DIV60==
def make_zipfile(output_filename, source_dir):

    # https://stackoverflow.com/questions/1855095/how-to-create-a-zip-archive-of-a-directory
    relroot = os.path.abspath(os.path.join(source_dir, os.pardir))
    with zipfile.ZipFile(output_filename, "w", zipfile.ZIP_DEFLATED) as zip:
        for root, dirs, files in os.walk(source_dir):
            # add directory (needed for empty dirs)
            zip.write(root, os.path.relpath(root, relroot))
            for file in files:
                filename = os.path.join(root, file)
                if os.path.isfile(filename): # regular files only
                    arcname = os.path.join(os.path.relpath(root, relroot), file)
                    zip.write(filename, arcname)


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
def PauseWithMessage(message = None):
  if (message != None):
    input(str(message))
  else:
    input("\nPress the <Enter> key to exit...")
  return


# ===================================================DIV60==
# Call the "main" function
if __name__ == '__main__':
    main()

# ===================================================DIV60==












