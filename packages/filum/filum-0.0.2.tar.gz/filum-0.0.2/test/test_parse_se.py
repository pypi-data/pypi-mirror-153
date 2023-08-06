import pathlib
import unittest
from test.expected_parser_outputs import expected_output_se

from bs4 import BeautifulSoup
from filum.parsers.parse_se import parse_se

html_fp = pathlib.Path(__file__).parent.resolve() / 'test_se.html'

with open(html_fp) as f:
    html_se = f.read()

soup_se = BeautifulSoup(html_se, 'html5lib')


class TestParsers(unittest.TestCase):
    def test_parse_se_returns_correct_dict(self):
        expected = expected_output_se
        output = parse_se(
            soup_se,
            'https://stackoverflow.com/questions/72349922/tableau-not-recognizing-snowflake-odbc-drivers-on-mac',
            'se'
            )
        self.assertCountEqual(output, expected)


if __name__ == '__main__':
    unittest.main()
