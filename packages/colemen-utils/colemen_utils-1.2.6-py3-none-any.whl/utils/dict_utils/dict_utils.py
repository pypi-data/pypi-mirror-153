# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
'''
    A module of utility methods used for manipulating dictionaries.

    ----------

    Meta
    ----------
    `author`: Colemen Atwood
    `created`: 06-03-2022 10:22:15
    `memberOf`: dict_utils
'''
# import random

from typing import Union as _Union
from colorama import Fore as _Fore
from colorama import Style as _Style
import utils.list_utils as _lu




def set_defaults(default_vals, obj):
    '''
        Sets default values on the dict provided, if they do not already exist.

        ----------

        Arguments
        -------------------------
        `default_vals` {dict}
            The default values to set on the obj.
        `obj` {dict}
            The object to assign default values to.

        Keyword Arguments
        -------------------------
        `arg_name` {type}
                arg_description

        Return {dict}
        ----------------------
        The obj with default values applied

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 12-09-2021 08:04:03
        `memberOf`: object_utils
        `version`: 1.0
        `method_name`: set_defaults
    '''
    for k, v in default_vals.items():
        if k not in obj:
            obj[k] = v
        # print(f"k: {k} - v: {v}")
    return obj

def keys_to_lower(dictionary):
    '''
        Converts all keys in a dictionary to lowercase.
    '''
    return {k.lower(): v for k, v in dictionary.items()}

def keys_to_list(data:dict)->list:
    '''
        return all keys in a dictionary as a list.

        ----------

        Arguments
        -------------------------
        `data` {dict}
            The dictionary to parse.

        Return {list|None}
        ----------------------
        A list of the keys in the dictionary.
        returns an empty list if it fails or a non-dictionary was provided.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 06-03-2022 07:49:21
        `memberOf`: objectUtils
        `version`: 1.0
        `method_name`: keys_to_list
        * @xxx [06-03-2022 07:50:27]: documentation for keys_to_list
    '''
    if isinstance(data,(dict)) is False:
        return []

    return list(data.keys())



def get_kwarg(key_name:_Union[list,str], default_val=False, value_type=None, **kwargs):
    '''
        Get a kwarg argument that optionally matches a type check or
        return the default value.

        ----------

        Arguments
        -------------------------
        `key_name` {list|string}
            The key name or a list of key names to search kwargs for.

        [`default_val`=False] {any}
            The default value to return if the key is not found or fails
            the type check (if provided.)

        [`value_type`=None] {any}
            The type or tuple of types.
            The kwarg value must match at least one of these.
            Leave as None to ignore type checking.
        `kwargs` {dict}
            The kwargs dictionary to search within.

        Return {any}
        ----------------------
        The value of the kwarg key if it is found.
        The default value if the key is not found or its value fails type checking.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 06-03-2022 08:33:36
        `memberOf`: objectUtils
        `version`: 1.0
        `method_name`: get_kwarg
        * @xxx [06-03-2022 08:38:33]: documentation for get_kwarg
    '''
    from utils.random_utils.rand_generation import gen_variations


    kwargs = keys_to_lower(kwargs)
    if isinstance(key_name, list) is False:
        key_name = [key_name]

    for name in key_name:
        # generate basic variations of the name
        varis = gen_variations(name)
        for v_name in varis:
            if v_name in kwargs:
                if value_type is not None:
                    if isinstance(kwargs[v_name], value_type) is True:
                        return kwargs[v_name]
                else:
                    return kwargs[v_name]
    return default_val

def get_arg(args:dict,key_name:_Union[list,str],default_val=False, value_type=None)->any:
    '''
        Get a key's value from a dictionary.

        ----------

        Arguments
        -------------------------
        `args` {dict}
            The dictionary to search within.

        `key_name` {str|list}
            The key or list of keys to search for.

        [`default_val`=False] {any}
            The value to return if the key is not found.

        [`value_type`=None] {any}
            The type the value should have. This can be a tuple of types.

        Return {any}
        ----------------------
        The key's value if it is found and matches the value_type (if provided.)
        The default value otherwise.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 06-02-2022 07:43:12
        `memberOf`: object_utils
        `version`: 1.0
        `method_name`: get_arg
        * @xxx [06-02-2022 07:46:35]: documentation for get_arg
    '''
    from utils.random_utils.rand_generation import gen_variations

    if isinstance(args,(dict)) is False:
        return default_val
    if len(args.keys()) == 0:
        return default_val

    args = keys_to_lower(args)
    # if defaults is not None:
    #     defaults = keys_to_lower(defaults)
    #     args = set_defaults(defaults,args)

    if isinstance(key_name, list) is False:
        key_name = [key_name]

    for name in key_name:
        # generate basic variations of the name
        varis = gen_variations(name)
        for v_name in varis:
            if v_name in args:
                if value_type is not None:
                    if isinstance(args[v_name], value_type) is True:
                        return args[v_name]
                else:
                    return args[v_name]
    return default_val

