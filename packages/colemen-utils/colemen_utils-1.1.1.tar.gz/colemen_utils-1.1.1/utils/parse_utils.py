# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-import
'''
    Module of string parsing methods.

    ----------

    Meta
    ----------
    `author`: Colemen Atwood
    `created`: 12-19-2021 13:57:27
    `memberOf`: parse_utils
    `version`: 1.0
    `method_name`: parse_utils
'''

# import json
# import hashlib
# import string

# import re
# import utils.object_utils as objUtils
import logging
import utils.object_utils as obj
import facades.sql_parse_facade as sql
logger = logging.getLogger(__name__)


def array_in_string(array, value, default=False):
    '''
        iterates the array provided checking if any element exists in the value.

        ----------

        Arguments
        -------------------------
        `array` {list}
            The list of terms to search for in the value.
        `value` {str}
            The string to search within
        [`default`=False] {mixed}
            The default value to return if no match is found.

        Return {mixed}
        ----------------------
        True if a match is found, returns the default value otherwise.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 12-19-2021 13:54:36
        `memberOf`: parse_utils
        `version`: 1.0
        `method_name`: array_in_string
    '''
    if len(array) == 0:
        return default
    if isinstance(value, (str)) is False:
        logger.warning('Second argument of array_in_string, must be a string.')
        logger.warning(value)
        return default
    for item in array:
        if item in value:
            return True
    return default

def array_replace_string(value,needles, new_string="", **kwargs):
    '''
        Replaces any matching substrings found in the needles list with new_string.

        ----------

        Arguments
        -------------------------
        `value` {str}
            The string that will be modified.
            
        `needles` {list}
            A list of strings to replace in the the value
            
        [`new_string`=""] {str}
            What the needle will be replaced with in the value
            

        Keyword Arguments
        -------------------------
        `max_replace` {int}
            The maximum number of replacements to make.
            if <= 0, it will find and replace all elements in the array.

        Return {str}
        ----------------------
        The formatted string.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 01-06-2022 10:36:28
        `memberOf`: parse_utils
        `version`: 1.0
        `method_name`: array_replace_string
    '''
    max_replace = obj.get_kwarg(['max','max replace'],0,(int),**kwargs)
    if len(needles) == 0:
        return value

    if isinstance(value, (str)) is False:
        logger.warning('value must be a string.')
        logger.warning(value)

    replace_count = 0
    result_string = value
    for needle in needles:
        if needle in value:
            replace_count += 1
            result_string = result_string.replace(needle,new_string)
            if max_replace > 0:
                if replace_count >= max_replace:
                    return result_string

    return result_string
