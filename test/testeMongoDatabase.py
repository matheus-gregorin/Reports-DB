import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from src.databases.mongoDatabase import MongoDatabase
from utils.colors import Colors
from datetime import datetime

#  Comando:
#  python -m unittest testeMongoDatabase.py

# Criando a classe de teste
class TesteMongoDatabase(unittest.TestCase):

    def setUp(self):
        """Configuração antes de cada teste"""
        self.uri = "Uri"
        self.database = "Projeto_bot"
        self.collection = "items"
        self.mongodb = MongoDatabase(self.uri, self.database, self.collection)

    def teste_busca_especifica_retorna_objeto_item_existe(self):
        """Testa se a busca por um indice que existe volta o objeto"""
        index = "name_item"
        name = "Limão"
        data = self.mongodb.busca_dado_especifico(index, name)
        self.assertIsNotNone(data)
        print(f"{Colors.GREEN} ✔ Teste busca_especifica retorna o objeto correto! Retorno: {data.get("name_item", "")} {Colors.RESET}\n")
        self.mongodb.close()

    def teste_busca_especifica_retorna_vazio_item_nao_existe(self):
        """Testa se a busca por um indice que não existe volta None"""
        index = "name_item"
        name = "Abobora"
        data = self.mongodb.busca_dado_especifico(index, name)
        self.assertIsNone(data)
        print(f"{Colors.GREEN} ✔ Teste busca_especifica não retorna None! Retorno: {data} {Colors.RESET}\n")
        self.mongodb.close()

    def teste_busca_todos_dados_data_especifica_retorna_erro_data_formato_errado(self):
        """Retorna lista vazia pois os parametros estão no formato errado"""
        data_inicial = "02-03-2024"
        data_final = "02-04-2024"
        date_start = datetime.strptime(data_inicial, "%d-%m-%Y")
        date_end = datetime.strptime(data_final, "%d-%m-%Y")
        data = self.mongodb.busca_todos_dados_data_especifica(date_start, date_end)
        data = list(data)
        self.assertListEqual(data, [])
        print(f"{Colors.GREEN} ✔ Teste busca_todos_dados_data_especifica retorna lista vazia! Retorno: {data} {Colors.RESET}\n")
        self.mongodb.close()

    def teste_busca_todos_dados_data_especifica_retorna_lista_data_formato_correto(self):
        """Retorna lista pois os parametros estão no formato correto e existem"""
        data_inicial = "2024-06-12"
        data_final = "2024-06-18"
        date_start = datetime.strptime(data_inicial, "%Y-%m-%d")
        date_end = datetime.strptime(data_final, "%Y-%m-%d")
        data = self.mongodb.busca_todos_dados_data_especifica(date_start, date_end)
        data = list(data)
        self.assertIsNotNone(data)
        print(f"{Colors.GREEN} ✔ Teste busca_todos_dados_data_especifica retorna lista! Retorno: {data} {Colors.RESET}\n")
        self.mongodb.close()


# Executar os testes
if __name__ == '__main__':
    unittest.main()
