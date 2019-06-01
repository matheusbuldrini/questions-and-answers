import unittest
from unittest.mock import patch, Mock
from unittest import TestCase

from classes.voteanswer import VoteAnswer as VoteAnswer
from classes.database import Database as Database
from classes.utils import Utils

class Test(TestCase):
    @classmethod
    def setUpClass(self):
        self.va = VoteAnswer()

    @patch.object(VoteAnswer, '_select_vote')
    @patch.object(VoteAnswer, '_insert')
    def test_validate_vote(self, mock__insert, mock__select_vote):
        mock__select_vote.return_value = 0;
        mock__insert.return_value = 1
        res = self.va.validate_vote(1,1,1)
        self.assertTrue(res)

    @patch.object(VoteAnswer, '_select_vote')
    @patch.object(VoteAnswer, '_insert')
    def test_validate_vote_2(self, mock__insert, mock__select_vote):
        mock__select_vote.return_value = 0;
        mock__insert.return_value = 0
        res = self.va.validate_vote(1,1,1)
        self.assertFalse(res)

    @patch.object(VoteAnswer, '_select_vote')
    @patch.object(VoteAnswer, '_insert')
    def test_validate_vote_3(self, mock__insert, mock__select_vote):
        mock__select_vote.return_value = 1;
        mock__insert.return_value = 1
        res = self.va.validate_vote(1,1,1)
        self.assertFalse(res)
        mock__insert.assert_not_called()
