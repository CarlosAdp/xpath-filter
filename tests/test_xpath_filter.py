from unittest import mock

from pathlib import Path
import unittest
import lxml.html

from xpath_filter import xpath_filter


class XPathFilterTest(unittest.TestCase):
    HTML_CONTENT = '<div class="article"><p>Content</p></div>'
    YAML_CONTENT = '''
        article:
            xpath: //div[@class="article"]
            matches: first
            elements:
                content: ./p/text()
    '''

    def test_xpath_filter_with_html_element(self):
        html = lxml.html.fromstring(self.HTML_CONTENT)
        xpaths = {
            'article': {
                'xpath': '//div[@class="article"]',
                'matches': 'first',
                'elements': {
                    'content': './p/text()'
                }
            }
        }
        expected_output = {'article': {'content': 'Content'}}
        result = xpath_filter(html, xpaths)
        self.assertEqual(result, expected_output)

    @mock.patch.object(Path, 'read_text')
    @mock.patch.object(Path, 'is_file')
    def test_xpath_filter_with_html_file(self, is_file, read_text):
        is_file: mock.MagicMock = is_file
        is_file.configure_mock()
        read_text.return_value = self.HTML_CONTENT

        xpaths = {
            'article': {
                'xpath': '//div[@class="article"]',
                'matches': 'first',
                'elements': {
                    'content': './p/text()'
                }
            }
        }
        expected_output = {'article': {'content': 'Content'}}
        result = xpath_filter('test_html.html', xpaths)
        self.assertEqual(result, expected_output)

    @mock.patch.object(Path, 'read_text')
    @mock.patch.object(Path, 'is_file')
    def test_xpath_filter_with_yaml_file(self, is_file, read_text):
        is_file.return_value = True
        read_text.return_value = self.YAML_CONTENT

        expected_output = {'article': {'content': 'Content'}}
        result = xpath_filter(lxml.html.fromstring(
            self.HTML_CONTENT), 'test_xpaths.yml')
        self.assertEqual(result, expected_output)

    @mock.patch.object(Path, 'read_text')
    @mock.patch.object(Path, 'is_file')
    def test_xpath_filter_with_invalid_yaml_file(self, is_file, read_text):
        is_file.return_value = True
        read_text.return_value = '{"format": '

        with self.assertRaises(ValueError):
            xpath_filter(lxml.html.fromstring(
                self.HTML_CONTENT), 'test_xpaths.yml')

    @mock.patch.object(Path, 'is_file')
    def test_xpath_filter_with_inexistent_file(self, is_file):
        is_file.return_value = False

        with self.assertRaises(ValueError):
            xpath_filter(lxml.html.fromstring(
                self.HTML_CONTENT), 'test_xpaths.yml')


if __name__ == '__main__':
    unittest.main()
