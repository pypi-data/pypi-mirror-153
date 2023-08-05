#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : io_utils.py
# Author            : Jiahao Yao
# Email             : jiahaoyao.math@gmail.com
# Date              : 03.16.2021
# Last Modified Date: 03.16.2020
# Last Modified By  : Jiahao Yao
#
# This file is part of the sysflow codebase
# Distributed under MIT license
#
# python basic io utilities
import pyperclip

def cprint(a):
    print(a)
    # safe 
    try: 
        pyperclip.copy(a)
    except: 
        pass

def sth(num):
    def S(num):
        "English ordinal suffix for the day of the month, 2 characters; i.e. 'st', 'nd', 'rd' or 'th'"
        if num in (11, 12, 13):  # Special case
            return "th"
        last = num % 10
        if last == 1:
            return "st"
        if last == 2:
            return "nd"
        if last == 3:
            return "rd"
        return "th"
    return "{}".format(num) + S(num)