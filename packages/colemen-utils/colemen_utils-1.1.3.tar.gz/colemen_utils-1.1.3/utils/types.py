# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long

# import random
# from typing import Union

# from colorama import Fore, Style

BOOL_TRUE_SYNONYMS = ["TRUE", "true", "True", "yes", "y", "1","sure","correct","affirmative"]
BOOL_FALSE_SYNONYMS = ["FALSE", "false", "False", "no", "n", "0","wrong","incorrect","nope","negative"]

VALID_PYTHON_TYPES = {
    "str":["string","str","text","varchar"],
    "int":["integer","number","int"],
    "float":["float","double"],
    "list":["list","array"],
    "tuple":["tuple","set"],
    "set":["set"],
    "dict":["dictionary","dict"],
    "boolean":["boolean","bool"]
}

def determine_boolean(value:str, def_val=None)->bool:
    '''
        Attempts to determine a boolean value from a string using synonyms

        ----------

        Arguments
        -------------------------
        `value` {string}
            The string to parse for a boolean value.

        [`def_val`=None] {mixed}
            The value to return if a boolean cannot be determined

        Return {bool|None|Mixed}
        ----------------------
        True if the value contains a True synonym.
        False if the value contains a False synonym.
        def_val [None] if no boolean value can be determined.


        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 12-09-2021 08:10:55
        `memberOf`: parse_utils
        `version`: 1.0
        `method_name`: determine_boolean
    '''
    result = def_val
    if value in BOOL_TRUE_SYNONYMS:
        result = True
    if value in BOOL_FALSE_SYNONYMS:
        result = False
    return result


def python_type_name(value):
    '''
        Attempts to determine the type name of the value provided.
        It checks if the value is a synonym of a known python type.

        ----------

        Arguments
        -------------------------
        `value` {string}
            The value to test.

        Return {string|None}
        ----------------------
        The type if it can be determined, None otherwise.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 03/21/2022 12:03:11
        `version`: 1.0
        `method_name`: python_type_name
        # @TODO []: documentation for python_type_name
    '''

    results = []
    if isinstance(value,(str)):
        value = [value]
    else:
        return None

    for test_val in value:
        test_val = test_val.lower()
        for type_name,val in VALID_PYTHON_TYPES.items():
            if test_val in val:
                results.append(type_name)
    results = list(set(results))
    if len(results) == 0:
        return None
    if len(results) == 1:
        return results[0]
    return results


