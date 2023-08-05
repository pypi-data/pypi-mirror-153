import datetime
import os
import re
import time
import urllib.request as libreq
from os.path import expanduser

import certifi
import dateutil.tz
from bs4 import BeautifulSoup

import schedule


class Config():
    # listing all the topics
    topics = ['cs.LG', 'math.NA', 'math.OC', 'quant-ph']


def arxskim(topic):
    # open the corresponding html to dump the paper

    now = datetime.datetime.now(dateutil.tz.tzlocal())
    year, week, day = now.isocalendar()
    timestamp = now.strftime('%Y_%m_%d_%H_%M_%S')

    home = expanduser("~")
    folder = os.path.join(home, 'Downloads', 'arxiv_news',
                          str(year), '{:02d}'.format(week))
    os.makedirs(folder, exist_ok=True)
    text_file = open(os.path.join(folder, topic.replace(
        '.', '-') + '-' + timestamp + ".md"), "w")

    # 1000 is a dummy variaable
    with libreq.urlopen('https://arxiv.org/list/' + topic + '/pastweek?skip=0&show=1000', cafile=certifi.where()) as url:
        html = url.read()
        soup = BeautifulSoup(html, 'html.parser')

    # get the html source code
    # print(soup.prettify())

    # get the webpage
    webpage = soup.get_text()

    l_date = re.findall('\w+, \d+ \w+ \d+', webpage)
    text_file.write("### " + l_date[-1] + '-' + l_date[-5]+'\n')

    l_titles = []
    l_links = []
    l_authors = []

    for wd in webpage.split('Authors:'):
        if 'Subjects' in wd:
            l_authors.append(wd.split('Subjects')[0].replace(
                '\n', '').replace('Comments:', ',').replace('Authors:', ''))

    # delete the comments: 
    _webpage = re.sub('Comments:.*\n', '\n', webpage)

    l_titles = re.findall("Title:.+", _webpage)
    l_titles = [title.replace('Title:', '') for title in l_titles]

    l_links = re.findall('\[\d+\]\s+arXiv:\w+.\w+', _webpage)
    l_links = ["https://arxiv.org/pdf/" +
               link.split('arXiv:')[1] + '.pdf' for link in l_links]

    assert len(l_titles) == len(l_links) and len(l_titles) == len(l_authors)

    for (title, link, author) in zip(l_titles, l_links, l_authors):
        text_file.write(
            "- " + title + ', [pdf]({})'.format(link) + ', ' + author + '\n')

    text_file.close()


def job():
    config = Config()
    for topic in config.topics:
        arxskim(topic)


def main():
    schedule.every().saturday.at("12:00").do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == '__main__':
    main()
