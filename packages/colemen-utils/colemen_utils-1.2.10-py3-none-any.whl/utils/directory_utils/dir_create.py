# pylint: disable=too-many-lines
# pylint: disable=too-many-locals
# pylint: disable=too-many-branches
# pylint: disable=bare-except
# pylint: disable=line-too-long
# pylint: disable=unused-import

'''
    Utility methods for Creating / Copying directories locally or over FTP.

    ----------

    Meta
    ----------
    `author`: Colemen Atwood
    `created`: 06-04-2022 10:43:25
    `memberOf`: directory_utils
'''

# import json
# from re import search
# import time
# import json
# from threading import Thread
import traceback as _traceback
import os as _os
from pathlib import Path as _Path
import logging as _logging

import ftputil as _ftputil



import utils.dict_utils as _obj
import utils.directory_utils as _dir
import utils.file_utils as _f
import utils.string_utils as _csu


logger = _logging.getLogger(__name__)


def create(path, dir_name=False, **kwargs):
    '''
        Create a directory or path of directories on the local machine or an FTP server.

        ----------

        Arguments
        -------------------------
        `path` {str}
            The path to create or a path to where it should create the dir_name directory
        [`dir_name`=False] {str}
            The name of the directory to create.

        Keyword Arguments
        -----------------
        [`ftp`=None] {obj}
            A reference to the ftputil object.

        Return {bool}
        ----------------------
        True upon success, false otherwise.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 12-19-2021 11:33:50
        `memberOf`: dir
        `version`: 1.0
        `method_name`: create
    '''
    success = False
    ftp = _obj.get_kwarg(["ftp"], None, None, **kwargs)
    if dir_name is not False:
        path = _os.path.join(path, dir_name)

    if ftp is not None:
        try:
            if ftp.path.exists(path) is False:
                ftp.makedirs(path, exist_ok=True)
                success = True
        except _ftputil.error.PermanentError as error:
            print(f"error: {str(error)}")
            print(_traceback.format_exc())
    else:
        if _dir.exists(path) is False:
            _Path(path).mkdir(parents=True, exist_ok=True)
            if _dir.exists(path) is True:
                success = True
        else:
            success = True

    return success




def copy(src, dst=False, **kwargs):
    '''
        Copy a directory to another location.

        ----------

        Arguments
        -------------------------
        `src` {str|list|dict}
            The source directory to copy.\n
            A list of dictionaries/lists:\n
                [["xxx","aaa"],{src_path:"xxx",dst_path:"aaa"}]
            A dictionary:\n
                {src_path:"xxx",dst_path:"aaa"}

        Keyword Arguments
        -------------------------
        `ftp` {obj}
            A reference to the ftputil object.
        [`ftp_direction`='local_to_server'] {str}
            The direction of the copying:
                local_to_server: Copy local directories/files to the FTP server.
                server_to_local: Copy FTP server directories/files to the Local machine.

        Return {type}
        ----------------------
        return_description

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 12-19-2021 12:34:48
        `memberOf`: dir
        `version`: 1.0
        `method_name`: copy
    '''
    ftp = _obj.get_kwarg(["ftp"], None, None, **kwargs)
    ftp_direction = _obj.get_kwarg(["ftp direction"], 'local_to_server', (str), **kwargs)
    copy_list = [src, dst]
    if dst is False:
        copy_list = _parse_copy_data_from_obj(src)

    for dir_data in copy_list:
        if ftp is not None:
            if ftp_direction == 'local_to_server':
                mirror_to_server(dir_data['src_path'], dir_data['dst_path'], **kwargs)
        else:
            mirror(dir_data['src_path'], dir_data['dst_path'], **kwargs)


