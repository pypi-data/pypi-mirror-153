#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : file_utils.py
# Author            : Chi Han, Jiayuan Mao, Jiahao Yao
# Email             : jiahaoyao.math@gmail.com
# Date              : 09.08.2019
# Last Modified Date: 02.03.2021
# Last Modified By  : Jiahao Yao
#
# This file is part of the VCML codebase
# Distributed under MIT license
#
# file system tools


import os
import pickle
import json
import shutil
from shutil import copy2
import ruamel.yaml as yaml
import numpy as np
import pathlib


def make_parent_dir(filename):
    parent_dir = os.path.dirname(filename)
    make_dir(parent_dir)


def make_dir(path):
    if not os.path.exists(path):
        os.makedirs(path, exist_ok=True)


def is_empty(path):
    return not os.path.exists(path) or (os.path.isdir(path) and len(os.listdir(path)) == 0)


def txt_like(filename):
    equivalent_suffix = [
        '.txt',
        '.md',
        '.sh',
        '.bash',
        '.log',
        '.tex',
        '.py',
        '.bash_profile',
        '.bashrc',
        '.out'
    ]
        
    return any(filename.endswith(suffix) for suffix in equivalent_suffix)


def try_pathlib2str(path):
    if isinstance(path, pathlib.Path):
        return str(path)
    return path

def load(filename):
    filename = try_pathlib2str(filename)
    # adding the symbolic link reading
    if os.path.islink(filename): 
        filename = os.readlink(filename)
    if filename.endswith('.pkl'):
        with open(filename, 'rb') as f:
            loaded = pickle.load(f)
    elif filename.endswith('.json'):
        with open(filename, 'r') as f:
            loaded = json.load(f)
    elif filename.endswith('.yml') or filename.endswith('.yaml'): 
        with open(filename, 'r') as f:
            loaded = yaml.safe_load(f)
    elif txt_like(filename): 
        with open(filename, 'r') as f:
            loaded = f.read()
    else:
        raise Exception('File not recognized: %s' % filename)
    return loaded

class NumpyEncoder(json.JSONEncoder):
    # https://stackoverflow.com/questions/26646362/numpy-array-is-not-json-serializable
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)

def dump(content, filename):
    # robust argument
    if (isinstance(content, str) or isinstance(content, pathlib.Path)) and (not isinstance(filename, str) and not isinstance(filename, pathlib.Path)):
        # BEAWARE: str might be insufficient
        # swap 
        content, filename = filename, content

    filename = try_pathlib2str(filename)
    if filename.endswith('.pkl'):
        with open(filename, 'wb') as f:
            pickle.dump(content, f, protocol=pickle.HIGHEST_PROTOCOL)
    elif filename.endswith('.json'):
        with open(filename, 'w') as f:
            json.dump(content, f, indent=4, cls=NumpyEncoder)
    elif filename.endswith('.yml') or filename.endswith('.yaml'): 
        with open(filename, 'w') as f:
            yaml.safe_dump(content, f, default_flow_style=False)
    elif txt_like(filename): 
        with open(filename, 'w') as f:
            f.write(content)
    else:
        raise Exception('File not recognized: %s' % filename)


def load_knowledge(name, knowledge_type, logger=None, from_source=False):
    filename = os.path.join(
        'knowledge',
        'source' if from_source else '',
        f'{name}_{knowledge_type}.json'
    )
    if os.path.exists(filename):
        knowledge = load(filename)
    else:
        knowledge = None
    if logger is not None:
        if knowledge is not None:
            logger(f'Loading knowledge \"{knowledge_type}\" for {name} '
                   f'length = {len(knowledge)}')
        else:
            logger(f'Loading knowledge \"{knowledge_type}\", but is None')
    return knowledge


def copy_verbose(src, dst, logger=None):
    message = f'copying from {src} to {dst}'
    if logger is not None:
        logger(message)
    else:
        print(message)
    copy2(src, dst)


def copytree_verbose(src, dst, logger=None):
    shutil.copytree(src, dst, copy_function=copy_verbose)

def get_lastline(file_str):
    return file_str.strip().split('\n')[-1]
    