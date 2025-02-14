from pymongo import MongoClient
from datetime import datetime
from colors import Colors
from reports import generate_excel
import time

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
                print(f"{Colors.GREEN}Conexão estabelecida com MongoDb!{Colors.RESET}")
                time.sleep(1)
                self.value = True
            else:
                time.sleep(1)
                raise ValueError("Nenhum documento encontrado na coleção. Cancelando operação! Valide o database e a tabela inserida e tente novamente!")

        except ConnectionError as e:
            print(f"{Colors.RED}Erro ao conectar ao MongoDB:{Colors.RESET}", f"{Colors.RED}{str(e)}{Colors.RESET}")
            time.sleep(1)
            self.value = None

        except Exception as e:
            print(f"{Colors.RED}Erro:{Colors.RESET}", f"{Colors.RED}{str(e)}{Colors.RESET}")
            time.sleep(1)
            self.value = None

    def start (self):

        start = True
        while start:
            print(f"{Colors.GREEN}\nO que você deseja encontrar?{Colors.RESET}")
            print(f"1 - Dado especifíco, por meio de um indíce.")
            print(f"2 - Todos os dados em um espaço de datas.")
            print(f"3 - Quantidade de itens nessa tabela.")
            print(f"4 - Retornar ao menu principal.\n")

            print(f"{Colors.YELLOW}**Necessário que a data de criação dos dados esteja como CREATED_AT para que seja feita a conversão de forma correta**{Colors.RESET}\n")

            metodos = { 1: "busca_dado_especifico", 2: "busca_todos_dados_data_especifica", 3: "quantidade_dados", 4: "sair" }
            op = int(input("Digite a opção desejada: "))
            option = metodos[op]
            metodo = getattr(self, option, None)

            if option == "busca_dado_especifico": # busca_dado_especifico
                indice = input("\nDigite o indíce: ")
                valor = input("\nDigite o valor a ser encontrado: ")

                print(f"\n{Colors.YELLOW}Fazendo a busca... Aguarde um instante{Colors.RESET}\n")
                document = metodo(indice, valor) # Usando o def busca_dado_especifico(self, index, value)

                if document:
                    print(f"{Colors.BLUE}Documento encontrado: {Colors.RESET}", document, "\n")

                    print("Deseja extrair relatório?")
                    print(f"{Colors.GREEN}1 - Sim{Colors.RESET}")
                    print(f"{Colors.RED}2 - Não{Colors.RESET}\n")
                    extract = input("Digite aqui: ")

                    if extract == "1":
                        self.extract_reports([document])
                    else:
                        print('\nOperação finalizada!')

                else:
                    print(f"{Colors.YELLOW}Nenhum documento encontrado!{Colors.RESET}")


            if option == "busca_todos_dados_data_especifica": # busca_todos_dados_data_especifica
                start = input("\nDigite a data inicial (Ex: YYYY-MM-DD): ")
                end = input("\nDigite a data final (Ex: YYYY-MM-DD): ")

                # Converter para datetime
                date_start = datetime.strptime(start, "%Y-%m-%d")
                date_end = datetime.strptime(end, "%Y-%m-%d")

                print(f"\n{Colors.YELLOW}Fazendo a busca... Aguarde um instante{Colors.RESET}\n")
                documents = metodo(date_start, date_end) # Usando o def busca_todos_dados_data_especifica(start, end)

                documents = list(documents)
                print(f"{Colors.BLUE}Documentos encontrados:{Colors.RESET}", documents, "\n")

                if documents:
                    print("\nDeseja extrair relatório?")
                    print(f"{Colors.GREEN}1 - Sim{Colors.RESET}")
                    print(f"{Colors.RED}2 - Não{Colors.RESET}\n")
                    extract = input("Digite aqui: ")

                    if extract == "1":
                        self.extract_reports(documents)
                    else:
                        print('\nOperação finalizada!')

                else:
                    print(f"{Colors.YELLOW}Nenhum documento encontrado!{Colors.RESET}")

            if option == "quantidade_dados": # quantidade_dados

                print(f"\n{Colors.YELLOW}Fazendo a busca... Aguarde um instante{Colors.RESET}\n")
                total = metodo()

                if total:
                    print(f"{Colors.BLUE}Encontrado um total de {Colors.RESET} {documents} documentos\n")
                else:
                    print(f"{Colors.YELLOW}Nenhum documento encontrado!{Colors.RESET}")

            if option == "sair":
                print(f"\n{Colors.YELLOW}Retornando ao menu principal{Colors.RESET}\n")
                start = False

    def busca_dado_especifico(self, index, value):
        try:
            document = self.collection.find_one({
                index: value
            })
            if document:
                return document
            else:
                return None
        except Exception as e:
            print(f"{Colors.RED}Erro ao buscar dado especifíco: {Colors.RESET}", e)
            return None

    def busca_todos_dados_data_especifica(self, start, end):
        try:
            documents = self.collection.find({
                "created_at": {
                    "$gte": start,
                    "$lte": end
                }
            })
            if documents:
                return documents
            else:
                return None
        except Exception as e:
            print(f"{Colors.RED}Erro ao busca todos os dados de uma data especifica: {Colors.RESET}", e, "\n")
            return None

    def quantidade_dados(self):
        try:
            documents = self.collection.count_documents({})
            if documents:
                return documents
            else:
                return None
        except Exception as e:
            print(f"{Colors.RED}Erro ao buscar quantidade total: {Colors.RESET}", e)
            return None
    
    def extract_reports(self, documents):
        print(f"\n{Colors.GREEN}Gerando a planilha EXCEL!{Colors.RESET}\n")
        generate_excel(documents, True)