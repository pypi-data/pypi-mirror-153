import datetime
import re
import utils.object_utils as obj
import colemen_file_utils as cfu
import colemen_string_utils as csu
import os
# pylint: disable=too-many-locals
# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring
# pylint: disable=line-too-long





def parse_master_sql(master_path,summary_path=None):
    '''
        Read and parse the master sql file and generate a directory structure that mirrors
        the layout.

        ----------

        Arguments
        -------------------------
        `master_path` {str}
            The path to the master sql file.
        [`summary_path`=None] {str}
            If provided the database summary file will be saved here.

        Return {bool}
        ----------------------
        True upon success, false otherwise.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 04-18-2022 08:46:24
        `memberOf`: parse_master_sql
        `version`: 1.0
        `method_name`: parse_master_sql
        # @xxx [04-18-2022 08:52:57]: documentation for parse_master_sql
    '''

    # print(f"master_path: {master_path}")
    # @Mstep [] confirm that the master sql file exists.
    if cfu.file.exists(master_path) is False:
        print(f"Failed to locate the master sql file {master_path}")
        return False

    # @Mstep [] Gather data about the master sql file.
    master_data = cfu.file.get_data(master_path)

    # @Mstep [] Read the contents of the master sql file.
    master_data['contents'] = cfu.file.read.read(master_path)

    # @Mstep [] parse the schemas from the content.
    master_data = parse_schemas(master_data)

    # @Mstep [] split the content by the tables.
    master_data = split_by_create_table(master_data)

    # @Mstep [] parse each table from the data.
    master_data = parse_tables(master_data)

    # @Mstep [] create each tables directory and sql file.
    master_data = create_tables(master_data)

    if summary_path is not None:
        # @Mstep [] write the summary json file.
        cfu.file.write.to_json(summary_path,master_data)
    return master_data


def parse_tables(file):
    '''
        Parse tables from the master sql 'contents_array' and generate their file paths
        then append the table data to the appropriate schema's "tables" list.

        ----------

        Arguments
        -------------------------
        `file` {dict}
            The dictionary containing the master sql content and meta data.

        Return {dict}
        ----------------------
        The master sql data dictionary with the schemas added.

        {
            "file_path": "Z:\\database\\master.sql",
            "file_name": "master.sql",
            "extension": ".sql",
            "name_no_ext": "master",
            "dir_path": "Z:\\database",
            "access_time": 1650271327,
            "modified_time": 1650271326,
            "created_time": 1646483983,
            "size": 84743,
            "contents": "string",
            "schemas": [
                {
                    "name":"beepBoopBleepBlorp",

                    "file_path":"Z:\\database\\beepBoopBleepBlorp",

                    "dir_path":"Z:\\database",

                    "tables":[
                        {
                            "schema": "idealech_Equari_Content_Database",
                            "name": "smolTittyGothGirl",
                            "sql": "string",
                            "sql_hash": "string",
                            "table_dir_path": "Z:\\database\\beepBoopBleepBlorp\\smolTittyGothGirl",
                            "file_path": "Z:\\database\\beepBoopBleepBlorp\\smolTittyGothGirl\\smolTittyGothGirl.sql"
                        },
                        ...
                    ]
                }
            ],
            ...
        }

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 04-18-2022 09:31:37
        `memberOf`: parse_master_sql
        `version`: 1.0
        `method_name`: parse_tables
        # @xxx [04-18-2022 09:34:10]: documentation for parse_tables
    '''

    # @Mstep [LOOP] iterate the file['contents_array']
    for idx,table_sql in enumerate(file['contents_array']):
        # @Mstep [] parse the schema name and table name.
        schema_table = get_schema_table_name(table_sql)
        # @Mstep [IF] if we successfully parsed the schema and table names.
        if isinstance(schema_table,(tuple)):
            # @Mstep [] generate a dictionary for the table.
            data = {
                'create_order_idx':idx,
                'schema':schema_table[0],
                'name':schema_table[1],
                'sql':''
            }
            # @Mstep [] add the sql and prepend the drop table statement to the data.
            data['sql'] = f"\n\nDROP TABLE IF EXISTS `{schema_table[0]}`.`{schema_table[1]}`;\n{table_sql}"
            data['sql_hash'] = csu.gen.hash(table_sql)
            # @Mstep [] generate the table's sql.
            data = gen_table_sql(data)

            # @Mstep [] add the table dict to the schema's tables array.
            file = add_table_to_schema(file,data)
    # @Mstep [RETURN] return the file data dict.
    return file

