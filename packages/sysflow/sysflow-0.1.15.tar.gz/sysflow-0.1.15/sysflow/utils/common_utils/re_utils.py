#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : re_utils.py
# Author            : Jiahao Yao
# Email             : jiahaoyao.math@gmail.com
# Date              : 05.05.2022
# Last Modified Date: 05.05.2022
# Last Modified By  : Jiahao Yao
#
# This file is part of the SYSflow codebase
# Distributed under MIT license
#
# regex python tools

import re


# reference: https://stackoverflow.com/questions/4703390/how-to-extract-a-floating-number-from-a-string
# TODO: combine the two? 
num_regex = r"[-+]?\d*\.?\d+|[-+]?\d+"
sci_num_regex = r"[-+]?\d*\.?\d+[eE][-+]?\d+"
