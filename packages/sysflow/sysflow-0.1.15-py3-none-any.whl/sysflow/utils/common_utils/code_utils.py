#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# File              : io_utils.py
# Author            : Jiahao Yao
# Email             : jiahaoyao.math@gmail.com
# Date              : 03.16.2021
# Last Modified Date: 03.16.2020
# Last Modified By  : Jiahao Yao
#
# This file is part of the sysflow codebase
# Distributed under MIT license
#
# python basic code template utilities
from sysflow.utils.common_utils.io_utils import cprint
import re
import argparse

def str2bool(v):
    if isinstance(v, bool):
       return v
    if v.lower() in ('yes', 'true', 't', 'y', '1'):
        return True
    elif v.lower() in ('no', 'false', 'f', 'n', '0'):
        return False
    else:
        raise argparse.ArgumentTypeError('Boolean value expected.')


def pack_params(*params, header=True):
    # https://github.com/Microsoft/vscode/issues/12146
    lines = []
    for param in params: 
        assert isinstance(param, str) 
        # exec('self.{} = {}'.format(param, param))
        lines.append('self.{} = {}'.format(param, param))
    if header: 
        lines = ['#region save the params'] + lines + ['#endregion']
    cprint('\n'.join(lines))

def load_params(*params, header=True):
    lines = []
    for param in params: 
        assert isinstance(param, str) 
        # exec('{} = self.{}'.format(param, param))
        lines.append('{} = self.{}'.format(param, param))
    if header: 
        lines = ['#region unpack the params'] + lines + ['#endregion']
    cprint('\n'.join(lines))

def pack_dict(d, *params, header=True):
    lines = []
    for param in params: 
        assert isinstance(param, str) 
        # exec("{}['{}'] = {}".format(d, param, param))
        lines.append("{}['{}'] = {}".format(d, param, param))
    if header: 
        lines = ['#region save the params'] + lines + ['#endregion']
    cprint('\n'.join(lines))
        
def load_dict(d, *params, header=True):
    lines = []
    for param in params: 
        assert isinstance(param, str) 
        # exec("{} = {}['{}']".format(param, d, param), globals())
        lines.append("{} = {}['{}']".format(param, d, param))
    if header: 
        lines = ['#region unpack the params'] + lines + ['#endregion']
    cprint('\n'.join(lines))

def load_hp(*params, header=True):
    # load the parameter for hpman      
    lines = []
    for param in params: 
        assert isinstance(param, str) 
        # exec("{} = {}['{}']".format(param, d, param), globals())
        lines.append("{} = _.get_value('{}')".format(param, param))
    if header: 
        lines = ['#region unpack the params'] + lines + ['#endregion']
    cprint('\n'.join(lines))

def arg2hp(s, header=True):
    # argparse to hpman
    s = s.replace("\"", "'")
    lines = []
    for line in s.split('\n'): 
        line = line.strip()
        if len(line) and line[0]!='#':
            var = re.findall(r"'--(.*?)'", line)[0] 
            val = re.findall(r"default=(.*)\)", line)[0] 
            lines.append("{} = _('{}', {})".format(var, var, val))
    if header: 
        lines = ['#region hpman parameters'] + lines + ['#endregion']
    cprint('\n'.join(lines))

def hp2arg(s, header=True):
    # hpman to argparse
    s = s.replace("\"", "'")
    lines = []
    extra_head = None
    for line in s.split('\n'): 
        line = line.strip()
        if len(line) and line[0]!='#':
            var, val = re.findall(r"\('(.*?)',\ (.*?)\)", line)[0]
            pyval = eval(val, {"__builtins__":None})
            # https://stackoverflow.com/questions/9072847/interpreting-strings-as-other-data-types-in-python
            val_type = type(pyval).__name__
            if val_type == 'bool': 
                val_type = 'str2bool'
                extra_head = 'from sysflow.utils.common_utils.code_utils import str2bool'
            lines.append("parser.add_argument('--{}', type={}, default={})".format(var, val_type, val))
    if extra_head: 
        lines = [extra_head] + lines

    if header: 
        lines = ['#region argparse parameters'] + lines + ['#endregion']
    cprint('\n'.join(lines))

def load_hp2hp(s, header=True):
    # load the parameter for hpman      
    lines = []
    s = s.replace("\"", "'")
    for line in s.split('\n'): 
        line = line.strip()
        if len(line) and line[0]!='#':
            var = re.findall(r"\('(.*?)',", line)[0] 
            lines.append("{} = _.get_value('{}')".format(var, var))
    if header: 
        lines = ['#region unpack the params'] + lines + ['#endregion']
    cprint('\n'.join(lines))