def gen_table_sql(table):
    '''
        Appends a header to the sql to let the user know this was auto generated.

        ----------

        Arguments
        -------------------------
        `table` {dict}
            The table's data dictionary.

        Return {dict}
        ----------------------
        The table data dictionary with the updated sql key.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 04-18-2022 09:14:55
        `memberOf`: parse_master_sql
        `version`: 1.0
        `method_name`: gen_table_sql
        # @xxx [04-18-2022 09:16:11]: documentation for gen_table_sql
    '''

    header = '''

-- * ======================= DO NOT MODIFY ======================== *
-- * This file was automatically generated from the master.sql file *
-- * Update the database model and export it to master.sql          *
-- * Then run the command:                                          *
-- * equari parse_master_sql                                        *
-- * ======================= DO NOT MODIFY ======================== *'''
    # @Mstep [] prepend the header text.
    table['sql'] = f"{header}\n{table['sql']}"
    # @Mstep [RETURN] return the table dict.
    return table

def create_tables(file):
    file['auto_updates'] = []

    # @Mstep [LOOP] iterate the master sql's "schemas" array.
    for schema in file['schemas']:
        # @Mstep [] create the schema directory.
        cfu.directory.create(schema['file_path'])
        # @Mstep [LOOP] iterate the tables in the schema's "tables" array.
        for table in schema['tables']:
            # @Mstep [] Create the table's directory.
            cfu.directory.create(table['table_dir_path'])

            if has_table_sql_changed(table):
                file['auto_updates'].append(table)
                # @Mstep [] write the sql file.
                cfu.file.write.write(table['file_path'],table['sql'])

    return file

def has_table_sql_changed(table):
    if cfu.file.exists(table['file_path']) is False:
        return True

    o_sql = cfu.file.read.read(table['file_path'])
    o_hash = csu.gen.hash(o_sql)

    if o_hash != csu.gen.hash(table['sql']):
        return True
    return False

def has_schema(file,name):
    '''
        Check to see if the schema exists in the file['schemas'] list.

        ----------

        Arguments
        -------------------------
        `file` {dict}
            The master sql file dictionary.

        `name` {string}
            The schema name to search for.


        Return {int|bool}
        ----------------------
        The schema's index in file['schemas'] if it is found, false otherwise.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 04-18-2022 09:21:44
        `memberOf`: parse_master_sql
        `version`: 1.0
        `method_name`: has_schema
        # @xxx [04-18-2022 09:23:24]: documentation for has_schema
    '''

    for idx,s in enumerate(file['schemas']):
        if s['name'] == name:
            return idx
    return False

def get_table_sql_hash(file,table,schema):

    # @Mstep [] get the tables schema.
    hs = has_schema(file,schema)
    schema = False
    # @Mstep [IF] if the schema was successfully located.
    if hs is not False:
        # @Mstep [] get the schema data from the master sql file dict.
        schema = file['schemas'][hs]

    if schema is not False:
        for tb in schema['tables']:
            if tb['name'] == table:
                return tb['sql_hash']
    return None

