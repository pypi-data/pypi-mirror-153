# pylint: disable=redefined-outer-name
# pylint: disable=line-too-long
# pylint: disable=unused-import
'''
    A module of utility methods used for generating strings

    ----------

    Meta
    ----------
    `author`: Colemen Atwood
    `created`: 12-09-2021 09:00:27
    `memberOf`: string_generation
    `version`: 1.0
    `method_name`: string_generation
'''



import json
import hashlib
import string
import random
from faker import Faker
import utils.object_utils as obj
import utils.string_format as mod
import facades.sql_generate_facade as sql



fake = Faker()


def to_hash(value):
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

    uppercase = obj.get_kwarg(['upper case', 'upper'], True, bool, **kwargs)
    lowercase = obj.get_kwarg(['lower case', 'lower'], True, bool, **kwargs)
    digits = obj.get_kwarg(['digits', 'numbers', 'numeric', 'number'], True, bool, **kwargs)
    symbols = obj.get_kwarg(['symbols', 'punctuation'], False, bool, **kwargs)
    exclude = obj.get_kwarg(['exclude'], [], (list, string), **kwargs)

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


    length = obj.get_kwarg(['length'], 100, int, **kwargs)
    line_char = obj.get_kwarg(['line_char'], "=", str, **kwargs)
    white_space = obj.get_kwarg(['white_space'], 1, int, **kwargs)
    print_div = obj.get_kwarg(['print'], True, (bool), **kwargs)

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
    typos = obj.get_kwarg(['typos'], True, bool, **kwargs)
    case_variations = obj.get_kwarg(['case'], True, bool, **kwargs)

    if isinstance(value,(str)):
        value = [value]

    result = []
    for term in value:
        # value = str(value)
        varis = []
        if typos is True:
            varis.extend(generate_typos(term))
        if case_variations is True:
            varis.append(mod.to_snake_case(term))
            varis.append(mod.to_screaming_snake(term))
            varis.extend(mod.to_title_case(varis))
            varis.extend(mod.to_title_case(varis,True))
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
        * @xxx [06-01-2022 10:30:00]: documentation for generate_typos
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

    for idx,_ in enumerate(word):
        tempword = replace_at(word,'',idx)
        typos.append(tempword)

    if len(typos) > 1:
        typos = list(set(typos))
    return typos

def wrong_key_typos(word,keyboard=None):
    word = word.lower()
    typos = []
    if keyboard is None:
        keyboard = TYPO_PROXIMITY_KEYBOARD


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

    for idx,_ in enumerate(word):
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

    for idx,_ in enumerate(word):
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




def text(minimum=10,maximum=500,null_bias=0):
    '''
        Wrapper method for fake.text()
        This adds the ability to randomly return null instead of the string.

        ----------

        Arguments
        -------------------------
        [`minimum`=10] {int}
            The minimum number of characters the text must contain.
        [`maximum`=500] {int}
            The maximum number of characters the text must contain.
        [`null_bias`=0] {int}
            The odds [0-100] that the method will return None.


        Return {type}
        ----------------------
        return_description

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 05-16-2022 09:43:01
        `memberOf`: string_generation
        `version`: 1.0
        `method_name`: text
        # @xxx [05-16-2022 09:49:18]: documentation for text
    '''

    if isinstance(null_bias,(bool)):
        null_bias = 50 if null_bias is True else 0

    if null_bias:
        if fake.boolean(null_bias):
            return None

    val = fake.text()[:random.randint(minimum,maximum)]
    val = val.replace("'","")
    return val

def phone(bias=50):
    '''
        Generate a random phone number or None.

        ----------

        Arguments
        -------------------------
        [`bias`=50] {int}
            The likelihood of returning a phone number.

            If bias = 100 it will always return a phone number and never None.


        Return {str|None}
        ----------------------
        A random fake phone number or None.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 06-03-2022 07:24:03
        `memberOf`: string_generation
        `version`: 1.0
        `method_name`: phone
        * @xxx [06-03-2022 07:25:42]: documentation for phone
    '''

    if fake.boolean(bias):
        return fake.phone_number()
    return None

def email(bias=50):
    '''
        Generate a random email or None.
        This is a wrapper for faker.email() just adding the possibility of not having a value.

        ----------

        Arguments
        -------------------------
        [`bias`=50] {int}
            The likelihood of returning an email.

            If bias = 100 it will always return an email and never None.


        Return {str|None}
        ----------------------
        A random fake email or None.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 06-03-2022 07:24:03
        `memberOf`: string_generation
        `version`: 1.0
        `method_name`: email
        * @xxx [06-03-2022 07:25:42]: documentation for email
    '''
    if fake.boolean(bias):
        return fake.free_email()
    return None

