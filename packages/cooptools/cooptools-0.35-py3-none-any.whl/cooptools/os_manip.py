import os
import shutil
import logging
import json
from enum import Enum
from typing import List

LOCALAPP_ROOT = 'LOCALAPPDATA'


class FileType(Enum):
    JSON = ".json"
    TXT = ".txt"
    CSV = ".csv"
    INI = ".ini"


def check_and_make_new_proj_localapp(app_root, proj_name):
    """ Verifies that the app_root exists at LOCALAPPDATA and then verifies that a subfolder exists at that directory
    for the proj_name.
    :return the full directory path to the proj_name
    """
    root = check_and_make_localapp_application_path_dir(app_root)
    return check_and_make_proj_path_dir(root, proj_name)


def root_and_name(root, name):
    """ Combines the root with the provided name to create a new directory or filepath
    :return string of the new directory or filepath"""
    return f"{root}\\{name}"


def check_and_make_proj_path_dir(root, proj_name):
    """Verifies that the directory at the provided root and proj_name exist
    :return the directory path"""
    proj_dir = root_and_name(root, proj_name)
    check_and_make_dirs(proj_dir)

    return proj_dir


def localapp_root(app_name):
    """ Returns the string of the directory that would be in the LOCALAPPDATA for the given app name"""
    local_app_data = os.getenv(LOCALAPP_ROOT)
    return f"{local_app_data}\\{app_name}"


def localapp_root_exists(app_name):
    """ Checks if the directory exists for the app_name in the LOCALAPPDATA"""
    dir = localapp_root(app_name)
    return os.path.isdir(dir)


def proj_dir(app_name, proj_name):
    """ Returns the string for a subfolder in the app root within LOCALAPPDATA"""
    app_root = localapp_root(app_name)
    return root_and_name(app_root, proj_name)


def proj_exists(app_name, proj_name):
    """ Checks if the directory exists for a subfolder within the app_name folder in LOCALAPPDATA"""
    return os.path.isdir(proj_dir(app_name, proj_name))


def check_and_make_dirs(dir):
    """ Checks if a directory exists, if not creates it
    :return the path to the directory
    """
    chk = os.path.isdir(dir)
    if not chk:
        os.makedirs(dir)
    return dir


def check_and_make_localapp_application_path_dir(application_root):
    """ Verifies the application_root folder exists in the LOCALAPPDATA
    :return path to the verified root
    """
    la_root = localapp_root(application_root)
    check_and_make_dirs(la_root)
    return la_root


def clean_file_type(file_path, file_type: FileType = None):
    if file_type is not None:
        split_string = file_path.split('.', 1)
        file_path = split_string[0] + str(file_type.value)

    return file_path

def create_file(file_path, file_type: FileType = None, lines: List = None):
    if file_type is not None:
        file_path = clean_file_type(file_path, file_type)

    with open(file_path, 'w') as outfile:
        try:
            if lines:
                outfile.writelines(lines)
        except Exception as e:
            logging.error(f"Unable to write file: {file_path}: {e}")

def filepath_at_check_and_make_dir(dir, file_name, file_type: FileType = None):
    check_and_make_dirs(dir)
    file_path = f"{dir}\\{file_name}"
    return clean_file_type(file_path, file_type)


def filepath_at_dir(app_root,
                    file_name,
                    proj_name=None,
                    file_type: FileType = None,
                    make_dirs: bool = True,
                    make_file: bool = True):

    # get the local app root with app root
    path = localapp_root(app_root)

    # append proj name dir if provided
    if proj_name is not None:
        path = root_and_name(path, proj_name)

    # make proj dir
    if make_dirs:
        check_and_make_dirs(path)

    # clean the filename
    clean_filename = clean_file_type(file_name, file_type)

    # get full path
    path = root_and_name(path, clean_filename)

    # make file
    if make_file:
        create_file(path, file_type=file_type)

    return path

def filepath_at_check_and_make_app_dir(app_root, file_name, file_type: FileType = None):
    app_path = localapp_root(app_root)
    return filepath_at_check_and_make_dir(app_path, file_name, file_type)


def filepath_at_check_and_make_app_proj_dir(app_root, proj_name, file_name, file_type: FileType = None):
    proj_path = check_and_make_new_proj_localapp(app_root, proj_name)
    return filepath_at_check_and_make_dir(proj_path, file_name, file_type)


def copy_file_from_to(filepath_to_copy: str, to_filepath: str):
    shutil.copy2(filepath_to_copy, to_filepath)


def try_save_json_data(my_jsonable_data, file_path, cls: json.JSONEncoder = None):
    with open(file_path, 'w') as outfile:
        try:
            accepted_method_names = ['toJson', 'to_json', 'tojson']
            to_json_method = next(iter(getattr(my_jsonable_data, x, None) for x in accepted_method_names), None)
            if to_json_method and callable(to_json_method):
                ret = outfile.write(json.dumps(to_json_method(), indent=4, cls=cls))
            else:
                ret = outfile.write(json.dumps(my_jsonable_data, indent=4, cls=cls))

            return ret
        except Exception as e:
            logging.error(f"Unable to write file: {file_path}: {e}")


def try_load_json_data(file_path, cls: json.JSONEncoder = None):
    ret = None

    if not os.path.isfile(file_path):
        return None

    with open(file_path, 'r+') as outfile:
        try:
            ret = json.load(outfile, cls=cls)
        except Exception as e:
            logging.error(f"Unable to read file: {file_path}: {e}")
    return ret


def save_application_json(my_jsonable_data, app_root, filename: str):
    file_path = filepath_at_check_and_make_app_dir(app_root, filename, file_type=FileType.JSON)
    return try_save_json_data(my_jsonable_data, file_path)


def save_project_json(my_jsonable_data, app_root, project_name, filename: str):
    file_path = filepath_at_check_and_make_app_proj_dir(app_root, project_name, filename, file_type=FileType.JSON)
    return try_save_json_data(my_jsonable_data, file_path)


def load_application_json(app_root, filename):
    file_path = filepath_at_check_and_make_app_dir(app_root, filename, file_type=FileType.JSON)
    return try_load_json_data(file_path)


def load_project_json(app_root, project, filename):
    proj_dir = check_and_make_new_proj_localapp(app_root, project)
    file_path = f"{proj_dir}\\{filename}.json"
    return try_load_json_data(file_path)