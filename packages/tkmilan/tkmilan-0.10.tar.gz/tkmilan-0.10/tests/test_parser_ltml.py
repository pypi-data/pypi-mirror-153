import unittest
import logging

from textwrap import dedent

from tkmilan import model
from tkmilan import parser


logger = logging.getLogger(__name__)


class Test_LTML(unittest.TestCase):
    # # For copy-paste under "result"
    # print('')
    # print('golden = [')
    # for cmd in result:
    #     print(f'    {cmd},')
    # print(']')
    # print('')
    def test_simple(self):
        html_string = 'Text<a>Link</a>More Text<br/>Line Break above<a href="clean">Clean Link</a>S1<span>S2</span>S3'
        golden = [
            model.TextElementInline(text='Text'),
            model.TextElementInline(text='Link', tag='a', tags=['a::0']),
            model.TextElementInline(text='More Text'),
            model.TextElement_br(),
            model.TextElementInline(text='Line Break above'),
            model.TextElementInline(text='Clean Link', tag='a', tags=['a-clean', 'a::1']),
            model.TextElementInline(text='S1'),
            model.TextElementInline(text='S2', tag='span', tags=['span::0']),
            model.TextElementInline(text='S3'),
        ]

        result = parser.parse_LTML(html_string)
        self.assertListEqual(result, golden)

    def test_data(self):
        html_string = dedent('''<span data-one="1" data-two="2">Text</span>''')
        golden = [
            model.TextElementInline(text='Text', tag='span', tags=['span::0'], data={
                'one': '1',
                'two': '2',
            }),
        ]

        result = parser.parse_LTML(html_string)
        self.assertListEqual(result, golden)

    def test_newlines(self):
        html_string = 'Some Text\nLine Break above'
        with self.assertWarns(Warning):
            golden = [
                model.TextElementInline(text='Some Text\nLine Break above'),
            ]

            result = parser.parse_LTML(html_string)
        self.assertListEqual(result, golden)

    def test_br(self):
        html_string = dedent('''Text<br/>Text''')
        golden = [
            model.TextElementInline(text='Text'),
            model.TextElement_br(),
            model.TextElementInline(text='Text'),
        ]
        result = parser.parse_LTML(html_string)

        self.assertListEqual(result, golden)


if __name__ == '__main__':
    import sys
    logs_lvl = logging.DEBUG if '-v' in sys.argv else logging.INFO
    logging.basicConfig(level=logs_lvl, format='%(levelname)5.5s:%(funcName)s: %(message)s', stream=sys.stderr)
    unittest.main()
