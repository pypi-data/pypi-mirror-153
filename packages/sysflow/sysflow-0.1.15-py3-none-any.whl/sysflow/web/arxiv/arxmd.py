import argparse
import datetime
import re
import urllib.request as libreq

import certifi
import dateutil.tz
from bs4 import BeautifulSoup


def parse_args():
    desc = "Get the markdown format for an arxiv paper"
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
    title = webpage.split('Title:')[1].split('Authors:')[0].strip()
    author = webpage.split('Authors:')[1].split('Download')[0].strip()
    link_title = '[{}](https://arxiv.org/pdf/{}.pdf)'.format(title, args.arxnum)
    year = '**Arxiv 20{}**'.format(args.arxnum[:2])
    info = link_title + '\n> ' + author + '\n> ' + '\n> ' + year
    print(info) 

if __name__ == '__main__':
    main()
