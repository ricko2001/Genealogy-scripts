import os
from pathlib import Path
import yaml
from datetime import datetime
from pathlib import Path
import zipfile
import shutil
import re

# As a first step, this build script builds from local source
# it does not get "fresh file" from GitHub

# this file lives in the repo root/dev util scripts dir
# the top level yaml config file is also here.

def main():
    try:
        repo_root = Path(r"C:\Users\rotter\Development\Genealogy\repo Genealogy-scripts")

        top_level_config_path = repo_root / "dev util scripts/_top_level_build_config.yaml"
        # top_level_config_name = "_top_level_build_config.yaml"
        if (not Path(top_level_config_path).exists() ):
            print("Can't find the top level config file.\n")

        with open(top_level_config_path, 'r') as top_lev:
            doc = yaml.safe_load(top_lev)
            suite_version = doc["SuiteVersion"]
            suite_name = doc["SuiteName"]
            project_root_dir_path = doc["ProjectRootDirPath"]
            project_list = doc["ProjectList"]
    except:
        print("Problem getting the values from the top level yaml file.\n")
        exit()

    time_stamp = time_stamp_now("file")
    
    distribution_dir_name = suite_name + "_v" + suite_version
    release_dir_name= "Release " + distribution_dir_name  + " " + time_stamp
    release_dir_path = Path(project_root_dir_path) / release_dir_name
    distribution_dir_path = release_dir_path / distribution_dir_name

    if release_dir_path.exists():
        raise Exception("Release dir already exists")
    Path.mkdir(release_dir_path)
    Path.mkdir(distribution_dir_path)

    # Process each project
    for project in project_list:
        project_dir_path = distribution_dir_path / project
        Path.mkdir(project_dir_path)
        try:
            utility_level_config_path = repo_root / "RM" / project / "_util_info.yaml"
            # utility_level_config_path = Path("RM") / project / "_util_info.yaml"
            with open(utility_level_config_path, 'r') as proj_lev:
                doc = yaml.safe_load(proj_lev)
                utility_version = doc["Version"]
                util_name = doc["UtilityName"]
                distribution_file_list = doc["DistributionFileList"]
                distribution_folder_list = doc["DistributionFolderList"]
        except:
            print("Problem getting the values from the util level yaml file.\n")
            pause_with_message("Press Enter to continue, window will close")
            exit()

        version_long = utility_version + "   " + time_stamp

        #  copy the files and folders that will be distributed in the zip

        # copy files to the distribution folder
        src_project_dir = Path(repo_root) / "RM"  / project 
        for file in distribution_file_list:
            shutil.copy(src_project_dir / file, distribution_dir_path / project)

        # copy folder to the distribution folder
        for folder in distribution_folder_list:
            dest_dir_name = distribution_dir_path / project / os.path.basename(folder)
            shutil.copytree(src_project_dir /folder, dest_dir_name)
            delete_pycache_folders(dest_dir_name)


        py_file_to_edit = distribution_dir_path / project / (util_name + ".py")
        with open(py_file_to_edit, "r") as sources:
            lines = sources.readlines()
        with open(py_file_to_edit, "w") as sources:
            for line in lines:
                sources.write(re.sub(r'UTILITY_VERSION_NUMBER_RM_UTILS_OVERRIDE', version_long, line))

    make_zipfile(
        release_dir_path / (str(distribution_dir_name) + ".zip"), 
        distribution_dir_path )
    
    # DONE

    # now, print out some instructions for archiving the build and 
    # releasing on GitHub

    git_tag = suite_name + "_v" + suite_version
    release_name = suite_name + " v" + suite_version

    print("\nMove the Release folder into the Release storage folder\n")

    print("\n\nRelease tag and name for Release on GitHub\n\n")
    print(f"tag git:\ngit tag --annotate {git_tag}")
    print("Write text in default text editor, save and close. Perhaps mini release notes")
    print(f"\nPush tag to github:\ngit push origin {git_tag}")
    print(f"\nDraft a release, titled:\n{release_name}")
    print('''\n\n
============================================
END OF SCRIPT
============================================
''')

    pause_with_message("Press Enter to continue, window will close")
    return 0

# ===================================================DIV60==
def delete_pycache_folders(root_folder):
    for dirpath, dirnames, filenames in os.walk(root_folder):
        if '__pycache__' in dirnames:
            pycache_path = os.path.join(dirpath, '__pycache__')
            shutil.rmtree(pycache_path)


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
