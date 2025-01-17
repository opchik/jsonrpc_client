import urllib
from django.test import TestCase
from unittest.mock import patch

from api_client.jsonrpc import JsonRpcClient


class TestJsonRpcClient(TestCase):
    def setUp(self):
        self.client = JsonRpcClient("http://localhost:8000/api")

    @patch('urllib.request.urlopen')
    def test_call_method_invalid(self, mock_urlopen):
        mock_urlopen.side_effect = RuntimeError("Connection refused")
        with self.assertRaises(RuntimeError):
            self.client.call_method("invalidMethod")
