import unittest
from unittest.mock import patch, Mock
from unittest import TestCase

from classes.user import User as User
from classes.database import Database as Database
from classes.utils import Utils

class Test(TestCase):
    @classmethod
    def setUpClass(self):
        self.us = User()

    #escolhe as funcoes para simular (é possível simular várias funcoes)
    @patch.object(Database, 'query')
    def test__select_count_by_email(self, mock_query):

        #configura o valor qe a funcao simulada vai retornar
        mock_query.return_value = [{'COUNT': 4}]

        #chama a funcao que será testada (essa NAO é simulada)
        res = self.us._select_count_by_email('this-Mail-Is-Not-In-Database@mail.com')
        #compara o resultado recebido com o resultdo esperado
        self.assertEqual(res, 4)

    @patch.object(User, '_select_all_by_userid')
    def test_get_by_id(self, mock__select_all_by_userid):

        mock__select_all_by_userid.return_value = ['user1']

        res = self.us.get_by_id(12345)
        self.assertTrue(res)

    @patch.object(User, '_select_count_by_email')
    @patch.object(User, '_insert')
    @patch.object(Utils, 'validate_not_empty')
    def test_validate_register(self, mock_validate_not_empty, mock__insert, mock__select_count_by_email):
        mock_validate_not_empty.return_value = True
        mock__select_count_by_email.return_value = 0
        mock__insert.return_value = 1
        res = self.us.validate_register('full name', 'email', 'pass')
        self.assertTrue(res)

    @patch.object(User, '_select_count_by_email')
    @patch.object(User, '_insert')
    @patch.object(Utils, 'validate_not_empty')
    def test_validate_register_2(self, mock_validate_not_empty, mock__insert, mock__select_count_by_email):
        mock_validate_not_empty.return_value = False
        res = self.us.validate_register('', '', '')
        self.assertFalse(res)
        mock__select_count_by_email.assert_not_called()
        mock__insert.assert_not_called()

    @patch.object(User, '_select_count_by_email')
    @patch.object(User, '_insert')
    @patch.object(Utils, 'validate_not_empty')
    def test_validate_register_3(self, mock_validate_not_empty, mock__insert, mock__select_count_by_email):
        mock_validate_not_empty.return_value = True
        mock__select_count_by_email.return_value = 3
        res = self.us.validate_register('full name', 'email', 'pass')
        self.assertFalse(res)
        mock__insert.assert_not_called()

    @patch.object(User, '_select_count_by_email')
    @patch.object(User, '_insert')
    @patch.object(Utils, 'validate_not_empty')
    def test_validate_register_4(self, mock_validate_not_empty, mock__insert, mock__select_count_by_email):
        mock_validate_not_empty.return_value = True
        mock__select_count_by_email.return_value = 0
        mock__insert.return_value = 0
        res = self.us.validate_register('full name', 'email', 'pass')
        self.assertFalse(res)

    @patch.object(User, '_select_count_by_email_password')
    @patch.object(Utils, 'validate_not_empty')
    def test_validate_login(self, mock_validate_not_empty, mock__select_count_by_email_password):
        mock_validate_not_empty.return_value = True
        mock__select_count_by_email_password.return_value = 1
        res = self.us.validate_login('email', 'pass')
        self.assertTrue(res)

    @patch.object(User, '_select_count_by_email_password')
    @patch.object(Utils, 'validate_not_empty')
    def test_validate_login_2(self, mock_validate_not_empty, mock__select_count_by_email_password):
        mock_validate_not_empty.return_value = False
        res = self.us.validate_login('', '')
        self.assertFalse(res)
        mock__select_count_by_email_password.assert_not_called()

    @patch.object(User, '_select_count_by_email_password')
    @patch.object(Utils, 'validate_not_empty')
    def test_validate_login_3(self, mock_validate_not_empty, mock__select_count_by_email_password):
        mock_validate_not_empty.return_value = True
        mock__select_count_by_email_password.return_value = 0
        res = self.us.validate_login('email', 'pass')
        self.assertFalse(res)

    @patch.object(User, '_update_password')
    @patch.object(User, '_update_but_password')
    @patch.object(Utils, 'validate_not_empty')
    def test_validate_update(self, mock_validate_not_empty, mock__update_but_password, mock__update_password):
        mock_validate_not_empty.return_value = True
        res = self.us.validate_update('fullname', 'email', 'password', 'description', 8)
        self.assertTrue(res)
        mock__update_but_password.assert_called_once()
        mock__update_password.assert_called_once()

    @patch.object(User, '_update_password')
    @patch.object(User, '_update_but_password')
    @patch.object(Utils, 'validate_not_empty')
    def test_validate_update_2(self, mock_validate_not_empty, mock__update_but_password, mock__update_password):
        mock_validate_not_empty.return_value = True
        res = self.us.validate_update('fullname', 'email', '', 'description', 8)
        self.assertTrue(res)
        mock__update_but_password.assert_called_once()
        mock__update_password.assert_not_called()

    @patch.object(User, '_update_password')
    @patch.object(User, '_update_but_password')
    @patch.object(Utils, 'validate_not_empty')
    def test_validate_update_3(self, mock_validate_not_empty, mock__update_but_password, mock__update_password):
        mock_validate_not_empty.return_value = False
        res = self.us.validate_update('', '', '', '', '')
        self.assertFalse(res)
        mock__update_but_password.assert_not_called()
        mock__update_password.assert_not_called()
