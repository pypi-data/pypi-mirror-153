# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# '''
#     A module of utility methods used for generating random data or performing various
#     actions randomly.

#     ----------

#     Meta
#     ----------
#     `author`: Colemen Atwood
#     `created`: 06-03-2022 10:22:15
#     `memberOf`: rand
#     `version`: 1.0
#     `method_name`: rand
# '''

import random
import hashlib
import time
import string
from typing import Union
from faker import Faker
# import facades.rand_utils_facade as rand



# from utils.object_utils import rand_option as option
# from utils.string_generation import text,phone,email,url,abstract_name,rand

from utils.dict_utils.dict_utils import get_kwarg as _get_kwarg



FAKER_INSTANCE:Faker = None

def fake()->Faker:
    if FAKER_INSTANCE is None:
        FAKER_INSTANCE = Faker()
    return FAKER_INSTANCE


def gen_variations(value):
    value = str(value)
    varis = []
    lower = value.lower()
    upper = value.upper()
    snake_case = lower.replace(" ", "_")
    screaming_snake_case = upper.replace(" ", "_")
    varis.append(lower)
    varis.append(upper)
    varis.append(snake_case)
    varis.append(screaming_snake_case)
    return varis


def boolean(bias=50):
    return random.randint(1,100) <= bias

def null_boolean():
    return{
        0: None,
        1: True,
        -1: False,
    }[random.randint(-1, 1)]

def md5(raw_output: bool = False) -> Union[bytes, str]:
    """Generate a random MD5 hash.

    If ``raw_output`` is ``False`` (default), a hexadecimal string representation of the MD5 hash
    will be returned. If ``True``, a ``bytes`` object representation will be returned instead.

    :sample: raw_output=False
    :sample: raw_output=True
    """
    res = hashlib.md5(str(random.random()).encode())
    if raw_output:
        return res.digest()
    return res.hexdigest()

def sha1(raw_output: bool = False) -> Union[bytes, str]:
    """Generate a random SHA1 hash.

    If ``raw_output`` is ``False`` (default), a hexadecimal string representation of the SHA1 hash
    will be returned. If ``True``, a ``bytes`` object representation will be returned instead.

    :sample: raw_output=False
    :sample: raw_output=True
    """
    res = hashlib.sha1(str(random.random()).encode())
    if raw_output:
        return res.digest()
    return res.hexdigest()

def sha256(raw_output:bool=False) -> Union[bytes, str]:
    res = hashlib.sha256(str(random.random()).encode())
    if raw_output:
        return res.digest()
    return res.hexdigest()

def past_date(days:Union[int,None]=None)->int:
    if days is None:
        days = random.randint(1,800)
    seconds = random.randint(1,86400)
    return int(time.time()) - ((days * 86400) + seconds)

def future_date(days:Union[int,None]=None)->int:
    if days is None:
        days = random.randint(1,800)
    seconds = random.randint(1,86400)
    return int(time.time()) + ((days * 86400) + seconds)

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

    uppercase = _get_kwarg(['upper case', 'upper'], True, bool, **kwargs)
    lowercase = _get_kwarg(['lower case', 'lower'], True, bool, **kwargs)
    digits = _get_kwarg(['digits', 'numbers', 'numeric', 'number'], True, bool, **kwargs)
    symbols = _get_kwarg(['symbols', 'punctuation'], False, bool, **kwargs)
    exclude = _get_kwarg(['exclude'], [], (list, string), **kwargs)

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

def text(minimum=10,maximum=500,null_bias=0):
    '''
        Wrapper method for fake().text()
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
        if fake().boolean(null_bias):
            return None

    val = fake().text()[:random.randint(minimum,maximum)]
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

    if fake().boolean(bias):
        return fake().phone_number()
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
    if fake().boolean(bias):
        return fake().free_email()
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
    if fake().boolean(bias):
        return fake().url()
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
    bias = _get_kwarg(['bias'], 100, (int), **kwargs)
    if fake().boolean(bias):
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

def _rand_option(options):
    list_len = len(options)
    try:
        return options[random.randint(0, list_len)]
    except IndexError:
        return _rand_option(options)
