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
    print(f"{Colors.GOLD}| Olá, seja bem-vindo ao REPORTS DB, seu facilitador de Relatórios para Banco de Dados, como posso te ajudar? |{Colors.RESET}")
    print(f"{Colors.GOLD}---------------------------------------------------------------------------------------------------------------{Colors.RESET}")
    print(f"1 - {Colors.GREEN}Gostaria de extrair dados do MONGODB.{Colors.RESET}")
    print(f"2 - {Colors.BLUE}Gostaria de extrair dados do MYSQL.{Colors.RESET}")
    print(f"3 - {Colors.BLACK}Gostaria de entender os recursos da aplicação.{Colors.RESET}")
    print(f"4 - {Colors.RED}Sair{Colors.RESET}\n")

    # opção
    choice = input("Digite a opção desejada: ")

    if choice != "4" and choice != "3":
        print(f"\n{Colors.GOLD}**Obs: Tenha em vista as permissões de firewall e acessos por meio de Host externos dentro do servidor do banco de dados fornecido!**")
        print(f"**ISSO PODE OCASIONAR POSSIVEIS ERROS!**{Colors.RESET}\n")

    if choice == "1":
        print(f"{Colors.GREEN}MONGODB selecionado!{Colors.RESET}\n")
        
        uri = input("Me informe aqui a uri de acesso do seu banco MONGODB (Connection_string): ")
        database = input("\nMe informe também o database: ")
        collection = input("\nE a collection que deseja extrair os dados: ")

        print(f"\n{Colors.GOLD}Aguarde um minuto estamos estabelecendo a conexão...{Colors.RESET}\n")
        connection = MongoDatabase(uri, database, collection)
        if connection.value is not None:
            connection.start()

    elif choice == "2":
        print(f"{Colors.BLUE}MYSQL selecionado!{Colors.RESET}\n")

        host = input("Me informe aqui o host de acesso do seu banco MYSQL: ")
        user = input("\nO user: ")
        password = input("\nE o password: ")
        database = input("\nMe informe também o database: ")
        table = input("\nE a tabela que deseja extrair os dados: ")

        print(f"\n{Colors.GOLD}Aguarde um minuto estamos estabelecendo a conexão...{Colors.RESET}\n")
        connection = MysqlDatabase(host, user, password, database, table)
        if connection.value is not None:
            connection.start()

    elif choice == "3":

        print(f"{Colors.GOLD}\nSOBRE A APLICAÇÃO{Colors.RESET}")

        print(
            f"""
        {Colors.BLUE}Nossa aplicação foi desenvolvida para simplificar e automatizar a geração de relatórios em Excel a partir de consultas predefinidas nos bancos de dados MongoDB e MySQL.
            
        Projetada para rodar diretamente no terminal, a ferramenta oferece uma interface simples e eficiente, permitindo que usuários executem queries padrão e obtenham relatórios organizados sem a necessidade de manipulação manual dos dados.

        Com suporte a múltiplos bancos de dados, a aplicação é ideal para desenvolvedores, analistas de dados e equipes que precisam extrair informações rapidamente, garantindo mais produtividade e precisão na análise de dados.{Colors.RESET} 🚀"""
        )


        print(f"{Colors.GOLD}\nCaso tenha interesse em saber mais, acesse o nosso repositório no Git Hub. {Colors.RESET}", "https://github.com/matheus-gregorin/Reports-DB")

    elif choice == "4":
        print(f"{Colors.RED}\nEncerrando\n{Colors.RESET}", end="", flush=True)
        for _ in range(5):
            time.sleep(0.1)  # Espera 0.5 segundos
            print(f"{Colors.RED}.{Colors.RESET}", end="", flush=True)
        print("\n")

        start = False
