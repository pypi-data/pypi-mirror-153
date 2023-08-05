#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 zenbook <zenbook@zenbook-XPS>
#
# Distributed under terms of the MIT license.

"""

"""

from pymysql.cursors import DictCursor
from .core import TableDict

dict_type = TableDict(None)


class KaniCursor(DictCursor):
    dict_type = dict_type
    table_dict_list = {}
    # You can override this to use OrderedDict or other dict-like types.

    def setup_table_dict_list(self, table_dict_list):
        self.table_dict_list = table_dict_list

    def set_table_dict(self, table_name, table_dict):
        self.table_dict_list[table_name] = table_dict

    def _conv_row(self, row):
        if row is None:
            return None
        table_name = self._result.fields[0].table_name
        if table_name in self.table_dict_list:
            table_dict = self.table_dict_list[table_name]
            return table_dict(zip(self._fields, row))
        else:
            result = self.dict_type(zip(self._fields, row))
            result._setattr('_table_name', table_name)
            return result
