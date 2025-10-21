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

# Criação dos arquivos segmentados em CSV (FUNÇÃO MODIFICADA)
def csv_order(df, name_store, num_store, prefixo_arquivo=""):
    # Se o dataframe estiver vazio, avisa e não faz nada
    if df.empty:
        print(f"\nNenhum item para processar no grupo '{prefixo_arquivo}'.")
        return

    df_copy = df.copy()
    df_copy.insert(0, "Filial", num_store)
    
    today = get_today_string()
    
    num_files = (len(df_copy) // 30) + (1 if len(df_copy) % 30 > 0 else 0)

    print(f"\nGerando {num_files} arquivo(s) para o grupo '{prefixo_arquivo}'...")

    for i in range(num_files):
        df_segment = df_copy.iloc[i * 30:(i + 1) * 30]

        # Adiciona o prefixo no nome do arquivo, se ele existir
        if prefixo_arquivo:
            name_file = f"{today}_F{num_store}_{prefixo_arquivo}_Sugestão_{i+1}.csv"
        else:
            name_file = f"{today}_F{num_store}_Sugestão_{i+1}.csv"
        
        file_path = base_path_save / name_file

        df_segment.to_csv(file_path, index=False, header=False, sep=";")
        print(f"Arquivo salvo: {file_path}")