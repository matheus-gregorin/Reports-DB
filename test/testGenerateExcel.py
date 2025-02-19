import unittest
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from utils.reports import generate_excel
from utils.colors import Colors
from datetime import datetime

#  Comando:
#  python -m unittest testGenerateExcel.py

# Criando a classe de teste
class TestGenerateExcel(unittest.TestCase):

    def teste_generate_excel_retorna_none_lista_vazia(self):
        """Testa se o envio de uma lista vazia retorna None"""
        data = generate_excel([])
        self.assertIsNone(data)
        print(f"{Colors.GREEN} ✔ Teste generate_excel retorna None! Retorno: {data} {Colors.RESET}\n")

    def teste_generate_excel_retorna_none_parametro_string(self):
        """Testa se o envio de uma lista vazia retorna None"""
        data = generate_excel("123")
        self.assertIsNone(data)
        print(f"{Colors.GREEN} ✔ Teste generate_excel retorna None! Retorno: {data} {Colors.RESET}\n")

# Executar os testes
if __name__ == '__main__':
    unittest.main()
