import unittest
from filum import helpers
from bs4 import BeautifulSoup

html = '<h1>Test</h1>'


class TestHelpers(unittest.TestCase):

    def test_bs4_to_md(self):
        soup = BeautifulSoup(html, 'html.parser')
        md = helpers.bs4_to_md(soup)
        self.assertEqual(md, '# Test\n\n')

    def test_html_to_md(self):
        md = helpers.html_to_md(html)
        self.assertEqual(md, '# Test\n\n')

    def test_root_url(self):
        self.assertEqual(helpers.root_url('https://reddit.com/r/python'), 'https://reddit.com')

    def test_iso_to_timestamp(self):
        self.assertEqual(helpers.iso_to_timestamp('2022-06-02T11:16:50'), 1654165010)

    def test_timestamp_to_iso(self):
        self.assertEqual(helpers.timestamp_to_iso(1654165010), '2022-06-02 11:16:50')


if __name__ == '__main__':
    unittest.main()
