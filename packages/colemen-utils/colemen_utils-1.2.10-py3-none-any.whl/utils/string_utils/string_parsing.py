# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=line-too-long
# pylint: disable=unused-import

'''
    A module of utility methods used for parsing strings

    ----------

    Meta
    ----------
    `author`: Colemen Atwood
    `created`: 06-04-2022 10:44:23
    `memberOf`: string_utils
'''


# import json
# import hashlib
# import string
import re


def determine_gender(value:str)->str:
    '''
        Use synonyms to determine the gender of a word.

        ----------

        Arguments
        -------------------------
        `value` {str}
            The word to test

        Return {str|None}
        ----------------------
        Either "male", "female" or None

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 06-04-2022 09:00:38
        `memberOf`: string_parsing
        `version`: 1.0
        `method_name`: determine_gender
        * @xxx [06-04-2022 09:02:44]: documentation for determine_gender
    '''


    female_synonyms = ['girl','female','woman','lady','miss','chica','lass','chick','grandmother','grandma','mom','mother','daughter','wife']
    male_synonyms = ['boy','male','man','dude','guy','husband','bro','grandfather','grandpa','dad','father','brother']

    value = value.lower()
    if value in female_synonyms:
        return "female"
    if value in male_synonyms:
        return "male"
    return None
