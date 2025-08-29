from pathlib import Path
from store_table import store_table

# Pasta base onde vão ser salvos os arquivos
base_path_save = Path('Z:\Yuri Winthor\Abastecimentos\Pedidos_Separados')

# Seleciona a filial do pedido a ser segmentado
def select_store():
    while True:
        try:
            num_store = int(input("Digite o número da filial do seu pedido: "))
            if num_store in store_table:
                name_store = store_table[num_store]
                return num_store, name_store
            else: 
                print("Número da filial inválido. Tente novamente.")
        except ValueError:
            print("Digite um número válido!")

# Criação dos arquivos segmentados em CSV
def csv_order(df, name_store, num_store):
    # Insere a coluna da filial no início
    df.insert(0, "Filial", num_store)

    # Garante que existe uma pasta específica para a filial
    path_save = base_path_save / f"{num_store:02}_{name_store}"
    path_save.mkdir(parents=True, exist_ok=True)

    # Calcula quantos arquivos vão ser gerados
    num_files = (len(df) // 30) + (1 if len(df) % 30 > 0 else 0)

    # Divide em blocos de 30 linhas
    for i in range(num_files):
        df_segment = df.iloc[i * 30:(i + 1) * 30]

        # Nome do arquivo de saída
        name_file = f"20250829_{name_store}_{i+1}.csv"
        file_path = path_save / name_file

        # Salva sem cabeçalho e separado por ";"
        df_segment.to_csv(file_path, index=False, header=False, sep=";")
        print(f"Arquivo salvo: {file_path}")
