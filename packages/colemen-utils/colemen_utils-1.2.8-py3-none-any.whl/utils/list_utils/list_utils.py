# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=unused-import
'''
    A module of utility methods used manipulating lists.

    ----------

    Meta
    ----------
    `author`: Colemen Atwood
    `created`: 06-03-2022 10:22:15
    `memberOf`: list_utils
'''

import utils.dict_utils as _obj

from utils.string_utils.string_conversion import array_to_string_list as to_string_list
from utils.string_utils.string_format import array_replace_string as replace_from_list
from utils.string_utils.string_format import array_in_string as find_in_string



def append(base=None,value=None,**kwargs):
    '''
        Append an item to the base list.
        This is a lazy way of merging lists or appending a single item.

        ----------

        Arguments
        -------------------------
        `base` {list}
            The list to append an item to.
        `value` {any}
            The value to append to the base.

        Keyword Arguments
        -------------------------
        [`skip_null`=True] {bool}
            if True and the value is None, it will not append it.

        Return {type}
        ----------------------
        return_description

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 06-01-2022 08:45:33
        `memberOf`: objectUtils
        `version`: 1.0
        `method_name`: append
        # @TODO []: documentation for append
    '''

    if base is None:
        base = []

    skip_null = _obj.get_kwarg(["skip_null"],True,(bool),**kwargs)
    if skip_null is True:
        if value is None:
            return base

    if isinstance(value,(list)):
        base = base + value
    else:
        base.append(value)
    return base

def strip_list_nulls(value:list)->list:
    '''
        Strip None values from a list.

        ----------

        Arguments
        -------------------------
        `value` {list}
            The list to filter None values from.

        Return {list}
        ----------------------
        The list with all None values removed.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 06-03-2022 08:38:50
        `memberOf`: objectUtils
        `version`: 1.0
        `method_name`: strip_list_nulls
        * @xxx [06-03-2022 08:39:37]: documentation for strip_list_nulls
    '''


    if isinstance(value,(list)) is False:
        return value
    return [x for x in value if x is not None]

def find_list_diff(list_one, list_two):
    '''
        find elements in list_one that do not exist in list_two.
        @param {list} list_one the primary list for comparison
        @param {list} list_two
        @function findListDiff
    '''
    return [x for x in list_one if x not in list_two]

def force_list(value)->list:
    '''
        Confirm that the value is a list, if not wrap it in a list.

        ----------

        Arguments
        -------------------------
        `value` {any}
            The value to test.

        Return {list}
        ----------------------
        The value as a list 

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 06-03-2022 09:13:57
        `memberOf`: object_utils
        `version`: 1.0
        `method_name`: force_list
        * @xxx [06-03-2022 09:14:52]: documentation for force_list
    '''


    if isinstance(value,(list)) is False:
        return [value]
    return value








