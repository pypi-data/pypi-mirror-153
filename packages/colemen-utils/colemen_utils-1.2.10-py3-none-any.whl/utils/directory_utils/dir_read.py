# pylint: disable=too-many-lines
# pylint: disable=too-many-locals
# pylint: disable=too-many-branches
# pylint: disable=bare-except
# pylint: disable=line-too-long
# pylint: disable=unused-import

'''
    A module of utility methods used for reading directories locally or over FTP.

    ----------

    Meta
    ----------
    `author`: Colemen Atwood
    `created`: 06-04-2022 10:44:23
    `memberOf`: directory_utils
'''

# import json
# from re import search
# import time
# import json
# from threading import Thread
import traceback as _traceback
import shutil as _shutil
import time as _time
import os as _os
from pathlib import Path
import logging as _logging

import ftputil as _ftputil
from ftputil.error import FTPOSError as _FTPOSError


import utils.file_utils as _f
import utils.dict_utils as _obj
import utils.string_utils as _csu
# import utils.directory_utils as _dir


logger = _logging.getLogger(__name__)


def get_files(search_path=False, **kwargs):
    return _f.get_files(search_path, **kwargs)


def exists(file_path, **kwargs):
    '''
        Confirms that the directory file_path exists

        ----------

        Arguments
        -------------------------
        `file_path` {str}
            The path to confirm.

        Keyword Arguments
        -----------------
        [`ftp`=None] {obj}
            A reference to the ftputil object.

        Return {bool}
        ----------------------
        True if the directory exists, false otherwise.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 12-19-2021 11:44:03
        `memberOf`: dir
        `version`: 1.0
        `method_name`: exists
    '''
    dir_exists = False
    ftp = _obj.get_kwarg(["ftp"], None, None, **kwargs)

    if ftp is not None:
        dir_exists = exists_ftp(file_path, ftp)
    else:
        if _os.path.isdir(file_path) is True:
            dir_exists = True

    return dir_exists


def exists_ftp(file_path, ftp):
    '''
        Checks if an FTP directory exists.

        ----------

        Arguments
        -------------------------
        `file_path` {str}
            The path to confirm.

        `ftp` {obj}
            A reference to the ftputil object.

        Return {bool}
        ----------------------
        True if the directory exists, false otherwise.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 12-19-2021 11:59:05
        `memberOf`: dir
        `version`: 1.0
        `method_name`: exists_ftp
    '''
    dir_exists = False
    try:
        if ftp.path.exists(file_path):
            dir_exists = True
    except _ftputil.error.PermanentError as error:
        print(f"error: {str(error)}")
    return dir_exists


def get_folders(search_path=False, **kwargs):
    '''
        Get all directories from the search_path.

        ----------

        Arguments
        -------------------------
        `search_path` {str|list}
            The search path or list of paths to iterate.\n
            This is the same as the keyword argument search_path,
            the kwarg is provided for consistency.

        Keyword Arguments
        -----------------
            [`search_path`=cwd] {str|list}
                The search path or list of paths to iterate.

            [`recursive`=True] {boolean}
                If True the path is iterated recursively

            [`exclude`=[]] {str|list}
                A string or list of strings, if the file path contains any of them,
                the directory is ignored.

            [`include`=[]] {str|list}
                A string or list of strings, if the file path does NOT contain any of them,
                the directory is ignored.

            [`paths_only`=False] {bool}
                If True, the returned value will be a list of directory paths.

            [`ftp`=None] {obj}
                A reference to the ftputil object.

        Return {list}
        ----------------------
        A list of dictionaries containing all matching directories.\n
        example:\n
            [{\n
                file_path:"beep/boop/bleep/blorp",\n
                dir_name:"blorp"\n
            },...]\n
        if paths_only = True:\n
            ["beep/boop/bleep/blorp",...]

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 12-19-2021 12:17:24
        `memberOf`: dir
        `version`: 1.0
        `method_name`: get_folders
    '''
    dir_array = []
    if search_path is False:
        search_path = _obj.get_kwarg(['search path', 'search'], _os.getcwd(), (list, str), **kwargs)
    if isinstance(search_path, list) is False:
        search_path = [search_path]

    recursive = _obj.get_kwarg(['recursive', 'recurse'], True, bool, **kwargs)

    include = _obj.get_kwarg(['include'], [], (list, str), **kwargs)
    if isinstance(include, (str)):
        include = [include]

    exclude = _obj.get_kwarg(['exclude', 'ignore', 'ignore array'], [], (list, str), **kwargs)
    if isinstance(exclude, (str)):
        exclude = [exclude]

    paths_only = _obj.get_kwarg(['paths only', 'path only'], False, (bool), **kwargs)

    ftp = _obj.get_kwarg(["ftp"], None, None, **kwargs)
    if ftp is not None:
        return get_folders_ftp(search_path, **kwargs)

    for path in search_path:
        # # pylint: disable=unused-variable
        for root, folders, files in _os.walk(path):
            # print(folders)
            for current_dir in folders:
                if paths_only:
                    dir_array.append(_os.path.join(root, current_dir))
                    continue
                dir_data = {}
                dir_data['dir_name'] = current_dir
                dir_data['file_path'] = _os.path.join(root, current_dir)
                ignore = False
                if len(exclude) > 0:
                    if _csu.array_in_string(exclude, dir_data['file_path']) is True:
                        continue
                if len(include) > 0:
                    if _csu.array_in_string(include, dir_data['file_path']) is False:
                        continue
                # if ignore_array is not False:
                #     for x in ignore_array:
                #         if x in dir_data['file_path']:
                #             ignore = True

                # if ignore is False:

                dir_array.append(dir_data)

            if recursive is False:
                break
    return dir_array


