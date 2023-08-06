# '''
#     A module of utility methods used for formatting strings.

#     ----------

#     Meta
#     ----------
#     `author`: Colemen Atwood
#     `created`: 12-09-2021 09:00:27
#     `memberOf`: string_conversion
#     `version`: 1.0
#     `method_name`: string_conversion
# '''


# # import json
# # import hashlib
# import logging
# from typing import Union
# import re
# import os
# import urllib.parse
# import utils.object_utils as obj

# logger = logging.getLogger(__name__)



# def to_pascal_case(subject:str,first_char_lower=False,first_char_alpha=True)->str:
#     '''
#         Convert a string to PascalCase.

#         ----------

#         Arguments
#         -------------------------
#         `subject` {str}
#             The string to format to PascalCase

#         [`first_char_lower`=False] {bool}
#             If True the first charact will be lower case, essentially making it camelCase.

#         [`first_char_alpha`=True] {bool}
#             If True, any leading not alphabetic characters are stripped.

#         Return {str}
#         ----------------------
#         The string formatted as PascalCase

#         Meta
#         ----------
#         `author`: Colemen Atwood
#         `created`: 06-03-2022 09:23:01
#         `memberOf`: string_format
#         `version`: 1.0
#         `method_name`: to_pascal_case
#         * @xxx [06-03-2022 09:26:00]: documentation for to_pascal_case
#     '''


#     subject = re.sub(r'[^a-zA-Z0-9_\s]', ' ', subject)

#     subject = to_snake_case(subject)
#     subject = re.sub(r'([a-zA-Z0-9])([a-zA-Z0-9]*)', lambda x: x.group(1).upper() + x.group(2).lower(), subject)

#     if first_char_alpha:
#         subject = re.sub(r'^[^a-zA-Z]*', r'', subject)
#     else:
#         first_char_lower=False
#     subject = re.sub(r'_', '', subject)

#     if first_char_lower:
#         subject = re.sub(r'^([A-Za-z])', lambda x: x.group(1).upper(), subject)

#     return subject

# def to_camel_case(subject:str,first_char_lower=True,first_char_alpha=True)->str:
#     '''
#         Convert a string to camelCase.

#         ----------

#         Arguments
#         -------------------------
#         `subject` {str}
#             The string to format to camelCase

#         [`first_char_lower`=True] {bool}
#             If True the first charact will be lower case.

#         [`first_char_alpha`=True] {bool}
#             If True, any leading not alphabetic characters are stripped.

#         Return {str}
#         ----------------------
#         The string formatted as camelCase

#         Meta
#         ----------
#         `author`: Colemen Atwood
#         `created`: 06-03-2022 09:23:01
#         `memberOf`: string_format
#         `version`: 1.0
#         `method_name`: to_camel_case
#         * @xxx [06-03-2022 09:26:00]: documentation for to_camel_case
#     '''
#     subject = re.sub(r'[^a-zA-Z0-9_\s]', ' ', subject)

#     subject = to_snake_case(subject)
#     subject = re.sub(r'([a-zA-Z0-9])([a-zA-Z0-9]*)', lambda x: x.group(1).upper() + x.group(2).lower(), subject)

#     if first_char_alpha:
#         subject = re.sub(r'^[^a-zA-Z]*', r'', subject)
#     else:
#         first_char_lower=False
#     subject = re.sub(r'_', '', subject)

#     if first_char_lower:
#         subject = re.sub(r'^([A-Za-z])', lambda x: x.group(1).lower(), subject)

#     return subject

# def to_snake_case(subject:str,first_char_alpha=False)->str:
#     '''
#         Convert a subject to snake_case.

#         ----------

#         Arguments
#         -----------------
#         `subject` {str}
#             The subject to convert

#         [`first_char_alpha`=False] {bool}
#             If True any leading non-alphabetic characters will be removed.

#         Return
#         ----------
#         `return` {str}
#             The subject converted to snake_case

#         Example
#         ----------
#         BeepBoop Bleep blorp => beep_boop_bleep_blorp
#     '''
#     subject = str(subject)

