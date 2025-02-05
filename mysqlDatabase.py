import mysql.connector
from datetime import datetime
from colors import Colors
from reports import generate_excel
import time

class MysqlDatabase:
    def __init__(self, host, user, password, database):
        # Conectar ao banco de dados
        try:
            connection = mysql.connector.connect(
                host=host,      # Endereço do servidor MySQL
                user=user,    # Usuário do banco de dados
                password=password,  # Senha do usuário
                database=database   # Nome do banco de dados
            )
            self.connection = connection

            if connection.is_connected():
                time.sleep(1)
                print(f"{Colors.BLUE}Conexão estabelecida com Mysql!{Colors.RESET}")
                self.value = True

            else:
                time.sleep(1)
                raise ValueError("Erro de conexão. Cancelando operação! Valide o database, user e password. Após isso, tente novamente!")

        except mysql.connector.Error as err:
            print(f"{Colors.RED}Erro ao conectar:{Colors.RESET} {err}\n")
            connection.close()
            self.value = False
            print(f"{Colors.YELLOW}Conexão encerrada.{Colors.RESET}")

    def start(self):
        
        print(f"{Colors.BLUE}\nO que você deseja encontrar?{Colors.RESET}")
        print(f"1 - Dado especifíco, por meio de um indíce de uma tabela.")
        print(f"2 - Todos os dados em um espaço de datas.")
        print(f"3 - Quantidade de itens nessa tabela.\n")

        print(f"{Colors.YELLOW}**Necessário que a data de criação dos dados esteja como CREATED_AT para que seja feita a conversão de forma correta**{Colors.RESET}\n")

        metodos = { 1: "busca_dado_especifico", 2: "busca_todos_dados_data_especifica", 3: "quantidade_dados" }
        op = int(input("Digite a opção desejada: "))
        option = metodos[op]
        metodo = getattr(self, option, None)

        if option == "busca_dado_especifico": # busca_dado_especifico
            tabela = input("\nDigite a tabela: ")
            indice = input("\nDigite o indíce: ")
            valor = input("\nDigite o valor a ser encontrado: ")

            print(f"\n{Colors.YELLOW}Fazendo a busca... Aguarde um instante{Colors.RESET}\n")
            document = metodo(tabela, indice, valor) # Usando o def busca_dado_especifico(self, index, value)

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
            tabela = input("\nDigite a tabela: ")
            start = input("\nDigite a data inicial (Ex: YYYY-MM-DD): ")
            end = input("\nDigite a data final (Ex: YYYY-MM-DD): ")

            # Converter para datetime
            date_start = datetime.strptime(start, "%Y-%m-%d")
            date_end = datetime.strptime(end, "%Y-%m-%d")

            print(f"\n{Colors.YELLOW}Fazendo a busca... Aguarde um instante{Colors.RESET}\n")
            documents = metodo(tabela, date_start, date_end) # Usando o def busca_todos_dados_data_especifica(tabela, start, end)

            if documents:
                print(f"{Colors.BLUE}Documento encontrado: {Colors.RESET}", documents, "\n")

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
            tabela = input("\nDigite a tabela: ")

            print(f"\n{Colors.YELLOW}Fazendo a busca... Aguarde um instante{Colors.RESET}\n")
            total = metodo(tabela)

            if total:
                print(f"{Colors.BLUE}Encontrado um total de {Colors.RESET} {total} documentos\n")
            else:
                print(f"{Colors.YELLOW}Nenhum documento encontrado!{Colors.RESET}")

    def busca_dado_especifico(self, tabela, index, value):

        cursor = self.connection.cursor()

        cursor.execute(f"SELECT * FROM {tabela} WHERE {index} = '{value}'")

        # Obter os nomes das colunas
        colunas = [desc[0] for desc in cursor.description]

        # Criar um array para armazenar os resultados como JSON | Aqui ela já retorna encapsulado em um array
        document = [dict(zip(colunas, row)) for row in cursor.fetchall()]
        if document:
            return document
        else:
            return None

    def busca_todos_dados_data_especifica(self, tabela, start, end):

        cursor = self.connection.cursor()

        # Query SQL equivalente ao MongoDB
        query = f"SELECT * FROM {tabela} WHERE created_at BETWEEN %s AND %s"

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

    def quantidade_dados(self, tabela):

        cursor = self.connection.cursor()

        cursor.execute(f"SELECT COUNT(*) FROM {tabela}")

        # Obter o resultado
        documents = cursor.fetchone()[0]  # A contagem está na primeira posição da tupla
        if documents:
            return documents
        else:
            return None
    
    def extract_reports(self, documents):
        print(f"\n{Colors.GREEN}Gerando a planilha EXCEL!{Colors.RESET}\n")
        generate_excel(documents)