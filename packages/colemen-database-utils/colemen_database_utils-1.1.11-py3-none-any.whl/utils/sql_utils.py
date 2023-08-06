# pylint: disable=missing-function-docstring
# pylint: disable=missing-class-docstring


def count_statements(sql):
    return len(to_statement_list(sql))


def to_statement_list(sql):
    sql = sql.replace(";", ";STATEMENT_END")
    statements = sql.split('STATEMENT_END')
    output = [x.strip() for x in statements if len(x.strip()) > 0]
    return output