def add_table_to_schema(file,table_data):
    '''
        Generates the tables sql file paths and adds the table dict
        to the appropriate schema's table list.

        ----------

        Arguments
        -------------------------
        `file` {dict}
            The master sql file dictionary.

        `table_data` {dict}
            The table's data dictionary.

        Return {dict}
        ----------------------
        The master sql data dictionary with the schemas added.

        {
            "file_path": "Z:\\database\\master.sql",
            "file_name": "master.sql",
            "extension": ".sql",
            "name_no_ext": "master",
            "dir_path": "Z:\\database",
            "access_time": 1650271327,
            "modified_time": 1650271326,
            "created_time": 1646483983,
            "size": 84743,
            "contents": "string",
            "schemas": [
                {
                    "name":"beepBoopBleepBlorp",

                    "file_path":"Z:\\database\\beepBoopBleepBlorp",

                    "dir_path":"Z:\\database",

                    "tables":[
                        {
                            "schema": "idealech_Equari_Content_Database",
                            "name": "smolTittyGothGirl",
                            "sql": "string",
                            "sql_hash": "string",
                            "table_dir_path": "Z:\\database\\beepBoopBleepBlorp\\smolTittyGothGirl",
                            "file_path": "Z:\\database\\beepBoopBleepBlorp\\smolTittyGothGirl\\smolTittyGothGirl.sql"
                        },
                        ...
                    ]
                }
            ],
            ...
        }

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 04-18-2022 09:27:10
        `memberOf`: parse_master_sql
        `version`: 1.0
        `method_name`: add_table_to_schema
        # @xxx [04-18-2022 09:31:24]: documentation for add_table_to_schema
    '''


    # @Mstep [] get the tables schema.
    hs = has_schema(file,table_data['schema'])
    schema = False
    # @Mstep [IF] if the schema was successfully located.
    if hs is not False:
        # @Mstep [] get the schema data from the master sql file dict.
        schema = file['schemas'][hs]

    # @Mstep [IF] if the schema was successfully retrieved from the master sql dict.
    if schema is not False:
        td = table_data
        # @Mstep [] generate the table_dir_path
        td['table_dir_path'] = csu.format.file_path(f"{schema['file_path']}/{td['name']}")
        # @Mstep [] generate the sql file's file_path
        td['file_path'] = csu.format.file_path(f"{td['table_dir_path']}/{td['name']}.sql")
        # @Mstep [] append the table data dictionary to the schema's tables list.
        file['schemas'][hs]['tables'].append(table_data)
    else:
        print(f"Failed to locate schema: {table_data['schema']}")

    # @Mstep [RETURN] return the file dict.
    return file

def split_by_create_table(file):
    '''
        Split the files contents by the SQLDBM delimiter.

        -- ************************************** `schema_name`.`table_name`

        This essentially creates an array where each indice is the sql creation
        statement for a table.

        ----------

        Arguments
        -------------------------
        `file` {dict}
            The dictionary containing the master sql content and meta data.

        Return {dict}
        ----------------------
        The master sql data dictionary with the schemas added.


        {
            "file_path": "Z:\\Structure\\Ra9\\2022\\22-0018 - equari_server\\database\\master.sql",
            "file_name": "master.sql",
            "extension": ".sql",
            "name_no_ext": "master",
            "dir_path": "Z:\\Structure\\Ra9\\2022\\22-0018 - equari_server\\database",
            "access_time": 1650271327,
            "modified_time": 1650271326,
            "created_time": 1646483983,
            "size": 84743,
            "contents": "string",
            "schemas": [xxx],
            "contents_array":[
                "sql create table statement",
                ...
            ]
        }


        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 04-18-2022 09:01:37
        `memberOf`: parse_master_sql
        `version`: 1.0
        `method_name`: split_by_create_table
        # @xxx [04-18-2022 09:06:52]: documentation for split_by_create_table
    '''
    # c = re.sub(r'-- \*{38} `[^`]*`.`[^`]*`','__TABLE_DIVIDER__',file['contents'])

    # @Mstep [] replace all matching sqldbm delimiters with "__TABLE_DIVIDER__".
    # c = re.sub(r'-- \*{38} `[^`]*`.`[^`]*`','__TABLE_DIVIDER__',file['contents'])
    c = re.sub(r'-- \*{38} (`[^`]*`.)?`[^`]*`','__TABLE_DIVIDER__',file['contents'])
    # @Mstep [] split the contents by "__TABLE_DIVIDER__" and set contents_array
    file['contents_array'] = c.split('__TABLE_DIVIDER__')
    # @Mstep [RETURN] return the file data dict.
    return file