#     if first_char_alpha:
#         subject = re.sub(r'^[^a-zA-Z]*',"",subject)

#     subject = re.sub(r'[^a-zA-Z0-9_\s]'," ",subject)
#     subject = re.sub(r'(\s|_)+',"_",subject)
#     subject = re.sub(r'([a-z])(?:\s|_)?([A-Z])',r"\1_\2",subject)
#     return subject.lower()

# def to_screaming_snake(subject:str):
#     '''
#         Convert a subject to SCREAMING_SNAKE_CASE.

#         ----------

#         Arguments
#         -----------------
#         `subject` {str}
#             The subject to convert

#         Return
#         ----------
#         `return` {str}
#             The subject converted to SCREAMING_SNAKE_CASE

#         Example
#         ----------
#         BeepBoop Bleep blorp => BEEP_BOOP_BLEEP_BLORP
#     '''

#     return to_snake_case(subject).upper()

# def to_kebab_case(subject:str)->str:
#     '''
#         Convert a string to kebab-case

#         ----------

#         Arguments
#         -------------------------
#         `subject` {str}
#             The string to convert to kebab-case.

#         Return {str}
#         ----------------------
#         The string in kebab-case.

#         Meta
#         ----------
#         `author`: Colemen Atwood
#         `created`: 06-03-2022 09:30:05
#         `memberOf`: string_format
#         `version`: 1.0
#         `method_name`: to_kebab_case
#         * @xxx [06-03-2022 09:30:57]: documentation for to_kebab_case
#     '''


#     subject = to_snake_case(subject)
#     return subject.replace("_","-")

# def to_dot_notation(subject:str)->str:
#     '''
#         Convert a string to dot.notation

#         ----------

#         Arguments
#         -------------------------
#         `subject` {str}
#             The string to convert to dot.notation


#         Return {str}
#         ----------------------
#         The string converted to dot.notation.

#         Meta
#         ----------
#         `author`: Colemen Atwood
#         `created`: 06-03-2022 09:31:04
#         `memberOf`: string_format
#         `version`: 1.0
#         `method_name`: to_dot_notation
#         * @xxx [06-03-2022 09:31:45]: documentation for to_dot_notation
#     '''


#     subject = to_snake_case(subject)
#     dotted = subject.replace("_",".")
#     output = re.sub(r'^\.*','',dotted)
#     return output

# def to_title_case(value:str,reverse=False)->str:
#     '''
#         Convert A String To Title Case.

#         ----------

#         Arguments
#         -------------------------
#         `value` {str}
#             The string to convert to Title Case
#         [`reverse`=False] {bool}
#             If True, all letters except for the first of each word will be capitalized.

#         Return {str}
#         ----------------------
#         The string in Title Case

#         Meta
#         ----------
#         `author`: Colemen Atwood
#         `created`: 06-03-2022 09:38:23
#         `memberOf`: string_format
#         `version`: 1.0
#         `method_name`: title_case
#         * @xxx [06-03-2022 09:39:51]: documentation for title_case
#     '''


#     orig_type = 'list'
#     if isinstance(value,(str)):
#         orig_type = 'string'
#         value = [value]
#     result = []
#     if reverse is True:
#         result = to_reverse_title_case(value)
#     else:
#         for word in value:
#             result.append(word.title())

#     if orig_type == 'list':
#         return result
#     if orig_type == 'string' and len(result) == 1:
#         return result[0]
#     else:
#         return result

# def to_reverse_title_case(value:str)->str:
#     '''
#         fORMAT a sTRING tO rEVERSE tITLE cASE.

#         ----------

#         Arguments
#         -------------------------
#         `value` {str}
#             The string to format to rEVERSE tITLE cASE

#         Return {str}
#         ----------------------
#         The string formatted to rEVERSE tITLE cASE

#         Meta
#         ----------
#         `author`: Colemen Atwood
#         `created`: 06-03-2022 09:40:53
#         `memberOf`: string_format
#         `version`: 1.0
#         `method_name`: reverse_title_case
#         * @xxx [06-03-2022 09:42:31]: documentation for reverse_title_case
#     '''


