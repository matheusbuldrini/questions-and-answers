import unittest
from unittest.mock import patch
from unittest import TestCase
import sys
sys.path.append('')
import classes.utils as Utils

class Test(TestCase):
    @classmethod
    def setUpClass(self):
        self.ut = Utils.Utils()

    def test_md5(self):
        md5 = self.ut.md5("12345")
        self.assertEqual(md5, "827ccb0eea8a706c4c34a16891f84e7b")
