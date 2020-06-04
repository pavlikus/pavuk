
class Search:

    """Base class for Search Engine"""
    headers = {'User-Agent': "Mozilla/5.0 (X11; Linux x86_64)"}


class YandexSearch(Search):

    url = 'https://yandex.com/search/'
    search_id = 'search-result'
    key = 'text'
    elements = {'tag': 'li', 'name': 'serp-item', 'xpath': '//li//h2'}
    title = None
    link = {'tag': 'a'}
    __next = "//span[contains(@class, 'pager__item')]/following-sibling::a"
    next_url = {'xpath': __next}


class GoogleSearch(Search):

    url = 'https://google.com/search'
    search_id = 'search'
    key = 'q'
    elements = {'tag': 'div', 'name': 'r', 'xpath': "//div[@class='r']"}
    title = {'tag': 'h3'}
    link = {'tag': 'a'}
    __next = "//div[@id='foot']//td[@class][2]/following-sibling::td/a"
    next_url = {'xpath': __next}
