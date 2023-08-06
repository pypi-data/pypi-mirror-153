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
    `memberOf`: string_conversion
    `version`: 1.0
    `method_name`: string_conversion
'''


# import json
# import hashlib
# import string
import re
import utils.object_utils as obj
# import utils.string_format as mod
import facades.sql_convert_facade as sql


def bool_to_string(value, **kwargs):
    '''
        Converts a boolean value to a string representation.

        ----------

        Arguments
        -------------------------
        `value` {bool}
            The boolean to convert

        Keyword Arguments
        -------------------------
        [`number`=False] {bool}
            if True, the result will be a string integer "1" for True and "0" for False.

        Return {string|None}
        ----------------------
        ("true"|"1") if the boolean is True, ("false"|"0") if it is False.

        None otherwise

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 12-09-2021 08:57:03
        `memberOf`: string_conversion
        `version`: 1.0
        `method_name`: bool_to_string
    '''

    number = obj.get_kwarg(["number"], False, (bool), **kwargs)
    result = None
    if value is True:
        result = "true"
        if number is True:
            result = "1"
    if value is False:
        result = "false"
        if number is True:
            result = "0"
    return result

def bool_to_int(value,default=0):
    '''
        Convert a boolean value to its integer equivalent.

        ----------

        Arguments
        -------------------------
        `value` {bool}
            The boolean to convert
        [`default`=0] {any}
            The default value to return if a boolean cannot be determined.



        Return {int}
        ----------------------
        The integer equivalent

        True = 1
        False = 0

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 06-01-2022 13:46:56
        `memberOf`: string_conversion
        `version`: 1.0
        `method_name`: bool_to_int
        * @xxx [06-01-2022 13:48:26]: documentation for bool_to_int
    '''


    if isinstance(value,(bool)) is False:
        return default

    if value is True:
        return 1
    if value is False:
        return 0

def to_bool(value,default=False):
    '''
        Convert a string to its boolean equivalent.

        ----------

        Arguments
        -------------------------
        `value` {str}
            the value to convert.
        [`default`=False] {any}
            The default value to return if a boolean cannot be determined.

        Return {bool}
        ----------------------
        The boolean equivalent if successful, the default value otherwise.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 06-01-2022 13:40:42
        `memberOf`: string_conversion
        `version`: 1.0
        `method_name`: to_bool
        * @xxx [06-01-2022 13:42:09]: documentation for to_bool
    '''


    if isinstance(value,(bool)):
        return value

    True_syns =["yes","y","sure","correct","indeed","right","affirmative","yeah","ya","true","1"]
    False_syns =["no","n","wrong","incorrect","false","negative","0"]
    if str(value).lower() in True_syns:
        return True
    if str(value).lower() in False_syns:
        return False
    return default

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
        `created`: 03\21\2022 12:17:01
        `version`: 1.0
        `method_name`: string_to_int
        # @xxx [03\21\2022 12:17:15]: documentation for string_to_int
    '''


    if isinstance(value,(int)):
        return value

    # @Mstep [IF] if the value contains non numeric chars.
    if re.match(r'[^0-9\.]',value) is not None:
        # @Mstep [] strip the non-numeric characters.
        value = re.sub(r'[^0-9\.]','',value)
    print(f"value: {value}")
    match = re.match(r'([0-9]*)',value)
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

        csu.convert.array_to_string_list(data)

        // 'kitties', 'and', 'titties'

        csu.convert.array_to_string_list(data,item_wrap="`",list_wrap="{")

        // {\`kitties\`, \`and\`, \`titties\`}


        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 06-02-2022 13:37:35
        `memberOf`: string_conversion
        `version`: 1.0
        `method_name`: array_to_string_list
        * @xxx [06-02-2022 13:43:18]: documentation for array_to_string_list
    '''


    from utils.string_format import sanitize_quotes
    list_prefix = ""
    list_suffix = ""
    item_prefix = ""
    item_suffix = ""


    item_wrap = obj.get_kwarg(["item wrap"], "AUTO", (str), **kwargs)
    item_sep = obj.get_kwarg(["item sep"], ", ", (str), **kwargs)
    item_prefix = obj.get_kwarg(["item prefix"], "", (str), **kwargs)
    item_suffix = obj.get_kwarg(["item suffix"], "", (str), **kwargs)
    list_wrap = obj.get_kwarg(["list wrap"], "", (str), **kwargs)
    list_prefix = obj.get_kwarg(["list prefix"], "", (str), **kwargs)
    list_suffix = obj.get_kwarg(["list suffix"], "", (str), **kwargs)

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
                    list_value = sanitize_quotes(list_value)
            if list_value == "None" or list_value is None:
                list_value = "NULL"
                item_prefix = ""
                item_suffix = ""

        list_string += f"{item_prefix}{list_value}{item_suffix}"
        if cur_idx != ilen:
            list_string += item_sep
        cur_idx += 1
    return f"{list_prefix}{list_string}{list_suffix}"
