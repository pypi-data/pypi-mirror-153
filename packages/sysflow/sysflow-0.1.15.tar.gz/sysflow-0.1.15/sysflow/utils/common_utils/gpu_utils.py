#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : interactive.py
# Author            : Jiahao Yao
# Email             : jiahaoyao.math@gmail.com
# Date              : 09.18.2020
# Last Modified Date: 09.18.2020
# Last Modified By  : Jiahao Yao
#
# This file is part of the FLOW codebase
# Distributed under MIT license

import os 
import numpy as np

def get_freer_gpu():
    os.system('nvidia-smi -q -d Memory |grep -A4 GPU|grep Free >tmp')
    memory_available = [int(x.split()[2]) for x in open('tmp', 'r').readlines()]
    return np.argmax(memory_available)
