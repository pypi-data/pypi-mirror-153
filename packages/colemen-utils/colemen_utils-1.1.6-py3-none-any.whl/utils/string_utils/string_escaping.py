'''
    A module of utility methods used for formatting strings.

    ----------

    Meta
    ----------
    `author`: Colemen Atwood
    `created`: 12-09-2021 09:00:27
    `memberOf`: string_utils
'''


# import json
# import hashlib
import logging as _logging
# from typing import Union as _Union
# import re as _re
# import os as _os
# import urllib.parse

import utils.dict_utils as _obj
from pyparsing import QuotedString
# from pyparsing import And, Suppress,Dict, Word, Literal, Group, Optional, ZeroOrMore, OneOrMore, Regex, restOfLine, alphanums,nums, printables, string, CaselessKeyword,nestedExpr,ParseException,quotedString,removeQuotes,originalTextFor,delimitedList,QuotedString

# from utils.dict_utils.dict_utils import get_kwarg as _obj.get_kwarg

logger = _logging.getLogger(__name__)

_numeric_char_codes = {
    "symbols":{
        ";":"&#59;",
        "#":"&#35;",
        "&":"&#38;",
        "!":"&#33;",
        "\"":"&#34;",
        "$":"&#36;",
        "%":"&#37;",
        "'":"&#39;",
        "(":"&#40;",
        ")":"&#41;",
        "*":"&#42;",
        "+":"&#43;",
        ",":"&#44;",
        "-":"&#45;",
        ".":"&#46;",
        "/":"&#47;",
        ":":"&#58;",
        "<":"&#60;",
        "=":"&#61;",
        ">":"&#62;",
        "?":"&#63;",
        "@":"&#64;",
        "[":"&#91;",
        "\\":"&#92;",
        "]":"&#93;",
        "^":"&#94;",
        "_":"&#95;",
        "`":"&#96;",
        "{":"&#123;",
        "|":"&#124;",
        "}":"&#125;",
        "~":"&#126;"
    },
    "numeric":{
        "0":"&#48;",
        "1":"&#49;",
        "2":"&#50;",
        "3":"&#51;",
        "4":"&#52;",
        "5":"&#53;",
        "6":"&#54;",
        "7":"&#55;",
        "8":"&#56;",
        "9":"&#57;"
    },
    "upper_case":{
        "A":"&#65;",
        "B":"&#66;",
        "C":"&#67;",
        "D":"&#68;",
        "E":"&#69;",
        "F":"&#70;",
        "G":"&#71;",
        "H":"&#72;",
        "I":"&#73;",
        "J":"&#74;",
        "K":"&#75;",
        "L":"&#76;",
        "M":"&#77;",
        "N":"&#78;",
        "O":"&#79;",
        "P":"&#80;",
        "Q":"&#81;",
        "R":"&#82;",
        "S":"&#83;",
        "T":"&#84;",
        "U":"&#85;",
        "V":"&#86;",
        "W":"&#87;",
        "X":"&#88;",
        "Y":"&#89;",
        "Z":"&#90;"
    },
    "lower_case":{

        "a":"&#97;",
        "b":"&#98;",
        "c":"&#99;",
        "d":"&#100;",
        "e":"&#101;",
        "f":"&#102;",
        "g":"&#103;",
        "h":"&#104;",
        "i":"&#105;",
        "j":"&#106;",
        "k":"&#107;",
        "l":"&#108;",
        "m":"&#109;",
        "n":"&#110;",
        "o":"&#111;",
        "p":"&#112;",
        "q":"&#113;",
        "r":"&#114;",
        "s":"&#115;",
        "t":"&#116;",
        "u":"&#117;",
        "v":"&#118;",
        "w":"&#119;",
        "x":"&#120;",
        "y":"&#121;",
        "z":"&#122;"
    }
}



