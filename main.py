from mongoDatabase import MongoDatabase
from mysqlDatabase import MysqlDatabase

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

print("---------------------------------------------------------------------------------------------------------------")
print(f"| Olá, seja bem-vindo ao REPORTS DB, seu facilitador de Relatórios para Banco de Dados, como posso te ajudar? |")
print("---------------------------------------------------------------------------------------------------------------")
print(f"1 - {GREEN}Gostaria de gerar relatórios para o MONGODB{RESET}")
print(f"2 - {BLUE}Gostaria de gerar relatórios para o MYSQL{RESET}")
print(f"3 - {PINK}Gostaria de entender os recursos da aplicação{RESET}")

escolha = int(input())

print(f"{GOLD}**Obs: Tenha em vista as permissões de firewall e acessos por meio de Host externos dentro do seu Servidor**")
print(f"**isso pode ocasionar possiveis erros!**{RESET}")

print("")

if escolha == 1:

    print(f"{GREEN}MONGODB selecionado!{RESET}")
    
    print("")
    print("Me informe aqui a uri de acesso do seu banco MONGODB")
    uri = input()

    print("")
    print("Me informe também o database a ser acessado")
    database = input()

    print("")
    print("E a collection que deseja acessar")
    collection = input()

    print("")
    print(f"{GOLD}Aguarde um minuto estamos realizando a conexão...{RESET}")
    mongo = MongoDatabase(uri, database, collection)

    print("")
    print(f"O que você deseja encontrar?")
    print(f"1 - {GREEN}Todos os dados desta tabela{RESET}")
    print(f"2 - {GREEN}O primeiro dado desta tabela{RESET}")
    print(f"3 - {GREEN}Todos os dados de um espaço de datas{RESET}")

    busca = "busca_" + input()
    metodo = getattr(mongo, busca, "Opção inválida")

    print(f"{YELLOW}Fazendo a busca... Aguarde um instante{RESET}")
    print(metodo())

if escolha == 2:
    print("MYSQL selecionado!")
    print(f"{RED}**Atente-se a veracidade do Host, User, Password e Database!**{RESET}")

if escolha == 3:
    print("SOBRE O SITEMA")
