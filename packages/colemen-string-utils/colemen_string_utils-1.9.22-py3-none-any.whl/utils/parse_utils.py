'''
    Module of string parsing methods.

    ----------

    Meta
    ----------
    `author`: Colemen Atwood
    `created`: 12-19-2021 13:57:27
    `memberOf`: parse_utils
    `version`: 1.0
    `method_name`: parse_utils
'''

# import json
# import hashlib
# import string

# import re
# import utils.objectUtils as objUtils
import logging
import utils.objectUtils as obj
import facades.sql_parse_facade as sql
logger = logging.getLogger(__name__)


BOOL_TRUE_SYNONYMS = ["TRUE", "true", "True", "yes", "y", "1"]
BOOL_FALSE_SYNONYMS = ["FALSE", "false", "False", "no", "n", "0"]
VALID_PYTHON_TYPES = {
    "str":["string","str"],
    "int":["integer","number","int"],
    "float":["float","double"],
    "list":["list","array"],
    "tuple":["tuple","set"],
    "set":["set"],
    "dict":["dictionary","dict"],
    "boolean":["boolean","boolean"]
}

def determine_boolean(value, def_val=None):
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

def array_in_string(array, value, default=False):
    '''
        iterates the array provided checking if any element exists in the value.

        ----------

        Arguments
        -------------------------
        `array` {list}
            The list of terms to search for in the value.
        `value` {str}
            The string to search within
        [`default`=False] {mixed}
            The default value to return if no match is found.

        Return {mixed}
        ----------------------
        True if a match is found, returns the default value otherwise.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 12-19-2021 13:54:36
        `memberOf`: parse_utils
        `version`: 1.0
        `method_name`: array_in_string
    '''
    if len(array) == 0:
        return default
    if isinstance(value, (str)) is False:
        logger.warning('Second argument of array_in_string, must be a string.')
        logger.warning(value)
        return default
    for item in array:
        if item in value:
            return True
    return default

def array_replace_string(value,needles, new_string="", **kwargs):
    '''
        Replaces any matching substrings found in the needles list with new_string.

        ----------

        Arguments
        -------------------------
        `value` {str}
            The string that will be modified.
            
        `needles` {list}
            A list of strings to replace in the the value
            
        [`new_string`=""] {str}
            What the needle will be replaced with in the value
            

        Keyword Arguments
        -------------------------
        `max_replace` {int}
            The maximum number of replacements to make.
            if <= 0, it will find and replace all elements in the array.

        Return {str}
        ----------------------
        The formatted string.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 01-06-2022 10:36:28
        `memberOf`: parse_utils
        `version`: 1.0
        `method_name`: array_replace_string
    '''
    max_replace = obj.get_kwarg(['max','max replace'],0,(int),**kwargs)
    if len(needles) == 0:
        return value

    if isinstance(value, (str)) is False:
        logger.warning('value must be a string.')
        logger.warning(value)

    replace_count = 0
    result_string = value
    for needle in needles:
        if needle in value:
            replace_count += 1
            result_string = result_string.replace(needle,new_string)
            if max_replace > 0:
                if replace_count >= max_replace:
                    return result_string

    return result_string

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
        The type if if it can be determined, None otherwise.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 03\21\2022 12:03:11
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