#     orig_type = 'list'

#     if isinstance(value,(str)):
#         orig_type = 'string'
#         value = [value]

#     result = []
#     for word in value:
#         lower = word.lower()
#         upper = word.upper()
#         result.append(f"{lower[0]}{upper[1:]}")

#     if orig_type == 'list':
#         return result
#     if orig_type == 'string' and len(result) == 1:
#         return result[0]
#     else:
#         return result





# def limit_length(subject, max_len=2, from_beginning=True):
#     '''
#         Limits the subject's character count to the max_len.

#         ----------

#         Arguments
#         -------------------------
#         `subject` {str}
#             The subject to convert
#         `max_len` {int}
#             The maximum length of the subject, if >= max_len the subject will not be padded.

#         [`limit_length`=False] {bool}
#             If True the subject will have excess characters removed from the beginning or end.
#         [`from_beginning`=True] {bool}
#             If True the subject will have excess characters removed from the beginning.\n
#             If False the subject will have excess characters removed from the end.

#         Return {str}
#         ----------------------
#         The formatted string

#         Meta
#         ----------
#         `author`: Colemen Atwood
#         `created`: 12-20-2021 14:48:31
#         `memberOf`: string_format
#         `version`: 1.0
#         `method_name`: limit_length
#     '''
#     subject = str(subject)
#     slen = len(subject)
#     if slen <= max_len:
#         return subject
#     else:
#         if from_beginning is True:
#             return subject[:max_len]
#         if from_beginning is False:
#             return subject[max_len:]


# def leftPad(subject, max_len=2, pad_char='0', limit_len=False, from_beginning=True):
#     '''
#         Convert a subject to snake_case.

#         ----------
#         Arguments
#         -----------------
#         `subject` {str}
#             The subject to convert
#         `max_len` {int}
#             The maximum length of the subject, if >= max_len the subject will not be padded.
#         `pad_char` {str}
#             The character to pad the subject with

#         [`limit_len`=False] {bool}
#             If True the subject will have excess characters removed from the beginning or end.

#         [`from_beginning`=True] {bool}
#             If True the subject will have excess characters removed from the beginning.\n
#             If False the subject will have excess characters removed from the end.
#         Return
#         ----------
#         `return` {str}
#             The subject formatted with left padding

#         Example
#         ----------
#         leftPad("1",5,'0') // "00001"
#         leftPad("/esls_test/server_source/TEST.scss",15,' ',True,True) // "/esls_test/serv"
#         leftPad("/e/TEST.scss",15,' ',True,False) // "   /e/TEST.scss"
#     '''
#     if limit_len is True:
#         subject = limit_length(subject, max_len, from_beginning)
#     subject = str(subject)
#     slen = len(subject)
#     if slen <= max_len:
#         subject = f"{pad_char * (max_len - slen)}{subject}"
#     return subject


# def rightPad(subject, max_len=2, pad_char='0'):
#     '''
#         Convert a subject to snake_case.

#         ----------
#         Arguments
#         -----------------
#         `subject` {subject}
#             The subject to convert
#         `max_len` {int}
#             The maximum length of the subject, if >= max_len the subject will not be padded.
#         `pad_char` {subject}
#             The character to pad the subject with
#         Return
#         ----------
#         `return` {subject}
#             The subject formatted with left padding

#         Example
#         ----------
#         leftPad("1",5,'0') // "00001"
#     '''
#     subject = str(subject)
#     slen = len(subject)
#     if slen <= max_len:
#         subject = f"{subject}{pad_char * (max_len - slen)}"
#     return subject


# def encode_quotes(value:str)->str:
#     '''
#         Encodes single and double quotes within the value to &apos; or &quot; respectively.

#         ----------

#         Arguments
#         -------------------------
#         `value` {str}
#             The string to encode

#         Return {str}
#         ----------------------
#         The encoded string.

