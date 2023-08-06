


# import re
import os
import json
# import shlex
# from datetime import datetime
# from inspect import getmembers, isfunction
# import importlib.util
# import json
# import sys

from typing import TYPE_CHECKING
import colemen_file_utils as cfu
import colemen_string_utils as csu
import utils.object_utils as obj
# import time

# from parse_sql import sql_to_json
# from reset_table import reset_table
# import utils.inputs as inputs
# from utils import inputs

# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=anomalous-backslash-in-string
# pylint: disable=line-too-long
# pylint: disable=import-outside-toplevel







class TableDataManager:
    def __init__(self,database,table,**kwargs):
        self.db = database
        self.table = table
        self.settings = {}
        self.data = {}

        self.insert_type = obj.get_kwarg(['insert_type'],"default",(str),**kwargs)
        self.set_defaults()

    def set_defaults(self):
        self.settings = self.table.settings

    # TODO []: import default data json file

    def import_data(self,ignore_errors=False):
        '''
            Reads the table's insert json file and returns the contents.

            ----------

            Arguments
            -------------------------

            [`ignore_errors`=False] {bool}
                If True, the errors will not printed to the console.

            Return {list}
            ----------------------
            The contents of the insert json file, which should be a list..
            If the file does not exist it will return an empty list.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 05-21-2022 13:04:36
            `memberOf`: TableManager
            `version`: 1.0
            `method_name`: import_default_json_data
            # @xxx [05-21-2022 13:05:43]: documentation for import_default_json_data
        '''
        path = self.data_path
        result = []

        if isinstance(path,(str)):
            if cfu.file.exists(path):
                result = cfu.file.read.as_json(path)
        else:
            if ignore_errors is False:
                print(f"Failed to locate the insert json file for table {self.name}")
                print(f"File path: {path}")

        return result

    # TODO []: save default data json file

    def save(self,gen_sql=True):
        '''
            Save the insert data to the insert json file.

            ----------

            Arguments
            -------------------------
            [`gen_sql`=True] {bool}
                If True, it will generate the insert SQL and save it as well.


            Return {bool}
            ----------------------
            True upon success, false otherwise.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 06-01-2022 15:23:15
            `memberOf`: TableManager
            `version`: 1.0
            `method_name`: save
            * @xxx [06-01-2022 15:23:45]: documentation for save
        '''

        idata = self.insert_data
        path = self.data_path

        if isinstance(idata,(list)) is False:
            return False

        # @Mstep [IF] if the data is empty.
        if len(idata) == 0:
            # @Mstep [IF] if the json file already exists
            if cfu.file.exists(path):
                # @Mstep [] delete the json file
                self.delete_json_data()
                # @Mstep [] delete the sql file.
                self.delete_sql_insert()
            return True

        if path is not None:
            cfu.file.write.to_json(path,idata)
            if gen_sql:
                self.gen_sql_insert()
            return True
        return False

    # TODO []: insert a single row into the default data.



    # # TODO []: set value of the data json file

    # def set_data(self,data=None):
    #     # @Mstep [IF] if data is None
    #     if data is None:
    #         # @Mstep [] set the insert data to an empty list.
    #         self.db.insert_data[self.name] = []
    #         # @Mstep [RETURN] return True
    #         return True

    #     if isinstance(data,(dict)):
    #         data = [data]

    #     self.db.insert_data[self.name] = []

    # xxx [06-02-2022 09:29:14]: generate the data insert SQL file

    def truncate(self):
        print(f"truncating table: {self.name}")
        self.db.connect()
        # @Mstep [] execute the create table sql which will essentially truncate it and add new columns.
        self.db.execute_sql_from_file(self.create_sql_path)

    def reset_table(self):
        sql = self.insert_sql
        if TYPE_CHECKING:
            from utils.DatabaseManager import DatabaseManager as db
            self.db:db

        if isinstance(sql,(str)):
            self.db.connect()
            # @Mstep [] execute the create table sql which will essentially truncate it and add new columns.
            self.db.execute_sql_from_file(self.create_sql_path)
            # @Mstep [] execute the insert sql
            self.db.execute_sql_from_file(self.insert_path)
            # print(f"boobs")
        return


    def gen_sql_insert(self):
        '''
            Generate the insert sql for the data.

            ----------

            Return {bool}
            ----------------------
            True upon success, false otherwise.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 06-02-2022 09:27:32
            `memberOf`: TableDataManager
            `version`: 1.0
            `method_name`: gen_sql_insert
            * @xxx [06-02-2022 09:28:12]: documentation for gen_sql_insert
        '''


        data = self.insert_data
        path = self.insert_path

        if isinstance(data,(list)) is False:
            print("Invalid insert data, it must be a list of dictionaries.")
            return False

        if len(data) == 0:
            # @Mstep [] delete the sql file.
            self.delete_sql_insert()
            return True

        sql = csu.gen.sql.insert_sql(data,self.name,self.schema)
        if sql:
            cfu.file.write.write(path,sql)
            return True

    def delete_data(self):
        self.delete_sql_insert()
        self.delete_json_data()

    def delete_sql_insert(self):
        '''
            Delete the sql insert file.

            ----------

            Return {bool}
            ----------------------
            True upon success, false otherwise.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 06-02-2022 09:38:43
            `memberOf`: TableDataManager
            `version`: 1.0
            `method_name`: delete_sql_insert
            * @xxx [06-02-2022 09:39:07]: documentation for delete_sql_insert
        '''


        path = self.insert_path
        if cfu.file.exists(path):
            return cfu.file.delete(path)
        return True

    def delete_json_data(self):
        '''
            Delete the json data file.

            ----------

            Return {bool}
            ----------------------
            True upon success, false otherwise.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 06-02-2022 09:38:43
            `memberOf`: TableDataManager
            `version`: 1.0
            `method_name`: delete_json_data
            * @xxx [06-02-2022 09:39:07]: documentation for delete_json_data
        '''
        path = self.data_path
        if cfu.file.exists(path):
            return cfu.file.delete(self.data_path)
        return True


    # TODO []: delete the default data json file

    # def generate_insert(self,insert_path=None,json_path=None,test=False):
    #     # if cfu.file.exists(self.settings["table_py_path"]):

    #     if insert_path is None:
    #         insert_path = self.settings['insert_sql_path']
    #         if test:
    #             insert_path = self.settings['insert_test_data_sql_path']

    #     if json_path is None:
    #         json_path = self.settings['insert_json_path']
    #         if test:
    #             json_path = self.settings['insert_test_data_json_path']

    #     # json_path = self.settings['insert_json_path']
    #     idata = cfu.file.read.as_json(json_path)
    #     if isinstance(idata,(list)):
    #         if len(idata) > 0:
    #             # insert_path = self.settings['insert_sql_path']
    #             sql = ''
    #             value_array = []
    #             columns = _get_all_columns(idata)
    #             for row in idata:
    #                 value_array.append(_gen_value_string(row,columns))
    #             column_string = _gen_column_string(columns)
    #             value_string = ',\n'.join(value_array)
    #             value_string = value_string.replace("'__NULL_VALUE__'",'null')
    #             value_string = value_string.replace("__NULL_VALUE__",'null')

    #             # @Mstep [] generate the schema string, this is for cases where a table has no schema.
    #             schema_string = ''
    #             if self.schema is not None:
    #                 schema_string = f"`{self.schema}`."

    #             sql += f"INSERT INTO {schema_string}`{self.name}` ({column_string}) VALUES \n"
    #             sql += f"{value_string};"

    #             cfu.file.write.write(insert_path,sql)
    #             # if test:
    #             #     self.test_data_batch()
    #             # else:
    #             #     self.generate_reset_batch()
    #             return True
    #     return False


    # def insert_default_data(self,data):
    #     '''
    #         Insert a new row or rows into the default data json file.

    #         ----------

    #         Arguments
    #         -------------------------
    #         `data` {dict|list}
    #             A dictionary or list of dictionaries to insert.
    #             Keys must correspond to the column in the table, they are case sensitive.
    #             This does `NOT` type match the columns, so if you fuck it up, its on you.

    #         Return {type}
    #         ----------------------
    #         return_description

    #         Meta
    #         ----------
    #         `author`: Colemen Atwood
    #         `created`: 06-01-2022 15:14:20
    #         `memberOf`: TableManager
    #         `version`: 1.0
    #         `method_name`: insert_default_data
    #         * @xxx [06-01-2022 15:16:46]: documentation for insert_default_data
    #     '''


    #     # self.main.insert_data()
    #     if isinstance(data,(list)) is False:
    #         data = [data]
    #     pri = self.primary
    #     # print(f"self.table_meta_data:{self.table_meta_data}")
    #     # print(f"pri: {pri}")


    #     rows = []
    #     for d in data:
    #         # print(f"d: {d}")
    #         row = d
    #         for c in self.column_names:
    #             if c in d:
    #                 if c == pri:
    #                     if d[c] is None:
    #                         row[c] = len(self.main.insert_data[self.name]) + 1
    #                         continue
    #                 row[c] = d[c]
    #             else:
    #                 if c == pri:
    #                     row[c] = len(self.main.insert_data[self.name]) + 1
    #                     continue
    #                 row[c] = None

    #         if has_required_columns(self,row,True):
    #             rows.append(row)

    #     if len(rows) > 0:
    #         inserts = self.main.insert_data[self.name]
    #         inserts = inserts + rows
    #         self.main.data['insert_data'][self.name] = inserts

    # def set_default_data(self,data):
    #     if isinstance(data,(list)) is False:
    #         data = [data]


    # def save_default_insert_json(self):
    #     '''
    #         Save the default insert data to the insert json file.

    #         ----------

    #         Meta
    #         ----------
    #         `author`: Colemen Atwood
    #         `created`: 06-01-2022 15:23:15
    #         `memberOf`: TableManager
    #         `version`: 1.0
    #         `method_name`: save_default_insert_json
    #         * @xxx [06-01-2022 15:23:45]: documentation for save_default_insert_json
    #     '''

    #     idata = self.main.insert_data[self.name]
    #     save_default_insert_json(self,idata)


    # def import_default_json_data(self,ignore_errors=False):
    #     '''
    #         Reads this table's insert json file and returns the contents.

    #         ----------

    #         Return {list|bool}
    #         ----------------------
    #         The contents of the insert json file, which should be a list..
    #         If the file does not exist it will return False.

    #         Meta
    #         ----------
    #         `author`: Colemen Atwood
    #         `created`: 05-21-2022 13:04:36
    #         `memberOf`: TableManager
    #         `version`: 1.0
    #         `method_name`: import_default_json_data
    #         # @xxx [05-21-2022 13:05:43]: documentation for import_default_json_data
    #     '''


    #     if cfu.file.exists(self.settings['insert_json_path']):
    #         return cfu.file.read.as_json(self.settings['insert_json_path'])
    #     else:
    #         if ignore_errors is False:
    #             print(f"Failed to locate the insert json file for table {self.settings['table_name']}")
    #             print(f"File path: {self.settings['insert_json_path']}")
    #         return False
    #     return False

    # def save_json(self,name,data):
    #     if name in self.settings:
    #         cfu.file.write.to_json(self.settings[name],data)
    #         return True
    #     return False

    # def insert_from_sql(self,sql_path=None):
    #     '''
    #         Execute an insert statement on the database from an sql file.

    #         ----------

    #         Arguments
    #         -------------------------
    #         [`sql_path`=None] {string}
    #             The path to the sql file to insert, if not provided the table's default insert sql is used.

    #         Return {type}
    #         ----------------------
    #         return_description

    #         Meta
    #         ----------
    #         `author`: Colemen Atwood
    #         `created`: 05-12-2022 10:11:00
    #         `memberOf`: TableManager
    #         `version`: 1.0
    #         `method_name`: insert_from_sql
    #         # @xxx [05-12-2022 10:12:37]: documentation for insert_from_sql
    #     '''

    #     if sql_path is None:
    #         sql_path = self.settings['insert_sql_path']

    #     if cfu.file.exists(sql_path):
    #         # sql = cfu.file.read.read(sql_path)
    #         db = self.main.connect_to_db()
    #         result = db.executeSqlFromFile(sql_path)

    # def get_current_contents(self):
    #     db = self.main.connect_to_db()
    #     db.run(f"SELECT * from `{self.table_data['schema']}`.`{self.table_data['name']}`;")
    #     result = db.fetchall()
    #     db.close()
    #     return result


    # def list_local_values(self,key=None):
    #     data = self.import_default_json_data()
    #     divider = csu.gen.title_divider(self.settings['table_name'])
    #     print(f"{divider}\n")
    #     for x in data:
    #         if key is not None:
    #             if key in x:
    #                 print(f"    {x[key]}")

    #     print(f"\n{divider}")

    # def get_row(self,column,value):
    #     data = self.import_default_json_data()
    #     # divider = csu.gen.title_divider(self.settings['table_name'])
    #     # print(f"{divider}\n")
    #     for x in data:
    #         if column in x:
    #             if x[column] == value:
    #                 return x
    #     return False




    def setting(self,key,default=None):
        return obj.get_arg(self.settings,key,default)

    @property
    def insert_data(self):
        '''
            Retrieves the insert data for this table depending on the insert_type

            ----------

            Return {type}
            ----------------------
            return_description

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 06-02-2022 08:41:06
            `memberOf`: TableDataManager
            `version`: 1.0
            `method_name`: insert_data
            * @TODO []: documentation for insert_data
        '''
        return self.db.insert_data[self.insert_type][self.name]

    
    def set_insert_data(self,data):
        '''
            Set the insert data for the table.

            ----------

            Arguments
            -------------------------
            `data` {list|dict|None}
                The insert data.
                `!!! CAUTION !!!`
                If data is None, the insert data is reset to an empty list.

                If a list of dictionaries is provided, the dictionaries are appended as rows to the insert data.

                If a dictionary is provided, the data is appended as a new row to the insert data.

            Return {bool}
            ----------------------
            True upon success, false otherwise.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 06-02-2022 09:44:54
            `memberOf`: TableDataManager
            `version`: 1.0
            `method_name`: insert_data
            * @xxx [06-02-2022 09:45:42]: documentation for insert_data
        '''


        # @Mstep [IF] if data is None
        if data is None:
            # @Mstep [] set the insert data to an empty list.
            self.db.insert_data[self.name] = []
            self.save(True)
            # @Mstep [RETURN] return True
            return True

        data = obj.force_list(data)
        primary_col_name = self.primary
        # print(f"self.table_meta_data:{self.table_meta_data}")
        # print(f"pri: {pri}")


        rows = []
        # @Mstep [LOOP] iterate the rows in the data provided.
        for row in data:
            # print(f"d: {d}")
            # @Mstep [LOOP] iterate the columns of the table.
            for col_name in self.table.column_names:
                # @Mstep [IF] if the column is the primary key.
                if col_name == primary_col_name:
                    # @Mstep [IF] if the row's value is None.
                    if row[col_name] is None:
                        # @Mstep [] set the value to the next available id.
                        row[col_name] = self.next_id
                        # @Mstep [] continue to the next column
                        continue
                # @Mstep [IF] if the column name is a key in the row dictionary.
                if col_name in row:
                    # TODO []: create a type validation for the row value.
                    continue
                # @Mstep [ELSE] if the column name is not a key in the row dictionary.
                else:
                    # @Mstep [] set the column name as a key on the row dict and its value is None
                    row[col_name] = None

            # @Mstep [IF] if all required columns have a value other than None in the row dictionary
            if has_required_columns(self.table,row,True):
                # @Mstep [] append the row to the rows list.
                rows.append(row)

        # @Mstep [] if the rows list contains at least one row.
        if len(rows) > 0:
            cur_idata = self.insert_data
            # @Mstep [] append the rows to the tables insert data list.
            cur_idata = cur_idata + rows
            # @Mstep [] update the master insert data dict with the new data.
            if self.insert_type == "default":
                self.table.data['default_insert_data'] = cur_idata
            if self.insert_type == "test":
                self.table.data['test_insert_data'] = cur_idata
            # self.db.insert_data[self.insert_type][self.name] = cur_idata
            self.db.insert_data[self.insert_type][self.name] = cur_idata
            self.db.save()
            # @Mstep [] save the insert json file and generate the insert SQL.
            return self.save(True)

    @property
    def data_path(self):
        if self.insert_type == "default":
            return obj.get_arg(self.settings,'insert_json_path',None)
        if self.insert_type == "test":
            return obj.get_arg(self.settings,'insert_test_data_json_path',None)

    @property
    def insert_path(self):
        if self.insert_type == "default":
            return obj.get_arg(self.settings,'insert_sql_path',None)
        if self.insert_type == "test":
            return obj.get_arg(self.settings,'insert_test_data_sql_path',None)

    @property
    def next_id(self):
        '''
            Get the next auto_increment id for this table.

            ----------

            Return {int}
            ----------------------
            The next available integer id for the table.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 06-02-2022 09:49:49
            `memberOf`: TableDataManager
            `version`: 1.0
            `method_name`: next_id
            * @xxx [06-02-2022 09:50:50]: documentation for next_id
        '''


        data = self.insert_data
        return len(data) + 1

    @property
    def primary(self):
        return get_primary_column(self)

    @property
    def table_name(self):
        return self.table.table_name

    @property
    def name(self):
        return self.table.name



    @property
    def insert_json(self):
        '''
            Import the insert json file and return the contents.

            ----------

            Return {list}
            ----------------------
            The insert contents which must be a list.
            If it does not exist or the contents are invalid the list is empty.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 06-02-2022 09:47:54
            `memberOf`: TableDataManager
            `version`: 1.0
            `method_name`: insert_json
            * @xxx [06-02-2022 09:49:00]: documentation for insert_json
        '''

        data = []
        if cfu.file.exists(self.data_path):
            res = cfu.file.read.as_json(self.data_path)
            if isinstance(res,(list)):
                data = res
        return data

    @property
    def create_sql_path(self):
        return self.settings['create_sql_path']

    @property
    def insert_sql(self):
        if cfu.file.exists(self.create_sql_path):
            return cfu.file.read.read(self.create_sql_path)
        return None

    @property
    def schema(self):
        '''
            Get the name of the schema that the table belongs to.

            ----------

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 06-02-2022 08:48:02
            `memberOf`: TableDataManager
            `version`: 1.0
            `method_name`: schema
            * @xxx [06-02-2022 08:48:37]: documentation for schema
        '''

        return self.table.schema

    @property
    def column_names(self):
        cols:list = self.table_meta_data
        names = []
        col_data:dict
        for col_data in cols:
            names.append(col_data['name'])
        return names

    @property
    def table_meta_data(self)->list:
        if isinstance(self.table.data['columns'],(list)):
            if len(self.table.data['columns']) == 0:
                self.table.data['columns'] = None

        if self.table.data['columns'] is None:
            # @Mstep [IF] if the create sql file does not exist, we cannot parse it.
            if self.table.create_sql_exists is False:
                # @Mstep [return] return an empty list.
                return []
            # @Mstep [] read the create file sql
            sql = cfu.file.read.read(self.create_sql_path)
            # @Mstep [] parse the sql for table data.
            create_file_data:dict = csu.parse.sql.parse(sql)
            # @Mstep [] if we successfully parse the create file.
            if isinstance(create_file_data,(dict)):
                # @Mstep [] update the table's data with the newly parsed data.
                self.table.data = {**self.table.data,**create_file_data}
                # @Mstep [RETURN] return the columns key of the tables data dict.
                return self.table.data['columns']
            return []
            # self.table.data['columns'] = self.data['create_file_data']['columns']
            # cfu.file.write.to_json("col_data.delete.json",col_data)
        else:
            return self.table.data['columns']

