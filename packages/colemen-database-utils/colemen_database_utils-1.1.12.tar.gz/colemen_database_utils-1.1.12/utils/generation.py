import datetime
import re
import utils.object_utils as obj
import colemen_file_utils as fileUtils

# pylint: disable=too-many-locals




class generation_utils:
    def __init__(self, db):
        self._data = {}
        self._db = db

    def sql_from_table(self, table_name):
        if self._db.data['db_type'] == "SQLITE":
            if self._db.table.exists(table_name) is True:
                return self.sql_table_create(table_name)
        if self._db.table.exists(table_name) is True:
            timestamp = datetime.datetime.now().strftime("%m-%d-%Y %H:%M:%S")
            data = f"-- ************************************** `{table_name}` - {timestamp} - CREATE START\n\n"
            data += "DROP TABLE IF EXISTS `" + str(table_name) + "`;\n\n"

            self._db.run("SHOW CREATE TABLE `" + str(table_name) + "`;")
            result = self._db.cur.fetchone()
            # print(f"result: ")
            # print(result)
            data += str(result['Create Table'])
            data += ";\n\n"

            data = data.replace("CREATE TABLE", "CREATE TABLE IF NOT EXISTS")
            data = re.sub(r'\)\sENGINE=[^;]*;', ');', data)

            data += f"-- ************************************** `{table_name}` - {timestamp} - CREATE END\n\n"

            data += f"-- ************************************** `{table_name}` - {timestamp} - INSERT START\n"
            column_list = self.array_to_list_string(self._db.table.get_column_array(table_name), ITEM_WRAP="`", LIST_WRAP="(")
            data += f"INSERT INTO `{table_name}` \n{column_list} VALUES \n"
            # print(f"{data}", COLOR="BLUE", BGCOLOR="BLACK", INCDEC=True)

            self._db.run("SELECT * FROM `" + str(table_name) + "`;")
            rows = self._db.fetchall()
            row_len = len(rows) - 1
            rc = 0
            for row in rows:
                list_suffix = "),\n"
                if rc == row_len:
                    list_suffix = ");\n"
                # print(f"{row}", COLOR="GREEN", BGCOLOR="BLACK", INCDEC=True)
                data += self.array_to_list_string(list(row.values()), ITEM_WRAP="AUTO", LIST_PREFIX="(", LIST_SUFFIX=list_suffix)
                rc += 1
            data += f"-- ************************************** `{table_name}` - {timestamp} - INSERT END"
            data += "\n\n\n\n"

            return data
            # print(f"{data}", COLOR="YELLOW", BGCOLOR="BLACK", INCDEC=True)
        else:
            return False

    def sql_table_create(self, table_name, **kwargs):
        '''
            Generates the sql used to create the table provided.

            ----------

            Arguments
            -------------------------
            `table_name` {string}
                The name of the table to generate the sql for.

            Keyword Arguments
            -------------------------
            [`file_path`] {string}
                if provided, the sql is saved to this file.
            [`compress`] {bool}
                If True, the sql is generated to be as small as possible (without literal compression)

            Return {string|bool}
            ----------------------
            if successful, the sql is returned otherwise False;

            Meta
            ----------
            `author`: Colemen Atwood
            `created`: 12-08-2021 13:03:52
            `memberOf`: generation
            `version`: 1.0
            `method_name`: sql_table_create
        '''
        file_path = obj.get_kwarg(["file path", "path"], False, (str), **kwargs)
        compress = obj.get_kwarg(["compress"], False, (bool), **kwargs)
        sql = False
        if self._db.data['db_type'] == "SQLITE":
            sql = self.__sqlite_table_create(table_name, compress)

        if sql is not False:
            if file_path is not False:
                fileUtils.file.write.write(file_path, sql)
        return sql
        #     self._db.run("SHOW CREATE TABLE `" + str(table_name) + "`;")
        #     result = self._db.cur.fetchone()
        #     data += str(result['Create Table'])
        #     data += ";"
        #     # data = data.replace(f"CREATE TABLE `{table_name}` (", f"CREATE TABLE IF NOT EXISTS `{table_name}`\n(")
        #     # data = re.sub(r'\)\sENGINE=[^;]*;', ');', data)
        #     # data = sqlTableCreateFormat(data)
        #     return data
        #     # print(f"{data}", COLOR="YELLOW", BGCOLOR="BLACK", INCDEC=True)
        # else:
        #     return False

    def __sqlite_table_create(self, table_name, compress=False):
        data = False
        if self._db.table.exists(table_name) is True:
            indent = "    "
            newline = "\n"
            if compress is True:
                newline = ""
                indent = ""
            data = ""
            data += "DROP TABLE IF EXISTS `" + str(table_name) + f"`;{newline}"
            data += "CREATE TABLE IF NOT EXISTS `" + str(table_name) + f"`{newline}"
            col_data = self._db.table.get_column_data_array(table_name)
            longest = self._db.table.get_longest_column_name("assets")
            padding = longest[1] + 2
            # print(col_data)
            col_strings = []
            primary_key = False
            for col in col_data:
                total_padding = " " * (padding - len(col['name']))
                if compress is True:
                    total_padding = " "
                default_value = ""
                null_value = "NOT NULL"
                if col['pk'] == 1:
                    primary_key = col['name']
                if col['notnull'] == 0:
                    null_value = "NULL"
                if col['dflt_value'] is not None:
                    default_value = f"DEFAULT {col['dflt_value']}"
                line = f"{indent}`{col['name']}`{total_padding}{col['type']} {null_value} {default_value}"
                col_strings.append(line)

            cols = f",{newline}".join(col_strings)
            data += f"({newline}{cols},{newline}"
            if primary_key is not False:
                data += f"{indent}PRIMARY KEY (`{primary_key}`){newline}"
            data += ");"
            data = data.replace(" ,", ",")
        return data

    def sql_data_insert(self, table_name):
        """
        Generates the SQL insert statement for all of the data in the table.

        @name generateSQLInsertFromTable
        @author Colemen Atwood
        @created 04/18/2021 08:53:14
        @version 1.0
        @param string table_name The name of the table to analyze
        @return string The SQL insert statement for data in the table, False otherwise.
        """
        if self._db.table.exists(table_name) is True:
            data = ""
            column_list = self.array_to_list_string(self._db.table.get_column_array(table_name), ITEM_WRAP="`", LIST_WRAP="(")
            data += f"INSERT INTO `{table_name}` \n{column_list} VALUES \n"

            self._db.run("SELECT * FROM `" + str(table_name) + "`;")
            rows = self._db.fetchall()
            if len(rows) == 0:
                return False
            row_len = len(rows) - 1
            row_count = 0
            for row in rows:
                list_suffix = "),\n"
                if row_count == row_len:
                    list_suffix = ");\n"
                # print(f"{row}", COLOR="GREEN", BGCOLOR="BLACK", INCDEC=True)
                data += self.array_to_list_string(list(row.values()), ITEM_WRAP="AUTO", LIST_PREFIX="(", LIST_SUFFIX=list_suffix)
                row_count += 1
            return data
        else:
            return False

    def sql_database_backup(self, **kwargs):
        compress = obj.get_kwarg(["compress"], False, (bool), **kwargs)
        file_path = obj.get_kwarg(["file path", "path"], False, (str), **kwargs)
        back_up_structure = obj.get_kwarg(["structure"], True, (str), **kwargs)
        back_up_data = obj.get_kwarg(["data"], True, (str), **kwargs)
        timestamp = datetime.datetime.now().strftime("%m-%d-%Y %H:%M:%S")
        tables = self._db.table.get_table_names()
        data = f"-- ******************   DATABASE BACKUP   ******************;\n-- ****************** {timestamp} ******************;\n\n"

        for table in tables:
            if back_up_structure is True:
                table_create = self.sql_table_create(table, compress=compress)
                if table_create is not False:
                    data += f"\n\n-- ************************************** `{table}` - {timestamp} - CREATE START\n\n"
                    data += table_create
                    data += f"\n\n-- ************************************** `{table}` - {timestamp} - CREATE END\n\n"
            if back_up_data is True:
                table_insert = self.sql_data_insert(table)
                if table_insert is not False:
                    data = f"\n\n-- ************************************** `{table}` - {timestamp} - INSERT START\n\n"
                    data += table_insert
                    data = f"\n\n-- ************************************** `{table}` - {timestamp} - INSERT END\n\n"

        # filename = r"testBackUp.sql"
        if file_path is not False:
            fileUtils.file.write.write(file_path, data)

        return data

    def array_to_list_string(self, array, **kwargs):
        list_prefix = ""
        list_suffix = ""
        item_prefix = ""
        item_suffix = ""
        item_sep = ", "
        item_wrap = obj.get_kwarg(["item wrap"], "", (str), **kwargs)

        if 'ITEM_SEP' in kwargs:
            item_sep = kwargs['ITEM_SEP']
        if 'ITEM_WRAP' in kwargs:
            dif_wrap = False
            if item_wrap == "(" or item_wrap == ")":
                item_prefix = "("
                item_suffix = ")"
                dif_wrap = True
            if item_wrap == "{" or item_wrap == "}":
                item_prefix = "{"
                item_suffix = "}"
                dif_wrap = True

            if dif_wrap is False:
                item_prefix = item_wrap
                item_suffix = item_wrap

        if 'ITEM_PREFIX' in kwargs:
            item_prefix = kwargs['ITEM_PREFIX']
        if 'ITEM_SUFFIX' in kwargs:
            item_suffix = kwargs['ITEM_SUFFIX']

        if 'LIST_WRAP' in kwargs:
            list_wrap = kwargs['LIST_WRAP']
            dif_wrap = False
            if list_wrap == "(" or list_wrap == ")":
                list_prefix = "("
                list_suffix = ")"
                dif_wrap = True
            if list_wrap == "{" or list_wrap == "}":
                list_prefix = "{"
                list_suffix = "}"
                dif_wrap = True
            if dif_wrap is False:
                list_prefix = list_wrap
                list_suffix = list_wrap

        if 'LIST_PREFIX' in kwargs:
            list_prefix = kwargs['LIST_PREFIX']
        if 'LIST_SUFFIX' in kwargs:
            list_suffix = kwargs['LIST_SUFFIX']

        ilen = len(array) - 1
        cur_idx = 0
        list_string = ""
        for list_value in array:
            if item_wrap == "AUTO":
                if isinstance(list_value, int):
                    item_prefix = ""
                    item_suffix = ""
                if isinstance(list_value, str):
                    item_prefix = "'"
                    item_suffix = "'"
                    if "'" in list_value:
                        list_value = sanitize_quotes(list_value)
                if list_value == "None" or list_value is None:
                    list_value = "NULL"
                    item_prefix = ""
                    item_suffix = ""

            list_string += f"{item_prefix}{list_value}{item_suffix}"
            if cur_idx != ilen:
                list_string += item_sep
            cur_idx += 1
        return f"{list_prefix}{list_string}{list_suffix}"

    def generate_update_string(self, data):
        # print("---generate_update_string---")
        return_string = ""
        total_column_count = 0
        total_value_count = 0

        for x, y in data.items():
            # print(f"------{x} - {y} - {type(y)}")
            if isinstance(x, str):
                total_column_count += 1
                # returnObj['columnString'] += f"{x},"
                if isinstance(y, str):
                    if is_boolean_string(y) is True:
                        total_value_count += 1
                        return_string += f"{x} = {determine_boolean_from_string(y)},"
                        # returnObj['valueString'] += f"{determine_boolean_from_string(y)},"
                        continue
                    if y == "NULL":
                        total_value_count += 1
                        return_string += f"{x} = NULL,"
                        # returnObj['valueString'] += "NULL,"
                        continue

                    y = sanitize_quotes(y)
                    # returnObj['valueString'] += f"'{y}',"
                    return_string += f"{x} = '{y}',"
                    total_value_count += 1
                    continue

                if isinstance(y, int):
                    total_value_count += 1
                    return_string += f"{x} = {y},"
                    # returnObj['valueString'] += f"{y},"
                    continue

                if isinstance(y, bool):
                    total_value_count += 1
                    return_string += f"{x} = {y},"
                    # returnObj['valueString'] += f"{y},"
                    continue

                if y is None:
                    total_value_count += 1
                    return_string += f"{x} = NULL,"
                    # returnObj['valueString'] += "NULL,"
                    continue

                # returnObj['valueString'] += f"{y},"

        return_string = strip_trailing_comma(return_string)

        # print(f"---total_column_count: {total_column_count}")
        # print(f"---total_value_count: {total_value_count}")
        # print("---generate_update_string---")
        return return_string

    def reverse_sanitize_quotes(self, string):
        return reverse_sanitize_quotes(string)

    def sanitize_quotes(self, string):
        return sanitize_quotes(string)


