#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : tensor_utils.py
# Author            : Chi Han, Jiayuan Mao
# Email             : haanchi@gmail.com, maojiayuan@gmail.com
# Date              : 09.08.2019
# Last Modified Date: 02.10.2019
# Last Modified By  : Chi Han, Jiayuan Mao
#
# This file is part of the VCML codebase
# Distributed under MIT license
#
# pytorch/numpy utilities


import numpy as np
import torch
import torch.nn.functional as F
from pprint import pprint


def to_tensor(x):
    if isinstance(x, torch.Tensor):
        return x
    elif isinstance(x, list):
        if isinstance(x[0], float):
            return torch.Tensor(x)
        elif isinstance(x[0], int):
            return torch.LongTensor(x)
        else:
            return x
    elif isinstance(x, np.ndarray):
        if x.dtype.char in ['d', 'f']:
            return torch.Tensor(x)
        elif x.dtype.char in ['l', 'b']:
            return torch.LongTensor(x)
        else:
            raise Exception('not convertable')
    elif isinstance(x, int) or isinstance(x, float) \
            or np.isscalar(x):
        return torch.tensor(x)
    else:
        raise Exception('not convertable')


def detach(tensor):
    if isinstance(tensor, torch.Tensor):
        if tensor.device.type == 'cuda':
            tensor = tensor.cpu()
        if tensor.requires_grad:
            tensor = tensor.detach()
        tensor = tensor.numpy()

    return tensor


def matmul(*mats):
    output = mats[0]
    for x in mats[1:]:
        if isinstance(output, torch.Tensor):
            output = torch.matmul(output, x)
        else:
            output = np.matmul(output, x)
    return output


def to_numpy(x):
    if isinstance(x, np.ndarray):
        return x
    elif isinstance(x, list):
        return np.array(x)
    elif isinstance(x, torch.Tensor):
        return x.cpu().detach().numpy()
    elif isinstance(x, torch.autograd.Variable):
        return x.data.cpu().numpy()


def to_normalized(x):
    if isinstance(x, torch.Tensor):
        return F.normalize(x, dim=-1)
    elif isinstance(x, np.ndarray):
        return to_normalized(torch.Tensor(x)).numpy()
    else:
        raise Exception('unsupported type: %s' % str(type(x)))


def init_seed(n=-1, index=-1):
    if n != -1:
        if index != -1:
            seed = n + index
        else:
            seed = n
        torch.manual_seed(seed)
        np.random.seed(seed)


def is_cuda(x):
    return x.device.type == 'cuda'


def valid_part(x, assert_finite=False):
    output = torch.isnan(x).bitwise_not() * (x.abs() != float('inf'))
    if assert_finite:
        output = output * (x.abs() < 1e10)
    return output


def is_valid_value(x, assert_finite):
    if not valid_part(x, assert_finite).all():
        return False
    else:
        return True


def assert_valid_value(*values, assert_finite=False):
    for i, x in enumerate(values):
        if not is_valid_value(x, assert_finite):
            pprint(values)
            print('Invalid tensor is', i)
            raise Exception('invalid value')


def index_by_list(tensor, indexes):
    if isinstance(tensor, torch.Tensor) or \
            isinstance(tensor, np.ndarray):
        return tensor[indexes]
    elif isinstance(tensor, list) or \
            isinstance(tensor, tuple):
        return [tensor[ind] for ind in indexes]
    else:
        raise Exception()


#  tools for visualization
import matplotlib
from matplotlib.lines import Line2D
def plot_grad_flow(named_parameters):
    '''Plots the gradients flowing through different layers in the net during training.
    Can be used for checking for possible gradient vanishing / exploding problems.

    Usage: Plug this function in Trainer class after loss.backwards() as
    "plot_grad_flow(self.model.named_parameters())" to visualize the gradient flow'''
    ave_grads = []
    max_grads= []
    layers = []
    for n, p in named_parameters:
        if(p.requires_grad) and ("bias" not in n):
            layers.append(n)
            ave_grads.append(p.grad.abs().mean())
            max_grads.append(p.grad.abs().max())
    plt.bar(np.arange(len(max_grads)), max_grads, alpha=0.1, lw=1, color="c")
    plt.bar(np.arange(len(max_grads)), ave_grads, alpha=0.1, lw=1, color="b")
    plt.hlines(0, -0.5, len(ave_grads)+0.5, lw=2, color="k" )
    plt.xticks(range(0,len(ave_grads), 1), layers)
    plt.xlim(left=-0.5, right=len(ave_grads)-0.5)
    plt.ylim(bottom = -0.001, top=0.10) # zoom in on the lower gradient regions
    plt.xlabel("Layers")
    plt.ylabel("average gradient")
    plt.title("Gradient flow")
    plt.grid(True)
    plt.legend([Line2D([0], [0], color="c", lw=4),
                Line2D([0], [0], color="b", lw=4),
                Line2D([0], [0], color="k", lw=4)], ['max-gradient', 'mean-gradient', 'zero-gradient'])
    plt.tight_layout()
    plt.show()


device = None

def init_gpu(use_gpu=True, gpu_id=0):
    global device
    if torch.cuda.is_available() and use_gpu:
        device = torch.device("cuda:" + str(gpu_id))
        print("Using GPU id {}".format(gpu_id))
    else:
        device = torch.device("cpu")
        print("GPU not detected. Defaulting to CPU.")


def set_device(gpu_id):
    torch.cuda.set_device(gpu_id)

class Ipdb(nn.Module):
    def __init__(self):
        super().__init__()
    def forward(self, x):
        import ipdb; ipdb.set_trace()
        return x
