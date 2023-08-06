# pylint: disable=too-many-lines
# pylint: disable=too-many-locals
# pylint: disable=too-many-branches
# pylint: disable=bare-except
# pylint: disable=line-too-long
# pylint: disable=unused-import

'''
    A module of utility methods used for deleting directories locally or over FTP.

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

import logging as _logging

import ftputil as _ftputil
from ftputil.error import FTPOSError as _FTPOSError


import utils.file_utils as _f
import utils.dict_utils as _obj
import utils.string_utils as _csu
import utils.directory_utils as _dir

logger = _logging.getLogger(__name__)

def delete(file_path, ftp=None,persistent=True):
    '''
        Deletes a directory from the local machine or FTP server.

        ----------

        Arguments
        -------------------------
        `file_path` {str}
            The path of the directory to delete.

        [`ftp`=None] {obj}
            A reference to the ftputil object.


        Return {bool}
        ----------------------
        True upon success, false otherwise.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 12-19-2021 11:56:21
        `memberOf`: dir
        `version`: 1.0
        `method_name`: delete
    '''
    attempt_limit = 100
    if persistent is False:
        attempt_limit = 1

    for _ in range(attempt_limit):
        # success = False
        if ftp is not None:
            success = delete_ftp(file_path, ftp)
        else:
            try:
                _shutil.rmtree(file_path)
                success = True
                return True
            except OSError as error:
                if persistent is False:
                    logger.warning("Failed to delete local directory: %s", file_path)
                    logger.warning("Error: %s : %s", file_path, error.strerror)
                    # success = False
                # print("Error: %s : %s" % (file_path, error.strerror))
        return success


def delete_ftp(file_path, ftp):
    '''
        Deletes a directory on an FTP server.

        ----------

        Arguments
        -------------------------
        `file_path` {str}
            The path of the directory to delete.

        [`ftp`=None] {obj}
            A reference to the ftputil object.

        Return {bool}
        ----------------------
        True upon success, false otherwise.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 12-19-2021 12:11:53
        `memberOf`: dir
        `version`: 1.0
        `method_name`: delete_ftp
    '''
    success = False
    if _dir.exists_ftp(file_path, ftp):
        # print(f"{file_path} exists.")
        try:
            ftp.rmtree(file_path)
            success = True
        except _FTPOSError as error:
            logger.warning("Failed to delete FTP directory: %s", file_path)
            logger.warning("Error: %s : %s", file_path, error.strerror)
    else:
        success = True
    return success

