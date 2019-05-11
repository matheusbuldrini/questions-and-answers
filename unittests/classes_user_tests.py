import unittest
from unittest.mock import patch, Mock
from unittest import TestCase

from classes.user import User as User
from classes.database import Database as Database

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