def mirror(src, dst, **kwargs):
    '''
        Mirrors a source directory to the destination directory.\n
        Optionally, copying files.\n

        ----------

        Arguments
        -------------------------
        `src` {str}
            The file path to be copied to the dst
        `dst` {str}
            The path to copy the src to.

        Keyword Arguments
        -------------------------
        [`empty_files`=False] {bool}
            If True, files are copied but have no contents.
        [`dirs_only`=False] {bool}
            If True, only directories are copied.
        [`recursive`=True] {bool}
            If True the path is iterated recursively
        [`exclude`=[]] {str|list}
            A string or list of strings, if the file path contains any of them,
            the directory is ignored.\n
            If provided, these rules apply to both files and directories.
        [`include`=[]] {str|list}
            A string or list of strings, if the file path does NOT contain any of them,
            the directory is ignored.\n
            If provided, these rules apply to both files and directories.
        [`exclude_dirs`=[]] {str|list}
            A string or list of strings, if the file path contains any of them,
            the directory is ignored.\n
            If provided, these rules apply only to directories.
        [`include_dirs`=[]] {str|list}
            A string or list of strings, if the file path does NOT contain any of them,
            the directory is ignored.\n
            If provided, these rules apply only to directories.
        [`exclude_files`=[]] {str|list}
            A string or list of strings, if the file path contains any of them,
            the directory is ignored.\n
            If provided, these rules apply only to files.
        [`include_files`=[]] {str|list}
            A string or list of strings, if the file path does NOT contain any of them,
            the directory is ignored.\n
            If provided, these rules apply only to files.
        [`ftp`=None] {obj}
            A reference to the ftputil object.
        [`ftp_direction`='local_to_server'] {str}
            The direction of the copying:
                local_to_server: Copy local directories/files to the FTP server.
                server_to_local: Copy FTP server directories/files to the Local machine.


        Return {type}
        ----------------------
        return_description

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 12-11-2021 14:34:12
        `memberOf`: dir
        `version`: 1.0
        `method_name`: mirror
    '''
    # if EMPTY_FILES is True, it creates a duplicate file with no content.
    empty_files = _obj.get_kwarg(['empty files'], False, bool, **kwargs)
    dirs_only = _obj.get_kwarg(['dirs only'], False, bool, **kwargs)
    recursive = _obj.get_kwarg(['recursive', 'recurse'], True, (bool), **kwargs)
    include = _obj.get_kwarg(['include'], [], (list, str), **kwargs)
    exclude = _obj.get_kwarg(['exclude'], [], (list, str), **kwargs)

    include_dirs = _obj.get_kwarg(['include dirs'], include, (list, str), **kwargs)
    exclude_dirs = _obj.get_kwarg(['exclude dirs'], exclude, (list, str), **kwargs)

    include_files = _obj.get_kwarg(['include files'], include, (list, str), **kwargs)
    exclude_files = _obj.get_kwarg(['exclude files'], exclude, (list, str), **kwargs)

    ftp = _obj.get_kwarg(["ftp"], None, None, **kwargs)
    ftp_direction = _obj.get_kwarg(["ftp direction"], 'local_to_server', (str), **kwargs)

    if ftp is not None:
        if ftp_direction == "local_to_server":
            return mirror_to_server(src, dst, **kwargs)

    src = _os.path.abspath(src)
    if _dir.exists(src) is False:
        logger.warning("Source path must exist.\nsource: %s", src)
        return False

    if _dir.exists(dst) is False:
        _os.makedirs(dst)
    dirs = _dir.get_folders(search_path=src, recursive=recursive,
                       include=include_dirs, exclude=exclude_dirs)

    for folder in dirs:
        folder['dst_path'] = folder['file_path'].replace(src, dst)
        try:
            _os.makedirs(folder['dst_path'], exist_ok=True)
            if dirs_only is False:
                files = _f.get_files(search_path=folder['file_path'], include=include_files,
                                       exclude=exclude_files, recursive=False)
                # newlist = [x['dst_path'] = x['file_path'].replace(src, dst) for x in files]
                for file in files:
                    file['src_path'] = file['file_path']
                    file['dst_path'] = file['file_path'].replace(src, dst)
                # folder['dst_path'] = folder['file_path'].replace(src, dst)
                if empty_files is True:
                    for file in files:
                        _f.write(file['dst_path'], "EMPTY TEST FILE CONTENT")
                else:
                    _f.copy(files)
        except:
            # print(f"{_traceback.format_exc()}")
            logger.warning("failed to create directory: %s", folder["dst_path"])
            logger.warning(_traceback.format_exc())


