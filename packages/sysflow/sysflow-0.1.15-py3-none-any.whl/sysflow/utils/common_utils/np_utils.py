#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : np_utils.py
# Author            : Jiahao Yao
# Email             : jiahaoyao.math@gmail.com
# Date              : 03.31.2020
# Last Modified Date: 03.31.2020
# Last Modified By  : Jiahao Yao
#
# This file is part of the flow codebase
# Distributed under MIT license
#
# numpy tools

def matprint(mat, fmt="g"):
    # adapted from: https://gist.github.com/lbn/836313e283f5d47d2e4e
    col_maxes = [max([len(("{:"+fmt+"}").format(x)) for x in col]) for col in mat.T]
    for x in mat:
        for i, y in enumerate(x):
            print(("{:"+str(col_maxes[i])+fmt+"}").format(y), end="  ")
        print("")
        