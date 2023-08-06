# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=line-too-long
# pylint: disable=unused-import

'''
    A module of utility methods used for converting to and from strings

    ----------

    Meta
    ----------
    `author`: Colemen Atwood
    `created`: 12-09-2021 09:00:27
    `memberOf`: string_utils
'''


# import json
# import hashlib
# import string
import re as _re
# import utils.string_format as mod
import utils.dict_utils as _obj
import utils.string_utils as _csu
import utils.type_utils as _types
from utils.type_utils.type_utils import determine_boolean,to_bool





def string_to_int(value):
    '''
        Attempts to convert a string to an integer.

        ----------

        Arguments
        -------------------------
        `value` {string|integer}
                The value to convert.


        Return {int|None}
        ----------------------
        The integer value if successful. Otherwise None.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 03-21-2022 12:17:01
        `version`: 1.0
        `method_name`: string_to_int
        # @xxx [03-21-2022 12:17:15]: documentation for string_to_int
    '''


    if isinstance(value,(int)):
        return value

    # @Mstep [IF] if the value contains non numeric chars.
    if _re.match(r'[^0-9\.]',value) is not None:
        # @Mstep [] strip the non-numeric characters.
        value = _re.sub(r'[^0-9\.]','',value)
    print(f"value: {value}")
    match = _re.match(r'([0-9]*)',value)
    if match is not None:
        value = match[1]

    if len(value) > 0:
        return int(value)

    return None

def array_to_string_list(array, **kwargs):
    '''
        Convert a python list to a literal list of items as a string.

        ----------

        Arguments
        -------------------------
        `array` {list}
            The list to convert to a string.

        Keyword Arguments
        -------------------------
        `arg_name` {type}
                arg_description

        `item_sep` {str}
            A string that will be used to separate the list items.

        `item_wrap` {str}
            A string that will be prepended and appended to each list item.
            This overrides the item_prefix and item_suffix.

        `item_prefix` {str}
            A string that will be prepended to each item in the list.

        `item_suffix` {str}
            A string that will be appended to each item in the list.

        `list_wrap` {str}
            A string that will be prepended and appended to the list as a whole.

        `list_prefix` {str}
            A string that will be prepended to the list string.

        `list_suffix` {str}
            A string that will be appended to the list string.

        Return {str}
        ----------------------
        The list as a string.


        Examples
        ----------------------
        data = ["kitties", "and", "titties"]

        _csu.convert.array_to_string_list(data)

        // 'kitties', 'and', 'titties'

        _csu.convert.array_to_string_list(data,item_wrap="`",list_wrap="{")

        // {\\`kitties\\`, \\`and\\`, \\`titties\\`}


        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 06-02-2022 13:37:35
        `memberOf`: string_conversion
        `version`: 1.0
        `method_name`: array_to_string_list
        * @xxx [06-02-2022 13:43:18]: documentation for array_to_string_list
    '''


    list_prefix = ""
    list_suffix = ""
    item_prefix = ""
    item_suffix = ""


    item_wrap = _obj.get_kwarg(["item wrap"], "AUTO", (str), **kwargs)
    item_sep = _obj.get_kwarg(["item sep"], ", ", (str), **kwargs)
    item_prefix = _obj.get_kwarg(["item prefix"], "", (str), **kwargs)
    item_suffix = _obj.get_kwarg(["item suffix"], "", (str), **kwargs)
    list_wrap = _obj.get_kwarg(["list wrap"], "", (str), **kwargs)
    list_prefix = _obj.get_kwarg(["list prefix"], "", (str), **kwargs)
    list_suffix = _obj.get_kwarg(["list suffix"], "", (str), **kwargs)

    # if 'ITEM_SEP' in kwargs:
    #     item_sep = kwargs['ITEM_SEP']
    # if 'ITEM_WRAP' in kwargs:
    dif_wrap = False
    if item_wrap == "(" or item_wrap == ")":
        item_prefix = "("
        item_suffix = ")"
        dif_wrap = True
    if item_wrap == "{" or item_wrap == "}":
        item_prefix = "{"
        item_suffix = "}"
        dif_wrap = True

    if dif_wrap is False:
        item_prefix = item_wrap
        item_suffix = item_wrap

    # if 'ITEM_PREFIX' in kwargs:
    #     item_prefix = kwargs['ITEM_PREFIX']
    # if 'ITEM_SUFFIX' in kwargs:
    #     item_suffix = kwargs['ITEM_SUFFIX']

    # if 'LIST_WRAP' in kwargs:
    # list_wrap = kwargs['LIST_WRAP']
    dif_wrap = False
    if list_wrap == "(" or list_wrap == ")":
        list_prefix = "("
        list_suffix = ")"
        dif_wrap = True
    if list_wrap == "{" or list_wrap == "}":
        list_prefix = "{"
        list_suffix = "}"
        dif_wrap = True

    if dif_wrap is False:
        list_prefix = list_wrap
        list_suffix = list_wrap

    # if 'LIST_PREFIX' in kwargs:
    #     list_prefix = kwargs['LIST_PREFIX']
    # if 'LIST_SUFFIX' in kwargs:
    #     list_suffix = kwargs['LIST_SUFFIX']

    ilen = len(array) - 1
    cur_idx = 0
    list_string = ""
    for list_value in array:
        if item_wrap == "AUTO":
            if isinstance(list_value, int):
                item_prefix = ""
                item_suffix = ""
            if isinstance(list_value, str):
                item_prefix = "'"
                item_suffix = "'"
                if "'" in list_value:
                    list_value = _csu.charcode_escape(list_value,chars=["'"])
            if list_value == "None" or list_value is None:
                list_value = "NULL"
                item_prefix = ""
                item_suffix = ""

        list_string += f"{item_prefix}{list_value}{item_suffix}"
        if cur_idx != ilen:
            list_string += item_sep
        cur_idx += 1
    return f"{list_prefix}{list_string}{list_suffix}"




