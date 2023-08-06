'''
    Setup for colemen_database_utils.
    Used for building the wheel and pip installation.

    ----------
    Meta
    ----------
    `author`: Colemen Atwood
    `created`: 12-09-2021 09:13:26
    `memberOf`: setup
    `version`: 1.0
'''
from setuptools import setup, find_packages

VERSION = '1.1.14'
DESCRIPTION = 'Colemen Database Utils'
LONG_DESCRIPTION = 'Colemen Database Utils'

# Setting up
setup(
    # the name must match the folder name 'verysimplemodule'
    name="colemen_database_utils",
    version=VERSION,
    author="Colemen Atwood",
    author_email="<atwoodcolemen@gmail.com>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    py_modules=[
        'colemen_database',
        'utils.DatabaseManager',
        'utils.TableDataManager',
        'utils.TableManager',
        'utils.generation',
        'utils.object_utils',
        'utils.sql_utils',
        'utils.table_utils',
        'utils.local_db_management',
    ],
    # add any additional packages that
    # need to be installed along with your package. Eg: 'caer'
    install_requires=[
        'colemen_string_utils>=0.0.6',
        'colemen_file_utils>=0.0.10',
        'mysql-connector'
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
