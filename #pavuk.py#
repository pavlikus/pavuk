#!/usr/bin/env python

import argparse

import formater

from scraper import engine
from scraper import scraper


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('keywords',
                        nargs='+',
                        help="search phrase")
    parser.add_argument('-s', '--search',
                        choices=('google', 'yandex'),
                        help="search engine")
    parser.add_argument('-o', '--output',
                        choices=('csv', 'json'),
                        help="output format file, default this console")

    args = parser.parse_args()

    scr = scraper.Scraper()
    if args.search == 'google':
        result = scr.get_urls(' '.join(args.keywords),
                              search=engine.GoogleSearchEngine)
    else:
        result = scr.get_urls(' '.join(args.keywords))
    scr.close()

    if args.output == 'csv':
        formater.to_csv(result)
    elif args.output == 'json':
        formater.to_json(result)
    else:
        for r in result:
            print(f"{r['title']} --- {r['url']}")
        print(f"Total links: {len(result)}")
