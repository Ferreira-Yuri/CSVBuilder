from file_selector import select_file
from column_identifier import read_file, identify_columns
from create_csv import csv_order, select_store
from database import get_products_from_supplier # <-- IMPORTA SUA NOVA FUNÇÃO
import pandas as pd 
def main():
    # 1. Seleciona o arquivo de pedidos
    file_path = select_file()
    if not file_path:
        print("Nenhum arquivo selecionado. Encerrando.")
        return

    # 2. Lê o arquivo Excel (sem cabeçalho)
    df_completo = read_file(file_path)

    # 3. Pega as colunas corretas (A = código, H = quantidade)
    product_col, quantity_col = identify_columns(df_completo)
    df_completo = df_completo[[product_col, quantity_col]]
    df_completo.columns = ["CodigoProduto", "Quantidade"]
    
    # Converte a coluna de código e quantidade para um tipo numérico para garantir a correspondência
    # com os dados do banco. 'coerce' transforma erros em 'NaT' (Not a Number)
    df_completo['CodigoProduto'] = pd.to_numeric(df_completo['CodigoProduto'], errors='coerce')
    df_completo['Quantidade'] = pd.to_numeric(df_completo['Quantidade'], errors='coerce')
    df_completo.dropna(subset=['CodigoProduto', 'Quantidade'], inplace=True) # Remove linhas onde o código não era um número
    df_completo['CodigoProduto'] = df_completo['CodigoProduto'].astype(int) # Garante que seja inteiro

    # 4. Pergunta ao usuário qual fornecedor buscar no banco
    fornecedor_db = input("\nDigite o nome do fornecedor para buscar no banco de dados (ex: INTELBRAS): ")

    # 5. Busca a lista de códigos de produto do fornecedor no banco
    lista_codigos_fornecedor = get_products_from_supplier(fornecedor_db)

    if not lista_codigos_fornecedor:
        print(f"AVISO: Nenhum produto encontrado no banco para '{fornecedor_db}'. Todos os itens do Excel serão tratados como 'OUTROS'.")

    # 6. Filtra o DataFrame do Excel usando a lista de códigos vinda do banco
    df_fornecedor = df_completo[df_completo['CodigoProduto'].isin(lista_codigos_fornecedor)]
    
    # O operador '~' significa 'NÃO'. Pega todos os itens que NÃO estão na lista.
    df_outros = df_completo[~df_completo['CodigoProduto'].isin(lista_codigos_fornecedor)]

    print(f"\nItens do Excel separados:")
    print(f"- {len(df_fornecedor)} itens encontrados que pertencem ao fornecedor '{fornecedor_db}'.")
    print(f"- {len(df_outros)} itens para os demais fornecedores.")

    # 7. Seleciona a filial
    num_store, name_store = select_store()

    # 8. Gera os arquivos para o FORNECEDOR ESPECÍFICO
    csv_order(
        df=df_fornecedor,
        name_store=name_store,
        num_store=num_store,
        prefixo_arquivo=f"FORNECEDOR_{fornecedor_db.replace(' ', '_').upper()}"
    )

    # 9. Gera os arquivos para os DEMAIS FORNECEDORES
    csv_order(
        df=df_outros,
        name_store=name_store,
        num_store=num_store,
        prefixo_arquivo="OUTROS_FORNECEDORES"
    )

    print("\nProcesso finalizado com sucesso!")


if __name__ == "__main__":
    main()