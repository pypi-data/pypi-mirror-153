from setuptools import setup, find_packages

VERSION = '1.8.19'
DESCRIPTION = 'Colemen String Utils'
LONG_DESCRIPTION = 'Colemen String Utils is a library of useful string generation and manipulation methods.'

# Setting up
setup(
    # the name must match the folder name 'verysimplemodule'
    name="colemen_string_utils",
    version=VERSION,
    author="Colemen Atwood",
    author_email="<atwoodcolemen@gmail.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    py_modules=[
        'colemen_string_utils',
        'utils.objectUtils',
        'utils.string_generation',
        'utils.string_conversion',
        'utils.string_format',
        'utils.parse_utils',
        'utils.parse_sql',
        'facades.sql_parse_facade',
        'facades.sql_generate_facade',
    ],
    install_requires=[
        
    ],  # add any additional packages that
    # need to be installed along with your package. Eg: 'caer'

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


