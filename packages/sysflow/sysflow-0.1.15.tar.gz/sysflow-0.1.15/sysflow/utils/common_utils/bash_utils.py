#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : bash_utils.py
# Author            : Jiahao Yao
# Email             : jiahaoyao.math@gmail.com
# Date              : 05.05.2022
# Last Modified Date: 05.05.2022
# Last Modified By  : Jiahao Yao
#
# This file is part of the SYSflow codebase
# Distributed under MIT license
#
# bash script tools
# use python to call bash script

import subprocess

def bash(cmd, output=False):
    if output: 
        return subprocess.Popen(cmd.split(), stdout=subprocess.PIPE).communicate()[0].strip().decode('utf-8')
    else: 
        subprocess.call(cmd, shell=True)
        


