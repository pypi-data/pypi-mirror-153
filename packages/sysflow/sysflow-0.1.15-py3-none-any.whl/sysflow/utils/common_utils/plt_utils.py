#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : plt_utils.py
# Author            : Chi Han, Jiayuan Mao
# Email             : haanchi@gmail.com, maojiayuan@gmail.com
# Date              : 09.08.2019
# Last Modified Date: 04.10.2019
# Last Modified By  : Chi Han, Jiayuan Mao
#
# This file is part of the VCML codebase
# Distributed under MIT license
#
# printing / visualization


import matplotlib
import numpy as np
import matplotlib.pyplot as plt

def import_plt(style="seaborn-darkgrid", backend="Qt5Agg", fontsize=10, usetex=True):
    # robust backend
    try: 
        matplotlib.use(backend)
    except: 
        try: 
            matplotlib.use('TKAgg')
        except: 
            matplotlib.use('Agg')
        
    plt.style.use(style)
    plt.rc("text", usetex=usetex)
    if usetex:
        matplotlib.rcParams["text.latex.preamble"] = [
            r"\usepackage{amssymb}",
            r"\usepackage{amsmath}",
            r"\usepackage{xcolor}",
        ]

    nice_fonts = {
    # Use LaTeX to write all text
    "text.usetex": usetex,
    "font.family": "serif",
    # Use 10pt font in plots, to match 10pt font in document
    "axes.labelsize": fontsize + 2,
    "font.size": fontsize + 2,
    # Make the legend/label fonts a little smaller
    "legend.fontsize": fontsize,
    "xtick.labelsize": fontsize,
    "ytick.labelsize": fontsize,
    }
    matplotlib.rcParams.update(nice_fonts)


def set_size(width=345, fraction=1, subplots=(1, 1)):
    """ Set figure dimensions to avoid scaling in LaTeX.

    Parameters
    ----------
    width: float or string
            Document width in points, or string of predined document type
    fraction: float, optional
            Fraction of the width which you wish the figure to occupy
    subplots: array-like, optional
            The number of rows and columns of subplots.
    Returns
    -------
    fig_dim: tuple
            Dimensions of figure in inches
    """
    if width == "thesis":
        width_pt = 426.79135
    elif width == "beamer":
        width_pt = 307.28987
    elif width == "pnas":
        width_pt = 246.09686
    else:
        width_pt = width

    # Width of figure (in pts)
    fig_width_pt = width_pt * fraction
    # Convert from pt to inches
    inches_per_pt = 1 / 72.27

    # Golden ratio to set aesthetic figure height
    golden_ratio = (5 ** 0.5 - 1) / 2

    # Figure width in inches
    fig_width_in = fig_width_pt * inches_per_pt
    # Figure height in inches
    fig_height_in = fig_width_in * golden_ratio * (subplots[0] / subplots[1])

    return (fig_width_in, fig_height_in)


def latex(label):
    return '$\\text{' + label + '}$'

def get_axes(num, plt):
    nrows = int(np.sqrt(num))
    ncols = num // nrows + 1

    fig, ax = plt.subplots(nrows=nrows, ncols=ncols, figsize=(ncols * 6.4, nrows * 4.8))
    ax_array = ax.flatten()
    return fig, ax_array

def plt_st(nrows=1, ncols=1, sharex=False, sharey=False):
    fig, ax = plt.subplots(nrows=nrows, ncols=ncols, sharex=False, sharey=False, figsize=set_size(subplots=(nrows, ncols)))
    return fig, ax

def plt_end(filename=None, show=True, tight=True, grid=True):
    if grid: 
        plt.grid()
    if tight:
        plt.tight_layout()
    if filename:
        plt.savefig(filename+'.pdf')
        plt.savefig(filename+'.png')
    if show:
        plt.show()
    plt.close()
    