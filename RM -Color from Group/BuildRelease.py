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
    try:
        with open('_util_info.yaml', 'r') as f:
            doc = yaml.safe_load(f)
            version_number_full = doc["Version"]
            util_name = doc["InternalName"]
            util_file_name = doc["OriginalFilename"]
            try:
                distribution_file_list = doc["DistributionFileList"]
            except:
                distribution_file_list = []
            try:
                distribution_folder_list = doc["DistributionFolderList"]
            except:
                distribution_folder_list = []
            try:
                PyInstaller_extra_params = doc["PyInstaller_extra_params"]
            except:
                PyInstaller_extra_params = []

        version_number_short = version_number_full[0:-2]
        distribution_dir_name = util_name + ' v' + version_number_short
        release_dir_name = ("Release " + util_name + ' v'
                            + version_number_short + "  " + time_stamp_now('file'))

        if os.path.exists(release_dir_name):
            raise Exception("Folder already exists")

        os.mkdir(release_dir_name)

        # create empty build log file to be filled in by user  TODO
        Path(os.path.join(release_dir_name, "Build_Log.txt")).touch()

        os.mkdir(os.path.join(release_dir_name, distribution_dir_name))
        # These are files that will be distributed in the zip

        distribution_dir_path = os.path.join(
            ".", release_dir_name, distribution_dir_name)

        # copy files to distribution folder
        # can't get these easily from the yaml list
        shutil.copy(util_name + ".py",     distribution_dir_path)
        shutil.copy("_util_info.yaml",     distribution_dir_path)

        # copy more files to the distribution folder
        for file in distribution_file_list:
            shutil.copy(file, distribution_dir_path)

        # copy the folders to the distribution folder
        for folder in distribution_folder_list:
            shutil.copytree(folder, os.path.join(distribution_dir_path, os.path.basename(folder) ))

        os.chdir(distribution_dir_path)
        # create the Version_rc.txt file for pyinstaller from _util_info.yaml
        subprocess.run(
            "create-version-file _util_info.yaml --outfile Version_rc.txt")

        # set up PyInstaller command line
        normal_params= " --onefile"
        normal_params += " --version-file Version_rc.txt"
        normal_params += (" " + util_name + ".py")

        extra_params = ''
        # get any extra params for PyInstaller
        for item in PyInstaller_extra_params:
            extra_params += (" " + item)

        print(f"{extra_params=}\n\n{normal_params=}\n\n")

        py_installer_cmd_line= "pyinstaller " + extra_params + normal_params

        # create the exe file
        subprocess.run(py_installer_cmd_line)

        os.remove("_util_info.yaml")
        os.remove("Version_rc.txt")
        shutil.move(util_name + ".spec",
                    os.path.join("build", util_name + ".spec"))

        shutil.copy(os.path.join("dist", util_file_name), util_file_name)
        shutil.move("build", "..")
        shutil.move("dist", "..")
        os.chdir("..")

        make_zipfile(distribution_dir_name + ".zip", distribution_dir_name)

        print("\n\nCopy window contents to build log in the Release folder."
              "In terminal: Ctl-Shift-A, Ctl-C\n")
        pause_with_message(" hit Enter to continue")

        git_tag = util_name + "_v" + version_number_short
        release_name = util_name + " v" + version_number_short

        print("\n\nRelease tag and name for Release on GitHub\n\n")
        print("tag git:\ngit tag --annotate " + util_name + "_v" + version_number_short)
        print("Write text in default text editor, save and close. Perhaps mini release notes")

        print("\nPush tag to github:\ngit push origin " + git_tag)
        print("\nDraft a release, title:\n" + release_name)
        print('''\n\n
============================================
END OF SCRIPT
============================================
''')
    except Exception as e:
        print(str(e))
        pause_with_message("\n\nPress Enter to continue, window will close")
        return 1
    pause_with_message("Press Enter to continue, window will close")
    return 0

# ===================================================DIV60==
def make_zipfile(output_filename, source_dir):

    # https://stackoverflow.com/questions/1855095/how-to-create-a-zip-archive-of-a-directory
    relative_root = os.path.abspath(os.path.join(source_dir, os.pardir))
    with zipfile.ZipFile(output_filename, "w", zipfile.ZIP_DEFLATED) as zip:
        for root, dirs, files in os.walk(source_dir):
            # add directory (needed for empty dirs)
            zip.write(root, os.path.relpath(root, relative_root))
            for file in files:
                filename = os.path.join(root, file)
                if os.path.isfile(filename):  # regular files only
                    archive_name = os.path.join(
                        os.path.relpath(root, relative_root), file)
                    zip.write(filename, archive_name)


# ===================================================DIV60==
def time_stamp_now(type=""):

    # return a TimeStamp string
    now = datetime.now()
    if type == '':
        dt_string = now.strftime("%Y-%m-%d %H:%M:%S")
    elif type == 'file':
        dt_string = now.strftime("%Y-%m-%d_%H%M%S")
    return dt_string


# ===================================================DIV60==
def pause_with_message(message=None):
    
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
