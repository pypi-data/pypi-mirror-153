#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : logger.py
# Author            : Jiahao Yao
# Email             : jiahaoyao.math@gmail.com
# Date              : 03.17.2021
# Last Modified Date: 03.17.2021
# Last Modified By  : Jiahao Yao
#
# This file is part of the VCML codebase
# Distributed under MIT license
# setup logger before running experiments 

import datetime
import os
import random
import sys
import uuid 
import inspect

import dateutil.tz
from sysflow.log.file_manager import FileManager
from sysflow.log.logger_utils import get_logger
from sysflow.utils.common_utils.file_utils import dump, load, make_dir


# set up the logger's
def exp_setup(exp_name, args):
    # args: namespace
    try: 
        file_path = os.path.abspath(sys.modules['__main__'].__file__)
    except: 
        try: 
            file_path = os.path.abspath(inspect.stack()[1].filename )
        except: 
            file_path = os.getcwd()
            
    if os.path.isdir(file_path): 
        data_dir = os.path.join(file_path, "exp")
    else: 
        data_dir = os.path.join(os.path.dirname(file_path), "exp")
    make_dir(data_dir)

    exp_dir = os.path.join(data_dir, exp_name)
    make_dir(exp_dir)

    now = datetime.datetime.now(dateutil.tz.tzlocal())
    timestamp = now.strftime("%m_%d_%Y_%H_%M_%S")
    # avoid collision
    run_id = str(uuid.uuid4())
    random_timestamp = "{}_{}".format(timestamp, run_id)
    exp_dir = os.path.join(exp_dir, random_timestamp)
    make_dir(exp_dir)

    # git-info
    FileManager(exp_dir)

    args.exp_dir = exp_dir

    params = vars(args)
    # save params
    param_dir = os.path.join(exp_dir, "train_params.json")
    dump(params, param_dir)

    # logger serve as stdout
    logger = get_logger(logpath=os.path.join(exp_dir, "logs"), filepath=file_path)
    logger.info(args)
    logger.info(exp_dir)

    # sys is global vars
    cmd_line = "python " + " ".join(sys.argv)
    logger.info(cmd_line)

    return exp_dir, logger
