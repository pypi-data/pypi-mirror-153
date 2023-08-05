import argparse
import datetime
import re
import urllib.request as libreq

import certifi
import dateutil.tz
from bs4 import BeautifulSoup


def parse_args():
    desc = "Get the abstract for an arxiv paper"
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

    # 1000 is a dummy variaable
    with libreq.urlopen('https://arxiv.org/abs/' + args.arxnum, cafile=certifi.where()) as url:
        html = url.read()
        soup = BeautifulSoup(html, 'html.parser')

    webpage = soup.get_text()

    # get the webpage
    webpage = soup.get_text()
    abstract = webpage.split('Abstract:')[1].split('Comments:')[0].strip()
    print(abstract)


if __name__ == '__main__':
    main()
