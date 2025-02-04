from openpyxl import Workbook
from datetime import datetime
from colors import Colors

# Criar uma planilha Excel
workbook = Workbook()

# Criar uma sheet
sheet = workbook.active

def generate_excel(documents):

        print(f"{Colors.GOLD}Modularizando o arquivo.. {Colors.RESET}\n")

        for indice, document in enumerate(documents):

            # Transforma o Dic de keys em uma lista
            headers = list(document.keys())
            headers.remove('_id')

            # Se fr o primeiro item da lista, insere o cabeçalho
            if indice == 0:
                sheet.append(headers)
            
            values = []
            for header in headers:

                # Valor daquele indíce
                value = document.get(header)

                # Elimina a inserção do _id
                if header != "_id":

                    # Tratamento do created_at
                    if header == "created_at" and isinstance(value, datetime):
                        value = value.strftime("%Y-%m-%d %H:%M:%S")

                    # Tratamento do updated_at
                    if header == "updated_at" and isinstance(value, datetime):
                        value = value.strftime("%Y-%m-%d %H:%M:%S")

                    # Se for array ou dicionário, converte para str
                    if isinstance(value, (list, dict)):
                        value = str(value)
                    
                    values.append(value)


            # Adiciona linha a planilha
            sheet.append(values)

        name = input(f"{Colors.BLUE}Qual o nome do arquivo? {Colors.RESET}\n")
        workbook.save(f"planilhas/{name}.xlsx")
        print(f"{Colors.YELLOW}Finalizado! Planilha salva em: planilhas/{name}.xlsx{Colors.RESET}")