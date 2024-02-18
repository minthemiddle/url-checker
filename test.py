from click.testing import CliRunner
from resolve_urls import main
from resolve_urls import resolve_url
from unittest.mock import MagicMock, patch
from urllib.parse import urlparse
import io
import requests
import sys
import unittest

class TestResolveUrl(unittest.TestCase):
    def setUp(self):
        self.mock_response = MagicMock()
        self.mock_response.status_code = 200

    def test_main_no_input_file(self):
        runner = CliRunner()
        result = runner.invoke(main, ["-i", "", "-o", "output.csv"])
    
        self.assertNotEqual(result.exit_code, 0)
        self.assertIn("Error: Invalid value for '-i'", result.output)

    @patch('resolve_urls.requests.head')
    def test_url_resolved_same_base(self, mock_head):
        mock_head.return_value = self.mock_response
        mock_response_url = 'http://example.com'
        self.mock_response.url = mock_response_url

        result = resolve_url('http://example.com')

        self.assertEqual(result, ('http://example.com', 'http://example.com', 'http', 200, 0))

    @patch('resolve_urls.requests.head')
    def test_url_resolved_different_base(self, mock_head):
        mock_head.return_value = self.mock_response
        mock_response_url = 'http://changed-example.com'
        self.mock_response.url = mock_response_url

        result = resolve_url('http://example.com')

        self.assertEqual(result, ('http://example.com', 'http://changed-example.com', 'http', 200, 1))
        
    @patch('resolve_urls.requests.head')
    def test_url_resolved_same_base_with_www(self, mock_head):
        mock_head.return_value = self.mock_response
        mock_response_url = 'https://www.test.com'
        self.mock_response.url = mock_response_url
    
        result = resolve_url('https://test.com')
    
        self.assertEqual(result, ('https://test.com', 'https://www.test.com', 'https', 200, 0))

    @patch('resolve_urls.requests.head')
    def test_url_resolved_https(self, mock_head):
        mock_head.return_value = self.mock_response
        mock_response_url = 'https://secure-example.com'
        self.mock_response.url = mock_response_url

        result = resolve_url('https://secure-example.com')

        self.assertEqual(result, ('https://secure-example.com', 'https://secure-example.com', 'https', 200, 0))

    @patch('resolve_urls.requests.head')
    def test_url_resolution_failed(self, mock_head):
        mock_head.side_effect = requests.exceptions.RequestException("Failed to resolve URL")

        result = resolve_url('http://example.com')

        self.assertEqual(result, ('http://example.com', None, None, 'Failed to resolve URL', None))

if __name__ == '__main__':
    unittest.main()
