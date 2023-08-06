# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long
# pylint: disable=global-statement
'''
    A module of utility methods used for generating random data.

    ----------

    Meta
    ----------
    `author`: Colemen Atwood
    `created`: 06-03-2022 10:22:15
    `memberOf`: random_utils
'''

import random as _random
import hashlib as _hashlib
import time as _time
import string as _string
from typing import Union as _Union
from faker import Faker as _Faker
import utils.random_utils.rand_utils as _ru
import utils.dict_utils as _obj
import utils.string_utils as _csu
# import facades.rand_utils_facade as rand



# from utils.object_utils import rand_option as option
# from utils.string_generation import text,phone,email,url,abstract_name,rand

# from utils.dict_utils.dict_utils import get_kwarg as _obj.get_kwarg

FAKER_INSTANCE = None



def faker()->_Faker:
    global FAKER_INSTANCE
    if FAKER_INSTANCE is None:
        FAKER_INSTANCE = _Faker()
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
    return _random.randint(1,100) <= bias

def null_boolean():
    return{
        0: None,
        1: True,
        -1: False,
    }[_random.randint(-1, 1)]

def md5(raw_output: bool = False) -> _Union[bytes, str]:
    """Generate a random MD5 hash.

    If ``raw_output`` is ``False`` (default), a hexadecimal string representation of the MD5 hash
    will be returned. If ``True``, a ``bytes`` object representation will be returned instead.

    :sample: raw_output=False
    :sample: raw_output=True
    """
    res = _hashlib.md5(str(_random.random()).encode())
    if raw_output:
        return res.digest()
    return res.hexdigest()

def sha1(raw_output: bool = False) -> _Union[bytes, str]:
    """Generate a random SHA1 hash.

    If ``raw_output`` is ``False`` (default), a hexadecimal string representation of the SHA1 hash
    will be returned. If ``True``, a ``bytes`` object representation will be returned instead.

    :sample: raw_output=False
    :sample: raw_output=True
    """
    res = _hashlib.sha1(str(_random.random()).encode())
    if raw_output:
        return res.digest()
    return res.hexdigest()

def sha256(raw_output:bool=False) -> _Union[bytes, str]:
    res = _hashlib.sha256(str(_random.random()).encode())
    if raw_output:
        return res.digest()
    return res.hexdigest()

def past_date(days:_Union[int,None]=None)->int:
    if days is None:
        days = _random.randint(1,800)
    seconds = _random.randint(1,86400)
    return int(_time.time()) - ((days * 86400) + seconds)

def future_date(days:_Union[int,None]=None)->int:
    if days is None:
        days = _random.randint(1,800)
    seconds = _random.randint(1,86400)
    return int(_time.time()) + ((days * 86400) + seconds)

def rand(length=12, **kwargs):
    '''
        Generates a cryptographically secure random _string.


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
            Characters to exclude from the random _string.

        Return
        ----------
        `return` {str}
            A random string of N length.
    '''

    uppercase = _obj.get_kwarg(['upper case', 'upper'], True, bool, **kwargs)
    lowercase = _obj.get_kwarg(['lower case', 'lower'], True, bool, **kwargs)
    digits = _obj.get_kwarg(['digits', 'numbers', 'numeric', 'number'], True, bool, **kwargs)
    symbols = _obj.get_kwarg(['symbols', 'punctuation'], False, bool, **kwargs)
    exclude = _obj.get_kwarg(['exclude'], [], (list, str), **kwargs)

    choices = ''
    if uppercase is True:
        choices += _string.ascii_uppercase
    if lowercase is True:
        choices += _string.ascii_lowercase
    if digits is True:
        choices += _string.digits
    if symbols is True:
        choices += _string.punctuation

    if len(exclude) > 0:
        if isinstance(exclude, str):
            exclude = list(exclude)
        for exd in exclude:
            choices = choices.replace(exd, '')

    return ''.join(_random.SystemRandom().choice(choices) for _ in range(length))