def get_folders_ftp(search_path=False, **kwargs):
    '''
        Get all directories from the search_path.

        ----------

        Arguments
        -------------------------
        `search_path` {str|list}
            The search path or list of paths to iterate.\n
            This is the same as the keyword argument search_path,
            the kwarg is provided for consistency.

        Keyword Arguments
        -----------------
            [`search_path`=cwd] {str|list}
                The search path or list of paths to iterate.

            `ftp` {obj}
                A reference to the ftputil object.

            [`recursive`=True] {boolean}
                If True the path is iterated recursively

            [`exclude`=[]] {str|list}
                A string or list of strings, if the file path contains any of them,
                the directory is ignored.

            [`include`=[]] {str|list}
                A string or list of strings, if the file path does NOT contain any of them,
                the directory is ignored.

            [`paths_only`=False] {bool}
                If True, the returned value will be a list of directory paths.


        Return {list}
        ----------------------
        A list of dictionaries containing all matching directories.\n
        example:\n
            [{\n
                file_path:"beep/boop/bleep/blorp",\n
                dir_name:"blorp"\n
            },...]\n
        if paths_only = True:\n
            ["beep/boop/bleep/blorp",...]

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 12-19-2021 12:31:27
        `memberOf`: dir
        `version`: 1.0
        `method_name`: get_folders_ftp
    '''
    dir_array = []
    if search_path is False:
        search_path = _obj.get_kwarg(['search path', 'search'], _os.getcwd(), (list, str), **kwargs)
    if isinstance(search_path, list) is False:
        search_path = [search_path]

    recursive = _obj.get_kwarg(['recursive', 'recurse'], True, bool, **kwargs)

    include = _obj.get_kwarg(['include'], [], (list, str), **kwargs)
    if isinstance(include, (str)):
        include = [include]

    exclude = _obj.get_kwarg(['exclude', 'ignore', 'ignore array'], [], (list, str), **kwargs)
    if isinstance(exclude, (str)):
        exclude = [exclude]

    paths_only = _obj.get_kwarg(['paths only', 'path only'], False, (bool), **kwargs)

    ftp = _obj.get_kwarg(["ftp"], None, None, **kwargs)
    if ftp is None:
        logger.warning("No FTP obj reference provided.")
        return False

    # print(f"search_path: {search_path}")
    for path in search_path:
        # # pylint: disable=unused-variable
        for root, folders, files in ftp.walk(path):
            # print(folders)
            for current_dir in folders:
                if paths_only:
                    dir_array.append(_os.path.join(root, current_dir))
                    continue
                dir_data = {}
                dir_data['dir_name'] = current_dir
                dir_data['file_path'] = _os.path.join(root, current_dir)
                ignore = False
                if len(exclude) > 0:
                    if _csu.array_in_string(exclude, dir_data['file_path']) is True:
                        continue
                if len(include) > 0:
                    if _csu.array_in_string(include, dir_data['file_path']) is False:
                        continue

                dir_array.append(dir_data)

            if recursive is False:
                break
    return dir_array


def index_files(start_path, extension_array=None, ignore_array=None, recursive=True):
    '''
        Iterates the start_path to find all files within.

        ----------
        Arguments
        -----------------

            `search_path`=cwd {str|list}
                The search path or list of paths to iterate.
            `ignore`=[] {str|list}
                A term or list or terms to ignore if the file path contains any of them.
            `extensions`=[] {str|list}
                An extension or list of extensions that the file must have.
            `recursive`=True {boolean}
                If True the path is iterated recursively

        return
        ----------
        `return` {str}
            A list of dictionaries containing all matching files.
    '''
    if isinstance(extension_array, list) is False:
        extension_array = []
    if isinstance(ignore_array, list) is False:
        ignore_array = []
    file_array = []
    # pylint: disable=unused-variable
    for root, folders, files in _os.walk(start_path):
        for file in files:
            file_data = file.get_data(_os.path.join(root, file))
            ignore = False

            if len(extension_array) > 0:
                if file_data['extension'] not in extension_array:
                    ignore = True

            if len(ignore_array) > 0:
                for ignore_string in ignore_array:
                    if ignore_string in file_data['file_path']:
                        ignore = True

            if ignore is False:
                # fd['file_hash'] = generateFileHash(fd['file_path'])
                file_array.append(file_data)

        if recursive is False:
            break
    return file_array
