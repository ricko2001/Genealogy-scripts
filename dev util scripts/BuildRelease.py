import os
from pathlib import Path
import yaml
from datetime import datetime
from pathlib import Path
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


        version_number_short = version_number_full[0:-2]
        project_dir_path = Path.cwd()

        release_dir_name = ("Release " + util_name + ' v'
                            + version_number_short + "  " + time_stamp_now('file'))
        release_dir_path = project_dir_path / release_dir_name

        distribution_dir_name = util_name + ' v' + version_number_short
        distribution_dir_path = release_dir_path / distribution_dir_name
        
        if release_dir_path.exists():
            raise Exception("Folder already exists")

        Path.mkdir(release_dir_path)

#        # These are files that will be distributed in the zip
        Path.mkdir(distribution_dir_path)

        # copy files to the distribution folder
        for file in distribution_file_list:
            shutil.copy(file, distribution_dir_path)

        # copy folder to the distribution folder
        for folder in distribution_folder_list:
            shutil.copytree(folder, distribution_dir_path /os.path.basename(folder) )

        make_zipfile(
            release_dir_path / (str(distribution_dir_name) + ".zip"), 
            distribution_dir_path )


        # print out some instructions for archiving the build and 
        # 
        # 
        # releasing on GitHub

        print("\n\nCopy window contents to build log in the Release folder."
              "In terminal: Ctl-Shift-A, Ctl-C\n")


        git_tag = util_name + "_v" + version_number_short
        release_name = util_name + " v" + version_number_short

        print("\n\nRelease tag and name for Release on GitHub\n\n")
        print(f"tag git:\ngit tag --annotate {util_name}_v{version_number_short}")
        print("Write text in default text editor, save and close. Perhaps mini release notes")

        print(f"\nPush tag to github:\ngit push origin {git_tag}")
        print(f"\nDraft a release, title:\n{release_name}")
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
def make_zipfile(output_file_path: Path, source_dir: Path):

    # https://stackoverflow.com/questions/1855095/how-to-create-a-zip-archive-of-a-directory
    #relative_root = os.path.abspath(os.path.join(source_dir, os.pardir))
    relative_root = source_dir.parent

    with zipfile.ZipFile(output_file_path, "w", zipfile.ZIP_DEFLATED) as zip:
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