# colab function 
def hp2colab(s):
    # hpman to colab notebook
    TYPE_COLAB = {
        'int': 'integer', 
        'float': 'number', 
        'bool': 'boolean', 
        'str': 'string'
    }
    s = s.replace("\"", "'")
    lines = []
    var_list = []
    for line in s.split('\n'): 
        line = line.strip()
        if len(line) and line[0]!='#':
            var, val = re.findall(r"\('(.*?)',\ (.*?)\)", line)[0]
            var_list.append(var)
            pyval = eval(val, {"__builtins__":None})
            # https://stackoverflow.com/questions/9072847/interpreting-strings-as-other-data-types-in-python
            val_type = type(pyval).__name__
            val_type = TYPE_COLAB[val_type]
            lines.append("{} = {} #@param {{type:'{}'}}".format(var, val, val_type))

    lines.append('\nfrom argparse import Namespace')

    namespace_line = ['{}={}'.format(var, var) for var in var_list]
    lines.append('args = Namespace({})'.format(', '.join(namespace_line)))
    
    cprint('\n'.join(lines))


def arg2colab(s):
    # hpman to colab notebook
    TYPE_COLAB = {
        'int': 'integer', 
        'float': 'number', 
        'str2bool': 'boolean', 
        'str': 'string'
    }
    s = s.replace("\"", "'")
    lines = []
    var_list = []
    for line in s.split('\n'): 
        line = line.strip()
        if len(line) and line[0]!='#':
            var, val_type, val = re.findall(r"'--(.*?)', *type=(.*?), *default=(.*?)[,\)]", line)[0]
            var_list.append(var)
            val_type = TYPE_COLAB[val_type]
            if 'help' in line: 
                comment = re.findall(r"help='(.*?)'\)", line)[0]
                lines.append("# {} \n{} = {} #@param {{type:'{}'}}".format(comment, var, val, val_type))

            else: 
                lines.append("{} = {} #@param {{type:'{}'}}".format(var, val, val_type))
        else: 
            if len(line) and line[0] == '#': 
                lines.append('#@markdown' + line[1:])
            else: 
                lines.append(line)
    lines.append('\nfrom argparse import Namespace')
    
    namespace_line = ['{}={}'.format(var, var) for var in var_list]
    lines.append('args = Namespace({})'.format(', '.join(namespace_line)))
    
    cprint('\n'.join(lines))


def load_hp2arg(s, header=True):
    # load the parameter using hpman to using argparse
    lines = []
    s = s.replace("\"", "'")
    for line in s.split('\n'): 
        line = line.strip()
        if len(line) and line[0]!='#':
            var = re.findall(r"\('(.*?)'\)", line)[0] 
            lines.append("{} = args.{}".format(var, var))
    if header: 
        lines = ['#region unpack the params'] + lines + ['#endregion']
    cprint('\n'.join(lines))

def load_hp2self(s, header=True):
    # load the parameter using hpman to using argparse
    lines = []
    s = s.replace("\"", "'")
    for line in s.split('\n'): 
        line = line.strip()
        if len(line) and line[0]!='#':
            var = re.findall(r"\('(.*?)'\)", line)[0] 
            lines.append("self.{} = {}".format(var, var))
    if header: 
        lines = ['#region unpack the params'] + lines + ['#endregion']
    cprint('\n'.join(lines))

def load_hp2pack_self(s, header=True):
    # load the parameter using hpman to using argparse
    lines = []
    s = s.replace("\"", "'")
    for line in s.split('\n'): 
        line = line.strip()
        if len(line) and line[0]!='#':
            var = re.findall(r"\('(.*?)'\)", line)[0] 
            lines.append("{} = self.{}".format(var, var))
    if header: 
        lines = ['#region unpack the params'] + lines + ['#endregion']
    cprint('\n'.join(lines))


def get_uniq(s): 
    # remove the repeating arguments (because we might paste the code everywhere)
    s_list = s.split('\n')
    unique_s_list = []
    for ss in s_list: 
        if ( len(ss.strip()) > 0 ) and (ss not in unique_s_list) and (ss.strip()[0]!= '#'):
            unique_s_list.append(ss)
    cprint('\n'.join(unique_s_list))

