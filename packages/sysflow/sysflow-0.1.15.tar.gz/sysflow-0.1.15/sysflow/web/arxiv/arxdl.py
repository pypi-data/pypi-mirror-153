import argparse
import datetime
import re
import urllib.request as libreq

import certifi
import dateutil.tz
from bs4 import BeautifulSoup


def parse_args():
    desc = "download for an arxiv paper"
    parser = argparse.ArgumentParser(description=desc)
    arg_lists = []

    def add_argument_group(name):
        arg = parser.add_argument_group(name)
        arg_lists.append(arg)
        return arg

    # qunatum control
    arx_arg = add_argument_group('arxiv')
    arx_arg.add_argument('arxnum', type=str, help='arxiv number of papers')
    args = parser.parse_args()

    return args


def main():
    global args
    args = parse_args()


    import urllib.request
    import os 

    url = 'https://arxiv.org/e-print/' + args.arxnum
    fname = '{}.tar.gz'.format(args.arxnum)
    urllib.request.urlretrieve(url, fname)

    import tarfile

    tar = tarfile.open(fname, "r:gz")
    tar.extractall(path=args.arxnum)
    tar.close()
    os.remove(fname)

    url = 'https://arxiv.org/pdf/' + args.arxnum + '.pdf'
    fname = '{}/{}.pdf'.format(args.arxnum, args.arxnum)
    urllib.request.urlretrieve(url, fname)


if __name__ == '__main__':
    main()
