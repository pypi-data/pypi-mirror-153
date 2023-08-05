import datetime
import os
import time
import urllib.request as libreq
from os.path import expanduser

import certifi
import dateutil.tz
import requests
import schedule
from bs4 import BeautifulSoup
from sysflow.web.arxiv.arxb import extract_from_text


def catch_scirate():
    url = "https://scirate.com/?range=7"
    page = requests.get(url)
    soup = BeautifulSoup(page.content, "html.parser")

    count = soup.find_all(class_="btn btn-default count")
    paper = soup.find_all(class_="paper-download btn btn-success")

    rate = [int(i.get_text()) for i in count]
    arxiv = [i["href"] for i in paper]
    arxid = [extract_from_text(i)[0] for i in arxiv]

    return rate, arxid


def arx2md(arxnum, rate, count):
    # 1000 is a dummy variaable
    with libreq.urlopen(
        "https://arxiv.org/abs/" + arxnum, cafile=certifi.where()
    ) as url:
        html = url.read()
        soup = BeautifulSoup(html, "html.parser")

    webpage = soup.get_text()

    # get the webpage
    webpage = soup.get_text()
    title = webpage.split("Title:")[1].split("Authors:")[0].strip()
    author = webpage.split("Authors:")[1].split("Download")[0].strip()
    link_title = "{}. {}, {}, [pdf](https://arxiv.org/pdf/{}.pdf), rate: {}\n".format(
        count, title, author, arxnum, rate
    )
    return link_title


def scirate_skim():
    # open the corresponding html to dump the paper

    now = datetime.datetime.now(dateutil.tz.tzlocal())
    year, week, day = now.isocalendar()
    timestamp = now.strftime("%Y_%m_%d_%H_%M_%S")

    home = expanduser("~")
    folder = os.path.join(home, "Downloads", "scirate_news", str(year), str(week))
    os.makedirs(folder, exist_ok=True)
    text_file = open(os.path.join(folder, "weekly" + "-" + timestamp + ".md"), "w")

    # get the twitter
    rates, arxids = catch_scirate()
    lines = []
    for count, (rate, arxid) in enumerate(zip(rates, arxids)):
        line = arx2md(arxid, rate, count + 1)
        lines.append(line)

    lines = "".join(lines)

    text_file.write(lines)
    text_file.close()


def job():
    scirate_skim()


def main():
    schedule.every().saturday.at("12:00").do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
