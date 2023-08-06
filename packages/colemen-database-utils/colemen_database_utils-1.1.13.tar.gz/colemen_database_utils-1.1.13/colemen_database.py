# import docutils.core
import sqlite3
import traceback
import sys
import re
# import io
import os
# import datetime
# import json
import mysql.connector
from mysql.connector import Error
import utils.object_utils as obj
import utils.sql_utils as sqlUtils
import utils.table_utils as tableUtils
import utils.generation as genUtils
import utils.DatabaseManager as databaseManager
DatabaseManager = databaseManager.DatabaseManager
# import utils.local_db_management as local

# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=invalid-name

def database(**kwargs)->databaseManager.DatabaseManager:
    '''
        Instantiate a DatabaseManager class.

        ----------


        Keyword Arguments
        -------------------------
        [`name`=None] {str}
            The name of the database.

        [`credentials`=None] {dict}
            The database credentials for a mySQL database.

        [`summary_path`=None] {str}
            The path to the summary file to load the database manager from.

        Return {DatabaseManager}
        ----------------------
        An instance of the DatabaseManager class.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 06-05-2022 13:52:33
        `memberOf`: colemen_database
        `version`: 1.0
        `method_name`: database
        * @xxx [06-05-2022 13:58:01]: documentation for database
    '''
    db = databaseManager.DatabaseManager()
    name = obj.get_kwarg(['name'],None,(str),**kwargs)
    summary_path = obj.get_kwarg(['summary_path'],None,(str),**kwargs)
    credentials = obj.get_kwarg(['credentials'],None,(dict),**kwargs)
    if name is not None:
        db.name = name
    if credentials is not None:
        db.credentials = credentials
    if summary_path is not None:
        db.load_from_summary(summary_path)
    return db



def new_database():
    return ColemenDatabase()


