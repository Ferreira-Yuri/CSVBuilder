from tkinter import Tk, filedialog
import os

input_dir = "Z:\Yuri Winthor\Abastecimentos\Orçamentos_Abastecimento"

def select_file():
    Tk().withdraw()  # esconde a janela principal do Tkinter
    file_path = filedialog.askopenfilename(
        initialdir=input_dir,       # abre direto na pasta padrão
        title="Selecione o arquivo de pedidos",
        filetypes=[("Arquivos Excel", "*.xls *.xlsx")]
    )
    return file_path
