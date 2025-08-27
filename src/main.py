from file_selector import select_file
from column_identifier import read_file, identify_columns
from create_csv import csv_order, select_store

def main():
    # 1. Seleciona o arquivo de pedidos
    file_path = select_file()
    if not file_path:
        print("Nenhum arquivo selecionado. Encerrando.")
        return

    # 2. Lê o arquivo Excel (sem cabeçalho)
    df = read_file(file_path)

    # 3. Pega as colunas corretas (A = código, H = quantidade)
    product_col, quantity_col = identify_columns(df)
    df = df[[product_col, quantity_col]]
    df.columns = ["CodigoProduto", "Quantidade"]

    # 4. Seleciona filial
    num_store, name_store = select_store()

    # 5. Gera os arquivos segmentados
    csv_order(df, name_store, num_store)

if __name__ == "__main__":
    main()
