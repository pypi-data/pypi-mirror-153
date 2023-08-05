#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : logger.py
# Author            : Jiayuan Gu
# Email             : 
# Date              : 
# Last Modified Date: 04.12.2019
# Last Modified By  : Jiahao Yao
#
# This file is part of the VCML codebase
# Distributed under MIT license
# logging and displaying information when running
# https://github.com/maxjaritz/mvpnet/blob/master/common/utils/logger.py


import logging
import os
import sys


def setup_logger(name, save_dir, comment=''):
    """
    Useage:

    timestamp = time.strftime('%m-%d_%H-%M-%S')
    hostname = socket.gethostname()
    run_name = '{:s}.{:s}'.format(timestamp, hostname)

    logger = setup_logger('mvpnet', output_dir, comment='test.{:s}'.format(run_name))
    logger = setup_logger('mvpnet', output_dir, comment='train.{:s}'.format(run_name))
    logger.info('{:d} GPUs available'.format(torch.cuda.device_count()))
    logger.info(args)

    
    Arguments:
        name {[type]} -- [description]
        save_dir {[type]} -- [description]
    
    Keyword Arguments:
        comment {str} -- [description] (default: {''})
    
    Returns:
        [type] -- [description]
    """
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)
    ch = logging.StreamHandler(stream=sys.stdout)
    ch.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s %(name)s %(levelname)s: %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    if save_dir:
        filename = 'log'
        if comment:
            filename += '.' + comment
        log_file = os.path.join(save_dir, filename + '.txt')
        fh = logging.FileHandler(log_file)
        fh.setLevel(logging.DEBUG)
        fh.setFormatter(formatter)
        logger.addHandler(fh)

    return logger