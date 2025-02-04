from pymongo import MongoClient
from datetime import datetime, timedelta
from colors import Colors
from reports import generate_excel
import time
import sys

class MongoDatabase:
    def __init__(self, uri, database, collection):
        try:
            # Conexão
            client = MongoClient(uri, serverSelectionTimeoutMS=5000)
            self.client = client

            # Esse comando gera uma exceção se não conseguir se conectar
            client.server_info()
            print(f"{Colors.GREEN}Host ok!{Colors.RESET} {uri}")

            # Conexão com o database
            db = client[database]
            self.database = db

            # Conexão com a collection
            collection = db[collection]
            self.collection = collection
            time.sleep(1)

            # Tenta realizar uma consulta simples para garantir que a coleção está funcionando
            document = collection.find_one()
            if document:
                print(f"{Colors.GREEN}Database ok!{Colors.RESET} {db.name}")
                time.sleep(1)
                print(f"{Colors.GREEN}Collection ok!{Colors.RESET} {collection.name}")
                time.sleep(1)
                print(f"{Colors.GREEN}Conexão estabelecida!{Colors.RESET}")
                time.sleep(1)
            else:
                time.sleep(1)
                raise ValueError("Nenhum documento encontrado na coleção. Cancelando operação! Valide a tabela inserida e tente novamente!")

        except ConnectionError as e:
            print(f"{Colors.RED}Erro ao conectar ao MongoDB:{Colors.RESET}", str(e))
            time.sleep(1)
            sys.exit()

        except Exception as e:
            print(f"{Colors.RED}Erro:{Colors.RESET}", f"{Colors.RED}{str(e)}{Colors.RESET}")
            time.sleep(1)
            sys.exit()





    def init (self):

        print(f"\nO que você deseja encontrar?")
        print(f"1 - {Colors.GREEN}Dado especifíco, por meio de um indíce.{Colors.RESET}")
        print(f"2 - {Colors.GREEN}Todos os dados em um espaço de datas.{Colors.RESET}")
        print(f"3 - {Colors.GREEN}Quantidade de itens nessa tabela.{Colors.RESET}\n")

        metodos = { 1: "busca_dado_especifico", 2: "busca_todos_dados_data_especifica", 3: "quantidade_dados" }

        op = int(input("Digite a opção desejada: "))

        option = metodos[op]
        metodo = getattr(self, option, None)

        if option == "busca_dado_especifico":
            indice = input("\nDigite o indíce: ")
            valor = input("\nDigite o valor a ser encontrado: ")

            print(f"\n{Colors.YELLOW}Fazendo a busca... Aguarde um instante{Colors.RESET}\n")
            document = metodo(indice, valor)

            print(f"{Colors.BLUE}Documento encontrado: {Colors.RESET}", document, "\n")

            print("Deseja extrair relatório?")
            print(f"{Colors.GREEN}1 - Sim{Colors.RESET}")
            print(f"{Colors.RED}2 - Não{Colors.RESET}\n")
            
            extract = input("Digite aqui: ")

            if extract == "1":
                self.extract_reports([document])
            else:
                print('\nOperação finalizada!')






    def busca_dado_especifico(self, index, value):
        document = self.collection.find_one({
            index: value
        })
        if document:
            return document
        else:
            return None
        

    def busca_todos_dados_data_especifica(self):
        return "escolha 2"


    def quantidade_dados(self):
        return "escolha 3"
    
    def extract_reports(self, documents):
        print(f"\n{Colors.GREEN}Gerando a planilha EXCEL!{Colors.RESET}\n")
        generate_excel(documents)