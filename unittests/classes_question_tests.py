import unittest
from unittest.mock import patch, Mock
from unittest import TestCase

from classes.question import Question as Question
from classes.answer import Answer as Answer
from classes.database import Database as Database
from classes.utils import Utils

class Test(TestCase):
    @classmethod
    def setUpClass(self):
        self.qt = Question()

    @patch.object(Question, '_edit')
    @patch.object(Question, '_insert')
    @patch.object(Utils, 'validate_not_empty')
    def test_validate_question_post(self, mock_validate_not_empty, mock__insert, mock__edit):
        mock__edit.return_value = 1;
        mock_validate_not_empty.return_value = True
        res = self.qt.validate_question_post('title', 'desc', 1, 'tag', 2)
        self.assertTrue(res)
        mock__insert.assert_not_called()

    @patch.object(Question, '_edit')
    @patch.object(Question, '_insert')
    @patch.object(Utils, 'validate_not_empty')
    def test_validate_question_post_2(self, mock_validate_not_empty, mock__insert, mock__edit):
        mock__insert.return_value = 1;
        mock_validate_not_empty.return_value = True
        res = self.qt.validate_question_post('title', 'desc', 1, 'tag', 0)
        self.assertTrue(res)
        mock__edit.assert_not_called()

    @patch.object(Question, '_edit')
    @patch.object(Question, '_insert')
    @patch.object(Utils, 'validate_not_empty')
    def test_validate_question_post_3(self, mock_validate_not_empty, mock__insert, mock__edit):
        mock_validate_not_empty.return_value = True
        res = self.qt.validate_question_post('title', 'desc', 0, 'tag', 1)
        self.assertFalse(res)
        mock__edit.assert_not_called()
        mock__insert.assert_not_called()

    @patch.object(Question, '_edit')
    @patch.object(Question, '_insert')
    @patch.object(Utils, 'validate_not_empty')
    def test_validate_question_post_4(self, mock_validate_not_empty, mock__insert, mock__edit):
        mock_validate_not_empty.return_value = False
        res = self.qt.validate_question_post('title', 'desc', 1, 'tag', 2)
        self.assertFalse(res)
        mock__edit.assert_not_called()
        mock__insert.assert_not_called()

    @patch.object(Question, 'get_by_id')
    @patch.object(Answer, 'remove_by_question_id')
    @patch.object(Question, '_delete')
    def test_remove(self, mock__delete, mock_remove_by_question_id, mock_get_by_id):
        mock_get_by_id.return_value = {'iduser': 15}
        res = self.qt.remove(1, 15)
        self.assertTrue(res)
        mock_remove_by_question_id.assert_called_once_with(1)
        mock__delete.assert_called_once_with(1, 15)

    @patch.object(Question, 'get_by_id')
    @patch.object(Answer, 'remove_by_question_id')
    @patch.object(Question, '_delete')
    def test_remove_2(self, mock__delete, mock_remove_by_question_id, mock_get_by_id):
        mock_get_by_id.return_value = {'iduser': 18}
        res = self.qt.remove(1, 15)
        self.assertFalse(res)
        mock_remove_by_question_id.assert_not_called()
        mock__delete.assert_not_called()
