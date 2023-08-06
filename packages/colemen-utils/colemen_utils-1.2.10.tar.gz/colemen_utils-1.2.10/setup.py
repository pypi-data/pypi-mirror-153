from setuptools import setup, find_packages

VERSION = '1.2.10'
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
        'utils.dict_utils',
        'utils.dict_utils.dict_utils',
        'utils.directory_utils',
        'utils.directory_utils.dir',
        'utils.directory_utils.dir_compression',
        'utils.directory_utils.dir_create',
        'utils.directory_utils.dir_delete',
        'utils.directory_utils.dir_read',
        'utils.directory_utils.dir_search',
        'utils.drawio',
        'utils.drawio.connector',
        'utils.drawio.diagram',
        'utils.drawio.diagram_utils',
        'utils.drawio.drawing',
        'utils.drawio.mcxell',
        'utils.drawio.nodeBase',
        'utils.drawio.nodes',
        'utils.drawio.onode',
        'utils.file_utils',
        'utils.file_utils.exiftool',
        'utils.file_utils.file_compression',
        'utils.file_utils.file_convert',
        'utils.file_utils.file_image',
        'utils.file_utils.file_read',
        'utils.file_utils.file_search',
        'utils.file_utils.file_string_facade',
        'utils.file_utils.file_utils',
        'utils.file_utils.file_write',
        'utils.file_utils.resources',
        'utils.list_utils',
        'utils.list_utils.list_utils',
        'utils.parse_sql',
        'utils.parse_utils',
        'utils.random_utils',
        'utils.random_utils.rand_generation',
        'utils.random_utils.rand_utils',
        'utils.sql_utils',
        'utils.sql_utils.sql_utils',
        'utils.string_utils',
        'utils.string_utils.string_conversion',
        'utils.string_utils.string_escaping',
        'utils.string_utils.string_format',
        'utils.string_utils.string_generation',
        'utils.string_utils.string_parsing',
        'utils.string_utils.string_strip',
        'utils.type_utils',
        'utils.type_utils.type_utils',
    ],
    # add any additional packages that
    # need to be installed along with your package. Eg: 'caer'
    install_requires=[
        'secure_delete',
        'ftputil',
        'ffmpeg-python',
        'pillow',
        'faker',
        'iptcinfo3',
        'patool',
        'pyparsing',
        'sqlparse',
        'colorama',
        'lxml',
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

