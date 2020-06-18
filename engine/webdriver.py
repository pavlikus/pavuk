from abc import ABC, abstractmethod
from time import sleep
from typing import Dict, List, Type

from bs4 import BeautifulSoup

from engine.search import Search

import requests

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException


class AbstractEngine(ABC):

    @abstractmethod
    def get_urls(self,
                 url: str,
                 keyword: str,
                 search: Type[Search]) -> List[Dict[str, str]]:
        raise NotImplementedError

    @abstractmethod
    def find_urls(self):
        raise NotImplementedError

    @abstractmethod
    def close(self):
        raise NotImplementedError


class Requests(AbstractEngine):

    def __init__(self):
        self.s = requests.Session()

    def get_urls(self,
                 url: str,
                 keyword: str,
                 qty: int = 0,
                 search: Type[Search] = None) -> List[Dict[str, str]]:
        urls = []
        url = search.url

        while True:
            response = self.s.get(url,
                                  params={search.key: keyword},
                                  headers=search.headers)
            if response.status_code == 200:
                soup = BeautifulSoup(response.text, 'lxml')
                items = soup.find(id=search.search_id)
                for item in items.find_all(search.element['tag'],
                                           class_=search.element['name']):

                    link = item.find(search.link['tag'])
                    if search.title is not None:
                        title = item.find(search.title['tag'])
                    else:
                        title = link

                        urls.append({'title': title.text,
                                     'url': link['href']})
                # if qty <= len(urls):
                #     break

                sleep(1)

        return urls

    def find_urls(self, url):
        ...

    def close(self):
        del self.s


class Selenium(AbstractEngine):

    def __init__(self):
        self.driver = self.__init_driver()

    def __init_driver(self):
        options = webdriver.ChromeOptions()
        # options.add_argument('--headless')
        options.add_argument('--start-maximized')
        return webdriver.Chrome(chrome_options=options)

    def __has_button_next(self, xpath):
        try:
            n = self.driver.find_element_by_xpath(xpath)
            n.click()
            sleep(1)
            return True
        except NoSuchElementException as e:
            print(e)

    def get_urls(self,
                 url: str,
                 keyword: str,
                 qty: int = 0,
                 search: Type[Search] = None) -> List[Dict[str, str]]:
        urls = []
        self.driver.get(url)

        while True:
            items = self.driver.find_element_by_id(search.search_id)
            for item in items.find_elements_by_xpath(search.elements['xpath']):

                link = item.find_element_by_tag_name(search.link['tag'])
                title = item.find_element_by_tag_name(search.title['tag'])

                url = {'title': title.text,
                       'url': link.get_attribute('href')}

                if url not in urls:
                    urls.append(url)

            next_url = self.__has_button_next(search.next_url['xpath'])
            if qty <= len(urls) or not next_url:
                break

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
