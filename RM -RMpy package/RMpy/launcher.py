import os
import sys
import sqlite3
from pathlib import Path
from datetime import datetime
import configparser
import subprocess
import traceback

sys.path.append( r'.' )
import RMpy.common as RMc  # type: ignore

# ===================================================DIV60==
def launcher(script_path,
            config_file_name,
            run_features_function,
            allow_db_changes = False,
            RMNOCASE_required = False,
            RegExp_required = False  ):
    

    db_connection = None
    report_display_app = None

    # ===========================================DIV50==
    # Errors go to console window
    # ===========================================DIV50==
    try:
        # config file must be in "current directory" and encoded as UTF-8 (no BOM).
        # see   https://docs.python.org/3/library/configparser.html
        config_file_path = os.path.join(RMc.get_current_directory(script_path), config_file_name)
        # Check that config file is at expected path and that it is readable & valid.
        if not os.path.exists(config_file_path):
            raise RMc.RM_Py_Exception(
                "ERROR: The configuration file, " + config_file_name
                + " must be in the same directory as the .py or .exe file." "\n\n")

        config = configparser.ConfigParser(empty_lines_in_values=False,
                                           interpolation=None)
        try:
            config.read(config_file_path, 'UTF-8')
        except:
            raise RMc.RM_Py_Exception(
                "ERROR: The " + config_file_name
                + " file contains a format error and cannot be parsed." "\n\n")
        try:
            report_path = config['FILE_PATHS']['REPORT_FILE_PATH']
        except:
            raise RMc.RM_Py_Exception(
                'ERROR: REPORT_FILE_PATH must be defined in the '
                + config_file_name + "\n\n")
        try:
            # Use UTF-8 encoding for the report file. Test for write-ability
            open(report_path,  mode='w', encoding='utf-8')
        except:
            raise RMc.RM_Py_Exception('ERROR: Cannot create the report file '
                                  + report_path + "\n\n")

    except RMc.RM_Py_Exception as e:
        RMc.pause_with_message(e)
        return 1
    except Exception as e:
        traceback.print_exception(e, file=sys.stdout)
        RMc.pause_with_message(
            "ERROR: Application failed. Please email error report:" "\n\n " +
            str(e)
            + "\n\n" "to the author")
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
            raise RMc.RM_Py_Exception(
                'ERROR: Path for report file display app not found: '
                + report_display_app)

        try:
            database_path = config['FILE_PATHS']['DB_PATH']
        except:
            raise RMc.RM_Py_Exception('ERROR: DB_PATH must be specified.')
        if not os.path.exists(database_path):
            raise RMc.RM_Py_Exception(
                'ERROR: Database path not found: ' + database_path
                + '\n\n\n' 'Absolute path checked:\n"'
                + os.path.abspath(database_path) + '"')

        if RMNOCASE_required:
            try:
                rmnocase_path = config['FILE_PATHS']['RMNOCASE_PATH']
            except:
                raise RMc.RM_Py_Exception(
                    'ERROR: RMNOCASE_PATH must be specified.')
            if not os.path.exists(rmnocase_path):
                raise RMc.RM_Py_Exception(
                    'ERROR: Path for RMNOCASE extension (unifuzz64.dll) not found: '
                    + rmnocase_path
                    + '\n\n' 'Absolute path checked:\n"'
                    + os.path.abspath(rmnocase_path) + '"')
            
        if RegExp_required:
            try:
                regexp_path = config['FILE_PATHS']['REGEXP_PATH']
            except:
                raise RMc.RM_Py_Exception(
                    'ERROR: REGEXP_PATH must be specified.')
            if not os.path.exists(rmnocase_path):
                raise RMc.RM_Py_Exception(
                    'ERROR: Path for REGEXP extension not found: '
                    + rmnocase_path
                    + '\n\n' 'Absolute path checked:\n"'
                    + os.path.abspath(rmnocase_path) + '"')

        # RM database file info
        file_modification_time = datetime.fromtimestamp(
            os.path.getmtime(database_path))

        if RMNOCASE_required and not RegExp_required:
            db_connection = RMc.create_db_connection(database_path, [rmnocase_path])
        elif not RMNOCASE_required and RegExp_required:
            db_connection = RMc.create_db_connection(database_path, [regexp_path])
        elif RMNOCASE_required and RegExp_required:
            db_connection = RMc.create_db_connection(database_path, [rmnocase_path, regexp_path])
        else:
            db_connection = RMc.create_db_connection(database_path, None)

        # write header to report file
        report_file.write("Report generated at      = " + RMc.time_stamp_now()
                          + "\n" "Database processed       = "
                          + os.path.abspath(database_path)
                          + "\n" "Database last changed on = "
                          + file_modification_time.strftime("%Y-%m-%d %H:%M:%S")
                          + "\n" "Python version           = "
                          + sys.version
                          + "\n" "SQLite library version   = "
                          + RMc.get_SQLite_library_version(db_connection) + "\n\n\n\n")

        run_features_function(config, db_connection, report_file)

    except (sqlite3.OperationalError, sqlite3.ProgrammingError) as e:
        report_file.write(
            "ERROR: SQL execution returned an error \n\n" + str(e))
        return 1
    except RMc.RM_Py_Exception as e:
        report_file.write(str(e))
        return 1
    except Exception as e:
        traceback.print_exception(e, file=report_file)
        report_file.write(
            "\n\n" "ERROR: Application failed. Please email report file to author. ")
        return 1
    finally:
        if db_connection is not None:
            if allow_db_changes:
                db_connection.commit()
            db_connection.close()
        report_file.close()
        if report_display_app is not None:
            subprocess.Popen([report_display_app, report_path])
    return 0


# ===================================================DIV60==