def parse_schemas(file):
    '''
        Parse schemas from the master sql files contents and generate data dicts
        for each one.

        ----------

        Arguments
        -------------------------
        `file` {dict}
            The dictionary containing the master sql content and meta data.

        Return {dict}
        ----------------------
        The master sql data dictionary with the schemas added.

        {
            "file_path": "Z:\\Structure\\Ra9\\2022\\22-0018 - equari_server\\database\\master.sql",
            "file_name": "master.sql",
            "extension": ".sql",
            "name_no_ext": "master",
            "dir_path": "Z:\\Structure\\Ra9\\2022\\22-0018 - equari_server\\database",
            "access_time": 1650271327,
            "modified_time": 1650271326,
            "created_time": 1646483983,
            "size": 84743,
            "contents": "string",
            "schemas": [
                {
                    "name":"beepBoopBleepBlorp",

                    "file_path":"Z:\\Structure\\Ra9\\2022\\22-0018 - equari_server\\database\\beepBoopBleepBlorp",

                    "dir_path":"Z:\\Structure\\Ra9\\2022\\22-0018 - equari_server\\database",

                    "tables":[]
                }
            ],
            ...
        }


        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 04-18-2022 08:56:49
        `memberOf`: parse_master_sql
        `version`: 1.0
        `method_name`: parse_schemas
        # @xxx [04-18-2022 09:01:21]: documentation for parse_schemas
    '''


    # @Mstep [] find all "CREATE SCHEMA" statements in the files contents using regex.
    matches = re.findall(r'CREATE SCHEMA IF NOT EXISTS `([^`]*)`;',file['contents'],re.IGNORECASE)
    file['schemas'] = []
    # @Mstep [IF] if create schema statements are found.
    if matches is not None:
        # @Mstep [IF] if there is atleast one schema
        if len(matches) > 0:
            # @Mstep [LOOP] iterate the schema statements.
            for s in matches:
                # @Mstep [] Create the schema data dictionary.
                schema = {}
                schema['name'] = s
                schema['file_path'] = csu.format.file_path(f"{file['dir_path']}/{s}")
                schema['dir_path'] = file['dir_path']
                schema['tables'] = []

                # if cfu.directory.exists(schema['file_path']) is False:
                    # print(f"Creating schema directory: {schema['file_path']}")
                #     cfu.directory.create(schema['file_path'])
                # @Mstep [] append the schema to the file data dictionary.
                file['schemas'].append(schema)
    # print("schemas: ",matches)
    # @Mstep [RETURN] return the file data dictionary.
    return file

def get_schema_table_name(sql):
    '''
        Parse a table create sql statement to capture the schema name and table name.

        ----------

        Arguments
        -------------------------
        `sql` {string}
            The sql statement to parse.


        Return {bool|tuple}
        ----------------------
        A tuple containing the schema and table name if successful, false otherwise.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 04-18-2022 09:09:08
        `memberOf`: parse_master_sql
        `version`: 1.0
        `method_name`: get_schema_table_name
        # @xxx [04-18-2022 09:10:24]: documentation for get_schema_table_name
    '''


    # @Mstep [] Capture the create table statement schema and table name.
    matches = re.findall(r'CREATE TABLE IF NOT EXISTS `([a-zA-Z_]*)`.`([a-zA-Z_]*)`',sql,re.IGNORECASE)
    # @Mstep [IF] if there is a match.
    if matches is not None:
        # @Mstep [IF] if there is atleast one matching statement.
        if len(matches) > 0:
            m = matches[0]
            # print(f"get_schema_table_name.matches: {m}")
            # @Mstep [return] return a tuple (schema,table)
            return (m[0],m[1])
    # @Mstep [RETURN] return False.
    return False