#         Meta
#         ----------
#         `author`: Colemen Atwood
#         `created`: 12-09-2021 08:15:52
#         `memberOf`: string_format
#         `version`: 1.0
#         `method_name`: encode_quotes
#     '''
#     value = value.replace("'", "&apos;")
#     value = value.replace('"', "&quot;")
#     return value


# def decode_quotes(value:str)->str:
#     '''
#         Decodes single and double quotes within the value from &apos; or &quot; respectively.

#         ----------

#         Arguments
#         -------------------------
#         `value` {str}
#             The string to decode

#         Return {str}
#         ----------------------
#         The decoded string.

#         Meta
#         ----------
#         `author`: Colemen Atwood
#         `created`: 12-09-2021 08:15:52
#         `memberOf`: string_format
#         `version`: 1.0
#         `method_name`: encode_quotes
#     '''
#     value = value.replace("&apos;", "'")
#     value = value.replace("&quot;", '"')
#     return value


# def strip_excessive_spaces(value:str)->str:
#     '''
#         Removes excessive (2 or more consecutive) spaces from the string.

#         ----------

#         Arguments
#         -------------------------
#         `value` {str}
#             The string to format.

#         Return {str}
#         ----------------------
#         The formatted string

#         Meta
#         ----------
#         `author`: Colemen Atwood
#         `created`: 12-09-2021 08:19:28
#         `memberOf`: string_format
#         `version`: 1.0
#         `method_name`: strip_excessive_spaces
#     '''
#     return re.sub(r'[\s\s]{2,}', ' ', value)


# def strip_excessive_chars(value:str,chars:Union[str,list])->str:
#     '''
#         Removes excessive (2 or more consecutive) chars from the string.

#         ----------

#         Arguments
#         -------------------------
#         `value` {str}
#             The string to format.
#         `chars` {str|list}
#             The chars to remove if they occur excessively.

#         Return {str}
#         ----------------------
#         The formatted string

#         Meta
#         ----------
#         `author`: Colemen Atwood
#         `created`: 06-03-2022 11:47:37
#         `memberOf`: string_format
#         `version`: 1.0
#         `method_name`: strip_excessive_chars
#     '''
#     if isinstance(chars,(str)):
#         chars = [chars]
#     for c in chars:
#         if c == " ":
#             c = "\\s"
#         reg_c = escape_regex(c)
#         exp = rf"[{reg_c}]{{2,}}"
#         # print(exp)
#         reg = re.compile(exp)
#         value = re.sub(reg, c, value)
#     return value


# def escape_regex(value:str)->str:
#     '''
#         Escapes regex special characters.

#         ----------

#         Arguments
#         -------------------------
#         `value` {str}
#             The string to escape.

#         Return {str}
#         ----------------------
#         The formatted string.

#         Meta
#         ----------
#         `author`: Colemen Atwood
#         `created`: 12-09-2021 08:46:32
#         `memberOf`: string_format
#         `version`: 1.0
#         `method_name`: escape_regex
#     '''
#     regex_chars = ["\\", "^", "$", "{", "}", "[", "]", "(", ")", ".", "*", "+", "?", "<", ">", "-", "&"]
#     for char in regex_chars:
#         value = value.replace(char, f"\\{char}")
#     return value

# def strip_any(value,chars,side='both'):
#     '''
#         Strips characters/strings from the beginning,end or both sides of a string.

#         ----------

#         Arguments
#         -------------------------
#         `value` {str}
#             The value to be formatted
#         `chars` {list}
#             A list of strings to be stripped from the value
#         [`side`='both'] {str}
#             Can be "left", "right", "both"

#         Return {str}
#         ----------------------
#         The formatted value.

