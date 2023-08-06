
import json
import colemen_file_utils as cfu
import utils.object_utils as obj
import colemen_string_utils as csu
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=missing-function-docstring
# pylint: disable=invalid-name
# pylint: disable=line-too-long

class table_utils:
    def __init__(self, db):
        self._data = {}
        self._db = db

    def exists(self, table_name):
        '''
            Checks to see if a table exists in the database.

            ----------

            Arguments
            -------------------------
            `table_name` {string}
                The name of the table to search for.


            Return {bool}
            ----------------------
            True if the table exists, False otherwise.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 12-08-2021 10:28:37
            `memberOf`: colemen_database
            `version`: 1.0
            `method_name`: is_table_in_database
        '''
        return bool(table_name in self.get_table_names())

    def delete(self, table_name):
        '''
            Deletes a table from the database

            ----------

            Arguments
            -------------------------
            `table_name` {string}
                The name of the table to delete.

            Return {type}
            ----------------------
            return_description

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 12-08-2021 12:07:01
            `memberOf`: table_utils
            `version`: 1.0
            `method_name`: delete
        '''
        self._db.run(f"DROP TABLE IF EXISTS `{table_name}`;")
    drop = delete

    def get_table_names(self):
        '''
            Gets all of the table names from the database

            ----------

            Return {list}
            ----------------------
            A list of table names in the database.
            ['some_table','some_other_table']

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 04-19-2021 10:26:13
            `memberOf`: colemen_database
            `version`: 1.0
            `method_name`: get_table_names
        '''
        result = []
        if self._db.data['db_type'] == "SQLITE":
            table_list = self.__sqlite_get_table_names()
            result = [x['name'] for x in table_list]

        if self._db.data['db_type'] == "MYSQL":
            table_list = self.__mysql_get_table_names()
            result = [x['name'] for x in table_list]
        return result

    def __mysql_get_table_names(self):
        '''
            Gets all of the table names from the databse

            Used Specifically for mysql databases.
            ----------

            Return {list}
            ----------------------
            A list of table names in the database.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 04-19-2021 10:26:13
            `memberOf`: colemen_database
            `version`: 1.0
            `method_name`: __mysql_get_table_names
        '''
        tables = []
        self._db.run("SHOW TABLES")
        for table in self._db.fetchall():
            fk = list(table.keys())[0]
            tables.append(table[fk])
        return tables

    def __sqlite_get_table_names(self):
        '''
            Gets all of the table names from the databse

            Used Specifically for sqlite databases.
            ----------

            Return {list}
            ----------------------
            A list of table names in the database.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 04-19-2021 10:26:13
            `memberOf`: colemen_database
            `version`: 1.0
            `method_name`: __sqlite_get_table_names
        '''
        self._db.run("SELECT name FROM sqlite_master WHERE type='table';")
        return self._db.fetchall()

    def get_column_array(self, table_name):
        '''
            Gets an array of column names from the table specified.

            ----------

            Arguments
            -------------------------
            `table_name` {string}
                    The name of the table to query


            Return {list}
            ----------------------
            A list of column names

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 04-19-2021 10:10:06
            `memberOf`: colemen_database
            `version`: 1.0
            `method_name`: get_column_array
        '''
        if self._db.data['db_type'] == "SQLITE":
            return self.__sqlite_get_column_array(table_name)
        if self._db.data['db_type'] == "MYSQL":
            return self.__mysql_get_column_array(table_name)

    def __sqlite_get_column_array(self, table_name):
        '''
            Gets an array of column names from the table specified.

            Specifically, used for sqlite tables.

            ----------

            Arguments
            -------------------------
            `table_name` {string}
                    The name of the table to query

            Return {list}
            ----------------------
            A list of column names

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 04-19-2021 10:12:36
            `memberOf`: colemen_database
            `version`: 1.0
            `method_name`: __sqlite_get_column_array
        '''
        col_names = []
        self._db.run(f"PRAGMA table_info({table_name})")
        res = self._db.cur.fetchall()
        for column in res:
            col_names.append(column['name'])
            # print(a['name'])
        return col_names

    def __mysql_get_column_array(self, table_name):
        '''
            Gets an array of column names from the table specified.

            Specifically used for mysql tables.

            ----------

            Arguments
            -------------------------
            `table_name` {string}
                The name of the table to query

            Return {list}
            ----------------------
            A list of column names

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 04-19-2021 10:15:01
            `memberOf`: colemen_database
            `version`: 1.0
            `method_name`: __mysql_get_column_array
        '''
        col_names = []
        self._db.run(f"desc {table_name};")
        # self._db.run(f"PRAGMA table_info({table_name})")
        res = self._db.cur.fetchall()
        # print(f"res:{res}")
        for column in res:
            col_names.append(column['Field'])
            # print(a['name'])
        return col_names

    def format_table_name(self,name):
        '''
            Formats a table name so that it is wrapped in accents 
            and the schema is separated by a period if present.

            ----------

            Arguments
            -------------------------
            `name` {string}
                The table name (and schema) to format.

            Return {string,boolean}
            ----------------------
            The formatted string if successful, False otherwise

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 04\\10\\2022 13:32:03
            `memberOf`: table_utils
            `version`: 1.0
            `method_name`: format_table_name
            # @TODO []: documentation for format_table_name
        '''
        name = csu.format.strip_any(name,["`",'"',"'"])
        name_list = name.split(".")
        output_name = []
        for n in name_list:
            if len(n) > 0:
                output_name.append(f"`{n}`")
        if len(output_name) > 1:
            return '.'.join(output_name)
        if len(output_name) == 1:
            return output_name[0]
        return False

    def get_column_data_array(self, table_name):
        '''
            Gets all data for each column in the table specified.

            ----------

            Arguments
            -------------------------
            `table_name` {string}
                The name of the table to query

            Return {list}
            ----------------------
            A list of dictionaries containing the column's data.
            Otherwise, it returns an empty list.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 12-08-2021 10:17:18
            `memberOf`: colemen_database
            `version`: 1.0
            `method_name`: get_column_data_array
        '''
        col_data = []
        if self._db.data['db_type'] == "SQLITE":
            col_data = self.__sqlite_get_column_data_array(table_name)
        if self._db.data['db_type'] == "MYSQL":
            col_data = self.__mysql_get_column_data_array(table_name)
        return col_data

    def __sqlite_get_column_data_array(self, table_name):
        '''
            Gets an array of all column data from the SQLite table specified.

            Specifically used for sqlite tables.

            ----------

            Arguments
            -------------------------
            `table_name` {string}
                The name of the table to query.

            Return {list}
            ----------------------
            A list of dictionaries containing the column's data.


            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 12-08-2021 10:19:40
            `memberOf`: colemen_database
            `version`: 1.0
            `method_name`: __sqlite_get_column_data_array
        '''
        cols = []
        self._db.run(f"PRAGMA table_info({table_name})")
        res = self._db.cur.fetchall()
        cols = [self._db.to_dict(x) for x in res]
        return cols

    def __mysql_get_column_data_array(self, table_name):
        '''
            Gets an array of all column data from the MySQL table specified.

            Specifically used for MySQL tables.

            ----------

            Arguments
            -------------------------
            `table_name` {string}
                The name of the table to query.

            Return {list}
            ----------------------
            A list of dictionaries containing the column's data.


            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 12-08-2021 10:19:40
            `memberOf`: colemen_database
            `version`: 1.0
            `method_name`: __mysql_get_column_data_array
        '''
        self._db.run(f"DESCRIBE {table_name};")
        res = self._db.cur.fetchall()
        return res

    def print_columns(self, table_name, name_only=True):
        '''
            Prints each column to the console.

            ----------

            Arguments
            -------------------------
            `table_name` {string}
                The name of the table to query

            [`name_only`=True] {bool}
                If False, all data about the column is printed.

            Return {None}
            ----------------------
            Does not return anything.

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 12-08-2021 10:52:53
            `memberOf`: colemen_database
            `version`: 1.0
            `method_name`: print_columns
        '''
        column_array = self.get_column_data_array(table_name)
        for col in column_array:
            if name_only is True:
                print(f"{table_name} - {col['name']}")
            else:
                print(json.dumps(col, indent=4))

    def get_longest_column_name(self, table_name):
        col_data = self.get_column_data_array(table_name)
        long_len = 0
        long_val = ""
        for col in col_data:
            if len(col['name']) > long_len:
                long_len = len(col['name'])
                long_val = col['name']
        return (long_val, long_len)

    def insert(self, table_name, data):
        '''
            Execute an insert query on the table specified.

            ----------

            Arguments
            -------------------------
            `table_name` {string}
                The name of the table to insert into.
            `data` {string|dict|list}
                If data is a string:
                    It is treated as an sql query and executed exactly as provided.

                If data is a dict:
                    The dictionary is filtered by its keys and the values are inserted.

                If data is a list of dictionaries:
                    Each dictionary is filtered and inserted into the table.

            Return {type}
            ----------------------
            return_description

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 12-08-2021 14:27:14
            `memberOf`: table_utils
            `version`: 1.0
            `method_name`: insert
        '''
        insert_multi = False
        if isinstance(data, (str)):
            data = [data]
        if isinstance(data, (list, dict)):
            if isinstance(data, (list)):
                new_data = []
                for row in data:
                    if isinstance(row, (dict)):
                        new_data.append(self._db.filter_dict_by_columns(row, table_name))
                data = new_data
                if len(data) > 1:
                    insert_multi = True
            if isinstance(data, (dict)):
                data = [self._db.filter_dict_by_columns(data, table_name)]

        if insert_multi is True:
            values_list = []
            keys = obj.get_unique_keys(data)
            column_list = self._db.gen.array_to_list_string(keys, ITEM_WRAP="", LIST_WRAP="(")
            sql = f"INSERT INTO `{table_name}` {column_list} VALUES \n"
            for row in data:
                if isinstance(row, (dict)):
                    values_list.append(self._db.gen.array_to_list_string([f"{row[x]}" if x in row else None for x in keys], ITEM_WRAP="AUTO", LIST_WRAP="("))
            values_string = ",\n".join(values_list)
            sql += f"{values_string};"

            cfu.file.write.write("temp.sql", sql)
            return self._db.run(sql)

        for row in data:
            if isinstance(row, (str)):
                self._db.run(row)
            if isinstance(row, (dict)):
                keys = obj.get_unique_keys(row)
                column_list = self._db.gen.array_to_list_string(keys, ITEM_WRAP="", LIST_WRAP="(")
                newlist = self._db.gen.array_to_list_string([f"{row[x]}" for x in keys], ITEM_WRAP="AUTO", LIST_WRAP="(")
                sql = f"INSERT INTO `{table_name}` {column_list}\n VALUES {newlist}"
                # print(sql)
                return self._db.run(sql)
