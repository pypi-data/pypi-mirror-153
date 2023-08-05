#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : file_manager.py
# Author            : Gregory Kahn
# Email             : 
# Date              : 
# Last Modified Date: 04.12.2020
# Last Modified By  : Jiahao Yao
#
# This file is part of the VCML codebase
# Distributed under MIT license
# logging and displaying information when running

from loguru import logger
import os
import shutil
import subprocess
import sys


class FileManager(object):
    """
    def _log(self):
        logger.info('')
        logger.info('Step {0}'.format(self._get_global_step_value() - 1))
        for key, value in sorted(self._tb_logger.items(), key=lambda kv: kv[0]):
            logger.info('{0} {1:.6f}'.format(key, np.mean(value)))
        self._tb_logger.clear()

        for line in str(timeit).split('\n'):
            logger.debug(line)
        timeit.reset()
    
    Arguments:
        object {[type]} -- [description]
    
    Returns:
        [type] -- [description]
    """
    def __init__(self, exp_name, log_fname=None, config_fname=None, add_logger=True):
        self._exp_name = exp_name
        self._exp_dir = exp_name
        self.badgr_dir = os.getcwd()
        print('setting up experiment: {0}'.format(self._exp_name))

        if not os.path.exists(self.git_commit_fname):
            subprocess.call('cd {0}; git log -1 > {1}'.format(self.badgr_dir, self.git_commit_fname),
                            shell=True)
        if not os.path.exists(self.git_diff_fname):
            subprocess.call('cd {0}; git diff > {1}'.format(self.badgr_dir, self.git_diff_fname),
                            shell=True)

        if config_fname is not None:
            shutil.copy(config_fname, os.path.join(self.exp_dir, 'config.py'))

        if add_logger:
            logger.remove()
            if log_fname:
                logger.add(os.path.join(self.exp_dir, log_fname),
                           format=self._exp_name + " {time} {level} {message}",
                           level="DEBUG")
            logger.add(sys.stdout,
                       colorize=True,
                       format="<yellow>" + self._exp_name + "</yellow> | "
                              "<green>{time:HH:mm:ss}</green> | "
                              "<blue>{level: <8}</blue> | "
                              "<magenta>{name}:{function}:{line: <5}</magenta> | "
                              "<white>{message}</white>",
                       level="DEBUG",
                       filter=lambda record: record["level"].name == "DEBUG")
            logger.add(sys.stdout,
                       colorize=True,
                       format="<yellow>" + self._exp_name + "</yellow> | "
                               "<green>{time:HH:mm:ss}</green> | "
                               "<blue>{level: <8}</blue> | "
                               "<white>{message}</white>",
                       level="INFO")

    @property
    def exp_dir(self):
        os.makedirs(self._exp_dir, exist_ok=True)
        return self._exp_dir

    ###########
    ### Git ###
    ###########

    @property
    def git_dir(self):
        git_dir = os.path.join(self.exp_dir, 'git')
        os.makedirs(git_dir, exist_ok=True)
        return git_dir

    @property
    def git_commit_fname(self):
        return os.path.join(self.git_dir, 'commit.txt')

    @property
    def git_diff_fname(self):
        return os.path.join(self.git_dir, 'diff.txt')

    ##############
    ### Models ###
    ##############

    @property
    def ckpts_dir(self):
        ckpts_dir = os.path.join(self.exp_dir, 'ckpts')
        os.makedirs(ckpts_dir, exist_ok=True)
        return ckpts_dir

    @property
    def ckpt_prefix(self):
        return os.path.join(self.ckpts_dir, 'ckpt')