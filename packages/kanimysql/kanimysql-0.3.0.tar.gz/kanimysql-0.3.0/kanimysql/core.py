#!/usr/bin/python
# -*-coding: utf-8 -*-

from __future__ import print_function
import pymysql
import re
import itertools
import string_utils
import six
from pymysql.constants import FIELD_TYPE
from builtins import str
try:
    import numpy as np
    NUMPY_SUPPORT = True
except:
    NUMPY_SUPPORT = False
try:
    import pandas as pd
    PANDAS_SUPPORT = True
except:
    PANDAS_SUPPORT = False
try:
    import freezegun
    FREEZEGUN_SUPPORT = True
except:
    FREEZEGUN_SUPPORT = False
from itertools import chain
from kaniattrdict import AttrDict
from funcy import project


def __repr__(self,):
    return '<class \'%s\'> %s' % (self.__class__.__name__, self.items())


def __custom_getattr__(self, key):
    if key not in self:
        return None
    return super(AttrDict, self).__getattr__(key)


def __setattr__(self, key, value):
    if key != 'id':
        if key not in self:
            raise KeyError("{} is not a legal colum name of this class:'{}'".format(repr(key), self.__class__.__name__))
    self._setattr('_is_modified', True)
    return super(AttrDict, self).__setitem__(key, value)


def __init__(self, *args, **kwargs):
    for key in self.columns:
        if key != 'id':
            super(AttrDict, self).__setitem__(key, None)
    AttrDict.__init__(self, *args, **kwargs)


def TableDict(table_name, conn=None):
    replace_dict = {'_table_name': table_name, '__repr__': __repr__, '__getattr__': __custom_getattr__}
    if conn:
        columns = [list(column_name.values())[0] for column_name in conn.column_name(table_name)]
        replace_dict['__init__'] = __init__
        replace_dict['__setattr__'] = __setattr__
        replace_dict['columns'] = columns
        replace_dict['_is_modified'] = False
    if isinstance(table_name, six.string_types):
        table_class_name = string_utils.snake_case_to_camel(table_name)
    else:
        table_class_name = 'TableDict'
    if six.PY2:
        table_class_name = bytes(table_name)
    return type(table_class_name, (AttrDict,), replace_dict)


def to_dict(instances):
    pickled = []
    for instance in instances:
        data = dict(instance)
        data['table_name'] = instance._table_name
        pickled.append(data)
    return pickled


def from_dict(dict_array, conn=None):
    instances = []
    for data in dict_array:
        if conn is None:
            instance = TableDict(data['table_name'])()
        else:
            instance = conn.get_table_class(data['table_name'])()
        del data['table_name']
        for key, value in data.items():
            instance[key] = value
        instances.append(instance)
    return instances


from .cursor import KaniCursor

err = pymysql.err
cursors = pymysql.cursors


