import pathlib
import unittest

from bs4 import BeautifulSoup
from filum.download import Download

html_fp = pathlib.Path(__file__).parent.resolve() / 'test_se.html'

with open(html_fp) as f:
    html_se = f.read()


class TestDownload(unittest.TestCase):
    def test_parse_html_creates_soup_from_html(self):
        d = Download('test')
        d.parse_html(html_se)
        self.assertIsInstance(d.soup, BeautifulSoup)


if __name__ == '__main__':
    unittest.main()
