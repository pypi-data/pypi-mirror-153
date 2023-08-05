#! /usr/bin/env python
# -*- coding: utf-8 -*-
# vim:fenc=utf-8
#
# Copyright © 2018 zenbook <zenbook@zenbook-XPS>
#
# Distributed under terms of the MIT license.

"""

"""


def count(column):
    return '#COUNT(`%s`)' % (column)


def sum(column):
    return '#SUM(`%s`)' % (column)


def desc(column):
    return '#`%s` DESC' % (column)


def escape(query):
    return '#%s' % (query)
