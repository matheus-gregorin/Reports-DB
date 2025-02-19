from openpyxl import Workbook
from datetime import datetime
from utils.colors import Colors
import time

def generate_excel(documents, isMongoDB = False):
        
    try:
        # Criar uma planilha Excel
        workbook = Workbook()

        # Criar uma sheet
        sheet = workbook.active

        print(f"{Colors.GOLD}Modularizando o arquivo.. {Colors.RESET}\n")

        if documents:
            for indice, document in enumerate(documents):
                # Transforma o Dic de keys em uma lista
                headers = list(document.keys())

                if isMongoDB:
                    headers.remove('_id')                 

                # Se for o primeiro item da lista, insere o cabeçalho
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
            time.sleep(1)
            workbook.save(f"../docs/{name}.xlsx")
            workbook.close()
            print(f"\n{Colors.YELLOW}Finalizado! Planilha salva em: planilhas/{name}.xlsx{Colors.RESET}")
            return documents
        else:
            print(f"{Colors.GOLD}Lista vazia, não é possivel gerar planilha{Colors.RESET}")
            return None
        
    except Exception as e:
        print(f"{Colors.RED} Erro ao gerar planilha, erro: {e} {Colors.RESET}")