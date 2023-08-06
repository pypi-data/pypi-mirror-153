import json
import hashlib
import string
import random
import utils.objectUtils as objUtils
import utils.string_format as strFormat
import facades.sql_generate_facade as sql

def hash(value):
    '''
        Generates a sha256 hash from the string provided.

        ----------
        Arguments
        -----------------
        `value` {str}
            The string to calculate the hash on.

        Return
        ----------
        `return` {str}
            The sha256 hash
    '''
    json_str = json.dumps(value).encode('utf-8')
    hex_dig = hashlib.sha256(json_str).hexdigest()
    return hex_dig


def rand(length=12, **kwargs):
    '''
        Generates a cryptographically secure random string.


        ----------
        Arguments
        -----------------
        `length`=12 {int}
            The number of characters that the string should contain.

        Keyword Arguments
        -----------------
        `upper_case`=True {bool}
            If True, uppercase letters are included.
            ABCDEFGHIJKLMNOPQRSTUVWXYZ

        `lower_case`=True {bool}
            If True, lowercase letters are included.
            abcdefghijklmnopqrstuvwxyz

        `digits`=True {bool}
            If True, digits are included.
            0123456789

        `symbols`=False {bool}
            If True, symbols are included.
            !"#$%&'()*+,-./:;<=>?@[]^_`{|}~

        `exclude`=[] {string|list}
            Characters to exclude from the random string.

        Return
        ----------
        `return` {str}
            A random string of N length.
    '''

    uppercase = objUtils.get_kwarg(['upper case', 'upper'], True, bool, **kwargs)
    lowercase = objUtils.get_kwarg(['lower case', 'lower'], True, bool, **kwargs)
    digits = objUtils.get_kwarg(['digits', 'numbers', 'numeric', 'number'], True, bool, **kwargs)
    symbols = objUtils.get_kwarg(['symbols', 'punctuation'], False, bool, **kwargs)
    exclude = objUtils.get_kwarg(['exclude'], [], (list, string), **kwargs)

    choices = ''
    if uppercase is True:
        choices += string.ascii_uppercase
    if lowercase is True:
        choices += string.ascii_lowercase
    if digits is True:
        choices += string.digits
    if symbols is True:
        choices += string.punctuation

    if len(exclude) > 0:
        if isinstance(exclude, str):
            exclude = list(exclude)
        for e in exclude:
            choices = choices.replace(e, '')

    return ''.join(random.SystemRandom().choice(choices) for _ in range(length))

def title_divider(message='',**kwargs):
    '''
        Generate a console log divider with centered message.

        ==================   hi there   ===================

        ----------

        Arguments
        -------------------------

        [`message`=''] {str}
            The message text to center in the divider. If not provided the divider will be solid.


        Keyword Arguments
        -------------------------
        [`white_space`=1] {int}
            How many spaces should be on each side of the message as padding.

        [`length`=100] {int}
            How many characters wide the title should be.

        [`line_char`="="] {str}
            The character to use as the "line" of the divider.

        [`print`=True] {bool}
            if True, this will print the divider it generates

        Return {str}
        ----------------------
        The divider string.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 04-28-2022 08:03:09
        `memberOf`: string_generation
        `version`: 1.0
        `method_name`: title_divider
        # @xxx [04-28-2022 08:08:04]: documentation for title_divider
    '''


    length = objUtils.get_kwarg(['length'], 100, int, **kwargs)
    line_char = objUtils.get_kwarg(['line_char'], "=", str, **kwargs)
    white_space = objUtils.get_kwarg(['white_space'], 1, int, **kwargs)
    print_div = objUtils.get_kwarg(['print'], True, (bool), **kwargs)

    if isinstance(line_char,(str,int)) is False:
        line_char = "="
    if len(line_char) > 1:
        line_char = line_char[0]

    msg_len = len(message)
    if length < msg_len:
        # print(f"Length {length} must be greater than the length of the message {msg_len}.")
        return message

    if msg_len == 0:
        return line_char * length

    # @Mstep [] calculate how many "line" chars must fill the excess space.
    char_count = (length / len(line_char)) - (msg_len+(white_space*2))
    # @Mstep [] calculate how many line chars should be on each side of the message.
    half_char = int(char_count / 2)

    # @Mstep [] generate the line char string.
    char_str = f"{line_char * half_char}"
    padding = ' ' * white_space
    line = f"{char_str}{padding}{message}{padding}{char_str}"


    if len(line) < length:
        dif = length - len(line)
        lchar = ''
        rchar = line_char * dif
        if (dif % 2) == 0:
            rchar = line_char * (dif / 2)
            lchar = line_char * (dif / 2)
        line = f"{char_str}{lchar}{padding}{message}{padding}{rchar}{char_str}"

    # print(len(line))
    if print_div is True:
        print(line)
    return line

# def is_even(num):
#     if (num % 2) == 0:
#         return True
#     return False

# print(title_divider())
# print(title_divider('boobs',line_char='_',length=75))

