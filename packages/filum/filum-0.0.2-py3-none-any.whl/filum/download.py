import traceback

import requests
from bs4 import BeautifulSoup

from filum.parsers.parse_hn import parse_hn
from filum.parsers.parse_reddit import parse_reddit
from filum.parsers.parse_se import parse_se


class Download:
    def __init__(self, url):
        self.url = url

    def process_url(self):
        # Reddit's unofficial API - add a '.json' suffix to any url
        if 'reddit.com' in self.url:
            self.url += '.json'
            self.site = 'reddit'
        elif 'news.ycombinator.com' in self.url:
            self.site = 'hn'
        elif 'stackexchange.com' in self.url or \
             'stackoverflow.com' in self.url:
            self.site = 'se'

        return self

    def get_response(self):
        headers = {
            'user-agent': 'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:100.0) Gecko/20100101 Firefox/100.0',
            'dnt': '1',
            'accept-encoding': 'gzip, deflate, br',
            'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8',
            'accept-language': 'en-US,en;q=0.5'
        }
        self.r = requests.get(self.url, headers=headers)
        return self

    def parse_html(self, raw):
        self.soup = BeautifulSoup(raw, 'html5lib')
        return self

    def prepare_response(self):
        if self.site == 'reddit':
            self.r = self.r.json()
        else:
            self.r = self.parse_html(self.r.text)
        return self

    def get_thread(self):
        if self.site == 'reddit':
            return parse_reddit(self)
        elif self.site == 'hn':
            return parse_hn(self)
        elif self.site == 'se':
            return parse_se(self.soup, self.url, self.site)

    def run(self):
        return self.process_url().get_response().prepare_response().get_thread()


hn_url_root = 'https://news.ycombinator.com/item?id=27336584'
hn_url_comment = 'https://news.ycombinator.com/item?id=31451536'
se_url_root = 'https://stats.stackexchange.com/questions/6/the-two-cultures-statistics-vs-machine-learning'
se_url_answer = 'https://stackoverflow.com/questions/15340582/python-extract-pattern-matches/15340666#15340666'
reddit_url_root = 'https://www.reddit.com/r/boardgames/comments/utkslk/tiny_epic_which_one_would_you_recommend/'


def main():
    Download(hn_url_root).process_url() \
                         .get_response() \
                         .prepare_response() \
                         .get_thread()


if __name__ == '__main__':
    try:
        main()
    except Exception:
        traceback.print_exc()
