import cx_Oracle as ora  # Mantenho o 'ora' como apelido, mas o pacote instalado deve ser 'python-oracledb'
import os
import sys

# ***************************************************************
# 1. CONFIGURAÇÃO DO ORACLE INSTANT CLIENT
# ***************************************************************

# Atenção: Este caminho deve ser o da pasta que contém a 'oci.dll'
INSTANT_CLIENT_PATH = r"C:\Users\DTS DISTRIBUIDORA\instantclient-basic-windows.x64-19.28.0.0.0dbru\instantclient_19_28" 

# Tenta inicializar o cliente Oracle usando a função moderna.
# Isso é crucial para resolver o erro DPI-1047.
try:
    # A função correta para pacotes recentes (python-oracledb) é init_oracle_client
    ora.init_oracle_client(lib_dir=INSTANT_CLIENT_PATH)
    print("STATUS: Oracle Client inicializado com sucesso.")
except AttributeError:
    # Captura o erro se a função init_oracle_client não existir (pacote muito antigo)
    print("AVISO: Usando a função obsoleta 'init_client'. Por favor, atualize o pacote 'cx_Oracle' para 'python-oracledb'.")
    try:
        # Tenta a função obsoleta, caso o pacote seja o antigo cx_Oracle
        ora.init_client(lib_dir=INSTANT_CLIENT_PATH)
        print("STATUS: Oracle Client (método obsoleto) inicializado com sucesso.")
    except Exception as e:
        print(f"ERRO FATAL: Falha ao inicializar o cliente Oracle com ambos os métodos. Detalhes: {e}")
        # Encerra o programa se a inicialização for crítica
        sys.exit(1) # Sai com código de erro
except Exception as e:
    # Captura qualquer outro erro, como a falha ao encontrar o caminho (DPI-1047 reaparecendo)
    print(f"ERRO FATAL: Falha ao inicializar o cliente Oracle. Verifique o CAMINHO ou VERSÃO. Detalhes: {e}")
    sys.exit(1) # Sai com código de erro


# ***************************************************************
# 2. DETALHES DA CONEXÃO
# ***************************************************************

DB_HOST = "192.168.2.3"
DB_PORT = "1521"
DB_SERVICE_NAME = "WINT"
DB_USER = "systock"
DB_PASSWORD = "wsystock01"

# Cria a string de conexão (Data Source Name)
DB_DSN = ora.makedsn(DB_HOST, DB_PORT, DB_SERVICE_NAME)


# ***************************************************************
# 3. FUNÇÃO DE CONEXÃO
# ***************************************************************

def connectOracle():
    """Tenta criar e retorna uma conexão com o banco de dados. Retorna None em caso de falha."""
    conn = None
    try:
        # Tenta conectar
        conn = ora.connect(DB_USER, DB_PASSWORD, DB_DSN)
        print("STATUS: Conexão com o Banco de Dados estabelecida com sucesso.")
        return conn
    except ora.DatabaseError as e:
        # Se a conexão falhar (problema de rede, credenciais, listener, etc.)
        error, = e.args
        print(f"\nERRO DE CONEXÃO ({error.code}): Falha ao conectar ao banco.")
        print(f"Mensagem do Oracle: {error.message}")
        return None
    except Exception as e:
        # Outros erros inesperados
        print(f"ERRO INESPERADO ao tentar conectar: {e}")
        return None
# (Cole isso no final do seu arquivo database.py, depois da função connectOracle)

def get_products_from_supplier(supplier_name):
    """
    Executa a query para buscar todos os códigos de produto de um fornecedor.
    Retorna uma lista de códigos.
    """
    # Conecta ao banco usando sua função já existente
    oraconnect = connectOracle()

    # Se a conexão falhar, retorna uma lista vazia
    if oraconnect is None:
        print("ERRO: Não foi possível buscar produtos. A conexão com o banco falhou.")
        return []

    # Adapta o nome do fornecedor para usar na cláusula LIKE
    supplier_pattern = f"{supplier_name.upper()}%"

    sql_query = """
        SELECT DISTINCT
            PCEST.CODPROD
        FROM
            PCEST
        INNER JOIN
            PCPRODUT ON PCEST.CODPROD = PCPRODUT.CODPROD
        INNER JOIN
            PCFORNEC ON PCPRODUT.CODFORNEC = PCFORNEC.CODFORNEC
        WHERE
            PCFORNEC.FORNECEDOR LIKE :supplier_pattern
    """
    
    product_codes = []
    cursor = None # Inicializa o cursor como None
    
    try:
        cursor = oraconnect.cursor()
        # Executa a query passando o padrão do fornecedor como parâmetro
        cursor.execute(sql_query, supplier_pattern=supplier_pattern)
        
        # Pega todos os resultados e transforma em uma lista de códigos
        for row in cursor:
            product_codes.append(row[0]) # row[0] é a primeira coluna (CODPROD)
            
        print(f"Banco de dados: Encontrados {len(product_codes)} códigos de produto para o fornecedor '{supplier_name}'.")

    except ora.Error as e:
        print(f"ERRO ao executar a consulta de fornecedor: {e}")
    finally:
        # Garante que o cursor e a conexão sejam sempre fechados
        if cursor:
            cursor.close()
        if oraconnect:
            oraconnect.close()
            print("STATUS: Conexão com o banco de dados fechada.")
            
    return product_codes