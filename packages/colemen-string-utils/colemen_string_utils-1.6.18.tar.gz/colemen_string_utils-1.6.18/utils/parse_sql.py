

import re
import shlex
import sqlparse
import colemen_file_utils as cfu
# # from sqlparse import sql
import utils.string_format as format

import utils.objectUtils as obj
from pyparsing import And, Suppress,Dict, Word, Literal, Group, Optional, ZeroOrMore, OneOrMore, Regex, restOfLine, alphanums,nums, printables, string, CaselessKeyword,nestedExpr,ParseException,quotedString,removeQuotes,originalTextFor,delimitedList,QuotedString






def strip_comments(value):
    '''
        Strips single line SQL comments from a string

        ----------

        Arguments
        -------------------------
        `value` {string}
            The string to parse

        Return {string}
        ----------------------
        The formatted string

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 03-21-2022 12:28:55
        `memberOf`: parse_sql
        `version`: 1.0
        `method_name`: strip_comments
        @xxx [03-21-2022 12:29:07]: documentation for strip_comments
    '''

    value = re.sub(r'--[^\n]*\n','',value)
    return value

def parse_list(value):
    value = value.asList()
    # print(type(value))
    # print(f"value: {value}")
    value = strip_sql_quotes(value[0])
    vals = value.split(",")
    vals = [format.strip_any(x,[" "]) for x in vals]
    return ','.join(vals)

def parse_key(value=None):
    if 'key' not in value.lower():
        return None
    value ="KEY `FK_ActivityLogs_ActivityTypeID` (`activity_type_id`, `activity_type_hash_id`),"
    _tick,_double_quote,_single_quote,_comma = [Suppress(x) for x in list('`"\',')]
    _quote = (_tick|_double_quote|_single_quote)
    _open_paren,_close_paren = [Suppress(x) for x in list('()')]
    # paren_word = _open_paren + Optional(_quote) + Word(alphanums + "_") + Optional(_quote) + _close_paren
    quoted_word = _quote + Word(alphanums + "_") + _quote    

    paren_word_list = _open_paren + Word(alphanums + "_,'\"` ") + _close_paren

    # KEY `FK_ActivityLogs_RequestLogID`
    key_name = Suppress(CaselessKeyword('KEY')) + quoted_word.setResultsName('key_name')

    foreign_col_name = paren_word_list.setResultsName('foreign_col_name').setParseAction(parse_list)

    grammar = key_name + foreign_col_name
    res = ZeroOrMore(Group(grammar).setResultsName('data')).parseString(value)

    output = None

    if len(res) > 0:
        data = res.as_dict()['data']
        new_data = {}
        for k,v in data.items():
            if k == "foreign_col_name":
                new_data[k] = v.split(",")
                continue
            if isinstance(v,(list)):
                new_data[k] = v[0]
                continue
            new_data[k] = v

        # print(new_data)
        output = new_data
    return output    

def parse_primary_key(value=None):
    if 'primary key' not in value.lower():
        return None
    # value = "PRIMARY KEY (`activity_log_id`)"
    value = "PRIMARY KEY (`activity_type_id`, `activity_type_hash_id`),"
    _tick,_double_quote,_single_quote,_period = [Suppress(x) for x in list('`"\'.')]
    _quote = (_tick|_double_quote|_single_quote)
    _open_paren,_close_paren = [Suppress(x) for x in list('()')]
    paren_word = _open_paren + Optional(_quote) + Word(alphanums + "_") + Optional(_quote) + _close_paren
    quoted_word = _quote + Word(alphanums + "_") + _quote
    paren_word_list = _open_paren + Word(alphanums + "_,'\"` ") + _close_paren
    primary_key = paren_word_list.setResultsName('primary_key').setParseAction(parse_list)
    grammar = Suppress(CaselessKeyword('primary key')) + primary_key
    res = ZeroOrMore(Group(grammar).setResultsName('data')).parseString(value)

    output = None

    if len(res) > 0:
        data = res.as_dict()['data']
        new_data = {}
        for k,v in data.items():
            if k == "primary_key":
                new_data[k] = v.split(",")
                continue
            if isinstance(v,(list)):
                new_data[k] = v[0]
                continue
            new_data[k] = v

        # print(new_data)
        output = new_data
    return output

