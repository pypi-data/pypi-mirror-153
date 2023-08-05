import json
# import shutil
import os
import re
# from pathlib import Path
import utils.objectUtils as ou
# import utils.dir_read as read
import utils.string_utils as csu

# todo - DOCUMENTATION FOR METHODS


def by_name(dir_name, search_path=None, **kwargs):
    '''
        Searches the path provided for directories that match the dir_name

        ----------
        Arguments
        -----------------
        `dir_name` {str|list}
            The string or list of strings to search for.
        `search_path`=cwd {str}
            The directory to search within.

        Keyword Arguments
        -----------------
            `recursive`=True {boolean}
                If True the path is searched recursively

            `case_sensitive`=True {bool}
                If False case is ignored.
            `exact_match`=True {bool}
                If False it will match with any dir that contains the dir_name argument
            `regex`=False {bool}
                If True the dir_name arg is treated as a regex string for comparisons.

        Return
        ----------
        `return` {None|list}
            A list of matching folders or None if no matching folders are found.
    '''
    if isinstance(dir_name, list) is False:
        dir_name = [dir_name]
    if search_path is None:
        search_path = os.getcwd()


    recursive = ou.get_kwarg(['recursive', 'recurse'], True, bool, **kwargs)
    case_sensitive = ou.get_kwarg(['case_sensitive'], True, (bool), **kwargs)
    exact_match = ou.get_kwarg(['exact_match'], True, (bool), **kwargs)
    regex = ou.get_kwarg(['regex', 'use regex'], False, (bool), **kwargs)

    if case_sensitive is False and regex is False:
        new_name_array = []
        for name in dir_name:
            if isinstance(name, str):
                new_name_array.append(name.lower())
        dir_name = new_name_array

    result_array = []
    # pylint: disable=unused-variable
    # pylint: disable=too-many-nested-blocks
    for root, folders, files in os.walk(search_path):
        for dname in folders:
            current_dir_path = os.path.join(root, dname)
            test_dir_name = dname
            # print(f"test_dir_name: {test_dir_name}")
            # print(f"current_dir_path: {current_dir_path}")

            if case_sensitive is False:
                test_dir_name = test_dir_name.lower()

            for name in dir_name:
                if len(name) == 0 or name == "*":
                    result_array.append(current_dir_path)
                    break

                if regex is not False:
                    match = re.search(name, test_dir_name)
                    if match is not None:
                        result_array.append(current_dir_path)

                if exact_match is True:
                    if test_dir_name == name:
                        result_array.append(current_dir_path)
                else:
                    if name in test_dir_name:
                        result_array.append(current_dir_path)
        if recursive is False:
            break

    if len(result_array) > 0:
        return result_array
    return None