def text(minimum=10,maximum=500,null_bias=0):
    '''
        Wrapper method for faker().text()
        This adds the ability to randomly return null instead of the _string.

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
        if faker().boolean(null_bias):
            return None

    val = faker().text()[:_random.randint(minimum,maximum)]
    val = val.replace("'","")
    return val

def phone(bias=100):
    '''
        Generate a random phone number or None.

        ----------

        Arguments
        -------------------------
        [`bias`=100] {int}
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

    if faker().boolean(bias):
        return faker().phone_number()
    return None

def email(bias=100):
    '''
        Generate a random email or None.
        This is a wrapper for faker.email() just adding the possibility of not having a value.

        ----------

        Arguments
        -------------------------
        [`bias`=100] {int}
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
    if faker().boolean(bias):
        return faker().free_email()
    return None

def url(bias=100):
    '''
        Generate a random url or None.
        This is a wrapper for faker.url() just adding the possibility of not having a value.

        ----------

        Arguments
        -------------------------
        [`bias`=100] {int}
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
    if faker().boolean(bias):
        return faker().url()
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
    bias = _obj.get_kwarg(['bias'], 100, (int), **kwargs)
    if faker().boolean(bias):
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
        return options[_random.randint(0, list_len)]
    except IndexError:
        return _rand_option(options)

def female_first_last_name():
    '''
        Generate a random female first and last name

        ----------

        Return {tuple}
        ----------------------
        A tuple (first,last)

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 06-05-2022 11:48:42
        `memberOf`: rand_generation
        `version`: 1.0
        `method_name`: female_first_last_name
        * @xxx [06-05-2022 11:49:20]: documentation for female_first_last_name
    '''

    
    fake = faker()
    return (fake.first_name_female(), fake.last_name())

def male_first_last_name():
    '''
        Generate a random male first and last name

        ----------

        Return {tuple}
        ----------------------
        A tuple (first,last)

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 06-05-2022 11:48:42
        `memberOf`: rand_generation
        `version`: 1.0
        `method_name`: male_first_last_name
        * @xxx [06-05-2022 11:49:20]: documentation for male_first_last_name
    '''    
    fake = faker()
    return (fake.first_name_male(), fake.last_name())

def gender()->str:
    '''
        Randomly generate a gender "male" or "female"

        ----------


        Return {str}
        ----------------------
        The gender.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 06-04-2022 10:11:34
        `memberOf`: rand_generation
        `version`: 1.0
        `method_name`: gender
        * @xxx [06-04-2022 10:12:06]: documentation for gender
    '''


    return _ru.option(["male","female"])

def user(**kwargs)->dict:
    '''
        Randomly generate a user data dictionary.

        ----------

        Keyword Arguments
        -------------------------
        [`gender`=None] {str|None}
            The gender of the user (male,female), if not provided one is randomly selected.

        [`password`=None] {str|None}
            The password for the user, if not provided one is randomly generated.

        Return {dict}
        ----------------------
        A user dictionary:
        {
            `gender`:"female",
            `first_name`:"Sarah",
            `last_name`:"Paulson",
            `password`:"Zxbp43JMGuPm",
            `email`:"dork@gmail.com",
            `phone`:"806.355.2586",
            `birthday`:123456789,
        }

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 06-04-2022 10:12:17
        `memberOf`: rand_generation
        `version`: 0.0.0
        `method_name`: user
        * @xxx [06-04-2022]: documentation for user
    '''


    fake = faker()

    data = {
        "gender":"",
        "first_name":"",
        "last_name":"",
        "password":_obj.get_kwarg(['password','pass'], rand(), (None,str), **kwargs),
        "email":"",
        "phone":"",
        "birthday":past_date(),
    }

    ugen = _obj.get_kwarg(['gender'], None, (None,str), **kwargs)
    # data['password'] = _obj.get_kwarg(['password','pass'], rand(), (None,str), **kwargs)

    if ugen is None:
        data['gender'] = gender()

    if isinstance(ugen,(str)):
        gen = _csu.determine_gender(ugen)
        if gen is None:
            data['gender'] = gender()
        else:
            data['gender'] = gen

    if data['gender'] == "female":
        data['first_name'] = fake.first_name_female()
    if data['gender'] == "male":
        data['first_name'] = fake.first_name_male()
    data['last_name'] = fake.last_name()
    data['email'] = fake.free_email()
    data['phone'] = fake.phone_number()

    return data