def parse_constraint(value):
    # value = "CONSTRAINT `FK_User_ProfileImageID_File` FOREIGN KEY `fkIdx_910` (`profile_image_id`) REFERENCES `idealech_Equari_Content_Database`.`files` (`file_id`) ON UPDATE NO ACTION ON DELETE CASCADE"
    # _quote = ('`'|'"'|"'")
    _tick,_double_quote,_single_quote,_period = [Suppress(x) for x in list('`"\'.')]
    _quote = (_tick|_double_quote|_single_quote)
    _open_paren,_close_paren = [Suppress(x) for x in list('()')]
    paren_word = _open_paren + Optional(_quote) + Word(alphanums + "_") + Optional(_quote) + _close_paren
    quoted_word = _quote + Word(alphanums + "_") + _quote
    # constraints = ["ON UPDATE","ON DELETE"]
    # constraint_conds = ["RESTRICT","CASCADE","SET NULL","NO ACTION","SET DEFAULT"]

    
    constraint_conditions = (CaselessKeyword('RESTRICT') | CaselessKeyword('CASCADE') | CaselessKeyword('SET NULL') | CaselessKeyword('NO ACTION') | CaselessKeyword('SET DEFAULT'))

    # quoted_paren_word = _quote + Word(alphanums + "_") + _quote
    constraint_name = Suppress(CaselessKeyword('CONSTRAINT')) + quoted_word.setResultsName('constraint_name')
    # constraint_name = Suppress(CaselessKeyword('CONSTRAINT')) + _quote + Word(alphanums + "_").setResultsName('constraint_name') + _quote

    foreign_key_name = Suppress(CaselessKeyword('FOREIGN KEY')) + quoted_word.setResultsName('foreign_key')
    local_col_name = paren_word.setResultsName('local_col_name') 
    foreign_table = Suppress(CaselessKeyword('REFERENCES')) + Optional(quoted_word.setResultsName('schema_name') + _period) + quoted_word.setResultsName('table_name')
    foreign_col_name = paren_word.setResultsName('foreign_col_name')

    on_delete = Suppress(CaselessKeyword('ON DELETE')) + constraint_conditions.setResultsName('on_delete')
    on_update = Suppress(CaselessKeyword('ON UPDATE')) + constraint_conditions.setResultsName('on_update')
    constraints = ZeroOrMore(on_delete | on_update)

    grammar = constraint_name + foreign_key_name + local_col_name + foreign_table + foreign_col_name + constraints
    res = ZeroOrMore(Group(grammar).setResultsName('data')).parseString(value)

    output = None

    if len(res) > 0:
        data = res.as_dict()['data']
        new_data = {}
        for k,v in data.items():
            if isinstance(v,(list)):
                new_data[k] = v[0]
                continue
            new_data[k] = v

        # print(new_data)
        output = new_data
    return output