def regex(value:str)->str:
    '''
        Escapes regex special characters.

        ----------

        Arguments
        -------------------------
        `value` {str}
            The string to escape.

        Return {str}
        ----------------------
        The formatted string.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 12-09-2021 08:46:32
        `memberOf`: string_format
        `version`: 1.0
        `method_name`: escape_regex
    '''
    regex_chars = ["\\", "^", "$", "{", "}", "[", "]", "(", ")", ".", "*", "+", "?", "<", ">", "-", "&"]
    for char in regex_chars:
        value = value.replace(char, f"\\{char}")
    return value
escape_regex = regex

def encode_quotes(value:str)->str:
    '''
        Encodes single and double quotes within the value to &apos; or &quot; respectively.

        ----------

        Arguments
        -------------------------
        `value` {str}
            The string to encode

        Return {str}
        ----------------------
        The encoded string.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 12-09-2021 08:15:52
        `memberOf`: string_format
        `version`: 1.0
        `method_name`: encode_quotes
    '''
    value = value.replace("'", "&apos;")
    value = value.replace('"', "&quot;")
    return value

def decode_quotes(value:str)->str:
    '''
        Decodes single and double quotes within the value from &apos; or &quot; respectively.

        ----------

        Arguments
        -------------------------
        `value` {str}
            The string to decode

        Return {str}
        ----------------------
        The decoded string.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 12-09-2021 08:15:52
        `memberOf`: string_format
        `version`: 1.0
        `method_name`: encode_quotes
    '''
    value = value.replace("&apos;", "'")
    value = value.replace("&quot;", '"')
    return value

def reverse_sanitize_quotes(string):
    orig_list = False
    if isinstance(string, (list)):
        orig_list = True
    if isinstance(string, (str)):
        string = [string]

    new_list = []
    for item in string:
        item = item.replace("&apos_", "'")
        item = item.replace("&quot_", '"')
        new_list.append(item)

    if len(new_list) == 1 and orig_list is False:
        return new_list[0]

    return new_list

def sanitize_quotes(string):
    orig_list = False
    if isinstance(string, (list)):
        orig_list = True
    if isinstance(string, (str)):
        string = [string]

    new_list = []
    for item in string:
        if isinstance(item, (str)):
            item = item.replace("'", "&apos_")
            item = item.replace('"', "&quot_")
        new_list.append(item)

    if len(new_list) == 1 and orig_list is False:
        return new_list[0]

    return new_list

def _get_numeric_charcode(char):
    for _,v in _numeric_char_codes.items():
        for c,code in v.items():
            if c == char:
                return code
    return None

def _get_numeric_charcode_chars(cat:str)->list:
    output = []
    if cat in _numeric_char_codes:
        for k,_ in _numeric_char_codes[cat].items():
            output.append(k)
    return output

def escape_charcode(value:str,reverse=False,**kwargs)->str:
    '''
        Escape character in a string with their character codes.

        ----------

        Arguments
        -------------------------
        `value` {str}
            The string to escape.

        [`reverse`=False] {bool}
            If True, it will unescape the charcoded characters.

        Keyword Arguments
        -------------------------
        `chars` {list|str}
            A list or string of characters to escape.

        [`symbols`=True] {bool}
            If True, all symbols will be escaped.

        [`numeric`=False] {bool}
            If True, all numeric will be escaped.

        [`upper_case`=False] {bool}
            If True, all upper_case will be escaped.

        [`lower_case`=False] {bool}
            If True, all lower_case will be escaped.

        Return {str}
        ----------------------
        The escaped string.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 06-04-2022 09:36:42
        `memberOf`: string_format
        `version`: 1.0
        `method_name`: escape_charcode
        * @xxx [06-04-2022 09:38:48]: documentation for escape_charcode
    '''

    if reverse is True:
        return charcode_unescape(value)

    chars = _obj.get_kwarg(["chars"], None, (list,str), **kwargs)
    symbols = _obj.get_kwarg(["symbols"], True, (bool), **kwargs)
    numeric = _obj.get_kwarg(["numeric"], False, (bool), **kwargs)
    upper_case = _obj.get_kwarg(["upper_case"], False, (bool), **kwargs)
    lower_case = _obj.get_kwarg(["lower_case"], False, (bool), **kwargs)

    if chars is not None:
        if isinstance(chars,(str)):
            chars = chars.split()
        for c in chars:
            code = _get_numeric_charcode(c)
            value = value.replace(c,code)
        return value

    chars = []

    if symbols is True:
        chars = chars + _get_numeric_charcode_chars('symbols')
    if numeric is True:
        chars = chars + _get_numeric_charcode_chars('numeric')
    if upper_case is True:
        chars = chars + _get_numeric_charcode_chars('upper_case')
    if lower_case is True:
        chars = chars + _get_numeric_charcode_chars('lower_case')

    for c in chars:
        code = _get_numeric_charcode(c)
        value = value.replace(c,code)

    return value