def url(bias=50):
    '''
        Generate a random url or None.
        This is a wrapper for faker.url() just adding the possibility of not having a value.

        ----------

        Arguments
        -------------------------
        [`bias`=50] {int}
            The likelihood of returning a url.

            If bias = 100 it will always return a url and never None.


        Return {str|None}
        ----------------------
        A random fake url or None.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 06-03-2022 07:24:03
        `memberOf`: string_generation
        `version`: 1.0
        `method_name`: url
        * @xxx [06-03-2022 07:25:42]: documentation for url
    '''
    if fake.boolean(bias):
        return fake.url()
    return None

def abstract_name(**kwargs):
    '''
        Generate an abstract (non-human) name consisting of an adjective and a noun.

        ----------

        Arguments
        -------------------------
        `arg_name` {type}
                arg_description

        Keyword Arguments
        -------------------------
        [`bias`=100] {int}
            The likelihood (0-100) of it returning an abstract name vs returning None

        Return {str|None}
        ----------------------
        The abstract name or None if the bias is provided.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 06-03-2022 07:36:04
        `memberOf`: string_generation
        `version`: 1.0
        `method_name`: abstract_name
        * @xxx [06-03-2022 07:38:26]: documentation for abstract_name
    '''
    bias = obj.get_kwarg(['bias'], 100, (int), **kwargs)
    if fake.boolean(bias):
        return f"{_rand_adjective()} {_rand_noun()}".title()
    return None


def _rand_adjective():
    options = ["adorable",
        "adventurous",
        "aggressive",
        "agreeable",
        "alert",
        "alive",
        "amused",
        "angry",
        "annoyed",
        "annoying",
        "anxious",
        "arrogant",
        "ashamed",
        "attractive",
        "average",
        "awful",
        "bad",
        "beautiful",
        "better",
        "bewildered",
        "black",
        "bloody",
        "blue",
        "blue-eyed",
        "blushing",
        "bored",
        "brainy",
        "brave",
        "breakable",
        "bright",
        "busy",
        "calm",
        "careful",
        "cautious",
        "charming",
        "cheerful",
        "clean",
        "clear",
        "clever",
        "cloudy",
        "clumsy",
        "colorful",
        "combative",
        "comfortable",
        "concerned",
        "condemned",
        "confused",
        "cooperative",
        "courageous",
        "crazy",
        "creepy",
        "crowded",
        "cruel",
        "curious",
        "cute",
        "dangerous",
        "dark",
        "dead",
        "defeated",
        "defiant",
        "delightful",
        "depressed",
        "determined",
        "different",
        "difficult",
        "disgusted",
        "distinct",
        "disturbed",
        "dizzy",
        "doubtful",
        "drab",
        "dull",
        "eager",
        "easy",
        "elated",
        "elegant",
        "embarrassed",
        "enchanting",
        "encouraging",
        "energetic",
        "enthusiastic",
        "envious",
        "evil",
        "excited",
        "expensive",
        "exuberant",
        "fair",
        "faithful",
        "famous",
        "fancy",
        "fantastic",
        "fierce",
        "filthy",
        "fine",
        "foolish",
        "fragile",
        "frail",
        "frantic",
        "friendly",
        "frightened",
        "funny",
        "gentle",
        "gifted",
        "glamorous",
        "gleaming",
        "glorious",
        "good",
        "gorgeous",
        "graceful",
        "grieving",
        "grotesque",
        "grumpy",
        "handsome",
        "happy",
        "healthy",
        "helpful",
        "helpless",
        "hilarious",
        "homeless",
        "homely",
        "horrible",
        "hungry",
        "hurt",
        "ill",
        "important",
        "impossible",
        "inexpensive",
        "innocent",
        "inquisitive",
        "itchy",
        "jealous",
        "jittery",
        "jolly",
        "joyous",
        "kind",
        "lazy",
        "light",
        "lively",
        "lonely",
        "long",
        "lovely",
        "lucky",
        "magnificent",
        "misty",
        "modern",
        "motionless",
        "muddy",
        "mushy",
        "mysterious",
        "nasty",
        "naughty",
        "nervous",
        "nice",
        "nutty",
        "obedient",
        "obnoxious",
        "odd",
        "old-fashioned",
        "open",
        "outrageous",
        "outstanding",
        "panicky",
        "perfect",
        "plain",
        "pleasant",
        "poised",
        "poor",
        "powerful",
        "precious",
        "prickly",
        "proud",
        "putrid",
        "puzzled",
        "quaint",
        "real",
        "relieved",
        "repulsive",
        "rich",
        "scary",
        "selfish",
        "shiny",
        "shy",
        "silly",
        "sleepy",
        "smiling",
        "smoggy",
        "sore",
        "sparkling",
        "splendid",
        "spotless",
        "stormy",
        "strange",
        "stupid",
        "successful",
        "super",
        "talented",
        "tame",
        "tasty",
        "tender",
        "tense",
        "terrible",
        "thankful",
        "thoughtful",
        "thoughtless",
        "tired",
        "tough",
        "troubled",
        "ugliest",
        "ugly",
        "uninterested",
        "unsightly",
        "unusual",
        "upset",
        "uptight",
        "vast",
        "victorious",
        "vivacious",
        "wandering",
        "weary",
        "wicked",
        "wide-eyed",
        "wild",
        "witty",
        "worried",
        "worrisome",
        "wrong",
        "zany",
        "zealous"]
    return _rand_option(options)