def parse_table_columns(sql):
    '''
        Parses an SQL create file into a list of column dictionaries.

        ----------

        Arguments
        -------------------------
        `sql` {str}
            The sql to parse or a file path to parse.

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
        `created`: 05-31-2022 07:59:37
        `memberOf`: TableManager
        `version`: 1.0
        `method_name`: parse_table_columns
        # @TODO []: documentation for parse_table_columns
    '''

    if cfu.file.exists(sql):
        sql = cfu.file.read.read(sql)
    # orig_sql = sql
    file_data = strip_keys_constraints(sql)
    file_data['columns'] = {}

    # sql = parse_primary_keys(sql)

    cols = {}
    parse = sqlparse.parse(file_data['sql'])
    for stmt in parse:
        # Get all the tokens except whitespaces
        tokens = [t for t in sqlparse.sql.TokenList(stmt.tokens) if t.ttype != sqlparse.tokens.Whitespace]
        is_create_stmt = False
        for i, token in enumerate(tokens):
            # Is it a create statements ?
            if token.match(sqlparse.tokens.DDL, 'CREATE'):
                is_create_stmt = True
                continue

            # If it was a create statement and the current token starts with "("
            if is_create_stmt and token.value.startswith("("):
                # Get the table name by looking at the tokens in reverse order till you find
                # a token with None type
                # print (f"table: {get_table_name(tokens[:i])}")

                # Now parse the columns
                txt = token.value
                # strip_indices(txt)
                # print("\n\n")
                columns = txt[1:txt.rfind(")")].replace("\n","").split(",")
                # print(columns)
                # print("\n\n")
                for column in columns:
                    c = ' '.join(column.split()).split()
                    # print(c)
                    if len(c) == 0:
                        continue
                    c_name = c[0].replace('\"',"")
                    c_name = c_name.replace('`','')
                    # c_type = c[1]  # For condensed type information
                    # OR
                    c_type = " ".join(c[1:]) # For detailed type informatio
                    data = {
                        "name":c_name,
                        "raw_type":c_type,
                        "default":None,
                        "size":None,
                        "allow_nulls":False,
                        "data_type":None,
                        "comment":None,
                        "shlexed":None,
                        "is_primary_key":False,
                    }
                    data['shlexed'] = shlex.split(data['raw_type'])
                    data = prep_shlexed(data)
                    # print (f"column: {c_name}")
                    # print (f"type: {c_type}")
                    if data['name'] in file_data['primary_keys']:
                        data['is_primary_key'] = True
                    data = parse_col_type(data)
                    data = parse_allow_null(data)
                    data = parse_col_comment(data)
                    
                    
                    del data['shlexed']
                    cols[c_name] = data
                # print ("---"*20)
                break
    # cols = determine_primary_column(cols)
    file_data['columns'] = cols
    # cfu.file.write.to_json("tmp.sql.delete.json",file_data)
    return file_data


def prep_shlexed(col_data):
    '''
        Prepares the shlexed property for parsing by combining indices as necessary.

        ----------

        Arguments
        -------------------------
        `col_data` {dict}
            The column_data dictionary produced by parse_table_columns
            Must include the shlexed property.

        Return {dict}
        ----------------------
        The col_data dictionary with an updated shlexed property.


        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 05-31-2022 07:55:19
        `memberOf`: TableManager
        `version`: 1.0
        `method_name`: prep_shlexed
        @xxx [05-31-2022 07:56:12]: documentation for prep_shlexed
    '''

    
    output = []
    previous_val = None
    for i,d in enumerate(col_data['shlexed']):
        dl = d.lower()
        if previous_val == "not" and dl == "null":
            output[-1] = "not null"
            continue
        if previous_val == "default":
            output[-1] = f"default {d}"
            continue
        if previous_val == "comment":
            output[-1] = f"comment {d}"
            continue
        if col_data['name'] == 'PRIMARY':
            if previous_val == "key":
                output[-1] = f"key {d}"
                continue

        #     if col_data['schlexed']
        output.append(d)
        previous_val = dl
    col_data['shlexed'] = output
    return col_data

def parse_allow_null(col_data):
    '''
        Determines if the column is allowed to be null.

        ----------

        Arguments
        -------------------------
        `col_data` {dict}
            The column_data dictionary produced by parse_table_columns
            Must include the shlexed property.

        Return {dict}
        ----------------------
        The col_data dictionary with an updated allow_nulls property.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 05-31-2022 07:29:36
        `memberOf`: TableManager
        `version`: 1.0
        `method_name`: parse_allow_null
        @xxx [05-31-2022 07:31:12]: documentation for parse_allow_null
    '''
    from utils.parse_utils import array_in_string
    nn_found = False
    for s in col_data['shlexed']:
        if array_in_string(["not null","NOT NULL"],s,False):
            nn_found = True
    if nn_found is False:
        col_data['allow_nulls'] = True
    return col_data

def parse_col_comment(col_data):
    '''
        Captures a comment related to the column.

        ----------

        Arguments
        -------------------------
        `col_data` {dict}
            The column_data dictionary produced by parse_table_columns
            Must include the shlexed property.


        Return {dict}
        ----------------------
        The col_data dictionary with an updated comment property.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 05-31-2022 07:52:33
        `memberOf`: TableManager
        `version`: 1.0
        `method_name`: parse_col_comment
        @xxx [05-31-2022 07:53:42]: documentation for parse_col_comment
    '''


    for s in col_data['shlexed']:
        if s.startswith('comment'):
            # re.replace(r'^comment\s*')
            cmt = s.replace('comment','')
            col_data['comment'] = format.strip_any(cmt,[" "])
            break

    return col_data

