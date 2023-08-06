# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
'''
    A module of utility methods used for searching files.

    ----------

    Meta
    ----------
    `author`: Colemen Atwood
    `created`: 06-04-2022 10:58:25
    `memberOf`: file_utils
'''

# import json
# import shutil
import os as _os
import re as _re


import utils.dict_utils as _obj
import utils.string_utils as _csu






def by_name(file_name, search_path=None, **kwargs):
    '''
        Searches the path provided for files that match the file_name

        ----------
        Arguments
        -----------------
        `file_name` {str|list}
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
                If False it will match with any file that contains the file_name argument
            `regex`=False {bool}
                If True the file_name arg is treated as a regex string for comparisons.

        Return
        ----------
        `return` {None|list}
            A list of matching files or None if no matching files are found.
    '''
    if isinstance(file_name, list) is False:
        file_name = [file_name]
    if search_path is None:
        search_path = _os.getcwd()

    extensions = _csu.extension(_obj.get_kwarg(['extensions', 'ext'], [], (list, str), **kwargs))
    if isinstance(extensions, str):
        extensions = [extensions]

    recursive = _obj.get_kwarg(['recursive', 'recurse'], True, bool, **kwargs)
    case_sensitive = _obj.get_kwarg(['case_sensitive'], True, (bool), **kwargs)
    exact_match = _obj.get_kwarg(['exact_match'], True, (bool), **kwargs)
    regex = _obj.get_kwarg(['regex', 'use regex'], False, (bool), **kwargs)

    if case_sensitive is False and regex is False:
        new_name_array = []
        for name in file_name:
            if isinstance(name, str):
                new_name_array.append(name.lower())
        file_name = new_name_array

    result_array = []
    # pylint: disable=unused-variable
    # pylint: disable=too-many-nested-blocks
    for root, folders, files in _os.walk(search_path):
        for file in files:
            skip = False
            current_file_path = _os.path.join(root, file)
            test_file_name = file

            test_file_ext = _csu.extension(_os.path.splitext(_os.path.basename(current_file_path))[1])
            if case_sensitive is False:
                test_file_name = test_file_name.lower()

            if len(extensions) > 0:
                if test_file_ext not in extensions:
                    skip = True

            if skip is False:
                for name in file_name:
                    if len(name) == 0 or "*" == name:
                        result_array.append(current_file_path)
                        break

                    if regex is not False:
                        match = _re.search(name, test_file_name)
                        if match is not None:
                            result_array.append(current_file_path)

                    if exact_match is True:
                        if test_file_name == name:
                            result_array.append(current_file_path)
                    else:
                        if name in test_file_name:
                            result_array.append(current_file_path)
        if recursive is False:
            break

    if len(result_array) > 0:
        return result_array
    return None
