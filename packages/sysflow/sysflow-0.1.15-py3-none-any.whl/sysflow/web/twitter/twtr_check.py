import datetime
import os
import time
from os.path import expanduser

import dateutil.tz
import schedule


class Config:
    # listing all the topics
    ai_bot_topics = [
        "ak92501",
        "Deep__AI",
        "slashML",
        "arXiv_Daily",
        "Montreal_AI",
        "deep_rl",
        "MLSTjournal",
    ]
    prof_topics = [
        "svlevine",
        "ylecun",
        "ericjang11",
        "fchollet",
        "gabrielpeyre",
        "josh_tobin_",
    ]
    tips_topcs = ["DynamicWebPaige", "y0b1byte", "ykilcher"]
    topics = ai_bot_topics + prof_topics + tips_topcs


def catch_twitter(topic, this_day, last_day):
    import twint

    c = twint.Config()
    c.Limit = 1
    c.Username = topic
    c.Store_json = True
    c.Output = "custom_out.json"
    c.Since = last_day
    c.Until = this_day
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
                (twitter["tweet"], code, paper, twitter_link, twitter["date"])
            )
            lines.append(line)
            count += 1

    return "\n".join(lines)


def twitter_skim(topic):
    # open the corresponding html to dump the paper

    now = datetime.datetime.now(dateutil.tz.tzlocal())
    year, week, day = now.isocalendar()
    timestamp = now.strftime("%Y_%m_%d_%H_%M_%S")

    # get the date of one week ago
    this_day = datetime.date.today()
    last_day = datetime.date.today() - datetime.timedelta(days=7)

    # get the format
    this_day = this_day.isoformat()
    last_day = last_day.isoformat()

    home = expanduser("~")
    folder = os.path.join(home, "Downloads", "twitter_news", str(year), '{:02d}'.format(week))
    os.makedirs(folder, exist_ok=True)
    text_file = open(
        os.path.join(folder, topic.replace(".", "-") + "-" + timestamp + ".md"), "w"
    )

    # get the twitter
    catch_twitter(topic, this_day, last_day)
    out = format_tweet(this_day, last_day)

    text_file.write(out)
    text_file.close()


def job():
    config = Config()
    for topic in config.topics:
        try:
            twitter_skim(topic)
        except:
            pass


def main():
    schedule.every().sunday.at("23:38").do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)


if __name__ == "__main__":
    main()
