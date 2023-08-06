# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-import

'''
    A module of utility methods used for formatting strings.

    ----------

    Meta
    ----------
    `author`: Colemen Atwood
    `created`: 12-09-2021 09:00:27
    `memberOf`: string_utils
'''



from typing import Union as _Union
import re as _re
import os as _os

import utils.string_utils as _csu
from utils.sql_utils.sql_utils import strip_comments as strip_sql_comments


def strip(value:str,chars:list,side='both'):
    '''
        Strips characters/strings from the beginning,end or both sides of a string.

        ----------

        Arguments
        -------------------------
        `value` {str}
            The value to be formatted

        `chars` {list}
            A list of strings to be stripped from the value

        [`side`='both'] {str}
            Can be "left", "right", "both"

        Return {str}
        ----------------------
        The formatted value.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 02-04-2022 10:25:04
        `memberOf`: string_format
        `version`: 1.0
        `method_name`: strip_any
    '''
    new_value = value
    cycle = True
    if side in ["both","left"]:
        cycle = True
        while cycle is True:
            matchFound = False
            for char in chars:
                if new_value.startswith(char):
                    new_value = new_value[len(char):]
                    matchFound = True
                else:
                    continue
            if matchFound is False:
                cycle = False
    if side in ["both","right"]:
        cycle = True
        while cycle is True:
            matchFound = False
            for char in chars:
                if new_value.endswith(char):
                    new_value = new_value[:-len(char)]
                    matchFound = True
                else:
                    continue
            if matchFound is False:
                cycle = False
    return new_value

def strip_excessive_spaces(value:str)->str:
    '''
        Removes excessive (2 or more consecutive) spaces from the string.

        ----------

        Arguments
        -------------------------
        `value` {str}
            The string to format.

        Return {str}
        ----------------------
        The formatted string

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 12-09-2021 08:19:28
        `memberOf`: string_format
        `version`: 1.0
        `method_name`: strip_excessive_spaces
    '''
    return strip_excessive_chars(value," ")

def strip_excessive_chars(value:str,chars:_Union[str,list])->str:
    '''
        Removes excessive (2 or more consecutive) chars from the string.

        ----------

        Arguments
        -------------------------
        `value` {str}
            The string to format.
        `chars` {str|list}
            The chars to remove if they occur excessively.

        Return {str}
        ----------------------
        The formatted string

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 06-03-2022 11:47:37
        `memberOf`: string_format
        `version`: 1.0
        `method_name`: strip_excessive_chars
    '''
    if isinstance(chars,(str)):
        chars = [chars]
    for c in chars:
        if c == " ":
            c = "\\s"

        reg_c = _csu.escape_regex(c)
        exp = rf"[{reg_c}]{{2,}}"
        # print(exp)
        reg = _re.compile(exp)
        value = _re.sub(reg, c, value)
    return value

def strip_start(text:str, prefix:str):
    '''
        Remove a string from the beginning of another string.

        ----------

        Arguments
        -------------------------
        `text` {str}
            The string to modify

        `prefix` {str}
            The string to remove from the beginning.

        Return {type}
        ----------------------
        return_description

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 06-04-2022 14:38:53
        `memberOf`: string_strip
        `version`: 1.0
        `method_name`: strip_start
        * @TODO []: documentation for strip_start
    '''

    while text.startsWith(prefix):
        text = text[-len(prefix):]
    return text

def strip_end(text:str, suffix:str):
    '''
        Strip a string from the end of the text.
        This will remove the suffix regardless of how many times it is repeated.

        ----------

        Arguments
        -------------------------
        `text` {str}
            The string to modify

        `suffix` {str}
            The string to remove from the ending of the other string.

        Return {str}
        ----------------------
        The text with the suffix removed.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 06-04-2022 14:43:01
        `memberOf`: string_strip
        `version`: 1.0
        `method_name`: strip_end
        * @xxx [06-04-2022 14:45:09]: documentation for strip_end
    '''

    while text.endswith(suffix):
        text = text[-len(suffix):]
    return text