def determine_boolean_from_string(string):
    if string in ["TRUE", "true", "True", "yes", "y", "1"]:
        return True
    if string in ["FALSE", "false", "False", "no", "n", "0"]:
        return False


def is_boolean_string(string):
    if string in ["TRUE", "true", "True", "yes", "y", "1"]:
        return True
    if string in ["FALSE", "false", "False", "no", "n", "0"]:
        return True
    return False


def boolToString(string):
    if string in ["TRUE", "true", "True", "yes", "y", "1"]:
        return "111111111"
    if string in ["FALSE", "false", "False", "no", "n", "0"]:
        return "000000000"
    return string


def strip_trailing_comma(string):
    return re.sub(",$", "", string)


def stripQuotes(string):
    string = string.replace("'", "")
    string = string.replace('"', "")
    string = string.replace('&apos_', "")
    string = string.replace('&quot_', "")
    return string


def reverse_sanitize_quotes(string):
    orig_list = False
    if isinstance(string, (list)):
        orig_list = True
    if isinstance(string, (str)):
        string = [string]

    new_list = []
    for item in string:
        item = item.replace("&apos_", "'")
        item = item.replace("&quot_", '"')
        new_list.append(item)

    if len(new_list) == 1 and orig_list is False:
        return new_list[0]

    return new_list


def sanitize_quotes(string):
    orig_list = False
    if isinstance(string, (list)):
        orig_list = True
    if isinstance(string, (str)):
        string = [string]

    new_list = []
    for item in string:
        if isinstance(item, (str)):
            item = item.replace("'", "&apos_")
            item = item.replace('"', "&quot_")
        new_list.append(item)

    if len(new_list) == 1 and orig_list is False:
        return new_list[0]

    return new_list
