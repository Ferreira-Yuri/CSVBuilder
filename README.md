# CSVBuilder – Segmentador de Pedidos

Este projeto tem como objetivo segmentar planilhas de pedidos em arquivos CSV menores (máx. 30 itens por arquivo), facilitando a importação no sistema da empresa.  

## 🚀 Funcionalidades
- Leitura automática da planilha mais recente na pasta `dados/input/`
- Identificação fixa das colunas:
  - Coluna **A** → Código do Produto  
  - Coluna **H** → Quantidade  
- Segmentação em lotes de até **30 itens**
- Inserção automática do código da filial em cada linha
- Salvamento em `dados/output/<filial>/` com arquivos nomeados sequencialmente

## 📂 Estrutura de Pastas

CSVBuilder/
│
├── dados/
│ ├── input/ # Arquivos de entrada (.xls ou .xlsx)
│ └── output/ # Saída dos CSVs segmentados
│
├── main.py
├── column_identifier.py
├── create_csv.py
├── store_table.py
├── requirements.txt
└── README.md


## ⚙️ Instalação

Clone o repositório e instale as dependências:

```bash
git clone https://github.com/seuusuario/CSVBuilder.git
cd CSVBuilder
pip install -r requirements.txt

▶️ Uso

Coloque o arquivo de pedidos na pasta dados/input/.

Execute o programa: python main.py

Informe o número da filial.

Os arquivos CSV serão gerados em dados/output/<filial>/.
