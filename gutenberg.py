#!/usr/bin/env python3
import argparse

import feedparser
import requests


def parse_it(url):
    feed = feedparser.parse(url)
    #    print(feed['items'])
    for item in feed['items']:
        if item['description'] == "Language: English":
            print("The title of the new book is:\n%s" % (item['title']))
            #            print(item['link'])
            s = item['link']
            re = requests.get("http://www.gutenberg.org/files/" + s[32:] + "/" + s[32:] + "-h/" + s[32:] + "-h.htm")
            if re.status_code == requests.codes.ok:
                print("The url of the html is:\n%s\n" % (re.url))
            else:
                print("Inaccessible")


def parse_args():
    parser = argparse.ArgumentParser(
        description="Give a url if you want to. For now default is http://www.gutenberg.org/cache/epub/feeds/today.rss")
    parser.add_argument("-u", "--url", dest="url",
                        help="Rss feed url",
                        default="http://www.gutenberg.org/cache/epub/feeds/today.rss", action='store')
    args = parser.parse_args()
    #    print(args)
    return args


def main():
    args = parse_args()
    parse_it(args.url)


if __name__ == "__main__":
    main()