def get_unique_keys(obj, **kwargs):
    '''
        Gets all unique keys in the object provided.

        @param {dict|list} obj - The object or list to search for keys within.
        @param {boolean} [**sort_list=True] - Sort the list alphabetically.
        @param {boolean} [**case_sensitive=True] - If True the case of the key is ignored.
        @param {boolean} [**force_lowercase=True] - Convert all keys to lowercase.
        @param {boolean} [**recursive=True] - Recurse into nested objects to find keys.
        @param {int} [**max_depth=500] - The maximum recursions it is allowed to make.
        @return {list} A list of unique keys from the object, if none are found the list is empty.
        @function get_unique_keys
    '''

    __current_depth = get_kwarg(['__current_depth'], 0, int, **kwargs)
    sort_list = get_kwarg(['sort_list'], False, bool, **kwargs)
    case_sensitive = get_kwarg(['case_sensitive'], True, bool, **kwargs)
    force_lowercase = get_kwarg(['force_lowercase'], True, bool, **kwargs)
    recursive = get_kwarg(['recursive'], True, bool, **kwargs)
    max_depth = get_kwarg(['max_depth'], 500, int, **kwargs)
    kwargs['__current_depth'] = __current_depth + 1

    keys = []

    if recursive is True and __current_depth < max_depth:
        if isinstance(obj, (list, tuple, set)):
            for element in obj:
                if isinstance(element, (list, dict)):
                    keys = keys + get_unique_keys(element, **kwargs)

    if isinstance(obj, dict):
        keys = list(obj.keys())

        if recursive is True and __current_depth < max_depth:
            # pylint: disable=unused-variable
            for k, value in obj.items():
                # find nested objects
                if isinstance(value, (list, dict, tuple, set)):
                    keys = keys + get_unique_keys(value, **kwargs)

    if case_sensitive is True:
        output = []
        lkkeys = []
        for key in keys:
            low_key = key.lower()
            if low_key not in lkkeys:
                output.append(key)
                lkkeys.append(low_key)
        keys = output

    if force_lowercase is True:
        keys = [x.lower() for x in keys]

    keys = list(set(keys))

    if sort_list is True:
        keys = sorted(keys, key=lambda x: int("".join([i for i in x if i.isdigit()])))
    return keys

def has_keys(data:dict,keys:list,**kwargs):
    '''
        confirm that a dictionary has all keys in the key list.

        ----------

        Arguments
        -------------------------
        `data` {dict}
            The dictionary to validate.

        `keys` {list}
            A list of keys that the data dict must contain.

        Keyword Arguments
        -------------------------
        [`message_template`=None] {str}
            The message to print to the console log if a key is missing.
            The string __KEY__ will be replaced with the missing key name.

        Return {bool}
        ----------------------
        True if the dict contains all the keys, False otherwise.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 06-03-2022 09:15:17
        `memberOf`: object_utils
        `version`: 1.0
        `method_name`: has_keys
        * @xxx [06-03-2022 09:18:47]: documentation for has_keys
    '''


    message_template = get_kwarg(['message_template'], None, (str), **kwargs)
    missing_keys = []
    keys = _lu.force_list(keys)
    for k in keys:
        if k not in data:
            if message_template is not None:
                msg = message_template.replace("__KEY__",k)
                print(_Fore.RED + msg + _Style.RESET_ALL)
            missing_keys.append(k)
    if len(missing_keys) > 0:
        return False
    return True

def remove_keys(data:dict,keys:_Union[list,str],**kwargs)->dict:
    '''
        Remove matching keys from a dictionary or keep only the matching keys.

        ----------

        Arguments
        -------------------------
        `data` {dict}
            The dictionary to filter.

        `keys` {list|str}
            A key or list of keys that will be removed from the dictionary.

        Keyword Arguments
        -------------------------
        [`reverse`=False] {bool}
            If True, all keys except the ones provided will be removed.

        Return {dict}
        ----------------------
        The dict with keys filtered.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 06-04-2022 10:15:45
        `memberOf`: dict_utils
        `version`: 1.0
        `method_name`: remove_keys
        * @xxx [06-04-2022 10:23:17]: documentation for remove_keys
    '''
    reverse = get_kwarg(['reverse'], False, (bool), **kwargs)
    keys = _lu.force_list(keys)


    output = {}
    for k,v in data.items():
        if reverse is True:
            if k in keys:
                output[k] = v
        else:
            if k not in keys:
                output[k] = v

    return output
