from collections import UserDict
from unittest import TestCase
from unittest.mock import patch

from util import http


class TestHTTP(TestCase):
    @patch("urllib.request.build_opener")
    def test_post_mapping_is_form_encoded(self, build_opener):
        http.open("https://example.com/", post_data=UserDict({"q": "hello world"}))
        request = build_opener.return_value.open.call_args.args[0]
        self.assertEqual(request.data, b"q=hello+world")

    @patch("urllib.request.build_opener")
    def test_post_bytes_are_preserved(self, build_opener):
        http.open("https://example.com/", post_data=b"raw body")
        request = build_opener.return_value.open.call_args.args[0]
        self.assertEqual(request.data, b"raw body")