def get_column_by_name(table,col):
    for c in table.data['column_data']:
        if c['name'] == col:
            return c
    return None

def get_primary_column(table):
    for c in table.table_meta_data:
        if c['is_primary_key'] is True or c['primary_key'] is True:
            return c['name']
    return None

def allow_null(table,column):
    for c in table.table_meta_data:
        if c['allow_nulls'] is True:
            return True
    return False

def has_required_columns(table,row,print_errors=True):
    '''
        validate a dictionary to confirm each column that does not allow nulls
        has a value.

        ----------

        Arguments
        -------------------------
        `table` {TableManager}
            A reference to the table manager instance.
        `row` {dict}
            The data dictionary to validate.
        [`print_errors`=True] {bool}
            If False it will just return False and not print the warning.

        Return {bool}
        ----------------------
        True upon success, false otherwise.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 06-01-2022 15:18:30
        `memberOf`: TableManager
        `version`: 1.0
        `method_name`: has_required_columns
        * @xxx [06-01-2022 15:20:28]: documentation for has_required_columns
    '''


    for k,v in row.items():
        if v is None:
            if allow_null(table,k) is False:
                if print_errors:
                    print(f"{k} is a required column in {table.name}, None was provided.")
                return False
    return True

def insert_single_row(table,data):
    '''
        Insert a new row or rows into the default data json file.

        ----------

        Arguments
        -------------------------
        `data` {dict|list}
            A dictionary or list of dictionaries to insert.
            Keys must correspond to the column in the table, they are case sensitive.
            This does `NOT` type match the columns, so if you fuck it up, its on you.

        Return {type}
        ----------------------
        return_description

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 06-01-2022 15:14:20
        `memberOf`: TableManager
        `version`: 1.0
        `method_name`: insert_default_data
        * @xxx [06-01-2022 15:16:46]: documentation for insert_default_data
    '''


    # self.main.insert_data()
    data = obj.force_list(data)
    primary_col_name = table.primary
    # print(f"self.table_meta_data:{self.table_meta_data}")
    # print(f"pri: {pri}")


    rows = []
    for row in data:
        # print(f"d: {d}")
        for col_name in table.column_names:
            if col_name in row:
                if col_name == primary_col_name:
                    if row[col_name] is None:
                        row[col_name] = len(table.main.insert_data[table.name]) + 1
                        continue
                row[col_name] = row[col_name]
            else:
                if col_name == primary_col_name:
                    row[col_name] = len(table.main.insert_data[table.name]) + 1
                    continue
                row[col_name] = None

        if has_required_columns(table,row,True):
            rows.append(row)


# TODO []: set defaults per column on a dictionary.
# def set_default_values(table,data):

#     for c in table.data['column_data']:
#         if c['is_primary_key'] is True:
#             return c['name']
#     return None

def has_column(table,col):
    for c in table.data['column_data']:
        if c['name'] == col:
            return True
    return False

def validate_row_types(table,data):
    new_data = {}
    for c in table.data['column_data']:
        val = None
        if c['name'] in data:
            val = data[c]
        if val is None:
            if c['allow_nulls'] is True:
                new_data[c['name']] = data[c]

        sql_type = csu.convert.sql.sql_type_to_python(c['type'])
        if sql_type is not None:
            if str(type(val).__name__) in sql_type:
                new_data[c['name']] = data[c]
            else:
                if "bool" in sql_type:
                    bool_val = csu.convert.to_bool(val)
                    new_data[c['name']] = bool_val
                    continue

# def save_default_insert_json(table,data):
#     cfu.file.write.to_json(table.settings['insert_json_path'],data)





