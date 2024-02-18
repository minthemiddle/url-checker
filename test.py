from click.testing import CliRunner
from resolve_urls import main, resolve_url
from unittest.mock import patch, MagicMock
import unittest
import requests

class TestResolveUrl(unittest.TestCase):
    def setUp(self):
        self.mock_response = MagicMock()
        self.mock_response.status_code = 200
        self.mock_response.url = 'http://example.com'

    def test_main_no_input_file(self):
        runner = CliRunner()
        result = runner.invoke(main, ["-i", "", "-o", "output.csv"])
        self.assertNotEqual(result.exit_code, 0)
        self.assertIn("Error: Invalid value for '-i'", result.output)

    def test_malformed_url(self):
        result = resolve_url('- https://example.com')
        self.assertEqual(result, ('- https://example.com', None, None, 'malformed_url', None))

    @patch('resolve_urls.requests.get')
    def test_url_resolved_same_base(self, mock_get):
        mock_get.return_value = self.mock_response
        result = resolve_url('http://example.com')
        self.assertEqual(result, ('http://example.com', 'http://example.com', 'http', 200, 0))

    @patch('resolve_urls.requests.get')
    def test_url_resolved_different_base(self, mock_get):
        self.mock_response.url = 'http://changed-example.com'
        mock_get.return_value = self.mock_response
        result = resolve_url('http://example.com')
        self.assertEqual(result, ('http://example.com', 'http://changed-example.com', 'http', 200, 1))

    @patch('resolve_urls.requests.get')
    def test_url_resolved_same_base_with_www(self, mock_get):
        self.mock_response.url = 'https://www.test.com'
        mock_get.return_value = self.mock_response
        result = resolve_url('https://test.com')
        self.assertEqual(result, ('https://test.com', 'https://www.test.com', 'https', 200, 0))

    @patch('resolve_urls.requests.get')
    def test_url_resolved_https(self, mock_get):
        self.mock_response.url = 'https://secure-example.com'
        mock_get.return_value = self.mock_response
        result = resolve_url('https://secure-example.com')
        self.assertEqual(result, ('https://secure-example.com', 'https://secure-example.com', 'https', 200, 0))

    @patch('resolve_urls.requests.get')
    def test_url_resolution_failed(self, mock_get):
        mock_get.side_effect = requests.exceptions.RequestException("Failed to resolve URL")
        result = resolve_url('http://example.com')
        self.assertEqual(result, ('http://example.com', None, None, 'failed', 0))

@patch('resolve_urls.requests.get')
def test_url_redirect(self, mock_get):
    # Set up the mock to simulate a redirect
    mock_response = MagicMock()
    mock_response.url = 'https://goodtools.substack.com/?utm_source=substack&utm_medium=email'
    mock_response.status_code = 200
    mock_response.history = [MagicMock(status_code=302, headers={'Location': 'https://goodtools.substack.com/?utm_source=substack&utm_medium=email'})]
    mock_get.return_value = mock_response

    # Call resolve_url with a URL that redirects
    result = resolve_url('https://substack.com/redirect/9fbbf243-d928-4401-ad01-61017c801ee9')

    # Check that the resolved_url is the redirected URL and base_url_changed is 0
    self.assertEqual(result, ('https://substack.com/redirect/9fbbf243-d928-4401-ad01-61017c801ee9', 'https://goodtools.substack.com/?utm_source=substack&utm_medium=email', 'https', 200, 0))

if __name__ == '__main__':
    unittest.main()
