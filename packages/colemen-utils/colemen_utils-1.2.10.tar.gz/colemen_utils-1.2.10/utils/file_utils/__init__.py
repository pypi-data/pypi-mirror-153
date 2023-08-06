# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-wildcard-import
# pylint: disable=wildcard-import
# pylint: disable=unused-import
'''
    A module of utility methods used for manipulating files locally or over FTP.

    ----------

    Meta
    ----------
    `author`: Colemen Atwood
    `created`: dtstamp
    `memberOf`: file_utils
'''

import utils.file_utils.file_read as read
import utils.file_utils.file_write as writer
import utils.file_utils.file_image as image
import utils.file_utils.file_convert as convert
import utils.file_utils.file_search as search
import utils.file_utils.file_compression as compress

# import utils.file_utils.file_string_facade
# from utils.string_utils import windows_file_name as format_windows_file_name
# from utils.string_utils import extension as format_extension
# from utils.string_utils import file_path as format_file_path
# from utils.string_utils import url as format_url


# import utils.file_utils.file_read
# import utils.file_utils.file_write
# import utils.file_utils.file_image
# import utils.file_utils.file_convert
# import utils.file_utils.file_search
# import utils.file_utils.file_compression

from utils.file_utils.file_read import *
from utils.file_utils.file_write import *
from utils.file_utils.file_image import *
from utils.file_utils.file_convert import *
from utils.file_utils.file_search import *
from utils.file_utils.file_compression import *

from utils.file_utils.file_utils import *
from utils.file_utils.resources import *
import utils.file_utils.exiftool as _exiftool



