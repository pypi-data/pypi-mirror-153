import argparse
import datetime
import os

import dateutil.tz
from rich import print


def parse_args():
    desc = "get the lastest news for twitter userID"
    parser = argparse.ArgumentParser(description=desc)
    arg_lists = []

    def add_argument_group(name):
        arg = parser.add_argument_group(name)
        arg_lists.append(arg)
        return arg

    # twitter arg
    twitter_arg = add_argument_group("twitter")
    twitter_arg.add_argument("twitter", type=str, help="twitter userID")
    args = parser.parse_known_args()

    return args


def catch_twitter(topic):
    import twint

    c = twint.Config()
    c.Limit = 1
    c.Username = topic
    c.Store_json = True
    c.Output = "custom_out.json"
    twint.run.Search(c)


def format_tweet(this_day, last_day):
    # this_day < day <= last_day
    import json

    # Opening JSON file
    f = open("custom_out.json", "r")

    tweets = []
    for line in f:
        tweets.append(json.loads(line))

    f.close()
    os.remove("custom_out.json")

    def get_code(urls):
        count = 1
        code_list = []
        for url in urls:
            if "github" in url:
                if count == 1:
                    code = "[code]({})".format(url)
                else:
                    code = "[code{}]({})".format(count, url)
                code_list.append(code)
                count += 1
        return ",".join(code_list)

    def get_paper(urls):
        count = 1
        code_list = []
        for url in urls:
            if "arxiv" in url:
                if count == 1:
                    code = "[paper]({})".format(url)
                else:
                    code = "[paper{}]({})".format(count, url)
                code_list.append(code)
                count += 1
        return ",".join(code_list)

    def get_date(iso_str):
        year, month, day = list(map(int, iso_str.split("-")))
        return datetime.date(year, month, day)

    count = 1
    lines = []
    for twitter in tweets:
        if get_date(twitter["date"]) <= get_date(this_day) and get_date(
            twitter["date"]
        ) > get_date(last_day):
            twitter_link = "[tweet]({})".format(twitter["link"])
            code = get_code(twitter["urls"])
            paper = get_paper(twitter["urls"])
            line = "{}. ".format(count) + " ".join(
                (
                    "[italic green4]{}[/italic green4]".format(twitter["tweet"]),
                    code,
                    paper,
                    twitter_link,
                    twitter["date"],
                )
            )
            lines.append(line)
            count += 1

    return "\n".join(lines[::-1])


def twitter_skim(topic):
    # open the corresponding html to dump the paper

    now = datetime.datetime.now(dateutil.tz.tzlocal())
    year, week, day = now.isocalendar()
    now.strftime("%Y_%m_%d_%H_%M_%S")

    # get the date of one week ago
    this_day = datetime.date.today()
    last_day = datetime.date.today() - datetime.timedelta(days=7)

    # get the format
    this_day = this_day.isoformat()
    last_day = last_day.isoformat()

    # get the twitter
    catch_twitter(topic)
    out = format_tweet(this_day, last_day)

    return out


def main():
    global args
    args = parse_args()

    twitter_id = args[0].twitter
    twitter_news = twitter_skim(twitter_id)

    print()
    print(twitter_news)


if __name__ == "__main__":
    # Usage I:
    # python twtr_skim.py elonmusk

    main()