#         Meta
#         ----------
#         `author`: Colemen Atwood
#         `created`: 02-04-2022 10:25:04
#         `memberOf`: string_format
#         `version`: 1.0
#         `method_name`: strip_any
#     '''
#     new_value = value
#     cycle = True
#     if side in ["both","left"]:
#         cycle = True
#         while cycle is True:
#             matchFound = False
#             for char in chars:
#                 if new_value.startswith(char):
#                     new_value = new_value[len(char):]
#                     matchFound = True
#                 else:
#                     continue
#             if matchFound is False:
#                 cycle = False
#     if side in ["both","right"]:
#         cycle = True
#         while cycle is True:
#             matchFound = False
#             for char in chars:
#                 if new_value.endswith(char):
#                     new_value = new_value[:-len(char)]
#                     matchFound = True
#                 else:
#                     continue
#             if matchFound is False:
#                 cycle = False
#     return new_value



# def strip_end(text, suffix):
#     if suffix and text.endswith(suffix):
#         return text[:-len(suffix)]
#     return text


# def windows_file_name(file_name:str)->str:
#     '''
#         Strips (window's) invalid characters from the file_name.\n
#         These characters are removed:\n
#         <>:"/\\|?*

#         ----------

#         Arguments
#         -------------------------
#         `file_name` {str}
#             The string to be parsed.

#         Return {str}
#         ----------------------
#             The parsed string

#         Meta
#         ----------
#         `author`: Colemen Atwood
#         `created`: 12-19-2021 13:32:36
#         `memberOf`: string_format
#         `version`: 1.0
#         `method_name`: windows_file_name
#     '''
#     return re.sub(r'[<>:"/\|?*]*', "", file_name)


# def extension(string:Union[str,list])->Union[str,list]:
#     '''
#         Formats a file extension to have no leading period.

#         ----------

#         Arguments
#         -------------------------
#         `value` {str|list}
#             The file extension(s) [separated by commas] or list of extensions to format

#         Keyword Arguments
#         -------------------------
#         `arg_name` {type}
#                 arg_description

#         Return {str}
#         ----------------------
#         The formatted file extension

#         Meta
#         ----------
#         `author`: Colemen Atwood
#         `created`: 12-19-2021 13:33:51
#         `memberOf`: string_format
#         `version`: 1.0
#         `method_name`: extension
#     '''
#     new_ext_array = []
#     if isinstance(string,(str)):
#         if "," in string:
#             string = string.split(",")
#     if isinstance(string, list) is False:
#         string = [string]

#     for ext in string:
#         # print(f"ext: {ext}")
#         ext = ext.lower()
#         ext = re.sub(r"^\.*", '', ext)
#         new_ext_array.append(ext)

#     if len(new_ext_array) > 1:
#         new_ext_array = list(set(new_ext_array))
#     if len(new_ext_array) == 1:
#         return new_ext_array[0]
#     return new_ext_array
# format_extension = extension

# def file_path(value:str, **kwargs)->str:
#     '''
#         Formats the path for use in windows.

#         ----------

#         Arguments
#         -------------------------
#         `value` {str}
#             The file path to format.

#         Keyword Arguments
#         -------------------------
#         [`strip_trailing_separator`=True] {bool}
#             if False, the path is allowed to end with a trailing separator.

#         [`escape_spaces`=False] {bool}
#             if True, any segments of the path that contains a space is wrapped in quotes.

#         [`url`=False] {bool}
#             if True, the path seperator is set to "/" regardless of the os settings.

#         [`url_encode`=False] {bool}
#             If True the url is has all special characters encoded.

#         [`url_decode`=False] {bool}
#             If True the url is has all special characters decoded.


#         Return {str}
#         ----------------------
#         The formatted file path.

