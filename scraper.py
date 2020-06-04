from typing import Dict, List

from engine import search as sc
from engine import webdriver as wb


class Scraper:

    def __init__(self, webdriver=None):
        webdriver_ = webdriver or wb.Selenium
        self.webdriver = webdriver_()  # Create webdriver object

    def get_urls(self,
                 keyword: str,
                 search: str,
                 *args,
                 **kwargs) -> List[Dict[str, str]]:

        searchers = {'google': sc.GoogleSearch,
                     'yandex': sc.YandexSearch}
        if search is not None:
            search = searchers[search]
        else:
            search = searchers['yandex']

        url = f"{search.url}?{search.key}={keyword}"

        return self.webdriver.get_urls(*args,
                                       url=url,
                                       keyword=keyword,
                                       search=search,
                                       **kwargs)

    def find_urls(self, *args, **kwargs) -> List[Dict[str, str]]:
        return self.webdriver.find_urls(*args, **kwargs)

    def close(self, *args, **kwargs):
        self.webdriver.close(*args, **kwargs)