class ColemenDatabase:
    def __init__(self):
        self.data = {}
        self.table = tableUtils.table_utils(self)
        self.gen = genUtils.generation_utils(self)
        self.con = None
        self.cur = None

        self.data['tables_cols_cache'] = {}

    def connect(self, **kwargs):
        '''
            Sets up the database connection with the initial settings.

            If the DB_PATH is provided, it attempts to connect to an sqlite database.

            If the DB_CREDENTIALS are provided, it attempts to connect to a mysql database.

            ----------

            Keyword Arguments
            -----------------
            `DB_PATH` {string}
                The filepath to the sqlite database

            [`create`=True] {bool}
                If True and SQLite database does not exist yet, create the file.

            `DB_CREDENTIALS` {dict}
                The credentials to connect to the mysql database
                {
                    "user":"string",
                    "password":"string",
                    "host":"string",
                    "database":"string"
                }

            Return {bool}
            ----------
                True upon success, false otherwise.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 04-19-2021 08:04:18
            `version`: 1.0
        '''
        dp_path = obj.get_kwarg(["db_path", "path"], None, str, **kwargs)
        db_creds = obj.get_kwarg(["db_credentials", "credentials", "creds"], None, (dict), **kwargs)
        create = obj.get_kwarg(["create"], True, (bool), **kwargs)
        connect_success = False
        if dp_path is not None:
            if ifFileExists(dp_path) is True or create is True:
                self.data['db_type'] = "SQLITE"
                self.data['db_path'] = dp_path
                if self.__connect_to_sqlite_db() is True:
                    connect_success = True

        if db_creds is not None:
            # if 'DB_CREDENTIALS' in kwargs:
            self.data['db_type'] = "MYSQL"
            self.data['db_credentials'] = db_creds
            if self.__connect_to_my_sqldb() is True:
                connect_success = True

        return connect_success

    def __connect_to_sqlite_db(self):
        '''
                Creates the connection to an sqlite database.

                ----------

                Meta
                ----------
                `author`: Colemen Atwood
                `created`: 04-19-2021 08:08:13
                `memberOf`: colemen_database
                `version`: 1.0
                `method_name`: __connect_to_sqlite_db
        '''
        if 'db_path' in self.data:
            self.data['db_type'] = "SQLITE"
            self.con = sqlite3.connect(self.data['db_path'])
            self.con.row_factory = sqlite3.Row
            self.cur = self.con.cursor()
            return True

        print("No Database Path Provided.")
        return False

    def __validate_db_credentials(self):
        '''
                Validates that all of the db_credentials are provided.

                ----------

                Return {bool}
                ----------------------
                True upon success, false otherwise.

                Meta
                ----------
                `author`: Colemen Atwood
                `created`: 04-19-2021 08:23:40
                `memberOf`: colemen_database
                `version`: 1.0
                `method_name`: __validate_db_credentials
        '''
        if 'db_credentials' in self.data:
            error_array = []
            creds = self.data['db_credentials']
            if 'user' not in creds:
                error_array.append('user is not provided in db_credentials')
            if 'password' not in creds:
                error_array.append('password is not provided in db_credentials')
            if 'host' not in creds:
                error_array.append('host is not provided in db_credentials')
            if 'database' not in creds:
                error_array.append('database is not provided in db_credentials')
            if len(error_array) == 0:
                # print("Successfully validated db_credentials")
                return True
            return False

        print("Credentials are needed to connect to the Mysql Database.")
        return False

    def __connect_to_my_sqldb(self):
        '''
            Attempts to connect to a mysql database.

            ----------

            Return {bool}
            ----------------------
            True upon success, false otherwise.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 04-19-2021 08:23:40
            `memberOf`: colemen_database
            `version`: 1.0
            `method_name`: __connect_to_my_sqldb
        '''
        connect_success = False
        if self.__validate_db_credentials() is True:
            self.data['db_type'] = "MYSQL"
            self.con = None
            try:

                self.con = mysql.connector.connect(
                    user=self.data['db_credentials']['user'],
                    password=self.data['db_credentials']['password'],
                    host=self.data['db_credentials']['host'],
                    database=self.data['db_credentials']['database']
                )
                self.cur = self.con.cursor(
                    buffered=True,
                    dictionary=True
                )

                if self.con.is_connected():
                    # print("Successfully connected to mysql database")
                    connect_success = True

            except Error as error:
                print(error)

            # finally:
            #     if self.con is not None and self.con.is_connected():
            #         self.con.close()

        return connect_success

    def run(self, sql, args=False):
        '''
            Executes a query on the database.

            ----------

            Arguments
            -------------------------
            `sql` {string}
                    The sql query to execute.

            `args` {list}
                    A list of arguments to apply to the sql query

            Return {None}
            ----------------------
            Returns Nothing

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 04-19-2021 10:07:54
            `memberOf`: colemen_database
            `version`: 1.0
            `method_name`: run
        '''
        statements = sql
        # if the sql is a string, split it into a list of statements
        if isinstance(sql, (str)):
            statements = sqlUtils.to_statement_list(sql)

        if len(statements) > 1:
            # print(f"Multiple statements [{len(statements)}] found in sql.")
            for statement in statements:
                # print(f"statement: {statement}")
                self.execute_single_statement(statement, args)

        if len(statements) == 1:
            self.execute_single_statement(sql, args)

    def close(self):
        self.con.close()
        self.con = None
        self.cur = None

    def execute_single_statement(self, sql, args=False):
        '''
            Executes a single SQL query on the database.

            ----------

            Arguments
            -------------------------
            `sql` {string}
                The SQL to be executed.

            `args` {list}
                A list of arguments for parameter substitution.

            Return {bool}
            ----------------------
            True upon success, false otherwise.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 12-09-2021 09:19:40
            `memberOf`: colemen_database
            `version`: 1.0
            `method_name`: execute_single_statement
        '''
        success = False
        if self.cur is None or self.con is None:
            print("Not connected to a database, aborting query.")
            return False
        try:
            if args is False:
                # print(f"executing sql: ",sql)
                self.cur.execute(sql)
            else:
                args = genUtils.sanitize_quotes(args)
                result = self.cur.execute(sql, args)
                # print(f"result: ",result)

            self.con.commit()
            success = True

        except mysql.connector.errors.DatabaseError:
            # print(f"ERROR: {err}", PRESET="FATAL_ERROR_INVERT")
            print(f"{traceback.format_exc()}")
            print(f"SQL: {sql}")

        except sqlite3.Warning as error:
            print(f"Warning: {error}")
            print(traceback.format_exc())

        except sqlite3.OperationalError as error:
            print(f"Fatal Error: {error}")
            print(traceback.format_exc())

        except AttributeError:
            print(f"{traceback.format_exc()}")
            print("")
            print(f"{print(sys.exc_info()[2])}")
            print("")
            print("")
            print(f"SQL: \033[38;2;(235);(64);(52)m{sql}")
        return success

    def runFromList(self, query_list, **kwargs):
        """ DOCBLOCK {
                "class_name":"Database",
                "method_name":"runFromList",
                "author":"Colemen Atwood",
                "created": "04-19-2021 08:04:18",
                "version": "1.0",
                "description":"Executes queries from a list.",
                "arguments":[
                    {
                        "name":"query_list",
                        "type":"list",
                        "description":"The list of sql queries."
                        "is_optional":False
                    },
                    {
                        "name":"DISABLE_KEY_RESTRAINTS",
                        "is_keywarg":True,
                        "type":"boolean",
                        "description":"If True, temporarily disable foreign_key_checks while executing the queries",
                        "is_optional":True
                    }
                ]
            }"""
        disableForeignKeyRestraints = True
        if 'DISABLE_KEY_RESTRAINTS' in kwargs:
            if kwargs['DISABLE_KEY_RESTRAINTS'] is False:
                disableForeignKeyRestraints = False
        if disableForeignKeyRestraints is True:
            self.run("SET foreign_key_checks = 0;")
        for q in query_list:
            self.run(q)

        if disableForeignKeyRestraints is True:
            self.run("SET foreign_key_checks = 1;")

    def runMulti(self, sql, args):
        sql = sql.replace(";", ";STATEMENT_END")
        statements = sql.split('STATEMENT_END')
        for s in statements:
            if len(s) > 0:
                # print(f"query: {s}")
                self.run(s, args)

    def fetchall(self):
        """ DOCBLOCK {
                "class_name":"Database",
                "method_name":"fetchall",
                "author":"Colemen Atwood",
                "created": "04-19-2021 08:04:18",
                "version": "1.0",
                "description":"Executes the fetchall method on the database and converts the result to a dictionary.",
                "returns":{
                    "type":"dict|list",
                    "description":"If there is more than one result, it returns a list of dicts.
                    If there is only one result, it returns a single dictionary."
                }
            }"""
        return self.to_dict(self.cur.fetchall())

    def fetchone(self):
        """ DOCBLOCK {
                "class_name":"Database",
                "method_name":"fetchone",
                "author":"Colemen Atwood",
                "created": "04-19-2021 08:04:18",
                "version": "1.0",
                "description":"Executes the fetchone method on the database.",
                "returns":{
                    "type":"dict",
                    "description":"The result of the fetchone command"
                }
            }"""
        r = self.cur.fetchone()
        return r

    def executeSqlFromFile(self, filePath, **kwargs):
        """ DOCBLOCK {
                "class_name":"Database",
                "method_name":"executeSqlFromFile",
                "author":"Colemen Atwood",
                "created": "04-19-2021 08:04:18",
                "version": "1.0",
                "description":"Executes queries stored in a file.",
                "arguments":[
                    {
                        "name":"filePath",
                        "type":"string",
                        "description":"The filePath to the sql file."
                        "is_optional":False
                    },
                    {
                        "name":"DISABLE_KEY_RESTRAINTS",
                        "is_keywarg":True,
                        "type":"boolean",
                        "description":"If True, temporarily disable foreign_key_checks while executing the queries",
                        "is_optional":True
                    }
                ]
            }"""
        with open(filePath, 'r', encoding='utf-8') as file:
            sql = file.read()
            sql = sql.replace(";", ";STATEMENT_END")
            statements = sql.split('STATEMENT_END')

        # self.run("SET foreign_key_checks=0;")
        # "SOURCE /backups/mydump.sql;" -- restore your backup within THIS session
        # statements = getSQLStatementsFromFile(filePath)
        # print(f"statements: {statements}")
        disableForeignKeyRestraints = True
        if 'DISABLE_KEY_RESTRAINTS' in kwargs:
            if kwargs['DISABLE_KEY_RESTRAINTS'] is False:
                disableForeignKeyRestraints = False
        return self.runFromList(statements, DISABLE_KEY_RESTRAINTS=disableForeignKeyRestraints)
        # self.run("SET foreign_key_checks=1;")

    def to_dict(self, result):
        # print(f"to_dict: resultType: {type(result)}")
        if isinstance(result, list):
            new_data = []
            for row in result:
                tmp = {}
                for col in row.keys():
                    tmp[col] = row[col]
                new_data.append(tmp)
            return new_data
        if isinstance(result, sqlite3.Row):
            new_data = {}
            for col in result.keys():
                new_data[col] = result[col]
            return new_data

    def get_table_names(self):
        return self.table.get_table_names()

    def filter_dict_by_columns(self, data_dict, table_name):
        '''
            Filters a dictionary by the columns in the table specified

            ----------

            Arguments
            -------------------------
            `data_dict` {dict}
                    The dictionary to be filtered.
            `table_name` {string}
                    The name of the table to use as the filter.

            Return {dict}
            ----------------------
            A dictionary with only keys that match columns of the table

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 12-08-2021 10:22:15
            `memberOf`: colemen_database
            `version`: 1.0
            `method_name`: filter_dict_by_columns
        '''
        if table_name not in self.data['tables_cols_cache']:
            self.data['tables_cols_cache'][table_name] = self.table.get_column_array(table_name)
        column_array = self.data['tables_cols_cache'][table_name]
        finalDict = {}
        for c in column_array:
            if c in data_dict:
                finalDict[c] = data_dict[c]
        return finalDict

    def generateColumnInsertString(self, table_name):
        collar = self.table.get_column_array(table_name)
        # print(f"{collar}")

        colStr = self.gen.array_to_list_string(collar, ITEM_WRAP="`", LIST_WRAP="(")
        # print(f"{colStr}")

    def generateColumnValueStrings(self, data):
        # print("---generateColumnValueStrings---")
        returnObj = {}
        returnObj['columnString'] = ""
        returnObj['valueString'] = ""
        totalColumnCount = 0
        totalValueCount = 0
        excludeString = []
        # excludeString = ["user_id", "barn_id"]

        for x, y in data.items():
            # print(f"------{x} - {y} - {type(y)}")
            if isinstance(x, str):
                totalColumnCount += 1
                if x in excludeString:
                    continue
                returnObj['columnString'] += f"{x},"
                if isinstance(y, str):
                    if isBooleanString(y) is True:
                        totalValueCount += 1
                        returnObj['valueString'] += f"{determineBooleanFromString(y)},"
                        continue
                    if y == "NULL":
                        totalValueCount += 1
                        returnObj['valueString'] += "NULL,"
                        continue
                    y = sanitizeQuotes(y)
                    returnObj['valueString'] += f"'{y}',"
                    totalValueCount += 1
                    continue

                if isinstance(y, int):
                    totalValueCount += 1
                    returnObj['valueString'] += f"{y},"
                    continue

                if isinstance(y, bool):
                    totalValueCount += 1
                    returnObj['valueString'] += f"{y},"
                    continue

                if y is None:
                    totalValueCount += 1
                    returnObj['valueString'] += "NULL,"
                    continue

                # returnObj['valueString'] += f"{y},"

        returnObj['columnString'] = stripTrailingComma(returnObj['columnString'])
        returnObj['valueString'] = stripTrailingComma(returnObj['valueString'])

        # print(f"---TotalColumnCount: {totalColumnCount}")
        # print(f"---TotalValueCount: {totalValueCount}")
        # print("---generateColumnValueStrings---")
        return returnObj


