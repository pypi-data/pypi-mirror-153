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
import utils.objectUtils as obj
import utils.string_format as format


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


