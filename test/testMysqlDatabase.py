import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.databases.mysqlDatabase import MysqlDatabase
from utils.colors import Colors
from datetime import datetime

#  Comando:
#  python -m unittest testMysqlDatabase.py

# Criando a classe de teste
class TesteMysqlDatabase(unittest.TestCase):

    def setUp(self):
        """Configuração antes de cada teste"""
        self.host = "localhost"
        self.user = "root"
        self.password = ""
        self.database = ""
        self.table = ""
        self.mysql = MysqlDatabase(self.host, self.user, self.password, self.database, self.table)

    def teste_busca_especifica_retorna_objeto_item_existe(self):
        """Testa se a busca por um indice que existe volta o objeto"""
        index = "nome"
        name = "João Silva"
        data = self.mysql.busca_dado_especifico(index, name)
        self.assertIsNotNone(data)
        print(f"{Colors.GREEN} ✔ Teste busca_especifica retorna o objeto correto! Retorno: {data[0].get('nome', '')} {Colors.RESET}\n")
        self.mysql.close()

    def teste_busca_especifica_retorna_vazio_item_nao_existe(self):
        """Testa se a busca por um indice que não existe volta None"""
        index = "nome"
        name = "Daniel"
        data = self.mysql.busca_dado_especifico(index, name)
        self.assertIsNone(data)
        print(f"{Colors.GREEN} ✔ Teste busca_especifica retorna None! Retorno: {data} {Colors.RESET}\n")
        self.mysql.close()

    def teste_busca_todos_dados_data_especifica_retorna_erro_data_formato_errado(self):
        """Retorna None pois os parametros estão no formato errado"""
        data_inicial = "02-03-2024"
        data_final = "02-04-2024"
        date_start = datetime.strptime(data_inicial, "%d-%m-%Y")
        date_end = datetime.strptime(data_final, "%d-%m-%Y")
        data = self.mysql.busca_todos_dados_data_especifica(date_start, date_end)
        self.assertEqual(data, None)
        print(f"{Colors.GREEN} ✔ Teste busca_todos_dados_data_especifica retorna None! Retorno: {data} {Colors.RESET}\n")
        self.mysql.close()

    def teste_busca_todos_dados_data_especifica_retorna_lista_data_formato_correto(self):
        """Retorna lista pois os parametros estão no formato correto e existem"""
        data_inicial = "2025-02-15"
        data_final = "2025-02-18"
        date_start = datetime.strptime(data_inicial, "%Y-%m-%d")
        date_end = datetime.strptime(data_final, "%Y-%m-%d")
        data = self.mysql.busca_todos_dados_data_especifica(date_start, date_end)
        data = list(data)
        self.assertIsNotNone(data)
        print(f"{Colors.GREEN} ✔ Teste busca_todos_dados_data_especifica retorna lista! Retorno: {data} {Colors.RESET}\n")
        self.mysql.close()


# Executar os testes
if __name__ == '__main__':
    unittest.main()
