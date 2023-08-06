from setuptools import setup, find_packages

VERSION = '1.1.3'
DESCRIPTION = 'Colemen Utils'
LONG_DESCRIPTION = 'Colemen Utils is a composite library of shit I find useful.'

# Setting up
setup(
    # the name must match the folder name 'verysimplemodule'
    name="colemen_utils",
    version=VERSION,
    author="Colemen Atwood",
    author_email="<atwoodcolemen@gmail.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    py_modules=[
        'colemen_utils',
        'facades.dict_utils_facade',
        'facades.directory_facade',
        'facades.files_facade',
        'facades.list_utils_facade',
        'facades.rand_string_facade',
        'facades.rand_utils_facade',
        'facades.sql_convert_facade',
        'facades.sql_facade',
        'facades.sql_generate_facade',
        'facades.sql_parse_facade',
        'facades.string_facade',
        'facades.types_facade',
        'facades.dict_utils_facade',
        'facades.directory_facade',
        'facades.files_facade',
        'facades.list_utils_facade',
        'facades.rand_string_facade',
        'facades.rand_utils_facade',
        'facades.sql_convert_facade',
        'facades.sql_facade',
        'facades.sql_generate_facade',
        'facades.sql_parse_facade',
        'facades.string_facade',
        'facades.types_facade',
        'utils.object_utils',
        'utils.parse_sql',
        'utils.files.dir',
        'utils.parse_utils',
        'utils.files.dir_compression',
        'utils.files.dir_search',
        'utils.files.exiftool',
        'utils.string_conversion',
        'utils.random_utils',
        'utils.string_format',
        'utils.files.file',
        'utils.files.file_compression',
        'utils.string_generation',
        'utils.files.file_convert',
        'utils.types',
        'utils.files.file_image',
        'utils.files.file_read',
        'utils.files.file_search',
        'utils.files.file_write',
        'utils.files.resources',
    ],
    # add any additional packages that
    # need to be installed along with your package. Eg: 'caer'
    install_requires=[
        'secure_delete',
        'ftputil',
        'ffmpeg-python',
        'pillow',
        'iptcinfo3',
        'patool',
        'pyparsing',
        'sqlparse',
        'colorama',
    ],

    keywords=['python'],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Education",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 3",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)