class KaniMySQL:
    def __init__(self, host, user, passwd, db=None, port=3306, charset='utf8', init_command='SET NAMES UTF8',
                 cursorclass=KaniCursor, use_unicode=True, autocommit=False, table_initialize=False, table_classes=None):
        self.host = host
        self.port = int(port)
        self.user = user
        self.passwd = passwd
        self.db = db
        self.cursorclass = cursorclass
        self.charset = charset
        self.init_command = init_command
        self.use_unicode = use_unicode
        self.autocommit_mode = bool(autocommit)
        self.connection = self.conn = pymysql.connect(host=self.host, port=self.port, user=self.user,
                                                      passwd=self.passwd, db=self.db, charset=charset,
                                                      init_command=init_command, cursorclass=self.cursorclass,
                                                      use_unicode=self.use_unicode, autocommit=self.autocommit_mode)
        self.connection.decoders[FIELD_TYPE.DECIMAL] = int
        self.connection.decoders[FIELD_TYPE.NEWDECIMAL] = int
        if NUMPY_SUPPORT:
            self.connection.encoders[np.float64] = pymysql.converters.escape_float
            self.connection.encoders[np.int64] = pymysql.converters.escape_int
        if PANDAS_SUPPORT:
            self.connection.encoders[pd.Timestamp] = pymysql.converters.escape_datetime
        if FREEZEGUN_SUPPORT:
            self.connection.encoders[freezegun.api.FakeDatetime] = pymysql.converters.escape_datetime

        self.cursor = self.cur = self.conn.cursor()
        self.debug = False

        if table_classes is None:
            self.table_classes = {}
            if table_initialize:
                table_names = [table['table_name'] for table in self.table_name()]
                for table_name in table_names:
                    self.table_classes[table_name] = TableDict(table_name, self)
                self.cursor.setup_table_dict_list(self.table_classes)
        else:
            self.table_classes = table_classes
            self.cursor.setup_table_dict_list(self.table_classes)

    def reconnect(self):
        self.connection = self.conn = pymysql.connect(host=self.host, port=self.port, user=self.user,
                                                      passwd=self.passwd, db=self.db, cursorclass=self.cursorclass,
                                                      charset=self.charset, init_command=self.init_command,
                                                      use_unicode=self.use_unicode, autocommit=self.autocommit_mode)
        self.cursor = self.cur = self.conn.cursor()
        return True

    def query(self, sql, args=None):
        """
        :param sql: string. SQL query.
        :param args: tuple. Arguments of this query.
        """
        return self.cur.execute(sql, args)

    @staticmethod
    def _backtick_columns(cols):
        """
        Quote the column names
        """
        def bt(s):
            b = '' if s == '*' or not s else '`'
            return [_ for _ in [b + (s or '') + b] if _]

        formatted = []
        for c in cols:
            if c[0] == '#':
                formatted.append(c[1:])
            elif c.startswith('(') and c.endswith(')'):
                # WHERE (column_a, column_b) IN ((1,10), (1,20))
                formatted.append(c)
            else:
                # backtick the former part when it meets the first dot, and then all the rest
                formatted.append('.'.join(bt(c.split('.')[0]) + bt('.'.join(c.split('.')[1:]))))

        return ', '.join(formatted)

    def _backtick(self, value):
        return self._backtick_columns((value,))

    @staticmethod
    def _whitespace_decorator(s, p=True, n=False):
        return ''.join((' ' if p else '', s, ' ' if n else ''))

    def _tablename_parser(self, table):
        result = re.match(r'^(\[(|>|<|<>|><)\])??(\w+)(\((|\w+)\))??$', table.replace(' ', ''))
        join_type = ''
        alias = ''
        formatted_tablename = self._backtick(table)
        if result:
            alias = result.group(5) if result.group(5) else ''

            tablename = result.group(3)

            formatted_tablename = ' '.join([self._backtick(tablename),
                                            'AS', self._backtick(alias)]) if alias else self._backtick(tablename)

            join_type = {'>': 'LEFT', '<': 'RIGHT', '<>': 'FULL', '><': 'INNER'}.get(result.group(2), '')
        else:
            tablename = table

        return {'join_type': join_type,
                'tablename': tablename,
                'alias': alias,
                'formatted_tablename': formatted_tablename}

    def _value_parser(self, value, columnname=False, placeholder='%s'):
        """
        Input: {'c1': 'v', 'c2': None, '#c3': 'uuid()'}
        Output:
        ('%s, %s, uuid()', [None, 'v'])                             # insert; columnname=False
        ('`c2` = %s, `c1` = %s, `c3` = uuid()', [None, 'v'])        # update; columnname=True
        No need to transform NULL value since it's supported in execute()
        """
        if not isinstance(value, dict):
            raise TypeError('Input value should be a dictionary')
        q = []
        a = []
        for k, v in value.items():
            if k[0] == '#':  # if is sql function
                q.append(' = '.join([self._backtick(k[1:]), str(v)]) if columnname else v)
            else:
                q.append(' = '.join([self._backtick(k), placeholder]) if columnname else placeholder)
                a.append(v)
        return ', '.join(q), tuple(a)

    def _join_parser(self, join):
        if not join:
            return ''

        # JOIN only supports <, <=, >, >=, <> and =
        _operators = {
            '$=': '=',
            '$EQ': '=',
            '$<': '<',
            '$LT': '<',
            '$>': '>',
            '$GT': '>',
            '$<=': '<=',
            '$LTE': '<=',
            '$>=': '>=',
            '$GTE': '>=',
            '$<>': '<>',
            '$NE': '<>',
        }

        join_query = ''
        for j_table, j_on in join.items():
            join_table = self._tablename_parser(j_table)
            joins = []
            for left_column, join_right_column in j_on.items():
                # {'left_table': {'$<>': 'right_table', }, }
                if isinstance(join_right_column, dict):
                    join_right_tables = []
                    for join_method, right_column in join_right_column.items():
                        j_symbol = _operators[join_method.upper()]
                        join_right_tables.append(j_symbol.join([self._backtick(left_column),
                                                                self._backtick(right_column)]))
                    joins.append(' AND '.join(join_right_tables))
                # {'left_table': 'right_table', }
                else:
                    joins.append('='.join([self._backtick(left_column), self._backtick(join_right_column)]))
            join_query += ''.join([(' ' + join_table['join_type']) if join_table['join_type'] else '',
                                   ' JOIN ',
                                   join_table['formatted_tablename'],
                                   ' ON ',
                                   ' AND '.join(joins)])
        return join_query

    def _where_parser(self, where, placeholder='%s'):
        if not where:
            return '', ()

        result = {'q': [], 'v': ()}

        _operators = {
            '$=': '=',
            '$EQ': '=',
            '$<': '<',
            '$LT': '<',
            '$>': '>',
            '$GT': '>',
            '$<=': '<=',
            '$LTE': '<=',
            '$>=': '>=',
            '$GTE': '>=',
            '$<>': '<>',
            '$NE': '<>',
            '$LIKE': 'LIKE',
            '$BETWEEN': 'BETWEEN',
            '$IN': 'IN'
        }

        _connectors = {
            '$AND': 'AND',
            '$OR': 'OR'
        }

        negative_symbol = {
            '=': '<>',
            '<': '>=',
            '>': '<=',
            '<=': '>',
            '>=': '<',
            '<>': '=',
            'LIKE': 'NOT LIKE',
            'BETWEEN': 'NOT BETWEEN',
            'IN': 'NOT IN',
            'AND': 'OR',
            'OR': 'AND'
        }
        # TODO: confirm datetime support for more operators
        # TODO: LIKE Wildcard support

        def _get_connector(c, is_not, whitespace=False):
            c = c or '='
            c = negative_symbol.get(c) if is_not else c
            return ' ' + c + ' ' if whitespace else c

        placeholder = '%s'

        def _combining(_cond, _operator=None, upper_key=None, connector=None, _not=False):
            if isinstance(_cond, dict):
                i = 1
                for k, v in _cond.items():
                    # {'$AND':{'value':10}}
                    if k.upper() in _connectors:
                        result['q'].append('(')
                        _combining(v, upper_key=upper_key, _operator=_operator, connector=_connectors[k.upper()], _not=_not)
                        result['q'].append(')')
                    # {'>':{'value':10}}
                    elif k.upper() in _operators:
                        _combining(v, _operator=_operators[k.upper()], upper_key=upper_key, connector=connector, _not=_not)
                    # {'$NOT':{'value':10}}
                    elif k.upper() == '$NOT':
                        _combining(v, upper_key=upper_key, _operator=_operator, connector=connector, _not=not _not)
                    # {'value':10}
                    else:
                        _combining(v, upper_key=k, _operator=_operator, connector=connector, _not=_not)
                    # append 'AND' by default except for the last one
                    if i < len(_cond):
                        result['q'].append(_get_connector('AND', is_not=_not, whitespace=True))
                    i += 1

            elif isinstance(_cond, list):
                # [{'age': {'$>': 22}}, {'amount': {'$<': 100}}]
                if all(isinstance(c, dict) for c in _cond):
                    l_index = 1
                    for l in _cond:
                        _combining(l, _operator=_operator, upper_key=upper_key, connector=connector, _not=_not)
                        if l_index < len(_cond):
                            result['q'].append(_get_connector(connector, is_not=_not, whitespace=True))
                        l_index += 1
                elif _operator in ['=', 'IN'] or not _operator:
                    s_q = self._backtick(upper_key) + (' NOT' if _not else '') + ' IN (' + ', '.join(['%s'] * len(_cond)) + ')'
                    result['q'].append('(' + s_q + ')')
                    result['v'] += tuple(_cond)
                elif _operator == 'BETWEEN':
                    s_q = self._backtick(upper_key) + (' NOT' if _not else '') + ' BETWEEN ' + ' AND '.join(['%s'] * len(_cond))
                    result['q'].append('(' + s_q + ')')
                    result['v'] += tuple(_cond)
                elif _operator == 'LIKE':
                    s_q = ' OR '.join(['(' + self._backtick(upper_key) + (' NOT' if _not else '') + ' LIKE %s)'] * len(_cond))
                    result['q'].append('(' + s_q + ')')
                    result['v'] += tuple(_cond)
                # if keyword not in prefilled list but value is not dict also, should return error

            elif _cond is None:
                s_q = self._backtick(upper_key) + ' IS' + (' NOT' if _not else '') + ' NULL'
                result['q'].append('(' + s_q + ')')
            else:
                if upper_key[0] == '#':
                    item_value = _cond
                    upper_key = upper_key[1:]  # for functions, remove the # symbol and no need to quote the value
                else:
                    item_value = placeholder
                    result['v'] += (_cond,)
                s_q = ' '.join([self._backtick(upper_key), _get_connector(_operator, is_not=_not), item_value])
                result['q'].append('(' + s_q + ')')

        _combining(where)
        return ' WHERE ' + ''.join(result['q']), result['v']

    @staticmethod
    def _limit_parser(limit=None):
        if isinstance(limit, list) and len(limit) == 2:
            return ' '.join((' LIMIT', ', '.join(str(l) for l in limit)))
        elif str(limit).isdigit():
            return ' '.join((' LIMIT', str(limit)))
        else:
            return ''

    def _yield_result(self, table):
        while True:
            result = self.cur.fetchone()
            if not result:
                break
            result._setattr('_table_name', table)
            yield result

    @staticmethod
    def isstr(s):
        try:
            return isinstance(s, basestring)  # Python 2 string
        except NameError:
            return isinstance(s, six.string_types)  # Python 3 string

    def _by_columns(self, columns):
        """
        Allow select.group and select.order accepting string and list
        """
        return columns if self.isstr(columns) else self._backtick_columns(columns)

    def select(self, table, columns=None, join=None, where=None, group=None, having=None, order=None, limit=None,
               iterator=False, fetch=True, distinct=False, first=False):
        """
        :type table: string
        :type columns: list
        :type join: dict
        :param join: {'[>]table1(t1)': {'user.id': 't1.user_id'}} -> "LEFT JOIN table AS t1 ON user.id = t1.user_id"
        :type where: dict
        :type group: string|list
        :type having: string
        :type order: string|list
        :type limit: int|list
        # TODO: change to offset
        :param limit: The max row number for this query.
                      If it contains offset, limit must be a list like [offset, limit]
        :param iterator: Whether to output the result in a generator. It always returns generator if the cursor is
                         SSCursor or SSDictCursor, no matter iterator is True or False.
        :type fetch: bool
        """
        if not isinstance(table, six.string_types):
            table = table._table_name

        if first:
            limit = 1

        is_columns_selected = True
        if not columns:
            columns = ['*']
            is_columns_selected = False

        where_q, _args = self._where_parser(where)

        # TODO: support multiple table

        _sql = ''.join(['SELECT ', 'DISTINCT' if distinct else '', self._backtick_columns(columns),
                        ' FROM ', self._tablename_parser(table)['formatted_tablename'],
                        self._join_parser(join),
                        where_q,
                        (' GROUP BY ' + self._by_columns(group)) if group else '',
                        (' HAVING ' + having) if having else '',
                        (' ORDER BY ' + self._by_columns(order)) if order else '',
                        self._limit_parser(limit), ';'])

        if self.debug:
            return self.cur.mogrify(_sql, _args)

        execute_result = self.cur.execute(_sql, _args)

        if not fetch:
            return execute_result

        if self.cursorclass in (pymysql.cursors.SSCursor, pymysql.cursors.SSDictCursor):
            return self.cur

        if iterator:
            return self._yield_result(table)

        if first:
            selected = self.cur.fetchone()
            if is_columns_selected:
                selected = [selected[re.sub('^#', '', column)] for column in columns]
        else:
            selected = self.fetchall()
            if is_columns_selected:
                selected = [tuple(row[re.sub('^#', '', column)] for column in columns) for row in selected]
            else:
                for row in selected:
                    row._setattr('_is_modified', False)

        return selected

    def select_page(self, limit, offset=0, **kwargs):
        """
        :type limit: int
        :param limit: The max row number for each page
        :type offset: int
        :param offset: The starting position of the page
        :return:
        """
        start = offset
        while True:
            result = self.select(limit=[start, limit], **kwargs)
            start += limit
            if result:
                yield result
            else:
                break
            if self.debug:
                break

    def get(self, table, column, join=None, where=None, insert=False, ifnone=None):
        """
        A simplified method of select, for getting the first result in one column only. A common case of using this
        method is getting id.
        :type table: string
        :type column: str
        :type join: dict
        :type where: dict
        :type insert: bool
        :param insert: If insert==True, insert the input condition if there's no result and return the id of new row.
        :type ifnone: string
        :param ifnone: When ifnone is a non-empty string, raise an error if query returns empty result. insert parameter
                       would not work in this mode.
        """
        if isinstance(table, AttrDict):
            table = table._table_name

        select_result = self.select(table=table, columns=[column], join=join, where=where, limit=1)

        if self.debug:
            return select_result

        result = select_result[0] if select_result else None

        if result:
            return result[0]

        if ifnone:
            raise ValueError(ifnone)

        if insert:
            if any([isinstance(d, dict) for d in where.values()]):
                raise ValueError("The where parameter in get() doesn't support nested condition with insert==True.")
            return self.insert(table=table, value=where)

        return None

    def insert(self, value, ignore=False, commit=True):
        """
        Insert a dict into db.
        :type table: string
        :type value: dict
        :type ignore: bool
        :type commit: bool
        :return: int. The row id of the insert.
        """
        table = value._table_name

        value_q, _args = self._value_parser(value, columnname=False)
        _sql = ''.join(['INSERT', ' IGNORE' if ignore else '', ' INTO ', self._backtick(table),
                        ' (', self._backtick_columns(value), ') VALUES (', value_q, ');'])

        if self.debug:
            return self.cur.mogrify(_sql, _args)

        self.cur.execute(_sql, _args)
        if commit:
            self.conn.commit()
        value.id = self.cur.lastrowid

        return self.cur.lastrowid

    def upsert(self, value, update_columns=None, commit=True):
        """
        :type table: string
        :type value: dict
        :type update_columns: list
        :param update_columns: specify the columns which will be updated if record exists
        :type commit: bool
        """
        if not isinstance(value, dict):
            raise TypeError('Input value should be a dictionary')

        if not update_columns:
            update_columns = value.keys()

        table = value._table_name

        value_q, _args = self._value_parser(value, columnname=False)

        _sql = ''.join(['INSERT INTO ', self._backtick(table), ' (', self._backtick_columns(value), ') VALUES ',
                        '(', value_q, ') ',
                        'ON DUPLICATE KEY UPDATE ',
                        ', '.join(['='.join([k, 'VALUES(' + k + ')']) for k in update_columns]), ';'])

        if self.debug:
            return self.cur.mogrify(_sql, _args)

        self.cur.execute(_sql, _args)
        if commit:
            self.conn.commit()
        return self.cur.lastrowid

    def insertmany(self, columns, value, ignore=False, commit=True):
        """
        Insert multiple records within one query.
        :type columns: list
        :type value: list|tuple
        :param value: Doesn't support MySQL functions
        :param value: Example: [(value1_column1, value1_column2,), ]
        :type ignore: bool
        :type commit: bool
        :return: int. The row id of the LAST insert only.
        """
        if not isinstance(value, (list, tuple)):
            raise TypeError('Input value should be a list or tuple')

        if isinstance(value, AttrDict):
            table = value._table_name

        # Cannot add semicolon here, otherwise it will not pass the Cursor.executemany validation
        _sql = ''.join(['INSERT', ' IGNORE' if ignore else '', ' INTO ', self._backtick(table),
                        ' (', self._backtick_columns(columns), ') VALUES (', ', '.join(['%s'] * len(columns)), ')'])
        _args = tuple(value)

        # For insertmany, the base queries for executemany and printing are different
        _sql_full = ''.join(['INSERT', ' IGNORE' if ignore else '', ' INTO ', self._backtick(table),
                             ' (', self._backtick_columns(columns), ') VALUES ',
                             ', '.join([''.join(['(', ', '.join(['%s'] * len(columns)), ')'])] * len(_args)),
                             ';'])

        _args_flattened = [item for sublist in _args for item in sublist]

        if self.debug:
            return self.cur.mogrify(_sql_full, _args_flattened)

        self.cur.executemany(_sql, _args)
        if commit:
            self.conn.commit()
        return self.cur.lastrowid

    def count(self, table, where=None):
        """
        Count matched rows.
        :type table: string
        :type where: dict
        """
        if not isinstance(table, six.string_types):
            table = table._table_name

        where_q, _where_args = self._where_parser(where)

        _sql = ''.join(['SELECT COUNT(*) FROM', self._tablename_parser(table)['formatted_tablename'],
                        where_q, ';'])
        _args = _where_args

        if self.debug:
            return self.cur.mogrify(_sql, _args)

        result = self.cur.execute(_sql, _args)

        return self.fetchall()[0]['COUNT(*)']

    def exists(self, table, where=None):
        """
        Check matched row existance.
        :type table: string
        :type where: dict
        """
        if not isinstance(table, six.string_types):
            table = table._table_name

        result = self.count(table, where)
        if result > 0:
            return True
        else:
            return False

    def update(self, value, where=None, columns=None, table=None, join=None, commit=True):
        """
        :type table: string
        :type value: dict
        :type where: dict
        :type join: dict
        :type commit: bool
        """
        if table is not None:
            if not isinstance(table, six.string_types):
                table = table._table_name
        else:
            if not value._is_modified:
                return -1  # Not modified
            table = value._table_name
            if where is None:
                if value.id is None:
                    raise ValueError('id value must be set on updating.')
                where = {'id': value.id}

        if columns:
            assert isinstance(columns, (tuple, list))
            value = dict((column, value[column]) for column in columns)

        value_q, _value_args = self._value_parser(value, columnname=True)

        where_q, _where_args = self._where_parser(where)

        _sql = ''.join(['UPDATE ', self._tablename_parser(table)['formatted_tablename'],
                        self._join_parser(join),
                        ' SET ', value_q, where_q, ';'])
        _args = _value_args + _where_args

        if self.debug:
            return self.cur.mogrify(_sql, _args)

        result = self.cur.execute(_sql, _args)
        if commit:
            self.commit()

        if isinstance(value, AttrDict):
            value._setattr('_is_modified', False)
        return result

    def delete(self, value=None, where=None, table=None, commit=True):
        """
        :type table: string
        :type where: dict
        :type commit: bool
        """
        assert not((value is not None) and (table is not None))

        if table is not None:
            if not isinstance(table, six.string_types):
                table = table._table_name
        elif value is not None:
            table = value._table_name
            if where is None:
                where = {'id': value.id}

        where_q, _args = self._where_parser(where)

        alias = self._tablename_parser(table)['alias']

        _sql = ''.join(['DELETE ',
                        alias + ' ' if alias else '',
                        'FROM ', self._tablename_parser(table)['formatted_tablename'], where_q, ';'])

        if self.debug:
            return self.cur.mogrify(_sql, _args)

        result = self.cur.execute(_sql, _args)
        if commit:
            self.commit()
        return result

    def column_name(self, table):
        if not isinstance(table, six.string_types):
            table = table._table_name
        _sql = "SELECT `COLUMN_NAME` FROM `INFORMATION_SCHEMA`.`COLUMNS` WHERE `TABLE_SCHEMA`=%s AND `TABLE_NAME`=%s;"
        _args = (self.db, table)

        self.cur.execute(_sql, _args)
        return self.fetchall()

    def table_name(self):
        _sql = "SELECT `table_name` FROM `INFORMATION_SCHEMA`.`TABLES` where `TABLE_SCHEMA`=%s;"
        _args = (self.db,)

        self.cur.execute(_sql, _args)
        return self.fetchall()

    def now(self):
        query = "SELECT NOW() AS now;"
        if self.debug:
            return query

        self.cur.execute(query)
        return self.cur.fetchone()[0 if self.cursorclass is pymysql.cursors.Cursor else 'now'].strftime(
            "%Y-%m-%d %H:%M:%S")

    def last_insert_id(self):
        query = "SELECT LAST_INSERT_ID() AS lid;"
        if self.debug:
            return query

        self.query(query)
        return self.cur.fetchone()[0 if self.cursorclass is pymysql.cursors.Cursor else 'lid']

    def fetchone(self):
        return self.cur.fetchone()

    def fetchall(self):
        return list(self.cur.fetchall())

    def fetchmany(self, size=None):
        return self.cur.fetchmany(size=size)

    def lastrowid(self):
        return self.cur.lastrowid

    def rowcount(self):
        return self.cur.rowcount

    def commit(self):
        self.conn.commit()

    def rollback(self):
        self.conn.rollback()

    def __del__(self):
        try:
            self.cur.close()
            self.conn.close()
        except:
            pass

    def close(self):
        self.cur.close()
        self.conn.close()

    def get_table_class(self, table_name):
        if not (table_name in self.table_classes):
            table_class = TableDict(table_name, self)
            self.table_classes[table_name] = table_class
            self.cur.set_table_dict(table_name, table_class)
        return self.table_classes[table_name]
