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
                    print(f"{Colors.BLUE}Connection established with Mysql!{Colors.RESET}")
                    self.table = table
                    time.sleep(1)
                    self.value = True
                else:
                    time.sleep(1)
                    raise ValueError("No documents found in the collection. Canceling operation! Validate the database and inserted table and try again!")

            else:
                time.sleep(1)
                raise ValueError("Connection error. Canceling operation! Validate the database, username and password. After that, try again!")

        except mysql.connector.Error as err:
            print(f"{Colors.RED}Error connecting:{Colors.RESET} {err}\n")
            time.sleep(1)
            self.value = None

            if connection:
                if connection.is_connected():
                    print(f"{Colors.YELLOW}Connection open.{Colors.RESET}")
                    time.sleep(1)
                    connection.close()
                else:
                    print(f"{Colors.YELLOW}Connection close.{Colors.RESET}")
            
            print(f"{Colors.YELLOW}Connection closed.{Colors.RESET}")
        
        except Exception as e:
            print(f"{Colors.RED}Error:{Colors.RESET}", f"{Colors.RED}{str(e)}{Colors.RESET}")
            time.sleep(1)
            self.value = None

            if connection:
                if connection.is_connected():
                    print(f"{Colors.YELLOW}Connection open.{Colors.RESET}")
                    time.sleep(1)
                    connection.close()
                else:
                    print(f"{Colors.YELLOW}Connection closed.{Colors.RESET}")
            
            print(f"{Colors.YELLOW}Connection closed.{Colors.RESET}")

    def start(self):

        start = True
        while start:
            print(f"{Colors.BLUE}\nWhat do you want to find?{Colors.RESET}")
            print(f"1 - Specific data, through a table index.")
            print(f"2 - All data in a date space.")
            print(f"3 - Number of items in this table.")
            print(f"4 - Return to menu.\n")

            methods = { 1: "search_specific_data", 2: "search_all_data_specific_data", 3: "quantity_data", 4: "exit" }
            op = int(input("Enter the desired option: "))
            option = methods[op]
            method = getattr(self, option, None)

            if op != 3 and op != 4:
                print(f"\n{Colors.YELLOW}**The data creation date must exist and be as CREATED_AT so that the search and conversion can be carried out correctly**{Colors.RESET}\n")

            if option == "search_specific_data": # search_specific_data
                index = input("\nEnter the index: ")
                value = input("\nEnter the value to be found: ")

                print(f"\n{Colors.YELLOW}Performing the search... Please wait a moment{Colors.RESET}\n")
                document = method(index, value) # Usando o def search_specific_data(self, index, value)

                if document:
                    print(f"{Colors.BLUE}Document found: {Colors.RESET}", document, "\n")

                    print("Do you want to extract report?")
                    print(f"{Colors.GREEN}1 - Yes{Colors.RESET}")
                    print(f"{Colors.RED}2 - No{Colors.RESET}\n")
                    extract = input("Type here: ")

                    if extract == "1":
                        self.extract_reports(document)
                    else:
                        print('\nOperation completed!')

                else:
                    print(f"{Colors.YELLOW}No documents found!{Colors.RESET}")
            
            if option == "search_all_data_specific_data": # search_all_data_specific_data
                start = input("\nEnter the start date (Ex: YYYY-MM-DD): ")
                end = input("\nEnter the final date (Ex: YYYY-MM-DD): ")

                # Converter para datetime
                date_start = datetime.strptime(start, "%Y-%m-%d")
                date_end = datetime.strptime(end, "%Y-%m-%d")

                print(f"\n{Colors.YELLOW}Fazendo a busca... Aguarde um instante{Colors.RESET}\n")
                documents = method(date_start, date_end) # Usando o def search_all_data_specific_data(tabela, start, end)

                #documents = list(documents)
                print(f"{Colors.BLUE}Documents found:{Colors.RESET}", documents, "\n")

                if documents:

                    print("Do you want to extract report?")
                    print(f"{Colors.GREEN}1 - Yes{Colors.RESET}")
                    print(f"{Colors.RED}2 - No{Colors.RESET}\n")
                    extract = input("Type here: ")

                    if extract == "1":
                        self.extract_reports(documents)
                    else:
                        print('\nOperation completed!')

                else:
                    print(f"{Colors.YELLOW}No documents found!{Colors.RESET}")

            if option == "quantity_data": # quantity_data

                print(f"\n{Colors.YELLOW}Performing the search... Please wait a moment{Colors.RESET}\n")
                total = method()
                if total:
                    print(f"{Colors.BLUE}Found a total of {Colors.RESET} {total} documents\n")
                else:
                    print(f"{Colors.YELLOW}No documents found!{Colors.RESET}")

            if option == "exit":
                print(f"\n{Colors.YELLOW}Returning to the main menu{Colors.RESET}\n")
                start = False
                self.connection.close()

    def search_specific_data(self, index, value):
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
            print(f"{Colors.RED}Error when searching for specific data: {Colors.RESET}", e)
            return None

    def search_all_data_specific_data(self, start, end):
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
            print(f"{Colors.RED}Error when searching all data for a specific date: {Colors.RESET}", e, "\n")
            return None

    def quantity_data(self):
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
            print(f"{Colors.RED}Error when searching total quantity: {Colors.RESET}", e)
            return None
        
    def close(self):
        self.connection.close()
    
    def extract_reports(self, documents):
        print(f"\n{Colors.GREEN}Generating the EXCEL spreadsheet!{Colors.RESET}\n")
        generate_excel(documents)