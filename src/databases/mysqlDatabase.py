import mysql.connector
from datetime import datetime
from utils.colors import Colors
from utils.reports import generate_excel
import time

class MysqlDatabase:
    def __init__(self, host, user, password, database, table):
        # Conectar ao banco de dados
        try:
            connection = None
            connection = mysql.connector.connect(
                host=host,      # Endereço do servidor MySQL
                user=user,    # Usuário do banco de dados
                password=password,  # Senha do usuário
                database=database   # Nome do banco de dados
            )
            self.connection = connection

            if connection.is_connected():
                time.sleep(1)

                cursor = self.connection.cursor()
                cursor.execute(f"SELECT * FROM {table}")

                documents = cursor.fetchall()
                if documents:
                    print(f"{Colors.BLUE}Conexão estabelecida com Mysql!{Colors.RESET}")
                    self.table = table
                    time.sleep(1)
                    self.value = True
                else:
                    time.sleep(1)
                    raise ValueError("Nenhum documento encontrado na coleção. Cancelando operação! Valide o database e a tabela inserida e tente novamente!")

            else:
                time.sleep(1)
                raise ValueError("Erro de conexão. Cancelando operação! Valide o database, user e password. Após isso, tente novamente!")

        except mysql.connector.Error as err:
            print(f"{Colors.RED}Erro ao conectar:{Colors.RESET} {err}\n")
            time.sleep(1)
            self.value = None

            if connection:
                if connection.is_connected():
                    print(f"{Colors.YELLOW}Conexão aberta.{Colors.RESET}")
                    time.sleep(1)
                    connection.close()
                else:
                    print(f"{Colors.YELLOW}Conexão fechada.{Colors.RESET}")
            
            print(f"{Colors.YELLOW}Conexão encerrada.{Colors.RESET}")
        
        except Exception as e:
            print(f"{Colors.RED}Erro:{Colors.RESET}", f"{Colors.RED}{str(e)}{Colors.RESET}")
            time.sleep(1)
            self.value = None

            if connection:
                if connection.is_connected():
                    print(f"{Colors.YELLOW}Conexão aberta.{Colors.RESET}")
                    time.sleep(1)
                    connection.close()
                else:
                    print(f"{Colors.YELLOW}Conexão fechada.{Colors.RESET}")
            
            print(f"{Colors.YELLOW}Conexão encerrada.{Colors.RESET}")

    def start(self):

        start = True
        while start:
            print(f"{Colors.BLUE}\nO que você deseja encontrar?{Colors.RESET}")
            print(f"1 - Dado especifíco, por meio de um indíce de uma tabela.")
            print(f"2 - Todos os dados em um espaço de datas.")
            print(f"3 - Quantidade de itens nessa tabela.")
            print(f"4 - Retornar ao menu principal.\n")

            metodos = { 1: "busca_dado_especifico", 2: "busca_todos_dados_data_especifica", 3: "quantidade_dados", 4: "sair" }
            op = int(input("Digite a opção desejada: "))
            option = metodos[op]
            metodo = getattr(self, option, None)

            if op != 3 and op != 4:
                print(f"\n{Colors.YELLOW}**Necessário que a data de criação dos dados exista e esteja como CREATED_AT para que seja feita a busca e a conversão de forma correta**{Colors.RESET}\n")

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
                        self.extract_reports(document)
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
                documents = metodo(date_start, date_end) # Usando o def busca_todos_dados_data_especifica(tabela, start, end)

                #documents = list(documents)
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
                    print(f"{Colors.BLUE}Encontrado um total de {Colors.RESET} {total} documentos\n")
                else:
                    print(f"{Colors.YELLOW}Nenhum documento encontrado!{Colors.RESET}")

            if option == "sair":
                print(f"\n{Colors.YELLOW}Retornando ao menu principal{Colors.RESET}\n")
                start = False
                self.connection.close()

    def busca_dado_especifico(self, index, value):
        try:

            cursor = self.connection.cursor()

            cursor.execute(f"SELECT * FROM {self.table} WHERE {index} = '{value}'")

            # Obter os nomes das colunas
            colunas = [desc[0] for desc in cursor.description]

            # Criar um array para armazenar os resultados como JSON | Aqui ela já retorna encapsulado em um array
            document = [dict(zip(colunas, row)) for row in cursor.fetchall()]
            if document:
                return document
            else:
                return None

        except Exception as e:
            print(f"{Colors.RED}Erro ao buscar dado especifíco: {Colors.RESET}", e)
            return None

    def busca_todos_dados_data_especifica(self, start, end):
        try:

            cursor = self.connection.cursor()

            # Query SQL equivalente ao MongoDB
            query = f"SELECT * FROM {self.table} WHERE created_at BETWEEN %s AND %s"

            # Executar query com parâmetros
            cursor.execute(query, (start, end))

            # Obter os nomes das colunas
            colunas = [desc[0] for desc in cursor.description]

            # Criar um array para armazenar os resultados como JSON | Aqui ela já retorna encapsulado em um array
            documents = [dict(zip(colunas, row)) for row in cursor.fetchall()]

            if documents:
                return documents
            else:
                return None
        except Exception as e:
            print(f"{Colors.RED}Erro ao busca todos os dados de uma data especifica: {Colors.RESET}", e, "\n")
            return None

    def quantidade_dados(self):
        try:

            cursor = self.connection.cursor()

            cursor.execute(f"SELECT COUNT(*) FROM {self.table}")

            # Obter o resultado
            documents = cursor.fetchone()[0]  # A contagem está na primeira posição da tupla
            if documents:
                return documents
            else:
                return None
        except Exception as e:
            print(f"{Colors.RED}Erro ao buscar quantidade total: {Colors.RESET}", e)
            return None
    
    def extract_reports(self, documents):
        print(f"\n{Colors.GREEN}Gerando a planilha EXCEL!{Colors.RESET}\n")
        generate_excel(documents)