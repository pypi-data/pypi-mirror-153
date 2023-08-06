


import re
import os
import time
import sys
# import json

import sqlite3
import mysql.connector
from mysql.connector import Error
import traceback
import utils.generation as genUtils
import utils.table_utils as tableUtils
# from datetime import datetime
# from inspect import getmembers, isfunction
import importlib.util


import colemen_file_utils as cfu
import colemen_string_utils as csu
from colorama import Fore, Style
import utils.object_utils as obj
# import modules.equari.equari_api as api
import utils.TableManager as table_manager
from utils.local_db_management import parse_master_sql

# from typing import TypeVar

# import time

# from parse_sql import sql_to_json
# from reset_table import reset_table
# import utils.inputs as inputs
# from utils import inputs

# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=anomalous-backslash-in-string
# pylint: disable=line-too-long

# table_manager_type = TypeVar('table_manager_type',table_manager.TableManager)



class DatabaseManager:
    def __init__(self,**kwargs):
        # self.main = parent
        self.table_data = None
        self.settings = {
            "setup_complete":False,
            "create_reset_batch_files":True,
            "database_batch_dir":True,
            "master_summary_file_name":"master.summary.json",
            "master_summary_path":f"{os.getcwd()}\\master.summary.json",
            "master_sql_path":f"{os.getcwd()}\\master.sql",
            "database_dir_path":f"{os.getcwd()}\\database",
            "verbose":True,
        }
        self.data = {
            "name":"database",
            "schemas":[],
            "tables":[],
            "insert_data":{
                "default":{},
                "test":{},
            },
            "tables_instances":[],
            "credentials":None,
        }
        # self.settings['setup_complete'] = self.setup()
        self.settings['verbose'] = obj.get_kwarg(['verbose'],False,(bool),**kwargs)
        self.con = None
        self.cur = None

        self.data['tables_cols_cache'] = {}

    def load_from_summary(self,summary_path=None):
        if summary_path is not None:
            if cfu.file.exists(summary_path):
                self.master_summary_path = summary_path
        self.settings['setup_complete'] = self.setup()

    def load_from_master_sql(self,sql_path,create_dir=True,dir_path=None,skip_orphans=True):
        '''
            Load the database from the master sql file.
            This will optionally create the directory structure for the database.

            ----------

            Arguments
            -------------------------
            `sql_path` {str}
                The path to the master sql file to import.

            [`create_dir`=True] {bool}
                If False the directory structure will not be created.

            [`dir_path`=cwd] {str}
                if create_dir is True this is where the directory structure will be created.
                By default that will be the current working directory.

            [`skip_orphans`=True] {bool}
                If False, the orphaned tables will have their table folders created in the root directory.
                "Orphans" are tables that do not belong to a schema, this option is irrelevant if there are
                no schemas.

            Keyword Arguments
            -------------------------
            `arg_name` {type}
                    arg_description

            Return {type}
            ----------------------
            return_description

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 06-01-2022 12:08:43
            `memberOf`: DatabaseManager
            `version`: 1.0
            `method_name`: load_from_master_sql
            * @TODO []: documentation for load_from_master_sql
        '''
        self.parse_master_sql(sql_path,create_dir=create_dir,dir_path=dir_path,skip_no_schema=skip_orphans)

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
        # print(f"{self.data['credentials']}")
        dp_path = obj.get_kwarg(["db_path", "path"], None, str, **kwargs)
        db_creds = obj.get_kwarg(["db_credentials", "credentials", "creds"], self.data['credentials'], (dict), **kwargs)
        create = obj.get_kwarg(["create"], True, (bool), **kwargs)
        connect_success = False
        if dp_path is not None:
            if cfu.file.exists(dp_path) is True or create is True:
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
        if self.con is not None:
            return True
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


    def setup(self):
        settings_defaults ={
            "setup_complete":False,
            "create_reset_batch_files":True,
            "database_batch_dir":True,
            "master_summary_file_name":"master.summary.json",
            "master_summary_path":f"{os.getcwd()}\\master.summary.json",
            "master_sql_path":f"{os.getcwd()}\\master.sql",
            "database_dir_path":f"{os.getcwd()}\\database",
            "verbose":True,
        }

        self.settings = obj.set_defaults(settings_defaults,self.settings)

        success = 0
        indexing = self.index_master()
        if indexing:
            success += 1
            self.gen_insert_data()



        if success == 1:
            print("Database Manager Setup Complete.")
            return True
        return False

    def index_master(self):
        '''
            Index all schemas and database tables that have been parsed.

            ----------

            Return {bool}
            ----------------------
            True upon success, false otherwise.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 05-30-2022 12:35:29
            `memberOf`: DatabaseManager
            `version`: 1.0
            `method_name`: index_master
            @xxx [05-30-2022 12:36:03]: documentation for index_master
        '''

        if cfu.file.exists(self.settings['master_summary_path']) is False:
            print(Fore.RED + f"Could not find {self.settings['master_summary_path']}" + Style.RESET_ALL)
            return False

        master = cfu.file.read.as_json(self.settings['master_summary_path'])
        longest_schema_name = 0
        schemas = []
        tables = []
        for schema in master['schemas']:
            if len(schema['name']) > longest_schema_name:
                longest_schema_name = len(schema['name'])

            schemas.append(schema)
            # @Mstep [LOOP] iterate the tables
            for tb in schema['tables']:
                # tb['default_insert_data'] = self.data['insert_data']['default'][tb['name']]
                tb['default_insert_data'] = obj.get_arg(
                    self.data['insert_data']['default'],
                    [tb['name']],
                    [],
                    (list))
                tb['test_insert_data'] = obj.get_arg(
                    self.data['insert_data']['test'],
                    [tb['name']],
                    [],
                    (list))
                # @Mstep [] instantiate a tablemanager for each table in the database.
                tables.append(table_manager.TableManager(self,tb['name'],None,summary_path=tb))

        self.data['schemas'] = schemas
        self.data['longest_schema_name'] = longest_schema_name
        self.data['tables_instances'] = tables
        # self.data['tables'] = tables
        return True

    def list_schemas(self):
        if self.settings['setup_complete'] is False:
            return False
        # master = cfu.file.read.as_json(f"{os.getcwd()}\\modules\\equari\\parse_master_sql.json")
        print(f"\n{csu.gen.title_divider('Equari Database Schemas')}\n\n")
        total_tables = 0
        for schema in self.data['schemas']:
            print(f"    {schema['name']}")
            total_tables += len(schema['tables'])

        print(f"Total Schemas: {len(self.data['schemas'])}")
        print(f"Total Tables: {total_tables}")
        print(f"\n\n{csu.gen.title_divider('Equari Database Schemas')}\n\n")

    def list_tables(self):
        if self.settings['setup_complete'] is False:
            return False
        print(f"\n{csu.gen.title_divider('Equari Database Tables')}\n\n")
        for table in self.data['tables']:
            print(Fore.RED + f"    {csu.format.rightPad(table.schema(),self.data['longest_schema_name'],' ')}" + Fore.CYAN + f" - {table.table_name}" + Style.RESET_ALL)
        print(f"Total Tables: {len(self.data['tables'])}")
        print(f"\n\n{csu.gen.title_divider('Equari Database Tables')}\n\n")

    def gen_insert_data(self):
        '''
            Iterate all tables to collect the default and test insert data files.
            Then it updates the property self.data['insert_data']

            `insert_data` = {
                `default`:{
                    table_name:[
                        {row_data},
                        ...
                    ]
                },
                `test`:{
                    table_name:[
                        {row_data},
                        ...
                    ]
                }
            }


            ----------

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 06-02-2022 08:24:10
            `memberOf`: DatabaseManager
            `version`: 1.0
            `method_name`: gen_insert_data
            * @xxx [06-02-2022 08:25:28]: documentation for gen_insert_data
        '''


        master_data = {
            "default":{},
            "test":{},
        }
        data = {}
        t:table_manager.TableManager
        for t in self.data['tables_instances']:
            # @Mstep [] get the table's default insert data.
            default_data = t.default_insert_json
            # @Mstep [] assign the data to the master_data dictionary.
            master_data['default'][t.table_name] = default_data


            # @Mstep [] get the table's test insert data.
            test_data = t.test_insert_json
            # @Mstep [] assign the data to the master_data dictionary.
            master_data['test'][t.table_name] = test_data
        
        self.data['insert_data'] = master_data

        # TODO []: remove this, only for testing shit.
        cfu.file.write.to_json("dbman.insert.json",data)
        # self.master_data['default'] = data


    def list_columns(self,table_name):
        t = get_table_by_name(self,table_name)
        cols = t.column_names
        for k in cols:
            print(k)

    def parse_master_sql(self,sql_path=None,**kwargs):
        create_dir = obj.get_kwarg(['create_dir'],True,(bool),**kwargs)
        dir_path = obj.get_kwarg(['dir_path'],None,(str),**kwargs)
        skip_no_schema = obj.get_kwarg(['skip_no_schema'],True,(bool),**kwargs)


        # summary_path = obj.get_kwarg(['summary_path'],None,(str),**kwargs)
        # if summary_path is None:
        #     summary_path = os.path.dirname(sql_path) + "\\" + os.path.basename(sql_path) + ".json"
        # self.settings['master_summary_path'] = os.path.dirname(sql_path) if summary_path is None else summary_path

        # sql_path = self.master_sql_path
        # summary_path = self.master_summary_path
        if sql_path is not None:
            if cfu.file.exists(sql_path):
                self.master_sql_path = sql_path
                self.master_summary_path = os.path.dirname(sql_path) + "\\" + self.settings['master_summary_file_name']


        data = csu.parse.sql.parse(sql_path)
        for t in data['tables']:
            t['name'] = t['table_name']

        for t in data['schemas']:
            t['name'] = t['schema_name']
            del t['schema_name']

        if create_dir:
            self.settings['database_dir_path'] = os.path.dirname(sql_path) if dir_path is None else dir_path
            print(f"self.settings['database_dir_path']:{self.settings['database_dir_path']}")

            data['schemas'] = generate_schema_dirs(self,data['schemas'])
            data['tables'] = generate_table_files(self,data['tables'],skip_no_schema=skip_no_schema)

        self.data['schemas'] = data['schemas']
        self.data['tables'] = data['tables']
        data = organize_summary_tables(data)
        self.save_master_summary()

    def save_master_summary(self):
        '''
            compiles the master summary dictionary and saves it.

            ----------


            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 06-01-2022 11:27:24
            `memberOf`: DatabaseManager
            `version`: 1.0
            `method_name`: save_master_summary
            * @xxx [06-01-2022 11:27:47]: documentation for save_master_summary
        '''
        # @Mstep [] update the tables data dictionary by gathering the summary from all tables. 
        tables = []
        t:table_manager.TableManager
        for t in self.data['tables_instances']:
            tables.append(t.table_summary)
        self.data['tables'] = tables

        data = {
            "name":self.name,
            "schemas":self.data['schemas'],
            "tables":self.data['tables'],
            "insert_data":self.data['insert_data'],
            "orphan_tables":find_orphan_tables(self),
            "database_dir_path":self.settings['database_dir_path'],
            "modified_timestamp":time.time(),
        }

        cfu.file.write.to_json(self.master_summary_path,data)
        # print(f"Saved master summary: {self.master_summary_path}")

    def table(self,name,schema=None)->table_manager.TableManager:
        '''
            Get a table from this database.

            ----------

            Arguments
            -------------------------
            `name` {str}
                The name of the table to retrieve.
            [`schema`=None] {str}
                The schema to search within, if not provided, it will return the first match.

            Return {TableManager|None}
            ----------------------
            The table instance or None.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 06-01-2022 14:05:18
            `memberOf`: DatabaseManager
            `version`: 1.0
            `method_name`: table
            * @TODO []: documentation for table
        '''
        return get_table_by_name(self,name,schema)


    def truncate(self,tables):
        tables = obj.force_list(tables)
        for table in tables:
            tb = self.table(table)
            if tb is not None:
                tb.truncate_table()

    def gen_default_reset(self,tables):
        '''
            Generate the insert sql file and reset the table in the databse.

            ----------

            Arguments
            -------------------------
            `tables` {str|list}
                The table name or list of table names to reset.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 06-02-2022 14:44:02
            `memberOf`: DatabaseManager
            `version`: 1.0
            `method_name`: gen_default_reset
            * @xxx [06-02-2022 14:45:14]: documentation for gen_default_reset
        '''


        tables = obj.force_list(tables)
        for table in tables:
            tb = self.table(table)
            if tb is not None:
                tb.gen_default_reset()

    @property
    def master_summary_path(self):
        '''
            Get the file path for the master sql json summary file.
            This file is generated when an sql file is parsed and the local directory is generated.

            ----------


            Return {str|None}
            ----------------------
            The sql json summary file path if it exists.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 05-31-2022 12:39:59
            `memberOf`: DatabaseManager
            `version`: 1.0
            `method_name`: master_summary_path
            @xxx [05-31-2022 12:41:14]: documentation for master_summary_path
        '''
        return self.settings['master_summary_path']

    @master_summary_path.setter
    def master_summary_path(self,new_path):
        '''
            Set the master sql json summary path.
            This is where the summary file is saved after an sql file is parsed into a directory.

            ----------

            Arguments
            -------------------------
            `new_path` {str}
                The new location to save the json summary.

            Return {str}
            ----------------------
            The new locations path.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 05-31-2022 12:41:26
            `memberOf`: DatabaseManager
            `version`: 1.0
            `method_name`: master_summary_path
            @xxx [05-31-2022 12:43:00]: documentation for master_summary_path
        '''

        self.settings['master_summary_path'] = new_path
        return self.settings['master_summary_path']


    @property
    def master_sql_path(self):
        '''
            Get the file path for the master sql json summary file.
            This file is generated when an sql file is parsed and the local directory is generated.

            ----------


            Return {str|None}
            ----------------------
            The sql json summary file path if it exists.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 05-31-2022 12:39:59
            `memberOf`: DatabaseManager
            `version`: 1.0
            `method_name`: master_sql_path
            @xxx [05-31-2022 12:41:14]: documentation for master_sql_path
        '''
        return self.settings['master_sql_path']

    @master_sql_path.setter
    def master_sql_path(self,new_path):
        '''
            Set the master sql json summary path.
            This is where the summary file is saved after an sql file is parsed into a directory.

            ----------

            Arguments
            -------------------------
            `new_path` {str}
                The new location to save the json summary.

            Return {str}
            ----------------------
            The new locations path.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 05-31-2022 12:41:26
            `memberOf`: DatabaseManager
            `version`: 1.0
            `method_name`: master_sql_path
            @xxx [05-31-2022 12:43:00]: documentation for master_sql_path
        '''

        self.settings['master_sql_path'] = new_path
        return self.settings['master_sql_path']


    @property
    def tables(self):
        '''
            Get the list of tables in this database.

            ----------

            Return {str|None}
            ----------------------
            The sql json summary file path if it exists.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 05-31-2022 12:39:59
            `memberOf`: DatabaseManager
            `version`: 1.0
            `method_name`: tables
            @xxx [05-31-2022 12:41:14]: documentation for tables
        '''
        return self.data['tables']

    def update_table_summary(self,table_name,new_data):
        '''
            Set the master sql json summary path.
            This is where the summary file is saved after an sql file is parsed into a directory.

            ----------

            Arguments
            -------------------------
            `new_path` {str}
                The new location to save the json summary.

            Return {str}
            ----------------------
            The new locations path.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 05-31-2022 12:41:26
            `memberOf`: DatabaseManager
            `version`: 1.0
            `method_name`: tables
            @xxx [05-31-2022 12:43:00]: documentation for tables
        '''

        for t in self.data['tables']:
            if t['name'] == table_name:
                t = {**t,**new_data}
        # self.data['tables'] = new_path
        # return self.data['tables']


    @property
    def schemas(self):
        '''
            Get the list of schemas in this database.

            ----------

            Return {str|None}
            ----------------------
            The sql json summary file path if it exists.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 05-31-2022 12:39:59
            `memberOf`: DatabaseManager
            `version`: 1.0
            `method_name`: schemas
            @xxx [05-31-2022 12:41:14]: documentation for schemas
        '''
        return self.data['schemas']

    @schemas.setter
    def schemas(self,new_path):
        '''
            Set the master sql json summary path.
            This is where the summary file is saved after an sql file is parsed into a directory.

            ----------

            Arguments
            -------------------------
            `new_path` {str}
                The new location to save the json summary.

            Return {str}
            ----------------------
            The new locations path.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 05-31-2022 12:41:26
            `memberOf`: DatabaseManager
            `version`: 1.0
            `method_name`: schemas
            @xxx [05-31-2022 12:43:00]: documentation for schemas
        '''

        self.data['schemas'] = new_path
        return self.data['schemas']


    @property
    def name(self):
        '''
            Get this databases name

            ----------

            Return {str|None}
            ----------------------
            The name of this database.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 05-31-2022 12:39:59
            `memberOf`: DatabaseManager
            `version`: 1.0
            `method_name`: name
            @xxx [05-31-2022 12:41:14]: documentation for name
        '''
        return self.data['name']

    @name.setter
    def name(self,new_name):
        '''
            Set the database name.
            This used for titling summary files.

            ----------

            Arguments
            -------------------------
            `new_name` {str}
                The new name of the database.

            Return {str}
            ----------------------
            The new locations path.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 05-31-2022 12:41:26
            `memberOf`: DatabaseManager
            `version`: 1.0
            `method_name`: name
            @xxx [05-31-2022 12:43:00]: documentation for name
        '''

        self.data['name'] = new_name
        self.settings['master_summary_file_name'] = f"{new_name}.summary.json"
        return self.data['name']

    @name.setter
    def credentials(self,new_creds):
        '''
            Set the database name.
            This used for titling summary files.

            ----------

            Arguments
            -------------------------
            `new_name` {str}
                The new name of the database.

            Return {str}
            ----------------------
            The new locations path.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 05-31-2022 12:41:26
            `memberOf`: DatabaseManager
            `version`: 1.0
            `method_name`: name
            @xxx [05-31-2022 12:43:00]: documentation for name
        '''

        self.data['credentials'] = new_creds
        return self.data['credentials']


    @property
    def insert_data(self):
        '''
            Get this databases insert_data

            ----------

            Return {str|None}
            ----------------------
            The insert_data of this database.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 05-31-2022 12:39:59
            `memberOf`: DatabaseManager
            `version`: 1.0
            `method_insert_data`: insert_data
            @xxx [05-31-2022 12:41:14]: documentation for insert_data
        '''
        if self.data['insert_data'] is None:
            self.gen_insert_data()
        return self.data['insert_data']

    def save(self,gen_insert_sql=True):
        '''
            Save the default insert data for all tables in the database and optionally generate the
            default insert SQL files.

            ----------

            Arguments
            -------------------------
            [`gen_insert_sql`=True] {bool}
                if False, the insert sql file will not be generated and saved.

            Keyword Arguments
            -------------------------
            `arg_name` {type}
                    arg_description

            Return {type}
            ----------------------
            return_description

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 06-01-2022 15:25:56
            `memberOf`: DatabaseManager
            `version`: 1.0
            `method_name`: save
            * @xxx [06-01-2022 15:27:53]: documentation for save
        '''

        t:table_manager.TableManager
        for t in self.data['tables_instances']:
            t.save_insert_data(gen_insert_sql)
            self.save_master_summary()

    @property
    def is_connected(self):
        if self.con is not None:
            return True
        return False


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
            statements = to_statement_list(sql)

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
            if self.data['credentials'] is not None:
                self.connect()
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

    def run_from_list(self, query_list, **kwargs):
        disable_foreign_key_restraints = True
        if 'DISABLE_KEY_RESTRAINTS' in kwargs:
            if kwargs['DISABLE_KEY_RESTRAINTS'] is False:
                disable_foreign_key_restraints = False
        if disable_foreign_key_restraints is True:
            self.run("SET foreign_key_checks = 0;")
        for q in query_list:
            self.run(q)

        if disable_foreign_key_restraints is True:
            self.run("SET foreign_key_checks = 1;")

    def run_multi(self, sql, args):
        sql = sql.replace(";", ";STATEMENT_END")
        statements = sql.split('STATEMENT_END')
        for s in statements:
            if len(s) > 0:
                # print(f"query: {s}")
                self.run(s, args)

    def fetchall(self):
        '''
            Executes the fetchall method on the database and converts the result to a dictionary.

            ----------


            Return {dict|list}
            ----------------------
            If there is more than one result, it returns a list of dicts.
            If there is only one result, it returns a single dictionary.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 06-02-2022 13:58:55
            `memberOf`: DatabaseManager
            `version`: 1.0
            `method_name`: fetchall
            * @xxx [06-02-2022 13:59:37]: documentation for fetchall
        '''
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

    def execute_sql_from_file(self, filePath, **kwargs):
        """ DOCBLOCK {
                "`class_name`":"Database",
                "`method_name`":"execute_sql_from_file",
                "`author`":"Colemen Atwood",
                "`created`": "04-19-2021 08:04:18",
                "`version`": "1.0",
                "`description`":"Executes queries stored in a file.",
                "`arguments`":[
                    {
                        "`name`":"filePath",
                        --------------------------
                        "`type`":"string",
                        "`description`":"The filePath to the sql file."
                        "`is_optional`":False
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
        disable_foreign_key_restraints = True
        if 'DISABLE_KEY_RESTRAINTS' in kwargs:
            if kwargs['DISABLE_KEY_RESTRAINTS'] is False:
                disable_foreign_key_restraints = False
        return self.run_from_list(statements, DISABLE_KEY_RESTRAINTS=disable_foreign_key_restraints)
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


    # def filter_dict_by_columns(self, data_dict, table_name):
    #     '''
    #         Filters a dictionary by the columns in the table specified

    #         ----------

    #         Arguments
    #         -------------------------
    #         `data_dict` {dict}
    #                 The dictionary to be filtered.
    #         `table_name` {string}
    #                 The name of the table to use as the filter.

    #         Return {dict}
    #         ----------------------
    #         A dictionary with only keys that match columns of the table

    #         Meta
    #         ----------
    #         `author`: Colemen Atwood
    #         `created`: 12-08-2021 10:22:15
    #         `memberOf`: colemen_database
    #         `version`: 1.0
    #         `method_name`: filter_dict_by_columns
    #     '''
    #     if table_name not in self.data['tables_cols_cache']:
    #         self.data['tables_cols_cache'][table_name] = self.table.get_column_array(table_name)
    #     column_array = self.data['tables_cols_cache'][table_name]
    #     finalDict = {}
    #     for c in column_array:
    #         if c in data_dict:
    #             finalDict[c] = data_dict[c]
    #     return finalDict

    # def generateColumnInsertString(self, table_name):
    #     collar = self.table.get_column_array(table_name)
    #     # print(f"{collar}")

    #     colStr = self.gen.array_to_list_string(collar, ITEM_WRAP="`", LIST_WRAP="(")
    #     # print(f"{colStr}")

    # def generateColumnValueStrings(self, data):
    #     # print("---generateColumnValueStrings---")
    #     returnObj = {}
    #     returnObj['columnString'] = ""
    #     returnObj['valueString'] = ""
    #     totalColumnCount = 0
    #     totalValueCount = 0
    #     excludeString = []
    #     # excludeString = ["user_id", "barn_id"]

    #     for x, y in data.items():
    #         # print(f"------{x} - {y} - {type(y)}")
    #         if isinstance(x, str):
    #             totalColumnCount += 1
    #             if x in excludeString:
    #                 continue
    #             returnObj['columnString'] += f"{x},"
    #             if isinstance(y, str):
    #                 if isBooleanString(y) is True:
    #                     totalValueCount += 1
    #                     returnObj['valueString'] += f"{determineBooleanFromString(y)},"
    #                     continue
    #                 if y == "NULL":
    #                     totalValueCount += 1
    #                     returnObj['valueString'] += "NULL,"
    #                     continue
    #                 y = sanitizeQuotes(y)
    #                 returnObj['valueString'] += f"'{y}',"
    #                 totalValueCount += 1
    #                 continue

    #             if isinstance(y, int):
    #                 totalValueCount += 1
    #                 returnObj['valueString'] += f"{y},"
    #                 continue

    #             if isinstance(y, bool):
    #                 totalValueCount += 1
    #                 returnObj['valueString'] += f"{y},"
    #                 continue

    #             if y is None:
    #                 totalValueCount += 1
    #                 returnObj['valueString'] += "NULL,"
    #                 continue

    #             # returnObj['valueString'] += f"{y},"

    #     returnObj['columnString'] = stripTrailingComma(returnObj['columnString'])
    #     returnObj['valueString'] = stripTrailingComma(returnObj['valueString'])

    #     # print(f"---TotalColumnCount: {totalColumnCount}")
    #     # print(f"---TotalValueCount: {totalValueCount}")
    #     # print("---generateColumnValueStrings---")
    #     return returnObj
















    # @insert_data.setter
    # def insert_data(self,table,new_data):
    #     '''
    #         Set the database insert_data.
    #         This used for titling summary files.

    #         ----------

    #         Arguments
    #         -------------------------
    #         `new_insert_data` {str}
    #             The new insert_data of the database.

    #         Return {str}
    #         ----------------------
    #         The new locations path.

    #         Meta
    #         ----------
    #         `author`: Colemen Atwood
    #         `created`: 05-31-2022 12:41:26
    #         `memberOf`: DatabaseManager
    #         `version`: 1.0
    #         `method_insert_data`: insert_data
    #         @xxx [05-31-2022 12:43:00]: documentation for insert_data
    #     '''

    #     self.data['insert_data'][table] = new_data













def schema_local_exists(schema):
    if cfu.file.exists(schema['file_path']):
        return True
    return False

def get_table_by_name(main,table_name,schema=None):
    table_name = csu.format.to_snake_case(table_name)
    t:table_manager.TableManager
    for t in main.data['tables_instances']:
        if schema is not None:
            if t['schema_name'] == schema:
                if t.table_name == table_name:
                    return t
        if t.table_name == table_name:
            return t
    return None

def generate_schema_dirs(main,schemas):

    db_path = main.settings['database_dir_path']
    for s in schemas:
        s['dir_path'] = f"{db_path}\\{s['name']}"
        if cfu.directory.exists(s['dir_path']) is False:
            cfu.directory.create(s['dir_path'])
    return schemas


def generate_table_files(main,tables,**kwargs):
    skip_no_schema = obj.get_kwarg(['skip_no_schema'],True,(bool),**kwargs)
    header = obj.get_kwarg(['header'],None,(bool,str),**kwargs)
    drop_table = obj.get_kwarg(['drop_table'],True,(bool),**kwargs)
    db_path = main.settings['database_dir_path']

    # print(f"generate_table_files.db_path: {db_path}")
    new_tables = []
    for t in tables:
        table_name = t['name']
        schema_name = t['schema_name']
        # print(f"t['columns']: {t['columns']}")
        t['modified_timestamp'] = time.time()

        if skip_no_schema is True:
            if schema_name is None:
                continue
        # schema_string = ""
        # if schema_name is not None:
        #     schema_string = f"\\{schema_name}"


        t['db_path'] = db_path
        t['has_test_files'] = False
        tb = table_manager.TableManager(main,table_name,schema_name,summary=t)
        # table_instances.append(tb)
        new_tables.append(tb.table_summary)
        # t['dir_path'] = f"{db_path}{schema_string}\\{table_name}"
        # t['table_dir_path'] = f"{db_path}{schema_string}\\{table_name}"
        # t['create_sql_path'] = f"{db_path}{schema_string}\\{table_name}\\{table_name}.sql"
        # t['table_summary_json_path'] = f"{db_path}{schema_string}\\{table_name}\\{table_name}.summary.json"
        # t['insert_test_data_sql_path'] = f"{db_path}{schema_string}\\{table_name}\\{table_name}.test_data.sql"
        # t['insert_sql_path'] = f"{db_path}{schema_string}\\{table_name}\\{table_name}.insert.sql"
        # t['insert_tmp_sql_path'] = f"{db_path}{schema_string}\\{table_name}\\{table_name}.tmp.sql"
        # t['insert_json_path'] = f"{db_path}{schema_string}\\{table_name}\\{table_name}.json"
        # t['insert_test_data_json_path'] = f"{db_path}{schema_string}\\{table_name}\\{table_name}.test_data.json"
        # t['test_data_batch_path'] = f"{db_path}{schema_string}\\{table_name}\\_{table_name}.reset.test_data.bat"
        # t['reset_batch_path'] = f"{db_path}{schema_string}\\{table_name}\\_{table_name}.reset.bat"
        # t['db_batch_path_test_data'] = f"{db_path}{schema_string}\\{table_name}\\_{table_name}.test_data.bat"
        # t['db_batch_path'] = f"{db_path}{schema_string}\\{table_name}\\{table_name}.test_data.bat"


        # if cfu.directory.exists(t['table_dir_path']) is False:
        #     cfu.directory.create(t['table_dir_path'])


        # sql = t['raw_statement']
        # if drop_table is True:
        #     sql = gen_drop_table(t['name'],t['schema_name'],sql)
        # sql = prepend_header(header,sql)
        # t['content_hash'] = csu.gen.hash(sql)
        # cfu.file.write.write(t['create_sql_path'],sql)
        # cfu.file.write.to_json(t['table_summary_json_path'],t)
    return new_tables


def gen_drop_table(table_name,schema_name=None,sql=None):
    '''
        Generate a drop table statement

        ----------

        Arguments
        -------------------------
        `table_name` {str}
            The name of the table to create a drop statement for.
        [`schema_name`=None] {str}
            The name of the schema the table belongs to.
        [`sql`=None] {str}
            The sql to prepend the drop statement to.

        Return {str}
        ----------------------
        The drop statement if no sql is provided, otherwise The sql with the drop statement prepended.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 06-01-2022 10:12:12
        `memberOf`: DatabaseManager
        `version`: 1.0
        `method_name`: gen_drop_table
        * @xxx [06-01-2022 10:44:44]: documentation for gen_drop_table
    '''
    drop = csu.gen.sql.drop_table(table_name,schema_name)
    if sql is not None:
        return f"\n\n{drop}\n\n{sql}"
    return drop


def prepend_header(header,sql):
    '''
        Append a header to the sql provided.

        ----------

        Arguments
        -------------------------
        `header` {str|bool}
            Rembember! This must be commented as it will be in the sql file!
            The header to apply to the sql or the path to the header file.

            if False, no header will be applied.

        `sql` {str}
            The sql content to prepend the header to.

        Keyword Arguments
        -------------------------
        `arg_name` {type}
                arg_description

        Return {type}
        ----------------------
        return_description

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 06-01-2022 10:02:44
        `memberOf`: DatabaseManager
        `version`: 1.0
        `method_name`: prepend_header
        @xxx [06-01-2022 10:05:18]: documentation for prepend_header
    '''
    if header is False:
        return sql

    default_header = '''

-- * ======================= DO NOT MODIFY ======================== *
-- * This file was automatically generated from the master.sql file *
-- * Update the database model and export it to master.sql          *
-- * ======================= DO NOT MODIFY ======================== *'''
    if isinstance(header,(str)):
        if cfu.file.exists(header) is False:
            default_header = header
        else:
            h =cfu.file.read.read(header)
            if h is not False:
                default_header = h

    # @Mstep [] prepend the header text.
    return f"{default_header}\n{sql}"


def organize_summary_tables(data):
    sorted_tables = []
    for s in data['schemas']:
        s['tables'] = []
        for t in data['tables']:
            if t['schema_name'] == s['name']:
                s['tables'].append(t)
                sorted_tables.append(t['name'])

    data['orphan_tables'] = []
    # print(f"sorted_tables: {sorted_tables}")
    for t in data['tables']:
        if t['name'] not in sorted_tables:
            data['orphan_tables'].append(t)

    del data['tables']
    del data['statements']
    return data

def find_orphan_tables(main):
    '''
        Locates all tables that are not associated to a known schema.

        ----------

        Arguments
        -------------------------
        `arg_name` {type}
                arg_description

        Keyword Arguments
        -------------------------
        `arg_name` {type}
                arg_description

        Return {type}
        ----------------------
        return_description

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 06-01-2022 11:49:06
        `memberOf`: DatabaseManager
        `version`: 1.0
        `method_name`: find_orphan_tables
        * @TODO []: documentation for find_orphan_tables
    '''


    sorted_tables = []
    for s in main.schemas:
        for t in main.tables:
            if t['name'] == s['name']:
                sorted_tables.append(t['name'])

    orphan_tables = []
    # print(f"sorted_tables: {sorted_tables}")
    for t in main.tables:
        if t['name'] not in sorted_tables:
            orphan_tables.append(t)

    # @Mstep [IF] if all tables are orphaned, then None of them are actually orphaned.
    if len(orphan_tables) == len(sorted_tables):
        # @Mstep [RETURN] return an empty list.
        return []
    # @Mstep [RETURN] return the orphan list.
    return orphan_tables



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

def to_statement_list(sql):
    sql = sql.replace(";", ";STATEMENT_END")
    statements = sql.split('STATEMENT_END')
    output = [x.strip() for x in statements if len(x.strip()) > 0]
    return output
# docutils.core.publish_file(
#     source_path=r"K:\OneDrive\Structure\Ra9\2021\21-0058 - DatabasePackage\REV-0001\.venv\docs\main.rst",
#     destination_path=r"K:\OneDrive\Structure\Ra9\2021\21-0058 - DatabasePackage\REV-0001\.venv\docs\main.html",
#     writer_name="html")
