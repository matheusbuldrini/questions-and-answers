import unittest
from unittest.mock import patch, Mock
from unittest import TestCase

from user import User as User

class Test(TestCase):
    @classmethod
    def setUpClass(self):
        self.us = User()

    @patch.object(User, '_select_all_by_userid')
    def test_get_by_id(self, mock__select_all_by_userid):

        mock__select_all_by_userid.return_value = ['user1']

        res = self.us.get_by_id(12345)
        self.assertTrue(res)
