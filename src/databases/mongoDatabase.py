from pymongo import MongoClient
from datetime import datetime
from utils.colors import Colors
from utils.reports import generate_excel
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

            self.value = False
            # Tenta realizar uma consulta simples para garantir que a coleção está funcionando
            document = collection.find_one()
            if document:
                print(f"{Colors.GREEN}Database ok!{Colors.RESET} {db.name}")
                time.sleep(1)
                print(f"{Colors.GREEN}Collection ok!{Colors.RESET} {collection.name}")
                time.sleep(1)
                print(f"{Colors.GREEN}Connection established with MongoDb!{Colors.RESET}")
                time.sleep(1)
                self.value = True
            else:
                time.sleep(1)
                raise ValueError("No documents found in the collection. Canceling operation! Validate the database and inserted table and try again!")

        except ConnectionError as e:
            print(f"{Colors.RED}Error connecting to MongoDB:{Colors.RESET}", f"{Colors.RED}{str(e)}{Colors.RESET}")
            time.sleep(1)
            self.value = None
            client.close()

        except Exception as e:
            print(f"{Colors.RED}Error:{Colors.RESET}", f"{Colors.RED}{str(e)}{Colors.RESET}")
            time.sleep(1)
            self.value = None
            client.close()

    def start (self):

        start = True
        while start:
            print(f"{Colors.GREEN}What do you want to find?{Colors.RESET}")
            print(f"1 - Specific data, through an index.")
            print(f"2 - All data in a date space.")
            print(f"3 - Number of items in this table.")
            print(f"4 - Return to main menu.\n")

            print(f"{Colors.YELLOW}**The data creation date must be CREATED_AT for the conversion to be carried out correctly**{Colors.RESET}\n")

            methods = { 1: "search_specific_data", 2: "search_all_data_specific_data", 3: "quantity_data", 4: "exit" }
            op = int(input("Enter the desired option: "))
            option = methods[op]
            method = getattr(self, option, None)

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
                        self.extract_reports([document])
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

                print(f"\n{Colors.YELLOW}Performing the search... Please wait a moment{Colors.RESET}\n")
                documents = method(date_start, date_end) # Usando o def search_all_data_specific_data(start, end)

                documents = list(documents)
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
                time.sleep(1)
                total = method()

                if total:
                    print(f"{Colors.BLUE}Found a total of {Colors.RESET} {total} documents")
                else:
                    print(f"{Colors.YELLOW}No documents found!{Colors.RESET}")

            if option == "exit":
                print(f"\n{Colors.YELLOW}Return to main menu{Colors.RESET}")
                start = False
                self.client.close()

    def search_specific_data(self, index, value):
        try:
            document = self.collection.find_one({
                index: value
            })
            if document:
                return document
            else:
                return None
        except Exception as e:
            print(f"{Colors.RED}Error when searching for specific data: {Colors.RESET}", e)
            return None

    def search_all_data_specific_data(self, start, end):
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
            print(f"{Colors.RED}Error when searching all data for a specific date: {Colors.RESET}", e, "\n")
            return None

    def quantity_data(self):
        try:
            documents = self.collection.count_documents({})
            if documents:
                return documents
            else:
                return None
        except Exception as e:
            print(f"{Colors.RED}Error when searching total quantity: {Colors.RESET}", e)
            return None

    def close(self):
        self.client.close()
    
    def extract_reports(self, documents):
        print(f"\n{Colors.GREEN}Generating the EXCEL spreadsheet!{Colors.RESET}\n")
        generate_excel(documents, True)