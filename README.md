# 🚀 Gerador de Relatórios em Excel - Terminal App V1

Automatize a extração de dados e a geração de relatórios no terminal!  
Este aplicativo, desenvolvido em **Python**, permite gerar **relatórios em Excel (.xlsx)** a partir de **consultas SQL e MongoDB**, otimizando a análise de dados sem a necessidade de manipulação manual.  

## ✨ **Principais Funcionalidades**

✅ **Conectividade flexível**: Suporte nativo para **MySQL e MongoDB**, com estrutura modular para fácil expansão.  
✅ **Código limpo e escalável**: Arquitetura baseada em **POO e princípios SOLID**, garantindo organização e manutenibilidade.  
✅ **Geração de relatórios otimizada**: Exportação de dados para **Excel** utilizando a biblioteca **openpyxl**.  
✅ **Execução estruturada**: O método `start()` organiza e gerencia o fluxo de execução de forma intuitiva.  
✅ **Alta eficiência**: Aplicação leve que roda diretamente no terminal, consumindo entre **1,3 MB e 1,6 MB** de memória.  
✅ **Testes automatizados**: Inclui testes unitários para validação de módulos e métodos, utilizando o **unittest**, uma ferramenta nativa do Python.

---

<br>

⚠️ Antes de utilizar o aplicativo, certifique-se de que você possui o **Python 3.12 ou superior** instalado em seu sistema.  

Para verificar a versão instalada, execute o comando:

    python --version

<br>

## ⚙️ **Instalação**
1. Clone o repositório:
   ```sh
   git clone https://github.com/seu-usuario/Reports-DB.git
   cd Reports-DB
2. Crie um ambiente virtual:
    ```sh
    python3 -m venv venv
    source venv/bin/activate   # No Windows, use: venv\Scripts\activate
    pip install -r requirements.txt
3. Entre na pasta raiz e rode o app:
    ```sh
    cd /src
    python3 main.py # Ou python
4. Para desativar o ambiente virtual, use:
    ```sh
    deactivate

## ⚙️ **Para testes Unitários**
1. Acesse a pasta de teste:
   ```sh
   cd test
2. Formate o setUp dentro da classe desejada, com as variaveis de teste do seu ambiente:
    ```sh
    # MongoDb:
    uri = ''
    database = ''
    collection = ''

    # Mysql:
    host = ''
    user = ''
    password = ''
    database = ''
    table = ''

3. Rode o comando respectivo da classe de teste:
    ```sh
    # Mongodb:
    python -m unittest testeMongoDatabase.py

    # Mysql:
    python -m unittest testeMysqlDatabase.py