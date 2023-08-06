import re

url_pattern_reddit = re.compile(r'https:\/\/www.reddit.com\/r\/.+\/comments\/')
url_pattern_so = re.compile(r'https:\/\/stackoverflow.com\/((questions)|(q)|(a))')
url_pattern_se = re.compile(r'https:\/\/.+\.stackexchange.com\/((questions)|(q)|(a))')
url_pattern_hn = re.compile(r'https:\/\/news.ycombinator.com\/item')

# TODO: Add patterns for other SE sites such as Ask Ubuntu, Server Fault,
# Super User

url_patterns = [url_pattern_reddit, url_pattern_so,
                url_pattern_se, url_pattern_hn]

# Custom exceptions for input validation


class InvalidInputError(Exception):
    '''Exception for errors due to invalid user input'''


class InvalidUrl(InvalidInputError):
    '''Invalid URL'''
    def __init__(self):
        self.message = ('Please enter a URL prefixed with "https://".\n'
                        'Supported sites: Reddit, Hacker News, Stack Exchange')
        super().__init__(self.message)


class InvalidThreadId(InvalidInputError):
    '''Invalid thread ID'''
    def __init__(self):
        self.message = ('Please enter a valid thread ID (positive integer). '
                        'Run `filum all` to see a list of thread IDs.')
        super().__init__(self.message)


# Validation functions


def is_valid_url(arg: str) -> bool:
    for pattern in url_patterns:
        if pattern.match(arg):
            return True
    raise InvalidUrl


def is_valid_id(arg: int) -> bool:
    if type(arg) == int:
        if arg > 0:
            return True
    raise InvalidThreadId
