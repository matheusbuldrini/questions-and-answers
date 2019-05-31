import unittest
from unittest.mock import patch, Mock
from unittest import TestCase

from classes.answer import Answer as Answer
from classes.database import Database as Database
from classes.utils import Utils

class Test(TestCase):
    @classmethod
    def setUpClass(self):
        self.an = Answer()
        self.utils = Utils()

    @patch.object(Answer, '_delete')
    def test_remove(self, mock__delete):
        self.assertTrue(self.an.remove(1,1))

    @patch.object(Answer, '_edit')
    @patch.object(Utils, 'validate_not_empty')
    def test_validate_answer_edit(self, mock_validate_not_empty, mock__edit):
        mock__edit.return_value = 1;
        mock_validate_not_empty.return_value = True
        res = self.an.validate_answer_edit('desc', 1, 2)
        self.assertTrue(res)

    @patch.object(Answer, '_edit')
    @patch.object(Utils, 'validate_not_empty')
    def test_validate_answer_edit_2(self, mock_validate_not_empty, mock__edit):
        mock__edit.return_value = 1;
        mock_validate_not_empty.return_value = True
        res = self.an.validate_answer_edit('desc', 0, 2)
        self.assertFalse(res)

    @patch.object(Answer, '_edit')
    @patch.object(Utils, 'validate_not_empty')
    def test_validate_answer_edit_3(self, mock_validate_not_empty, mock__edit):
        mock__edit.return_value = 1;
        mock_validate_not_empty.return_value = False
        res = self.an.validate_answer_edit('desc', 1, 2)
        self.assertFalse(res)

    @patch.object(Answer, '_insert')
    @patch.object(Utils, 'validate_not_empty')
    def test_validate_answer_post(self, mock_validate_not_empty, mock__insert):
        mock__insert.return_value = 1;
        mock_validate_not_empty.return_value = True
        res = self.an.validate_answer_post('desc', 1, 2)
        self.assertTrue(res)

    @patch.object(Answer, '_insert')
    @patch.object(Utils, 'validate_not_empty')
    def test_validate_answer_post_2(self, mock_validate_not_empty, mock__insert):
        mock__insert.return_value = 1;
        mock_validate_not_empty.return_value = True
        res = self.an.validate_answer_post('desc', 0, 2)
        self.assertFalse(res)

    @patch.object(Answer, '_insert')
    @patch.object(Utils, 'validate_not_empty')
    def test_validate_answer_post_3(self, mock_validate_not_empty, mock__insert):
        mock__insert.return_value = 1;
        mock_validate_not_empty.return_value = False
        res = self.an.validate_answer_post('desc', 1, 2)
        self.assertFalse(res)

    @patch.object(Answer, '_insert_vote')
    def test_vote(self, mock__insert_vote):
        self.an.vote(1, 1, 1)
        mock__insert_vote.assert_called_once_with(1,1,1)
