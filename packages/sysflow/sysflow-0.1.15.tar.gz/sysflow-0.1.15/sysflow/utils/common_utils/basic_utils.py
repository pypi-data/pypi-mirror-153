#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : basic_utils.py
# Author            : Jiahao Yao
# Email             : jiahaoyao.math@gmail.com
# Date              : 09.08.2019
# Last Modified Date: 10.21.2020
# Last Modified By  : Jiahao Yao
#
# This file is part of the VCML codebase
# Distributed under MIT license
#
# python basic utilities

import sys
import numpy as np
import itertools
import operator

def dict_gather(dicts):
    summon = {}
    for d in dicts:
        for key, value in d.items():
            if key not in summon:
                summon[key] = []
            summon[key].append(value)
    output = {
        key: np.array(values)
        for key, values in summon.items()
    }
    return output

def merge_dicts(d1, d2):
    # merge two dicts without duplication
    # https://stackoverflow.com/questions/31323388/merging-two-dicts-in-python-with-no-duplication-permitted
    return {} if any(d1[k] != d2[k] for k in d1.keys() & d2) else dict(d1, **d2)

def inverse_dict(d):
    inv_map = {v: k for k, v in d.items()}
    return inv_map

def contains(x, elements):
    for e in elements:
        if e in x:
            return True
    return False


def only_contains(x, elements):
    for y in x:
        if y not in elements:
            return False
    return True


def belongs_to(stats, query):
    for cat, items in stats.items():
        if query in items:
            return cat
    return None


def intersection(*arg, as_set=False):
    """
    Taking the intersection of multiple iterables.
    """
    output = arg[0]

    if as_set:
        output = set(output)
    else:
        # as list
        output = list(output)

    for y in arg[1:]:
        if as_set:
            output = output.intersection(set(y))
        else:
            set_y = set(y)
            output = [i for i in output if i in set_y]

    return output


def union(*arg, as_set=False):
    """
    Taking the union of multiple iterables
    If the first input is set, or `as_set` is True, the output will be cast
    to a set variable. Otherwise, the output will be a list instance
    """

    output = arg[0]

    if as_set:
        output = set(output)
    else:
        # as list
        output = list(output)

    for y in arg[1:]:
        if as_set:
            output = output.union(set(y))
        else:
            set_output = set(output)
            output = output + [i for i in y if i not in set_output]

    return output


def sum_list(*arg):
    output = arg[0]
    for y in arg[1:]:
        output = output + y
    return output


def difference(x, y):
    # only set or list supported
    if isinstance(x, set):
        return x.difference(set(y))
    else:
        set_y = set(y)
        return [i for i in x if i not in set_y]


def get_size(obj, seen=None):
    """Recursively finds size of objects"""
    size = sys.getsizeof(obj)
    if seen is None:
        seen = set()
    obj_id = id(obj)
    if obj_id in seen:
        return 0
    seen.add(obj_id)
    if isinstance(obj, dict):
        size += sum([get_size(v, seen) for v in obj.values()])
        size += sum([get_size(k, seen) for k in obj.keys()])
    elif hasattr(obj, '__dict__'):
        size += get_size(obj.__dict__, seen)
    elif hasattr(obj, '__iter__') and\
            not isinstance(obj, (str, bytes, bytearray)):
        size += sum([get_size(i, seen) for i in obj])
    return size


class matrix_dict:
    """
    A matrix-like dict class
    Each query takes two keys
    """
    def __init__(self, keys_x, keys_y, values):
        self.keys_x = keys_x
        self.keys_y = keys_y
        self.values = values
        self.build_dict()
        self.assert_values()

    def build_dict(self):
        self.dict_x = dict(zip(self.keys_x, range(self.dim_x)))
        self.dict_y = dict(zip(self.keys_y, range(self.dim_y)))

    def assert_values(self):
        values = self.values
        assert isinstance(values, list) and len(values) == self.dim_x
        for y_values in values:
            assert isinstance(y_values, list)
            assert len(y_values) == self.dim_y

    @property
    def dim_x(self):
        return len(self.keys_x)

    @property
    def dim_y(self):
        return len(self.keys_y)

    def __getitem__(self, query):
        query_x, query_y = query
        output = self.values[
            self.dict_x[query_x]
        ][
            self.dict_y[query_y]
        ]
        return output


#python utils
def sortB(a, b, reverse=False):
    # sort A with B
    ab = sorted(zip(a, b), key=operator.itemgetter(1), reverse=reverse)
    a2, b2 = zip(*ab)
    if isinstance(a, str):
        return str(a2), str(b2)
    elif isinstance(a, list):
        return list(a2), list(b2)
    elif isinstance(a, np.ndarray):
        return np.array(a2), np.array(b2)
    else:
        return a2, b2

def sortBs(a_list, b, reverse=False):
    # sort A_list with B
    n = len(a_list)
    new_a_list = []
    for i, a in enumerate(a_list):
        if i == n - 1: 
            new_a, new_b = sortB(a, b, reverse=reverse)
        else: 
            new_a, _ = sortB(a, b, reverse=reverse)
        new_a_list.append(new_a)
    return new_a_list, new_b
        
def unilist(a):
    return list(set(a))

def unilistB(a, b=None):
    # https://stackoverflow.com/questions/12897374/get-unique-values-from-a-list-in-python
    # filter list a with unique b
    used = set()
    if b == None:
        b = a
    unique = [aa for aa, bb in zip(a,b) if bb not in used and (used.add(bb) or True)]
    return unique

def chunklist(seq, num):
    # https://stackoverflow.com/questions/2130016/splitting-a-list-into-n-parts-of-approximately-equal-length
    k, m = divmod(len(seq), num)
    return (seq[i * k + min(i, m):(i + 1) * k + min(i + 1, m)] for i in range(num))

# flatten the list of lists
# https://stackoverflow.com/questions/952914/how-to-make-a-flat-list-out-of-list-of-lists?page=1&tab=active#tab-top
flattenlist = lambda l: [item for sublist in l for item in sublist]

def concatlist(l_list):
    # https://stackoverflow.com/questions/716477/join-list-of-lists-in-python
    return list(itertools.chain.from_iterable(l_list))

def translist(l_list):
    # https://stackoverflow.com/questions/23940937/reshape-list-of-lists-based-on-position-of-the-element
    return [list(x) for x in zip(*l_list)]

# transpose the list of tuples
# https://stackoverflow.com/questions/43437240/pythonic-way-to-flip-a-list-tuple
transpose_list = lambda t: list(zip(*t))
