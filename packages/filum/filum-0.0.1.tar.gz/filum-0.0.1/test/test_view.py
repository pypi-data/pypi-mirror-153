import unittest
from filum.view import RichView

view = RichView()


class TestView(unittest.TestCase):
    def test_stringify(self):
        query_result = {
            'num': 1,
            'title': 'Some title',
            'posted_timestamp': 1622404036,
            'saved_timestamp': 1654005888.148201,
            'score': 0,
            'source': 'hn',
            'tags': None
            }
        result_values = query_result.values()

        stringified = ('1', 'Some title', '1622404036', '1654005888.148201', '0', 'hn', 'None')

        self.assertEqual(view.stringify(result_values), stringified)


if __name__ == '__main__':
    unittest.main()
