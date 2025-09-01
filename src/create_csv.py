from pathlib import Path
from store_table import store_table
from datetime import date

# Pasta base onde vão ser salvos os arquivos
base_path_save = Path(r'Z:\Yuri Winthor\Abastecimentos\Pedidos_Separados')

def select_store():
    print("Filiais disponíveis:")
    for num, nome in store_table.items():
        print(f"{num} - {nome}")

    while True:
        try:
            num_store = int(input("\nDigite o número da filial do seu pedido: "))
            if num_store in store_table:
                return num_store, store_table[num_store]
            else: 
                print("Número da filial inválido. Tente novamente.")
        except ValueError:
            print("Digite um número válido!")

def get_today_string():
    return date.today().strftime("%Y%m%d")  # formato AAAAMMDD

# Criação dos arquivos segmentados em CSV
def csv_order(df, name_store, num_store):
    # Insere a coluna da filial no início
    df.insert(0, "Filial", num_store)

    # Data de hoje no formato AAAAMMDD
    today = get_today_string()

    # Calcula quantos arquivos vão ser gerados
    num_files = (len(df) // 30) + (1 if len(df) % 30 > 0 else 0)

    # Divide em blocos de 30 linhas
    for i in range(num_files):
        df_segment = df.iloc[i * 30:(i + 1) * 30]

        # Nome do arquivo de saída (vai tudo direto na pasta base)
        name_file = f"{today}_F{num_store}_Sugestão_{i+1}.csv"
        file_path = base_path_save / name_file

        # Salva sem cabeçalho e separado por ";"
        df_segment.to_csv(file_path, index=False, header=False, sep=";")
        print(f"Arquivo salvo: {file_path}")