def parse_col_type(col_data):
    '''
        Parses the SQL column type from the column data.

        ----------

        Arguments
        -------------------------
        `col_data` {dict}
            The column_data dictionary produced by parse_table_columns
            Must include the shlexed property.

        Return {dict}
        ----------------------
        The col_data dictionary with an updated data_type property.


        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 05-31-2022 07:54:14
        `memberOf`: TableManager
        `version`: 1.0
        `method_name`: parse_col_type
        @xxx [05-31-2022 07:54:59]: documentation for parse_col_type
    '''


    sql_data_types = [
        "mediumtext",
        "mediumblob",
        "varbinary",
        "timestamp",
        "mediumint",
        "tinytext",
        "tinyblob",
        "smallint",
        "longtext",
        "longblob",
        "datetime",
        "varchar",
        "tinyint",
        "integer",
        "decimal",
        "boolean",
        "double",
        "double",
        "binary",
        "bigint",
        "float",
        "float",
        "year",
        "time",
        "text",
        "enum",
        "date",
        "char",
        "bool",
        "blob",
        "set",
        "int",
        "dec",
        "bit",
    ]

    for t in col_data['shlexed']:
        for sql_type in sql_data_types:
            if sql_type in t.lower():
                col_data['data_type'] = sql_type
                break

        col_data['size'] = parse_column_size(t)
        break
    # lower_raw = col_data['raw_type'].lower()
    # for t in sql_data_types:
    #     if lower_raw.startswith(t):
    #         # print(f"data type: {t}")
    #         col_data['data_type'] = t
    #         break
    return col_data

def parse_column_size(type_string):
    '''
        Called by parse_col_type
        This will capture the column size if the type supports it.

        ----------

        Arguments
        -------------------------
        `type_string` {str}
            The type of the column, example: "varchar(500)"

        Return {int|None}
        ----------------------
        The integer size of the column upon success, None otherwise.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 05-31-2022 07:26:51
        `memberOf`: TableManager
        `version`: 1.0
        `method_name`: parse_column_size
        @xxx [05-31-2022 07:28:25]: documentation for parse_column_size
    '''


    sized_cols = [
        "varbinary",
        "mediumint",
        "timestamp",
        "smallint",
        "datetime",
        "varchar",
        "decimal",
        "integer",
        "tinyint",
        "binary",
        "double",
        "double",
        "bigint",
        "float",
        "float",
        "text",
        "char",
        "time",
        "blob"
        "dec",
        "int",
        "bit",
    ]

    lower_raw = type_string.lower()
    for sc in sized_cols:
        if sc in lower_raw:
            pat = re.compile(sc+r"\(([0-9]*)\)")
            match = re.findall(pat,lower_raw)
            if match is not None:
                if len(match) > 0:
                    return int(match[0])
    return None



def strip_keys_constraints(sql):
    output = {
        "sql":[],
        "keys":[],
        "constraints":[],
    }
    lines = sql.split("\n")
    for line in lines:
        if len(line) == 0 or is_line_comment(line):
            continue
        # print(f"line: {line}")
        if is_line_key(line):
            output['keys'].append(line)
            continue
        if is_line_constraint(line):
            output['constraints'].append(line)
            continue
        # match = re.findall(r'^(\w+\s*)?key',line,re.IGNORECASE)
        # match = re.findall(r'^((\w+\s*)?key|constraint)',line,re.IGNORECASE)
        output['sql'].append(line)
    output['sql'] = '\n'.join(output['sql'])

    if len(output['keys']) > 0:
        primary_keys = []
        for k in output['keys']:
            data = parse_primary_keys(k)
            if len(data) > 0:
                primary_keys = data
        output['primary_keys'] = primary_keys

    if len(output['constraints']) > 0:
        foreign_keys = []
        for k in output['constraints']:
            data = parse_constraint(k)
            if data is not None:
                foreign_keys.append(data)
                continue
            data = parse_key(k)
            if data is not None:
                foreign_keys.append(data)
                continue
        output['foreign_keys'] = foreign_keys

    return output

