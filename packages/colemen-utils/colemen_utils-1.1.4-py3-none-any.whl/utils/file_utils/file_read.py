# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
'''
    Utility methods for reading files.
'''


import json
import os
import re
import io
import gzip

import utils.dict_utils as obj

# from utils.dict_utils.dict_utils import get_kwarg as obj.get_kwarg
from utils.string_utils.string_format import file_path as _format_file_path


def read(file_path, **kwargs):
    '''
        reads a file.

        @param {string} file_path - The path to the file to read.
        @param {boolean} [**json] - Read the file as json
        @param {boolean} [**array] - Read the file into an array of lines.
        @param {boolean} [**data_array] - Read the file into an array of line data dictionaries.

    '''
    as_type = obj.get_kwarg(['as', 'as type'], [], (list, str), **kwargs)
    if isinstance(as_type, (str)):
        as_type = [as_type]
    read_as_json = obj.get_kwarg(['json', 'as json'], False, bool, **kwargs)
    read_to_array = obj.get_kwarg(['array', 'to_array'], False, bool, **kwargs)
    read_to_data_array = obj.get_kwarg(['data_array'], False, bool, **kwargs)
    # data_array = obj.get_kwarg(['data array'], False, bool, **kwargs)

    if read_as_json is True:
        return as_json(file_path)

    if read_to_array is True:
        return to_array(file_path)

    if read_to_data_array is True:
        return data_array(file_path)

    if "duf" in as_type:
        return duf(file_path)

    if if_file_exists(file_path) is True:
        with open(file_path, 'r', encoding='utf-8') as file:
            try:
                return file.read()
            except UnicodeDecodeError:
                print(f"read_file - file_path UnicodeDecodeError: {file_path}")
    else:
        print(f"read_file - file_path does not exist: {file_path}")
        return False


def to_array(file_path):
    '''
        Reads a file into an array with each indice being one line.
    '''
    if if_file_exists(file_path) is True:
        with open(file_path, 'r', encoding='utf-8') as file:
            try:
                file_array = file.read().splitlines()
                return file_array
            except UnicodeDecodeError:
                print(f"UnicodeDecodeError - file_path: {file_path}")
    return False


def as_json(file_path):
    '''
        Read a json file into a dictionary.
        strips all comments from file before reading.
    '''
    file_path = _format_file_path(file_path)
    if if_file_exists(file_path) is True:
        file_path = file_path.replace("\\", "/")
        file_contents = __parse_json_comments(file_path)
        try:
            return json.loads(file_contents)
        except json.decoder.JSONDecodeError as error:
            error_message = str(error)
            if "decode using utf-8-sig" in error_message:
                decoded_data = file_contents.encode().decode('utf-8-sig')
                return json.loads(decoded_data)

            # json.decoder.JSONDecodeError: Unexpected UTF-8 BOM(decode using utf-8-sig)
    return False


def __parse_json_comments(file_path):
    '''
        strips comments from a json file.

        @return The contents of the file as a string.
    '''
    file_array = data_array(file_path)
    output_array = []
    for file in file_array:
        match = re.search(r'^\s*\/\/', file['raw_content'])
        if match is None:
            output_array.append(file)
    return file_content_data_to_string(output_array)


def data_array(file_path):
    final_data = []
    file_content = to_array(file_path)
    for i, line in enumerate(file_content):
        data = {}
        data['line_number'] = i
        data['raw_content'] = line
        final_data.append(data)
    return final_data


def file_content_data_to_string(file_content, **kwargs):
    """Takes an array of file content and returns the raw_content as a string"""

    strip_empty_lines = False
    if 'STRIP_EMPTY_LINES' in kwargs:
        strip_empty_lines = kwargs['STRIP_EMPTY_LINES']

    final_string = ""
    if isinstance(file_content, str):
        return file_content
    # print(f"-------file_content: {file_content}")
    for content in file_content:
        # print(f"x: {x}")
        if len(content['raw_content']) != 0 and strip_empty_lines is True or strip_empty_lines is False:
            final_string += f"{content['raw_content']}\n"
    return final_string


def if_file_exists(file_path):
    if os.path.isfile(file_path) is True:
        return True
    else:
        return False


def duf(file_path):
    contents = None
    if isinstance(file_path, (dict)):
        file_path = file_path['file_path']
    try:
        with gzip.open(file_path, 'rb') as stuff:
            with io.TextIOWrapper(stuff, encoding='utf-8') as decoder:
                # print(f"File is compressed. - {file_path}")
                contents = json.loads(decoder.read())
    except gzip.BadGzipFile:
        # print(f"File is not compressed. - {file_path}")
        contents = as_json(file_path)

    return contents
