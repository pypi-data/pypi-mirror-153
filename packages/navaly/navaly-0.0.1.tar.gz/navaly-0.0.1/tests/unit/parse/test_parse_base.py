from io import BytesIO, FileIO, IOBase
import unittest
import os

from naval.fetch.fetch_base import Fetch_Base
from naval.parse.parse_base import Parse_Base
from naval.fetch.master_fetch import Master_Fetch

from .common_tests import Common_Tests


class Test_Fetch_Base(unittest.TestCase, Common_Tests):
    @classmethod
    def setUpClass(cls):
        cls.source = os.path.join("samples", "sample_file.txt")
        cls.source2 = os.path.join("samples", "sample_file.file")

        cls.fetch_obj = Master_Fetch.get_fetch_object(cls.source)
        cls.fetch_obj2 = Master_Fetch.get_fetch_object(BytesIO())

        cls.parse_obj = Parse_Base(cls.fetch_obj)
        cls.parse_obj2 = Parse_Base(cls.fetch_obj2)

    def test_text_to_file(self):
        with self.assertRaises(NotImplementedError):
            self.parse_obj.text_to_file()

    def test_html_to_file(self):
        with self.assertRaises(NotImplementedError):
            self.parse_obj.html_to_file()

    def test_get_text(self):
        with self.assertRaises(NotImplementedError):
            self.parse_obj.get_text()

    def test_get_html(self):
        with self.assertRaises(NotImplementedError):
            self.parse_obj.get_html()


if __name__ == '__main__':
    unittest.main()