if __name__ == '__main__':
    a = 1
    b = 2 
    mydict = {}
    pack_dict('mydict', 'b')

    mydict2 = {}
    pack_dict('mydict2', 'a', 'b')


    mydict3 = {'ab': 2, 'cd': 5}
    load_dict('mydict3', 'ab', 'cd')

    class mycls: 
        u = 1
        bb = 2
        pack_params('u', 'bb')

    myclass = mycls()

    load_params('u', 'bb')

    load_params('device', 'D', 'G', 'G_optimizer', 'D_optimizer', header=False)

    load_hp('device', 'D')

    s = """
    parser.add_argument("--niters", type=int, default=10000)
    parser.add_argument("--batch_size", type=int, default=2000)
    parser.add_argument("--lr", type=float, default=3e-4)
    parser.add_argument("--weight_decay", type=float, default=0)
    parser.add_argument("--critic_weight_decay", type=float, default=0)
    parser.add_argument("--save", type=str, default="data/test_steinNS")
    parser.add_argument("--viz_freq", type=int, default=1000)
    parser.add_argument("--d_iters", type=int, default=5)
    parser.add_argument("--g_iters", type=int, default=1)
    parser.add_argument("--l2", type=float, default=10.0)
    """

    arg2hp(s)

    ss = """
    niters = _.('niters', 10000)
    batch_size = _.('batch_size', 2000)
    lr = _.('lr', 3e-4)
    weight_decay = _.('weight_decay', 0)
    critic_weight_decay = _.('critic_weight_decay', 0)
    save = _.('save', "data/test_steinNS")
    viz_freq = _.('viz_freq', 1000)
    d_iters = _.('d_iters', 5)
    g_iters = _.('g_iters', 1)
    l2 = _.('l2', 10.0)
    """

    hp2arg(ss)

    load_hp2hp(ss)

    hp2colab(ss)


    s = """
            niters = args.niters
            batch_size = args.batch_size
            lr = args.lr
            weight_decay = args.weight_decay
            critic_weight_decay = args.critic_weight_decay
            save = args.save
            viz_freq = args.viz_freq
            d_iters = args.d_iters
            g_iters = args.g_iters
            l2 = args.l2
            r = args.r
            sd = args.sd
            n_comp = args.n_comp
            z_dim = args.z_dim
            lr_D = args.lr_D
            out_dim = args.out_dim
            hid_dim = args.hid_dim
            model = args.model
            dim = args.dim
            G_path = args.G_path
            D_path = args.D_path
            use_spectrum = args.use_spectrum
            #endregion

            #region unpack the params
            niters = args.niters
            batch_size = args.batch_size
            lr = args.lr
            weight_decay = args.weight_decay
            critic_weight_decay = args.critic_weight_decay
            save = args.save
            viz_freq = args.viz_freq
            d_iters = args.d_iters
            g_iters = args.g_iters
            l2 = args.l2
            r = args.r
            sd = args.sd
            n_comp = args.n_comp
            z_dim = args.z_dim
            lr_D = args.lr_D
            out_dim = args.out_dim
            hid_dim = args.hid_dim
            model = args.model
            dim = args.dim
            clip_D = args.clip_D
            clip_value = args.clip_value
            loss_A = args.loss_A
            mmd_ratio_in = args.mmd_ratio_in
            mmd_two_sample = args.mmd_two_sample
            mmd_beta = args.mmd_beta
            G_loss = args.G_loss
    """
    get_uniq(s)


    s = """
        # problem setup
        parser.add_argument('--model', type=str, default='mb', choices=['mb', 'dw', 'gaussian'], help='which trajectories we are using for the datasets')
        parser.add_argument('--dim', type=int, default=2, help='the dimension of the dataset')
        parser.add_argument('--gen_thres_eng', type=float, default=100.0, help='the energy ratio for generating the initial data')

        # GAN
        parser.add_argument('--clip_D', type=str2bool, default=False, help='whether to clip the parameter for the discriminator')
        parser.add_argument('--clip_value', type=float, default=.1, help='the bounds for the clipping parameter of the discriminator')
        parser.add_argument('--use_spectrum', type=str2bool, default=False, help='whether to use spectrum normalization in the discriminator to force the lipschitz constant')
        parser.add_argument('--disc_zero', type=str2bool, default=True, help='whether to penalize the l2 penalty towards zero; otherwise penalize the norm to one')
        parser.add_argument('--l2', type=float, default=10.0, help='the coefficient of l2 penality in the loss of generator')
        parser.add_argument('--d_iters', type=int, default=5, help='the number of iterations for discriminator every round')
        parser.add_argument('--g_iters', type=int, default=1, help='the number of iterations for generators every round')

        # MMD
        parser.add_argument('--mmd_ratio_in', type=str2bool, default=False, help='whethe to put the partition function inside when computing the mmd')
        parser.add_argument('--mmd_two_sample', type=str2bool, default=False, help='whether to use two independent groups of samples to estimate the mmd')
        parser.add_argument('--mmd_beta', type=float, default=1.0, help='the parameter of gaussian kernel: std of the gaussian kernel is sigma = 1 / sqrt( 2 * beta )')

        # network
        parser.add_argument('--hid_dim', type=int, default=100, help='the dimension for the hidden layer in the neural network')

        # training 
        parser.add_argument('--loss_A', type=str2bool, default=True, help='whether to use loss type A: i.e. the 1st formula for the loss; otherwise, use the 2nd formula for the loss')
        parser.add_argument('--G_loss', type=str, default='GAN', choices=['GAN', 'MMD', 'GAN+MMD'], help='the type of loss for the generator: 1. GAN --- use the GAN formula for training; 2. MMD -- use the MMD for the generator (i.e. not training the discriminator); 3. GAN+MMD --- combine the both loss functions')
        parser.add_argument('--niters', type=int, default=10000, help='the number of iterations for training the neural networks')
        parser.add_argument('--batch_size', type=int, default=2000, help='the batch size for training the network')
        parser.add_argument('--lr', type=float, default=3e-4, help='the learning for the generator')
        parser.add_argument('--lr_D', type=float, default=1e-4, help='the learning rate of discriminator')

        # utils 
        parser.add_argument('--viz_freq', type=int, default=1000, help='the frequency of generating the visualization data')
        parser.add_argument('--log_freq', type=int, default=1000, help='the frequency of logging during the training')
        parser.add_argument('--G_path', type=str, default='', help='if given, load the generator from the G-path')
        parser.add_argument('--D_path', type=str, default='', help='if given, load the discriminator from the D-path')
    """

    arg2colab(s)
