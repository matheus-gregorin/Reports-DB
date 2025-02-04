from mongoDatabase import MongoDatabase
from mysqlDatabase import MysqlDatabase
from colors import Colors

print("---------------------------------------------------------------------------------------------------------------")
print(f"| Olá, seja bem-vindo ao REPORTS DB, seu facilitador de Relatórios para Banco de Dados, como posso te ajudar? |")
print("---------------------------------------------------------------------------------------------------------------")
print(f"1 - {Colors.GREEN}Gostaria de extrair dados do MONGODB.{Colors.RESET}")
print(f"2 - {Colors.BLUE}Gostaria de extrair dados do MYSQL.{Colors.RESET}")
print(f"3 - {Colors.PINK}Gostaria de entender os recursos da aplicação.{Colors.RESET}\n")

# Escolha
choice = input("Digite a opção desejada: ")


print(f"\n{Colors.GOLD}**Obs: Tenha em vista as permissões de firewall e acessos por meio de Host externos dentro do servidor do banco de dados fornecido!**")
print(f"**ISSO PODE OCASIONAR POSSIVEIS ERROS!**{Colors.RESET}\n")

if choice == "1":

    print(f"{Colors.GREEN}MONGODB selecionado!{Colors.RESET}\n")
    
    uri = input("Me informe aqui a uri de acesso do seu banco MONGODB: ")

    database = input("\nMe informe também o database: ")

    collection = input("\nE a collection que deseja extrair os dados: ")

    print(f"\n{Colors.GOLD}Aguarde um minuto estamos estabelecendo a conexão...{Colors.RESET}\n")

    connection = MongoDatabase(uri, database, collection)
    connection.init()

elif choice == "2":
    print("MYSQL selecionado!")
    print(f"{Colors.RED}**Atente-se a veracidade do Host, User, Password e Database!**{Colors.RESET}")

elif choice == "3":
    print("SOBRE O SITEMA")

else:
    print("Opcção inválida")