def is_line_key(line):
    match = re.match(r'^(\w+\s*)?key',line,re.IGNORECASE)
    if match is not None:
        return True
    return False

def is_line_comment(line):
    match = re.match(r'^--',line,re.IGNORECASE)
    if match is not None:
        return True
    return False


def is_line_constraint(line):
    match = re.match(r'^constraint',line,re.IGNORECASE)
    if match is not None:
        return True
    return False

def parse_primary_keys(sql):
    primary_keys = []
    match = re.findall(r'primary\s*key\s*\(([a-zA-Z0-9_,\`\'\"\s]*)\)',sql,re.IGNORECASE)
    if match is not None:
        if len(match) > 0:
            keys = strip_sql_quotes(match[0])
            keys = keys.split(",")
            keys = [format.strip_any(x,[" "]) for x in keys]
            primary_keys = keys
        # print(match)
    return primary_keys

def strip_sql_quotes(sql):
    '''
        Remove all quotes from an sql string.
        This includes these characters:
        - Double Quote - "
        - Single Quote - '
        - Accent/Tick  - `

        ----------

        Arguments
        -------------------------
        `value` {str}
            The string to strip of quotes.

        Return {str}
        ----------------------
        The string without quotations.

        Meta
        ----------
        `author`: Colemen Atwood
        `created`: 05-31-2022 11:56:37
        `memberOf`: parse_sql
        `version`: 1.0
        `method_name`: strip_sql_quotes
        @xxx [05-31-2022 11:58:02]: documentation for strip_sql_quotes
    '''


    sql = sql.replace("'",'')
    sql = sql.replace('"','')
    sql = sql.replace('`','')
    return sql


# def format_sql_string(sql):
#     '''
#         Format an SQL string to a consistent indentation.

#         ----------

#         Arguments
#         -------------------------
#         `sql` {string}
#             The sql string to format.

#         Return {string}
#         ----------------------
#         The formatted SQL

#         Meta
#         ----------
#         `author`: Colemen Atwood
#         `created`: 03-21-2022 12:38:32
#         `version`: 1.0
#         `method_name`: format_sql_string
#         @xxx [03-21-2022 12:38:41]: documentation for format_sql_string
#     '''


#     raw = sql
#     statements = sqlparse.split(raw)
#     new_contents = []
#     for state in statements:
#         new_state = sqlparse.format(state, reindent=True, keyword_case='upper')
#         new_contents.append(new_state)
#     if len(new_contents) > 0:
#         return "\n".join(new_contents)
#     return False

# def get_statements(sql):
#     '''
#         Parses the SQL statements from the string.

#         ----------

#         Arguments
#         -------------------------
#         `sql` {string}
#             The sql string to parse.

#         Return {list}
#         ----------------------
#         A list of SQL statements.

#         Meta
#         ----------
#         `author`: Colemen Atwood
#         `created`: 03-21-2022 12:40:52
#         `version`: 1.0
#         `method_name`: get_statements
#         @xxx [03-21-2022 12:40:58]: documentation for get_statements
#     '''


#     raw = sql
#     if cfu.file.exists(sql):
#         raw = cfu.file.read.read(sql)
#     raw = strip_comments(raw)
#     raw = format_sql_string(raw)
#     return sqlparse.parse(raw)

# def parse(sql):
    


# class Parse:
#     def __init__(self,**kwargs):
#         self.settings = {}
#         self.data = {
#             "raw_sql":"",
#             "file_path":ou.get_kwarg(['file path'],None,(str),**kwargs),
#         }
        
    
#     def read(self):
#         if self.data['file_path'] is not None:
#             if cfu.file.exists(self.data['file_path']):
#                 self.data['raw_sql'] = cfu.file

# # statements = get_statements("_sql_parse_test.sql")
# # for x in statements:
# #     print(f"========================")
# #     print(str(x))
# # print(statements)


# path = "Z:\\Structure\\Ra9\\2022\\22-0018 - equari_server\\database\\idealech_Equari_Management_Database\\activity_logs\\activity_logs.sql"
# cols = parse_table_columns(path)
# cfu.file.write.to_json("colums.delete.json",cols)

# parse_constraint()
# parse_primary_key()
# parse_key()