#         Meta
#         ----------
#         `author`: Colemen Atwood
#         `created`: 12-09-2021 08:45:08
#         `memberOf`: string_format
#         `version`: 1.0
#         `method_name`: file_path
#     '''
#     strip_trailing_separator = obj.get_kwarg(["strip_trailing_separator"], True, (bool), **kwargs)
#     treat_as_url = obj.get_kwarg(["url"], False, (bool), **kwargs)
#     escape_spaces = obj.get_kwarg(["escape spaces"], False, (bool), **kwargs)
#     path_sep = escape_regex(os.path.sep)
#     if treat_as_url is True:
#         return url(value, **kwargs)
#     # print(f"path_sep: {path_sep}")
#     value = re.sub(r'(\\|\/)', path_sep, value)
#     regex = re.compile(rf'{path_sep}+')
#     value = re.sub(regex, path_sep, value)
#     # only clean the path for non urls
#     if len(value) > 250:
#         # print(f"clean path: ",value)
#         value = clean_path(value)
#         # print(f"clean path: ",value)
#     if escape_spaces:
#         path_array = value.split(os.path.sep)
#         new_path_array = []
#         for seg in path_array:
#             seg_string = seg
#             if " " in seg_string:
#                 seg_string = f'"{seg_string}"'
#             new_path_array.append(seg_string)
#         value = path_sep.join(new_path_array)
#     if strip_trailing_separator is True:
#         value = strip_end(value, path_sep)
#     return value


# def url(value:str, **kwargs)->str:
#     '''
#         Formats a url string

#         ----------

#         Arguments
#         -------------------------
#         `value` {str}
#             The url to format

#         Keyword Arguments
#         -------------------------
#         [`encode`=False] {bool}
#             If True the url is has all special characters encoded.

#         [`decode`=False] {bool}
#             If True the url is has all special characters decoded.

#         [`strip_trailing_separator`=True] {bool}
#             if False, the path is allowed to end with a trailing separator.

#         Return {str}
#         ----------------------
#         The formatted url

#         Meta
#         ----------
#         `author`: Colemen Atwood
#         `created`: 12-17-2021 14:28:23
#         `memberOf`: string_format
#         `version`: 1.0
#         `method_name`: url
#     '''
#     strip_trailing_separator = obj.get_kwarg(["strip_trailing_separator"], True, (bool), **kwargs)
#     encode = obj.get_kwarg(["encode", "url_encode"], False, (bool), **kwargs)
#     decode = obj.get_kwarg(["decode", "url_decode"], False, (bool), **kwargs)
#     path_sep = "/"
#     value = re.sub(r'(\\|\/)', path_sep, value)
#     regex = re.compile(rf'{path_sep}+')
#     value = re.sub(regex, path_sep, value)
#     if encode is True:
#         value = urllib.parse.quote(value)
#     if decode is True:
#         value = urllib.parse.unquote(value)

#     if strip_trailing_separator is True:
#         value = strip_end(value, path_sep)

#     return value


# def clean_path(path):
#     path = path.replace('/', os.sep).replace('\\', os.sep)
#     path = re.sub(r'^[\\\?]*','',path)
#     if os.sep == '\\' and '\\\\?\\' not in path:
#         # fix for Windows 260 char limit
#         relative_levels = len([directory for directory in path.split(os.sep) if directory == '..'])
#         cwd = [directory for directory in os.getcwd().split(os.sep)] if ':' not in path else []
#         path = '\\\\?\\' + os.sep.join(cwd[:len(cwd)-relative_levels] + [directory for directory in path.split(os.sep) if directory != ''][relative_levels:])
#         # path = path.replace("\\\\?\\?\\","\\\\?\\")
#     path = path.replace("\\\\?\\?\\","\\\\?\\")
#     return path
# # \\?\?\Z:\Structure\Ra9\2021\21-0132 - EquariUI\EquariUI\EquariUI Beta\equari-beta\node_modules\equari-cryptadia-core\node_modules\preact-router\match\node_modules\.cache\.rts2_cache_cjs\rpt2_73e3afccd1fb4711c5e0a2849dd91b2323492db2\types\cache\0e26fd72fe37b4bfe0d3c7edcd1abb1561780380
# # test_path = r"\\?\?\Z:\Structure\Ra9\2021\21-0132 - EquariUI\EquariUI\EquariUI Beta\equari-beta\node_modules\equari-cryptadia-core\node_modules\preact-router\match\node_modules\.cache\.rts2_cache_cjs\rpt2_73e3afccd1fb4711c5e0a2849dd91b2323492db2\types\cache\0e26fd72fe37b4bfe0d3c7edcd1abb1561780380"
# # print(file_path(test_path))


