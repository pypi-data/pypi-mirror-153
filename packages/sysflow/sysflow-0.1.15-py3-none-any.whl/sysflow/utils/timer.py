#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : timer.py
# Author            : Jiahao Yao
# Email             : jiahaoyao.math@gmail.com
# Date              : 04.04.2020
# Last Modified Date: 05.07.2021
# Last Modified By  : Jiahao Yao
#
# This file is part of the Flow codebase
# Distributed under MIT license

from collections import defaultdict
import time

class TimeIt(object):
    """Time the module
    # https://github.com/gkahn13/badgr/blob/92881c5df057aa50acbb92160afb51bea24d629f/src/badgr/utils/python_utils.py#L175-L228
    Example:
    with timeit('sth'):
        dosomething()

    for line in str(timeit).split('\n'):
        print(line)
    """
    def __init__(self, prefix=''):
        self.prefix = prefix
        self.start_times = dict()
        self.elapsed_times = defaultdict(int)

        self._with_name_stack = []

    def __call__(self, name):
        self._with_name_stack.append(name)
        return self

    def __enter__(self):
        self.start(self._with_name_stack[-1])
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        timeit.stop(self._with_name_stack.pop())

    def start(self, name):
        assert(name not in self.start_times)
        self.start_times[name] = time.time()

    def stop(self, name):
        assert(name in self.start_times)
        self.elapsed_times[name] += time.time() - self.start_times[name]
        self.start_times.pop(name)

    def elapsed(self, name):
        return self.elapsed_times[name]

    def display(self):
        for line in str(timeit).split('\n'):
            if len(line): 
                _, name, time = line.split()
                line = '{}: {}'.format(name, time)
            print(line)

    def _display(self):
        lines = []
        for line in str(timeit).split('\n'):
            if len(line): 
                _, name, time = line.split()
                line = '{}: {}'.format(name, time)
                lines.append(line)
        return lines
            
    def reset(self):
        self.start_times = dict()
        self.elapsed_times = defaultdict(int)

    def __str__(self):
        s = ''
        names_elapsed = sorted(self.elapsed_times.items(), key=lambda x: x[1], reverse=True)
        for name, elapsed in names_elapsed:
            if 'total' not in self.elapsed_times:
                s += '{0}: {1: <10} {2:.1f}\n'.format(self.prefix, name, elapsed)
            else:
                assert(self.elapsed_times['total'] >= max(self.elapsed_times.values()))
                pct = 100. * elapsed / self.elapsed_times['total']
                s += '{0}: {1: <10} {2:.1f} ({3:.1f}%)\n'.format(self.prefix, name, elapsed, pct)
        if 'total' in self.elapsed_times:
            times_summed = sum([t for k, t in self.elapsed_times.items() if k != 'total'])
            other_time = self.elapsed_times['total'] - times_summed
            assert(other_time >= 0)
            pct = 100. * other_time / self.elapsed_times['total']
            s += '{0}: {1: <10} {2:.1f} ({3:.1f}%)\n'.format(self.prefix, 'other', other_time, pct)
        return s

timeit = TimeIt()


class Timer:    
    def __enter__(self):
        self.start = time.perf_counter()
        return self

    def __exit__(self, *args):
        self.end = time.perf_counter()
        self.interval = self.end - self.start