def mirror_to_server(src, dst, **kwargs):
    '''
        Mirrors the local source directory to the FTP destination directory.
        Optionally, copying files.

        ----------

        Arguments
        -------------------------
        `src` {str}
            The LOCAL file path to be copied to the dst
        `dst` {str}
            The FTP path to copy the src to.

        Keyword Arguments
        -------------------------
        `ftp` {obj}
            A reference to the ftputil object.
        [`dirs_only`=False] {bool}
            If True, only directories are copied.
        [`recursive`=True] {bool}
            If True the path is iterated recursively
        [`exclude`=[]] {str|list}
            A string or list of strings, if the file path contains any of them,
            the directory is ignored.\n
            If provided, these rules apply to both files and directories.
        [`include`=[]] {str|list}
            A string or list of strings, if the file path does NOT contain any of them,
            the directory is ignored.\n
            If provided, these rules apply to both files and directories.
        [`exclude_dirs`=[]] {str|list}
            A string or list of strings, if the file path contains any of them,
            the directory is ignored.\n
            If provided, these rules apply only to directories.
        [`include_dirs`=[]] {str|list}
            A string or list of strings, if the file path does NOT contain any of them,
            the directory is ignored.\n
            If provided, these rules apply only to directories.
        [`exclude_files`=[]] {str|list}
            A string or list of strings, if the file path contains any of them,
            the directory is ignored.\n
            If provided, these rules apply only to files.
        [`include_files`=[]] {str|list}
            A string or list of strings, if the file path does NOT contain any of them,
            the directory is ignored.\n
            If provided, these rules apply only to files.



        Return {type}
        ----------------------
        return_description

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 12-11-2021 14:34:12
        `memberOf`: dir
        `version`: 1.0
        `method_name`: mirror
    '''
    # if EMPTY_FILES is True, it creates a duplicate file with no content.
    dirs_only = _obj.get_kwarg(['dirs only'], False, bool, **kwargs)
    recursive = _obj.get_kwarg(['recursive', 'recurse'], True, (bool), **kwargs)
    include = _obj.get_kwarg(['include'], [], (list, str), **kwargs)
    exclude = _obj.get_kwarg(['exclude'], [], (list, str), **kwargs)

    include_dirs = _obj.get_kwarg(['include dirs'], include, (list, str), **kwargs)
    exclude_dirs = _obj.get_kwarg(['exclude dirs'], exclude, (list, str), **kwargs)

    include_files = _obj.get_kwarg(['include files'], include, (list, str), **kwargs)
    exclude_files = _obj.get_kwarg(['exclude files'], exclude, (list, str), **kwargs)

    ftp = _obj.get_kwarg(["ftp"], None, None, **kwargs)
    if ftp is None:
        logger.warning("No FTP object provided.")
        return False

    src = _os.path.abspath(src)
    if _dir.exists(src) is False:
        logger.warning("Source path must exist.\nsource: %s", src)
        return False

    if _dir.exists(dst, ftp=ftp) is False:
        create(dst, ftp=ftp)

    dirs = _dir.get_folders(search_path=src, recursive=recursive,
                       include=include_dirs, exclude=exclude_dirs, ftp=ftp)

    for folder in dirs:
        folder['dst_path'] = folder['file_path'].replace(src, dst)
        try:
            create(folder['dst_path'], ftp=ftp)
            if dirs_only is False:
                files = _f.get_files(search_path=folder['file_path'], include=include_files,
                                       exclude=exclude_files, recursive=False, ftp=ftp)
                # newlist = [x['dst_path'] = x['file_path'].replace(src, dst) for x in files]
                for file in files:
                    file['src_path'] = file['file_path']
                    file['dst_path'] = file['file_path'].replace(src, dst)
                _f.copy(files, ftp=ftp)
        except:
            logger.warning("failed to create directory: %s", folder["dst_path"])
            logger.warning(_traceback.format_exc())


def _parse_copy_data_from_obj(file_obj):
    data = {
        "src_path": None,
        "dst_path": None,
    }
    if isinstance(file_obj, (tuple, list)):
        if len(file_obj) == 2:
            data['src_path'] = file_obj[0]
            data['dst_path'] = file_obj[1]
        else:
            print("Invalid list/tuple provided for copy file. Must be [source_file_path, destination_file_path]")
    if isinstance(file_obj, (dict)):
        for syn in _f.resources.SRC_PATH_SYNONYMS:
            synvar = _csu.variations(syn)
            for synonym_variant in synvar:
                if synonym_variant in file_obj:
                    data['src_path'] = file_obj[synonym_variant]
        for syn in _f.resources.DEST_PATH_SYNONYMS:
            synvar = _csu.variations(syn)
            for synonym_variant in synvar:
                if synonym_variant in file_obj:
                    data['dst_path'] = file_obj[synonym_variant]

    if _dir.exists(data['src_path']) is False:
        print(f"Invalid source path provided, {data['src_path']} could not be found.")
    return data



























