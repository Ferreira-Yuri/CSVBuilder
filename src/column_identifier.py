import pandas as pd

def read_file(file):
    """
    Lê o arquivo Excel sem cabeçalho.
    """
    df = pd.read_excel(file, header=None) 

    print("Planilha carregada, total de linhas:", len(df))
    return df

def identify_columns(df):
    """
    Identifica colunas fixas no novo formato:
    Coluna A (índice 0) = Código do Produto
    Coluna H (índice 7) = Quantidade
    """
    try:
        product_col = df.columns[0]   # Coluna A
        quantity_col = df.columns[7]  # Coluna H
    except IndexError:
        raise ValueError("O arquivo não contém as colunas esperadas (A e H).")

    return product_col, quantity_col
