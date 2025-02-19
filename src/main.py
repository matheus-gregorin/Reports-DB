import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from databases.mongoDatabase import MongoDatabase
from databases.mysqlDatabase import MysqlDatabase
from utils.colors import Colors
import time

start = True
while start:
    print(f"{Colors.GOLD}\n---------------------------------------------------------------------------------------------------------------{Colors.RESET}")
    print(f"{Colors.GOLD}| Hi, welcome to REPORTS DB, your Database Reporting facilitator, how can I help you? |{Colors.RESET}")
    print(f"{Colors.GOLD}---------------------------------------------------------------------------------------------------------------{Colors.RESET}")
    print(f"1 - {Colors.GREEN}I would like to extract data from MONGODB.{Colors.RESET}")
    print(f"2 - {Colors.BLUE}I would like to extract data from MYSQL.{Colors.RESET}")
    print(f"3 - {Colors.BLACK}I would like to understand about the application.{Colors.RESET}")
    print(f"4 - {Colors.RED}Exit.{Colors.RESET}\n")

    # option
    choice = input("Enter the desired option: ")

    if choice != "4" and choice != "3":
        print(f"\n{Colors.GOLD}**Obs: Keep in mind firewall permissions and access via external hosts within the provided database server!**")
        print(f"**THIS MAY CAUSE POSSIBLE ERRORS!**{Colors.RESET}\n")

    if choice == "1":
        print(f"{Colors.GREEN}MONGODB select!{Colors.RESET}\n")
        
        uri = input("Tell me the access uri of your MONGODB bank (Connection_string) here: ")
        database = input("\nAlso tell me the database:")
        collection = input("\nAnd the collection you want to extract the data from: ")

        print(f"\n{Colors.GOLD}Wait a minute we are establishing the connection...{Colors.RESET}\n")
        connection = MongoDatabase(uri, database, collection)
        if connection.value is not None:
            connection.start()

    elif choice == "2":
        print(f"{Colors.BLUE}MYSQL select!{Colors.RESET}\n")

        host = input("Tell me the access host for your MYSQL database here: ")
        user = input("\nYour user: ")
        password = input("\nand your password: ")
        database = input("\nAlso let me know the database: ")
        table = input("\nAnd the table you want to extract the data from: ")

        print(f"\n{Colors.GOLD}Wait a minute we are establishing the connection...{Colors.RESET}\n")
        connection = MysqlDatabase(host, user, password, database, table)
        if connection.value is not None:
            connection.start()

    elif choice == "3":

        time.sleep(1)
        print(f"{Colors.GOLD}\nABOUT THE APPLICATION{Colors.RESET}")

        print(
            f"""
        {Colors.BLUE}Our application was developed to simplify and automate the generation of reports in Excel based on predefined queries in the MongoDB and MySQL databases.
            
        Designed to run directly in the terminal, the tool offers a simple and efficient interface, allowing users to execute standard queries and obtain organized reports without the need for manual data manipulation.

        With support for multiple databases, the application is ideal for developers, data analysts and teams that need to extract information quickly, ensuring more productivity and accuracy in data analysis.{Colors.RESET} 🚀"""
        )


        print(f"{Colors.GOLD}\nIf you are interested in finding out more, access our repository on Git Hub. {Colors.RESET}", "https://github.com/matheus-gregorin/Reports-DB")

    elif choice == "4":
        print(f"{Colors.RED}Exit\n{Colors.RESET}", end="", flush=True)
        for _ in range(5):
            time.sleep(0.1)  # Espera 0.5 segundos
            print(f"{Colors.RED}.{Colors.RESET}", end="", flush=True)
        print("\n")

        start = False