def determineBooleanFromString(string):
    if string in ["TRUE", "true", "True", "yes", "y", "1"]:
        return True
    if string in ["FALSE", "false", "False", "no", "n", "0"]:
        return False


def isBooleanString(string):
    if string in ["TRUE", "true", "True", "yes", "y", "1"]:
        return True
    if string in ["FALSE", "false", "False", "no", "n", "0"]:
        return True


def boolToString(string):
    if string in ["TRUE", "true", "True", "yes", "y", "1"]:
        return "111111111"
    if string in ["FALSE", "false", "False", "no", "n", "0"]:
        return "000000000"
    return string


def stripTrailingComma(string):
    return re.sub(",$", "", string)


def stripQuotes(string):
    string = string.replace("'", "")
    string = string.replace('"', "")
    string = string.replace('dWTR7FtHTcNn', "")
    string = string.replace('cURQWIwovfJj', "")
    return string


def sanitizeQuotes(string):
    string = string.replace("'", "dWTR7FtHTcNn")
    string = string.replace('"', "cURQWIwovfJj")
    return string


def stripIndentation(string):
    string = re.sub(r'^\s+', '', string, 0, re.MULTILINE)
    return string


def sanitizeCommas(string):
    string = re.sub(r'\s,', ',', string)
    return string


def stripExcessiveSpaces(string):
    string = re.sub(r'[\s\s]{2,}', ' ', string)
    return string


def ifFileExists(filePath):
    if os.path.isfile(filePath) is True:
        return True
    else:
        return False

# docutils.core.publish_file(
#     source_path=r"K:\OneDrive\Structure\Ra9\2021\21-0058 - DatabasePackage\REV-0001\.venv\docs\main.rst",
#     destination_path=r"K:\OneDrive\Structure\Ra9\2021\21-0058 - DatabasePackage\REV-0001\.venv\docs\main.html",
#     writer_name="html")
