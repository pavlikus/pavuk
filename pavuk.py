#!/usr/bin/env python

import argparse
from typing import Dict, List

import formater

import scraper


def get_args():
    """Parse command line arguments"""

    parser = argparse.ArgumentParser(description="Your Web Scraper")
    parser.add_argument('keywords',
                        nargs='+',
                        help="search phrase")
    parser.add_argument('-s', '--search',
                        choices=('google', 'yandex'),
                        help="search engine")
    parser.add_argument('-q', '--qty',
                        type=int,
                        help="Quantity links in output result, max 100")
    parser.add_argument('-o', '--output',
                        choices=('csv', 'json'),
                        help="output format file, default this console")
    parser.add_argument('-r', '--recursive',
                        action='store_true',
                        help="Find all links on main result")

    args = parser.parse_args()

    # Check QTY links
    if args.qty and 0 >= args.qty > 100:
        parser.error("Quantity links must be from 1 to 100")

    return args


def get_result(keywords: str,
               search: str,
               qty: int = 0) -> List[Dict[str, str]]:
    """Get main seach result"""

    scr = scraper.Scraper()
    qty = qty or 0
    result = scr.get_urls(' '.join(keywords), qty=qty, search=search)
    scr.close()

    return result


def find_links(urls: List[str]) -> List[Dict[str, str]]:
    """Find all links recursive"""

    scr = scraper.Scraper()
    links = []
    for url in urls:
        links.extend(scr.find_urls(url))
    scr.close()

    return links


def writer(result: List[Dict[str, str]],
           output: str = None,
           filename: str = None) -> None:
    """Write result to output"""

    outputs = {'csv': formater.to_csv,
               'json': formater.to_json}

    filename = filename or f"output.{output}"
    if output is not None:
        outputs[output](result, filename=filename)
    else:
        for r in result:
            print(f"{r['title']} --- {r['url']}")
        print(f"Total links: {len(result)}")


def main():

    args = get_args()
    result = get_result(args.keywords, args.search, args.qty)
    links = []

    # TODO: add multiproccesing
    if args.recursive:
        links = find_links([r['url'] for r in result])

    writer(result, args.output)
    if links:
        writer(links, args.output, filename=f"links.{args.output}")


if __name__ == '__main__':
    main()
