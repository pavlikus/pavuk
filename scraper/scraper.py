from typing import Dict, List

from .engine import Selenium


class Scraper:

    def __init__(self, engine=None):
        engine_ = engine or Selenium
        self.engine = engine_()  # Create engine object

    def get_urls(self, *args, **kwargs) -> List[Dict[str, str]]:
        return self.engine.get_urls(*args, **kwargs)

    def close(self, *args, **kwargs):
        self.engine.close(*args, **kwargs)
