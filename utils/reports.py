import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
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

        print(f"{Colors.GOLD}Modularizing the file... {Colors.RESET}\n")

        if documents:
            for index, document in enumerate(documents):
                # Transforma o Dic de keys em uma lista
                headers = list(document.keys())

                if isMongoDB:
                    headers.remove('_id')                 

                # Se for o primeiro item da lista, insere o cabeçalho
                if index == 0:
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

                        # Se for array ou dicionário, converte para str ex: "{addrees:"Rua 1", number: 44}"
                        if isinstance(value, (list, dict)):
                            value = str(value)
                        
                        values.append(value)


                # Adiciona linha a planilha
                sheet.append(values)

            # Obtém o diretório base do projeto (a raiz, subindo a partir de "src")
            base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))

            # Caminho absoluto para salvar na pasta "docs"
            docs_dir = os.path.join(base_dir, "docs")

            # Garante que a pasta "docs" existe
            os.makedirs(docs_dir, exist_ok=True)

            name = input(f"{Colors.BLUE}What is the name of the file? {Colors.RESET}\n")

            # Caminho completo para salvar o arquivo
            file_path = os.path.join(docs_dir, f"{name}.xlsx")

            time.sleep(1)
            workbook.save(file_path)
            workbook.close()
            print(f"\n{Colors.YELLOW}Finished! Spreadsheet saved in: {file_path} {Colors.RESET}")
            return documents
        else:
            print(f"{Colors.GOLD}Empty list, cannot generate spreadsheet.{Colors.RESET}")
            return None
        
    except Exception as e:
        print(f"{Colors.RED} Error generating spreadsheet, error: {e} {Colors.RESET}")