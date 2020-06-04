from abc import ABC, abstractmethod
from time import sleep
from typing import Dict, List, Type

from bs4 import BeautifulSoup

import requests

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


class SearchEngine:

    """Base class for Search Engine"""
    headers = {'User-Agent': "Mozilla/5.0 (X11; Linux x86_64)"}


class YandexSearchEngine(SearchEngine):

    url = 'https://yandex.com/search/'
    search_id = 'search-result'
    key = 'text'
    elements = {'tag': 'li', 'name': 'serp-item', 'xpath': '//li//h2'}
    title = None
    link = {'tag': 'a'}
    __next = "//span[contains(@class, 'pager__item')]/following-sibling::a"
    next_url = {'xpath': __next}


class GoogleSearchEngine(SearchEngine):

    url = 'https://google.com/search'
    search_id = 'search'
    key = 'q'
    elements = {'tag': 'div', 'name': 'r', 'xpath': "//div[@class='r']"}
    title = {'tag': 'h3'}
    link = {'tag': 'a'}
    __next = "//div[@id='foot']//td[@class][2]/following-sibling::td/a"
    next_url = {'xpath': __next}


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
            for item in items.find_all(search.element['tag'],
                                       class_=search.element['name']):
                # if search.title is not None:
                link = item.find(search.link['tag'],
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
        self.driver = self.__init_driver()

    def __init_driver(self):
        options = webdriver.ChromeOptions()
        # options.add_argument('--headless')
        options.add_argument('--start-maximized')
        return webdriver.Chrome(chrome_options=options)

    def get_urls(self,
                 keyword: str,
                 qty: int = 0,
                 search: Type[SearchEngine] = None) -> List[Dict[str, str]]:
        urls = []
        search = search or YandexSearchEngine
        url = f"{search.url}?{search.key}={keyword}"
        self.driver.get(url)

        while True:
            items = self.driver.find_element_by_id(search.search_id)
            for item in items.find_elements_by_xpath(search.elements['xpath']):

                link = item.find_element_by_tag_name(search.link['tag'])
                if search.title is not None:
                    title = item.find_element_by_tag_name(search.title['tag'])
                else:
                    title = link
                urls.append({'title': title.text,
                             'url': link.get_attribute('href')})

            if qty <= len(urls):
                break

            self.driver.find_element_by_xpath(search.next_url['xpath']).click()
            sleep(1)

        return urls if not qty else urls[:qty]

    def find_urls(self, url):
        self.driver.get(url)
        links = []
        try:
            items = self.driver.find_elements_by_tag_name('a')
            for item in items:
                link = {'title': item.text,
                        'url': item.get_attribute('href')}
                if link['url'] and link not in links:
                    links.append(link)
        except NoSuchElementException as e:
            print(url, e)
        finally:
            return links

    def close(self):
        self.driver.close()