def variations(value,**kwargs):
    '''
        Generates simple variations of the string provided.

        ----------
        Arguments
        -----------------
        `string` {str}
            The string to generate variations of

        Keyword Arguments
        -----------------
        `typos`=True {bool}
            if True typos are generated:
            missed keys, wrong keys, transposed keys and double characters.
        `case`=True {bool}
            if True case variations are generated:
            snake case, screaming snake case, title case, reverse title case.

            This will apply to all typos as well.

        Return
        ----------
        `return` {str}
            A list of variations.

        Example
        ----------
        BeepBoop => ['BEEPBOOPBLEEPBLORP','beepboopbleepblorp','beep_boop','BEEP_BOOP']
    '''
    typos = objUtils.get_kwarg(['typos'], True, bool, **kwargs)
    case_variations = objUtils.get_kwarg(['case'], True, bool, **kwargs)

    if isinstance(value,(str)):
        value = [value]

    result = []
    for term in value:
        # value = str(value)
        varis = []
        if typos is True:
            varis.extend(generate_typos(term))
        if case_variations is True:
            varis.append(strFormat.to_snake_case(term))
            varis.append(strFormat.to_screaming_snake(term))
            varis.extend(strFormat.title_case(varis))
            varis.extend(strFormat.title_case(varis,True))
        if len(varis) > 1:
            varis = list(set(varis))
        result.extend(varis)
    return result

TYPO_PROXIMITY_KEYBOARD = {
        '1': "2q",
        '2': "1qw3",
        '3': "2we4",
        '4': "3er5",
        '5': "4rt6",
        '6': "5ty7",
        '7': "6yu8",
        '8': "7ui9",
        '9': "8io0",
        '0': "9op-",
        '-': "0p",
        'q': "12wa",
        'w': "qase32",
        'e': "wsdr43",
        'r': "edft54",
        't': "rfgy65",
        'y': "tghu76",
        'u': "yhji87",
        'i': "ujko98",
        'o': "iklp09",
        'p': "ol-0",
        'a': "zswq",
        's': "azxdew",
        'd': "sxcfre",
        'f': "dcvgtr",
        'g': "fvbhyt",
        'h': "gbnjuy",
        'j': "hnmkiu",
        'k': "jmloi",
        'l': "kpo",
        'z': "xsa",
        'x': "zcds",
        'c': "xvfd",
        'v': "cbgf",
        'b': "vnhg",
        'n': "bmjh",
        'm': "nkj"
    }


def generate_typos(text):
    '''
        Generate typo variations of the text provided.

        ----------

        Arguments
        -------------------------
        `text` {str}
            The text to generate typos of.

        Return {list}
        ----------------------
        A list of typo strings.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 06-01-2022 10:29:06
        `memberOf`: string_generation
        `version`: 1.0
        `method_name`: generate_typos
        @xxx [06-01-2022 10:30:00]: documentation for generate_typos
    '''


    if len(text) == 0:
        return []
    typos = []
    typos.extend(missed_key_typos(text))
    typos.extend(wrong_key_typos(text))
    typos.extend(transposed_chars(text))
    typos.extend(double_char_typos(text))
    if len(typos) > 1:
        typos = list(set(typos))
    return typos

def missed_key_typos(word):
    word = word.lower()
    typos = []
    # length = len(word)

    for idx,letter in enumerate(word):
        tempword = replace_at(word,'',idx)
        typos.append(tempword)

    if len(typos) > 1:
        typos = list(set(typos))
    return typos

def wrong_key_typos(word,keyboard=TYPO_PROXIMITY_KEYBOARD):
    word = word.lower()
    typos = []


    for letter in word:
        if letter in keyboard:
            temp_word = word
            for char in keyboard[letter]:
                typos.append(temp_word.replace(letter,char).strip())

    # print(f"typos: ",typos)
    if len(typos) > 1:
        typos = list(set(typos))
    return typos

def transposed_chars(word):
    word = word.lower()
    typos = []

    for idx,letter in enumerate(word):
        tempword = word
        tempchar = tempword[idx]
        if idx + 1 != len(tempword):
            tempword = replace_at(tempword,tempword[idx + 1],idx)
            tempword = replace_at(tempword,tempchar,idx + 1)
            typos.append(tempword)
    # print(f"typos: ",typos)
    if len(typos) > 1:
        typos = list(set(typos))
    return typos

def double_char_typos(word):
    word = word.lower()
    typos = []

    for idx,letter in enumerate(word):
        tempword = word[0:idx]
        tempword += word[idx-1:]
        # if idx != len(word) - 1:
            # tempword += word[idx + 1]
        if len(tempword) == len(word) + 1:
            typos.append(tempword)

    if len(typos) > 1:
        typos = list(set(typos))
    return typos

def replace_at(s, newstring, index, nofail=False):
    # raise an error if index is outside of the string
    if not nofail and index not in range(len(s)):
        raise ValueError("index outside given string")

    # if not erroring, but the index is still not in the correct range..
    if index < 0:  # add it to the beginning
        return newstring + s
    if index > len(s):  # add it to the end
        return s + newstring

    # insert the new string between "slices" of the original
    return s[:index] + newstring + s[index + 1:]



# print(variations(["abc","123"],case=False))
# print(missed_key_typos("colemen"))
