#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : file_manager.py
# Author            : Gregory Kahn
# Email             :
# Date              :
# Last Modified Date: 03.17.2021
# Last Modified By  : Jiahao Yao
#
# This file is part of the VCML codebase
# Distributed under MIT license
# logging and displaying information when running

# from loguru import logger
import os
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

    badgr_dir = "."

    def __init__(self, exp_dir):
        self._exp_dir = exp_dir

        if not os.path.exists(self.cmd_fname):
            with open(self.cmd_fname, "w") as f:
                f.write(self.get_cmd_line())

        if not os.path.exists(self.git_commit_fname):
            subprocess.call(
                "cd {0}; git log --graph --pretty=format:'%C(bold red)%h%Creset -%C(yellow)%d%Creset %s %Cgreen(%cr) %C(bold blue)<%an>%Creset' --decorate  --abbrev-commit > {1}".format(
                    exp_dir, self.git_commit_fname
                ),
                shell=True,
            )
        if not os.path.exists(self.git_diff_fname):
            subprocess.call(
                "cd {0}; git diff > {1}".format(exp_dir, self.git_diff_fname),
                shell=True,
            )

        if not os.path.exists(self.git_status_fname):
            subprocess.call(
                "cd {0}; git status > {1}".format(exp_dir, self.git_status_fname),
                shell=True,
            )

    @property
    def exp_dir(self):
        os.makedirs(self._exp_dir, exist_ok=True)
        return self._exp_dir

    @property
    def cmd_dir(self):
        cmd_dir = os.path.join(self.exp_dir, "script")
        os.makedirs(cmd_dir, exist_ok=True)
        return cmd_dir

    @property
    def cmd_fname(self):
        return os.path.join(self.cmd_dir, "script.sh")

    def get_cmd_line(self):
        cmd_line_list = sys.argv
        cmd_line_list = ["\npython"] + cmd_line_list
        cmd_line = " ".join(cmd_line_list)
        return cmd_line

    ###########
    ### Git ###
    ###########

    @property
    def git_dir(self):
        git_dir = os.path.join(self.exp_dir, "git")
        os.makedirs(git_dir, exist_ok=True)
        return git_dir

    @property
    def git_commit_fname(self):
        return os.path.join(self.git_dir, "commit.txt")

    @property
    def git_diff_fname(self):
        return os.path.join(self.git_dir, "diff.txt")

    @property
    def git_status_fname(self):
        return os.path.join(self.git_dir, "status.txt")

    ##############
    ### Models ###
    ##############

    @property
    def ckpts_dir(self):
        ckpts_dir = os.path.join(self.exp_dir, "ckpts")
        os.makedirs(ckpts_dir, exist_ok=True)
        return ckpts_dir

    @property
    def ckpt_prefix(self):
        return os.path.join(self.ckpts_dir, "ckpt")
