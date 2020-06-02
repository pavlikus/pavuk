from abc import ABC, abstractmethod
from typing import Dict, List, Type

from bs4 import BeautifulSoup

import requests

from selenium import webdriver


class SearchEngine:

    """Base class for Search Engine"""
    headers = {'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.61 Safari/537.36',
               'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
               'Upgrade-Insecure-Requests': '1',
               'DNT': '1'}


class YandexSearchEngine(SearchEngine):

    url = 'https://yandex.com/search/'
    search_id = 'search-result'
    key = 'text'
    elements = {'type': 'li', 'name': 'serp-item', 'xpath': '//li//h2'}
    title = None
    link = {'type': 'a'}


class GoogleSearchEngine(SearchEngine):

    url = 'https://google.com/search'
    search_id = 'search'
    key = 'q'
    elements = {'type': 'div', 'name': 'r', 'xpath': "//div[@class='r']"}
    title = {'type': 'h3'}
    link = {'type': 'a'}


# TODO: Optimisation search element (XPath, ...)
class AbstractEngine(ABC):

    @abstractmethod
    def get_urls(self,
                 keyword: str,
                 search: Type[SearchEngine]) -> List[Dict[str, str]]:
        raise NotImplementedError

    @abstractmethod
    def find_urls(self):
        raise NotImplementedError

    @abstractmethod
    def close(self):
        raise NotImplementedError


class Requests(AbstractEngine):

    def get_urls(self,
                 keyword: str,
                 search: Type[SearchEngine] = None) -> List[Dict[str, str]]:
        urls = []
        search = search or YandexSearchEngine
        r = requests.Session()
        response = r.get(search.url,
                         params={search.key: keyword},
                         headers=search.headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'lxml')
            items = soup.find(id=search.search_id)
            import pdb
            pdb.set_trace()
            for item in items.find_all(search.element['type'],
                                       class_=search.element['name']):
                #if search.title is not None:
                link = item.find(search.link['type'],
                                 class_=search.link['name'])

                urls.append({'title': link.text,
                             'url': link['href']})
        return urls

    def find_urls(self, url):
        ...

    def close(self):
        ...


class Selenium(AbstractEngine):

    def __init__(self):
        self.driver = webdriver.Chrome()

    def get_urls(self,
                 keyword: str,
                 search: Type[SearchEngine] = None) -> List[Dict[str, str]]:

        urls = []
        search = search or YandexSearchEngine
        url = f"{search.url}?{search.key}={keyword}"
        self.driver.get(url)
        # import pdb
        #  pdb.set_trace()
        items = self.driver.find_element_by_id(search.search_id)
        for item in items.find_elements_by_xpath(search.elements['xpath']):

            link = item.find_element_by_tag_name(search.link['type'])
            if search.title is not None:
                title = item.find_element_by_tag_name(search.title['type'])
            else:
                title = link
            urls.append({'title': title.text,
                         'url': link.get_attribute('href')})
        return urls

    def find_urls(self, url):
        ...

    def close(self):
        self.driver.close()