charcode = escape_charcode

def charcode_unescape(value:str)->str:
    '''
        Unescape the character codes from escape_charcode.

        ----------

        Arguments
        -------------------------
        `value` {str}
            The string to unescape.

        Return {str}
        ----------------------
        The unescaped string.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 06-04-2022 09:39:02
        `memberOf`: string_format
        `version`: 1.0
        `method_name`: charcode_unescape
        * @xxx [06-04-2022 09:39:50]: documentation for charcode_unescape
    '''

    for _,v in _numeric_char_codes.items():
        for c,code in v.items():
            value = value.replace(code,c)
    return value

def quoted_commas(value,escape_value="__ESCAPED_COMMA__",reverse=False):
    '''
        Escape commas that are located within quotes.

        ----------

        Arguments
        -------------------------
        `value` {str}
            The string to search within
        [`escape_value`='__ESCAPED_COMMA__] {str}
            The value to replace commas with.
        `reverse` {bool}
            if True it will replace the escaped commas with actual commas.

        Return {str}
        ----------------------
        The string with escaped commas.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 06-01-2022 06:54:48
        `memberOf`: parse_sql
        `version`: 1.0
        `method_name`: escape_quoted_commas
        @xxx [06-01-2022 06:57:45]: documentation for escape_quoted_commas
    '''

    if reverse is True:
        return value.replace(escape_value,",")

    sql_qs = QuotedString("'", esc_quote="''")
    quote = sql_qs.search_string(value)
    if len(quote) > 0:
        quote = quote.asList()
        for q in quote:
            if len(q) == 1:
                q = q[0]
            esc = q.replace(",",escape_value)
            value = value.replace(q,esc)

    return value
escape_quoted_commas = quoted_commas

def quoted_chars(value,reverse=False):
    '''
        Escape characters that can effect parsing which are located within quotes.

        ----------

        Arguments
        -------------------------
        `value` {str}
            The string to search within

        `reverse` {bool}
            if True it will reverse the escaped chars with their actual chars.

        Return {str}
        ----------------------
        The string with escaped chars.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 06-01-2022 06:54:48
        `memberOf`: parse_sql
        `version`: 1.0
        `method_name`: escape_quoted_chars
        @xxx [06-01-2022 06:57:45]: documentation for escape_quoted_chars
    '''

    escapes = [
        [",","__&#44__"],
        [";","__&#59__"],
        ["(","__&#40__"],
        [")","__&#41__"],
        ["`","__&#96__"],
        ['"',"__&#34__"],
        ["'","__&#39__"],
    ]


    if reverse is True:
        for e in escapes:
            value = value.replace(e[1],e[0])
        return value

    for e in escapes:
        sql_qs = QuotedString("'", esc_quote="''")
        quote = sql_qs.search_string(value)
        if len(quote) > 0:
            quote = quote.asList()
            # print(f"quote: {quote}")
            for q in quote:
                if len(q) == 1:
                    q = q[0]
                esc = q.replace(e[0],e[1])
                value = value.replace(q,esc)
    # print(sql_qs.search_string(value))
    return value
escape_quoted_chars = quoted_chars











