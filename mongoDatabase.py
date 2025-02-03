from pymongo import MongoClient
from datetime import datetime, timedelta
import time

# Códigos ANSI para cores
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
GRAY = '\033[90m'
PINK = '\033[35m'
PURPLE = '\033[35m'  # Para roxo, utilizamos o magenta
GOLD = '\033[33m'
BLACK = '\033[30m'
RESET = '\033[0m'  # Reseta a cor para a cor padrão

class MongoDatabase:
    def __init__(self, uri, database, collection):

        try:

            client = MongoClient(uri, serverSelectionTimeoutMS=5000)
            self.client = client

            client.server_info()  # Esse comando gera uma exceção se não conseguir se conectar
            print(f"{GREEN}Url ok!{RESET}")
            time.sleep(1)

            db = client[database]
            self.database = db
            print(f"{GREEN}Database ok!{RESET} {db.name}")
            time.sleep(1)

            collection = db[collection]
            self.collection = collection
            print(f"{GREEN}Collection ok!{RESET} {collection.name}")
            time.sleep(1)

            # Tenta realizar uma consulta simples para garantir que a coleção está funcionando
            document = collection.find_one()
            if document:
                print(f"{GREEN}Conexão com o MongoDB bem-sucedida!{RESET}")
                time.sleep(1)
            else:
                print(f"{YELLOW}Nenhum documento encontrado na coleção.{RESET}")
                time.sleep(1)

        except ConnectionError as e:
            print(f"{RED}Erro ao conectar ao MongoDB:{RESET}", str(e))
            time.sleep(1)

        except Exception as e:
            print(f"{RED}Outro erro ocorreu:{RESET}", str(e))
            time.sleep(1)

    def busca_1(self):
        documents = self.collection.find()
        if documents:
            for document in documents:
                print(document.get('name', 'name invalid'))

    def busca_2(self):
        return "escolha 2"

    def busca_3(self):
        return "escolha 3"