def _rand_noun():
    options = ["Actor",
        "Gold",
        "Painting",
        "Advertisement",
        "Grass",
        "Parrot",
        "Afternoon",
        "Greece",
        "Pencil",
        "Airport",
        "Guitar",
        "Piano",
        "Ambulance",
        "Hair",
        "Pillow",
        "Animal",
        "Hamburger",
        "Pizza",
        "Answer",
        "Helicopter",
        "Planet",
        "Apple",
        "Helmet",
        "Plastic",
        "Army",
        "Holiday",
        "Portugal",
        "Australia",
        "Honey",
        "Potato",
        "Balloon",
        "Horse",
        "Queen",
        "Banana",
        "Hospital",
        "Quill",
        "Battery",
        "House",
        "Rain",
        "Beach",
        "Hydrogen",
        "Rainbow",
        "Beard",
        "Ice",
        "Raincoat",
        "Bed",
        "Insect",
        "Refrigerator",
        "Belgium",
        "Insurance",
        "Restaurant",
        "Boy",
        "Iron",
        "River",
        "Branch",
        "Island",
        "Rocket",
        "Breakfast",
        "Jackal",
        "Room",
        "Brother",
        "Jelly",
        "Rose",
        "Camera",
        "Jewellery",
        "Russia",
        "Candle",
        "Jordan",
        "Sandwich",
        "Car",
        "Juice",
        "School",
        "Caravan",
        "Kangaroo",
        "Scooter",
        "Carpet",
        "King",
        "Shampoo",
        "Cartoon",
        "Kitchen",
        "Shoe",
        "China",
        "Kite",
        "Soccer",
        "Church",
        "Knife",
        "Spoon",
        "Crayon",
        "Lamp",
        "Stone",
        "Crowd",
        "Lawyer",
        "Sugar",
        "Daughter",
        "Leather",
        "Sweden",
        "Death",
        "Library",
        "Teacher",
        "Denmark",
        "Lighter",
        "Telephone",
        "Diamond",
        "Lion",
        "Television",
        "Dinner",
        "Lizard",
        "Tent",
        "Disease",
        "Lock",
        "Thailand",
        "Doctor",
        "London",
        "Tomato",
        "Dog",
        "Lunch",
        "Toothbrush",
        "Dream",
        "Machine",
        "Traffic",
        "Dress",
        "Magazine",
        "Train",
        "Easter",
        "Magician",
        "Truck",
        "Egg",
        "Manchester",
        "Uganda",
        "Eggplant",
        "Market",
        "Umbrella",
        "Egypt",
        "Match",
        "Van",
        "Elephant",
        "Microphone",
        "Vase",
        "Energy",
        "Monkey",
        "Vegetable",
        "Engine",
        "Morning",
        "Vulture",
        "England",
        "Motorcycle",
        "Wall",
        "Evening",
        "Nail",
        "Whale",
        "Eye",
        "Napkin",
        "Window",
        "Family",
        "Needle",
        "Wire",
        "Finland",
        "Nest",
        "Xylophone",
        "Fish",
        "Nigeria",
        "Yacht",
        "Flag",
        "Night",
        "Yak",
        "Flower",
        "Notebook",
        "Zebra",
        "Football",
        "Ocean",
        "Zoo",
        "Forest",
        "Oil",
        "Garden",
        "Fountain",
        "Orange",
        "Gas",
        "France",
        "Oxygen",
        "Girl",
        "Furniture",
        "Oyster",
        "Glass",
        "Garage",
        "Ghost"
        ]
    return _rand_option(options)

# def _get_faker()->Faker:
#     if FAKER_INSTANCE is None:
#         FAKER_INSTANCE = Faker()

#     return FAKER_INSTANCE

def _rand_option(options):
    list_len = len(options)
    try:
        return options[random.randint(0, list_len)]
    except IndexError:
        return _rand_option(options)