# def strip_empty_lines(value:str)->str:
#     '''
#         Strip empty lines from the value.

#         ----------

#         Arguments
#         -------------------------
#         `value` {str}
#             The string to strip empty lines from.

#         Return {str}
#         ----------------------
#         The string with empty lines removed.

#         Meta
#         ----------
#         `author`: Colemen Atwood
#         `created`: 06-03-2022 09:42:38
#         `memberOf`: string_format
#         `version`: 1.0
#         `method_name`: strip_empty_lines
#         * @xxx [06-03-2022 09:43:29]: documentation for strip_empty_lines
#     '''


#     lines = value.split("\n")
#     new_lines = [x for x in lines if len(x) > 0]
#     return '\n'.join(new_lines)



# def reverse_sanitize_quotes(string):
#     orig_list = False
#     if isinstance(string, (list)):
#         orig_list = True
#     if isinstance(string, (str)):
#         string = [string]

#     new_list = []
#     for item in string:
#         item = item.replace("&apos_", "'")
#         item = item.replace("&quot_", '"')
#         new_list.append(item)

#     if len(new_list) == 1 and orig_list is False:
#         return new_list[0]

#     return new_list

# def sanitize_quotes(string):
#     orig_list = False
#     if isinstance(string, (list)):
#         orig_list = True
#     if isinstance(string, (str)):
#         string = [string]

#     new_list = []
#     for item in string:
#         if isinstance(item, (str)):
#             item = item.replace("'", "&apos_")
#             item = item.replace('"', "&quot_")
#         new_list.append(item)

#     if len(new_list) == 1 and orig_list is False:
#         return new_list[0]

#     return new_list





# def array_in_string(array, value, default=False):
#     '''
#         iterates the array provided checking if any element exists in the value.

#         ----------

#         Arguments
#         -------------------------
#         `array` {list}
#             The list of terms to search for in the value.
#         `value` {str}
#             The string to search within
#         [`default`=False] {mixed}
#             The default value to return if no match is found.

#         Return {mixed}
#         ----------------------
#         True if a match is found, returns the default value otherwise.

#         Meta
#         ----------
#         `author`: Colemen Atwood
#         `created`: 12-19-2021 13:54:36
#         `memberOf`: parse_utils
#         `version`: 1.0
#         `method_name`: array_in_string
#     '''
#     if len(array) == 0:
#         return default
#     if isinstance(value, (str)) is False:
#         logger.warning('Second argument of array_in_string, must be a string.')
#         logger.warning(value)
#         return default
#     for item in array:
#         if item in value:
#             return True
#     return default

# def array_replace_string(value,needles, new_string="", **kwargs):
#     '''
#         Replaces any matching substrings found in the needles list with new_string.

#         ----------

#         Arguments
#         -------------------------
#         `value` {str}
#             The string that will be modified.

#         `needles` {list}
#             A list of strings to replace in the the value

#         [`new_string`=""] {str}
#             What the needle will be replaced with in the value


#         Keyword Arguments
#         -------------------------
#         `max_replace` {int}
#             The maximum number of replacements to make.
#             if <= 0, it will find and replace all elements in the array.

#         Return {str}
#         ----------------------
#         The formatted string.

#         Meta
#         ----------
#         `author`: Colemen Atwood
#         `created`: 01-06-2022 10:36:28
#         `memberOf`: parse_utils
#         `version`: 1.0
#         `method_name`: array_replace_string
#     '''
#     max_replace = obj.get_kwarg(['max','max replace'],0,(int),**kwargs)
#     if len(needles) == 0:
#         return value

#     if isinstance(value, (str)) is False:
#         logger.warning('value must be a string.')
#         logger.warning(value)

#     replace_count = 0
#     result_string = value
#     for needle in needles:
#         if needle in value:
#             replace_count += 1
#             result_string = result_string.replace(needle,new_string)
#             if max_replace > 0:
#                 if replace_count >= max_replace:
#                     return result_string

#     return result_string









# # ----------========== ALIASES ==========----------
# left_pad = leftPad

